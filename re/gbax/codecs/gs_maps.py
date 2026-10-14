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


# --- actors (added 14 Oct; see notes/gs_maps.md "Actors and puzzle objects") ---------------------------------------
# Main-image far-call veneers that room code reaches through its own import veneers (`ldr r4,[pc]; bx r4; .word f`):
#   reset   = Event_RunObjectHookAndWait(table): rebuilds the actor table from `table`, rows from slot 8
#   extra   = Event_CallWithLastActiveObjectId(table): spawns `table` from the slot after the last occupied one
#   prepare = Scene_AssignViewFlags(table): rows with condition 0 get flag 0x164 (inside the camera bounds: shown) or
#             0x165 (outside: not spawned at load)
# GS1 VERIFIED: veneer words at 0x0808A028/30/38 -> 0x08091780 / 0x080917AC / 0x0808B868, matching alchemy's
# decompile (SRC/FIELD/COMMON/EVENT/EVENT.C, OBJECT/OBJECT3.C, BATTLE/EFFECT/EFFECT26.C). GS2: the same three entries
# of alchemy's TLA far-call table at 0x080C8008 (INFERRED from that table's order).
FAR_ACTOR_CALLS = {"AGSE": {0x0808A028: "reset", 0x0808A030: "extra", 0x0808A038: "prepare"},
                   "AGFE": {0x080C8028: "reset", 0x080C8030: "extra", 0x080C8038: "prepare"}}
FIRST_PLACED_SLOT = 8            # ACTOR_FIRST_PLACED: slots 0-7 belong to party ids (GS1 0x0808B3EC, VERIFIED)
LAST_SLOT = 65                   # the actor table at field-state +0x14 holds slots 0..65


def flag_scope(flag):
    """Lifetime of a game flag. VERIFIED: GS1 0x0808AB74 / GS2 0x080C9C38 (Scene_ResetFlagsOnEnter)."""
    if flag is None or flag in (0xFFFF, -1):
        return None
    f = flag & 0xFFF
    if 0x80 <= f <= 0xDF:
        return "visit"           # cleared on every room entry (djinn 'fled' flags = djinn flag + 0x50 live here)
    if 0x200 <= f <= 0x2FF:
        return "room"            # cleared on every room entry (unless the load keeps state)
    if 0x300 <= f <= 0x3FF:
        return "place_group"     # cleared when entering a room of another place group (room table byte 2)
    if f in (0x164, 0x165):
        return "view"            # set by Scene_AssignViewFlags for camera-streamed actors
    return "saved"               # the whole 0x200-byte flag block at 0x02000040 is in the save


def decode_condition(c):
    """Placement/event condition word: 0xFFFF always; bit 0x1000 set -> while flag set; else while flag clear."""
    if c in (0xFFFF, -1):
        return {"show": "always"}
    d = {"flag": c & 0xFFF, "show": "while_set" if c & 0x1000 else "while_clear", "scope": flag_scope(c)}
    if not c & 0x1000 and 0x30 <= c <= 0x7F:
        d["also_while_clear"] = c + 0x50        # djinn rows: hidden once caught (c) or fled this visit (c + 0x50)
    if c == 0:
        d["show"] = "always_view_streamed"      # flag 0 is never set; with 'prepare' the camera decides (0x164/0x165)
    return d


def placement_rows(code, off, start_slot=FIRST_PLACED_SLOT, limit=80):
    """Decode a placement table (24-byte ScenePlacement rows ending at id -1) the way Event_SpawnObjectTable
    (GS1 0x0808B3EC) numbers them: ids 0-7 are party members in their own slot; ids 8..0x2705 take the next slot from
    `start_slot` whether or not their condition holds; larger ids keep the previous slot."""
    rows, slot, prev = [], start_slot, None
    o = off
    while o + 24 <= len(code) and u16(code, o) != 0xFFFF and len(rows) < limit:
        sid, cond = u16(code, o), u16(code, o + 2)
        sid_s = sid - 0x10000 if sid & 0x8000 else sid
        if sid_s <= 7:
            s, party = sid_s, True
        elif sid_s <= 0x2705:
            s, party, slot = slot, False, slot + 1
        else:
            s, party = prev, False
        prev = s
        beh = u32(code, o + 4)
        x, y, z = s32(code, o + 8) / 65536, s32(code, o + 12) / 65536, s32(code, o + 16) / 65536
        r = {"index": len(rows), "slot": s, "party_member": party, "sprite": sid, "sprite_id": sid & 0xFFF,
             "sprite_parts": 2 if sid >> 12 == 2 else 1, "flag": cond, "condition": decode_condition(cond),
             "behavior": f"0x{beh:08X}" if beh >= 0x10000 else beh,
             "behavior_kind": {1: "stand", 2: "wander"}.get(beh, "script" if CODE_BASE <= beh < CODE_BASE + 0x10000
                                                              else "engine"),
             "x": x, "y": y, "z": z, "tile": [int(x) // 16, int(z) // 16], "angle": u16(code, o + 20),
             "talk_facing": code[o + 22], "share_prev_sprite": bool(code[o + 23] & 1),
             # raw fields kept for earlier consumers
             "b4": code[o + 4], "b5_7": code[o + 5:o + 8].hex(), "b22": code[o + 22], "b23": code[o + 23]}
        if s is not None and s > LAST_SLOT:
            r["note"] = "beyond slot 65: the spawner stops before this row"
        if sid_s > 0x2705:
            r["note"] = "id > 0x2705: the spawner keeps the previous slot"
        rows.append(r)
        o += 24
    return rows


def scan_actor_calls(code, far_calls):
    """Static scan of a room's Thumb code for the calls that spawn actor tables. Finds the room's import veneers whose
    target is one of `far_calls`, then a linear disassembly tracks literal loads into r0 (`ldr rX,=lit`, `adds/mov
    r0,rX`) up to each `bl` to such a veneer. Returns [(kind, r0 value or None, call site)]."""
    import capstone
    ven = {}
    for o in range(0, len(code) - 7, 2):
        if u32(code, o) == STUB and (u32(code, o + 4) & ~1) in far_calls:
            ven[CODE_BASE + o] = far_calls[u32(code, o + 4) & ~1]
    if not ven:
        return []
    md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)
    out, o, regs = [], 0, {}
    while o < len(code) - 1:
        n = 0
        for ins in md.disasm(code[o:], CODE_BASE + o):
            n += ins.size
            m, ops = ins.mnemonic, ins.op_str
            parts = [p.strip() for p in ops.split(",")] if ops else []
            if m == "ldr" and "[pc, #" in ops:
                lit = ((ins.address + 4) & ~3) + int(ops.split("#")[1].rstrip("]"), 0)
                if CODE_BASE <= lit <= CODE_BASE + len(code) - 4:
                    regs[parts[0]] = u32(code, lit - CODE_BASE)
                else:
                    regs.pop(parts[0], None)
            elif m in ("adds", "mov", "movs") and ((len(parts) == 2 and parts[1] in regs)
                                                    or (len(parts) == 3 and parts[2] == "#0" and parts[1] in regs)):
                regs[parts[0]] = regs[parts[1]]
            elif m == "bl":
                tgt = int(ops.lstrip("#"), 0)
                if tgt in ven:
                    out.append((ven[tgt], regs.get("r0"), ins.address))
                for r_ in ("r0", "r1", "r2", "r3"):
                    regs.pop(r_, None)
            elif m.startswith("pop") or m == "bx" or (m == "push" and "lr" in ops):
                regs = {}
            elif parts and not m.startswith(("str", "cmp", "b", "tst", "push")):
                regs.pop(parts[0], None)
        o += max(n, 2)
        if n == 0:
            regs = {}
    return out


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


# --- tile animation (map polish, 14 Oct) ----------------------------------------------------------------------------
# Area part +0x30 (GS1) / +0x34 (GS2) is a tile-animation script, decoded to 0x0202D000 and started by
# MapAnimation_StartChannels (GS1 0x080118D8; alchemy SRC\FIELD\COMMON\MAP\MAP3.C). VERIFIED by disassembly of the GS1
# update routine 0x0801179C (scheduled every frame):
#   start list: u16 words up to the first 0xFFFF; 0xFDnn starts channel nn&15 on the words after it, paused if bit 7.
#   channel:    [src, count, dst, wait] copies `count` 8x8 chars from char src to char dst, then waits `wait` frames
#               (0 = the next command runs in the same frame); 0xFFFF restarts the channel; 0xFEnn jumps to
#               start + nn*4 bytes; 0xFEFF stops it (the cursor stays on it).
#   chars are counted from VRAM 0x06004000, i.e. exactly this exporter's vram[] index (tile number + char_block*512).
#   src >= 0x600 reads EWRAM 0x0201C000 + src*32 instead (literal at GS1 0x0801189C) = 0x02028000+, the 4th tileset
#   block, which never sits in BG VRAM (0x06010000 is OBJ VRAM): it only holds animation frames.
# The first copy of every running channel happens on the first field frame (timer starts at 0), so the base map shows
# frame 0 of each animation. Many placeholder tiles (e.g. GS1 Mercury Lighthouse's solid red blocks) are animation
# destinations that are never seen in their stored form.
GBA_FPS = 59.7275
ANIM_MAX_FRAMES = 8192              # cycle search per channel
ANIM_MAX_SPAN = 3600                # cap on a combined (LCM) cycle exported as one Tiled animation
ANIM_MAX_KEYS = 120                 # cap on keyframes per exported tile


