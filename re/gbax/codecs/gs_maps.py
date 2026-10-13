"""Golden Sun 1 & 2 field maps -> engine-neutral PNG + Tiled JSON + collision/event JSON.

    python -m gbax.codecs.gs_maps ROM [--map N ...] [--all] [--no-render]

N is a *room* number (the game's map id, the index used by warps, place names and map code). Output goes to
games/<slug>/maps/: index.json, index.html (gallery), areas/area_NNN/ (graphics, shared by rooms that use the same
area) and rooms/room_NNN/ (Tiled map, events). See notes/gs_maps.md for the formats and what is VERIFIED.

Data path (GS1 addresses; GS2 found the same way, by following the master file table like gsmagic does):

  room table   0x0809F1A8  8 bytes/room: u16 map-code file, u8 place group, u8 kind, u16 area, u16 0
  area table   0x08013784  12 bytes/area: six u16 file numbers + base 0x128 (GS2 0x26C):
                           map container, palette (448 B = 14 BG palettes), 4 tileset blocks (16 KB 4bpp each,
                           format 2) = VRAM char blocks 0-3
  container    header (0x3C GS1 / 0x40 GS2) + compressed parts at u32 offsets +0x24...
               +0x24 metatiles (16x16 = 4 GBA tilemap entries), XOR-delta coded (FUN_0800F9F4)
               +0x28 height-shape table (4 bytes per shape)
               +0x2C cell grid 128x128: u16 metatile plane + event plane + shape plane, interleaved into 4-byte cells
                     by the ARM routine at 0x0800A37C (copied to RAM by FUN_0800FAC8)
  map code     per room, compressed Thumb code run at 0x02008000; it starts with `ldr r4,=f; bx r4` stubs. Stubs
               1-4 return data tables: entrances, warps, actors (NPCs/objects), event handlers.
"""
import argparse
import html
import json
import struct
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from ..rom import Rom
from .golden_sun import Decoder

ROM_BASE = 0x08000000
CODE_BASE = 0x02008000           # map code runs here
STUB = 0x47204C00                # ldr r4,[pc,#0]; bx r4
# room_var: s16 current room. GS1: read by FUN_0808A5F4 (0x02000240 + 0x1C0). GS2: map-code table getters compare
# 0x02000240 + 0x1E0 with room numbers to pick per-room tables when several rooms share one map-code file.
GAMES = {"AGSE": {"filetable": 0x320000, "gs": 1, "room_var": 0x02000400},
         "AGFE": {"filetable": 0x680000, "gs": 2, "room_var": 0x02000420}}
# Thumb code of the place-name lookup's loop (GS1 0x0808B182..; FUN_0808a5d0 -> 0x0808B158). Its table pointer is
# loaded into r5 a few instructions earlier.
PLACE_LOOP = bytes.fromhex("ea78 8023 1340 002b")
CELLS = 128                      # the cell grid is 128 x 128 cells of 16x16 px
TABLE_NAMES = {1: "entrances", 2: "warps", 3: "actors", 4: "events"}


def u16(b, o):
    return struct.unpack_from("<H", b, o)[0]


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def s32(b, o):
    return struct.unpack_from("<i", b, o)[0]


def bgr555_to_rgb(words):
    w = np.asarray(words, dtype=np.uint32)
    r, g, b = w & 31, (w >> 5) & 31, (w >> 10) & 31
    return np.stack([(r << 3) | (r >> 2), (g << 3) | (g >> 2), (b << 3) | (b >> 2)], -1).astype(np.uint8)


def decode_metatiles(t):
    """Part +0x24 after decompression -> u16 tilemap entries (4 per 16x16 metatile). Port of FUN_0800F9F4: byte 0 is
    the coding type, then (len-1)/2 entries; type 1 stores high bytes then low bytes, types 1 and 2 are XOR-delta."""
    kind, n = t[0], (len(t) - 1) // 2
    if len(t) % 2 == 0:
        return np.zeros(0, np.uint16)        # the game skips even-length data too
    if kind == 0:
        return np.frombuffer(t[1:1 + 2 * n], "<u2").copy()
    if kind == 1:
        v = (np.frombuffer(t[1:1 + n], np.uint8).astype(np.uint16) << 8) | np.frombuffer(t[1 + n:1 + 2 * n], np.uint8)
    elif kind == 2:
        v = np.frombuffer(t[1:1 + 2 * n], "<u2").astype(np.uint16)
    else:
        raise ValueError(f"metatile coding {kind}")
    return np.bitwise_xor.accumulate(v)


def decode_cells(raw):
    """Part +0x2C (0x10000 bytes) -> (tile u16[128,128], event u8[128,128], shape u8[128,128]). Port of the ARM
    routine at 0x0800A37C: plane 2 is the tile plane, where a low 12 bits of 0xFFF means 'next number in sequence'."""
    raw = bytes(raw).ljust(0x10000, b"\0")
    tiles = np.frombuffer(raw[0x8000:0x10000], "<u2").astype(np.int64)
    ph = (tiles & 0xFFF) == 0xFFF
    k = np.cumsum(ph) - 1
    seq = np.where(k < 0xFFF, (tiles & 0xF000) + k, tiles)
    tiles = np.where(ph, seq, tiles).astype(np.uint16)
    event = np.frombuffer(raw[0:0x4000], np.uint8)
    shape = np.frombuffer(raw[0x4000:0x8000], np.uint8)
    return tiles.reshape(CELLS, CELLS), event.reshape(CELLS, CELLS).copy(), shape.reshape(CELLS, CELLS).copy()


