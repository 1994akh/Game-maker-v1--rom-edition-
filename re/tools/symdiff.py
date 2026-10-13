"""Symbol-by-symbol comparison of a FireRed-based hack against vanilla FireRed.

The hack is built on v1.0 but the clean ROM on hand is Rev 1. For every symbol in both maps, the Rev 1 bytes are
relocated to their v1.0 form (absolute pointers and Thumb BL calls are retargeted using the two symbol maps), then
compared with the hack at the symbol's v1.0 address. Differences are explained, where possible, with the patch lists
shipped by CFRU and DPE (hooks, repoints, routine pointers, byte replacements, special inserts).

Writes reports/symbol_diff.csv and reports/symbol_diff.md.

Usage: python tools/symdiff.py [--hack PATH] [--base PATH]
"""
import argparse
import bisect
import csv
import re
import struct
from collections import Counter, defaultdict
from pathlib import Path

import env

POINTER_REGIONS = ((0x02000000, 0x02040000), (0x03000000, 0x03008000), (0x08000000, 0x0A000000))


# ---------------------------------------------------------------- symbols

def read_sym(path):
    """Return a list of (addr, size, name) for every symbol, in file order."""
    out = []
    for line in Path(path).read_text().splitlines():
        p = line.split()
        if len(p) == 4:
            out.append((int(p[0], 16), int(p[2], 16), p[3]))
    return out


def pair_symbols(v10, rev1):
    """Pair symbols across versions by (name, occurrence). Returns [(name, v10_addr, v10_size, rev1_addr, rev1_size)]."""
    def keyed(syms):
        seen, out = Counter(), {}
        for addr, size, name in syms:
            out[(name, seen[name])] = (addr, size)
            seen[name] += 1
        return out, seen

    a, ca = keyed(v10)
    b, cb = keyed(rev1)
    pairs = []
    for key, (va, vs) in a.items():
        name = key[0]
        if key in b and ca[name] == cb[name]:
            ra, rs = b[key]
            pairs.append((name, va, vs, ra, rs))
    return pairs


class Relocator:
    """Maps Rev 1 addresses to v1.0 addresses using the delta of the nearest preceding paired symbol.

    `exact(addr)` reports whether addr lies inside a sized symbol (reliable) or only after a label (a guess).
    """

    def __init__(self, pairs):
        entries = sorted({(ra, va - ra, rs) for _, va, _, ra, rs in pairs})
        self.starts = [s for s, _, _ in entries]
        self.deltas = [d for _, d, _ in entries]
        self.ends = [s + z for s, _, z in entries]

    def __call__(self, addr):
        i = bisect.bisect_right(self.starts, addr) - 1
        if i < 0 or addr >> 24 != self.starts[i] >> 24:
            return None
        return addr + self.deltas[i]

    def exact(self, addr):
        i = bisect.bisect_right(self.starts, addr) - 1
        while i >= 0 and self.starts[i] > addr - 0x10000:
            if self.starts[i] <= addr < self.ends[i]:
                return True
            i -= 1
        return False


class SymbolIndex:
    """Names the symbol containing an address (v1.0 map)."""

    def __init__(self, syms):
        rows = sorted((a, max(s, 1), n) for a, s, n in syms)
        self.starts = [r[0] for r in rows]
        self.rows = rows

    def name(self, addr):
        i = bisect.bisect_right(self.starts, addr) - 1
        if i >= 0:
            a, s, n = self.rows[i]
            if addr < a + s:
                return n if addr == a else f"{n}+0x{addr - a:X}"
        return None


# ---------------------------------------------------------------- relocation

def is_pointer(word):
    return any(lo <= word < hi for lo, hi in POINTER_REGIONS)


def decode_bl(h1, h2, addr):
    if (h1 & 0xF800) != 0xF000 or (h2 & 0xF800) != 0xF800:
        return None
    off = ((h1 & 0x7FF) << 12) | ((h2 & 0x7FF) << 1)
    if off & 0x400000:
        off -= 0x800000
    return addr + 4 + off


def encode_bl(target, addr):
    off = target - (addr + 4)
    if not -0x400000 <= off < 0x400000:
        return None
    off &= 0x7FFFFF
    return 0xF000 | (off >> 12), 0xF800 | ((off >> 1) & 0x7FF)


