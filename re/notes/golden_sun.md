# Golden Sun 1 & 2: format notes

Golden Sun (AGSE, 8 MB, SHA-1 `5c469520…`) and The Lost Age (AGFE, 16 MB, SHA-1 `b5006632…`). Both are by Camelot
and share an engine. Addresses below are GS1 unless marked GS2.

## Layout

- **Master file table**: GS1 `0x08320000` (975 entries), GS2 `0x08680000` (1,723 entries). It's an array of ROM
  pointers. Entry 0 is the ROM start, entry 1 is the table itself, and entry 2 is a build timestamp string
  (GS1 `010918151347`, GS2 `030205144838`). Entries 3–18 are code modules.
- **Code modules** (GS1: 16 entries, 14 distinct; GS2: 15/14) each start with an export table of Thumb long-jump
  stubs, `ldr r4,=func; bx r4`.
- **GetFile(index)**: GS1 `0x08002F40`, which returns `table[index]`. It has 145 direct callers. In GS2 the table
  is loaded at `0x08013300`.
- **Loaders**: `0x08002F10` and `0x0800479C` DMA a file into memory or VRAM unchanged.
  `0x08002FB0(index, dest)` decompresses it.
- **Decompressor**: 708 bytes of ARM code at GS1 `0x08002544` (GS2 `0x080128AC`; same code). The game copies it to
  RAM, then calls it through `bx r6`/`bx r7` stubs at `0x080072FC`. Its arguments are r0 = file and r1 = destination;
  it returns the decoded size in r0.

## Compression (first byte of a file)

| Byte | Format | gbax |
|---|---|---|
| `0x00` | Bit-level LZ. 16-bit words are read least-significant bit first. Literals are 8 bits. Match distances use a bit width that grows with output written so far (`out - dest - 0x20`, up to 11 bits) or a 5-bit short form, plus a 12-bit form. Lengths are prefix-coded, 2–7, then extended. | emulated with the game's own routine (`gbax.emu`) |
| `0x01` | Byte LZ. A control byte gives 8 flags, most significant bit first. 0 = literal byte. 1 = `b0 b1`: distance `(b0&0xF0)<<4 \| b1`, length field `b0&0x0F`; field 0 means a third byte gives `b2+16`; field 0 with distance 0 ends the stream. Copies length+1 bytes. | native Python, identical to the game on 35/35 GS1 files |
| other | Not handled by the decompressor. | raw |

A file whose first byte is `0x00` isn't necessarily compressed, since plenty of raw data starts with a zero. gbax
counts a file as compressed only when the decompressor consumes it to within 4 bytes of its end.

| | Compressed (verified) | Raw | Code |
|---|---|---|---|
| GS1 | 560 (263 format 0, 35 format 1, 262 format 2) | 399 | 14 |
| GS2 | 1,002 (467 format 0, 65 format 1, 470 format 2) | 706 | 14 |

## Portraits (solved)

- **Archive layout**: a u16 offset table at the start of the file (first offset = table size), then entries. Each
  entry is a 16-colour palette (32 bytes) followed by compressed sprite data. GS1 file #240 (57 portraits), GS2 file
  #470 (84).
- **Loader**: GS1 `FUN_0801a4fc(index, ..., bank)` calls GetFile(240), picks the entry, decodes it, then DMAs the
  32-byte palette to OBJ palette bank `0x05000200 + bank*0x20`. It has 8 callers.
- **Sprite routine ("routine A")**: ARM, 0x278 bytes at GS1 `0x08015AFC` (GS2 `0x08038B18`, found by signature).
  It's copied to RAM slot 0x31 (`0x03001E50 + 0x31*4` holds the copy's address) and called through the
  `bx r3` trampoline at `0x080072F0`. Arguments: r0 = sprite data, r1 = output, r2 = pointer to a word holding the
  source pointer. Output: 8 bits per pixel, linear rows, 32x32 = 0x400 bytes; pixel values index the entry's
  palette (low 4 bits).
- **Routine B** (`0x08015E10`, or `0x08015D74` in mode 1) converts that 8bpp output into 4bpp tiles (4x4 tiles,
  0x200 bytes). `FUN_08003fa4(slot, size, src)` then allocates OBJ VRAM and DMAs the tiles in.
- gbax decodes every entry with routine A in the emulator and accepts it only if the entry is consumed to its end.
  Results: GS1 54 portraits, GS2 77, in `files/sprites/index.html`.