def tiles_4bpp(block):
    a = np.frombuffer(bytes(block), np.uint8).reshape(-1, 8, 4)
    px = np.empty((a.shape[0], 8, 8), np.uint8)
    px[:, :, 0::2] = a & 15
    px[:, :, 1::2] = a >> 4
    return px


class GsMaps:
    def __init__(self, rom_path):
        self.rom = Rom.load(rom_path)
        self.d = self.rom.data
        if self.rom.code not in GAMES:
            raise SystemExit(f"not Golden Sun 1/2 (game code {self.rom.code})")
        g = GAMES[self.rom.code]
        self.gs, self.ft, self.room_var = g["gs"], g["filetable"], g["room_var"]
        self.dec = Decoder(self.rom)
        self._cache = {}
        self._find_tables()
        self._load_text()

    # --- tables ------------------------------------------------------------------------------------------------
    def file_addr(self, n):
        return u32(self.d, self.ft + 4 * n) & 0x1FFFFFF

    def file_size(self, n):
        return self.file_addr(n + 1) - self.file_addr(n)

    def _find_tables(self):
        d, ft, gs1 = self.d, self.ft, self.gs == 1
        # Same pointer chase as gsmagic (adituv/gsmagic Form1.cs loadEntireMap), verified against FUN_0800FB38.
        p = u32(d, (u32(d, ft + 0x18) & 0x1FFFFFF) + 0xC)
        self.rooms_addr = u32(d, (p & 0x1FFFFFC) - 4) & 0x1FFFFFF
        p = u32(d, (u32(d, ft + 0xC) & 0x1FFFFFF) + 0x10C + 0x20 * gs1) & 0x1FFFFFF
        self.area_base = u32(d, (p & 0x1FFFFFC) - 4 - 0x160 * gs1)
        self.areas_addr = u32(d, (p & 0x1FFFFFC) - 8 - 0x164 * gs1) & 0x1FFFFFF
        n = 0
        while u16(d, self.rooms_addr + 8 * n) and n < 1000:
            n += 1
        self.n_rooms = n          # trimmed to the debug room labels in _load_text when the text export exists
        self.n_areas = max(u16(d, self.rooms_addr + 8 * i + 4) for i in range(n)) + 1
        # place-name table (FUN_0808a5d0 -> name lookup): 8-byte rows {s16 key, u16 door|0x8000 key-is-room, u32 name}
        # The loop pattern occurs in more than one function; keep the table whose first rows are the title screen,
        # clear-data and world-map names (group 0, 1, 2 -> names 0, 1, 2).
        self.place_addr = None
        i = d.find(PLACE_LOOP)
        while i >= 0 and self.place_addr is None:
            for back in range(2, 0x30, 2):
                ins = u16(d, i - back)
                if ins >> 8 == 0x4D:                     # ldr r5,[pc,#imm]
                    lit = ((i - back + 4) & ~3) + (ins & 0xFF) * 4
                    t = u32(d, lit) & 0x1FFFFFF
                    if t + 24 <= len(d) and [struct.unpack_from("<hHI", d, t + 8 * j) for j in range(3)] == \
                            [(0, 0x7FFF, 0), (1, 0x7FFF, 1), (2, 0x7FFF, 2)]:
                        self.place_addr = t
                    break
            i = d.find(PLACE_LOOP, i + 2)
        self.places = []
        if self.place_addr:
            o = self.place_addr
            while struct.unpack_from("<h", d, o)[0] != -1 and len(self.places) < 2000:
                k, f, v = struct.unpack_from("<hHI", d, o)
                self.places.append((k, f, v))
                o += 8

    def _load_text(self):
        ws = self.rom.workspace
        self.strings, self.place_first, self.room_label_first = {}, None, None
        p = ws / "text" / "strings.json"
        if p.exists():
            self.strings = json.loads(p.read_text(encoding="utf-8"))
        g = ws / "text" / "groups.json"
        if g.exists():
            loc = json.loads(g.read_text(encoding="utf-8"))["groups"].get("location_names")
            if loc:
                self.place_first = loc["first_id"]
                for i in range(loc["first_id"], loc["last_id"] + 1):     # debug room labels: TITLE, UTIL, WORLD..
                    if self.strings.get(str(i)) == "TITLE":
                        self.room_label_first = i
                        # one label per room; the table's zero terminator comes a few rows later
                        self.n_rooms = min(self.n_rooms, loc["last_id"] + 1 - i)
                        break

    def text(self, i):
        return self.strings.get(str(i)) if i is not None else None

    def room(self, r):
        b = self.d[self.rooms_addr + 8 * r:self.rooms_addr + 8 * r + 8]
        return {"room": r, "code_file": u16(b, 0), "group": b[2], "kind": b[3], "area": u16(b, 4), "extra": u16(b, 6)}

    def place_names(self, r):
        """[(door or None, name index)] for room r, in table order. The game takes the first row whose key matches
        (room number if bit 15 of the door field is set, else the room's place group) and whose door matches."""
        grp, out = self.room(r)["group"], []
        for k, f, v in self.places:
            if (k == r) if f & 0x8000 else (k == grp):
                door = None if f & 0x7FFF == 0x7FFF else ((f & 0x7FFF) ^ 0x4000) - 0x4000
                out.append((door, v))
        return out

    def area_files(self, a):
        return [u16(self.d, self.areas_addr + 12 * a + 2 * j) + self.area_base for j in range(6)]

    # --- decoding ----------------------------------------------------------------------------------------------
    def decode_file(self, n):
        if n in self._cache:
            return self._cache[n]
        a, size = self.file_addr(n), self.file_size(n)
        fmt = self.d[a]
        if fmt == 2:
            out = self.dec.decode_format2(a | ROM_BASE, size)[0]
        elif fmt in (0, 1):
            out = self.dec.decode(a | ROM_BASE)
        else:
            out = self.d[a:a + size]
        self._cache[n] = out
        return out

    def load_area(self, a):
        files = self.area_files(a)
        c = self.file_addr(files[0])
        d = self.d
        hl = u32(d, c + 0x24)
        nparts = (hl - 0x24) // 4 if 0x3C <= hl <= 0x40 else 6
        hdr = d[c:c + 0x24]
        layers = []
        for l in range(3):
            rec = hdr[0xC + 8 * l:0x14 + 8 * l]
            layers.append({"layer": l, "bg": 3 - l, "priority": hdr[4 + l], "char_block": hdr[7 + l] - 1,  # may be -1: tiles 512+ then start at block 0
                           "enabled": True, "offset_x8": rec[0], "offset_y8": rec[1],
                           "scroll_ratio_x16": rec[2], "scroll_ratio_y16": rec[3],
                           "auto_scroll": [struct.unpack_from("<b", rec, 4)[0], struct.unpack_from("<b", rec, 5)[0]],
                           "rec_bytes_6_7": rec[6:8].hex()})
        parts = {}
        for i in range(nparts):
            off = u32(d, c + 0x24 + 4 * i)
            key = f"+0x{0x24 + 4 * i:02X}"
            if not off:
                parts[key] = None
                continue
            fmt = d[c + off]
            try:
                data = self.dec.decode((c + off) | ROM_BASE) if fmt in (0, 1) else None
            except Exception as e:  # noqa: BLE001 - report, don't stop the export
                data = None
                parts[key] = {"offset": off, "format": fmt, "error": str(e)}
                continue
            parts[key] = {"offset": off, "format": fmt, "size": len(data) if data is not None else None, "data": data}
        # The three layers sit side by side in the 128x128 grid. Header bytes 0-3 (x8 px) are camera bounds and can
        # be larger than a layer's region (e.g. 0,0,128,128), so clip the map to the space before the next layer.
        W, H = hdr[2] * 8, hdr[3] * 8
        for L in layers:
            for M in layers:
                if M is L:
                    continue
                dx, dy = (M["offset_x8"] - L["offset_x8"]) * 8, (M["offset_y8"] - L["offset_y8"]) * 8
                if dx > 0 and dy == 0:
                    W = min(W, dx)
                if dy > 0 and dx == 0:
                    H = min(H, dy)
            W = min(W, CELLS * 16 - L["offset_x8"] * 8)
            H = min(H, CELLS * 16 - L["offset_y8"] * 8)
        A = {"area": a, "files": files, "header": hdr.hex(), "bounds_px": [hdr[0] * 8, hdr[1] * 8, hdr[2] * 8, hdr[3] * 8],
             "width": W, "height": H, "layers": layers, "parts": parts}
        pal = self.decode_file(files[1])
        A["palette_words"] = list(struct.unpack_from(f"<{len(pal) // 2}H", pal))
        vram = bytearray(0x10000)
        for j, f in enumerate(files[2:6]):
            blk = self.decode_file(f)[:0x4000]
            vram[0x4000 * j:0x4000 * j + len(blk)] = blk
        A["vram"] = bytes(vram)
        mt = parts.get("+0x24")
        A["metatiles"] = decode_metatiles(mt["data"]) if mt and mt.get("data") else np.zeros(0, np.uint16)
        cl = parts.get("+0x2C")
        if not (cl and cl.get("data")):
            raise ValueError("no cell grid (+0x2C)")
        A["tile"], A["event"], A["shape"] = decode_cells(cl["data"])
        hs = parts.get("+0x28")
        A["shapes"] = [list(hs["data"][i:i + 4]) for i in range(0, len(hs["data"]) - 3, 4)] if hs and hs.get("data") else []
        return A

    # --- rendering ---------------------------------------------------------------------------------------------
    def layer_cells(self, A, l):
        """Cell window (x0, y0, w, h, pixel shift x, y) of layer l in the 128x128 grid."""
        L = A["layers"][l]
        sx, sy = L["offset_x8"], L["offset_y8"]
        w = (A["width"] + (sx & 1) * 8 + 15) // 16
        h = (A["height"] + (sy & 1) * 8 + 15) // 16
        return sx >> 1, sy >> 1, w, h, (sx & 1) * 8, (sy & 1) * 8

    def render_layer(self, A, l):
        """-> (RGBA uint8 [H,W,4] cropped to the map, metatile keys [h,w] (-1 empty), window)."""
        L = A["layers"][l]
        x0, y0, w, h, px, py = self.layer_cells(A, l)
        cb = L["char_block"]
        pal = bgr555_to_rgb(A["palette_words"] + [0] * (256 - len(A["palette_words"])))
        tiles = tiles_4bpp(A["vram"])                    # 2048 tiles
        mts = A["metatiles"]
        nmt = len(mts) // 4
        ys, xs = np.mgrid[y0:y0 + h, x0:x0 + w]
        inside = (ys < CELLS) & (xs < CELLS)
        ids = np.where(inside, A["tile"][np.minimum(ys, CELLS - 1), np.minimum(xs, CELLS - 1)].astype(np.int64) & 0xFFF, -1)
        ids[ids >= nmt] = -1
        img = np.zeros((h * 16, w * 16, 4), np.uint8)
        if not L["enabled"] or nmt == 0:
            return img[py:py + A["height"], px:px + A["width"]], np.full((h, w), -1), (x0, y0, w, h, px, py)
        ent = np.where(ids[..., None] >= 0, mts.reshape(-1, 4)[np.maximum(ids, 0)], 0).astype(np.int64)  # [h,w,4]
        tn = (ent & 0x3FF) + cb * 512
        valid = (ids[..., None] >= 0) & (tn < 2048) & (tn >= 0)
        tp = tiles[np.where(valid, tn, 0)]                   # [h,w,4,8,8]
        hf = (ent & 0x400) != 0
        vf = (ent & 0x800) != 0
        tp = np.where(hf[..., None, None], tp[..., :, ::-1], tp)
        tp = np.where(vf[..., None, None], tp[..., ::-1, :], tp)
        tp = np.where(valid[..., None, None], tp, 0)
        pidx = (ent >> 12)[..., None, None] * 16 + tp
        rgba = np.concatenate([pal[pidx], np.where(tp > 0, 255, 0).astype(np.uint8)[..., None]], -1)  # [h,w,4,8,8,4]
        rgba = rgba.reshape(h, w, 2, 2, 8, 8, 4).transpose(0, 2, 4, 1, 3, 5, 6).reshape(h * 16, w * 16, 4)
        img[:] = rgba
        return img[py:py + A["height"], px:px + A["width"]], ids, (x0, y0, w, h, px, py)

    def draw_order(self, A):
        """Back-to-front layer order: higher priority number first; on ties the lower BG number (= higher layer
        index, since layer l is BG 3-l) is drawn later, i.e. on top. INFERRED from gsmagic's renderer."""
        en = [L for L in A["layers"] if L["enabled"]]
        return [L["layer"] for L in sorted(en, key=lambda L: (-L["priority"], L["layer"]))]

    def composite(self, A, imgs):
        pal = bgr555_to_rgb(A["palette_words"][:1] or [0])
        out = np.zeros((A["height"], A["width"], 3), np.uint8)
        out[:] = pal[0]
        blend = A.get("blend")
        top_is = np.full(out.shape[:2], -1, np.int8)      # which layer is currently topmost (-1 backdrop)
        for l in self.draw_order(A):
            im = imgs[l]
            m = im[..., 3] > 0
            if blend and blend["mode"] == 1 and blend["first"][3 - l]:
                below_ok = np.array([blend["second"][3 - t] if t >= 0 else blend["second"][5] for t in range(-1, 3)])
                b = m & below_ok[top_is + 1]
                mix = (im[..., :3].astype(np.int32) * blend["eva"] + out.astype(np.int32) * blend["evb"]) >> 4
                out[b] = np.minimum(mix[b], 255).astype(np.uint8)
                out[m & ~b] = im[..., :3][m & ~b]
            else:
                out[m] = im[..., :3][m]
            top_is[m] = l
        return out

    # --- map code ----------------------------------------------------------------------------------------------
    def map_code(self, r):
        R = self.room(r)
        code = self.decode_file(R["code_file"])
        stubs = []
        k = 0
        while 8 * k + 8 <= len(code) and u32(code, 8 * k) == STUB:
            stubs.append(u32(code, 8 * k + 4))
            k += 1
        tables = {}
        for k, t in enumerate(stubs):
            if not 1 <= k <= 4:
                continue
            # Run the getter in the emulator with this room as the current room: in GS2 several rooms share a
            # map-code file and the getters pick the room's own table. Falls back to the static `ldr r0,=x; bx lr`.
            v = None
            try:
                g = self.dec.gba
                g.write(CODE_BASE, code)
                try:     # Unicorn caches translated blocks: drop the previous room's code at the same addresses
                    g.uc.ctl_remove_cache(CODE_BASE, CODE_BASE + 0x10000)
                except AttributeError:
                    pass
                g.write(self.room_var, struct.pack("<h", r))
                v = g.call(t | 1, (), thumb=True, max_instructions=200_000)
            except Exception:  # noqa: BLE001
                v = None
            o = (t & ~1) - CODE_BASE
            if not (v and CODE_BASE <= v < CODE_BASE + len(code)) and 0 <= o < len(code) - 4 and code[o + 1] == 0x48                     and u16(code, o + 2) == 0x4770:                                         # ldr r0,=x; bx lr
                v = u32(code, (((t & ~1) + 4) & ~3) + code[o] * 4 - CODE_BASE)
            if v and CODE_BASE <= v < CODE_BASE + len(code):
                tables[k] = v
        return code, stubs, tables

    def parse_tables(self, r):
        code, stubs, tables = self.map_code(r)
        bounds = sorted(set(v - CODE_BASE for v in tables.values() if 0 <= v - CODE_BASE < len(code))) + [len(code)]
        end = lambda o: min([b for b in bounds if b > o] or [len(code)])  # noqa: E731
        out = {"code_size": len(code), "stubs": [f"0x{s:08X}" for s in stubs],
               "tables": {TABLE_NAMES.get(k, f"stub{k}"): f"0x{v:08X}" for k, v in tables.items()}}
        ent, war, act, evt = [], [], [], []
        if 1 in tables:                                   # entrances: 24 bytes
            o = tables[1] - CODE_BASE
            while o + 24 <= end(o) and u16(code, o) != 0xFFFF:
                ent.append({"id": u16(code, o), "flag": u16(code, o + 2), "x": u16(code, o + 4), "y": u16(code, o + 6),
                            "z": u16(code, o + 8), "angle": u16(code, o + 10), "rest": code[o + 12:o + 24].hex()})
                o += 24
        if 2 in tables:          # warps: u32 room | door << 12 | event << 20 | flags << 28; end 0x1FF / -1
            o = tables[2] - CODE_BASE
            while o + 4 <= end(o):
                v = u32(code, o)
                if v & 0xFFF == 0x1FF or v == 0xFFFFFFFF:
                    break
                war.append({"event": (v >> 20) & 0xFF, "to_room": v & 0xFFF, "to_door": (v >> 12) & 0xFF,
                            "flags": v >> 28, "raw": f"0x{v:08X}"})
                o += 4
        if 3 in tables:                                   # actors: 24 bytes
            o = tables[3] - CODE_BASE
            i = 0
            while o + 24 <= end(o) and u16(code, o) != 0xFFFF:
                act.append({"index": i, "sprite": u16(code, o), "flag": u16(code, o + 2), "b4": code[o + 4],
                            "b5_7": code[o + 5:o + 8].hex(), "x": s32(code, o + 8) / 65536,
                            "y": s32(code, o + 12) / 65536, "z": s32(code, o + 16) / 65536,
                            "angle": u16(code, o + 20), "b22": code[o + 22], "b23": code[o + 23]})
                o += 24
                i += 1
        if 4 in tables:                                   # event handlers: 12 bytes
            o = tables[4] - CODE_BASE
            while o + 12 <= end(o):
                typ, b1, id_, flag, val = code[o], code[o + 1], u16(code, o + 4), u16(code, o + 6), u32(code, o + 8)
                if typ == 0xFF or (u32(code, o) == 0 and id_ == 0 and val == 0):
                    break
                e = {"type": typ, "b1": b1, "b2_3": u16(code, o + 2), "id": id_, "flag": flag}
                if CODE_BASE <= val < CODE_BASE + len(code):
                    e["script"] = f"0x{val:08X}"
                else:
                    e["text_id"] = val
                    if self.text(val):
                        e["text"] = self.text(val)
                evt.append(e)
                o += 12
        out.update(entrances=ent, warps=war, actors=act, events=evt)
        return out, code