def relocate(data, rev1_addr, v10_addr, reloc, func_starts, is_code):
    """Return (bytes as they should appear at v10_addr, set of offsets holding pointers, {offset: alternative}).

    Alternatives are the unrelocated bytes of pointers whose relocation is a guess; either form counts as a match.
    """
    out = bytearray(data)
    ptr_offsets = set()
    alternatives = {}
    # Absolute pointers in 4-byte aligned words (literal pools, pointer tables, struct fields).
    first = (-rev1_addr) % 4
    for off in range(first, len(data) - 3, 4):
        word = struct.unpack_from("<I", data, off)[0]
        target = word & ~1
        if is_pointer(word):
            ptr_offsets.add(off)
            new = reloc(target)
            if new is not None and new != target:
                struct.pack_into("<I", out, off, new | (word & 1))
                if not reloc.exact(target):
                    alternatives[off] = data[off:off + 4]
    # Thumb BL calls: relative, so they change whenever caller and callee shift by different amounts.
    if is_code:
        off = (rev1_addr & 1)
        while off < len(data) - 3:
            h1, h2 = struct.unpack_from("<HH", data, off)
            target = decode_bl(h1, h2, rev1_addr + off)
            if target is not None and target in func_starts:
                new_target = reloc(target)
                enc = encode_bl(new_target, v10_addr + off) if new_target is not None else None
                if enc:
                    struct.pack_into("<HH", out, off, *enc)
                    off += 4
                    continue
            off += 2
    return bytes(out), ptr_offsets, alternatives


def accept_alternatives(expected, actual, alternatives):
    """Where a guessed pointer relocation disagrees with the hack but the unrelocated value matches, use that."""
    exp = bytearray(expected)
    for off, alt in alternatives.items():
        if actual[off:off + 4] == alt:
            exp[off:off + 4] = alt
    return bytes(exp)


# ---------------------------------------------------------------- source index (pokefirered)

C_FUNC = re.compile(r"^(?:static\s+)?(?:inline\s+)?(?:NAKED\s+)?(?:const\s+)?(?:struct\s+)?\w[\w\s\*]*?\b(\w+)\s*\([^;{]*\)\s*\n\{",
                    re.M)
C_DATA = re.compile(r"^(?:static\s+)?(?:const\s+)?(?:(?:struct|union|enum)\s+)?\w+\s+(?:const\s+)?\**\s*(?:const\s+)?(\w+)"
                    r"\s*(?:\[[^\]]*\]\s*)*(?:ALIGNED\(\d+\)\s*)?=", re.M)
ASM_FUNC = re.compile(r"^\s*(?:thumb|arm|non_word_aligned_thumb)_func_start\s+(\w+)", re.M)
ASM_GLOBAL = re.compile(r"^\s*\.global\s+(\w+)", re.M)


