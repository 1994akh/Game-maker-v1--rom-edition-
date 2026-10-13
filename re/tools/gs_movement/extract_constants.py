"""Re-derive Golden Sun 1/2 field-movement constants straight from the ROM bytes (static, no emulator).

Usage (from C:\\Users\\aaron\\Documents\\UnboundHack):
    .venv\\Scripts\\python.exe tools\\gs_movement\\extract_constants.py [--gs1 ROM] [--gs2 ROM] [--out FILE]

For each ROM it finds, by pattern rather than by hard-coded address:
  - the only KEYINPUT (0x04000130) reader and the RAM key words it writes (held / new presses / sticky);
  - the 16-entry d-pad -> angle table (u16, 0x10000 = 360 deg) and every function that loads it
    (= the field movement controllers);
  - in each controller, the constants stored to object +0x30 (max speed) and +0x34 (acceleration)
    and the distances passed to the polar-offset routine (probe lengths), all 16.16 fixed point;
  - the polar-offset routine itself (GS1 0x0800447C) and its 1024-step sine table;
  - the "talk to the nearest actor" literal pool (|dy| limit, angle window).
Writes UTF-8 JSON (default tools\\gs_movement\\out\\gs_movement_constants.json).
"""
import argparse
import json
import math
import struct
import sys
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from gbax import re as R  # noqa: E402
from gbax.rom import Rom  # noqa: E402

GS1 = ROOT / "games" / "AGSE-5c469520-Golden-Sun-USA-Europe" / "rom" / "Golden Sun (USA, Europe).gba"
GS2 = Path(r"C:\Users\aaron\OneDrive\Apps-Roms\Golden Sun - The Lost Age (USA, Europe).gba")
BASE = 0x08000000
DIR_TABLE = struct.pack("<16H", 0xFFFF, 0, 0x8000, 0xFFFF, 0xC000, 0xE000, 0xA000, 0xC000,
                        0x4000, 0x2000, 0x6000, 0x4000, 0xFFFF, 0, 0x8000, 0xFFFF)
# GS1 0x0800447C polar offset: push {r5,r6,lr}; mov r6,sl; mov r5,r8; push {r5,r6}; mov sl,r0; movs r0,#0x80;
# mov r8,r1; lsls r0,r0,#7; add r0,r8; adds r5,r2,#0  (no PC-relative bytes)
POLAR_SIG = bytes.fromhex("60b55646 4546 60b4 8246 8020 8846 c001 4044 151c".replace(" ", ""))
DPAD_INDEX = ["none", "R", "L", "R+L", "U", "U+R", "U+L", "U+R+L", "D", "D+R", "D+L", "D+R+L",
              "U+D", "U+D+R", "U+D+L", "all"]

md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail = True


def fx(v):
    """16.16 fixed point -> float pixels."""
    v = v - (1 << 32) if v & 0x80000000 else v
    return round(v / 65536, 5)


def func_start(rom, addr, limit=0x400):
    """Walk back to the nearest `push {..., lr}`."""
    for a in range(addr & ~1, addr - limit, -2):
        h = int.from_bytes(rom.data[a - BASE:a - BASE + 2], "little")
        if (h & 0xFF00) == 0xB500:
            return a
    return None


def sweep(rom, start, polar, length=0x700):
    """Linear Thumb sweep with naive constant tracking. Records str to [obj,#0x30/#0x34] and polar-call r0."""
    regs, stores, probes = {}, [], []
    for i in md.disasm(rom.data[start - BASE:start - BASE + length], start):
        m, ops = i.mnemonic, i.operands
        if m in ("pop",) and any(o.type == ARM_OP_REG and i.reg_name(o.reg) == "pc" for o in ops):
            break
        if m == "movs" and len(ops) == 2 and ops[1].type == ARM_OP_IMM:
            regs[ops[0].reg] = ops[1].imm
        elif m == "lsls" and len(ops) == 3 and ops[2].type == ARM_OP_IMM and ops[1].reg in regs:
            regs[ops[0].reg] = (regs[ops[1].reg] << ops[2].imm) & 0xFFFFFFFF
        elif m == "ldr" and len(ops) == 2 and ops[1].type == ARM_OP_MEM and i.reg_name(ops[1].mem.base) == "pc":
            la = ((i.address + 4) & ~3) + ops[1].mem.disp
            regs[ops[0].reg] = rom.u32(la - BASE)
        elif m == "str" and len(ops) == 2 and ops[1].type == ARM_OP_MEM and ops[1].mem.disp in (0x30, 0x34) \
                and ops[0].reg in regs:
            stores.append(dict(at=f"0x{i.address:08X}", field=f"+0x{ops[1].mem.disp:02X}",
                               value=f"0x{regs[ops[0].reg]:X}", px=fx(regs[ops[0].reg])))
        elif m == "bl":
            if ops[0].imm == polar:
                r0 = regs.get(md.disasm(b"\x00\x20", 0).__next__().operands[0].reg)  # r0 register id
                probes.append(dict(at=f"0x{i.address:08X}", dist=None if r0 is None else f"0x{r0:X}",
                                   px=None if r0 is None else fx(r0)))
            regs = {}
        elif ops and ops[0].type == ARM_OP_REG and m not in ("cmp", "tst", "cmn", "str", "strh", "strb", "push"):
            regs.pop(ops[0].reg, None)
    return stores, probes