## Battle effect bitmaps (solved)

- **Layout**: a raw file that starts with a palette, then a format-0/1 compressed stream running to the end of the
  file. Battle effects use a 0x80-byte (64-colour) palette, and their decoded pixels are 8 bits each, all below 64.
  A few files use 0x20 or 0x200-byte palettes.
- **Loader** (battle module #12): `file = GetFile(N)`, then `copy(0x05000000, file, 0x80, …)` through the `bx r3`
  trampoline. The copy routine is in RAM at `0x03001388`. Then `FUN_08005340(file + 0x80, buffer)` decompresses.
  86 GetFile calls in 52 functions, in `re_battle_getfile.c` in the GS1 workspace.
- **Pixels** are linear 8bpp bitmaps, not tiles. The width isn't stored in the file; gbax guesses it (at the true
  width a pixel usually equals the one below). Most are animation strips: 32/64/128/256 px wide, or 120/240 for
  screen-sized ones.
- gbax finds them by data shape (palette + stream consumed to the end). GS1 has 111 (of 113 candidates), GS2 165,
  in the same gallery as the portraits.
- Still open: frame sizes and animation timing (in the battle module's tables); files that mix several pieces of
  different widths (GS1 #165, GS2 #240).

## Maps (found, not yet extracted)

`FUN_0800fb38(area)` (GS1, kernel) loads a map. A 12-byte record at `table + area*12` gives a u16 file number (plus
a base constant). That file is a container: header bytes 0–0x13 hold dimensions and settings, and u32 offsets at
+0x24, +0x28, +0x2C, +0x30 and +0x34 point to format-0/1 compressed parts (tilesets, tilemaps and so on), each
decompressed into its own RAM buffer. The offset at +0x38 points to more data. Other loaders read four u16 file
numbers from struct fields at +4/+6/+8/+10.

## Format 2 (solved: 4bpp tile blocks)

- 271 GS1 / 486 GS2 files start with `0x02`, usually `02 83`. They decode to 16 KB each, one GBA tile block of
  512 4bpp tiles: map and scene tilesets.
- **Decoder**: ARM, 0x4EC bytes at GS1 `0x08002808` (GS2 `0x08012B74`, found by signature), right after the format
  0/1 decompressor. It begins `ldrb r2,[r0],#1; cmp r2,#2; movne r0,#4; bxne lr`. Wrapper `FUN_08005394(src, dest)`
  copies it to RAM and calls it through the `bx r6` trampoline. Arguments: r0 = file (with its type byte),
  r1 = destination; returns the size. It takes the DMA registers in r3 and uses DMA internally, so gbax's emulator
  now emulates DMA.
- **How it was found**: static analysis and decoder discovery both failed. The decoder doesn't start with an `stmfd`
  prologue, so the ARM-routine finder skipped it, and it needs DMA. The 25-second live trace of the intro
  (`gbax trace --launch`) caught the RAM code reading files 298–301 at `0x03006004`, called from `0x080053C4`.
  That led straight to the wrapper.
- Decoded: GS1 262 of 271, GS2 470 of 486. The rest hold several streams or an unusual layout (e.g. GS1 #52).
- Still to do: which palettes and tilemaps go with each tileset; the map containers (below) should link them.
- Enemy and character sprites still aren't identified. A live trace during a battle will show which files and
  routines they use.

## Text, mechanics tables and movement (solved, 13 Oct)

Each has its own notes file and a re-runnable exporter (`python -m gbax.codecs.<module> ROM [ROM2]`), writing JSON
under `games\<slug>\text\` and `games\<slug>\data\`:

| Topic | Notes | Module | Result |
|---|---|---|---|
| Text | `gs_text.md` | `golden_sun_text` | Huffman with one tree per previous character; every string decodes (GS1 10,722, GS2 12,461), identical to the game's own routine run in the emulator; name-list ID ranges in `groups.json` |
| Psynergy, classes, Djinn, Summons | `gs_abilities_classes.md` | `gs_abilities` | Abilities 519 / 734, classes 92 / 111 used, Djinn 28 / 72, Summons 16 / 29; class selection logic from code; checked against goldensunwiki.net |
| Enemies, encounters, items, characters | `gs_units_items.md` | `gs_units` | Enemies 163 / 378 real, groups, encounter tables, items incl. the utility-Psynergy items, PC stat curves |
| Field movement | `gs_movement.md` | `tools\gs_movement\` | Free movement on 16.16 positions: walk 1.0, run 1.5 px/frame, 0.25 px/frame² acceleration, normalised diagonals, 8 px wall probe with ±22.5° slides; measured live in mGBA |
| Maps | `gs_maps.md` | `gs_maps` | Rooms → areas (palette + 4 tilesets, 3 layers, 128×128 cell grid with collision/height/events); PNG + Tiled JSON + collision/events JSON; 176/186 GS1 and 301/312 GS2 areas render cleanly. 14 Oct: actors by slot with their talk/Psynergy events (98.7% resolved), exits with arrival points (GS1 99.1%, GS2 99.5%), tile animation, blend glows, all 16 height shapes, reachable cells, parallax. Open: a full GS2 re-render with the new code |
| Field sprites | `gs_field_sprites.md` | `gs_field_sprites` | Every field sprite as a sheet + per-direction animations with 60 Hz frame durations: GS1 251 sprites (5,170 frames), GS2 511 (9,799); the animation script opcodes and facing kinds from code |
| World map | `gs_worldmap.md` | `gs_worldmap` | Both world maps as PNG + Tiled JSON with terrain classes, regions, encounter rules and entry points (GS1 4096×5120, GS2 8192×8192); walking classes 5–12, the ship sails 1–4 and 6 (and, like walking, refuses event-255 cells). Open: town icon → room, ship states from a late save |
| Battle sprites | `gs_battle_sprites.md` | `gs_battle_sprites` | Enemy → battle table → sprite table; run-length frames, one shared 224-colour palette + 5 recolour maps; 161/165 and 370/380 enemy records, party sheets and weapon overlays |
| Battle rules | `gs_battle_mechanics.md` | `gs_battle` | Damage, healing, elemental power/resist, criticals, 92 status effects, turn order, fleeing, Djinn recovery, Summons (% of max HP in both games), rewards; Python reference matches the ROM routines in 2,794 emulated checks (14 Oct: GS1 guard levels, Summon bonus, Drain, PP recovery, turn-order bonus fixed) |
| Field Psynergy | `gs_field_psynergy.md` | `gs_field` | Shared cast pipeline, 4-direction targeting, type-5 room events with phases; Move/Frost/Growth/Reveal handlers decoded; Lost Age handlers (§12) call the puzzle script every frame; puzzle logic lives in per-room scripts |
| Music | `music_export.md` | `gbax\music_export.py` + GBA Mus Ripper | MIDI (with loop markers) + one SoundFont per game: GS1 260, GS2 403, Unbound 519 songs |

## Graphics pipelines still to reverse

The callers of the core graphics functions, by code module (GS1):

| Module | OBJ VRAM uploads (`0x08003FA4`) | Decompress (`0x08005340`) | GetFile | Likely role |
|---|---|---|---|---|
| #12 `0x080C9000` | – | 38 | 86 | battle: effects solved (above); enemies and backgrounds still open |
| #4 `0x08015000` | 33 | 1 | 13 | overworld sprites, menus, icons, portraits |
| #3 `0x08009000` | 3 | 22 | 24 | maps and field data |

Method for each: take a caller, `gbax decompile` it, find which file index it passes to GetFile and what decodes
the result, then emulate that routine as with portraits.

The kernel's stub table at `0x08000100`–`0x080002FF` (`ldr r4,=func; bx r4`) has no static callers. It's probably
copied to RAM and called from there.

## Graphics

Decoded graphics include **8bpp** tilesets (256 colours). For example, GS1 file #223 renders correctly as 8bpp tiles
16 wide. Previews are written in both 4bpp and 8bpp because the bit depth isn't stored with the data.

## Sound

Nintendo's MP2K/M4A engine (69 functions fingerprinted in GS1, 62 in GS2). Song tables: GS1 `0x080FC684` (312
entries, 260 with tracks), GS2 `0x081C4530` (800 entries, 403 with tracks). Each game has two instrument sets.

## Open questions

- What the 271 / 486 files starting with `0x02` are. They're not compressed with this routine; next step is to find
  their readers through GetFile's callers.
- Palettes for everything except portraits. gbax's generic matcher (adjacency, embedded headers) produces noise for
  most Golden Sun graphics, because they're archives and custom sprite formats rather than plain tiles. Each
  pipeline above has to be reversed; portraits show the pattern.
- ~~The text encoding~~: solved, see "Text, mechanics tables and movement" above.
- Native Python port of format 0, using the emulator as the reference. It's optional, since emulation is exact.