def index_source(root):
    """Return {name: (kind, relative_file)} from the decomp's C and asm sources."""
    idx = {}
    for path in list(root.glob("src/**/*.c")) + list(root.glob("src/**/*.h")) + list(root.glob("asm/**/*.s")) + \
            list(root.glob("data/**/*.s")) + list(root.glob("data/**/*.inc")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix in (".c", ".h"):
            for m in C_FUNC.finditer(text):
                idx.setdefault(m.group(1), ("code", rel))
            for m in C_DATA.finditer(text):
                idx.setdefault(m.group(1), ("data", rel))
        else:
            for m in ASM_FUNC.finditer(text):
                idx.setdefault(m.group(1), ("code", rel))
            for m in ASM_GLOBAL.finditer(text):
                idx.setdefault(m.group(1), ("data", rel))
    return idx


# ---------------------------------------------------------------- patch lists (CFRU / DPE)

ADDR = r"(?:0x)?([0-9A-Fa-f]{6,8})"


def norm_addr(text):
    a = int(text, 16)
    return a if a >= 0x08000000 else a | 0x08000000


def load_patch_lists(projects):
    """Return [(start, end, source, kind, label)] in v1.0 addresses."""
    patches = []
    for proj, root in projects.items():
        def lines(name):
            p = root / name
            if not p.exists():
                return []
            return [l.split("@")[0].strip() for l in p.read_text(errors="replace").splitlines()
                    if l.strip() and not l.lstrip().startswith(("#", "@", "//"))]

        for l in lines("hooks"):
            m = re.match(rf"(\w+)\s+{ADDR}\s+(\d+)", l)
            if m:
                a = norm_addr(m.group(2)) & ~1
                patches.append((a, a + 12, proj, "hook", m.group(1)))
        for name, kind in (("routinepointers", "routine pointer"), ("repoints", "repoint")):
            for l in lines(name):
                m = re.match(rf"(\w+)\s+{ADDR}", l)
                if m:
                    a = norm_addr(m.group(2))
                    patches.append((a, a + 4, proj, kind, m.group(1)))
        for l in lines("bytereplacement"):
            m = re.match(rf"{ADDR}\s+((?:\S+\s*)+)$", l)
            if m:
                a = norm_addr(m.group(1))
                patches.append((a, a + max(1, len(m.group(2).split())), proj, "byte replacement", ""))
        sp = root / "special_inserts.asm"
        if sp.exists():
            label = ""
            for l in sp.read_text(errors="replace").splitlines():
                c = re.match(r"\s*@+\s*(.+)", l)
                if c:
                    label = c.group(1).strip()[:60]
                m = re.match(rf"\s*\.org\s+{ADDR}", l)
                if m:
                    a = norm_addr(m.group(1))
                    patches.append((a, a + 4, proj, "special insert", label))
    return sorted(patches)


def patches_in(patches, starts, lo, hi):
    i = bisect.bisect_left(starts, lo - 16)
    out = []
    while i < len(patches) and patches[i][0] < hi:
        if patches[i][1] > lo:
            out.append(patches[i])
        i += 1
    return out


# ---------------------------------------------------------------- classification

def diff_offsets(a, b):
    return [i for i, (x, y) in enumerate(zip(a, b)) if x != y]


def classify(expected, actual, ptr_offsets, size, patches, v10_addr, names):
    diffs = diff_offsets(expected, actual)
    if not diffs:
        return "unchanged", 0, ""
    notes = []
    hooks = [p for p in patches if p[3] == "hook"]
    if hooks:
        notes.append("; ".join(f"{p[2]} hook {p[4]} @0x{p[0]:07X}" for p in hooks))
    other = Counter(f"{p[2]} {p[3]}" for p in patches if p[3] != "hook")
    if other:
        notes.append(", ".join(f"{k} x{v}" if v > 1 else k for k, v in other.items()))

    # Are all differences inside pointer words or retargeted BL calls?
    refs = {}
    align = (-v10_addr) % 4
    for d in diffs:
        w = d - ((d - align) % 4)
        if w >= 0 and w + 4 <= size and (w in ptr_offsets or is_pointer(struct.unpack_from("<I", expected, w)[0])) \
                and is_pointer(struct.unpack_from("<I", actual, w)[0]):
            old = struct.unpack_from("<I", expected, w)[0] & ~1
            new = struct.unpack_from("<I", actual, w)[0] & ~1
            refs[w] = f"{names.name(old) or hex(old)} -> {names.name(new) or f'0x{new:07X}'}"
            continue
        for b in (d - (d - (v10_addr & 1)) % 2, d - (d - (v10_addr & 1)) % 2 - 2):
            if b < 0 or b + 4 > size or b in refs:
                continue
            te = decode_bl(*struct.unpack_from("<HH", expected, b), v10_addr + b)
            ta = decode_bl(*struct.unpack_from("<HH", actual, b), v10_addr + b)
            if te is not None and ta is not None:
                refs[b] = f"call {names.name(te) or hex(te)} -> {names.name(ta) or f'0x{ta:07X}'}"
                break
        else:
            refs = None
            break
    if refs:
        moved = [refs[k] for k in sorted(refs)][:6]
        if len(refs) > 6:
            moved.append(f"... {len(refs) - 6} more")
        notes.append("refs: " + "; ".join(moved))
        status = "calls redirected" if any(v.startswith("call") for v in refs.values()) else "references moved"
        return status, len(diffs), " | ".join(notes)

    pct = len(diffs) / size
    if hooks:
        status = "hooked"
    elif pct > 0.5:
        status = "overwritten"
    elif max(diffs) - min(diffs) < 16:
        # A small patch; if it contains ldr+bx it is an unlisted hook.
        chunk = actual[min(diffs) & ~1: max(diffs) + 2]
        has_bx = any((chunk[i + 1] == 0x47 and chunk[i] & 0x87 == 0) for i in range(0, len(chunk) - 1, 2))
        status = "hooked (unlisted)" if has_bx else "patched"
    else:
        status = "modified"
    return status, len(diffs), " | ".join(notes)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hack", default=str(env.UNBOUND))
    ap.add_argument("--base", default=str(env.FIRERED_REV1))
    args = ap.parse_args()

    hack = Path(args.hack).read_bytes()
    base = Path(args.base).read_bytes()
    v10 = read_sym(env.SYMBOLS_V10)
    rev1 = read_sym(env.SYMBOLS_REV1)
    pairs = pair_symbols(v10, rev1)
    reloc = Relocator(pairs)
    names = SymbolIndex(v10)
    source = index_source(env.EXTERNAL / "pokefirered")
    # BL targets: any paired symbol start not known to be data (library functions aren't in the source index).
    func_starts_rev1 = {ra for name, _, _, ra, _ in pairs if source.get(name, ("unknown",))[0] != "data"}
    patches = load_patch_lists({"CFRU": env.EXTERNAL / "Complete-Fire-Red-Upgrade",
                                "DPE": env.EXTERNAL / "DPE-Unbound"})
    patch_starts = [p[0] for p in patches]

    rows = []
    for name, va, vs, ra, rs in pairs:
        if not (0x08000000 <= va < 0x09000000) or vs == 0:
            continue
        kind, src = source.get(name, ("unknown", ""))
        if vs != rs:
            rows.append(dict(name=name, kind=kind, file=src, v10=va, rev1=ra, size=vs, status="differs v1.0/Rev 1",
                             diff=0, note=f"size {vs} in v1.0, {rs} in Rev 1"))
            continue
        exp, ptrs, alts = relocate(base[ra - 0x08000000: ra - 0x08000000 + rs], ra, va, reloc, func_starts_rev1,
                                   kind != "data")
        act = hack[va - 0x08000000: va - 0x08000000 + vs]
        exp = accept_alternatives(exp, act, alts)
        pl = patches_in(patches, patch_starts, va, va + vs)
        status, ndiff, note = classify(exp, act, ptrs, vs, pl, va, names)
        rows.append(dict(name=name, kind=kind, file=src, v10=va, rev1=ra, size=vs, status=status, diff=ndiff,
                         note=note))

    env.REPORTS.mkdir(exist_ok=True)
    with open(env.REPORTS / "symbol_diff.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "kind", "source_file", "v10_addr", "rev1_addr", "size", "status", "bytes_changed",
                    "pct_changed", "note"])
        for r in sorted(rows, key=lambda r: r["v10"]):
            w.writerow([r["name"], r["kind"], r["file"], f"0x{r['v10']:08X}", f"0x{r['rev1']:08X}", r["size"],
                        r["status"], r["diff"], f"{r['diff'] / r['size']:.0%}", r["note"]])

    write_summary(rows, patches)


