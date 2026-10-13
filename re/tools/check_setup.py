"""Smoke test: symbols line up with the ROMs, and pyghidra can start Ghidra."""
import sys

import env

CHARMAP = {0x00: " ", 0xFF: "$", **{0xBB + i: chr(65 + i) for i in range(26)},
           **{0xD5 + i: chr(97 + i) for i in range(26)}, **{0xA1 + i: str(i) for i in range(10)}}


def decode(raw):
    return "".join(CHARMAP.get(b, "?") for b in raw).split("$")[0]


def species_name(rom, syms, idx):
    off, _ = syms["gSpeciesNames"]
    return decode(rom[off + idx * 11: off + (idx + 1) * 11])


v10 = env.load_symbols(env.SYMBOLS_V10)
rev1 = env.load_symbols(env.SYMBOLS_REV1)
base = env.FIRERED_REV1.read_bytes()
hack = env.UNBOUND.read_bytes()

print(f"symbols in ROM: v1.0 {len(v10):,}, rev1 {len(rev1):,}")
print("FireRed rev1, gSpeciesNames[1..3]:", [species_name(base, rev1, i) for i in (1, 2, 3)])
print("Unbound at v1.0 gSpeciesNames[1..3]:", [species_name(hack, v10, i) for i in (1, 2, 3)])

if "--ghidra" in sys.argv:
    import pyghidra
    pyghidra.start()
    from ghidra.framework import Application
    print("Ghidra started:", Application.getApplicationVersion())
