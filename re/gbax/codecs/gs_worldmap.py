"""Golden Sun world map (GS1 area 1 / room 2, GS2 world map) decoder and exporter.

The world map is not a normal field map. It is a mode-2 affine scene (two rotated/tilted 8bpp backgrounds) fed
from a chunk table. Format (see notes/gs_worldmap.md for evidence and addresses):

* chunk table file (GS1 0xD4, GS2 0x197): u32 offsets from the file start, one per 256x256 px chunk and layer.
  GS1 16x20 chunks (offset table 2 x 320 words), GS2 32x32 chunks (2 x 1024 words). Layer 0 (back, BG3) first,
  then layer 1 (front, BG2). An offset of 0 (GS2 only) is an empty chunk (zero-filled buffer).
* each chunk: byte-LZ body (the format-1 coding without its format byte), 0x400 bytes = 16x16 cells x u32:
  bits 0-15 metatile id, bits 16-23 event id (0 = none, GS2 0xFF = solid), bits 24-30 (GS1) / 24-29 (GS2)
  region "kind", bit 31 a terrain flag (GS2 bit 30 unused here). Only layer 0 carries event/kind/flag.
* metatile file (GS1 0xD5, GS2 0x198): 4 bytes per metatile = 8bpp tile numbers TL, TR, BL, BR.
* graphics variant (palette, 4 x 8 KB 8bpp tile banks; GS2 also collision + animation) chosen by the kind of
  the cell under the player: GS1 kind 21 -> variant 1 else 0; GS2 kind//10: 2 -> 2, 3 -> 3, 4 -> 1, else 0.
  Back layer uses banks 0-1 (VRAM 0x06008000), front layer banks 2-3 (0x0600C000).
* terrain class: per 8x8 tile, 4x4 nibbles (8 bytes) from the collision file (GS1 0xD7, GS2 per variant):
  bytes 0-0x7FF back layer, 0x800-0xFFF front layer. Front wins if non-zero, then back, else class 7.

World positions (the 16.16 values the game moves) are 2 world units per output pixel.

Usage:
    .venv\\Scripts\\python.exe -m gbax.codecs.gs_worldmap <rom.gba> [--out DIR] [--no-tmj]
"""
import argparse
import collections
import json
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from .golden_sun import decode_format1
from .gs_maps import GsMaps, bgr555_to_rgb

GAMES = {
    1: dict(
        chunk_table=0xD4, metatiles=0xD5, chunks=(16, 20), kind_mask=0x7F,
        variant_table=0x080132CC, variant_fields=("palette", "bank0", "bank1", "bank2", "bank3", "layer_data"),
        n_variants=2, shared={"animation": 0xD6, "collision": 0xD7},
        behavior_table=0x0801353C, behavior_groups=3,
        rules={"foot": 0x0809D7A8}, encounter_table=0x0809C610, room=2,
    ),
    2: dict(
        chunk_table=0x197, metatiles=0x198, chunks=(32, 32), kind_mask=0x3F,
        variant_table=0x0802ED34,
        variant_fields=("palette", "animation", "collision", "bank0", "bank1", "bank2", "bank3",
                        "anim_bank0", "anim_bank1"),
        n_variants=4, shared={"misc_0x199": 0x199},
        behavior_table=0x0802F004, behavior_groups=5,
        rules={"foot": 0x080EEDBC, "ship": 0x080EEF34}, encounter_table=0x080EDACC, room=2,
    ),
}

# Movement facts gathered from code (addresses in notes/gs_worldmap.md); px/frame in world units (2 per image px).
MOVEMENT = {
    1: {"controller": "0x0800F2F8", "walk": 0.5, "walk_accel": 0.25, "run": 1.0, "run_accel": 1.25,
        "walkable_classes": list(range(5, 13)), "probe_px": 7},
    2: {"controllers": {"foot_0x080279B0": [0.5, 0.25, 1.0, 0.5], "foot_0x0802A124": [0.5, 0.25],
                        "candidate_ship_0x08028534": [1.25, 0.5]},
        "foot_classes": list(range(5, 13)),
        "ship_surface_classes": [1, 2, 3, 4, 6],
        "ship_raised_classes_by_mode": {"0": [1, 2, 3, 4, 5, 6], "1": list(range(1, 9)),
                                        "2": list(range(1, 9)) + [10], "other": [4, 5, 6, 7, 8, 10]},
        "solid_event_id": 255},
}


