"""Shared paths for the project's scripts. Import this before using pyghidra."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS = ROOT / "apps"
EXTERNAL = ROOT / "external"
REPORTS = ROOT / "reports"

ROMS = Path(r"C:\Users\aaron\OneDrive\Apps-Roms")
UNBOUND = ROMS / "Pokemon Unbound (v2.1.1.1).gba"
FIRERED_REV1 = ROMS / "Pokemon" / "Pokemon - FireRed Version (USA, Europe) (Rev 1).gba"

SYMBOLS_V10 = EXTERNAL / "pokefirered-symbols" / "pokefirered.sym"
SYMBOLS_REV1 = EXTERNAL / "pokefirered-symbols" / "pokefirered_rev1.sym"

ROM_BASE = 0x08000000

os.environ.setdefault("JAVA_HOME", str(next(APPS.glob("jdk-21*"))))
os.environ.setdefault("GHIDRA_INSTALL_DIR", str(next(APPS.glob("ghidra_*_PUBLIC"))))


def load_symbols(path):
    """Return {name: (rom_offset, size)} for symbols that live in ROM."""
    syms = {}
    for line in Path(path).read_text().splitlines():
        parts = line.split()
        if len(parts) != 4:
            continue
        addr, _, size, name = int(parts[0], 16), parts[1], int(parts[2], 16), parts[3]
        if ROM_BASE <= addr < ROM_BASE + 0x2000000:
            syms[name] = (addr - ROM_BASE, size)
    return syms
