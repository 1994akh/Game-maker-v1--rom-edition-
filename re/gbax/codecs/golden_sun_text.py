"""Golden Sun 1 & 2 (Camelot) game text: decoder, control codes, exporter.

Both games keep every line of text (dialogue, menus, names, descriptions) in one string bank addressed by a 16-bit
string ID. The text is Huffman-coded with one code tree per *previous* character (an order-1 context model).

Engine routines (ARM, byte-identical in both games; found here by signature):

  text_open(state, id)  GS1 0x08015570  GS2 0x08038580   literal -> TEXT TABLE  (GS1 0x080736B8, GS2 0x080A9F54)
  text_next(state)      GS1 0x08015430  GS2 0x0803843C   literal -> CHAR TABLE  (GS1 0x0803842C, GS2 0x08060C30)
  state = {u32 prev_char, u32 stream_ptr, u32 bit_buffer}; text_next returns the next character (0 = end).

TEXT TABLE: one 8-byte record per block of 256 strings: {u32 bitstream, u32 lengths}. String ``id`` lives in block
``id >> 8``; its bits start at ``bitstream + sum(lengths of the (id & 0xFF) strings before it)``. A length is a run of
0xFF bytes plus one final byte (0xFF = "add 255 and keep reading"). The string count isn't stored: block i's lengths
table starts exactly where its bitstream ends, which bounds it.

Bit reader: 32-bit little-endian words, least-significant bit first; a stream may start on any byte.

CHAR TABLE: {u32 tree_data, u32 offsets} per 256-character page (both games have one page). ``offsets`` is a u16 array
indexed by the previous character; ``tree = tree_data + offsets[prev]``. A tree is a pre-order bit string read forwards
from ``tree`` (0 = internal node, 1 = leaf). Leaf symbols are 12-bit values packed backwards below ``tree``: leaf k
(pre-order) at p = tree - (k + k // 2): even k -> (b[p-1] << 4) | (b[p-2] >> 4); odd k -> ((b[p-1] & 0xF) << 8) | b[p-2].
Walk: at an internal node read one text bit; 0 = left child (next node in the tree string), 1 = right child (skip the
left subtree). The first character's context is 0; character 0 ends the string.

Control codes (expander GS1 FUN_08018040, copier FUN_080196c4; see notes/gs_text.md). Codes that take an argument
are followed by one raw character holding it.

Usage:
    python -m gbax.codecs.golden_sun_text ROM [--out DIR] [--verify N] [--id ID ...]
"""
import argparse
import json
import random
import re
import struct
import sys
from pathlib import Path

# ARM code of text_open without its literal: lsr r3,r1,#8; ldr ip,[pc,#0x50]; add ip,ip,r3,lsl#3; ldm ip,{r2,r4};
# ands r1,r1,#0xff. Its literal (the text table) is at +0x5C.
TEXT_OPEN_SIGNATURE = bytes.fromhex("2134a0e1 50c09fe5 83c18ce0 14009ce8 ff1011e2".replace(" ", ""))
TEXT_OPEN_LITERAL = 0x5C
# ARM code of text_next: push {r5,r6}; ldm r0,{r1,r2,r3}; ldr ip,[pc,#0x12c]. Its literal (char table) is at +0x13C.
TEXT_NEXT_SIGNATURE = bytes.fromhex("60002de9 0e0090e8 2cc19fe5".replace(" ", ""))
TEXT_NEXT_LITERAL = 0x13C
ROM_BASE = 0x08000000

