"""Golden Sun 1 / 2 battle sprites (enemies, party, weapons) and the shared sprite table.

    python -m gbax.codecs.gs_battle_sprites ROM [ROM2 ...]

Writes games/<slug>/battle_sprites/:
    enemies/NNN_<name>.png   one sheet per enemy record (all frames, real palette, palette swap applied,
                             colour 0 transparent); enemies.json describes them
    sprites/NNNN.png         every entry of the game's sprite table (party battle sprites, weapons, enemy bases,
                             field sprites), unswapped; sprites.json gives sizes, frame rectangles, raw fields
    palette.png / palette.json   the 224-colour global sprite palette
    index.html               gallery

Pipeline (VERIFIED in code, see notes/gs_battle_sprites.md):
    enemy record .battle_id -> battle table (8 B: u16 sprite id, u8 flags, u8 (variant<<1 | ...), u8, 3 pad)
    sprite id -> sprite table (20 B: w, h, flags, ?, ?, n_anims, 0, ?, ?, ?, type, 0, frames*, anims*)
    frames* == 0 -> sprite-to-file map (u16 file, u16 sprite) -> file, format 0/1 compressed, starts with a
                    0-terminated list of u32 offsets (relative to the file start), one per frame
    frame data: type 0 = RLE; type 3 = u16 header + RLE or a back-referenced stream expanded by the game's
                own Thumb routine (emulated); type 1 = format 0/1 compressed raw 8bpp
    RLE: byte 0 ends, 0xE0..0xFF skip (b - 0xDF) transparent pixels, else one pixel (global palette index)
    palette swap n (1..5): byte map at remap + 0x100*(n-1), applied to every pixel byte < 0xE0
"""
import json
import struct
import sys
import hashlib
from html import escape
from pathlib import Path

import numpy as np
from PIL import Image

from ..rom import Rom
from ..emu import Gba
from .golden_sun import Decoder

ROOT = Path(__file__).resolve().parents[2]

# Addresses (all VERIFIED: code that reads them is cited in notes/gs_battle_sprites.md)
GAMES = {
    "AGSE": dict(file_table=0x08320000, sprite_table=0x08185024, sprite_count=512, palette=0x0800779C,
                 remap=0x080092B8, file_map=0x08012FA0, battle_table=0x080C7420, battle_count=172,
                 stage1=0x0800A97C, two_part=(0x1DC, 0x1E3)),
    "AGFE": dict(file_table=0x08680000, sprite_table=0x08300000, sprite_count=716, palette=0x08017B10,
                 remap=0x080203A8, file_map=0x0802E91C, battle_table=0x08130D0C, battle_count=387,
                 stage1=0x08021940, two_part=()),
}
# Sprite-id groups outside the enemy table. INFERRED from the decoded images (no code link yet), see notes.
GROUPS = {
    "AGSE": dict(party={300: "Isaac", 301: "Garet", 302: "Ivan", 303: "Mia", 305: "Jenna"},
                 weapon_overlay=range(320, 340), status_icon=range(340, 370), summon_piece=range(370, 391),
                 battle_misc=range(391, 400)),
    "AGFE": dict(party={490: "Isaac", 495: "Garet", 500: "Ivan", 504: "Mia", 508: "Felix", 513: "Jenna",
                        517: "Sheba", 521: "Piers"},
                 weapon_overlay=range(490, 526), summon_piece=range(642, 667), battle_misc=range(667, 685),
                 status_icon=range(685, 716)),
}


def category(code, sid, enemy_ids):
    """Returns (category, character name or None)."""
    g = GROUPS[code]
    if sid in g["party"]:
        return "party", g["party"][sid]
    if sid in enemy_ids:
        return "enemy", None
    for k in ("weapon_overlay", "status_icon", "summon_piece", "battle_misc"):
        if sid in g[k]:
            return k, None
    return "field", None


BUF = 0x02010000
OK = ("ok", "empty")


