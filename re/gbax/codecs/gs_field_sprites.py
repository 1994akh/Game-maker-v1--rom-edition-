"""Golden Sun 1 / 2 field (overworld) sprites: player, party, NPCs and objects, with their animations.

    python -m gbax.codecs.gs_field_sprites ROM [ROM2 ...]

Writes games/<slug>/field_sprites/:
    NNNN.png        sheet: every frame of sprite NNNN (row-major grid, real palette, colour 0 transparent); when an
                    animation shows a frame mirrored, a second block below holds the mirrored copy of every frame
    NNNN.json       frame rectangles + animations expanded per facing direction (walk_s, walk_se, ... idle_n),
                    each frame with its sheet region and a duration in 60 Hz frames (Godot SpriteFrames at 60 FPS)
    sprites.json    index: every field sprite, category, name, facing kind, actor uses (from the map exporter)
    palette.json    the 224-colour global sprite palette (shared with battle sprites)
    index.html      gallery with animated previews

Pipeline (see notes/gs_field_sprites.md; VERIFIED = ROM code / alchemy C that matches the ROM):
    sprite record (20 B, table GS1 0x08185024 / GS2 0x08300000; decoded by gs_battle_sprites.SpriteSet):
        +0 w, +1 h, +2 u16 scale, +4 facing kind, +5 n_anims, +6 s8 adjust_x, +7 s8 adjust_y, +8 box_x, +9 box_y,
        +10 codec, +12 frame list*, +16 animation list*
    animation script (Sprite_ComposeAnimationFrame, GS1 ~0x0800AC00, GS2 ~0x08021AF0): byte pairs (op, arg)
        op < 0xEF        show frame `op` (+ facing offset) for `arg` frames (timer += arg<<4, step 0x10/frame)
        F0 k             set the facing kind to k for the following frames (0x11 etc. = no facing)
        F1 x             hold the current frame forever (stop)
        F5 n             keep the current frame n more frames
        FD p             jump to byte offset p of this script (loop)
        FE a             switch to animation a (chain)
        FF n             hide the sprite for n frames
        EF x             hide and end
        F2/F3 (GS2: set object bytes +0x17/+0x16), FC (GS2: calls 0x081C0010(arg), likely a sound), others: no-op
    facing: frame = base + (table[kind][angle sector] & 7), mirrored horizontally when bit 7 is set.
"""
import json
import struct
import sys
from html import escape
from pathlib import Path

import numpy as np
from PIL import Image

from ..rom import Rom
from .gs_battle_sprites import SpriteSet, GAMES as BGAMES, category as battle_category, slug_dir

# Facing tables (VERIFIED: literal pools of the compose routine; GS1 0x0800AD48, GS2 0x08021E14..0x08021E28,
# GS2 kind dispatch jump table at 0x08021BE8). kind -> (table address, shift, centered)
FACING = {
    "AGSE": {1: (0x0801307C, 13, False), 22: (0x0801308C, 13, False), 2: (0x08013094, 13, False),
             20: (0x08013094, 13, False), 3: (0x0801309C, 12, False), 5: (0x080130AC, 12, False),
             8: (0x080130BC, 13, True), 88: (0x080130C4, 13, True), 4: (0x080130CC, 10, False),
             6: (0x0801310C, 10, False)},
    "AGFE": {1: (0x0802EAC4, 13, False), 22: (0x0802EAD4, 13, False), 2: (0x0802EADC, 13, False),
             20: (0x0802EADC, 13, False), 3: (0x0802EAE4, 12, False), 5: (0x0802EB04, 10, False),
             8: (0x0802EB44, 13, True)},
}
# Facing angle: u16, 0 = east, 0x4000 = south (down the screen). VERIFIED (gs_movement.md, d-pad table).
DIRS = [("e", 0x0000), ("se", 0x2000), ("s", 0x4000), ("sw", 0x6000), ("w", 0x8000), ("nw", 0xA000),
        ("n", 0xC000), ("ne", 0xE000)]