def anim_channels(data):
    """Part bytes -> (u16 words, [{channel, paused, start}]). Mirrors the engine's start-list scan exactly."""
    w = struct.unpack_from(f"<{len(data) // 2}H", data)
    ch = {}
    i = 0
    while i < len(w) and w[i] != 0xFFFF:
        if w[i] & 0xFF00 == 0xFD00:
            ch[w[i] & 15] = {"channel": w[i] & 15, "paused": bool(w[i] & 0x80), "start": i + 1}
        i += 1
    return w, [ch[k] for k in sorted(ch)]


def anim_run(w, start, nframes=ANIM_MAX_FRAMES):
    """Run one channel like MapAnimation_Update -> (copies [(frame, src, count, dst)], cycle_start, period, how).
    how: loop (state repeats: frames >= cycle_start repeat every period), stop (0xFEFF), runaway or cap."""
    cur, timer, ev, seen = start, 0, [], {}
    for f in range(nframes):
        k = (cur, timer)
        if k in seen:
            return ev, seen[k], f - seen[k], "loop"
        seen[k] = f
        guard = 0
        while True:
            if timer:
                timer -= 1
                break
            guard += 1
            if guard > 4096 or cur >= len(w):
                return ev, f, 0, "runaway"
            op = w[cur]
            if op == 0xFFFF:
                cur = start
                continue
            if op & 0xFF00 == 0xFE00:
                if op & 0xFF == 0xFF:
                    return ev, f + 1, 0, "stop"
                cur = start + (op & 0xFF) * 2
                continue
            if cur + 3 >= len(w):
                return ev, f, 0, "runaway"
            ev.append((f, op, w[cur + 1], w[cur + 2]))
            timer = w[cur + 3]
            cur += 4
    return ev, nframes, 0, "cap"


def anim_schedule(runs, chans, end):
    """Copies of the given channels for frames [0, end), repeating each loop, in engine order -> {frame: [(s,n,d)]}."""
    by = {}
    for c in sorted(chans):
        ev, p0, P, how = runs[c]
        for (f, s, n, d) in ev:
            if f < end:
                by.setdefault(f, []).append((c, s, n, d))
        if how == "loop" and P:
            cyc = [e for e in ev if e[0] >= p0]
            k = 1
            while p0 + k * P < end:
                for (f, s, n, d) in cyc:
                    if f + k * P < end:
                        by.setdefault(f + k * P, []).append((c, s, n, d))
                k += 1
    return {f: [(s, n, d) for (c, s, n, d) in sorted(v, key=lambda e: e[0])] for f, v in sorted(by.items())}


def anim_apply(state, copies):
    """Forward char copies (DMA order). state: char -> source char whose stored bytes it now shows."""
    for (s, n, d) in copies:
        for i in range(n):
            state[d + i] = state.get(s + i, s + i)


def min_period(seq):
    """Shortest prefix that repeats to give seq (list of (key, frames))."""
    n = len(seq)
    for p in range(1, n + 1):
        if n % p == 0 and all(seq[i] == seq[i % p] for i in range(n)):
            return seq[:p]
    return seq


# --- display blend script (map polish, 14 Oct) ----------------------------------------------------------------------
# GS1 part +0x34 / GS2 part +0x38, decoded to 0x0202DE00 and run every frame by DisplayBlend_RunScript (alchemy
# SRC\GRAPHICS\DISPLAY\DISPLAY4.C; started by DisplayBlend_StartScript, which ignores a script that is just 0xFFFF).
# Words: 0x3nnn = write BLDCNT (and continue at once); any other value is written to BLDALPHA when BLDCNT's mode is
# alpha (0x40), else to BLDY, and the next word is the wait in frames; 0xFFFF restarts; 0xFEnn jumps to start + nn*4
# bytes; 0xFEFF stops. Typical: 0x3F42 = BG1 (layer 2) blended over everything, EVB 16 and EVA pulsing 5..12, i.e.
# an additive glow. That is what the "placeholder" red/black radial blocks on GS1 Mercury Lighthouse layer 2 are
# (area 56): glow lights, not missing graphics. GS2's old "4-byte +0x38 form" reading was wrong: it is this script.
def parse_blend_script(data):
    w = struct.unpack_from(f"<{len(data) // 2}H", data)
    if not w or w[0] == 0xFFFF:
        return None
    bc, steps, i, end = None, [], 0, "runaway"
    while i < len(w) and len(steps) < 256:
        v = w[i]
        if v == 0xFFFF:
            end = "restart"
            break
        if v & 0xFF00 == 0xFE00:
            end = "stop" if v & 0xFF == 0xFF else f"jump {(v & 0xFF) * 2}"
            break
        if v & 0xF000 == 0x3000:
            bc = v
            i += 1
            continue
        st = {"bldcnt": bc, "frames": w[i + 1] if i + 1 < len(w) else 0}
        if bc is not None and bc & 0xC0 == 0x40:
            st.update(bldalpha=v, eva=min(v & 31, 16), evb=min((v >> 8) & 31, 16))
        else:
            st.update(bldy=v, evy=min(v & 31, 16))
        steps.append(st)
        i += 2
    if not steps:
        return None
    first = steps[0]
    bc0 = first["bldcnt"] or 0
    return {"bldcnt": bc0, "mode": (bc0 >> 6) & 3, "first": [(bc0 >> k) & 1 for k in range(6)],
            "second": [(bc0 >> (8 + k)) & 1 for k in range(6)], "eva": first.get("eva", 16), "evb": first.get("evb", 0),
            "evy": first.get("evy", 0), "first_target_layers": [3 - k for k in (1, 2, 3) if (bc0 >> k) & 1],
            "steps": steps, "end": end}


# --- height shapes (map polish, 14 Oct) -----------------------------------------------------------------------------
# Cell byte 3 indexes the area's shape table (part +0x28 -> 0x0202C000, 4 B/shape). Byte 0 low nibble picks one of 16
# functions; bytes 1-3 are heights h0..h2 in 8 px units (signed, except GS1 fn 11 which reads them unsigned). The
# function gets (x & 15, z & 15) and returns the ground height. VERIFIED by disassembly: GS1 table 0x080134FC
# (functions 0x08011CE0-0x08011F48), GS2 table 0x0802EFC4 (0x0802D23C-0x0802D45A). GS1 and GS2 agree on 0-9 and
# 12-13; they differ on 10, 11, 14 and 15. Divisions truncate toward zero, like the game's.
SHAPE_TABLES = {1: (0x132FC, 0x133FC, 0x134FC), 2: (0x2EDC4, 0x2EEC4, 0x2EFC4)}   # round mask, diag3 index, fn table
SHAPE_NAMES = {
    1: ["flat", "slope_x", "slope_z", "step_diag_tl_br", "step_diag_tr_bl", "slope_diag_x_plus_z_2seg",
        "slope_diag_z_minus_x_2seg", "round_mask", "step_x8", "step_z8", "slope_x_2seg", "slope_z_2seg_unsigned",
        "diag3", "diag3_mirror_x", "flat", "flat"],
    2: ["flat", "slope_x", "slope_z", "step_diag_tl_br", "step_diag_tr_bl", "slope_diag_x_plus_z_2seg",
        "slope_diag_z_minus_x_2seg", "round_mask", "step_x8", "step_z8", "diag3_transposed",
        "diag3_transposed_mirror", "diag3", "diag3_mirror_x", "quad_tl_tr_bottom", "quad_top_bl_br"]}


def _tdiv(a, b):
    q = abs(a) // b
    return q if a >= 0 else -q


