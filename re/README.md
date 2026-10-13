# re/ — reverse-engineering toolkit and notes

Taken from the local analysis workspace (`C:\Users\aaron\Documents\UnboundHack`) so the work travels with the repo.
Code, notes and analysis reports only: **no ROMs and nothing extracted from them** (`.gitignore` keeps them out).

| Path | Contents |
|---|---|
| `PROCEDURE.md` | Step-by-step flow for taking any GBA game apart (identify, scan, fingerprint, Ghidra, symbol diff or format work, live tracing, extract, catalog, rebuild). |
| `UNBOUNDHACK_README.md` | The local workspace's README: layout, findings so far, environment. |
| `notes/golden_sun.md` | Every Golden Sun format and address found so far (file table, compression 0/1/2, portraits, battle effects, maps, open questions). |
| `gbax/` | The general GBA extraction toolkit (`python -m gbax ...`): identify, scan, sigs, extract, palettes, ghidra, refs, decompile, callers, trace. Golden Sun codecs in `gbax/codecs/`. |
| `tools/` | FireRed-hack scripts: Unbound symbol diff, moved tables, Unbound Ghidra project, WSL setup. |
| `reports/` | Output of those scripts (Unbound vs FireRed symbol diff, moved symbols, free space, Ghidra function list). |

## What needs the local PC

Everything that reads a ROM runs on the PC, because the ROMs are never uploaded: gbax extraction, Ghidra projects,
mGBA live tracing (`gbax trace`), and the WSL builds. The original ROMs live in `OneDrive\Apps-Roms` (read-only);
per-ROM workspaces are in `UnboundHack\games\`.

The local workspace is still the working copy for those runs; changes to the toolkit get synced back here.
