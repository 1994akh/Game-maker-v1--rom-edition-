"""Export a game's master asset table (a pointer table that indexes most of the ROM, often including itself).

Each entry gets a size (distance to the next entry in address order), a guess at what it holds, and its first bytes,
so custom formats can be grouped and reverse-engineered by their headers.
"""
import csv
import re
from collections import Counter

from .rom import ROM_BASE


def classify(data, off, size, veneer_offsets):
    head = data[off:off + 16]
    if off in veneer_offsets:
        return "code module (export stubs)"
    if re.fullmatch(rb"[\x20-\x7e\n\r\t]+\x00*", data[off:off + min(size, 64)] or b"\0"):
        return "text/string"
    if size >= 32 and all(b == head[0] for b in data[off:off + min(size, 256)]):
        return "fill"
    if size >= 512 and head[:1] not in (b"\x00", b"\x01", b"\x02"):
        sample = data[off:off + 512]
        top_clear = sum(1 for i in range(1, len(sample), 2) if not sample[i] & 0x80)
        if top_clear >= 0.97 * (len(sample) // 2):
            return "raw BGR555 colour data"
    return f"type 0x{head[0]:02X}" if head else "empty"


def export(rom, table_addr, entries, veneer_offsets):
    data = rom.data
    t = table_addr - ROM_BASE
    ptrs = [int.from_bytes(data[t + 4 * i:t + 4 * i + 4], "little") for i in range(entries)]
    order = sorted(set(p for p in ptrs if ROM_BASE <= p < ROM_BASE + rom.size))
    nxt = {p: (order[i + 1] if i + 1 < len(order) else ROM_BASE + rom.size) for i, p in enumerate(order)}
    rows, kinds = [], Counter()
    for i, p in enumerate(ptrs):
        if not ROM_BASE <= p < ROM_BASE + rom.size:
            rows.append((i, f"0x{p:08X}", 0, "not a ROM pointer", ""))
            continue
        off, size = p - ROM_BASE, nxt[p] - p
        kind = classify(data, off, size, veneer_offsets)
        kinds[kind] += 1
        rows.append((i, f"0x{p:08X}", size, kind, data[off:off + 16].hex(" ")))
    path = rom.workspace / f"filetable_{table_addr:08X}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["index", "address", "size", "kind", "first_16_bytes"])
        w.writerows(rows)
    return path, kinds
