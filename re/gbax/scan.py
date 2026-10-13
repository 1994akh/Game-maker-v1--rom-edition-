"""Map an unknown ROM: pointers, pointer tables, compressed blobs, code seeds, BIOS calls, entropy, free space."""
from collections import Counter

import numpy as np

from . import compression
from .rom import ROM_BASE

BIOS_CALLS = {
    0x00: "SoftReset", 0x01: "RegisterRamReset", 0x02: "Halt", 0x03: "Stop", 0x04: "IntrWait", 0x05: "VBlankIntrWait",
    0x06: "Div", 0x07: "DivArm", 0x08: "Sqrt", 0x09: "ArcTan", 0x0A: "ArcTan2", 0x0B: "CpuSet", 0x0C: "CpuFastSet",
    0x0D: "GetBiosChecksum", 0x0E: "BgAffineSet", 0x0F: "ObjAffineSet", 0x10: "BitUnPack", 0x11: "LZ77UnCompWram",
    0x12: "LZ77UnCompVram", 0x13: "HuffUnComp", 0x14: "RLUnCompWram", 0x15: "RLUnCompVram",
    0x16: "Diff8bitUnFilterWram", 0x17: "Diff8bitUnFilterVram", 0x18: "Diff16bitUnFilter", 0x19: "SoundBias",
    0x1A: "SoundDriverInit", 0x1B: "SoundDriverMode", 0x1C: "SoundDriverMain", 0x1D: "SoundDriverVSync",
    0x1E: "SoundChannelClear", 0x1F: "MidiKey2Freq", 0x25: "MultiBoot", 0x28: "SoundDriverVSyncOff",
    0x29: "SoundDriverVSyncOn",
}


def words(data):
    return np.frombuffer(data[: len(data) & ~3], dtype="<u4")


def halfwords(data):
    return np.frombuffer(data[: len(data) & ~1], dtype="<u2")


def pointer_census(data):
    """Return (offsets of aligned words that point into this ROM, their targets without the Thumb bit)."""
    w = words(data).astype(np.int64)
    hi = ROM_BASE + len(data)
    mask = (w >= ROM_BASE) & (w < hi)
    offs = np.nonzero(mask)[0] * 4
    return offs, (w[mask] & ~1) - ROM_BASE, (w[mask] & 1).astype(bool)


def pointer_tables(ptr_offs, min_len=4):
    """Runs of consecutive pointer words: [(start, count)]."""
    out = []
    if len(ptr_offs) == 0:
        return out
    run_start, prev = ptr_offs[0], ptr_offs[0]
    for o in ptr_offs[1:]:
        if o != prev + 4:
            n = (prev - run_start) // 4 + 1
            if n >= min_len:
                out.append((int(run_start), int(n)))
            run_start = o
        prev = o
    n = (prev - run_start) // 4 + 1
    if n >= min_len:
        out.append((int(run_start), int(n)))
    return out


def thumb_bl_targets(data):
    """Count Thumb BL call targets (ROM offsets)."""
    h = halfwords(data).astype(np.int64)
    first = (h[:-1] & 0xF800) == 0xF000
    second = (h[1:] & 0xF800) == 0xF800
    idx = np.nonzero(first & second)[0]
    off = ((h[idx] & 0x7FF) << 12) | ((h[idx + 1] & 0x7FF) << 1)
    off = np.where(off & 0x400000, off - 0x800000, off)
    tgt = idx * 2 + 4 + off
    tgt = tgt[(tgt >= 0) & (tgt < len(data))]
    return Counter(tgt.tolist())


def veneers(data):
    """Thumb long-jump stubs 'ldr rX,[pc,#0]; bx rX; .word target|1' (module export tables, patch hooks).

    Returns {stub_offset: target_offset}.
    """
    h = halfwords(data)
    out = {}
    idx = np.nonzero(((h[:-1] & 0xF8FF) == 0x4800) & ((h[1:] & 0xFF87) == 0x4700))[0]
    for i in idx:
        reg = (int(h[i]) >> 8) & 7
        if (int(h[i + 1]) >> 3) & 0xF != reg or (i * 2) % 4:
            continue
        tgt = int.from_bytes(data[i * 2 + 4:i * 2 + 8], "little")
        if tgt & 1 and ROM_BASE <= tgt < ROM_BASE + len(data):
            out[int(i * 2)] = (tgt & ~1) - ROM_BASE
    return out