def shape_height_px(gs, fn, hb, x, z, round_mask, diag3):
    """Reference port of the 16 terrain-height functions. hb = the three raw shape bytes 1..3; x, z = 0..15 inside the
    cell; round_mask/diag3 = the two 256-byte tables (SHAPE_TABLES). Returns the ground height in px (the game works in
    16.16 fixed point; results are exact multiples of 1/65536 px)."""
    s = [((b ^ 0x80) - 0x80) * 8 for b in hb]           # signed, px
    h0, h1, h2 = s
    F = 65536
    H0, H1, H2 = h0 * F, h1 * F, h2 * F
    if fn == 0 or (gs == 1 and fn in (14, 15)):
        return h0
    if fn == 1:
        return (H0 + _tdiv((H1 - H0) * x, 16)) / F
    if fn == 2:
        return (H0 + _tdiv((H1 - H0) * z, 16)) / F
    if fn in (3, 4):
        t = x + z if fn == 3 else z - x + 15
        return max(h0, h1) if t == 15 else (h0 if t <= 14 else h1)
    if fn == 5:
        t = x + z
        if t == 15:
            return h1
        return (H0 + _tdiv((H1 - H0) * t, 15)) / F if t <= 14 else (H1 + _tdiv((H2 - H1) * (t - 15), 15)) / F
    if fn == 6:
        t = z - x + 15
        if t == 15:
            return h1
        return (H0 + _tdiv((H1 - H0) * t, 16)) / F if t <= 14 else (H1 + _tdiv((H2 - H1) * (z - x), 16)) / F
    if fn == 7:
        return h0 + (h1 - h0) * round_mask[z * 16 + x]
    if fn == 8:
        return h0 if x <= 7 else h1
    if fn == 9:
        return h0 if z <= 7 else h1
    if fn == 12:
        return s[diag3[z * 16 + x]]
    if fn == 13:
        return s[diag3[z * 16 + 15 - x]]
    if gs == 1:
        if fn == 10:
            return (H0 + _tdiv((H1 - H0) * x, 8)) / F if x <= 7 else (H1 + _tdiv((H2 - H1) * (x - 8), 8)) / F
        if fn == 11:
            u0, u1, u2 = (b * 8 * F for b in hb)        # ldrb: unsigned in this one function
            return (u0 + _tdiv((u1 - u0) * z, 8)) / F if z <= 7 else (u1 + _tdiv((u2 - u1) * (z - 8), 8)) / F
    else:
        if fn == 10:
            return s[diag3[x * 16 + z]]
        if fn == 11:
            return s[diag3[x * 16 + 15 - z]]
        if fn == 14:
            return (h0 if x <= 7 else h1) if z <= 7 else h2
        if fn == 15:
            return h0 if z <= 7 else (h1 if x <= 7 else h2)
    raise ValueError(fn)


# --- exits (warps) and arrival points (14 Oct, second pass) ---------------------------------------------------------
# Exit list = map-code stub 2. VERIFIED against the engine's reader: GS1 MapGroupTable_SelectEntry 0x0808A5F8 (alchemy
# SRC\FIELD\COMMON\MAP\SELECT_GROUP_ENTRY.C), GS2 0x080C9694 (Ghidra; called by the field loop 0x080C9944 with the exit id
# that 0x080CB91C returns). The list is a stream of u32 words:
#   header: upper 20 bits clear, bits 0-11 = the room (scene) the group belongs to; a header of 0x1FF ends the list.
#   exit:   bits 0-11 to_room, 12-19 to_door (entrance id in the target room), 20-27 exit id (the event id the field
#           loop returns; 0xFF = any), bit 28: a flag word follows. A word whose exit id is 0 (the next header) or
#           whose room is 0x1FF ends the group.
# The engine finds the group whose header is the current room, then takes the first exit whose id matches and whose
# flag word is 0, 0xFFFFFFFF (GS2 only) or a flag that is CLEAR. No match: the first exit's room, entrance 0.
# No group: the room doesn't change. Before this pass the exporter read every word as an exit, so group headers,
# flag words and other rooms' groups (GS2 rooms share code) were listed as warps.
def parse_exit_list(code, off, end=None):
    end = len(code) if end is None else end
    groups, cur, o = [], None, off
    while o + 4 <= end:
        w = u32(code, o)
        o += 4
        if cur is None:
            if w & 0xFFFFF000:
                continue
            if w & 0xFFF == 0x1FF:
                break
            cur = {"scene": w & 0xFFF, "offset": f"0x{CODE_BASE + o - 4:08X}", "exits": []}
            groups.append(cur)
            continue
        flag = None
        if w & 0x10000000 and o + 4 <= end:
            flag = u32(code, o)
            o += 4
        sid, door, kind = w & 0xFFF, (w >> 12) & 0xFF, (w >> 20) & 0xFF
        if sid == 0x1FF or kind == 0:
            cur = None
            if not w & 0xFFFFF000:
                if sid == 0x1FF:
                    break
                cur = {"scene": sid, "offset": f"0x{CODE_BASE + o - 4:08X}", "exits": []}
                groups.append(cur)
            continue
        cond = "always" if flag in (None, 0, 0xFFFFFFFF) else f"while flag 0x{flag:X} is clear"
        cur["exits"].append({"event": kind, "to_room": sid, "to_door": door, "flags": w >> 28,
                             "flag": flag, "condition": cond, "raw": f"0x{w:08X}"})
    return groups


def parse_door_block(blk):
    """GS2 area part +0x3C, decompressed to 0x0202E000 by the area loader (GS2 0x0802A6B8). VERIFIED reader GS2
    0x080CC7C4: u16 @0 = offset of the door list, u16 @4 = offset of the camera regions.
    Door: 6 bytes {u8 id (0xFF ends), s16 x px, s16 z px, u8 flags}; flags bits 0-3 = facing in 1/16 turns
    (angle = n << 12: 4 south, 12 north, 0 east, 8 west), bit 4 = height y 8 px, bit 5 = keep the camera.
    Camera region: 4 x s8 {left, top, right, bottom} in 16-px cells, 0xFF ends; the first region that holds
    (x, z - ground height) becomes the camera box (left/top pulled back so the box is at least 240 x 160)."""
    doors, cams = [], []
    if not blk or len(blk) < 6:
        return doors, cams
    o = u16(blk, 0)
    while o + 6 <= len(blk) and blk[o] != 0xFF:
        x, z = struct.unpack_from("<hh", blk, o + 1)
        f = blk[o + 5]
        doors.append({"id": blk[o], "x": x, "z": z, "angle": (f & 0xF) << 12, "y": 8 if f & 0x10 else None,
                      "keep_camera": bool(f & 0x20), "flags": f})
        o += 6
    o = u16(blk, 4)
    while o + 4 <= len(blk) and blk[o] != 0xFF:
        c4 = list(struct.unpack_from("<4b", blk, o))
        cams.append({"cells": c4, "px": [v * 16 for v in c4]})
        o += 4
    return doors, cams


def resolve_arrival(door, entrances, doors=None):
    """Where the party appears when it enters a room through entrance `door`.
    GS2 0x080CC9C8 (VERIFIED): 1) the room's entrance table (stub 1): the first row with this id whose flag is FFFF or
    SET (0x080CC67C); 2) on the field (state +0x18A == 2) the area's door table (parse_door_block, 0x080CC7C4);
    3) otherwise the first entrance row. GS1 has no door table (area headers end at +0x38): 1) then 3).
    The export assumes a fresh game (all flags clear), so flagged entrance rows are reported but not preferred."""
    rows = [e for e in entrances if e["id"] == door]
    if rows:
        e = next((x for x in rows if x.get("flag") == 0xFFFF), rows[0])
        return {"source": "entrance", "x": e["x"], "y": e["y"], "z": e["z"], "angle": e["angle"],
                "camera_px": e.get("camera_px"), "entrance_flag": e.get("flag")}
    for d_ in doors or []:
        if d_["id"] == door:
            return {"source": "door", "x": d_["x"], "y": d_["y"], "z": d_["z"], "angle": d_["angle"],
                    "keep_camera": d_["keep_camera"]}
    if entrances:
        e = entrances[0]
        return {"source": "default", "x": e["x"], "y": e["y"], "z": e["z"], "angle": e["angle"],
                "camera_px": e.get("camera_px"), "note": f"entrance {door} not found; the game uses the first row"}
    return None


def warp_props(w_):
    """Tiled properties of a warp trigger (exit row + its resolved arrival)."""
    a_ = w_.get("arrival") or {}
    return {"to_room": w_["to_room"], "to_door": w_["to_door"], "to_x": a_.get("x"), "to_y": a_.get("y"),
            "to_z": a_.get("z"), "to_angle": a_.get("angle"), "arrival": a_.get("source"),
            "exit_flag": None if w_.get("flag") in (None, 0, 0xFFFFFFFF) else w_["flag"]}


WARP_PROP_KEYS = ("to_room", "to_door", "to_x", "to_y", "to_z", "to_angle", "arrival", "exit_flag")


