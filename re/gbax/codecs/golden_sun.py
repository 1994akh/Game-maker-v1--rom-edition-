"""Golden Sun 1 & 2 (Camelot) file compression.

The game's loader (GS1: FUN_08002fb0) takes a file from the master table and runs an ARM decompressor that it first
copies into RAM (GS1: 708 bytes at ROM 0x08002544). The first byte of the file selects the format:

  0x00  bit-level LZ: 16-bit little-endian words read LSB-first; literals are 8-bit; match distances use a bit width
        that grows with the amount already written; lengths are prefix-coded. Decoded here by emulating the game's
        own routine (gbax.emu), so it's exact by construction.
  0x01  byte-level LZ: a control byte gives 8 flags, most significant bit first. 0 = copy one literal byte.
        1 = back-reference: bytes b0,b1 give distance (b0 & 0xF0) << 4 | b1 and length field n = b0 & 0x0F;
        if n == 0, a third byte gives n = b2 + 16, and n == 0 with distance 0 ends the stream. Copies n + 1 bytes.

Any other first byte is not handled by this routine (the game returns without writing).
"""
import math

import numpy as np

from ..emu import EWRAM, Gba

# First bytes of the decompressor (ARM). Used to find it in either game.
DECOMPRESSOR_SIGNATURE = bytes.fromhex("e0422de9 0120d0e4 000052e3 8c00001a 011041e2 219081e2".replace(" ", ""))
# First bytes of the format-2 decoder (ARM; GS1 0x08002808, right after the format 0/1 decompressor). It starts by
# checking the format byte: ldrb r2,[r0],#1; cmp r2,#2; movne r0,#4; bxne lr. Found by live tracing in mGBA: the
# game copies it to RAM (FUN_08005394) and it reads the file from there.
FORMAT2_SIGNATURE = bytes.fromhex("0120d0e4 020052e3 0400a013 1eff2f11".replace(" ", ""))
# First bytes of the sprite routine (ARM; GS1 0x08015AFC). The game copies it to RAM and calls it with
# r0 = sprite data, r1 = output buffer, r2 = pointer to a word holding the source pointer. Output: 8 bits per pixel,
# linear rows (a 32x32 portrait is 0x400 bytes).
SPRITE_SIGNATURE = bytes.fromhex("60002de9 28508fe2 0c0095e8 0f50a0e3".replace(" ", ""))
DEST = EWRAM
SPRITE_OUT = EWRAM + 0x10000     # 64 KB output window
SPRITE_SRC_SLOT = EWRAM + 0x100  # the word r2 points at
SPRITE_INPUT = EWRAM + 0x20000   # where non-ROM (decoded) files are placed for the routine to read


def find_decompressor(rom):
    i = rom.data.find(DECOMPRESSOR_SIGNATURE)
    if i < 0 or i % 4:
        raise LookupError("Golden Sun decompressor not found in this ROM")
    return i + 0x08000000


def decode_format1(data, off, limit=0x40000):
    """Native decoder for format 0x01. off points at the format byte. Returns (output, bytes consumed)."""
    if data[off] != 1:
        raise ValueError("not format 1")
    p, out = off + 1, bytearray()
    while True:
        flags = data[p]
        p += 1
        for bit in range(7, -1, -1):
            if not flags >> bit & 1:
                out.append(data[p])
                p += 1
                continue
            b0, b1 = data[p], data[p + 1]
            p += 2
            dist = (b0 & 0xF0) << 4 | b1
            n = b0 & 0x0F
            if n == 0:
                if dist == 0:
                    return bytes(out), p - off
                n = data[p] + 16
                p += 1
            if dist > len(out):
                raise ValueError("distance before start of output")
            for _ in range(n + 1):
                out.append(out[-dist])
            if len(out) > limit:
                raise ValueError("output too large")


def archive_offsets(data):
    """Offsets of an archive file: a u16 offset table at the start (first offset = table size), entries ascending and
    inside the file, zero for empty slots. None if the data doesn't have that shape."""
    if len(data) < 8:
        return None
    first = int.from_bytes(data[0:2], "little")
    if first < 4 or first % 2 or first >= len(data):
        return None
    offs = [int.from_bytes(data[i:i + 2], "little") for i in range(0, first, 2)]
    nz = [o for o in offs if o]
    if len(nz) < 2 or nz[0] != first or any(b <= a for a, b in zip(nz, nz[1:])) or nz[-1] >= len(data):
        return None
    return offs