def u32(d, o):
    return struct.unpack_from("<I", d, o)[0]


def lz_body(d, addr, limit=0x8000):
    """Byte-LZ data without a format byte (the game's Resource_DecodeByteLz)."""
    return decode_format1(b"\x01" + bytes(d[addr:addr + limit]), 0)[0]


def variant_of(gs, kind):
    """Graphics variant for a cell kind (numpy array)."""
    if gs == 1:
        return (kind == 21).astype(np.int64)
    q = kind // 10
    return np.select([q == 3, q == 2, q == 4], [3, 2, 1], 0).astype(np.int64)


def behavior_group(gs, kind, flag31):
    g = np.where(flag31, 0x10, 0)
    if gs == 1:
        return np.where(kind == 21, 0x20, g)
    g = np.where(kind > 40, 0x20, g)
    g = np.where(kind == 36, 0x40, g)
    return np.where((kind == 12) | (kind == 15), 0x30, g)


def encounter_region(gs, kind):
    return kind if gs == 1 else kind % 20


class WorldMap:
    def __init__(self, rom_path):
        self.gm = GsMaps(rom_path)
        self.d = self.gm.d
        self.gs = self.gm.gs
        self.cfg = GAMES[self.gs]
        self.workspace = Path(self.gm.rom.workspace)

    # ---------------------------------------------------------------- data
    def load(self):
        c, d, gm = self.cfg, self.d, self.gm
        cw, ch = c["chunks"]
        base = gm.file_addr(c["chunk_table"])
        n = cw * ch
        self.words = np.zeros((2, ch * 16, cw * 16), np.uint32)
        self.empty_chunks = [0, 0]
        for layer in range(2):
            for i in range(n):
                off = u32(d, base + 4 * (layer * n + i))
                if off == 0:
                    self.empty_chunks[layer] += 1
                    continue
                raw = lz_body(d, base + off)
                assert len(raw) == 0x400, (layer, i, len(raw))
                cy, cx = divmod(i, cw)
                self.words[layer, cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16] = \
                    np.frombuffer(raw, "<u4").reshape(16, 16)
        w0 = self.words[0]
        self.mt = (self.words & 0xFFFF).astype(np.int64)
        self.event = ((self.words >> 16) & 0xFF).astype(np.int64)
        self.kind = ((w0 >> 24) & c["kind_mask"]).astype(np.int64)
        self.flag31 = (w0 >> 31).astype(bool)
        self.flag30 = ((w0 >> 30) & 1).astype(bool) if self.gs == 2 else np.zeros_like(self.flag31)
        self.var = variant_of(self.gs, self.kind)
        self.metatiles = np.frombuffer(gm.decode_file(c["metatiles"]), np.uint8)
        self.metatiles = self.metatiles[: len(self.metatiles) // 4 * 4].reshape(-1, 4)
        # variants
        vt = c["variant_table"] & 0x1FFFFFF
        k = len(c["variant_fields"])
        self.variants = []
        for v in range(c["n_variants"]):
            files = {f: u32(d, vt + 4 * (v * k + j)) for j, f in enumerate(c["variant_fields"])}
            pal = lz_body(d, gm.file_addr(files["palette"]))
            pal = bgr555_to_rgb(struct.unpack_from("<%dH" % (len(pal) // 2), pal))
            banks = [gm.decode_file(files["bank%d" % b]) for b in range(4)]
            coll = gm.decode_file(files["collision"] if "collision" in files else c["shared"]["collision"])
            self.variants.append(dict(files=files, palette=pal, banks=banks, collision=coll))
        self.behavior = list(d[c["behavior_table"] & 0x1FFFFFF:(c["behavior_table"] & 0x1FFFFFF) + 16 * c["behavior_groups"]])

    # ---------------------------------------------------------------- render
    def metatile_stack(self, v, layer):
        b = self.variants[v]["banks"]
        tiles = np.frombuffer(b[2 * layer] + b[2 * layer + 1], np.uint8).reshape(256, 8, 8)
        m = self.metatiles
        out = np.zeros((len(m), 16, 16), np.uint8)
        out[:, :8, :8], out[:, :8, 8:] = tiles[m[:, 0]], tiles[m[:, 1]]
        out[:, 8:, :8], out[:, 8:, 8:] = tiles[m[:, 2]], tiles[m[:, 3]]
        return out

    def index_image(self, layer):
        """8bpp colour index per pixel for one layer (0 = transparent)."""
        nmt = len(self.metatiles)
        mt = np.minimum(self.mt[layer], nmt - 1)
        hc, wc = mt.shape
        out = np.zeros((hc, wc, 16, 16), np.uint8)
        for v in range(len(self.variants)):
            sel = self.var == v
            if sel.any():
                out[sel] = self.metatile_stack(v, layer)[mt[sel]]
        return out.transpose(0, 2, 1, 3).reshape(hc * 16, wc * 16)

    def rgba(self, idx):
        h, w = idx.shape
        var_px = np.repeat(np.repeat(self.var, 16, 0), 16, 1)
        out = np.zeros((h, w, 4), np.uint8)
        for v, V in enumerate(self.variants):
            pal = np.zeros((256, 4), np.uint8)
            pal[:len(V["palette"]), :3] = np.array(V["palette"], np.uint8)
            pal[1:, 3] = 255
            sel = var_px == v
            out[sel] = pal[idx[sel]]
        return out

    def terrain_classes(self):
        """Terrain class per 2x2 px sample (the game's GetWorldMapCollision), shape (H/2, W/2)."""
        nmt = len(self.metatiles)
        hc, wc = self.var.shape
        var_t = np.repeat(np.repeat(self.var, 2, 0), 2, 1)
        result = []
        for layer in range(2):
            mt = np.minimum(self.mt[layer], nmt - 1)
            t = self.metatiles[mt].reshape(hc, wc, 2, 2).transpose(0, 2, 1, 3).reshape(hc * 2, wc * 2)
            cls = np.zeros((hc * 2, wc * 2, 4, 4), np.uint8)
            for v, V in enumerate(self.variants):
                raw = np.frombuffer(V["collision"][layer * 0x800:(layer + 1) * 0x800], np.uint8).reshape(256, 4, 2)
                lut = np.zeros((256, 4, 4), np.uint8)
                for c in range(4):
                    b = raw[:, :, c >> 1]
                    lut[:, :, c] = (b >> 4) if c & 1 else (b & 15)
                sel = var_t == v
                cls[sel] = lut[t[sel]]
            result.append(cls.transpose(0, 2, 1, 3).reshape(hc * 8, wc * 8))
        back, front = result
        return np.where(front != 0, front, np.where(back != 0, back, 7)).astype(np.uint8)

    # ---------------------------------------------------------------- tables
    def rules(self):
        out = {}
        for name, addr in self.cfg["rules"].items():
            rows, a = [], addr & 0x1FFFFFF
            while True:
                r = struct.unpack_from("<4h", self.d, a)
                if r[0] == -1:
                    break
                rows.append({"region": r[0], "key": r[1], "flag_clear": None if r[2] == -1 else r[2], "zone": r[3]})
                a += 8
            out[name] = rows
        return out

    def zone(self, z):
        a = (self.cfg["encounter_table"] & 0x1FFFFFF) + 0x1C * z
        rate, level = struct.unpack_from("<2H", self.d, a)
        groups = list(struct.unpack_from("<8H", self.d, a + 4))
        weights = list(self.d[a + 20:a + 28])
        return {"zone": z, "rate": rate, "target_level": level,
                "groups": [{"group": g, "weight": w} for g, w in zip(groups, weights) if w]}

    def room_tables(self):
        """Entrances / warps / events of the world-map room, from the gs_maps export (if present)."""
        p = self.workspace / "maps" / "rooms" / ("room_%03d" % self.cfg["room"]) / "events.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    def room_names(self):
        p = self.workspace / "maps" / "index.json"
        names = {}
        if not p.exists():
            return names

        def walk(o):
            if isinstance(o, dict):
                if isinstance(o.get("room"), int) and isinstance(o.get("name"), str) and o["room"] not in names:
                    names[o["room"]] = o["name"]
                for x in o.values():
                    walk(x)
            elif isinstance(o, list):
                for x in o:
                    walk(x)
        walk(json.loads(p.read_text(encoding="utf-8")))
        return names


# -------------------------------------------------------------------- export helpers
def runs(mask_ids, skip=(0,)):
    """Row runs of equal ids, merged vertically when identical. Returns [(id, x0, y0, w, h)] in cells."""
    h, w = mask_ids.shape
    rects, open_ = [], {}
    for y in range(h):
        row, cur = mask_ids[y], {}
        x = 0
        while x < w:
            v = int(row[x])
            if v in skip:
                x += 1
                continue
            x1 = x
            while x1 < w and row[x1] == v:
                x1 += 1
            key = (v, x, x1 - x)
            if key in open_:
                r = open_.pop(key)
                r[4] += 1
                cur[key] = r
            else:
                cur[key] = [v, x, y, x1 - x, 1]
            x = x1
        rects += open_.values()
        open_ = cur
    rects += open_.values()
    return [tuple(r) for r in rects]


TERRAIN_COLOURS = [(0, 0, 0), (10, 30, 120), (20, 60, 170), (40, 100, 210), (80, 170, 230), (110, 190, 80),
                   (210, 200, 120), (60, 150, 60), (150, 120, 70), (20, 90, 30), (190, 170, 110), (130, 130, 130),
                   (230, 230, 230), (90, 60, 40), (200, 60, 60), (255, 0, 255)]


def export(rom_path, out=None, tmj=True):
    wm = WorldMap(rom_path)
    wm.load()
    gs, cfg = wm.gs, wm.cfg
    out = Path(out) if out else wm.workspace / "worldmap"
    out.mkdir(parents=True, exist_ok=True)
    hc, wc = wm.var.shape
    W, H = wc * 16, hc * 16
    log = []

    idx = [wm.index_image(0), wm.index_image(1)]
    layers = [wm.rgba(i) for i in idx]
    Image.fromarray(layers[0], "RGBA").save(out / "layer_back.png", optimize=True)
    Image.fromarray(layers[1], "RGBA").save(out / "layer_front.png", optimize=True)
    comp = Image.fromarray(layers[0], "RGBA")
    comp.alpha_composite(Image.fromarray(layers[1], "RGBA"))
    bg = Image.new("RGBA", comp.size, (0, 0, 0, 255))
    bg.alpha_composite(comp)
    bg.convert("RGB").save(out / "composite.png", optimize=True)
    bg.convert("RGB").resize((W // 4, H // 4), Image.BOX).save(out / "composite_quarter.png")

    cls = wm.terrain_classes()
    Image.fromarray(cls, "L").save(out / "terrain_classes.png", optimize=True)
    prev = np.array(TERRAIN_COLOURS, np.uint8)[cls]
    Image.fromarray(prev, "RGB").save(out / "terrain_preview.png", optimize=True)
    class_hist = {int(k): int(v) for k, v in zip(*np.unique(cls, return_counts=True))}

    for name, arr in (("regions.png", wm.kind), ("events.png", wm.event[0])):
        Image.fromarray(arr.astype(np.uint8), "L").save(out / name, optimize=True)

    # ---------------- tables
    room = wm.room_tables()
    names = wm.room_names()
    warps = {w["event"]: w for w in (room or {}).get("warps", [])}
    handlers = collections.defaultdict(list)
    for e in (room or {}).get("events", []):
        handlers[e["id"]].append(e)

    events = []
    for layer in range(2):
        for ev, x, y, w, h in runs(wm.event[layer]):
            o = {"layer": layer, "event_id": ev, "cell_rect": [x, y, w, h], "px_rect": [x * 16, y * 16, w * 16, h * 16],
                 "region": int(wm.kind[y, x])}
            if ev == 255 and gs == 2:
                o["solid"] = True
            if ev in warps:
                o["to_room"], o["to_door"] = warps[ev]["to_room"], warps[ev]["to_door"]
                o["to_name"] = names.get(warps[ev]["to_room"])
            hs = [h_ for h_ in handlers.get(ev, []) if h_.get("type", 0) & 0xF == 2]
            if hs:
                o["handlers"] = [{"script": h_.get("script"), "flag": h_.get("flag")} for h_ in hs]
            events.append(o)
    cell_ids = sorted({o["event_id"] for o in events if not o.get("solid")})
    matched = [e for e in cell_ids if e in warps or e in handlers]
    log.append("event ids on cells: %d, with a warp or handler in room %d: %d" % (len(cell_ids), cfg["room"], len(matched)))

    entrances = []
    for e in (room or {}).get("entrances", []):
        px, pz = e["x"] / 2, e["z"] / 2
        cx, cy = int(px // 16), int(pz // 16)
        inside = 0 <= cx < wc and 0 <= cy < hc
        entrances.append({"id": e["id"], "px": [px, pz], "world": [e["x"], e["y"], e["z"]], "angle": e["angle"],
                          "cell": [cx, cy], "terrain_class": int(cls[int(pz // 2), int(px // 2)]) if inside else None,
                          "region": int(wm.kind[cy, cx]) if inside else None})
    # verification: entrances should sit next to event cells (towns) -> distance in px to nearest event cell
    ev_cells = np.argwhere((wm.event[0] != 0) & (wm.event[0] != 255))
    if len(ev_cells) and entrances:
        cent = ev_cells[:, ::-1] * 16 + 8
        dists = [float(np.min(np.hypot(*(cent - np.array(e["px"])).T))) for e in entrances]
        log.append("entrance -> nearest event cell distance px: median %.1f, <=48px: %d/%d"
                   % (float(np.median(dists)), sum(x <= 48 for x in dists), len(dists)))
        walk = set(MOVEMENT[gs].get("walkable_classes", MOVEMENT[gs].get("foot_classes")))
        log.append("entrances on walkable class: %d/%d" % (sum(e["terrain_class"] in walk for e in entrances), len(entrances)))

    # town/landmark icons are placed actors; entry happens on actor contact (alchemy MapActor_UpdateContact)
    actors = []
    for a in (room or {}).get("actors", []):
        x, y, z = a.get("x", 0), a.get("y", 0), a.get("z", 0)
        actors.append({"index": a.get("index"), "slot": a.get("slot"), "sprite": a.get("sprite"),
                       "px": [x / 2, z / 2] if (x or z) else None, "world": [x, y, z],
                       "condition": a.get("condition"), "behavior": a.get("behavior"),
                       "talk_events": a.get("talk_events")})
    log.append("actors: %d, with a static position: %d" % (len(actors), sum(a["px"] is not None for a in actors)))

    rules = wm.rules()
    zones = sorted({r["zone"] for rs in rules.values() for r in rs})
    groups = wm.behavior
    key_classes = {}
    for g in range(cfg["behavior_groups"]):
        for cl in range(16):
            key_classes.setdefault(groups[g * 16 + cl], set()).add((g * 16, cl))
    region_ids, region_counts = np.unique(wm.kind, return_counts=True)
    regions = []
    for k, n in zip(region_ids.tolist(), region_counts.tolist()):
        sel = wm.kind == k
        er = int(encounter_region(gs, k))
        r = {"kind": k, "cells": n, "variant": int(variant_of(gs, np.array([k]))[0]), "encounter_region": er,
             "behavior_groups": sorted({int(x) for x in np.unique(behavior_group(gs, wm.kind[sel], wm.flag31[sel]))}),
             "rules": {m: [x for x in rs if x["region"] == er] for m, rs in rules.items()},
             "warps_inside": sorted({names.get(o["to_room"], str(o["to_room"])) for o in events
                                     if o["region"] == k and "to_room" in o})}
        ys, xs = np.nonzero(sel)
        r["cell_bbox"] = [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]
        regions.append(r)

    spec = {
        "game": "GS%d" % gs, "rom": Path(rom_path).name,
        "size_px": [W, H], "cells": [wc, hc], "cell_px": 16, "chunks": list(cfg["chunks"]), "chunk_px": 256,
        "world_units_per_px": 2,
        "files": {"chunk_table": cfg["chunk_table"], "metatiles": cfg["metatiles"], **cfg["shared"]},
        "metatile_count": int(len(wm.metatiles)),
        "empty_chunks": wm.empty_chunks,
        "variants": [{"files": V["files"], "colours": len(V["palette"])} for V in wm.variants],
        "cell_format": {"bits_0_15": "metatile", "bits_16_23": "event id (0 none%s)" % (", 255 solid" if gs == 2 else ""),
                        "bits_24_%d" % (30 if gs == 1 else 29): "region kind", "bit_31": "terrain flag (behaviour group 0x10)"},
        "terrain": {"sample_px": 2, "default_class": 7, "class_histogram": class_hist,
                    "behavior_table": {"address": hex(cfg["behavior_table"]),
                                       "groups": {hex(g * 16): groups[g * 16:g * 16 + 16] for g in range(cfg["behavior_groups"])}},
                    "key_to_group_class": {int(k): sorted(v) for k, v in key_classes.items()}},
        "movement": MOVEMENT[gs],
        "encounters": {"rules": rules, "zones": [wm.zone(z) for z in zones]},
        "regions": regions,
        "events": events,
        "entrances": entrances,
        "actors": actors,
        "warps": list(warps.values()),
        "verification": log,
    }
    (out / "worldmap.json").write_text(json.dumps(spec, indent=1), encoding="utf-8")
    cells = {"width": wc, "height": hc, "kind": wm.kind.ravel().tolist(), "flag31": wm.flag31.astype(int).ravel().tolist(),
             "event_back": wm.event[0].ravel().tolist(), "variant": wm.var.ravel().tolist(),
             # The terrain class at each 16 px cell's centre (the 2 px samples at (8, 8) inside the cell), for a
             # cell-based walkability grid; the full 2 px map stays in terrain_classes.png.
             "terrain_class": cls[4::8, 4::8].astype(int).ravel().tolist()}
    if gs == 2:
        cells["flag30"] = wm.flag30.astype(int).ravel().tolist()
    (out / "cells.json").write_text(json.dumps(cells), encoding="utf-8")

    if tmj:
        write_tmj(wm, out, idx, events, entrances, actors)
    for line in log:
        print(line)
    print("wrote", out, "size", W, "x", H, "terrain classes", class_hist)
    return spec


def write_tmj(wm, out, idx, events, entrances, actors):
    hc, wc = wm.var.shape
    key = [(wm.var * 65536 + np.minimum(wm.mt[layer], len(wm.metatiles) - 1)) * 2 + layer for layer in range(2)]
    allk = np.unique(np.concatenate([k.ravel() for k in key]))
    imgs, gid_of = [], {}
    for k in allk.tolist():
        layer, v, mt = k & 1, (k >> 1) // 65536, (k >> 1) % 65536
        ys, xs = np.nonzero(key[layer] == k)
        y, x = ys[0], xs[0]
        tile = idx[layer][y * 16:y * 16 + 16, x * 16:x * 16 + 16]
        if not tile.any():
            gid_of[k] = 0
            continue
        imgs.append((k, layer, v, x, y))
        gid_of[k] = len(imgs)
    cols = 64
    rows = (len(imgs) + cols - 1) // cols
    sheet = np.zeros((rows * 16, cols * 16, 4), np.uint8)
    for i, (k, layer, v, x, y) in enumerate(imgs):
        sheet[(i // cols) * 16:(i // cols) * 16 + 16, (i % cols) * 16:(i % cols) * 16 + 16] = \
            _cell_rgba(wm, idx[layer], v, x, y)
    Image.fromarray(sheet, "RGBA").save(out / "tileset.png", optimize=True)
    lut = np.vectorize(gid_of.get, otypes=[np.int64])
    data = [lut(k).ravel().tolist() for k in key]
    objs, oid = [], 1
    ev_layer = []
    for o in events:
        x, y, w, h = o["px_rect"]
        props = [{"name": n, "type": "int" if isinstance(o[n], int) else "string", "value": o[n]}
                 for n in ("event_id", "layer", "region", "to_room", "to_door", "to_name") if o.get(n) is not None]
        if o.get("handlers"):
            props.append({"name": "scripts", "type": "string", "value": ",".join(str(h["script"]) for h in o["handlers"])})
        ev_layer.append({"id": oid, "name": str(o.get("to_name") or o["event_id"]), "type": "solid" if o.get("solid") else "event",
                         "x": x, "y": y, "width": w, "height": h, "properties": props})
        oid += 1
    ent_layer = []
    for e in entrances:
        ent_layer.append({"id": oid, "name": "entrance %d" % e["id"], "type": "entrance", "point": True,
                          "x": e["px"][0], "y": e["px"][1],
                          "properties": [{"name": "entrance_id", "type": "int", "value": e["id"]},
                                         {"name": "angle", "type": "int", "value": e["angle"]}]})
        oid += 1
    act_layer = []
    for a in actors:
        if a["px"] is None:
            continue
        act_layer.append({"id": oid, "name": "actor %d" % a["index"], "type": "actor", "point": True,
                          "x": a["px"][0], "y": a["px"][1],
                          "properties": [{"name": "sprite", "type": "int", "value": a["sprite"] or 0},
                                         {"name": "slot", "type": "int", "value": a["slot"] or 0}]})
        oid += 1
    tmj = {"type": "map", "version": "1.10", "orientation": "orthogonal", "renderorder": "right-down",
           "width": wc, "height": hc, "tilewidth": 16, "tileheight": 16, "infinite": False,
           "nextlayerid": 6, "nextobjectid": oid,
           "properties": [{"name": "terrain_classes", "type": "file", "value": "terrain_classes.png"},
                          {"name": "terrain_sample_px", "type": "int", "value": 2},
                          {"name": "world_units_per_px", "type": "int", "value": 2}],
           "tilesets": [{"firstgid": 1, "name": "worldmap", "image": "tileset.png", "imagewidth": cols * 16,
                         "imageheight": rows * 16, "tilewidth": 16, "tileheight": 16, "tilecount": len(imgs),
                         "columns": cols, "margin": 0, "spacing": 0}],
           "layers": [
               {"id": 1, "name": "back", "type": "tilelayer", "width": wc, "height": hc, "x": 0, "y": 0,
                "opacity": 1, "visible": True, "data": data[0]},
               {"id": 2, "name": "front", "type": "tilelayer", "width": wc, "height": hc, "x": 0, "y": 0,
                "opacity": 1, "visible": True, "data": data[1]},
               {"id": 3, "name": "events", "type": "objectgroup", "x": 0, "y": 0, "opacity": 1, "visible": True,
                "draworder": "topdown", "objects": ev_layer},
               {"id": 4, "name": "entrances", "type": "objectgroup", "x": 0, "y": 0, "opacity": 1, "visible": True,
                "draworder": "topdown", "objects": ent_layer},
               {"id": 5, "name": "actors", "type": "objectgroup", "x": 0, "y": 0, "opacity": 1, "visible": True,
                "draworder": "topdown", "objects": act_layer}]}
    (out / "worldmap.tmj").write_text(json.dumps(tmj), encoding="utf-8")
    print("tmj: %d unique metatile images" % len(imgs))


def _cell_rgba(wm, idx_layer, v, x, y):
    V = wm.variants[v]
    pal = np.zeros((256, 4), np.uint8)
    pal[:len(V["palette"]), :3] = np.array(V["palette"], np.uint8)
    pal[1:, 3] = 255
    return pal[idx_layer[y * 16:y * 16 + 16, x * 16:x * 16 + 16]]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("rom")
    ap.add_argument("--out")
    ap.add_argument("--no-tmj", action="store_true")
    a = ap.parse_args(argv)
    export(a.rom, a.out, tmj=not a.no_tmj)


if __name__ == "__main__":
    sys.exit(main())
