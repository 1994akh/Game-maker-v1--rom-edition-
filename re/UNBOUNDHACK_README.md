# UnboundHack

Analysis and modding workspace. The original ROMs stay untouched in `OneDrive\Apps-Roms`; everything here only
reads them.

## End goal (updated 2026-10-12)

A new game for personal use that combines parts of Pokémon Unbound, Golden Sun and Golden Sun: The Lost Age, built
as a **native Android app for the Samsung Galaxy Z Fold 7**. It has to work on both the folded cover screen and the
unfolded inner screen, and switch between them. It's no longer a GBA ROM, so ROM size, RAM, VRAM and palette limits
don't apply, and engines are rebuilt as needed.

What that means for this project:
- **Decompilation is now the source material and the spec, not the build.** We take apart all three games fully:
  every asset, every data table, and the rules each system follows (battle formulas, AI, map and event logic). The
  rebuilt engines reproduce that behaviour; the GBA machine code itself won't run in the app.
- **Assets** are exported to normal formats: PNG for graphics, JSON for data and maps, MIDI and SoundFont (or
  rendered audio) for music, UTF-8 for text.
- **Code reuse**: Pokémon logic is available as readable C (the FireRed decomp plus CFRU/DPE source) to port or use
  as reference. Golden Sun has no source, so its systems are specified from Ghidra and live tracing, then rewritten.
- **Open decisions** (the user's): engine and language for the app, scope of the first playable version, and how the
  two games' systems combine.

The tools stay general: gbax and the procedure work for any GBA game.

Target games so far: Pokémon Unbound, Golden Sun, Golden Sun: The Lost Age.

**Start with [PROCEDURE.md](PROCEDURE.md)**, the step-by-step flow for taking any GBA game apart, and **gbax**, the
program that automates it: `.venv\Scripts\python.exe -m gbax all <rom.gba>`.

## Layout

| Path | Contents |
|---|---|
| `gbax/` | The general GBA extraction toolkit (identify, scan, sigs, extract, ghidra). Works on any ROM. |
| `gbax/sigdb/` | Function fingerprint databases (`pokefirered_sdk.json`: 427 Nintendo SDK/library functions). |
| `games/<CODE>-<sha1>-<name>/` | One workspace per ROM: gbax reports, file tables, assets, Ghidra project. |
| `notes/` | Per-game format notes (`golden_sun.md`). |
| `build/` | FireRed v1.0 and Rev 1 built from source in WSL (SHA-1 verified), with the v1.0 ELF and map. |
| `ghidra/` | Unbound Ghidra project with original, CFRU/DPE and relocated names (`tools/build_ghidra_project.py`). |
| `tools/` | FireRed-hack-specific scripts (symbol diff, moved tables, Unbound Ghidra build) and `wsl_setup.sh`. |
| `reports/` | Output of the FireRed-hack scripts. |
| `apps/` | Portable tools: Ghidra 12.1.4, Temurin JDK 21, HexManiacAdvance 0.5.6.1. Installers are in `apps/_downloads`. |
| `external/pokefirered` | pret FireRed decompilation (source). |
| `external/pokefirered-symbols` | Symbol maps for FireRed v1.0 (`pokefirered.sym`) and Rev 1 (`pokefirered_rev1.sym`). |
| `external/Complete-Fire-Red-Upgrade` | CFRU engine source (Skeli789). |
| `external/DPE-Unbound`, `external/Dynamic-Pokemon-Expansion` | Pokémon data expansion, Unbound branch and master. |
| `.venv/` | Python 3.13 virtualenv with pyghidra and capstone. |

Installed system-wide: Python 3.13 (per-user), mGBA 0.10.5. Already present: Git, .NET 6 Desktop Runtime.

## Running scripts

Use the venv's Python, for example `.venv\Scripts\python.exe tools\check_setup.py --ghidra`.

- `tools/check_setup.py`: checks that the symbols line up with the ROMs and that pyghidra can start Ghidra.
- `tools/analyze_rom.py <hack.gba> <base.gba>`: read-only byte comparison, writes to `reports/`.
- `tools/symdiff.py`: symbol-by-symbol diff of Unbound against vanilla FireRed (Rev 1 bytes relocated to v1.0
  addresses), with changes attributed to CFRU/DPE patch lists. Writes `reports/symbol_diff.md` (summary, per-system
  rollup) and `reports/symbol_diff.csv` (all ~30,000 symbols).
- `tools/inspect_symbol.py NAME ...` or `--status patched --kind code --sample 10`: shows the changed bytes of
  specific symbols, decoding pointers and `BL` calls.

## Findings so far

- Unbound is 32 MB, built on FireRed **v1.0** (BPRE, version byte 0). It has about 1.6 MB of free space left.
- The base ROM on hand is FireRed **Rev 1** (v1.1). Rev 1 shifts most code and data by small amounts, so a plain
  byte diff overstates the changes (87% "changed"). Matching each symbol's address in the v1.0 and Rev 1 maps
  fixes this.
- Unbound has moved the species-name table: the v1.0 address of `gSpeciesNames` no longer holds names.
- Symbol diff (`reports/symbol_diff.md`): of ~30,200 vanilla symbols, 21,490 are byte-identical in Unbound,
  678 functions are hooked (557 via public CFRU/DPE hook lists, 121 not listed), ~2,200 patched or modified, and
  ~4,950 overwritten (almost all data: graphics, learnsets, trainer parties, Pokédex text). 434 code changes aren't
  in the public CFRU/DPE lists, so they're Unbound-specific or from a newer private CFRU.
- Caveat: "unchanged" doesn't mean "still used". CFRU reroutes the battle engine through hooks, so many untouched
  vanilla battle functions are probably dead code.

- Golden Sun 1 and 2: Nintendo's MP2K sound engine (song tables found), custom compression (no BIOS decompression
  stubs), a self-indexing master file table (GS1 `0x08320000`, 975 entries; GS2 `0x08680000`, 1,723 entries), and
  15–16 code modules that export functions through jump stubs. See the table at the end of PROCEDURE.md.

