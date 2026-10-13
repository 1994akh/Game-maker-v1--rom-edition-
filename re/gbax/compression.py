"""GBA BIOS compression formats (LZ77, Huffman, RLE, Diff filter): decoding and candidate validation.

Header word: low byte = type (0x10 LZ77, 0x24/0x28 Huffman 4/8-bit, 0x30 RLE, 0x81/0x82 Diff 8/16-bit),
upper 24 bits = decompressed size.
"""


class DecodeError(Exception):
    pass


def lz77(src, off, limit=1 << 22):
    """Return (decoded bytes, compressed length)."""
    hdr = int.from_bytes(src[off:off + 4], "little")
    if hdr & 0xFF != 0x10:
        raise DecodeError("not LZ77")
    size = hdr >> 8
    if not 0 < size <= limit:
        raise DecodeError("bad size")
    out = bytearray()
    p = off + 4
    n = len(src)
    while len(out) < size:
        if p >= n:
            raise DecodeError("truncated")
        flags = src[p]
        p += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                if p + 1 >= n:
                    raise DecodeError("truncated")
                b1, b2 = src[p], src[p + 1]
                p += 2
                length = (b1 >> 4) + 3
                disp = ((b1 & 0xF) << 8 | b2) + 1
                if disp > len(out):
                    raise DecodeError("displacement before start")
                for _ in range(length):
                    out.append(out[-disp])
            else:
                if p >= n:
                    raise DecodeError("truncated")
                out.append(src[p])
                p += 1
    return bytes(out[:size]), p - off


def rle(src, off, limit=1 << 22):
    hdr = int.from_bytes(src[off:off + 4], "little")
    if hdr & 0xFF != 0x30:
        raise DecodeError("not RLE")
    size = hdr >> 8
    if not 0 < size <= limit:
        raise DecodeError("bad size")
    out = bytearray()
    p = off + 4
    while len(out) < size:
        if p >= len(src):
            raise DecodeError("truncated")
        flag = src[p]
        p += 1
        if flag & 0x80:
            out += bytes([src[p]]) * ((flag & 0x7F) + 3)
            p += 1
        else:
            n = (flag & 0x7F) + 1
            out += src[p:p + n]
            p += n
    return bytes(out[:size]), p - off


def huffman(src, off, limit=1 << 22):
    hdr = int.from_bytes(src[off:off + 4], "little")
    bits = hdr & 0x0F
    if hdr & 0xF0 != 0x20 or bits not in (4, 8):
        raise DecodeError("not Huffman")
    size = hdr >> 8
    if not 0 < size <= limit:
        raise DecodeError("bad size")
    tree = off + 4
    tree_size = (src[tree] + 1) * 2
    root = tree + 1
    p = tree + tree_size
    out = bytearray()
    acc, nacc = 0, 0
    while len(out) < size:
        if p + 4 > len(src):
            raise DecodeError("truncated")
        word = int.from_bytes(src[p:p + 4], "little")
        p += 4
        node = root
        for i in range(32):
            b = (word >> (31 - i)) & 1
            nd = src[node]
            child = (node & ~1) + (nd & 0x3F) * 2 + 2 + b
            leaf = nd & (0x80 >> b)  # bit 7: child 0 is a leaf; bit 6: child 1 is a leaf
            if child >= tree + tree_size:
                raise DecodeError("tree overflow")
            if leaf:
                acc |= src[child] << nacc
                nacc += bits
                if nacc == 8:
                    out.append(acc & 0xFF)
                    acc, nacc = 0, 0
                    if len(out) >= size:
                        break
                node = root
            else:
                node = child
    return bytes(out[:size]), p - off


DECODERS = {0x10: ("lz77", lz77), 0x30: ("rle", rle), 0x24: ("huff4", huffman), 0x28: ("huff8", huffman)}


def huffman_tree_ok(src, off):
    """Walk the whole tree: every child must stay inside it, and 4-bit leaves must be < 16."""
    hdr = src[off]
    tree = off + 4
    end = tree + (src[tree] + 1) * 2
    if end > len(src):
        return False
    stack, seen = [tree + 1], set()
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        nd = src[node]
        base = (node & ~1) + (nd & 0x3F) * 2 + 2
        for b in (0, 1):
            child = base + b
            if child >= end:
                return False
            if nd & (0x80 >> b):
                if (hdr & 0x0F) == 4 and src[child] > 15:
                    return False
            else:
                stack.append(child)
    return True


def try_decode(src, off, min_size=32, max_size=0x40000):
    """Decode a candidate at off. Returns (kind, data, compressed_len) or None.

    Real assets are decompressed into RAM or VRAM, so they fit in 256 KB (EWRAM) and have a 2/4-aligned size.
    """
    if off + 4 > len(src):
        return None
    t = src[off]
    if t not in DECODERS:
        return None
    size = int.from_bytes(src[off + 1:off + 4], "little")
    if not min_size <= size <= max_size or size % (2 if t == 0x10 else 4):
        return None
    if t in (0x24, 0x28) and not huffman_tree_ok(src, off):
        return None
    kind, fn = DECODERS[t]
    try:
        data, clen = fn(src, off, max_size)
    except (DecodeError, IndexError):
        return None
    # A real compressed blob shrinks its data (RLE/LZ) and doesn't run absurdly long.
    if clen > size + size // 8 + 16:
        return None
    return kind, data, clen
