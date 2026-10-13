# GBA extraction procedure

How to take any GBA game apart for reuse in a combined game. Steps 1–4 are automated by **gbax**
(`python -m gbax ...`, run with `.venv\Scripts\python.exe`). Each ROM gets its own workspace folder,
`games\<CODE>-<sha1>-<name>\`, so results from different games sit side by side. Original ROMs are only ever read.

```
 ROM ──► 1 identify ──► 2 scan ──► 3 fingerprint ──► 4 Ghidra ──► 5 decomp check ─┬─► 6a symbol diff (hack of a decomp)
                                                                                └─► 6b format work (no decomp)
                                                                                         │
                                         7 extract to common formats ◄───────────────────┘
                                                      │
                                         8 catalog ──► 9 port into the host engine
```

## 1. Identify — `gbax identify ROM`

Output: `identify.json`, and `songs.csv` when the game uses Nintendo's sound engine.

- Header: title, game code, version, and whether the header checksum is valid. Also the SHA-1, matched against known
  ROMs.
- Save type, from the SDK's save-library ID string (`FLASH1M_V103`, `FLASH_V123`, `EEPROM_V124`, ...).
- BIOS functions the game wraps in stubs. These tell you which built-in decompressors it uses: no `LZ77UnComp*`
  stub usually means custom compression.
- Sound engine: whether Nintendo's MP2K/M4A ("Sappy") engine is present, found by function fingerprints, plus the
  song table and the number of songs and instrument sets.

## 2. Scan — `gbax scan ROM [--deep]`

Output: `scan.json`, `blobs.csv`, `pointer_tables.csv`, `regions.csv`, `function_seeds.json`, `filetable_*.csv`.

- Every pointer in the ROM, and runs of pointers (tables).
- **Master file table**: a pointer table that spans most of the ROM and lists itself. Camelot games have one, and
  it's the game's own index of every asset and code module. gbax exports it with each entry's size, a guess at its
  kind, and its first bytes.
- BIOS-format compressed blobs (LZ77, RLE, Huffman) that something points to. Each one is test-decoded and checked
  against RAM size and alignment. `--deep` tries every aligned offset instead of only pointed-to ones.
- Code entry points: Thumb `BL` call targets, Thumb function pointers, and long-jump stubs
  (`ldr rX,=func; bx rX`), which are used both for module exports and for patch hooks.
- Entropy per 64 KB block, and runs of free space.

## 3. Fingerprint — `gbax sigs ROM`

Output: `sig_matches.csv`, `sig_inferred_labels.json`.

Finds known library functions by their bytes, with pointers and call offsets masked out. When a function matches,
the pointers inside it name that game's data. For example, `m4aSongNumStart` leads to the song table.

- Signature databases are in `gbax\sigdb\`. `pokefirered_sdk` (427 functions) is built from the FireRed decomp.
- Add one from any other decomp: `gbax sigs-build game.elf game.map game.gba <name>`. Add `--all` to include game
  code as well as library code; that's useful against hacks of the same game.

## 4. Ghidra project — `gbax ghidra ROM [--analyze] [--rebuild]`

Output: `games\...\ghidra\<slug>.gpr`. Open it with `apps\ghidra_*\ghidraRun.bat`.

- Sets up the GBA memory map (BIOS, EWRAM, IWRAM, IO, palette, VRAM, OAM, ROM at `0x08000000`).
- Defaults the whole ROM to Thumb, with the reset handler as ARM, plus any ARM functions found by fingerprint.
- Names from step 3 go in the `SDK` namespace and BIOS stubs in `BIOS`. Every scan seed becomes a function, and
  compressed blobs get a label and a comment.
- `--analyze` runs full auto-analysis. It's slow on big ROMs (around an hour for 32 MB).

## 5. Decomp check (manual)

Is there a decompilation, or at least a symbol map, for the game or the game it's based on?

- **Yes** (Pokémon Ruby/Sapphire/Emerald/FireRed/LeafGreen, Mystery Dungeon, Minish Cap, Fire Emblem, and others):
  build it in WSL (`tools\wsl_setup.sh` shows how) and verify the SHA-1 matches. Then go to 6a.
- **No** (Golden Sun 1 and 2 have none as of this writing): go to 6b.

## 6a. Symbol diff, for hacks of a decompiled game

Example: Unbound on FireRed. The scripts are in `tools\` and are currently specific to FireRed.

- `symdiff.py`: classifies every original function and table as unchanged, hooked, patched, moved or overwritten,
  explaining changes with the patch lists of known engines (CFRU, DPE).
- `moved_symbols.py`: finds where each relocated table now lives, by following the original code's pointers.
- `build_ghidra_project.py`: a Ghidra project with original names, plus names for the hack's new code taken from
  its hooks.

## 6b. Format work, for games without a decomp

1. Group the master-table entries by their first bytes (`filetable_*.csv`). Each group is usually one format.
2. Find the code that reads them:
   - `gbax refs ROM <table address>` lists the code that loads the table's address (`ldr` instructions) and the
     `BL` calls to any function.
   - `gbax decompile ROM <address> [--arm SIZE]` prints Ghidra's C-like decompilation. Add `--arm` for routines
     written in ARM code; these are often copied into RAM, so watch for DMA copies of code followed by a `bx`.
   - Follow the chain: table, then GetFile, then the loader, then the decompressor.
3. Decode with the game's own routine first: `gbax.emu.Gba(rom).call(addr, (src, dest))` runs it on an emulated
   ARM7 with the GBA memory map. That's exact by construction. Write native decoders where they're simple, and
   check them against the emulator.
   When reading code stalls, let the emulator search: `gbax.re.discover_decoders(rom, addr, size, candidates)`
   runs every ARM routine start (or any candidate list, such as the scan's function seeds) on the data. It keeps
   the routines that read it to the end and produce output. It found nothing for Golden Sun's format 2; decoders
   that keep their state in a struct or work frame by frame need live tracing instead.
4. Verify each group: a real compressed file is consumed to its end. `emu.Gba.call_tracking_reads` reports how far
   the routine read.
5. Register the codec in `gbax\profiles.py`; `gbax extract` then decodes the whole master table.
6. Record the formats in `notes\<game>.md`. Golden Sun's are in `notes\golden_sun.md`.

### Live tracing — `gbax trace ROM --launch [--seconds N]`

When static work stalls, watch the real game. This launches mGBA (the Qt app, `mGBA.exe -g`; the SDL build can't
open the GDB socket on Windows) and connects to its GDB server on port 2345. It breaks on the game's file loader and
logs every load: file number, caller and format. For files in formats gbax can't decode, it sets read watchpoints
on their bytes. The code that reads them next is the decoder, even when it runs from a RAM copy. It's logged with
registers, plus a dump of that RAM code. Output goes to `games\<rom>\trace\<time>\`. Currently wired for Golden Sun's
loader (found from the master table); other games need their loader address.

mGBA's own log is a second trace source that needs no debugger: `mGBA.exe -l 255` prints every DMA transfer with
source and destination, and every BIOS call.

The emulator (`gbax.emu`) runs DMA transfers immediately when a routine writes a DMA control register. Golden Sun's
format-2 decoder depends on that.

## 7. Extract to common formats — `gbax extract ROM`

Output: `assets\bin\*.bin` (decoded data) and `assets\png\*.png` (grayscale tile previews), plus `assets\index.csv`.

Target formats that any host engine can take in:

| Asset | Format | Status |
|---|---|---|
| Tiles and sprites | PNG with its real palette, plus JSON for size and frames | `gbax palettes`: colour PNGs plus an HTML gallery. 88% correct on FireRed; Golden Sun needs its palette links reversed |
| Palettes | JASC `.pal` / JSON | to do |
| Tilemaps and metatiles | JSON | to do |
| Music | MIDI + SoundFont (`.sf2`) from MP2K songs and instrument sets | song tables found; export to do |
| Sound effects | WAV | to do |
| Text | UTF-8 JSON, keyed by the game's IDs | to do (needs each game's encoding) |
| Data tables (stats, items, moves) | JSON/CSV with named fields | per-game |

### Palettes — `gbax palettes ROM`

Output: `color\*.png`, `color\palettes.csv` and `color\index.html`, a gallery to open in a browser.

Each graphic is paired with a palette using structural evidence, tried in order of measured precision (checked
against FireRed's symbol names with `tools\eval_palettes.py`):

| Evidence | Precision alone |
|---|---|
| Parallel tables: a graphics table and a palette table of the same stride and length | 100% |
| Struct fields: graphic and palette fields in the same array of structs | 95% |
| A palette pointer in the word right after a graphics pointer | 80% (right 60/63 times when it disagrees with adjacency) |
| The next palette stored after the graphic | 81% |
| A palette embedded at the start of the same file (file-table games) | unmeasured |

The content fit (whether neighbouring pixels get similar colours) can't rank palettes, but it does tell plausible
renderings (median 0.2) from noise (0.6 and up). Weak evidence that renders as noise is rejected.

Results: FireRed 88% correct (1,453 of 1,653 checked). Unbound has 4,614 of 4,632 graphics coloured. Golden Sun:
only a handful pass, because its graphics-to-palette links are game-specific and still to be reversed.

## 8. Catalog

Everything extracted goes into one place, with a source game, an original address, a type and a license note.
That's the shared pool the combined game draws from.

## 9. Rebuild in the app

The target is a native Android app (Galaxy Z Fold 7), not a GBA ROM. GBA machine code doesn't run there, so:

- **Assets** go in through the common formats from step 7.
- **Systems** are rebuilt in the app's engine. Decomps (FireRed, plus CFRU/DPE source) are ported or followed line by
  line. Games without a decomp (Golden Sun) are rebuilt from a written spec: Ghidra decompilation plus live traces
  of the real game.
- **Behaviour checks**: the original game, running in mGBA with `gbax trace`, is the reference to compare the
  rebuild against.

## What each game needs, so far

| | Pokémon Unbound | Golden Sun | Golden Sun: The Lost Age |
|---|---|---|---|
| Code / size | BPRE, 32 MB | AGSE, 8 MB | AGFE, 16 MB |
| Base / decomp | FireRed v1.0 + CFRU + DPE | none | none |
| Sound | MP2K (86 functions fingerprinted), 327 songs | MP2K (69), 312 songs | MP2K (62), 800 songs |
| Compression | BIOS LZ77 (8,800 blobs) | Camelot formats 0/1 (`0x08002544`) and 2 (`0x08002808`); 560 files decoded | same routines (`0x080128AC`, `0x08012B74`); 1,002 decoded |
| Graphics | 4bpp | 4bpp and 8bpp | 4bpp and 8bpp |
| Asset index | none; pointers spread through the code | master table `0x08320000`, 975 entries | master table `0x08680000`, 1,723 entries |
| Code layout | one image plus CFRU's hooks | 16 code modules with export stubs | 15 code modules with export stubs |
| Path | 6a | 6b | 6b |