def patch_tiled_warps(tmj_path, warps):
    """Rewrite the warp properties of an existing room .tmj (tile-event objects) without re-rendering."""
    if not tmj_path.exists():
        return False
    m = json.loads(tmj_path.read_text(encoding="utf-8"))
    by = {}
    for w_ in warps:
        by.setdefault(w_["event"], w_)
    for L in m.get("layers", []):
        if L.get("type") != "objectgroup" or L.get("name") != "tile events":
            continue
        for o in L.get("objects", []):
            props = [p for p in o.get("properties", []) if p["name"] not in WARP_PROP_KEYS]
            ev_id = next((p["value"] for p in props if p["name"] == "event_id"), None)
            if ev_id in by:
                o["type"] = "warp"
                props += [{"name": k, "type": "string" if isinstance(v, str) else "int", "value": v}
                          for k, v in warp_props(by[ev_id]).items() if v is not None]
            elif o.get("type") == "warp":
                o["type"] = "trigger"
            o["properties"] = props
    tmj_path.write_text(json.dumps(m, separators=(",", ":")), encoding="utf-8")
    return True


def resolve_warps(ws):
    """Second pass over maps/rooms/*/events.json: give every exit its arrival point in the target room, patch the
    room .tmj warp objects, and write maps/warps.json (the whole warp graph). Returns coverage counts."""
    ev = {}
    for p in sorted((ws / "rooms").glob("room_*/events.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        ev[d["room"]] = (p, d)
    cov = {"exits": 0, "checked": 0, "by_source": {}, "no_target_room": 0, "unresolved_examples": []}
    graph = []
    for r, (p, d) in sorted(ev.items()):
        for w_ in d.get("warps", []):
            cov["exits"] += 1
            t = ev.get(w_["to_room"])
            if t is None:
                w_["arrival"] = None
                cov["no_target_room"] += 1
            else:
                cov["checked"] += 1
                w_["arrival"] = resolve_arrival(w_["to_door"], t[1].get("entrances", []), t[1].get("doors"))
                src = (w_["arrival"] or {}).get("source", "none")
                cov["by_source"][src] = cov["by_source"].get(src, 0) + 1
                if src in ("default", "none") and len(cov["unresolved_examples"]) < 40:
                    cov["unresolved_examples"].append({"room": r, "exit": w_["event"], "to_room": w_["to_room"],
                                                       "to_door": w_["to_door"]})
            graph.append({"room": r, "exit": w_["event"], "to_room": w_["to_room"], "to_door": w_["to_door"],
                          "condition": w_.get("condition", "always"), "arrival": w_["arrival"]})
        p.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
        patch_tiled_warps(p.parent / f"room_{r:03d}.tmj", d.get("warps", []))
    ok = cov["by_source"].get("entrance", 0) + cov["by_source"].get("door", 0)
    cov["resolved_entrance_or_door"] = ok
    cov["resolved_pct"] = round(100 * ok / cov["checked"], 1) if cov["checked"] else None
    (ws / "warps.json").write_text(json.dumps({"rule": resolve_arrival.__doc__.strip(), "coverage": cov,
                                               "exits": graph}, indent=1, ensure_ascii=False), encoding="utf-8")
    return cov


def refresh_warps(gm, rooms=None):
    """Re-read only the warp-related tables of already-exported rooms (fast; no rendering), then resolve_warps.
    Updates events.json keys entrances/warps/exit_groups/exit_group/doors/camera_regions and index.json coverage."""
    ws = gm.rom.workspace / "maps"
    rooms = list(range(gm.n_rooms)) if rooms is None else rooms
    keys = ("entrances", "warps", "exit_groups", "exit_group", "doors", "camera_regions")
    idx_p = ws / "index.json"
    index = json.loads(idx_p.read_text(encoding="utf-8")) if idx_p.exists() else {}
    for r in rooms:
        p = ws / "rooms" / f"room_{r:03d}" / "events.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        try:
            ev, _ = gm.parse_tables(r)
        except Exception as e:  # noqa: BLE001
            print(f"room {r}: {type(e).__name__}: {e}", flush=True)
            continue
        for k in keys:
            if k in ev:
                d[k] = ev[k]
        p.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
        ent = index.get("rooms", {}).get(str(r))
        if ent and "counts" in ent:
            ent["counts"]["warps"] = len(d.get("warps", []))
            ent["counts"]["entrances"] = len(d.get("entrances", []))
    cov = resolve_warps(ws)
    if index:
        c = index.setdefault("coverage", {})
        c.update(warps_checked=cov["checked"], warps_door_found=cov["by_source"].get("entrance", 0), warps=cov)
        idx_p.write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    return cov


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
            # Meaning (VERIFIED: alchemy Map_LoadLayeredScene + Map_UpdateLayerScroll, MAP.C; the field loader reads
            # the same record): BG scroll = view * ratio/16 + phase + offset, view = camera top-left clamped to the
            # bounds; phase += speed/16 px per frame (signed bytes 4-5) and wraps at (mask+1)*8 px (bytes 6-7).
            sp = layers[-1]["auto_scroll"]
            layers[-1].update({"scroll_scale": [rec[2] / 16, rec[3] / 16],
                               "autoscroll_px_per_frame": [sp[0] / 16, sp[1] / 16],
                               "autoscroll_wrap_px": [(rec[6] + 1) * 8 if sp[0] else None, (rec[7] + 1) * 8 if sp[1] else None]})
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
        self.tile_anim(A)
        return A

    def visible_mask(self, A):
        """GS2: bool [ceil(H/16), ceil(W/16)] of image cells inside the union of the area's camera regions (part
        +0x3C). The engine clamps the view to the region box (Map_UpdateLayerScroll clamps the BG scroll to the
        camera limits), so cells outside every region are never on screen. None when the area has no regions."""
        if self.gs != 2:
            return None
        try:
            _, regions = self.area_doors(A["area"])
        except Exception:  # noqa: BLE001
            return None
        if not regions:
            return None
        A["camera_regions_px"] = [c["px"] for c in regions]
        H, W = (A["height"] + 15) // 16, (A["width"] + 15) // 16
        zz, xx = np.mgrid[0:H, 0:W] * 16
        vis = np.zeros((H, W), bool)
        for (rx0, ry0, rx1, ry1) in A["camera_regions_px"]:
            vis |= (xx + 16 > rx0) & (xx < rx1) & (zz + 16 > ry0) & (zz < ry1)
        return vis

    # --- tile animation ----------------------------------------------------------------------------------------
    def tile_anim(self, A):
        """Decode the area's tile-animation script (GS1 part +0x30, GS2 +0x34; see anim_channels). Sets A['anim']
        (JSON summary), A['anim_runs'] (running channels) and replaces A['vram'] by the state the player sees on
        the first frame (frame 0 of every running channel applied); A['vram_raw'] keeps the stored chars."""
        key = "+0x30" if self.gs == 1 else "+0x34"
        part = A["parts"].get(key)
        A["vram_raw"], A["anim_runs"], A["anim_dst"], A["anim_t0"], A["anim"] = A["vram"], {}, {}, 0, None
        A["anim_tiles"], A["anim_reg"] = {}, {}
        if not part or not part.get("data"):
            return
        w, chans = anim_channels(part["data"])
        runs, summary = {}, []
        for ch in chans:
            r = anim_run(w, ch["start"])
            ev, p0, P, how = r
            dst = sorted({d + i for (_, s, n, d) in ev for i in range(n)})
            cmds, i = [], ch["start"]
            while i < len(w) and len(cmds) < 256:
                op = w[i]
                if op == 0xFFFF or op & 0xFF00 == 0xFE00:
                    cmds.append("restart" if op == 0xFFFF else ("stop" if op & 0xFF == 0xFF else f"jump {op & 0xFF}"))
                    break
                cmds.append(list(w[i:i + 4]))
                i += 4
            summary.append({"channel": ch["channel"], "paused": ch["paused"], "start_word": ch["start"], "end": how,
                            "cycle_start_frame": p0, "period_frames": P, "dst_chars": len(dst),
                            "dst_char_range": [dst[0], dst[-1]] if dst else None, "commands": cmds})
            if not ch["paused"] and how in ("loop", "stop", "cap"):
                runs[ch["channel"]] = r
                A["anim_dst"][ch["channel"]] = set(dst)
        t0 = max([r[1] for r in runs.values() if r[3] in ("loop", "stop")] + [0])
        state = {}
        for f, copies in anim_schedule(runs, runs.keys(), t0 + 1).items():
            anim_apply(state, copies)
        raw = A["vram_raw"]
        vram = bytearray(raw)
        for d, s in state.items():
            if 0 <= d < 2048 and 0 <= s < 2048:
                vram[d * 32:d * 32 + 32] = raw[s * 32:s * 32 + 32]
        A["vram"], A["anim_runs"], A["anim_t0"] = bytes(vram), runs, t0
        A["anim"] = {"part": key, "words": len(w), "channels": summary, "steady_from_frame": t0,
                     "chars_changed_at_start": len(state), "fps": GBA_FPS}

    def anim_layer(self, A, l, ids):
        """Animation id per cell of layer l (0 = static); fills A['anim_tiles'][aid] = {frames: [(rgba16, n_frames)],
        channels, truncated}. A cell animates when one of its metatile's four chars is an animation destination."""
        out = np.zeros(ids.shape, np.int64)
        runs = A["anim_runs"]
        if not runs or not len(A["metatiles"]):
            return out
        cb = A["layers"][l]["char_block"]
        mts = A["metatiles"].reshape(-1, 4).astype(np.int64)
        allc = set().union(*A["anim_dst"].values())
        lut = np.zeros(len(mts) + 1, np.int64)
        for mt in np.unique(ids[ids >= 0]):
            k = (int(mt), cb)
            if k not in A["anim_reg"]:
                ent = [int(e) for e in mts[mt]]
                tn = [(e & 0x3FF) + cb * 512 for e in ent]
                A["anim_reg"][k] = self._anim_tile(A, ent, tn) if any(t in allc for t in tn) else 0
            lut[mt] = A["anim_reg"][k]
        return np.where(ids >= 0, lut[np.clip(ids, 0, len(mts))], 0)

    def _anim_tile(self, A, ent, tn):
        runs, t0 = A["anim_runs"], A["anim_t0"]
        S = {c for c, d in A["anim_dst"].items() if d & set(tn)}
        while True:                                     # channels feeding the sources of these channels
            srcs = {s + i for c in S for (_, s, n, d) in runs[c][0] for i in range(n)}
            more = {c for c, d in A["anim_dst"].items() if d & srcs} - S
            if not more:
                break
            S |= more
        span = 1
        for c in S:
            if runs[c][3] == "loop" and runs[c][2]:
                span = span * runs[c][2] // np.gcd(span, runs[c][2])
        truncated = span > ANIM_MAX_SPAN
        span = min(span, ANIM_MAX_SPAN)
        sched = anim_schedule(runs, S, t0 + span)
        state, fr = {}, sorted(sched)
        i = 0
        while i < len(fr) and fr[i] <= t0:
            anim_apply(state, sched[fr[i]])
            i += 1
        seq = [(tuple(state.get(c, c) for c in tn), t0)]
        for f in fr[i:]:
            anim_apply(state, sched[f])
            t = tuple(state.get(c, c) for c in tn)
            if t != seq[-1][0]:
                seq.append((t, f))
        frames = [(t, (seq[j + 1][1] if j + 1 < len(seq) else t0 + span) - f) for j, (t, f) in enumerate(seq)]
        if len(frames) > 1 and frames[-1][0] == frames[0][0]:     # the cycle wraps into the first keyframe
            frames = [(frames[0][0], frames[0][1] + frames[-1][1])] + frames[1:-1]
        if len(frames) < 2:
            return 0
        frames = min_period(frames)
        if len(frames) > ANIM_MAX_KEYS:
            frames, truncated = frames[:ANIM_MAX_KEYS], True
        if "tiles_raw" not in A:
            A["tiles_raw"] = tiles_4bpp(A["vram_raw"])
            A["pal_rgb"] = bgr555_to_rgb(A["palette_words"] + [0] * (256 - len(A["palette_words"])))
        aid = len(A["anim_tiles"]) + 1
        A["anim_tiles"][aid] = {"frames": [(self._metatile_rgba(A, ent, t), n) for t, n in frames],
                                "channels": sorted(S), "truncated": truncated}
        return aid

    @staticmethod
    def _metatile_rgba(A, ent, chars):
        img = np.zeros((16, 16, 4), np.uint8)
        tiles, pal = A["tiles_raw"], A["pal_rgb"]
        for q, (e, c) in enumerate(zip(ent, chars)):
            if not 0 <= c < len(tiles):
                continue
            px = tiles[c]
            if e & 0x400:
                px = px[:, ::-1]
            if e & 0x800:
                px = px[::-1, :]
            y, x = (q // 2) * 8, (q % 2) * 8
            img[y:y + 8, x:x + 8, :3] = pal[(e >> 12) * 16 + px]
            img[y:y + 8, x:x + 8, 3] = np.where(px > 0, 255, 0)
        return img

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
        if blend and blend["mode"] in (2, 3) and blend["evy"]:          # brighten / darken the topmost first targets
            tgt = np.array([blend["first"][5]] + [blend["first"][3 - t] for t in range(3)], bool)[top_is + 1]
            o = out.astype(np.int32)
            o = o + ((255 - o) * blend["evy"] >> 4) if blend["mode"] == 2 else o - (o * blend["evy"] >> 4)
            out[tgt] = o[tgt].astype(np.uint8)
        return out

    # --- map code ----------------------------------------------------------------------------------------------
    @staticmethod
    def stub_imports(code):
        """Copy of the room code whose import veneers into the main image (`ldr r4,[pc]; bx r4; .word 0x08xxxxxx`)
        are replaced by `movs r0,#0; bx lr`. Getters run on it see a fresh game (every flag test returns 0) and can't
        fault on engine state the emulator lacks (Scene_AssignViewFlags reads the camera through an IWRAM pointer;
        without this, getters that call it, e.g. GS1 Bilibin room 31, returned no actor table)."""
        c = bytearray(code)
        for o in range(0, len(c) - 7, 2):
            if u32(c, o) == STUB and ROM_BASE <= u32(c, o + 4) < ROM_BASE + 0x02000000:
                c[o:o + 4] = b"\x00\x20\x70\x47"
        return bytes(c)

    @staticmethod
    def relocate_bl(code):
        """Apply the loader's Thumb-call relocation. Map code is stored with every `bl` pair (0xF000/0xF800
        halfwords) holding its target as an offset from the block start (target = base + stored + 2); after decoding,
        Resource_LoadCode runs the ARM routine GS1 0x08002D5C over the block to make them pc-relative. VERIFIED from
        alchemy SRC/SYSTEM/RESOURCE/PATCH_THUMB_BRANCH.S + RESOURCE.C, and by data: GS1 room 31's Scene_GetPlacements
        call lands on its Scene_AssignViewFlags import veneer only after this step. Before 14 Oct, map_code.bin and
        the emulated getters used unrelocated code."""
        c = bytearray(code)
        p = 2
        while p < len(c):
            ip = u16(c, p)
            p += 2
            if ip >> 11 != 31 or u16(c, p - 4) >> 11 != 30:
                continue
            v = ((((u16(c, p - 4) & 0x7FF) << 11) | (ip & 0x7FF)) << 1) - (p - 2)
            v &= 0xFFFFFFFF
            struct.pack_into("<HH", c, p - 4, 0xF000 | ((v >> 12) & 0x7FF), 0xF800 | ((v >> 1) & 0x7FF))
        return bytes(c)

    def map_code(self, r):
        R = self.room(r)
        code = self.relocate_bl(self.decode_file(R["code_file"]))
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
                g.write(CODE_BASE, self.stub_imports(code))
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

    def area_doors(self, a):
        """GS2: the area's door table and camera regions (part +0x3C, see parse_door_block). ([], []) if absent."""
        key = ("doors", a)
        if key not in self._cache:
            res = ([], [])
            try:
                c = self.file_addr(self.area_files(a)[0])
                if u32(self.d, c + 0x24) >= 0x40 and u32(self.d, c + 0x3C):
                    off = u32(self.d, c + 0x3C)
                    if self.d[c + off] in (0, 1):
                        res = parse_door_block(self.dec.decode((c + off) | ROM_BASE))
            except Exception:  # noqa: BLE001 - a missing table just leaves the fallback to the entrance table
                pass
            self._cache[key] = res
        return self._cache[key]

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
                cam = struct.unpack_from("<4h", code, o + 14)   # camera left/top/right/bottom px; -1 = keep (GS2 0x080CC67C)
                ent.append({"id": u16(code, o), "flag": u16(code, o + 2), "x": u16(code, o + 4), "y": u16(code, o + 6),
                            "z": u16(code, o + 8), "angle": u16(code, o + 10), "rest": code[o + 12:o + 24].hex(),
                            "camera_px": [None if v == -1 else v for v in cam]})
                o += 24
        if 2 in tables:          # exits: scene groups of u32 words, see parse_exit_list (VERIFIED reader)
            o = tables[2] - CODE_BASE
            groups = parse_exit_list(code, o, end(o))
            own = next((g_ for g_ in groups if g_["scene"] == r), None)
            war = list(own["exits"]) if own else []
            out["exit_group"] = own["scene"] if own else None
            out["exit_groups"] = [{"scene": g_["scene"], "offset": g_["offset"], "exits": len(g_["exits"])}
                                  for g_ in groups]
        if 3 in tables:                                   # actors: 24-byte ScenePlacement rows
            o = tables[3] - CODE_BASE
            act = placement_rows(code[:end(o)], o)
            for a_ in act:
                a_["source"] = "placements"
        # actor tables that room scripts spawn later (static scan; see scan_actor_calls)
        far = FAR_ACTOR_CALLS.get(self.rom.code, {})
        calls = scan_actor_calls(code, far)
        prepared = any(k_ == "prepare" for k_, _, _ in calls)
        last_main = max([a_["slot"] for a_ in act if not a_["party_member"] and a_["slot"] is not None],
                        default=FIRST_PLACED_SLOT - 1)
        spawned, seen = [], set()
        for kind, tab, site in calls:
            if kind == "prepare" or tab is None or not CODE_BASE <= tab < CODE_BASE + len(code):
                continue
            if tab == tables.get(3) or (kind, tab) in seen:
                if (kind, tab) not in seen and tab == tables.get(3):
                    seen.add((kind, tab))
                continue
            seen.add((kind, tab))
            start = FIRST_PLACED_SLOT if kind == "reset" else last_main + 1
            rows = placement_rows(code, tab - CODE_BASE, start_slot=start)
            for a_ in rows:
                a_.update(source=f"script:{kind}", table=f"0x{tab:08X}", call_site=f"0x{site:08X}",
                          slot_basis="from slot 8 (actor table rebuilt)" if kind == "reset" else
                          "after the placement table's last row (assumes that row is present)")
            spawned.extend(rows)
        out["actor_spawning"] = {
            "placements_prepared_by_view": prepared,
            "script_calls": [{"kind": k_, "table": f"0x{t_:08X}" if t_ else None, "call_site": f"0x{s_:08X}"}
                             for k_, t_, s_ in calls]}
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
        # resolve actor-targeted events (talk, Psynergy on actor) to an actor slot; the placement table wins over
        # script-spawned rows that share a slot number
        by_slot = {}
        for a_ in act + spawned:
            if a_["slot"] is not None:
                by_slot.setdefault(a_["slot"], a_)
        for e in evt:
            t_ = e["type"]
            if t_ & 0xF == 0 or (t_ & 0xF == 5 and t_ & 0x10 and not t_ & 0x80):
                s_ = e["id"] & 0xFF if t_ & 0xF == 5 else e["id"]
                e["actor_slot"] = s_
                a_ = by_slot.get(s_)
                if a_ is not None:
                    e["actor"] = {"source": a_["source"], "index": a_["index"], "table": a_.get("table")}
                    key = "talk" if t_ & 0xF == 0 else "psynergy"
                    lst = a_.setdefault(f"{key}_events", [])
                    lst.append({"type": t_, "ability": e["b1"] if key == "psynergy" else None, "flag": e["flag"],
                                "script": e.get("script"), "text_id": e.get("text_id")})
                elif s_ < FIRST_PLACED_SLOT:
                    e["actor"] = {"source": "party", "index": s_}
        for a_ in act + spawned:
            if a_["condition"].get("show") == "always_view_streamed" and not prepared:
                a_["condition"]["show"] = "while_clear"
        if self.gs == 2:                                  # door arrival points of the room's area (part +0x3C)
            out["doors"], out["camera_regions"] = self.area_doors(self.room(r)["area"])
        out.update(entrances=ent, warps=war, actors=act, actors_spawned=spawned, events=evt)
        return out, code


# --- export --------------------------------------------------------------------------------------------------------
def shape_edges(gm, A):
    """Ground height (px) at the four edge midpoints of every height shape: {index: {L, R, T, B}}."""
    t = SHAPE_TABLES[gm.gs]
    rm, dg = gm.d[t[0]:t[0] + 256], gm.d[t[1]:t[1] + 256]
    pts = {"L": (0, 8), "R": (15, 8), "T": (8, 0), "B": (8, 15), "C": (8, 8)}
    return {i: {k: shape_height_px(gm.gs, s[0] & 15, s[1:], x, z, rm, dg) for k, (x, z) in pts.items()}
            for i, s in enumerate(A["shapes"])}


def reachable_cells(gm, A, seeds, regions=None):
    """Flood fill of the cells the player can reach, per collision layer (bool [h, w] in layer-window cells).
    Rules (gs_movement.md, VERIFIED there): event byte 0xFF is solid; a step between neighbours is allowed when the
    ground height across the shared edge changes by -12..+8 px (the shape functions give the height). Seeds:
    (x, y, z, kind, layer) px from entrances, doors, actors and exit tiles (layer given); other seeds go on layer 0
    (objects start there; byte +0x22 changes only through layer-switch tiles), else on the nearest-height layer. regions (GS2 camera regions, px) additionally bound the fill: a cell counts only when
    (x, z - ground) is inside one of them, the same test the game uses to pick the camera box."""
    E = shape_edges(gm, A)
    flat = {"L": 0, "R": 0, "T": 0, "B": 0, "C": 0}
    out, grids = [], []
    for l in range(3):
        x0, y0, w, h, px, py = gm.layer_cells(A, l)
        ev = A["event"][y0:min(y0 + h, CELLS), x0:min(x0 + w, CELLS)]
        sh = A["shape"][y0:min(y0 + h, CELLS), x0:min(x0 + w, CELLS)]
        hh = {k: np.vectorize(lambda i, k=k: E.get(int(i), flat)[k], otypes=[float])(sh) for k in flat} if sh.size else {}
        ok = ev != 255
        if regions and sh.size:
            zz, xx = np.mgrid[0:ev.shape[0], 0:ev.shape[1]]
            cx, cz = xx * 16 + 8, zz * 16 + 8 - hh["C"]
            ok &= np.any([(cx >= r[0]) & (cx < r[2]) & (cz >= r[1]) & (cz < r[3]) for r in regions], axis=0)
        grids.append((ev, hh, ok))
        out.append(np.zeros(ev.shape, bool))
    stack = []
    for (x, y, z, kind, layer) in seeds:
        cx, cz = int(x) >> 4, int(z) >> 4
        best = None
        for l, (ev, hh, ok) in enumerate(grids):
            if layer is not None and l != layer:
                continue
            if 0 <= cz < ev.shape[0] and 0 <= cx < ev.shape[1] and ok[cz, cx]:
                d = 0 if l == 0 else 1000 + abs(hh["C"][cz, cx] - (y or 0))    # objects start on layer 0
                if best is None or d < best[0]:
                    best = (d, l)
        if best is not None:
            stack.append((best[1], cz, cx))
    nb = ((0, 1, "R", "L"), (0, -1, "L", "R"), (1, 0, "B", "T"), (-1, 0, "T", "B"))
    while stack:
        l, z, x = stack.pop()
        m = out[l]
        if m[z, x]:
            continue
        m[z, x] = True
        ev, hh, ok = grids[l]
        for dz, dx, ea, eb in nb:
            z2, x2 = z + dz, x + dx
            if 0 <= z2 < m.shape[0] and 0 <= x2 < m.shape[1] and not m[z2, x2] and ok[z2, x2]:
                if -12 <= hh[eb][z2, x2] - hh[ea][z, x] <= 8:
                    stack.append((l, z2, x2))
    return out


def unique_tiles(imgs_keys, A, anim_ids=None):
    """Collect unique 16x16 RGBA tiles over all layers -> (tileset image, per-layer gid arrays, tilecount, columns,
    Tiled 'tiles' list with animations, number of unique tiles). A tile's identity is its pixels plus its animation
    id, so placeholder tiles that look alike but animate differently stay apart. Layout: static tiles first; then
    every animated tile starts its own row with its frames in the next columns (the contiguous layout Godot's
    TileSetAtlasSource animation needs), and the Tiled animation lists them with durations in ms."""
    anim_ids = anim_ids or {}
    seen, order, gids = {}, [], {}
    for l, (img, ids, win) in imgs_keys.items():
        x0, y0, w, h, px, py = win
        full = np.zeros((h * 16, w * 16, 4), np.uint8)
        full[py:py + img.shape[0], px:px + img.shape[1]] = img
        aids = anim_ids.get(l)
        g = np.zeros((h, w), np.int64)
        for cy in range(h):
            for cx in range(w):
                t = full[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16]
                aid = int(aids[cy, cx]) if aids is not None else 0
                if not aid and not t[..., 3].any():
                    continue
                key = (t.tobytes(), aid)
                if key not in seen:
                    seen[key] = len(order) + 1
                    order.append((t, aid))
                g[cy, cx] = seen[key]
        gids[l] = g
    store = A.get("anim_tiles") or {}
    statics = [i for i, (t, aid) in enumerate(order) if not aid]
    anims = [i for i, (t, aid) in enumerate(order) if aid]
    cols = max([16] + [len(store[order[i][1]]["frames"]) for i in anims])
    pos = {i: k for k, i in enumerate(statics)}
    p = ((len(statics) + cols - 1) // cols) * cols
    for i in anims:                                     # pack: a tile and its frames never wrap across a row
        n = len(store[order[i][1]]["frames"])
        if p % cols + n > cols:
            p += cols - p % cols
        pos[i] = p
        p += n
    rows = max(1, (p + cols - 1) // cols)
    sheet = np.zeros((rows * 16, cols * 16, 4), np.uint8)

    def put(p, t):
        sheet[(p // cols) * 16:(p // cols) * 16 + 16, (p % cols) * 16:(p % cols) * 16 + 16] = t

    tiles_json = []
    for i, (t, aid) in enumerate(order):
        put(pos[i], t)
        if aid:
            frames = store[aid]["frames"]
            for k, (fimg, n) in enumerate(frames[1:], 1):
                put(pos[i] + k, fimg)
            tiles_json.append({"id": pos[i], "animation": [{"tileid": pos[i] + k, "duration": max(1, round(n * 1000 / GBA_FPS))}
                                                            for k, (fimg, n) in enumerate(frames)],
                               "properties": [{"name": "frames_60hz", "type": "string", "value": ",".join(str(n) for _, n in frames)},
                                              {"name": "anim_channels", "type": "string", "value": ",".join(map(str, store[aid]["channels"]))}]})
    remap = np.zeros(len(order) + 1, np.int64)
    remap[1:] = [pos[i] + 1 for i in range(len(order))]
    gids = {l: np.where(g > 0, remap[g], 0) for l, g in gids.items()}
    return sheet, gids, rows * cols, cols, tiles_json, len(order)


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
    done_areas, seeds_by_area = {}, {}
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
                bp = A["parts"].get("+0x34" if gm.gs == 1 else "+0x38")
                if bp and bp.get("data"):
                    A["blend"] = parse_blend_script(bp["data"])
                info.update({k: A[k] for k in ("header", "bounds_px", "width", "height", "layers")})
                info["blend"] = A.get("blend")
                info["parts"] = {k: ({kk: vv for kk, vv in p.items() if kk != "data"} if p else None) for k, p in A["parts"].items()}
                info["palette"] = [f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}" for c in bgr555_to_rgb(A["palette_words"])]
                info["metatiles"] = len(A["metatiles"]) // 4
                info["height_shapes"] = A["shapes"]
                info["tile_animation"] = A["anim"]
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
                    vis = gm.visible_mask(A)
                    if vis is not None:     # GS2: never-visible filler outside every camera region is blanked
                        info["visible_rects_px"] = A["camera_regions_px"]
                        for l, (img, ids, win) in list(imgs.items()):
                            x0, y0, w, h, px, py = win
                            keep = np.repeat(np.repeat(vis, 16, 0), 16, 1)[:img.shape[0], :img.shape[1]]
                            img2 = img.copy()
                            img2[~keep] = 0
                            imgs[l] = (img2, ids, win)
                            full = np.zeros((h * 16, w * 16), bool)
                            full[py:py + keep.shape[0], px:px + keep.shape[1]] = keep
                            A.setdefault("vis_cells", {})[l] = full.reshape(h, 16, w, 16).any(axis=(1, 3))
                        info["hidden_px_outside_camera_regions"] = int((~vis).sum()) * 256
                    comp = gm.composite(A, {l: v[0] for l, v in imgs.items()})
                    Image.fromarray(comp, "RGB").save(ad / "composite.png", optimize=True)
                    en = {l: v for l, v in imgs.items() if A["layers"][l]["enabled"]}
                    aids = {l: gm.anim_layer(A, l, v[1]) * A.get("vis_cells", {}).get(l, 1) for l, v in en.items()}
                    sheet, gids, nt, cols, tjs, nu = unique_tiles(en, A, aids)
                    Image.fromarray(sheet, "RGBA").save(ad / "tileset.png", optimize=True)
                    A["gids"], A["windows"], A["ntiles"] = gids, {l: v[2] for l, v in imgs.items()}, nt
                    A["tile_cols"], A["tile_anims"] = cols, tjs
                    info["unique_tiles_16"] = nu
                    info["animated_tiles_16"] = len(tjs)
                    info["tileset_columns"] = cols
                    pal = bgr555_to_rgb(A["palette_words"])
                    Image.fromarray(np.repeat(np.repeat(pal.reshape(-1, 16, 3), 8, 0), 8, 1), "RGB").save(ad / "palette.png")
                # collision per layer window
                coll = {"cell_px": 16, "solid_value": 255, "layers": [], "height_shapes": [
                    {"index": i, "function": s[0] & 15, "kind": SHAPE_NAMES[gm.gs][s[0] & 15], "flags": s[0] >> 4,
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
                        info["nonsolid_bounds_px"] = info["walkable_bounds_px"]      # refined by refine_walkable()
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
        seeds_by_area.setdefault(a, []).append(ev_out)
        entry["counts"] = {k: len(ev.get(k, [])) for k in ("entrances", "warps", "actors", "events")}
        if A is not None and "gids" in A:
            write_tiled(gm, A, r, ev, rd, a)
            entry["tiled"] = f"rooms/room_{r:03d}/room_{r:03d}.tmj"
        entry["area_status"] = A_all[str(a)]["status"]
        R_all[str(r)] = entry
        print(f"room {r:3d} area {a:3d} {A_all[str(a)]['status'][:60]:60s} {entry['name']}", flush=True)
    if render:
        refine_walkable(gm, ws, done_areas, seeds_by_area)
    write_height_shapes(gm, ws)
    index["rooms"] = dict(sorted(R_all.items(), key=lambda kv: int(kv[0])))
    index["areas"] = dict(sorted(A_all.items(), key=lambda kv: int(kv[0])))
    ok = sum(1 for v in index["areas"].values() if v["status"] == "ok")
    # second pass: every exit gets its arrival point in the target room (entrance table, GS2 door table, default);
    # warps_door_found keeps its old meaning (door id found in the target's entrance table)
    wc = resolve_warps(ws)
    wt, wok = wc["checked"], wc["by_source"].get("entrance", 0)
    index["coverage"] = {"areas_ok": ok, "areas_seen": len(index["areas"]),
                         "areas_empty_stub": sum(1 for v in index["areas"].values() if v["status"].startswith("empty")),
                         "warps_checked": wt, "warps_door_found": wok, "warps": wc,
                         "rooms_events_ok": sum(1 for v in index["rooms"].values() if v.get("events_status") == "ok"),
                         "rooms_seen": len(index["rooms"])}
    (ws / "index.json").write_text(json.dumps(index, indent=1, ensure_ascii=False), encoding="utf-8")
    write_gallery(gm, index, ws)
    return index


def write_height_shapes(gm, ws):
    """maps/height_shapes.json: the 16 terrain-height functions of this game (names, the two 256-byte lookup tables)
    and every function sampled on a 16x16 cell for unit heights (h0, h1, h2) = (0, 1, 2) x 8 px, so a converter can
    check its port against shape_height_px()."""
    t = SHAPE_TABLES[gm.gs]
    rm, dg = gm.d[t[0]:t[0] + 256], gm.d[t[1]:t[1] + 256]
    hb = (0, 1, 2)
    doc = {"game": gm.rom.code, "function_table": f"0x{t[2] | ROM_BASE:08X}",
           "round_mask_table": f"0x{t[0] | ROM_BASE:08X}", "diag3_table": f"0x{t[1] | ROM_BASE:08X}",
           "entry": "4 bytes: byte 0 low nibble = function, bytes 1-3 = h0..h2 (signed, x8 px; GS1 fn 11 unsigned)",
           "call": "height = fn(h, x & 15, z & 15); walkable step: -12 <= ground - floor <= +8 px",
           "names": SHAPE_NAMES[gm.gs], "round_mask": list(rm), "diag3": list(dg),
           "samples_h_0_1_2": {str(f): [[shape_height_px(gm.gs, f, hb, x, z, rm, dg) for x in range(16)] for z in range(16)]
                               for f in range(16)}}
    (ws / "height_shapes.json").write_text(json.dumps(doc, separators=(",", ":")), encoding="utf-8")


def area_seeds(evs):
    """Seeds for reachable_cells from the events of every room on an area -> ([(x, y, z, kind, layer)], regions)."""
    seeds, regions = [], None
    for ev in evs:
        for e in ev.get("entrances", []):
            seeds.append((e["x"], e["y"], e["z"], "entrance", None))
        for d_ in ev.get("doors", []) or []:
            seeds.append((d_["x"], d_["y"], d_["z"], "door", None))
        for ac in (ev.get("actors") or []) + (ev.get("actors_spawned") or []):
            if ac.get("x") or ac.get("z"):
                seeds.append((ac["x"], ac["y"], ac["z"], "actor", None))
        if ev.get("camera_regions"):
            regions = [c["px"] for c in ev["camera_regions"]]
        exits = {w_["event"] for w_ in ev.get("warps", [])}
        for l, ids in (ev.get("tile_event_ids_by_layer") or {}).items():
            for v in set(ids) & exits:
                seeds.append(("tile", v, None, "tile", int(l)))
    return seeds, regions


def refine_walkable(gm, ws, done_areas, seeds_by_area):
    """Second pass: walkable_bounds_px = bounding box of the cells reachable from the rooms' entrances, doors, actors
    and exit tiles (reachable_cells), instead of every non-solid cell; filler such as GS2 Champa's 'A' tiles is left
    out. Rooms of the area not exported in this run contribute their events.json from disk when present."""
    by_area = {}
    for r in range(gm.n_rooms):
        try:
            by_area.setdefault(gm.room(r)["area"], []).append(r)
        except Exception:  # noqa: BLE001
            pass
    for a, A in done_areas.items():
        if A is None or "gids" not in A:
            continue
        evs = list(seeds_by_area.get(a, []))
        have = {e["room"] for e in evs}
        for r in by_area.get(a, []):
            f = ws / "rooms" / f"room_{r:03d}" / "events.json"
            if r not in have and f.exists():
                evs.append(json.loads(f.read_text(encoding="utf-8")))
        seeds, regions = area_seeds(evs)
        tiles = []
        for (x, y, z, kind, layer) in seeds:
            if kind == "tile":                          # exit-tile seeds: every cell carrying that event id
                x0, y0, w, h, px, py = gm.layer_cells(A, layer)
                sub = A["event"][y0:min(y0 + h, CELLS), x0:min(x0 + w, CELLS)]
                tiles += [(int(cx) * 16 + 8, 0, int(cz) * 16 + 8, "tile", layer) for cz, cx in zip(*np.nonzero(sub == y))]
        seeds = [sd for sd in seeds if sd[3] != "tile"] + tiles
        reach = reachable_cells(gm, A, seeds, regions)
        ad = ws / "areas" / f"area_{a:03d}"
        info = json.loads((ad / "area.json").read_text(encoding="utf-8"))
        ys, xs = np.nonzero(np.any([np.pad(m, ((0, 128 - m.shape[0]), (0, 128 - m.shape[1]))) for m in reach], axis=0))
        info["reachable"] = {"seeds": len(seeds), "camera_regions": regions, "cells_by_layer": [int(m.sum()) for m in reach]}
        if len(xs):
            info["walkable_bounds_px"] = [int(xs.min()) * 16, int(ys.min()) * 16, int(xs.max() + 1) * 16, int(ys.max() + 1) * 16]
            info["walkable_bounds_source"] = "reachable"
            if regions:                                 # one box per camera region (the reachable part inside it)
                rects = []
                for (rx0, ry0, rx1, ry1) in regions:
                    k = (xs * 16 + 8 >= rx0) & (xs * 16 + 8 < rx1) & (ys * 16 + 8 >= ry0) & (ys * 16 + 8 < ry1)
                    if k.any():
                        rects.append([int(xs[k].min()) * 16, int(ys[k].min()) * 16, int(xs[k].max() + 1) * 16, int(ys[k].max() + 1) * 16])
                info["walkable_rects_px"] = rects
        else:
            info["walkable_bounds_source"] = "nonsolid (no seed landed)"
        (ad / "area.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
        cf = ad / "collision.json"
        if cf.exists():
            coll = json.loads(cf.read_text(encoding="utf-8"))
            for l, m in enumerate(reach):
                coll["layers"][l]["reachable"] = m.astype(np.uint8).tolist()
            cf.write_text(json.dumps(coll, separators=(",", ":")), encoding="utf-8")


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
                       **({"parallaxx": A["layers"][l]["scroll_ratio_x16"] / 16, "parallaxy": A["layers"][l]["scroll_ratio_y16"] / 16}
                          if (A["layers"][l]["scroll_ratio_x16"], A["layers"][l]["scroll_ratio_y16"]) != (16, 16) else {}),
                       "properties": [{"name": "priority", "type": "int", "value": A["layers"][l]["priority"]},
                                      *([{"name": "blend", "type": "string", "value": ("add" if A["blend"]["evb"] >= 16 else "mix")
                                           if A["blend"]["mode"] == 1 else ("brighten" if A["blend"]["mode"] == 2 else "darken")},
                                         {"name": "blend_eva16", "type": "int", "value": A["blend"]["eva"]},
                                         {"name": "blend_evb16", "type": "int", "value": A["blend"]["evb"]},
                                         {"name": "blend_evy16", "type": "int", "value": A["blend"]["evy"]}]
                                        if A.get("blend") and l in A["blend"]["first_target_layers"] else []),
                                      {"name": "autoscroll_x_px_per_frame", "type": "float", "value": A["layers"][l]["auto_scroll"][0] / 16},
                                      {"name": "autoscroll_y_px_per_frame", "type": "float", "value": A["layers"][l]["auto_scroll"][1] / 16},
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
    warps = {}
    for w_ in ev.get("warps", []):     # several rows per exit id = flag alternatives; with flags clear the first wins
        warps.setdefault(w_["event"], w_)
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
                p.update(warp_props(warps[v]))
            if v in handlers:
                p.update(handler_type=handlers[v]["type"], script=handlers[v].get("script"))
            trig.append(obj(f"event {v}", "warp" if v in warps else "trigger", x - px, y - py, ww, hh, p))
    groups.append(("tile events", trig))
    groups.append(("entrances", [obj(f"entrance {e['id']}", "entrance", e["x"], e["z"], props={"id": e["id"], "y": e["y"],
                                 "angle": e["angle"]}, point=True) for e in ev.get("entrances", [])]))
    groups.append(("doors", [obj(f"door {d_['id']}", "door", d_["x"], d_["z"], props={"id": d_["id"], "y": d_["y"],
                             "angle": d_["angle"]}, point=True) for d_ in ev.get("doors", [])]))
    def actor_obj(ac):
        t = (ac.get("talk_events") or [{}])[0]
        c = ac["condition"]
        psy = ac.get("psynergy_events") or []
        return obj(f"actor slot {ac['slot']}", "actor", ac["x"], ac["z"], props={
            "slot": ac["slot"], "row": ac["index"], "source": ac["source"], "table": ac.get("table"),
            "sprite": ac["sprite"], "sprite_id": ac["sprite_id"], "party_member": int(ac["party_member"]),
            "y": ac["y"], "angle": ac["angle"], "behavior": str(ac["behavior"]), "flag": ac["flag"],
            "show": c["show"], "show_flag": c.get("flag"), "flag_scope": c.get("scope"),
            "psynergy_abilities": ",".join(str(p["ability"]) for p in psy) or None,
            "script": t.get("script"), "text_id": t.get("text_id")}, point=True)

    groups.append(("actors", [actor_obj(ac) for ac in ev.get("actors", [])]))
    if ev.get("actors_spawned"):
        groups.append(("actors (script-spawned)", [actor_obj(ac) for ac in ev["actors_spawned"]]))
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
                         "columns": A.get("tile_cols", 16), "margin": 0, "spacing": 0}]}
    if A.get("tile_anims"):
        tmj["tilesets"][0]["tiles"] = A["tile_anims"]
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
    ap.add_argument("--warps-only", action="store_true",
                    help="only re-read exits/entrances/doors of exported rooms and resolve arrivals (fast)")
    a = ap.parse_args(argv)
    gm = GsMaps(a.rom)
    print(f"{gm.rom.code}: rooms {gm.n_rooms} @0x{gm.rooms_addr | ROM_BASE:08X}, areas {gm.n_areas} "
          f"@0x{gm.areas_addr | ROM_BASE:08X} (+{gm.area_base}), place table "
          f"{'0x%08X' % (gm.place_addr | ROM_BASE) if gm.place_addr else None} ({len(gm.places)} rows)")
    if a.warps_only:
        print(json.dumps(refresh_warps(gm, None if a.all or not a.map else a.map)))
        return 0
    idx = export(gm, None if a.all or not a.map else a.map, render=not a.no_render)
    print(json.dumps(idx["coverage"]))


if __name__ == "__main__":
    sys.exit(main())