SYSTEMS = [  # first match wins; matched against the decomp source path
    ("Battle engine & AI", r"battle|pokeball|/reshow_battle|/trainer_slide"),
    ("Pokémon data & rules", r"data/pokemon/|/pokemon\.c|/evolution|/daycare|/egg_hatch|/pokemon_storage|/pokemon_icon"),
    ("Trainers", r"trainer"),
    ("Graphics & tilesets", r"data/graphics/|/graphics\.c|data/tilesets/|object_event_graphics|object_event_pic"),
    ("Text & strings", r"strings\.c|data/text/|pokedex_text|move_descriptions|easy_chat"),
    ("Maps, overworld & scripts", r"field_|event_object|overworld|fieldmap|/map_|region_map|scrcmd|script|"
                                  r"wild_encounter|data/maps|metatile|/event_data|/fldeff|/coord_event|heal_location"),
    ("Menus & UI", r"menu|pokedex|summary_screen|start_menu|list_menu|text_window|naming_screen|berry_pouch|"
                   r"tm_case|/bag|/shop|/option|/new_game|oak_speech|/title_screen|/intro"),
    ("Audio", r"m4a|sound|/music|data/sound"),
    ("Core engine", r"/main\.c|gpu_regs|malloc|/task\.c|/sprite\.c|/bg\.c|/window\.c|dma3|decompress|/save|flash|"
                    r"/random|/palette|/text\.c|/string_util|/blit|/scanline|/agb|/lib|/m4a|/rtc|/link|/isagbprn"),
]


def system_of(path):
    for name, pat in SYSTEMS:
        if re.search(pat, path):
            return name
    return "Other" if path else "Unindexed (libraries, asm data)"