# --- control codes --------------------------------------------------------------------------------------------
# code -> (tag, number of argument characters). Tags without an argument render as {TAG}; with one as {TAG:n}.
CONTROL = {
    0x01: ("BOX", 0),      # end of a text box: wait for a button, then continue in a fresh box (usage)
    0x02: ("END", 0),      # end of message: stops the expander like 0x00 (code); waits for a button (usage)
    0x03: ("\n", 0),       # line break (usage); rendered as a real newline
    0x04: ("CODE04", 0),   # rare (GS2 x1, before {BOX}); meaning unknown
    0x05: ("PAUSE", 0),    # short pause between phrases ("Ugh...{PAUSE} Ughnn...")
    0x06: ("CODE06", 0),   # rare (x1 each game, ends a string in place of {END}); meaning unknown
    0x07: ("/FX", 0),      # back to normal text after {COLOR:n} / {FX:n} (usage)
    0x08: ("COLOR", 1),    # text colour; arg 4 Mars, 5 Venus, 8 Mercury, 10 Jupiter (Djinn names), 16 = default
    0x09: ("FX", 1),       # text effect (2, 4, 6) on strained/emphasised speech; exact effect unknown
    0x0A: ("CODE0A", 1),   # 0x0A-0x0C, 0x0F take one argument and 0x0E two (FUN_080196c4); only in debug text
    0x0B: ("CODE0B", 1),
    0x0C: ("CODE0C", 1),
    0x0E: ("CODE0E", 2),
    0x0F: ("CODE0F", 1),
    0x10: ("LEADER", 0),   # name of the character whose index is at 0x02000240+500 (party leader)
    0x11: ("NAME", 1),     # name of playable character (arg - 1): 1 Isaac 2 Garet 3 Ivan 4 Mia 5 Felix 6 Jenna 7 Sheba 8 Piers
    0x12: ("UNIT", 1),     # name of the unit passed to the message (battle actor / joining character); arg is always 1
    0x13: ("CLASS", 1),    # class name from the message parameter (string class_base + class)
    0x14: ("ITEM", 1),     # item name from the message parameter (string item_base + (item & 0x1FF))
    0x15: ("ABILITY", 0),  # ability/Psynergy/Djinni name from the message parameter (string ability_base + n)
    0x16: ("NUM", 0),      # decimal number from the message parameter; sets the plural flag when |n| > 1
    0x17: ("PLACE", 0),    # area name from the message parameter (string place_base + area_name_index(n))
    0x18: ("DASH", 0),     # GS1: expands to glyphs 0x8F 0x2D (GS2 uses glyph 0xB0 in the same strings)
    0x19: ("S", 0),        # plural suffix: "s" (or "es" after s/S) when the last {NUM} was > 1
    0x1A: ("BTN", 1),      # 2-glyph button icon: glyphs 0x80 + 2*(arg-1), +1
    0x1B: ("'S", 0),       # possessive: "'s", or just "'" after s/S
    0x1C: ("CODE1C", 1),   # one use in GS2
    0x1D: ("ART", 1),      # article class of an item name: 2 a, 3 an, 4 some, 5 none, 6 the (inferred)
    0x1E: ("YESNO", 0),    # ends a question; stops the expander like 0x00 (code); a yes/no choice follows (usage)
}
ARG_COUNT = {c: n for c, (_, n) in CONTROL.items()}
# Codes 0x00-0x1F not listed above never occur (0x0D, 0x1F) and are rendered as {XX}.

# Per-game string groups (IDs). index = id - first. Verified bases come from the expander's literal pool
# (GS1 0x08018574, GS2 0x0803B638): class, item, ability, place. Others are found from the data (see notes).
GROUPS = {
    "AGSE": {
        "character_names": (102, 109, "PC names by character index 0-7 (default names; 109 is a 'PC07' placeholder)"),
        "item_descriptions": (117, 385, "item descriptions, same index as item_names"),
        "item_names": (386, 654, "item names by item index (base 0x182 from the {ITEM} handler)"),
        "enemy_names": (655, 818, "enemy names by enemy index (0 = '???')"),
        "ability_names": (819, 1337, "ability names (Psynergy, Djinn, summons, enemy and weapon abilities) by ability "
                                     "index (base 0x333 from the {ABILITY} handler)"),
        "ability_descriptions": (1338, 1856, "ability descriptions, same index as ability_names"),
        "djinn_names": (1119, 1198, "abilities 300-379: 20 slots per element, Venus/Mercury/Mars/Jupiter; "
                                    "unused slots are '='"),
        "djinn_descriptions": (1638, 1717, "descriptions of abilities 300-379"),
        "summon_names": (1199, 1222, "abilities 380-403: 6 slots per element, 4 used"),
        "summon_descriptions": (1718, 1741, "descriptions of abilities 380-403"),
        "class_names": (1857, 2059, "class names by class index (base 0x741 from the {CLASS} handler; 0 = 'NPC')"),
        "location_names": (2459, 2767, "area/map names (base 0x99B from the {PLACE} handler), incl. debug maps"),
        "element_names": (2954, 2957, "element names in element order Venus, Mercury, Mars, Jupiter"),
    },
    "AGFE": {
        "character_names": (131, 138, "PC names by character index 0-7"),
        "item_descriptions": (146, 606, "item descriptions, same index as item_names"),
        "item_names": (607, 1067, "item names by item index (base 0x25F from the {ITEM} handler)"),
        "enemy_names": (1068, 1446, "enemy names by enemy index (0 = '???')"),
        "ability_names": (1447, 2180, "ability names by ability index (base 0x5A7 from the {ABILITY} handler)"),
        "ability_descriptions": (2181, 2914, "ability descriptions, same index as ability_names"),
        "djinn_names": (1747, 1826, "abilities 300-379: 20 slots per element, Venus/Mercury/Mars/Jupiter; "
                                    "18 used per element (slots 18-19 are 'Earth18'-style placeholders)"),
        "djinn_descriptions": (2481, 2560, "descriptions of abilities 300-379"),
        "summon_names": (1827, 1859, "abilities 380-412: 8 slots per element (Venus 380, Mercury 388, Mars 396, "
                                     "Jupiter 404) + Catastrophe at 412; Daedalus appears twice (402, 403)"),
        "summon_descriptions": (2561, 2593, "descriptions of abilities 380-412"),
        "class_names": (2915, 3158, "class names by class index (base 0xB63 from the {CLASS} handler; 0 = 'NPC'; "
                                    "244 classes, 3159 is a '?' slot)"),
        "location_names": (3672, 4094, "area/map names (base 0xE58 from the {PLACE} handler), incl. debug maps"),
        "element_names": (4283, 4286, "element names in element order Venus, Mercury, Mars, Jupiter"),
    },
}