# Animation numbers. 1/2/3/4/11/19: alchemy FIELD_EVENT.H names; 2 walk / 5 run / 8 push: chosen by the on-foot
# controller GS1 0x0800EBEC (VERIFIED for the player). 0 'still' is INFERRED from its script (one frame, hold).
ANIM_NAMES = {0: "still", 1: "idle", 2: "walk", 3: "nod", 4: "shake_head", 5: "run", 8: "push", 11: "hammer",
              19: "sprawled"}
# Party field sprites: INFERRED from the decoded sheets (checked visually), not from code.
PARTY = {
    "AGSE": {0: "Isaac", 1: "Garet", 2: "Ivan", 3: "Mia", 5: "Jenna", 6: "Felix"},
    "AGFE": {0: "Isaac", 1: "Garet", 2: "Ivan", 3: "Mia", 4: "Felix", 5: "Jenna", 6: "Sheba", 7: "Piers"},
}
TERMINATORS = (0xF1, 0xFD, 0xFE, 0xEF)


def s8(b):
    return b - 256 if b > 127 else b


class FieldSprites:
    def __init__(self, rom):
        self.ss = SpriteSet(rom)
        self.code = self.ss.code
        self.facing = {}
        for k, (a, sh, cen) in FACING[self.code].items():
            n = 1 << (16 - sh)
            self.facing[k] = (list(self.ss.bytes(a, n)), sh, cen, a)

    # --- facing
    def facing_attr(self, kind, angle):
        f = self.facing.get(kind)
        if f is None:
            return 0
        tab, sh, cen, _ = f
        a = (angle + (1 << (sh - 1)) if cen else angle) & 0xFFFF
        return tab[(a >> sh) & (len(tab) - 1)]

    # --- scripts
    def scripts(self, e):
        out, p = [], e["anims_ptr"]
        if not p:
            return out
        for k in range(e["n_anims"]):
            s = self.ss.u32(p + 4 * k)
            if not self.ss.is_rom(s):
                out.append(None)
                continue
            b, q = [], s
            while len(b) < 512:
                op, arg = self.ss.bytes(q, 2)
                b += [op, arg]
                q += 2
                if op in TERMINATORS:
                    break
            out.append(bytes(b))
        return out

    def run_script(self, script, kind0, angle, nframes):
        """Expands one script for one facing angle. Returns dict(frames=[(frame, flip, dur)], loop_start, next,
        end) where frame None means hidden. The pairs are followed once; FD gives the loop start."""
        seq, kind, pos, starts = [], kind0, 0, {}
        res = dict(loop_start=None, next=None, end="hold", errors=[])
        steps = 0
        while pos + 1 < len(script) and steps < 256:
            steps += 1
            starts.setdefault(pos, len(seq))
            op, arg = script[pos], script[pos + 1]
            pos += 2
            if op == 0xF0:
                kind = arg
            elif op == 0xF5:
                if seq:
                    seq[-1][2] += arg
            elif op == 0xFF:
                seq.append([None, False, arg])
            elif op == 0xEF:
                res["end"] = "hide"
                break
            elif op == 0xF1:
                res["end"] = "hold"
                break
            elif op == 0xFD:
                res["end"] = "loop"
                res["loop_start"] = starts.get(arg, 0)
                break
            elif op == 0xFE:
                res["end"] = "next"
                res["next"] = arg & 0x7F
                break
            elif op in (0xF2, 0xF3, 0xF4, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFC):
                continue
            else:
                attr = self.facing_attr(kind, angle)
                f = op + (attr & 7)
                if f >= nframes:
                    res["errors"].append(f"frame {f} >= {nframes}")
                seq.append([f, bool(attr & 0x80), arg])
        res["frames"] = seq
        res["kinds_used"] = kind
        return res

    def directional(self, script, kind0):
        """True if any shown frame depends on the facing angle."""
        kind = kind0
        for i in range(0, len(script) - 1, 2):
            op = script[i]
            if op == 0xF0:
                kind = script[i + 1]
            elif op < 0xEF and kind in self.facing:
                return True
        return False

    # --- decoding
    def frames(self, e):
        src, flist = self.ss.frame_list(e)
        out, stats = [], []
        for fa, buf, off in flist:
            try:
                px, st = self.ss.decode_frame(e, fa, buf, off)
            except Exception as ex:  # emulator failure on a bad frame
                px, st = None, f"error {ex}"
            stats.append(st)
            out.append(px if px is not None else np.zeros((e["height"], e["width"]), np.uint8))
        return src, out, stats


