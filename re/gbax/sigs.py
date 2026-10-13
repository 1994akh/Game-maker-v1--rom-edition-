"""Function fingerprints: build them from a decomp's ELF + map + ROM, and find them in other ROMs.

A signature is a function's bytes with the parts that change between games masked out: absolute pointers in literal
pools and the offsets of BL calls. When a signature matches, each masked pointer is read back from the target ROM and
named after what it pointed to in the reference build (e.g. m4aSongNumStart's literal -> that game's gSongTable).
"""
import bisect
import json
import re
from pathlib import Path

import numpy as np

SIGDB = Path(__file__).resolve().parent / "sigdb"

# Objects that come from Nintendo's SDK or the toolchain rather than the game itself.
SDK_OBJECTS = r"m4a|agb_flash|siirtc|libagbsyscall|libgcc\.a|libc\.a|isagbprn|librfu|libgcnmultiboot|crt0|multiboot"
POINTER_RANGES = ((0x02000000, 0x02040000), (0x03000000, 0x03008000), (0x08000000, 0x0A000000))


def _is_ptr(v):
    return any(lo <= v < hi for lo, hi in POINTER_RANGES)


def parse_map_objects(map_path):
    """[(start, size, object)] for every .text input section in a GNU ld map."""
    out = []
    pat = re.compile(r"^\s*\.text\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\S+)")
    for line in Path(map_path).read_text(errors="replace").splitlines():
        m = pat.match(line)
        if m and int(m.group(2), 16):
            out.append((int(m.group(1), 16), int(m.group(2), 16), m.group(3)))
    return sorted(out)


def build(elf_path, map_path, rom_path, out_name, objects=SDK_OBJECTS, min_size=12):
    from elftools.elf.elffile import ELFFile
    rom = Path(rom_path).read_bytes()
    objs = parse_map_objects(map_path)
    obj_starts = [o[0] for o in objs]
    with open(elf_path, "rb") as f:
        syms = [(s.name, s["st_value"], s["st_size"], s["st_info"]["type"])
                for s in ELFFile(f).get_section_by_name(".symtab").iter_symbols()
                if s.name and not s.name.startswith("$")]
    named = sorted((v & ~1, z, n) for n, v, z, t in syms if t in ("STT_FUNC", "STT_OBJECT") and v)
    named_starts = [a for a, _, _ in named]
    # Exact-address names, including size-less asm labels like gSongTable; prefer global-looking names.
    exact = {}
    for n, v, z, t in sorted(syms, key=lambda s: (s[0].startswith((".", "_")), s[2] == 0)):
        if t in ("STT_FUNC", "STT_OBJECT", "STT_NOTYPE") and v:
            exact.setdefault(v & ~1 if t == "STT_FUNC" else v, n)

    def name_of(addr):
        if addr in exact:
            return exact[addr]
        i = bisect.bisect_right(named_starts, addr) - 1
        if i >= 0 and addr < named[i][0] + max(named[i][1], 1):
            return named[i][2] if addr == named[i][0] else f"{named[i][2]}+0x{addr - named[i][0]:X}"
        return None

    sigs = []
    for name, val, size, typ in syms:
        if typ != "STT_FUNC" or size < min_size or not 0x08000000 <= val < 0x0A000000:
            continue
        addr, thumb = val & ~1, bool(val & 1)
        i = bisect.bisect_right(obj_starts, addr) - 1
        obj = objs[i][2] if i >= 0 and addr < objs[i][0] + objs[i][1] else ""
        if objects and not re.search(objects, obj):
            continue
        off = addr - 0x08000000
        body = bytearray(rom[off:off + size])
        mask = bytearray(b"\xff" * size)
        refs = {}
        for k in range((-addr) % 4, size - 3, 4):
            v = int.from_bytes(body[k:k + 4], "little")
            if _is_ptr(v):
                mask[k:k + 4] = b"\0\0\0\0"
                refs[k] = name_of(v & ~1) or f"0x{v:08X}"
        if thumb:
            k = 0
            while k < size - 3:
                h1 = int.from_bytes(body[k:k + 2], "little")
                h2 = int.from_bytes(body[k + 2:k + 4], "little")
                if (h1 & 0xF800) == 0xF000 and (h2 & 0xF800) == 0xF800 and mask[k]:
                    for j in (k, k + 2):
                        mask[j] = 0
                        mask[j + 1] &= 0xF8
                    k += 4
                else:
                    k += 2
        else:
            for k in range(0, size - 3, 4):
                if body[k + 3] & 0x0F == 0x0B and mask[k + 3]:  # ARM BL
                    mask[k:k + 3] = b"\0\0\0"
        sigs.append({"name": name, "object": obj.split("/")[-1], "size": size, "thumb": thumb,
                     "bytes": body.hex(), "mask": mask.hex(), "refs": {str(k): v for k, v in refs.items()}})
    SIGDB.mkdir(exist_ok=True)
    path = SIGDB / f"{out_name}.json"
    path.write_text(json.dumps({"source": str(elf_path), "count": len(sigs), "sigs": sigs}), encoding="utf-8")
    return path, len(sigs)


def _anchor(body, mask):
    """Longest fully-unmasked run: (offset, length)."""
    best, start = (0, 0), None
    for i, m in enumerate(list(mask) + [0]):
        if m == 0xFF:
            if start is None:
                start = i
        elif start is not None:
            if i - start > best[1]:
                best = (start, i - start)
            start = None
    return best


def match(rom_data, db_names=None, min_anchor=8):
    """Return (matches, inferred_labels). matches: [(name, object, rom_offset, size, thumb, unique)]."""
    dbs = [p for p in SIGDB.glob("*.json") if not db_names or p.stem in db_names]
    rom = np.frombuffer(rom_data, dtype=np.uint8)
    matches, inferred = [], {}
    for db in dbs:
        for s in json.loads(db.read_text(encoding="utf-8"))["sigs"]:
            body, mask = bytes.fromhex(s["bytes"]), bytes.fromhex(s["mask"])
            a_off, a_len = _anchor(body, mask)
            if a_len < min_anchor:
                continue
            anchor = body[a_off:a_off + a_len]
            b, m = np.frombuffer(body, dtype=np.uint8), np.frombuffer(mask, dtype=np.uint8)
            want = b & m
            hits, pos = [], 0
            while True:
                i = rom_data.find(anchor, pos)
                if i < 0:
                    break
                pos = i + 1
                start = i - a_off
                if start < 0 or start % 2 or start + len(body) > len(rom_data):
                    continue
                if np.array_equal(rom[start:start + len(body)] & m, want):
                    hits.append(start)
            for h in hits:
                matches.append((s["name"], s["object"], h, s["size"], s["thumb"], len(hits) == 1))
                if len(hits) == 1:
                    for k, ref in s["refs"].items():
                        v = int.from_bytes(rom_data[h + int(k):h + int(k) + 4], "little")
                        if "+" not in ref and not ref.startswith("0x") and _is_ptr(v):
                            inferred.setdefault(ref, set()).add(v & ~1 if v >= 0x08000000 else v)
    labels = {k: sorted(v)[0] for k, v in inferred.items() if len(v) == 1}
    return matches, labels
