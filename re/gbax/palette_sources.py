"""Collect graphics, palettes and pairing evidence from a ROM for gbax.palettes."""
import csv

import numpy as np

from . import palettes as P
from .rom import ROM_BASE


def read_palette_banks(data, off, max_banks=16):
    """Uncompressed palette at off: consecutive 16-colour banks while they still look like palettes."""
    banks = 0
    while banks < max_banks and P.palette_like_strict(data[off + banks * 32: off + banks * 32 + 32]):
        banks += 1
    return data[off: off + banks * 32] if banks else None


def from_pointer_rom(rom, scan_r):
    """Graphics/palettes from BIOS-compressed blobs and pointed-to uncompressed palettes, with struct/parallel evidence."""
    from .scan import pointer_census
    data = rom.data
    graphics, palettes = [], {}
    for off, kind, size, clen, dec in scan_r["blobs"]:
        addr = off + ROM_BASE
        pal_ok = size % 32 == 0 and size <= 512 and P.palette_like(dec, len(dec) // 2)
        if pal_ok:
            palettes[addr] = P.Palette(addr, P.bgr555(dec), dec, kind)
        # Anything bigger than one 16-colour palette could also be tiles (small icons often pass the palette test);
        # it's a candidate both ways and the arrays it sits in decide its role.
        if size % 32 == 0 and size >= 64:
            graphics.append(P.Graphic(addr, dec, (4,), kind))
    ptr_offs, ptr_tgts, ptr_thumb = pointer_census(data)
    gfx_addrs = {g.addr for g in graphics}
    for t in set((ptr_tgts[~ptr_thumb]).tolist()):
        addr = t + ROM_BASE
        if addr in gfx_addrs or addr in palettes or t % 2:
            continue
        raw = read_palette_banks(data, t)
        if raw:
            palettes[addr] = P.Palette(addr, P.bgr555(raw), raw, "raw")

    def target_at(o):
        v = int.from_bytes(data[o:o + 4], "little")
        return v & ~1 if ROM_BASE <= v < ROM_BASE + rom.size else None

    is_g = gfx_addrs.__contains__
    is_p = palettes.__contains__
    arrays = P.strided_arrays(ptr_offs)
    fields, parallel = P.array_pairs(arrays, target_at, is_g, is_p)
    struct = P.struct_pairs(ptr_offs, target_at, is_g, is_p)
    # Ambiguous blobs that the arrays use as palettes are palettes, not graphics.
    used_as_palette = set(P.array_pairs.palette_columns)
    for ev in (fields, parallel):
        for pals in ev.values():
            used_as_palette.update(pals)
    graphics = [g for g in graphics if not (g.addr in palettes and g.addr in used_as_palette)]
    return graphics, list(palettes.values()), {"struct": struct, "parallel": parallel, "fields": fields}


def from_file_table(rom, files_dir):
    """Graphics/palettes from an extracted master file table (custom-format games such as Golden Sun)."""
    graphics, palettes, embedded = [], {}, {}
    with open(files_dir / "index.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if r["status"] == "code":
            continue
        data = (files_dir / r["file"]).read_bytes()
        addr = int(r["address"], 16)
        n = len(data)
        is_pal = n % 32 == 0 and 32 <= n <= 2048 and all(
            P.palette_like_strict(data[i:i + 32]) for i in range(0, n, 32))
        if is_pal:
            palettes[addr] = P.Palette(addr, P.bgr555(data), data, f"file #{r['index']}")
            if n <= 32:
                continue
        if r["status"] == "compressed" and n % 32 == 0 and n >= 128:
            bpps = (4, 8) if n % 64 == 0 else (4,)
            graphics.append(P.Graphic(addr, data, bpps, f"file #{r['index']}"))
        # A palette embedded at the start of the file: 256 or 16 colours.
        for colors in (256, 16):
            if n > colors * 2 + 32 and all(P.palette_like_strict(data[i:i + 32]) for i in range(0, colors * 2, 32)):
                pa = addr + 1  # distinct key for the embedded palette
                palettes[pa] = P.Palette(pa, P.bgr555(data[:colors * 2]), data[:colors * 2],
                                         f"file #{r['index']} header")
                embedded.setdefault(addr, set()).add(pa)
                break
    return graphics, list(palettes.values()), embedded