def write_summary(rows, patches):
    order = ["unchanged", "references moved", "calls redirected", "patched", "hooked", "hooked (unlisted)",
             "modified", "overwritten", "differs v1.0/Rev 1"]
    L = ["# Symbol-by-symbol diff: Unbound vs FireRed v1.0", "",
         "Each original FireRed function or table was relocated from Rev 1 to its v1.0 address and compared with "
         "Unbound. Full list: `symbol_diff.csv`.", "",
         "## Status counts", "", "| Status | Code | Data | Unknown | Total | Bytes |", "|---|---|---|---|---|---|"]
    for st in order:
        sel = [r for r in rows if r["status"] == st]
        if not sel:
            continue
        c = Counter(r["kind"] for r in sel)
        L.append(f"| {st} | {c['code']:,} | {c['data']:,} | {c['unknown']:,} | {len(sel):,} | "
                 f"{sum(r['size'] for r in sel):,} |")
    L += ["", "Statuses:",
          "- **unchanged**: identical to vanilla after relocation.",
          "- **references moved**: code and data intact, only pointers changed (a table or function it uses was "
          "replaced elsewhere).",
          "- **calls redirected**: code intact except `BL` calls now going to different functions.",
          "- **patched**: a small edit (under 16 bytes) with no branch out.",
          "- **hooked**: CFRU or DPE redirects it to new code (named in the note).",
          "- **hooked (unlisted)**: small `ldr`+`bx` style redirect not in the public CFRU/DPE lists, so likely "
          "Unbound-specific.",
          "- **modified**: larger edits that keep most of the original.",
          "- **overwritten**: more than half the bytes differ; the space was reused or the routine replaced.",
          "- **differs v1.0/Rev 1**: the symbol changed size between versions, so it can't be compared exactly.", ""]

    # Rollup by game system: what can be reused straight from the vanilla decomp vs what Unbound replaced.
    L += ["## By game system", "",
          "Share of each system's original symbols that are still byte-identical in Unbound (after relocation). "
          "High means the pokefirered source still describes Unbound's version; low means Unbound/CFRU/DPE "
          "replaced it.", "",
          "| System | Code unchanged | Data unchanged | Hooked | Patched/modified | Overwritten |",
          "|---|---|---|---|---|---|"]
    per_sys = defaultdict(Counter)
    for r in rows:
        s = system_of(r["file"])
        per_sys[s][r["kind"] + "_total"] += 1
        per_sys[s][r["kind"] + "_" + r["status"]] += 1
        per_sys[s][r["status"]] += 1

    def share(c, kind):
        t = c[kind + "_total"]
        return f"{c[kind + '_unchanged'] / t:.0%} of {t:,}" if t else "–"

    for s, _ in SYSTEMS + [("Other", ""), ("Unindexed (libraries, asm data)", "")]:
        c = per_sys.get(s)
        if not c:
            continue
        L.append(f"| {s} | {share(c, 'code')} | {share(c, 'data')} | "
                 f"{c['hooked'] + c['hooked (unlisted)']:,} | {c['patched'] + c['modified']:,} | "
                 f"{c['overwritten']:,} |")
    L.append("")

    # Source files with most changes (code only).
    changed = [r for r in rows if r["status"] not in ("unchanged", "differs v1.0/Rev 1") and r["file"]]
    per_file = defaultdict(lambda: Counter())
    for r in rows:
        if r["file"]:
            per_file[r["file"]]["total"] += 1
            if r in changed:
                per_file[r["file"]][r["status"]] += 1
    top = sorted(per_file.items(), key=lambda kv: -(kv[1]["total"] - kv[1]["unchanged"] if False else
                                                    sum(v for k, v in kv[1].items() if k != "total")))[:30]
    L += ["## Source files with the most changed symbols", "",
          "| File | Changed / total | Hooked | Modified/overwritten | Refs moved |", "|---|---|---|---|---|"]
    for f, c in top:
        ch = sum(v for k, v in c.items() if k != "total")
        if not ch:
            break
        L.append(f"| `{f}` | {ch}/{c['total']} | {c['hooked'] + c['hooked (unlisted)']} | "
                 f"{c['modified'] + c['overwritten']} | {c['references moved']} |")

    # Changes not explained by CFRU/DPE.
    unexplained = [r for r in rows if r["status"] in ("modified", "overwritten", "hooked (unlisted)", "patched")
                   and "CFRU" not in r["note"] and "DPE" not in r["note"] and r["kind"] == "code"]
    unexplained.sort(key=lambda r: -r["diff"])
    L += ["", f"## Code changes not explained by public CFRU/DPE lists ({len(unexplained):,})", "",
          "Likely Unbound-specific edits, or CFRU changes made after the public version. Top 40 by bytes changed:",
          "", "| Function | File | Status | Bytes changed / size |", "|---|---|---|---|"]
    for r in unexplained[:40]:
        L.append(f"| `{r['name']}` | `{r['file']}` | {r['status']} | {r['diff']}/{r['size']} |")

    hooked = [r for r in rows if r["status"] == "hooked"]
    by_src = Counter(p[2] for p in patches if p[3] == "hook")
    L += ["", "## Patch-list coverage", "",
          f"- CFRU/DPE hook entries: {sum(by_src.values())} ({', '.join(f'{k} {v}' for k, v in by_src.items())}); "
          f"vanilla symbols carrying at least one: {len(hooked)}"]
    (env.REPORTS / "symbol_diff.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:20]))


if __name__ == "__main__":
    main()