def field_ids(ss, actor_ids=()):
    """Sprite-table ids outside the battle groups of gs_battle_sprites, plus every id a map actor uses (e.g. GS1
    sprite 0, which the battle table's clamp entry also names, and GS1 396-399)."""
    cfg = BGAMES[ss.code]
    enemy = set()
    for i in range(cfg["battle_count"]):
        enemy.add(ss.u16(cfg["battle_table"] + 8 * i))
    for t in cfg["two_part"]:
        enemy.add(t + 1)
    return [e["id"] for e in ss.entries
            if e and (battle_category(ss.code, e["id"], enemy)[0] == "field" or e["id"] in actor_ids)]


def actor_uses(slug):
    """sprite id -> number of map actors that use it (from gbax.codecs.gs_maps output), plus two-part ids."""
    uses, two = {}, set()
    for p in sorted((slug / "maps" / "rooms").glob("*/events.json")):
        try:
            j = json.loads(p.read_text())
        except (OSError, ValueError):
            continue
        for a in j.get("actors", []):
            v = a.get("sprite")
            if v is None or v == 0xFFFF:
                continue
            sid, kind = v & 0xFFF, v >> 12
            uses.setdefault(sid, {"actors": 0, "rooms": set()})
            uses[sid]["actors"] += 1
            uses[sid]["rooms"].add(j.get("room"))
            if kind == 2:
                two.add(sid)
    return uses, two


