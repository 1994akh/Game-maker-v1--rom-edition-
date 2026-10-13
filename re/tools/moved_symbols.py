"""Find where a hack relocated vanilla tables and functions.

For every vanilla symbol, collect each place the vanilla ROM stores a pointer to it (literal pools, pointer tables),
map those places to v1.0 addresses, and read what the hack stores there now. If most of them agree on a different
address, the symbol was moved (repointed) there.

Writes reports/moved_symbols.csv: name, kind, v1.0 address, new address, references agreeing / total.

Usage: python tools/moved_symbols.py [--min-agree 0.6]
"""
import argparse
import csv
import struct
from collections import Counter, defaultdict

import env
import symdiff as sd


def pointer_sites(rom):
    """{target_without_thumb_bit: [offset, ...]} for every aligned word in rom that is a ROM pointer."""
    sites = defaultdict(list)
    for i, (w,) in enumerate(struct.iter_unpack("<I", rom[: len(rom) & ~3])):
        if 0x08000000 <= w < 0x0A000000:
            sites[w & ~1].append(i * 4)
    return sites


def find_moved(hack, base, pairs, reloc, min_agree):
    base_sites = pointer_sites(base)
    out = []
    for name, va, vs, ra, rs in pairs:
        if not (0x08000000 <= va < 0x09000000):
            continue
        refs = base_sites.get(ra, [])
        if not refs:
            continue
        seen = Counter()
        for off in refs:
            pos = reloc(0x08000000 + off)
            if pos is None:
                continue
            p = pos - 0x08000000
            seen[struct.unpack_from("<I", hack, p)[0] & ~1] += 1
        if not seen:
            continue
        new, n = seen.most_common(1)[0]
        total = sum(seen.values())
        if new != va and 0x08000000 <= new < 0x0A000000 and n / total >= min_agree:
            out.append((name, va, vs, new, n, total, seen.get(va, 0)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-agree", type=float, default=0.6)
    args = ap.parse_args()

    hack, base = env.UNBOUND.read_bytes(), env.FIRERED_REV1.read_bytes()
    pairs = sd.pair_symbols(sd.read_sym(env.SYMBOLS_V10), sd.read_sym(env.SYMBOLS_REV1))
    reloc = sd.Relocator(pairs)
    source = sd.index_source(env.EXTERNAL / "pokefirered")
    moved = find_moved(hack, base, pairs, reloc, args.min_agree)

    env.REPORTS.mkdir(exist_ok=True)
    with open(env.REPORTS / "moved_symbols.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "kind", "source_file", "v10_addr", "size", "new_addr", "refs_to_new", "refs_total",
                    "refs_still_old"])
        for name, va, vs, new, n, total, old in sorted(moved, key=lambda m: m[1]):
            kind, src = source.get(name, ("unknown", ""))
            w.writerow([name, kind, src, f"0x{va:08X}", vs, f"0x{new:08X}", n, total, old])
    kinds = Counter(source.get(m[0], ("unknown",))[0] for m in moved)
    print(f"{len(moved):,} vanilla symbols moved: {dict(kinds)}")
    for m in moved:
        if m[0] in ("gSpeciesNames", "gBattleMoves", "gMoveNames", "gSpeciesInfo", "gBaseStats", "gTrainers",
                    "gEvolutionTable", "gLevelUpLearnsets", "gItems", "gAbilityNames"):
            print(f"  {m[0]}: 0x{m[1]:08X} -> 0x{m[3]:08X} ({m[4]}/{m[5]} refs)")


if __name__ == "__main__":
    main()