def analyse(path):
    rom = Rom.load(path)
    out = dict(rom=str(path), code=rom.code, sha1=rom.sha1)
    # key reader
    keys = []
    for w in R.find_refs(rom, 0x04000130):
        for ld in R.find_literal_loads(rom, w):
            lits = []
            for i in md.disasm(rom.data[ld - BASE:ld - BASE + 0x30], ld):
                if i.mnemonic == "ldr" and "pc" in i.op_str:
                    v = rom.u32(((i.address + 4) & ~3) + int(i.op_str.split("#")[1].rstrip("]"), 0) - BASE)
                    if v >> 24 == 3:
                        lits.append(f"0x{v:08X}")
            keys.append(dict(reader=f"0x{ld:08X}", ram_words=lits))
    out["keyinput_readers"] = keys
    # polar routine + sine table
    p = rom.data.find(POLAR_SIG)
    polar = p + BASE if p >= 0 else None
    out["polar_offset_routine"] = None if polar is None else f"0x{polar:08X}"
    sine = rom.data.find(struct.pack("<4H", 0, 0x0192, 0x0324, 0x04B6))
    if sine >= 0:
        tab = struct.unpack_from("<257H", rom.data, sine)
        err = max(abs(tab[k] - min(0xFFFF, round(65536 * math.sin(k * math.pi / 512)))) for k in range(257))
        out["sine_table"] = dict(address=f"0x{sine + BASE:08X}", entries=257, max_abs_error_vs_sin=err,
                                 unit="1.0 = 0x10000, 1024 steps per circle")
    # direction table and controllers
    tables = []
    i = -1
    while (i := rom.data.find(DIR_TABLE, i + 1)) >= 0:
        users = []
        for w in R.find_refs(rom, i + BASE):
            for ld in R.find_literal_loads(rom, w):
                fs = func_start(rom, ld)
                stores, probes = sweep(rom, fs, polar) if fs and polar else ([], [])
                users.append(dict(load=f"0x{ld:08X}", function=None if fs is None else f"0x{fs:08X}",
                                  speed_stores=stores, polar_probes=probes))
        tables.append(dict(address=f"0x{i + BASE:08X}", users=users))
    out["dpad_angle_table"] = dict(index="(KEYS >> 4) & 0xF; bit0 Right, bit1 Left, bit2 Up, bit3 Down",
                                   angles={DPAD_INDEX[k]: f"0x{struct.unpack_from('<H', DIR_TABLE, 2 * k)[0]:04X}"
                                           for k in range(16)}, copies=tables)
    # NPC talk search literal pool: |dy| limit, then (after one word) the angle window
    j = rom.data.find(struct.pack("<I", 0x002FFFFF))
    pools = []
    while j >= 0:
        win = rom.data[j:j + 20]
        if struct.pack("<I", 0xFFFFD001) in win:  # upper bound 0x2FFF is a literal (GS1) or an immediate (GS2)
            pools.append(f"0x{j + BASE:08X}")
        j = rom.data.find(struct.pack("<I", 0x002FFFFF), j + 4)
    out["talk_probe_literal_pool"] = dict(addresses=pools, dy_limit_px=fx(0x002FFFFF),
                                          angle_window=["-0x2FFF", "+0x2FFF"], deg=round(0x2FFF * 360 / 65536, 2))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gs1", default=str(GS1))
    ap.add_argument("--gs2", default=str(GS2))
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "out" / "gs_movement_constants.json"))
    a = ap.parse_args()
    res = {"GS1": analyse(a.gs1), "GS2": analyse(a.gs2)}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1), encoding="utf-8")
    for g, r in res.items():
        print(g, r["code"], "keys", r["keyinput_readers"], "polar", r["polar_offset_routine"],
              "sine", r.get("sine_table", {}).get("address"))
        for t in r["dpad_angle_table"]["copies"]:
            for u in t["users"]:
                sp = ", ".join(f"{s['field']}={s['px']}" for s in u["speed_stores"])
                pr = sorted({p["px"] for p in u["polar_probes"] if p["px"] is not None})
                print(f"  table {t['address']} fn {u['function']}: {sp} | probes px {pr}")
        print("  talk pool", r["talk_probe_literal_pool"]["addresses"])
    print("wrote", a.out)


if __name__ == "__main__":
    main()
