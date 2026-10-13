# Golden Sun 1 & 2: game text

All game text in both games (dialogue, menus, names, descriptions) is in one string bank per ROM, addressed by a
16-bit string ID. It's Huffman-coded with an order-1 context model: there's one code tree for each *previous*
character. The decoder is `gbax/codecs/golden_sun_text.py`. Every string in both games decodes to exactly what the
game's own routine produces, checked by running that routine in the emulator: GS1 10,722 of 10,722, GS2 12,461 of
12,461.

## Re-running

```
.venv\Scripts\python.exe -m gbax.codecs.golden_sun_text "games\AGSE-5c469520-Golden-Sun-USA-Europe\rom\Golden Sun (USA, Europe).gba"
.venv\Scripts\python.exe -m gbax.codecs.golden_sun_text "C:\Users\aaron\OneDrive\Apps-Roms\Golden Sun - The Lost Age (USA, Europe).gba"
```

Options:

- `--verify -1` compares every string with the emulated game routine. It takes about 15–20 s per game; `--verify N`
  checks N random strings instead.
- `--id 102 822` prints the given strings.
- `--out DIR` changes the output directory.

The command writes these files to `games/<slug>/text/`:

| File | Contents |
|---|---|
| `strings.json` | `{"id": text}`. Line breaks are real `\n` characters. |
| `strings.txt` | One `id<TAB>text` per line, with line breaks written as `{NL}`. |
| `groups.json` | The table addresses, counts and kinds (below), the control-code table, and the name/description ID ranges, each with examples. |

From Python: `decode_string(rom, id)`, `string_table(rom)`, `export_all(rom, out_dir)`, `verify_emulated(rom, ids)` and
`TextBank(data).decode_codes(id)`, which returns the raw codes. `rom` can be a gbax `Rom` or the ROM bytes.

## Engine routines and tables (VERIFIED)

Both routines are ARM code and byte-identical between the two games, apart from their literal pools. gbax finds them
by signature.

| | GS1 (AGSE) | GS2 (AGFE) |
|---|---|---|
| `text_open(state, id)` | `0x08015570` | `0x08038580` |
| `text_next(state)` → char | `0x08015430` | `0x0803843C` |
| Text table (literal at `text_open+0x5C`) | `0x080736B8`, 42 blocks | `0x080A9F54`, 49 blocks |
| Bitstreams + length tables, interleaved per block | `0x08038434`–`0x080736B7` | `0x08060C38`–`0x080A9F53` |
| Char table (literal at `text_next+0x13C`) | `0x0803842C` | `0x08060C30` |
| Tree data / tree offsets | `0x08037464` / `0x08038334` (124 contexts) | `0x0805F914` / `0x08060A4C` (242 contexts) |
| Strings | **10,722** (last block 226) | **12,461** (last block 173) |
| Text expander (control codes) | `FUN_08018040` | (same code, not separately located) |
| String copier | `FUN_080196C4` | (not located) |
| Pool of string-ID bases | `0x08018574` | `0x0803B638` |

GS1 callers: the routines are DMA'd to RAM before use. Literal pools at `0x08018184` and `0x080197AC` hold `text_next`;
the pool at `0x08019BF8` holds `text_open`, and `FUN_08019bac` is the wrapper that calls it.

### Format