class TextBank:
    """Decoder for one ROM's text bank."""

    def __init__(self, data, code=None):
        self.data = data if isinstance(data, (bytes, bytearray)) else data.data
        d = self.data
        self.code = code or d[0xAC:0xB0].decode("ascii", "replace")
        self.text_open = d.find(TEXT_OPEN_SIGNATURE)
        self.text_next = d.find(TEXT_NEXT_SIGNATURE)
        if self.text_open < 0 or self.text_next < 0:
            raise ValueError("Golden Sun text routines not found in this ROM")
        self.text_table = self._u32(self.text_open + TEXT_OPEN_LITERAL) - ROM_BASE
        self.char_table = self._u32(self.text_next + TEXT_NEXT_LITERAL) - ROM_BASE
        self.tree_data = self._u32(self.char_table) - ROM_BASE
        self.tree_offsets = self._u32(self.char_table + 4) - ROM_BASE
        self._trees = {}
        self.blocks = self._read_blocks()
        self.count = sum(len(b[2]) for b in self.blocks)
        self.groups = GROUPS.get(self.code, {})
        self._pc_names = None

    def _u32(self, off):
        return struct.unpack_from("<I", self.data, off)[0]

    def _read_blocks(self):
        """[(bitstream_off, lengths_off, [string start offsets])] for every block."""
        d = self.data
        blocks = []
        i = 0
        while True:
            rec = self.text_table + 8 * i
            bits, lens = self._u32(rec), self._u32(rec + 4)
            if not (ROM_BASE <= bits < ROM_BASE + len(d) and ROM_BASE <= lens < ROM_BASE + len(d)):
                break
            bits -= ROM_BASE
            lens -= ROM_BASE
            if blocks and bits <= blocks[-1][0]:
                break
            starts, pos, p = [], bits, lens
            while pos < lens and len(starts) < 256:
                starts.append(pos)
                n = 0
                while True:
                    b = d[p]
                    p += 1
                    n += b
                    if b != 0xFF:
                        break
                pos += n
            blocks.append((bits, lens, starts))
            i += 1
            if len(starts) < 256:
                break
        return blocks

    def _tree(self, prev):
        """Nested tree for context ``prev``: node = symbol (int) or (left, right). Cached."""
        t = self._trees.get(prev)
        if t is not None:
            return t
        d = self.data
        if prev >> 8:
            raise ValueError(f"character page {prev >> 8} not present")
        tree = self.tree_data + struct.unpack_from("<H", d, self.tree_offsets + 2 * prev)[0]
        state = {"bit": 0, "leaf": 0}

        def sym(k):
            p = tree - (k + (k >> 1))
            if k & 1:
                return ((d[p - 1] & 0xF) << 8) | d[p - 2]
            return (d[p - 1] << 4) | (d[p - 2] >> 4)

        def build(depth=0):
            if depth > 64:
                raise ValueError("tree too deep")
            k = state["bit"]
            state["bit"] += 1
            if (d[tree + (k >> 3)] >> (k & 7)) & 1:
                state["leaf"] += 1
                return sym(state["leaf"] - 1)
            return (build(depth + 1), build(depth + 1))

        t = self._trees[prev] = build()
        return t

    def string_offset(self, sid):
        blk, idx = sid >> 8, sid & 0xFF
        if blk >= len(self.blocks) or idx >= len(self.blocks[blk][2]):
            raise IndexError(f"string id {sid} out of range (count {self.count})")
        return self.blocks[blk][2][idx]

    def decode_codes(self, sid, limit=4000):
        """Raw character codes of string ``sid`` (without the terminating 0)."""
        d = self.data
        pos = self.string_offset(sid)
        base, k = pos & ~3, (pos & 3) * 8
        out, prev = [], 0
        while len(out) < limit:
            node = self._tree(prev)
            while isinstance(node, tuple):
                node = node[(d[base + (k >> 3)] >> (k & 7)) & 1]
                k += 1
            if node == 0:
                return out
            out.append(node)
            prev = node
        raise ValueError(f"string {sid}: no terminator within {limit} chars")

    # -- rendering ------------------------------------------------------------------------------------------
    def pc_name(self, index):
        if self._pc_names is None:
            g = self.groups.get("character_names")
            self._pc_names = [render(self.decode_codes(i)) for i in range(g[0], g[1] + 1)] if g else []
        return self._pc_names[index] if 0 <= index < len(self._pc_names) else None

    def decode(self, sid):
        return render(self.decode_codes(sid), self.pc_name)