class SpriteSet:
    def __init__(self, rom):
        self.rom, self.d = rom, rom.data
        self.code = bytes(self.d[0xAC:0xB0]).decode("ascii")
        self.cfg = GAMES[self.code]
        self.dec = Decoder(rom)
        self.gba = Gba(rom)
        pal = np.frombuffer(self.bytes(self.cfg["palette"], 0x1C0), "<u2")
        rgb = np.stack([(pal & 31) << 3, ((pal >> 5) & 31) << 3, ((pal >> 10) & 31) << 3], 1)
        rgb = rgb | (rgb >> 5)
        self.rgb = np.vstack([rgb, np.tile([255, 0, 255], (32, 1))]).astype(np.uint8)  # >= 0xE0: magenta (bad)
        self.file_map = {}
        a = self.cfg["file_map"]
        while self.u16(a + 2):
            self.file_map[self.u16(a + 2)] = self.u16(a)
            a += 4
        self.entries = [self.entry(i) for i in range(self.cfg["sprite_count"])]
        starts = sorted({e["frames_ptr"] for e in self.entries if e and e["frames_ptr"]}
                        | {e["anims_ptr"] for e in self.entries if e and e["anims_ptr"]})
        self.list_starts = starts

    # --- raw access
    def u16(self, a): return struct.unpack_from("<H", self.d, a - 0x08000000)[0]
    def u32(self, a): return struct.unpack_from("<I", self.d, a - 0x08000000)[0]
    def bytes(self, a, n): return bytes(self.d[a - 0x08000000:a - 0x08000000 + n])
    def is_rom(self, p): return 0x08000000 <= p < 0x08000000 + len(self.d)

    def entry(self, i):
        a = self.cfg["sprite_table"] + 20 * i
        e = self.bytes(a, 20)
        if e == bytes(20):
            return None
        return dict(id=i, address=a, width=e[0], height=e[1], raw=e[2:12].hex(" "), flags=e[2], n_anims=e[5],
                    type=e[10], frames_ptr=self.u32(a + 12), anims_ptr=self.u32(a + 16))

    # --- frame sources
    def frame_list(self, e):
        """Returns (source description, list of (frame address or None, bytes-like buffer, offset))."""
        if e["frames_ptr"] == 0:
            f = self.file_map.get(e["id"])
            if f is None:
                return {"source": "file", "file": None}, []
            fa = self.u32(self.cfg["file_table"] + 4 * f)
            buf = self.dec.decode(fa)
            offs = []
            while 4 * len(offs) + 4 <= len(buf):
                o = struct.unpack_from("<I", buf, 4 * len(offs))[0]
                if not o:
                    break
                offs.append(o)
            return {"source": "file", "file": f, "file_address": f"0x{fa:08X}"}, [(None, buf, o) for o in offs]
        p = e["frames_ptr"]
        nxt = next((s for s in self.list_starts if s > p), p + 4 * 64)
        frames = []
        for k in range(min((nxt - p) // 4, 256)):
            fa = self.u32(p + 4 * k)
            if not self.is_rom(fa) or fa < 0x08100000:
                break
            frames.append((fa, self.d, fa - 0x08000000))
        return {"source": "rom", "frames_list": f"0x{p:08X}"}, frames

    @staticmethod
    def rle(buf, pos, n):
        out = np.zeros(n, np.uint8)
        q = 0
        while pos < len(buf):
            x = buf[pos]
            pos += 1
            if x == 0:
                return out, q, True
            if x > 0xDF:
                q += x - 0xDF
            else:
                if q < n:
                    out[q] = x
                q += 1
        return out, q, False

    def decode_frame(self, e, fa, buf, off):
        """Returns (pixels h x w uint8 or None, status)."""
        w, h, t = e["width"], e["height"], e["type"]
        n = w * h
        if fa is None and off >= len(buf):  # GS2 file 543 lists two frames at the very end of the file
            return np.zeros((h, w), np.uint8), "empty"
        if t in (0, 2):  # GS2's dispatcher sends every type other than 1 and 3 to the plain RLE decoder
            px, q, done = self.rle(buf, off, n)
        elif t == 3:
            self.gba.write(BUF, bytes(0x4000))
            r = self.gba.call(self.cfg["stage1"] | 1, (fa, BUF), thumb=True, max_instructions=2_000_000)
            src = self.d if self.is_rom(r) else self.gba.read(BUF, 0x4000)
            px, q, done = self.rle(src, (r - 0x08000000) if self.is_rom(r) else r - BUF, n)
        elif t == 1:
            raw = self.dec.decode(fa)
            if len(raw) < n:
                return None, f"type 1: {len(raw)} bytes < {n}"
            # linear 8bpp rows (checked visually: a tile-order reading scrambles the summon pieces)
            px, q, done = np.frombuffer(raw[:n], np.uint8).copy(), n, True
        else:
            return None, f"type {t} not handled"
        if not done or q > n:
            return None, f"RLE ran {q}/{n} pixels, terminated={done}"
        return px.reshape(h, w), "ok"

    def remap(self, px, variant):
        if not variant:
            return px
        tab = np.frombuffer(self.bytes(self.cfg["remap"] + 0x100 * (min(variant, 5) - 1), 0x100), np.uint8).copy()
        tab[0] = 0
        tab[0xE0:] = np.arange(0xE0, 0x100)
        return tab[px]

    def sheet(self, frames, cols=8):
        """frames: list of h x w arrays (equal sizes). Returns RGBA image and frame rectangles."""
        h, w = frames[0].shape
        cols = min(cols, len(frames))
        rows = (len(frames) + cols - 1) // cols
        idx = np.zeros((rows * h, cols * w), np.uint8)
        rects = []
        for k, f in enumerate(frames):
            y, x = (k // cols) * h, (k % cols) * w
            idx[y:y + h, x:x + w] = f
            rects.append(dict(frame=k, x=x, y=y, w=w, h=h))
        rgba = np.dstack([self.rgb[idx], np.where(idx == 0, 0, 255).astype(np.uint8)])
        return Image.fromarray(rgba, "RGBA"), rects

    def anims(self, e):
        out, p = [], e["anims_ptr"]
        if not p:
            return out
        ptrs = [self.u32(p + 4 * k) for k in range(e["n_anims"])]
        for k, s in enumerate(ptrs):
            if not self.is_rom(s):
                break
            later = [x for x in ptrs + self.list_starts if x > s]
            end = min(later) if later else s + 32
            out.append(self.bytes(s, min(end - s, 64)).hex(" "))
        return out

    def decode_sprite(self, sid, variant=0):
        e = self.entries[sid] if 0 <= sid < len(self.entries) else None
        if e is None:
            return None, None, []
        src, flist = self.frame_list(e)
        frames, stats = [], []
        for k, (fa, buf, off) in enumerate(flist):
            px, st = self.decode_frame(e, fa, buf, off)
            stats.append(st)
            if px is not None:
                frames.append(self.remap(px, variant))
        return e, src, (frames, stats)


def slug_dir(rom):
    code = bytes(rom.data[0xAC:0xB0]).decode("ascii")
    sha = hashlib.sha1(rom.data).hexdigest()[:8]
    hits = sorted((ROOT / "games").glob(f"{code}-{sha}-*"))
    return hits[0] if hits else ROOT / "games" / f"{code}-{sha}"


def safe(s):
    return "".join(c if c.isalnum() else "_" for c in s).strip("_") or "unnamed"


CSS = ("body{font-family:system-ui,sans-serif;margin:16px;background:#1d1f24;color:#e8e8e8}"
       "h1,h2{font-weight:600}.grid{display:flex;flex-wrap:wrap;gap:10px}"
       "figure{margin:0;background:#2a2d34;border-radius:6px;padding:6px;max-width:100%}"
       "figure img{image-rendering:pixelated;max-width:100%;background:"
       "repeating-conic-gradient(#3a3d44 0 25%,#30333a 0 50%) 0 0/16px 16px}"
       "figcaption{font-size:12px;color:#b8bcc6;margin-top:4px}")


def export(rom_path):
    rom = Rom.load(rom_path)
    S = SpriteSet(rom)
    out = slug_dir(rom) / "battle_sprites"
    for sub in ("enemies", "sprites"):
        (out / sub).mkdir(parents=True, exist_ok=True)
        for old in (out / sub).glob("*.png"):
            old.unlink()

    # palette
    Image.fromarray(np.repeat(np.repeat(S.rgb[:224].reshape(14, 16, 3), 8, 0), 8, 1), "RGB").save(out / "palette.png")
    (out / "palette.json").write_text(json.dumps(dict(
        address=f"0x{S.cfg['palette']:08X}", colors=224, note="index 0 is transparent; BGR555 expanded to 8-bit",
        rgb=[[int(c) for c in x] for x in S.rgb[:224]]), indent=1), encoding="utf-8")

    # battle table
    bt = []
    for i in range(S.cfg["battle_count"]):
        a = S.cfg["battle_table"] + 8 * i
        r = S.bytes(a, 8)
        bt.append(dict(index=i, sprite=S.u16(a), flags=r[2], variant=(r[3] >> 1) & 15, byte3=r[3], byte4=r[4]))
    enemy_sprite_ids = {x["sprite"] for x in bt if x["sprite"]}
    two_part = set(S.cfg["two_part"])

    # every sprite-table entry
    sprites_json, cards_s, ok_s, frames_ok, frames_all = [], [], 0, 0, 0
    cache = {}
    for e in S.entries:
        if e is None:
            continue
        e2, src, (frames, stats) = S.decode_sprite(e["id"])
        cache[e["id"]] = (e2, src, frames, stats)
        frames_all += len(stats)
        frames_ok += sum(s in OK for s in stats)
        cat, who = category(S.code, e["id"], enemy_sprite_ids | {x + 1 for x in enemy_sprite_ids & two_part})
        rec = dict(id=e["id"], category=cat, character=who, width=e["width"], height=e["height"], type=e["type"],
                   table_bytes_2_11=e["raw"], n_anims=e["n_anims"], **src,
                   frames_total=len(stats), frames_ok=sum(s in OK for s in stats),
                   frame_errors={str(k): s for k, s in enumerate(stats) if s != "ok"},
                   anims_hex=S.anims(e), png=None, frame_rects=[])
        if frames and len(frames) == len(stats):
            img, rects = S.sheet(frames)
            name = f"{e['id']:04d}.png"
            img.save(out / "sprites" / name)
            rec.update(png=f"sprites/{name}", frame_rects=rects)
            ok_s += 1
            cards_s.append(f'<figure><img loading="lazy" src="sprites/{name}" alt=""><figcaption>#{e["id"]} {who or cat} '
                           f'{e["width"]}x{e["height"]}, {len(frames)} frames, type {e["type"]}</figcaption></figure>')
        elif frames:
            img, rects = S.sheet(frames)
            name = f"{e['id']:04d}_partial.png"
            img.save(out / "sprites" / name)
            rec.update(png=f"sprites/{name}")
        sprites_json.append(rec)

    # enemies
    ej =slug_dir(rom) / "data" / "enemies.json"
    enemies = json.loads(ej.read_text(encoding="utf-8"))["enemies"] if ej.exists() else []
    enemies_json, cards_e, ok_e = [], [], 0
    for en in enemies:
        bid = en.get("battle_id")
        rec = dict(id=en["id"], name=en.get("name"), battle_id=bid, png=None)
        if bid is None:
            rec["status"] = "no battle_id"
            enemies_json.append(rec)
            continue
        b = bt[bid] if bid < len(bt) else bt[0]  # the game clamps out-of-range ids to entry 0
        rec.update(battle_table_entry=b["index"], clamped=bid >= len(bt), sprite=b["sprite"], variant=b["variant"],
                   battle_flags=b["flags"], byte3=b["byte3"], byte4=b["byte4"])
        if b["sprite"] == 0 and b["flags"] == 0:
            # An all-zero entry (or a clamp to entry 0) means no battle sprite of its own; exporting sprite 0 would
            # show the field sprite of Isaac. Doom Dragon's side heads are like this (drawn with the main body).
            rec["status"] = "no sprite of its own (all-zero battle-table entry)"
            enemies_json.append(rec)
            continue
        parts = [b["sprite"]] + ([b["sprite"] + 1] if b["sprite"] in two_part else [])
        frames, stats = [], []
        for sid in parts:
            if sid not in cache or cache[sid][0] is None:
                stats.append(f"sprite {sid} empty")
                continue
            e, src, fr, st = cache[sid]
            frames += [S.remap(f, b["variant"]) for f in fr]
            stats += st
            rec.setdefault("sources", []).append(dict(sprite=sid, width=e["width"], height=e["height"], **src))
        rec["frames_total"], rec["frames_ok"] = len(stats), sum(s in OK for s in stats)
        if frames and all(s in OK for s in stats) and len({f.shape for f in frames}) == 1:
            img, rects = S.sheet(frames)
            name = f"{en['id']:03d}_{safe(en.get('name') or '')}.png"
            img.save(out / "enemies" / name)
            rec.update(png=f"enemies/{name}", frame_rects=rects, status="ok")
            ok_e += 1
            cards_e.append(f'<figure><img loading="lazy" src="enemies/{name}" alt=""><figcaption>{en["id"]} '
                           f'{escape(en.get("name") or "")} - sprite {b["sprite"]}'
                           f'{", swap " + str(b["variant"]) if b["variant"] else ""}</figcaption></figure>')
        elif frames and all(s in OK for s in stats):  # two parts of different sizes: one sheet per part
            names = []
            for j, sid in enumerate(parts):
                fr = [S.remap(f, b["variant"]) for f in cache[sid][2]]
                img, _ = S.sheet(fr)
                name = f"{en['id']:03d}_{safe(en.get('name') or '')}_part{j}.png"
                img.save(out / "enemies" / name)
                names.append(f"enemies/{name}")
            rec.update(png=names, status="ok (two parts)")
            ok_e += 1
            cards_e += [f'<figure><img loading="lazy" src="{n}" alt=""><figcaption>{en["id"]} '
                        f'{escape(en.get("name") or "")} part {j}</figcaption></figure>' for j, n in enumerate(names)]
        else:
            rec["status"] = "failed: " + "; ".join(sorted(set(s for s in stats if s not in OK)))
        enemies_json.append(rec)

    summary = dict(rom=str(rom_path), code=S.code, sprite_table=f"0x{S.cfg['sprite_table']:08X}",
                   sprite_entries=len(S.entries), sprite_entries_nonempty=sum(e is not None for e in S.entries),
                   sprites_exported_complete=ok_s, frames_ok=frames_ok, frames_total=frames_all,
                   battle_table=f"0x{S.cfg['battle_table']:08X}", battle_entries=len(bt),
                   enemies=len(enemies), enemies_exported=ok_e,
                   file_map={str(k): v for k, v in sorted(S.file_map.items())})
    (out / "sprites.json").write_text(json.dumps(dict(summary=summary, sprites=sprites_json), indent=1),
                                      encoding="utf-8")
    (out / "enemies.json").write_text(json.dumps(dict(summary=summary, battle_table=bt, enemies=enemies_json),
                                                 indent=1, ensure_ascii=False), encoding="utf-8")
    battle_cards = [c for c, s in zip(cards_s, [r for r in sprites_json if r["png"] and "partial" not in r["png"]])
                    if s["category"] != "field"]
    field_cards = [c for c, s in zip(cards_s, [r for r in sprites_json if r["png"] and "partial" not in r["png"]])
                   if s["category"] == "field"]
    (out / "index.html").write_text(
        "<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>{S.code} battle sprites</title><style>{CSS}</style><h1>{S.code} battle sprites</h1>"
        f"<p>Enemies exported: {ok_e} of {len(enemies)}. Sprite-table entries exported: {ok_s} of "
        f"{summary['sprite_entries_nonempty']} ({frames_ok} of {frames_all} frames). Colour 0 is transparent "
        f"(checkerboard).</p><h2>Enemies</h2><div class=grid>" + "\n".join(cards_e) +
        "</div><h2>Battle sprite-table entries (party, weapons, enemy bases)</h2><div class=grid>"
        + "\n".join(battle_cards) + "</div><h2>Field sprite-table entries</h2><div class=grid>"
        + "\n".join(field_cards) + "</div>", encoding="utf-8")
    return summary, out


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 1
    for p in argv:
        s, out = export(p)
        print(f"{s['code']}: enemies {s['enemies_exported']}/{s['enemies']}, sprite entries "
              f"{s['sprites_exported_complete']}/{s['sprite_entries_nonempty']}, frames {s['frames_ok']}/"
              f"{s['frames_total']} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