- **state** = `{u32 prev_char, u32 stream_ptr, u32 bit_buffer}`. `prev_char` starts at 0.
- **Text table**: one 8-byte record `{u32 bitstream, u32 lengths}` for each block of 256 strings.
  - String `id` is in block `id >> 8`. Its bits start at `bitstream + Σ lengths[0 .. (id & 0xFF) - 1]`.
  - A length is a run of `0xFF` bytes plus a final byte; each `0xFF` adds 255 and continues.
  - Each block's lengths table starts exactly where its bitstream ends. That boundary is how the string count of the
    last block is found (it isn't stored).
- **Bits**: 32-bit little-endian words, least-significant bit first. A string can start on any byte; the first word
  is shifted right by `8*(addr&3)`. In the ARM code, a sentinel bit in `bit_buffer` marks when it's empty.
- **Char table**: `{u32 tree_data, u32 offsets}` for each 256-character page.
  - Both games have one page. The page-1 entry would overlap the first bitstream, so characters are 0–0xFF.
  - `tree = tree_data + u16 offsets[prev_char]`.
- **Tree**: a pre-order bit string read forwards from `tree`, where 0 = internal node and 1 = leaf.
  - Decoding: at each internal node, read one text bit. 0 = left child, which is the next node in the tree string.
    1 = skip the left subtree, counting its leaves, and go to the right child.
  - Leaf symbols are 12-bit values packed backwards below `tree`. Leaf `k` is at `p = tree - (k + k//2)`:
    even `k` → `b[p-1]<<4 | b[p-2]>>4`; odd `k` → `(b[p-1]&0xF)<<8 | b[p-2]`.
- Character 0 ends the string. The next string's context restarts at 0.

## Character set

- `0x20`–`0x7E` are ASCII. `{`, `}` and `\` never occur.
- `0xA1`–`0xDF` are JIS X 0201 half-width katakana. The expander special-cases `0xDE`/`0xDF` (the voicing marks) and
  `0xA1`/`0xA4`/`0xA5`.
- GS2 reuses two of those slots in English text (INFERRED from context):
  - `0xB0` is a dash, rendered `—`. It's used 36 times, e.g. "What in—!!!" and "Earth Star—requires Mythril Bag".
  - `0xAE` is `®` ("Game Boy® Advance", string 4468).
- Shift-JIS pairs appear only in GS2 debug strings 4194 and 5456–5476, and are rendered as Japanese.
- GS1 uses no characters above `0x7E`.

## Control codes

Codes `0x08`–`0x0C`, `0x0F`, `0x11`–`0x14`, `0x1A`, `0x1C` and `0x1D` take one argument character; `0x0E` takes two
(VERIFIED in `FUN_080196C4` and `FUN_08018040`). The tags are the ones gbax renders.

| Code | Tag | Meaning | Evidence |
|---|---|---|---|
| 00 | – | End of string | code |
| 01 | `{BOX}` | Ends a box: wait for a button, then continue in a new box | usage, 1,964 / 1,800 uses |
| 02 | `{END}` | Ends the message. The expander stops on it, like 00. | code + usage |
| 03 | newline | Line break (`{NL}` in strings.txt) | usage |
| 04 | `{CODE04}` | 1 use (GS2 12459, before `{BOX}`) | unknown |
| 05 | `{PAUSE}` | Short pause ("Ugh...{PAUSE} Ughnn...") | usage, INFERRED |
| 06 | `{CODE06}` | 1 use per game, ending a string in place of `{END}` | unknown |
| 07 | `{/FX}` | Back to normal after `{COLOR}` or `{FX}` | usage, INFERRED |
| 08 n | `{COLOR:n}` | Text colour. Djinn names use 4 Mars, 5 Venus, 8 Mercury, 10 Jupiter, then `{COLOR:16}` to return to normal. Error messages use 5. | usage, INFERRED |
| 09 n | `{FX:n}` | A text effect (n = 2, 4 or 6) on strained or emphasised speech ("{FX:4}Ohhh...{/FX}"). The exact effect (speed or shake) is unknown. | usage |
| 0A–0C, 0F n; 0E n m | `{CODE0x:n}` | Debug text only | arguments VERIFIED |
| 10 | `{LEADER}` | Name of the character whose index is at `0x02000240+500` (the party leader): "{LEADER}'s party has been annihilated" | code |
| 11 n | `{NAME:Isaac}` | Name of playable character n−1: 1 Isaac, 2 Garet, 3 Ivan, 4 Mia, 5 Felix, 6 Jenna, 7 Sheba, 8 Piers. Rendered with the default name. | code (`FUN_08077008(n-1)`) + usage |
| 12 n | `{UNIT:1}` | Name of the unit passed to the message (battle actor, joining character). n is always 1. | code |
| 13 n | `{CLASS:n}` | Class name from the message parameter: string = class base + class | code |
| 14 n | `{ITEM:n}` | Item name from the message parameter: string = item base + (item & 0x1FF) | code |
| 15 | `{ABILITY}` | Ability, Psynergy or Djinni name from the message parameter: string = ability base + n | code |
| 16 | `{NUM}` | Decimal number from the message parameter. Sets the plural flag when \|n\|>1. | code |
| 17 | `{PLACE}` | Area name: place base + `FUN_0808a5d0(n,1)` | code |
| 18 | `{DASH}` | GS1: expands to glyphs `0x8F 0x2D`. GS2's matching strings use glyph `0xB0` instead. | code |
| 19 | `{S}` | Plural suffix: "s", or "es" after s/S, when the last `{NUM}` was greater than 1 | code |
| 1A n | `{BTN:n}` | Two-tile icon made of glyphs `0x80+2(n-1)` and `0x81+2(n-1)`. Used as button prompts ("{BTN:3}+{BTN:1}:Arrange items"). Which button each n is: INFERRED. | code |
| 1B | `{'S}` | Possessive: "'s", or just "'" after s/S | code |
| 1C n | `{CODE1C:n}` | 1 use (GS2 10941) | unknown |
| 1D n | `{ART:n}` | Prefix on item names giving the article: 2 a, 3 an, 4 some, 5 none, 6 the. For example: an Herb, an Antidote, some Milk, Masamune, the Ruin Key. The n argument of `{ITEM:n}` and `{CLASS:n}` (1 = bare, 2 = with article) is passed to the word inserter `FUN_08017e88`. | usage, INFERRED |
| 1E | `{YESNO}` | Ends a question. The expander stops on it, like 00. | code + usage |

## String groups (IDs; index = id − first)

Four bases are VERIFIED from the expander's literal pool: class, item, ability and place. The rest are anchored on
known names and aligned by structure. For example, Adept Ring's description is "Ring: Use to restore 7 PP" and
Quake's is "Attack with a powerful quake."

| Group | GS1 | GS2 |
|---|---|---|
| Character names (index 0–7) | 102–109 (109 = "PC07") | 131–138 |
| Item descriptions | 117–385 | 146–606 |
| Item names (lead with `{ART:n}`) | 386–654 (269; base 0x182) | 607–1067 (461; base 0x25F) |
| Enemy names | 655–818 (164) | 1068–1446 (379) |
| Ability names | 819–1337 (519; base 0x333) | 1447–2180 (734; base 0x5A7) |
| Ability descriptions | 1338–1856 | 2181–2914 |
| Djinn names (abilities 300–379; 20 slots per element) | 1119–1198 (28 used) | 1747–1826 |
| Djinn descriptions | 1638–1717 | 2481–2560 |
| Summon names (abilities 380+) | 1199–1222 (6 slots per element; 16 used) | 1827–1859 (8 per element, plus Catastrophe at 412) |
| Summon descriptions | 1718–1741 | 2561–2593 |
| Class names | 1857–2059 (base 0x741; 0 = "NPC") | 2915–3159 (base 0xB63) |
| Location and area names | 2459–2767 (base 0x99B; ends in debug maps) | 3672–4094 (base 0xE58) |
| Element names (Earth, Water, Fire, Wind) | 2954–2957 | 4283–4286 |

Unused slots are `?` or `=`.

Known strings check out. In GS1: Isaac 102, Garet 103, Ivan 104, Mia 105, Felix 106, Jenna 107, Sheba 108, Move 959,
Quake 822, Cure 909, Douse 852, Frost 843, Growth 831, Reveal 963, Flint 1119, Granite 1120, Forge 1159, Fizz 1139,
Squire 1858. GS2 has the same set plus Piers at 138.

## Quality

| | Clean (plain text + known tags) | Placeholder (`?`, `=`, `???`, `-`, empty) | Unknown codes |
|---|---|---|---|
| GS1 | 9,896 (92.3%) | 825 | 1 (`{CODE06}`) |
| GS2 | 11,554 (92.7%) | 892 | 15 (debug, Japanese, `{CODE06}`) |

Of the non-placeholder strings, 99.99% (GS1) and 99.87% (GS2) are clean.

## Open questions

- What `{FX:n}` does, and the exact colours for each `{COLOR:n}`. The renderer that consumes the expander's u16 ring
  buffer at `base+0xEB0` hasn't been located yet.
- `{CODE04}` and `{CODE06}`, and the debug-only codes 0A–0F and 1C.
- The `{ART:n}` mapping is inferred from usage. The word inserter `FUN_08017e88` would confirm it.
- `{BTN:n}`: which button each n is. That needs the font glyphs `0x80`–`0x8B`.
- The exact class count: the names run to 2059 (GS1) and 3159 (GS2), and are followed by "Enemy".