# Glyphs the English font reuses inside the half-width katakana range (from context, GS2 only):
# 0xAE in "Game Boy(R) Advance" (string 4468), 0xB0 where the text needs a dash ("What in-!!!", "Earth Star-requires").
LATIN_OVERRIDES = {0xAE: "®", 0xB0: "—"}


def render(codes, pc_name=None):
    """Turn character codes into text with readable tags.

    Printable ASCII is kept ('{' / '}' / '\\' never occur in either game). 0x03 becomes a newline. 0xA1-0xDF are
    JIS X 0201 half-width katakana (the expander special-cases 0xDE/0xDF, the voicing marks, and 0xA1/0xA4/0xA5) except
    the LATIN_OVERRIDES. Shift-JIS pairs (only in GS2 debug strings 4194 and 5456-5476) are decoded. Anything else is
    {XX} in hex.
    """
    out = []
    i, n = 0, len(codes)
    while i < n:
        c = codes[i]
        i += 1
        if c in CONTROL:
            tag, nargs = CONTROL[c]
            args = codes[i:i + nargs]
            i += nargs
            if tag == "\n":
                out.append("\n")
            elif not nargs:
                out.append("{%s}" % tag)
            elif tag == "NAME" and pc_name and args and pc_name(args[0] - 1):
                out.append("{NAME:%s}" % pc_name(args[0] - 1))
            else:
                out.append("{%s:%s}" % (tag, ",".join(str(a) for a in args)))
        elif 0x20 <= c < 0x7F and c not in (0x5C, 0x7B, 0x7D):
            out.append(chr(c))
        elif c in LATIN_OVERRIDES:
            out.append(LATIN_OVERRIDES[c])
        elif (0x81 <= c <= 0x9F or 0xE0 <= c <= 0xEF) and i < n and 0x40 <= codes[i] <= 0xFC and codes[i] != 0x7F:
            try:
                out.append(bytes([c, codes[i]]).decode("cp932"))
                i += 1
            except UnicodeDecodeError:
                out.append("{%02X}" % c)
        elif 0xA1 <= c <= 0xDF:
            out.append(bytes([c]).decode("cp932"))
        else:
            out.append("{%02X}" % c)
    return "".join(out)


UNKNOWN_TAG = re.compile(r"\{(?:[0-9A-F]{2}|CODE[0-9A-F]{2}(?::[\d,]+)?)\}")
PLACEHOLDERS = {"", "?", "=", "???", "-"}


def classify(text):
    """'clean' (plain text + known tags), 'placeholder' (?, =, ...) or 'unknown' (raw/unknown codes)."""
    if text.strip() in PLACEHOLDERS:
        return "placeholder"
    if UNKNOWN_TAG.search(text) or any("　" <= ch <= "￯" for ch in text):
        return "unknown"
    return "clean"


# --- module API ---------------------------------------------------------------------------------------------
_BANKS = {}


def _bank(rom):
    data = rom if isinstance(rom, (bytes, bytearray)) else rom.data
    b = _BANKS.get(id(data))
    if b is None:
        b = _BANKS[id(data)] = TextBank(data)
    return b


def decode_string(rom, string_id):
    """Text of ``string_id`` (``rom`` = gbax Rom or ROM bytes) with control codes rendered as tags."""
    return _bank(rom).decode(string_id)