## Environment

- WSL Ubuntu 26.04 (runs as root; no Linux user created yet) with arm-none-eabi binutils/gcc and pret's agbcc in
  `/opt/gba`. `tools/wsl_setup.sh` rebuilds everything.

- Golden Sun compression is solved (formats 0 and 1, see `notes/golden_sun.md`). Every file-table entry is extracted
  to `games/AG*/files/` (GS1: 298 decoded, 661 raw; GS2: 532 decoded, 1,176 raw), with 4bpp and 8bpp previews.

- Palettes (`gbax palettes`): FireRed 88% correct against symbol names, Unbound 4,614 of 4,632 graphics coloured.
  Galleries are at `games/<rom>/color/index.html`. Golden Sun's palette links are still to be reversed.

- Golden Sun portraits are solved: archive of palette + compressed sprite entries, decoded by emulating the game's
  sprite routine. GS1 54 and GS2 77 portraits at `games/AG*/files/sprites/index.html`.
- Golden Sun battle effects are solved: palette + compressed 8bpp bitmaps (GS1 111, GS2 165), in the same gallery.
- Golden Sun format 2 is solved through live tracing in mGBA (`gbax trace`): 16 KB 4bpp tile blocks, likely map and
  scene tilesets. GS1 262 and GS2 470 decoded.

## Next

- Golden Sun: enemy sprites and battle backgrounds (module #12), overworld sprites/menus (#4), maps (#3), the files
  starting with 0x02, and the text format. See `notes/golden_sun.md`.
- Music export for all three games: MP2K songs to MIDI, instrument sets to SoundFont.
- Render full scenes from tileset + tilemap + palette (tilemaps currently show as noise).