def master_tables(tables, ptr_targets_at, size):
    """Pointer tables whose entries reach across most of the ROM: likely a game's asset/file index."""
    out = []
    for start, n in tables:
        if n < 100:
            continue
        tg = ptr_targets_at(start, n)
        span = (max(tg) - min(tg)) / size
        if span > 0.5:
            out.append({"address": f"0x{start + ROM_BASE:08X}", "entries": n, "span": round(span, 2),
                        "self_reference": bool(any(t == start for t in tg))})
    return out


def function_seeds(data, bl_targets, thumb_ptrs):
    """Likely Thumb function starts: BL targets or Thumb-bit pointers that begin with PUSH or a typical leaf opcode."""
    h = halfwords(data)
    seeds = {}
    for t, n in bl_targets.items():
        if t % 2 == 0 and t // 2 < len(h):
            op = int(h[t // 2])
            if (op & 0xFE00) == 0xB400 and op & 0x100:  # push {..., lr}
                seeds[t] = ("bl", n)
            elif n >= 3:
                seeds[t] = ("bl", n)
    for t in thumb_ptrs:
        if t % 2 == 0 and t // 2 < len(h) and (int(h[t // 2]) & 0xFE00) == 0xB400:
            seeds.setdefault(int(t), ("ptr", 0))
    return seeds


def bios_calls(data):
    """BIOS functions used, from Thumb 'swi n; bx lr' stubs (how SDKs wrap them) and inline swi counts."""
    stubs, inline = {}, Counter()
    h = halfwords(data)
    swi = np.nonzero((h & 0xFF00) == 0xDF00)[0]
    for i in swi:
        n = int(h[i]) & 0xFF
        if n not in BIOS_CALLS:
            continue
        inline[BIOS_CALLS[n]] += 1
        if i + 1 < len(h) and h[i + 1] == 0x4770:
            stubs.setdefault(BIOS_CALLS[n], int(i * 2))
    return stubs, inline


def entropy_map(data, block=0x10000):
    out = []
    for s in range(0, len(data), block):
        b = np.frombuffer(data[s:s + block], dtype=np.uint8)
        counts = np.bincount(b, minlength=256)
        p = counts[counts > 0] / len(b)
        out.append((s, float(-(p * np.log2(p)).sum()), float(counts[0xFF] / len(b)), float(counts[0] / len(b))))
    return out


def free_runs(data, min_len=0x400):
    out = []
    for fill in (0xFF, 0x00):
        b = np.frombuffer(data, dtype=np.uint8) == fill
        d = np.diff(np.concatenate(([0], b.astype(np.int8), [0])))
        starts, ends = np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]
        for s, e in zip(starts, ends):
            if e - s >= min_len:
                out.append((int(s), int(e - s), f"0x{fill:02X}"))
    return sorted(out)


def compressed_blobs(data, candidates, min_size=32):
    """Decode every candidate offset; return [(offset, kind, decoded_size, compressed_size, data)]."""
    out = []
    for off in sorted(set(int(c) for c in candidates)):
        if off % 4:
            continue
        r = compression.try_decode(data, off, min_size=min_size)
        if r:
            kind, dec, clen = r
            out.append((off, kind, len(dec), clen, dec))
    return out


def scan(rom, deep=False):
    data = rom.data
    ptr_offs, ptr_tgts, ptr_thumb = pointer_census(data)
    tables = pointer_tables(ptr_offs)
    bl = thumb_bl_targets(data)
    seeds = function_seeds(data, bl, ptr_tgts[ptr_thumb])
    vens = veneers(data)
    for stub, tgt in vens.items():
        seeds.setdefault(tgt, ("veneer", 0))

    def targets_at(start, n):
        return [(int.from_bytes(data[start + 4 * i:start + 4 * i + 4], "little") & ~1) - ROM_BASE for i in range(n)]

    masters = master_tables(tables, targets_at, len(data))
    stubs, inline = bios_calls(data)
    candidates = ptr_tgts[~ptr_thumb]
    if deep:
        candidates = np.arange(0, len(data) - 4, 4)
    blobs = compressed_blobs(data, candidates)
    return {
        "pointers": int(len(ptr_offs)),
        "pointer_targets": int(len(set(ptr_tgts.tolist()))),
        "pointer_tables": tables,
        "bl_calls": int(sum(bl.values())),
        "function_seeds": seeds,
        "veneers": vens,
        "master_tables": masters,
        "bios_stubs": stubs,
        "bios_inline": dict(inline),
        "blobs": blobs,
        "entropy": entropy_map(data),
        "free": free_runs(data),
    }
