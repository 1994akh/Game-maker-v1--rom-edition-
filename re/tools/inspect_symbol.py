"""Show how one or more vanilla symbols differ in the hack: changed byte ranges, with Thumb BL and pointer decoding.

Usage: python tools/inspect_symbol.py NAME [NAME ...]
       python tools/inspect_symbol.py --status patched --kind code --sample 15
"""
import argparse
import csv
import random
import struct

import env
import symdiff as sd


def describe_word(buf, off, addr, names):
    if off + 4 > len(buf):
        return ""
    h1, h2 = struct.unpack_from("<HH", buf, off)
    t = sd.decode_bl(h1, h2, addr + off)
    if t is not None:
        return f"BL {names.name(t) or hex(t)}"
    if (addr + off) % 4 == 0:
        w = struct.unpack_from("<I", buf, off)[0]
        if sd.is_pointer(w):
            return f".word {names.name(w & ~1) or hex(w)}"
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--status")
    ap.add_argument("--kind")
    ap.add_argument("--sample", type=int, default=10)
    args = ap.parse_args()

    names = list(args.names)
    if args.status:
        with open(env.REPORTS / "symbol_diff.csv", encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r["status"] == args.status and (not args.kind or r["kind"] == args.kind)]
        random.seed(0)
        names += [r["name"] for r in random.sample(rows, min(args.sample, len(rows)))]

    hack, base = env.UNBOUND.read_bytes(), env.FIRERED_REV1.read_bytes()
    v10, rev1 = sd.read_sym(env.SYMBOLS_V10), sd.read_sym(env.SYMBOLS_REV1)
    pairs = {p[0]: p for p in sd.pair_symbols(v10, rev1)}
    reloc = sd.Relocator(pairs.values())
    idx_v10, idx_rev1 = sd.SymbolIndex(v10), sd.SymbolIndex(rev1)
    source = sd.index_source(env.EXTERNAL / "pokefirered")
    funcs = {p[3] for n, p in pairs.items() if source.get(n, ("unknown",))[0] != "data"}

    for name in names:
        _, va, vs, ra, rs = pairs[name]
        kind = source.get(name, ("unknown", ""))[0]
        exp, _, alts = sd.relocate(base[ra - 0x08000000: ra - 0x08000000 + rs], ra, va, reloc, funcs, kind != "data")
        act = hack[va - 0x08000000: va - 0x08000000 + vs]
        exp = sd.accept_alternatives(exp, act, alts)
        orig = base[ra - 0x08000000: ra - 0x08000000 + rs]
        diffs = sd.diff_offsets(exp, act)
        print(f"== {name} ({kind}) v1.0 0x{va:08X} size {vs}: {len(diffs)} bytes differ")
        shown = set()
        for d in diffs:
            o = d & ~3
            if o in shown:
                continue
            shown.add(o)
            print(f"  +0x{o:04X} rev1 {orig[o:o+4].hex(' ')} [{describe_word(orig, o, ra, idx_rev1)}]"
                  f" -> expect {exp[o:o+4].hex(' ')} [{describe_word(exp, o, va, idx_v10)}]"
                  f" | hack {act[o:o+4].hex(' ')} [{describe_word(act, o, va, idx_v10)}]")
            if len(shown) >= 6:
                print("  ...")
                break


if __name__ == "__main__":
    main()