def string_table(rom):
    bank = _bank(rom)
    return [bank.decode(i) for i in range(bank.count)]


def verify_emulated(rom, ids):
    """Run the game's own text_open/text_next (ARM, in the emulator) on ``ids``; return the IDs that differ."""
    from ..emu import Gba
    bank = _bank(rom)
    gba = Gba(rom)
    state = 0x02000000
    bad = []
    for sid in ids:
        gba.call(ROM_BASE + bank.text_open, (state, sid), thumb=False)
        got = []
        while len(got) < 4000:
            c = gba.call(ROM_BASE + bank.text_next, (state,), thumb=False)
            if c == 0:
                break
            got.append(c)
        if got != bank.decode_codes(sid):
            bad.append(sid)
    return bad


def export_all(rom, out_dir):
    """Write strings.json, strings.txt and groups.json to out_dir; return a summary dict."""
    bank = _bank(rom)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    strings = [bank.decode(i) for i in range(bank.count)]
    (out_dir / "strings.json").write_text(
        json.dumps({str(i): s for i, s in enumerate(strings)}, indent=1, ensure_ascii=False), encoding="utf-8")
    with open(out_dir / "strings.txt", "w", encoding="utf-8", newline="\n") as f:
        for i, s in enumerate(strings):
            f.write(f"{i}\t{s.replace(chr(10), '{NL}')}\n")
    kinds = {}
    for s in strings:
        k = classify(s)
        kinds[k] = kinds.get(k, 0) + 1
    groups = {}
    for name, (first, last, note) in bank.groups.items():
        rows = [(i, strings[i]) for i in range(first, last + 1)]
        real = [(i, s) for i, s in rows if classify(s) != "placeholder"]
        groups[name] = {
            "first_id": first, "last_id": last, "count": last - first + 1, "non_placeholder": len(real),
            "index": "id - first_id", "note": note,
            "examples": {str(i): s for i, s in real[:6]},
        }
    summary = {
        "game": bank.code,
        "text_open": f"0x{ROM_BASE + bank.text_open:08X}", "text_next": f"0x{ROM_BASE + bank.text_next:08X}",
        "text_table": f"0x{ROM_BASE + bank.text_table:08X}", "blocks": len(bank.blocks),
        "char_table": f"0x{ROM_BASE + bank.char_table:08X}",
        "tree_data": f"0x{ROM_BASE + bank.tree_data:08X}", "tree_offsets": f"0x{ROM_BASE + bank.tree_offsets:08X}",
        "strings": bank.count, "kinds": kinds,
        "control_codes": {f"0x{c:02X}": {"tag": t if t != "\n" else "newline", "args": a}
                          for c, (t, a) in CONTROL.items()},
    }
    (out_dir / "groups.json").write_text(json.dumps({"summary": summary, "groups": groups}, indent=1,
                                                    ensure_ascii=False), encoding="utf-8")
    return summary


def main(argv=None):
    from ..rom import Rom
    ap = argparse.ArgumentParser(description="Decode and export Golden Sun 1/2 text.")
    ap.add_argument("rom")
    ap.add_argument("--out", help="output directory (default: games/<slug>/text)")
    ap.add_argument("--id", type=lambda s: int(s, 0), nargs="*", help="print these string IDs instead of exporting")
    ap.add_argument("--verify", type=int, default=0, metavar="N",
                    help="also check N random strings (0 = none, -1 = all) against the game's own routine (emulated)")
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(errors="backslashreplace")
    except (AttributeError, ValueError):
        pass
    rom = Rom.load(a.rom)
    bank = _bank(rom)
    if a.id:
        for sid in a.id:
            print(f"{sid}\t{bank.decode(sid)!r}")
        return
    out = Path(a.out) if a.out else rom.workspace / "text"
    s = export_all(rom, out)
    print(f"{s['game']}: text_open {s['text_open']}, text_next {s['text_next']}, text table {s['text_table']} "
          f"({s['blocks']} blocks), char table {s['char_table']}")
    print(f"{s['strings']} strings: {s['kinds']} -> {out}")
    if a.verify:
        ids = list(range(bank.count))
        if a.verify > 0:
            ids = sorted(random.Random(1).sample(ids, min(a.verify, len(ids))))
        bad = verify_emulated(rom, ids)
        print(f"emulated check: {len(ids) - len(bad)}/{len(ids)} strings identical to the game's decoder"
              + (f"; mismatches {bad[:20]}" if bad else ""))


if __name__ == "__main__":
    main()
