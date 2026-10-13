"""Write decompressed blobs to disk and render tile-graphics previews."""
import csv

import numpy as np
from PIL import Image


def tiles_to_image(data, bpp=4, tiles_wide=16):
    """Render GBA 8x8 tiles (4bpp or 8bpp) as a grayscale image."""
    tile_bytes = 32 if bpp == 4 else 64
    n = len(data) // tile_bytes
    if n == 0:
        return None
    rows = (n + tiles_wide - 1) // tiles_wide
    img = np.zeros((rows * 8, tiles_wide * 8), dtype=np.uint8)
    raw = np.frombuffer(data[: n * tile_bytes], dtype=np.uint8)
    if bpp == 4:
        px = np.empty(raw.size * 2, dtype=np.uint8)
        px[0::2], px[1::2] = raw & 0x0F, raw >> 4
        px = px * 17
    else:
        px = raw
    px = px.reshape(n, 8, 8)
    for t in range(n):
        r, c = divmod(t, tiles_wide)
        img[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = px[t]
    return Image.fromarray(img, mode="L")


def looks_like_palette(data):
    """16 or 256 BGR555 colours with the unused top bit clear."""
    if len(data) not in (32, 512):
        return False
    w = np.frombuffer(data, dtype="<u2")
    return bool((w & 0x8000).sum() == 0)


def extract_filetable(rom, table_csv, codec, previews=True):
    """Write every master-table entry: decoded when the game's codec verifies it's compressed, raw otherwise."""
    out_dir = rom.workspace / "files"
    (out_dir / "bin").mkdir(parents=True, exist_ok=True)
    if previews:
        (out_dir / "png").mkdir(exist_ok=True)
    dec = codec.Decoder(rom)
    rows, counts = [], {}
    with open(table_csv, encoding="utf-8") as f:
        entries = list(csv.DictReader(f))
    seen = set()
    for e in entries:
        if e["kind"] == "not a ROM pointer" or e["address"] in seen:
            continue
        seen.add(e["address"])
        addr, size = int(e["address"], 16), int(e["size"])
        if e["kind"].startswith("code module"):
            status, data = "code", None
        else:
            status, data = dec.classify(addr, size)
        if data is None:
            data = rom.data[addr - 0x08000000: addr - 0x08000000 + size]
        stem = f"{int(e['index']):04d}_{addr:08X}_{status}"
        (out_dir / "bin" / f"{stem}.bin").write_bytes(data)
        png = ""
        if previews and status == "compressed" and len(data) % 32 == 0 and len(data) >= 128:
            # Bit depth isn't stored with the data (Golden Sun uses both), so render both readings.
            made = []
            for bpp in (4, 8):
                img = tiles_to_image(data, bpp) if len(data) % (8 * bpp) == 0 else None
                if img is not None:
                    name = f"png/{stem}_{bpp}bpp.png"
                    img.save(out_dir / name)
                    made.append(name)
            png = ";".join(made)
        counts[status] = counts.get(status, 0) + 1
        rows.append((e["index"], e["address"], status, size, len(data), e["kind"], f"bin/{stem}.bin", png))
    with open(out_dir / "index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["index", "address", "status", "rom_size", "decoded_size", "first_byte_kind", "file", "preview"])
        w.writerows(rows)
    return out_dir, counts


def extract(rom, blobs, previews=True, max_previews=2000):
    out_dir = rom.workspace / "assets"
    (out_dir / "bin").mkdir(parents=True, exist_ok=True)
    if previews:
        (out_dir / "png").mkdir(exist_ok=True)
    rows, made = [], 0
    for off, kind, size, clen, data in blobs:
        stem = f"{off + 0x08000000:08X}_{kind}"
        (out_dir / "bin" / f"{stem}.bin").write_bytes(data)
        guess = "palette" if looks_like_palette(data) else "tiles?" if size % 32 == 0 else "data"
        png = ""
        if previews and guess == "tiles?" and made < max_previews:
            img = tiles_to_image(data, 4)
            if img is not None:
                png = f"png/{stem}.png"
                img.save(out_dir / png)
                made += 1
        rows.append((f"0x{off + 0x08000000:08X}", kind, size, clen, guess, f"bin/{stem}.bin", png))
    with open(out_dir / "index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["address", "compression", "size", "compressed_size", "guess", "file", "preview"])
        w.writerows(rows)
    return out_dir, len(rows), made