def build_sheet(fs, frames, cols, need_mirror):
    h, w = frames[0].shape
    rows = (len(frames) + cols - 1) // cols
    idx = np.zeros((rows * h * (2 if need_mirror else 1), cols * w), np.uint8)
    rects = []
    for k, f in enumerate(frames):
        y, x = (k // cols) * h, (k % cols) * w
        idx[y:y + h, x:x + w] = f
        if need_mirror:
            idx[rows * h + y:rows * h + y + h, x:x + w] = f[:, ::-1]
        rects.append(dict(frame=k, x=x, y=y, w=w, h=h))
    rgba = np.dstack([fs.ss.rgb[idx], np.where(idx == 0, 0, 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA"), rects, rows * h


def export(rom_path):
    rom = Rom.load(rom_path) if hasattr(Rom, "load") else Rom(rom_path)
    fs = FieldSprites(rom)
    code = fs.code
    slug = slug_dir(rom)
    out = slug / "field_sprites"
    out.mkdir(parents=True, exist_ok=True)
    uses, two_part = actor_uses(slug)
    ids = field_ids(fs.ss, set(uses))
    index, cov = [], dict(sprites=0, frames=0, frames_ok=0, anims=0, anim_errors=0, empty=0)
    previews = {}
    for sid in ids:
        e = fs.ss.entries[sid]
        raw = fs.ss.bytes(e["address"], 20)
        kind = raw[4]
        src, frames, stats = fs.frames(e)
        scripts = fs.scripts(e)
        if not frames:
            cov["empty"] += 1
            index.append(dict(id=sid, width=e["width"], height=e["height"], frames=0, note="no frames",
                              actor_uses=uses.get(sid, {}).get("actors", 0)))
            continue
        cov["sprites"] += 1
        cov["frames"] += len(frames)
        cov["frames_ok"] += sum(s in ("ok", "empty") for s in stats)
        # expand animations
        anims, need_mirror = [], False
        for n, sc in enumerate(scripts):
            if sc is None:
                continue
            base_name = ANIM_NAMES.get(n, f"anim_{n:02d}") if kind in (3, 4, 5, 6, 8, 88) or sid in PARTY[code] \
                else f"anim_{n:02d}"
            dirs = DIRS if fs.directional(sc, kind) else [(None, 0x4000)]
            for dname, ang in dirs:
                r = fs.run_script(sc, kind, ang, len(frames))
                need_mirror |= any(f[1] for f in r["frames"])
                cov["anims"] += 1
                cov["anim_errors"] += bool(r["errors"])
                anims.append(dict(name=f"{base_name}_{dname}" if dname else base_name, script=n,
                                  direction=dname, angle=ang if dname else None, frames=r["frames"],
                                  end=r["end"], loop_start=r["loop_start"], next=r["next"],
                                  errors=r["errors"], script_hex=sc.hex(" ")))
        cols = {5: 5, 3: 3, 8: 8}.get(kind, 8 if len(frames) >= 8 else len(frames))
        img, rects, mirror_y = build_sheet(fs, frames, cols, need_mirror)
        img.save(out / f"{sid:04d}.png")
        # resolve regions; name resolution for 'next'
        names_by_script = {}
        for a in anims:
            names_by_script.setdefault(a["script"], {})[a["direction"]] = a["name"]
        janims = []
        for a in anims:
            fr = []
            for f, flip, dur in a["frames"]:
                if f is None or f >= len(rects):
                    fr.append(dict(frame=None, hidden=f is None, flip_h=False, region=None, duration=dur))
                    continue
                rc = rects[f]
                fr.append(dict(frame=f, flip_h=flip, duration=dur,
                               region=[rc["x"], rc["y"] + (mirror_y if flip else 0), rc["w"], rc["h"]]))
            nxt = None
            if a["next"] is not None:
                tgt = names_by_script.get(a["next"], {})
                nxt = tgt.get(a["direction"]) or tgt.get(None) or (next(iter(tgt.values())) if tgt else None)
            janims.append(dict(name=a["name"], script=a["script"], direction=a["direction"], angle=a["angle"],
                               fps=60, loop=a["end"] == "loop", loop_start=a["loop_start"], end=a["end"],
                               next=nxt, next_script=a["next"], frames=fr, errors=a["errors"],
                               script_hex=a["script_hex"]))
        name = PARTY[code].get(sid)
        multi = kind in (3, 4, 5, 6, 8, 88)
        cat = "party" if name else ("person" if multi and len(scripts) >= 3 else "object")
        u = uses.get(sid, {})
        meta = dict(id=sid, game=code, name=name, category=cat, width=e["width"], height=e["height"],
                    record=dict(address=f"0x{e['address']:08X}", raw=raw.hex(" "), scale=struct.unpack_from("<H", raw, 2)[0],
                                facing_kind=kind, n_anims=raw[5], adjust_x=s8(raw[6]), adjust_y=s8(raw[7]),
                                box_x=raw[8], box_y=raw[9], codec=raw[10]),
                    source=src, frame_status=stats, sheet=f"{sid:04d}.png", sheet_size=list(img.size),
                    columns=cols, mirrored_block_y=mirror_y if need_mirror else None, frames=rects,
                    facing=dict(kind=kind, table=f"0x{fs.facing[kind][3]:08X}" if kind in fs.facing else None,
                                values=[f"0x{x:02X}" for x in fs.facing[kind][0]] if kind in fs.facing else None,
                                sector_shift=fs.facing[kind][1] if kind in fs.facing else None),
                    animations=janims, actor_uses=u.get("actors", 0), actor_rooms=sorted(r for r in u.get("rooms", ()) if r is not None),
                    two_part_actor=sid in two_part)
        (out / f"{sid:04d}.json").write_text(json.dumps(meta, indent=1))
        index.append(dict(id=sid, name=name, category=cat, width=e["width"], height=e["height"],
                          frames=len(frames), facing_kind=kind, animations=len(scripts),
                          actor_uses=u.get("actors", 0), sheet=f"{sid:04d}.png", json=f"{sid:04d}.json",
                          bad_frames=sum(s not in ("ok", "empty") for s in stats)))
        pv = next((a for a in janims if a["name"] in ("walk_s", "walk_se")), None) or \
            next((a for a in janims if a["frames"] and all(f["region"] for f in a["frames"])), None)
        if pv:
            previews[sid] = dict(n=pv["name"], f=[f["region"] + [f["duration"]] for f in pv["frames"] if f["region"]])
    used = set(uses)
    exported = {i["id"] for i in index if i.get("frames")}
    cats = {}
    for i in index:
        cats[i.get("category", "none")] = cats.get(i.get("category", "none"), 0) + 1
    summary = dict(game=code, sprite_table=f"0x{BGAMES[code]['sprite_table']:08X}", field_sprite_ids=len(ids),
                   coverage=cov, categories=cats,
                   actor_sprites=dict(distinct=len(used), exported=len(used & exported),
                                      missing=sorted(used - exported)),
                   directions=[d for d, _ in DIRS], anim_names=ANIM_NAMES, sprites=index)
    (out / "sprites.json").write_text(json.dumps(summary, indent=1))
    pal = fs.ss.rgb[:0xE0]
    (out / "palette.json").write_text(json.dumps(dict(colors=[f"#{r:02X}{g:02X}{b:02X}" for r, g, b in pal],
                                                      transparent_index=0)))
    write_html(out, code, summary, previews)
    return summary


def write_html(out, code, summary, previews):
    c = summary["coverage"]
    rows = []
    for s in summary["sprites"]:
        if not s.get("frames"):
            continue
        label = f"{s['id']:04d}" + (f" {escape(s['name'])}" if s.get("name") else "")
        rows.append(
            f"<div class='c {s['category']}'><div class='h'>{label}</div>"
            f"<canvas id='p{s['id']}' width='{s['width']*2}' height='{s['height']*2}'></canvas>"
            f"<div class='m'>{s['category']} · {s['width']}×{s['height']} · {s['frames']} fr · kind {s['facing_kind']}"
            f" · {s['animations']} anims · actors {s['actor_uses']}</div>"
            f"<a href='{s['json']}'>json</a> <a href='{s['sheet']}'>sheet</a>"
            f"<details><summary>sheet</summary><img src='{s['sheet']}'></details></div>")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{code} field sprites</title><style>
body{{font-family:system-ui,sans-serif;margin:16px;background:#1d1f24;color:#e8e8e8}}
.g{{display:flex;flex-wrap:wrap;gap:8px}}.c{{background:#2a2d34;padding:6px;border-radius:6px;font-size:12px;max-width:100%}}
.party{{outline:2px solid #e0b040}}.h{{font-weight:600}}.m{{color:#aaa}}canvas{{image-rendering:pixelated;background:#3a3f48}}
img{{image-rendering:pixelated;max-width:100%;background:#3a3f48}}a{{color:#8cf}}
</style></head><body><h1>{code} field sprites</h1>
<p>{c['sprites']} sprites, {c['frames_ok']}/{c['frames']} frames decoded, {c['anims']} animations
({c['anim_errors']} with errors). Map actors use {summary['actor_sprites']['distinct']} sprite ids, {summary['actor_sprites']['exported']} exported.
Previews play walk_s (or the first animation) at 60 FPS.</p>
<div class="g">{''.join(rows)}</div>
<script>const P={json.dumps(previews, separators=(',', ':'))};
for(const [id,a] of Object.entries(P)){{const cv=document.getElementById('p'+id);if(!cv||!a.f.length)continue;
const ctx=cv.getContext('2d');ctx.imageSmoothingEnabled=false;const im=new Image();im.src=String(id).padStart(4,'0')+'.png';
let i=0,t=0;function draw(){{const f=a.f[i];ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage(im,f[0],f[1],f[2],f[3],0,0,f[2]*2,f[3]*2);}}
im.onload=()=>{{draw();setInterval(()=>{{t++;if(t>=Math.max(1,a.f[i][4])){{t=0;i=(i+1)%a.f.length;draw();}}}},1000/60);}};}}
</script></body></html>"""
    (out / "index.html").write_text(html, encoding="utf-8")


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    for p in argv:
        s = export(p)
        c = s["coverage"]
        print(f"{s['game']}: {c['sprites']} sprites, frames {c['frames_ok']}/{c['frames']}, anims {c['anims']} "
              f"(errors {c['anim_errors']}), categories {s['categories']}, actor sprites "
              f"{s['actor_sprites']['exported']}/{s['actor_sprites']['distinct']} missing {s['actor_sprites']['missing'][:20]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
