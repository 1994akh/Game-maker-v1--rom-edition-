"""Read-only comparison of a GBA ROM hack against its clean base ROM.

Writes to reports/:
  summary.md           header info, hashes, change and free-space overview
  changed_regions.csv  contiguous ranges of the base ROM's address space that the hack changed
  free_space.csv       runs of 0xFF in the hack that are long enough to be usable free space

Usage: python tools/analyze_rom.py <hack.gba> <base.gba> [--min-free N] [--block N]
"""
import argparse
import csv
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"


def header(rom: bytes) -> dict:
    return {
        "title": rom[0xA0:0xAC].rstrip(b"\0").decode("ascii", "replace"),
        "code": rom[0xAC:0xB0].decode("ascii", "replace"),
        "maker": rom[0xB0:0xB2].decode("ascii", "replace"),
        "version": rom[0xBC],
    }


def changed_regions(hack: bytes, base: bytes, block: int):
    """Coalesce changed blocks into (start, end, bytes_changed) over the base's length."""
    regions, start, count = [], None, 0
    for off in range(0, len(base), block):
        a, b = base[off:off + block], hack[off:off + block]
        if a != b:
            n = sum(x != y for x, y in zip(a, b))
            if start is None:
                start, count = off, 0
            count += n
        elif start is not None:
            regions.append((start, off, count))
            start = None
    if start is not None:
        regions.append((start, len(base), count))
    return regions


def free_runs(rom: bytes, min_len: int):
    return [(m.start(), m.end()) for m in re.finditer(rb"\xff{%d,}" % min_len, rom)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hack")
    ap.add_argument("base")
    ap.add_argument("--min-free", type=int, default=256, help="shortest 0xFF run counted as free space")
    ap.add_argument("--block", type=int, default=0x100, help="diff granularity in bytes")
    args = ap.parse_args()

    hack = Path(args.hack).read_bytes()
    base = Path(args.base).read_bytes()
    REPORTS.mkdir(exist_ok=True)

    regions = changed_regions(hack, base, args.block)
    runs = free_runs(hack, args.min_free)

    with open(REPORTS / "changed_regions.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start", "end", "length", "bytes_changed"])
        for s, e, n in regions:
            w.writerow([f"0x{s:07X}", f"0x{e:07X}", e - s, n])

    with open(REPORTS / "free_space.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start", "end", "length"])
        for s, e in sorted(runs, key=lambda r: r[0]):
            w.writerow([f"0x{s:07X}", f"0x{e:07X}", e - s])

    mb = 1 << 20
    changed_bytes = sum(n for _, _, n in regions)
    changed_span = sum(e - s for s, e, _ in regions)
    total_free = sum(e - s for s, e in runs)
    added = hack[len(base):]
    added_used = len(added) - sum(min(e, len(hack)) - max(s, len(base))
                                  for s, e in runs if e > len(base))

    lines = ["# ROM analysis", ""]
    for label, path, rom in (("Hack", args.hack, hack), ("Base", args.base, base)):
        h = header(rom)
        lines.append(f"**{label}:** `{Path(path).name}`  ")
        lines.append(f"size {len(rom):,} bytes, SHA-1 `{hashlib.sha1(rom).hexdigest()}`, "
                     f"title `{h['title']}`, code `{h['code']}`, maker `{h['maker']}`, version {h['version']}")
        lines.append("")

    lines += [
        "## Changes inside the base ROM's address space",
        f"- {changed_bytes:,} of {len(base):,} bytes differ ({changed_bytes / len(base):.1%})",
        f"- spread over {len(regions):,} regions covering {changed_span:,} bytes "
        f"(at {args.block}-byte granularity)",
        "",
        "## Space beyond the base ROM",
        f"- {len(added):,} bytes added past 0x{len(base):07X}; about {added_used:,} of them in use",
        "",
        f"## Free space (0xFF runs of at least {args.min_free} bytes)",
        f"- total {total_free:,} bytes ({total_free / mb:.2f} MB) in {len(runs):,} runs",
        f"- largest: " + ", ".join(f"0x{s:07X} ({e - s:,})" for s, e in
                                   sorted(runs, key=lambda r: r[0] - r[1])[:5]),
        "",
        "## Per-MB breakdown",
        "",
        "| Range | Changed vs base | Free |",
        "|---|---|---|",
    ]
    for i in range(len(hack) // mb):
        lo, hi = i * mb, (i + 1) * mb
        if lo < len(base):
            n = sum(x != y for x, y in zip(base[lo:hi], hack[lo:hi]))
            chg = f"{n / (min(hi, len(base)) - lo):.1%}"
        else:
            chg = "added"
        free = sum(max(0, min(e, hi) - max(s, lo)) for s, e in runs)
        lines.append(f"| 0x{lo:07X} | {chg} | {free:,} |")

    (REPORTS / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