# --- export --------------------------------------------------------------------------------------------------------
def unique_tiles(imgs_keys, A):
    """Collect unique 16x16 RGBA tiles over all layers -> (tileset image, per-layer gid arrays)."""
    seen, tiles, gids = {}, [], {}
    for l, (img, ids, win) in imgs_keys.items():
        x0, y0, w, h, px, py = win
        full = np.zeros((h * 16, w * 16, 4), np.uint8)
        full[py:py + img.shape[0], px:px + img.shape[1]] = img
        g = np.zeros((h, w), np.int64)
        for cy in range(h):
            for cx in range(w):
                t = full[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                if not t[..., 3].any():
                    continue
                key = t.tobytes()
                if key not in seen:
                    seen[key] = len(tiles) + 1
                    tiles.append(t)
                g[cy, cx] = seen[key]
        gids[l] = g
    cols = 16
    rows = max(1, (len(tiles) + cols - 1) // cols)
    sheet = np.zeros((rows * 16, cols * 16, 4), np.uint8)
    for i, t in enumerate(tiles):
        sheet[(i // cols) * 16:(i // cols) * 16 + 16, (i % cols) * 16:(i % cols) * 16 + 16] = t
    return sheet, gids, len(tiles)


def merge_runs(mask_vals, cell=16, skip=(0,)):
    """Horizontal runs of equal non-skipped values -> rectangles (x, y, w, h, value) in px."""
    rects = []
    h, w = mask_vals.shape
    for y in range(h):
        x = 0
        while x < w:
            v = int(mask_vals[y, x])
            if v in skip:
                x += 1
                continue
            x1 = x
            while x1 + 1 < w and mask_vals[y, x1 + 1] == v:
                x1 += 1
            rects.append((x * cell, y * cell, (x1 - x + 1) * cell, cell, v))
            x = x1 + 1
    return rects


def export(gm, rooms=None, render=True):
    ws = gm.rom.workspace / "maps"
    (ws / "areas").mkdir(parents=True, exist_ok=True)
    (ws / "rooms").mkdir(parents=True, exist_ok=True)
    rooms = list(range(gm.n_rooms)) if rooms is None else rooms
    old = ws / "index.json"
    index = json.loads(old.read_text(encoding="utf-8")) if old.exists() and rooms != list(range(gm.n_rooms)) else {}
    index.update({"game": gm.rom.code, "rom_title": gm.rom.title, "room_table": f"0x{gm.rooms_addr | ROM_BASE:08X}",
                  "area_table": f"0x{gm.areas_addr | ROM_BASE:08X}", "area_file_base": gm.area_base,
                  "place_table": f"0x{gm.place_addr | ROM_BASE:08X}" if gm.place_addr else None,
                  "rooms_total": gm.n_rooms, "areas_total": gm.n_areas})
    R_all = index.setdefault("rooms", {})
    A_all = index.setdefault("areas", {})
    done_areas = {}
    for r in rooms:
        R = gm.room(r)
        a = R["area"]
        names = gm.place_names(r)
        default = next((v for door, v in names if door is None), names[0][1] if names else None)
        pf = gm.place_first
        entry = dict(R, name=gm.text(pf + default) if pf is not None and default is not None else None,
                     name_id=pf + default if pf is not None and default is not None else None,
                     label=gm.text(gm.room_label_first + r) if gm.room_label_first else None,
                     names_by_door=[{"door": d_, "name": gm.text(pf + v) if pf is not None else None, "name_index": v}
                                    for d_, v in names])
        # ---- area graphics (once per area)
        if a not in done_areas:
            done_areas[a] = None
            ad = ws / "areas" / f"area_{a:03d}"
            ad.mkdir(exist_ok=True)
            info = {"area": a, "files": gm.area_files(a)}
            try:
                A = gm.load_area(a)
                done_areas[a] = A
                vis = A["parts"].get("+0x38")
                if gm.gs == 2 and vis and vis.get("data") and len(vis["data"]) >= 4:
                    v = vis["data"]
                    bc = u16(v, 0)
                    A["blend"] = {"bldcnt": bc, "mode": (bc >> 6) & 3, "first": [(bc >> i) & 1 for i in range(6)],
                                  "second": [(bc >> (8 + i)) & 1 for i in range(6)], "eva": min(v[2], 16), "evb": min(v[3], 16)}
                info.update({k: A[k] for k in ("header", "bounds_px", "width", "height", "layers")})
                info["blend"] = A.get("blend")
                info["parts"] = {k: ({kk: vv for kk, vv in p.items() if kk != "data"} if p else None) for k, p in A["parts"].items()}
                info["palette"] = [f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}" for c in bgr555_to_rgb(A["palette_words"])]
                info["metatiles"] = len(A["metatiles"]) // 4
                info["height_shapes"] = A["shapes"]
                info["draw_order"] = gm.draw_order(A)
                if A["width"] == 0 or A["height"] == 0:
                    raise ValueError("zero size in header")
                if render:
                    imgs = {}
                    for l in range(3):
                        img, ids, win = gm.render_layer(A, l)
                        imgs[l] = (img, ids, win)
                        A["layers"][l]["enabled"] = bool(img[..., 3].any())     # empty layer -> not drawn
                        if A["layers"][l]["enabled"]:
                            Image.fromarray(img, "RGBA").save(ad / f"layer{l}.png", optimize=True)
                    info["draw_order"] = gm.draw_order(A)
                    comp = gm.composite(A, {l: v[0] for l, v in imgs.items()})
                    Image.fromarray(comp, "RGB").save(ad / "composite.png", optimize=True)
                    en = {l: v for l, v in imgs.items() if A["layers"][l]["enabled"]}
                    sheet, gids, nt = unique_tiles(en, A)
                    Image.fromarray(sheet, "RGBA").save(ad / "tileset.png", optimize=True)
                    A["gids"], A["windows"], A["ntiles"] = gids, {l: v[2] for l, v in imgs.items()}, nt
                    info["unique_tiles_16"] = nt
                    pal = bgr555_to_rgb(A["palette_words"])
                    Image.fromarray(np.repeat(np.repeat(pal.reshape(-1, 16, 3), 8, 0), 8, 1), "RGB").save(ad / "palette.png")
                # collision per layer window
                coll = {"cell_px": 16, "solid_value": 255, "layers": [], "height_shapes": [
                    {"index": i, "function": s[0] & 15, "flags": s[0] >> 4,
                     "heights_8px": [((b ^ 0x80) - 0x80) for b in s[1:]]} for i, s in enumerate(A["shapes"])]}
                for l in range(3):
                    x0, y0, w, h, px, py = gm.layer_cells(A, l)
                    sl = np.s_[y0:min(y0 + h, CELLS), x0:min(x0 + w, CELLS)]
                    coll["layers"].append({"layer": l, "grid_x": x0, "grid_y": y0, "pixel_shift": [px, py],
                                           "width": int(A["event"][sl].shape[1]), "height": int(A["event"][sl].shape[0]),
                                           "event": A["event"][sl].tolist(), "shape": A["shape"][sl].tolist(),
                                           "tile_flags": (A["tile"][sl] >> 12).tolist()})
                (ad / "collision.json").write_text(json.dumps(coll, separators=(",", ":")), encoding="utf-8")
                info["status"] = "ok" if info.get("metatiles", 0) > 1 else "empty (stub map: 1 metatile)"
                if A["layers"] and render:
                    walk = [(A["event"][gm.layer_cells(A, l)[1]:, gm.layer_cells(A, l)[0]:][:(A["height"] + 15) // 16,
                             :(A["width"] + 15) // 16] != 255) for l in range(3)]
                    ys, xs = np.nonzero(walk[0] | walk[1] | walk[2])
                    if len(xs):
                        info["walkable_bounds_px"] = [int(xs.min()) * 16, int(ys.min()) * 16, int(xs.max() + 1) * 16, int(ys.max() + 1) * 16]
            except Exception as e:  # noqa: BLE001
                info["status"] = f"error: {type(e).__name__}: {e}"
            (ad / "area.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
            A_all[str(a)] = {"status": info["status"], "width": info.get("width"), "height": info.get("height"),
                             "unique_tiles_16": info.get("unique_tiles_16"), "files": info["files"]}
        A = done_areas.get(a)
        # ---- room: events + Tiled map
        rd = ws / "rooms" / f"room_{r:03d}"
        rd.mkdir(exist_ok=True)
        try:
            ev, code = gm.parse_tables(r)
            (rd / "map_code.bin").write_bytes(code)
            entry["events_status"] = "ok"
        except Exception as e:  # noqa: BLE001
            ev, entry["events_status"] = {}, f"error: {type(e).__name__}: {e}"
        ev_out = dict(room=r, area=a, name=entry["name"], label=entry["label"], code_file=R["code_file"],
                      code_base=f"0x{CODE_BASE:08X}", **ev)
        if A is not None:
            for l in range(3):
                x0, y0, w, h, px, py = gm.layer_cells(A, l)
                sub = A["event"][y0:min(y0 + h, CELLS), x0:min(x0 + w, CELLS)]
                ids = sorted(set(int(v) for v in np.unique(sub)) - {0, 255})
                ev_out.setdefault("tile_event_ids_by_layer", {})[str(l)] = ids
        (rd / "events.json").write_text(json.dumps(ev_out, indent=1, ensure_ascii=False), encoding="utf-8")
        entry["counts"] = {k: len(ev.get(k, [])) for k in ("entrances", "warps", "actors", "events")}
        if A is not None and "gids" in A:
            write_tiled(gm, A, r, ev, rd, a)
            entry["tiled"] = f"rooms/room_{r:03d}/room_{r:03d}.tmj"
        entry["area_status"] = A_all[str(a)]["status"]
        R_all[str(r)] = entry
        print(f"room {r:3d} area {a:3d} {A_all[str(a)]['status'][:60]:60s} {entry['name']}", flush=True)
    index["rooms"] = dict(sorted(R_all.items(), key=lambda kv: int(kv[0])))
    index["areas"] = dict(sorted(A_all.items(), key=lambda kv: int(kv[0])))
    ok = sum(1 for v in index["areas"].values() if v["status"] == "ok")
    # consistency check of the warp decoding: every warp's door should be an entrance id of its target room
    wt = wok = 0
    for r, e in index["rooms"].items():
        evp = ws / "rooms" / f"room_{int(r):03d}" / "events.json"
        if not evp.exists():
            continue
        for w_ in json.loads(evp.read_text(encoding="utf-8")).get("warps", []):
            tp = ws / "rooms" / f"room_{w_['to_room']:03d}" / "events.json"
            if tp.exists():
                wt += 1
                wok += any(x["id"] == w_["to_door"] for x in json.loads(tp.read_text(encoding="utf-8")).get("entrances", []))
    index["coverage"] = {"areas_ok": ok, "areas_seen": len(index["areas"]),
                         "areas_empty_stub": sum(1 for v in index["areas"].values() if v["status"].startswith("empty")),
                         "warps_checked": wt, "warps_door_found": wok,
                         "rooms_events_ok": sum(1 for v in index["rooms"].values() if v.get("events_status") == "ok"),
                         "rooms_seen": len(index["rooms"])}
    (ws / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    write_gallery(gm, index, ws)
    return index


def write_tiled(gm, A, r, ev, rd, a):
    rel = f"../../areas/area_{a:03d}/"
    W, H = (A["width"] + 15) // 16 + 1, (A["height"] + 15) // 16 + 1
    layers, lid = [], 1
    for l in gm.draw_order(A):
        g = A["gids"][l]
        x0, y0, w, h, px, py = A["windows"][l]
        data = np.zeros((H, W), np.int64)
        data[:min(h, H), :min(w, W)] = g[:H, :W]
        layers.append({"id": lid, "name": f"layer{l} (BG{3 - l})", "type": "tilelayer", "x": 0, "y": 0, "width": W,
                       "height": H, "opacity": 1, "visible": True, "offsetx": -px, "offsety": -py,
                       "data": data.ravel().tolist(),
                       "properties": [{"name": "priority", "type": "int", "value": A["layers"][l]["priority"]},
                                      {"name": "scroll_ratio_x16", "type": "int", "value": A["layers"][l]["scroll_ratio_x16"]},
                                      {"name": "scroll_ratio_y16", "type": "int", "value": A["layers"][l]["scroll_ratio_y16"]}]})
        lid += 1
    objs, oid = [], 1

    def obj(name, typ, x, y, w=0, h=0, props=None, point=False):
        nonlocal oid
        o = {"id": oid, "name": name, "type": typ, "x": x, "y": y, "width": w, "height": h, "rotation": 0, "visible": True,
             "properties": [{"name": k, "type": "string" if isinstance(v, str) else ("float" if isinstance(v, float) else "int"),
                             "value": v} for k, v in (props or {}).items() if v is not None]}
        if point:
            o["point"] = True
        oid += 1
        return o

    groups = []
    trig = []
    warps = {w_["event"]: w_ for w_ in ev.get("warps", [])}
    handlers = {}
    for e in ev.get("events", []):
        if e["type"] != 0:
            handlers.setdefault(e["id"], e)
    for l in range(3):
        x0, y0, w, h, px, py = gm.layer_cells(A, l)
        sub = A["event"][y0:min(y0 + h, CELLS), x0:min(x0 + w, CELLS)]
        for (x, y, ww, hh, v) in merge_runs(sub, skip=(0, 255)):
            p = {"event_id": v, "layer": l}
            if v in warps:
                p.update(to_room=warps[v]["to_room"], to_door=warps[v]["to_door"])
            if v in handlers:
                p.update(handler_type=handlers[v]["type"], script=handlers[v].get("script"))
            trig.append(obj(f"event {v}", "warp" if v in warps else "trigger", x - px, y - py, ww, hh, p))
    groups.append(("tile events", trig))
    groups.append(("entrances", [obj(f"entrance {e['id']}", "entrance", e["x"], e["z"], props={"id": e["id"], "y": e["y"],
                                 "angle": e["angle"]}, point=True) for e in ev.get("entrances", [])]))
    talk = {e["id"]: e for e in ev.get("events", []) if e["type"] == 0}
    acts = []
    for ac in ev.get("actors", []):
        t = talk.get(ac["index"], {})
        acts.append(obj(f"actor {ac['index']}", "actor", ac["x"], ac["z"], props={
            "sprite": ac["sprite"], "y": ac["y"], "angle": ac["angle"], "b4": ac["b4"], "flag": ac["flag"],
            "script": t.get("script"), "text_id": t.get("text_id")}, point=True))
    groups.append(("actors", acts))
    for name, objs_ in groups:
        layers.append({"id": lid, "name": name, "type": "objectgroup", "draworder": "topdown", "x": 0, "y": 0,
                       "opacity": 1, "visible": True, "objects": objs_})
        lid += 1
    ts = Image.open(rd.parent.parent / "areas" / f"area_{a:03d}" / "tileset.png")
    tmj = {"type": "map", "version": "1.10", "tiledversion": "1.10.2", "orientation": "orthogonal",
           "renderorder": "right-down", "width": W, "height": H, "tilewidth": 16, "tileheight": 16, "infinite": False,
           "nextlayerid": lid, "nextobjectid": oid, "layers": layers,
           "properties": [{"name": "room", "type": "int", "value": r}, {"name": "area", "type": "int", "value": a},
                          {"name": "pixel_width", "type": "int", "value": A["width"]},
                          {"name": "pixel_height", "type": "int", "value": A["height"]}],
           "tilesets": [{"firstgid": 1, "name": f"area_{a:03d}", "image": rel + "tileset.png", "imagewidth": ts.width,
                         "imageheight": ts.height, "tilewidth": 16, "tileheight": 16, "tilecount": A["ntiles"],
                         "columns": 16, "margin": 0, "spacing": 0}]}
    (rd / f"room_{r:03d}.tmj").write_text(json.dumps(tmj, separators=(",", ":")), encoding="utf-8")


def write_gallery(gm, index, ws):
    cards = []
    for r, e in index["rooms"].items():
        a = e["area"]
        img = f"areas/area_{a:03d}/composite.png"
        ok = (ws / img).exists()
        cards.append(f"<figure>{'<img loading=lazy src=' + json.dumps(img) + '>' if ok else '<div class=miss>no render</div>'}"
                     f"<figcaption><b>{int(r)}</b> {html.escape(str(e.get('name')))} <small>{html.escape(str(e.get('label')))}"
                     f" · area {a} · {e.get('counts', {})}</small></figcaption></figure>")
    cov = index["coverage"]
    page = ("<!doctype html><meta charset=utf-8><title>Golden Sun maps</title><style>"
            ":root{--bg:#f6f5f2;--fg:#1d1d1f;--card:#fff;--muted:#666}"
            "@media (prefers-color-scheme:dark){:root{--bg:#161616;--fg:#eee;--card:#222;--muted:#aaa}}"
            "body{background:var(--bg);color:var(--fg);font:14px system-ui;margin:16px}"
            ".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}"
            "figure{margin:0;background:var(--card);padding:8px;border-radius:6px}"
            "img{width:100%;image-rendering:pixelated;max-height:420px;object-fit:contain;background:#000}"
            "small{color:var(--muted);display:block}.miss{height:120px;display:grid;place-items:center;color:var(--muted)}</style>"
            f"<h1>{html.escape(gm.rom.title)} ({gm.rom.code}) maps</h1><p>Areas rendered: {cov['areas_ok']} of "
            f"{cov['areas_seen']}; rooms with event tables: {cov['rooms_events_ok']} of {cov['rooms_seen']}.</p>"
            f"<div class=g>{''.join(cards)}</div>")
    (ws / "index.html").write_text(page, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("rom")
    ap.add_argument("--map", type=int, action="append", help="room number (repeatable)")
    ap.add_argument("--all", action="store_true", help="all rooms (default when --map is not given)")
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args(argv)
    gm = GsMaps(a.rom)
    print(f"{gm.rom.code}: rooms {gm.n_rooms} @0x{gm.rooms_addr | ROM_BASE:08X}, areas {gm.n_areas} "
          f"@0x{gm.areas_addr | ROM_BASE:08X} (+{gm.area_base}), place table "
          f"{'0x%08X' % (gm.place_addr | ROM_BASE) if gm.place_addr else None} ({len(gm.places)} rows)")
    idx = export(gm, None if a.all or not a.map else a.map, render=not a.no_render)
    print(json.dumps(idx["coverage"]))


if __name__ == "__main__":
    sys.exit(main())