def square_width(n):
    w = int(math.isqrt(n))
    return w if w * w == n and w % 8 == 0 else 32


class Decoder:
    """Decode Golden Sun files, using the game's own decompressor where no native decoder exists."""

    def __init__(self, rom):
        self.rom = rom
        self.routine = find_decompressor(rom)
        i = rom.data.find(SPRITE_SIGNATURE)
        self.sprite_routine = i + 0x08000000 if i >= 0 and i % 4 == 0 else None
        i = rom.data.find(FORMAT2_SIGNATURE)
        self.format2_routine = i + 0x08000000 if i >= 0 and i % 4 == 0 else None
        self.gba = Gba(rom)

    def decode_format2(self, addr, file_size):
        """Decode a format-2 file with the game's own routine. Some files hold several streams back to back; each
        is decoded in turn. Returns (output, bytes consumed)."""
        out, pos = bytearray(), addr
        while pos < addr + file_size - 4 and self.rom.data[pos - 0x08000000] == 2:
            self.gba.write(DEST, b"\0" * 0x40000)
            n, consumed = self.gba.call_tracking_reads(self.format2_routine, (pos, DEST), pos, 0x40000,
                                                      thumb=False, max_instructions=20_000_000)
            if not 0 < n <= 0x40000 or consumed <= 1:
                break
            out += self.gba.read(DEST, n)
            pos += consumed
            pos += (-(pos - addr)) % 4 if self.rom.data[pos - 0x08000000] != 2 else 0  # streams are word-aligned
        return bytes(out), pos - addr

    def decode_sprite(self, src_addr, max_out=0x10000):
        """Run the game's sprite routine on data at src_addr. Returns (8bpp pixels, bytes consumed)."""
        g = self.gba
        g.write(SPRITE_OUT, b"\0" * max_out)
        g.write(SPRITE_SRC_SLOT, src_addr.to_bytes(4, "little"))
        _, consumed, written = g.call_tracking(self.sprite_routine, (src_addr, SPRITE_OUT, SPRITE_SRC_SLOT, 0),
                                               (src_addr, 0x10000), (SPRITE_OUT, max_out),
                                               thumb=False, max_instructions=5_000_000)
        return g.read(SPRITE_OUT, written), consumed

    def archive_sprites(self, file_addr, data, in_rom):
        """Decode every entry of a palette+sprite archive. Yields (entry index, palette bytes or None, pixels, width).
        An entry counts only if the routine consumes it to within 8 bytes of its end."""
        offs = archive_offsets(data)
        if not offs or self.sprite_routine is None:
            return
        base = file_addr if in_rom else SPRITE_INPUT
        if not in_rom:
            self.gba.write(SPRITE_INPUT, data)
        ends = sorted(set(o for o in offs if o)) + [len(data)]
        for i, o in enumerate(offs):
            if not o:
                continue
            end = ends[ends.index(o) + 1]
            from ..palettes import palette_like_strict
            pal = data[o:o + 32] if palette_like_strict(data[o:o + 32]) else None
            start = o + (32 if pal else 0)
            try:
                px, consumed = self.decode_sprite(base + start)
            except RuntimeError:
                continue
            if not px or abs((end - start) - consumed) > 8:
                continue
            yield i, pal, px, square_width(len(px))

    def palette_bitmaps(self, files_dir):
        """Raw files that are a palette (0x20/0x40/0x80/0x100/0x200 bytes) followed by a compressed stream consumed to
        the file's end; battle effect animations use 0x80 (64 colours) and 8bpp pixels below 64.
        Yields (file index, palette bytes, decoded pixels)."""
        import csv
        from ..palettes import palette_like
        with open(files_dir / "index.csv", encoding="utf-8") as f:
            rows = [x for x in csv.DictReader(f) if x["status"] == "raw"]
        for x in rows:
            a, n = int(x["address"], 16), int(x["rom_size"])
            data = self.rom.data[a - 0x08000000: a - 0x08000000 + n]
            for psize in (0x20, 0x40, 0x80, 0x100, 0x200):
                if n <= psize + 8 or data[psize] not in (0, 1) or not palette_like(data, psize // 2):
                    continue
                status, out = self.classify(a + psize, n - psize)
                if status == "compressed":
                    yield int(x["index"]), data[:psize], out
                    break

    def extract_sprites(self, files_dir):
        """Decode every palette+sprite archive among the extracted files to files/sprites/*.png with a gallery.
        Returns the number of sprites written."""
        import csv
        from PIL import Image
        from ..palettes import GALLERY_CSS, bgr555, fit_score
        out = files_dir / "sprites"
        out.mkdir(exist_ok=True)
        for old in out.glob("*.png"):
            old.unlink()
        with open(files_dir / "index.csv", encoding="utf-8") as f:
            rows = [x for x in csv.DictReader(f) if x["status"] != "code"]
        cards = []
        for x in rows:
            data = (files_dir / x["file"]).read_bytes()
            if not archive_offsets(data):
                continue
            for i, pal, px, w in self.archive_sprites(int(x["address"], 16), data, x["status"] == "raw"):
                h = len(px) // w
                idx = np.frombuffer(px[:w * h], np.uint8).reshape(h, w) & 15
                colors = bgr555(pal) if pal else np.repeat(np.arange(0, 256, 17, dtype=np.uint8)[:, None], 3, 1)
                if fit_score(idx, colors) > 0.5:  # noise: not really a sprite
                    continue
                name = f"{int(x['index']):04d}_{i:03d}.png"
                Image.fromarray(colors[idx], "RGB").save(out / name)
                cards.append(f'<figure><img loading="lazy" src="{name}" alt=""><figcaption>file #{x["index"]} '
                             f'entry {i}, {w}x{h}{"" if pal else ", no palette"}</figcaption></figure>')
        n_portraits = len(cards)
        from ..palettes import guess_bitmap_width
        bitmaps = []
        for fidx, pal, px in self.palette_bitmaps(files_dir):
            colors = bgr555(pal)
            colors = np.concatenate([colors, np.zeros((256 - len(colors), 3), np.uint8)])
            arr = np.frombuffer(px, np.uint8)
            if arr.max() >= len(pal) // 2:  # pixels beyond the palette: not this kind of bitmap
                continue
            w = guess_bitmap_width(arr)
            h = len(arr) // w
            name = f"{fidx:04d}_bitmap.png"
            Image.fromarray(colors[arr[:w * h].reshape(h, w)], "RGB").save(out / name)
            bitmaps.append(f'<figure><img loading="lazy" src="{name}" alt=""><figcaption>file #{fidx}, {w}x{h}, '
                           f'{len(pal) // 2} colours</figcaption></figure>')
        (out / "index.html").write_text(
            f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{self.rom.title} graphics</title><style>{GALLERY_CSS}</style><h1>{self.rom.title} graphics</h1>"
            f"<p>Decoded with the game's own routines. Portraits: {n_portraits}. Palette + bitmap files (battle "
            f"effects and similar): {len(bitmaps)}.</p><h1>Portraits</h1><div class=grid>" + "\n".join(cards)
            + "</div><h1>Battle effects and other bitmaps</h1><div class=grid>" + "\n".join(bitmaps) + "</div>",
            encoding="utf-8")
        return n_portraits + len(bitmaps), out

    def emulate(self, addr, with_consumed=False):
        self.gba.write(DEST, b"\0" * 0x40000)
        n, consumed = self.gba.call_tracking_reads(self.routine, (addr, DEST), addr, 0x40000, thumb=False)
        if not 0 < n <= 0x40000:
            raise ValueError(f"decompressor returned size {n}")
        out = self.gba.read(DEST, n)
        return (out, consumed) if with_consumed else out

    def classify(self, addr, file_size):
        """Return (status, decoded bytes or None). status: 'compressed' when the stream ends within 4 bytes of the
        file's end (real compressed data), 'raw' when decoding fails or stops well short of the end."""
        fmt = self.rom.data[addr - 0x08000000]
        try:
            if fmt == 1:
                out, consumed = decode_format1(self.rom.data, addr - 0x08000000)
            elif fmt == 0:
                out, consumed = self.emulate(addr, with_consumed=True)
            elif fmt == 2 and self.format2_routine:
                out, consumed = self.decode_format2(addr, file_size)
            else:
                return "raw", None
        except (ValueError, RuntimeError, IndexError):
            return "raw", None
        return ("compressed", out) if file_size - 4 <= consumed <= file_size else ("raw", None)

    def decode(self, addr):
        fmt = self.rom.data[addr - 0x08000000]
        if fmt == 1:
            return decode_format1(self.rom.data, addr - 0x08000000)[0]
        if fmt == 0:
            return self.emulate(addr)
        raise ValueError(f"format 0x{fmt:02X} isn't compressed with this routine")
