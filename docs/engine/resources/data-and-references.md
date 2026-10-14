## Data, references and tools beyond Godot: research findings (2026-10-13)

Labels: VERIFIED means I saw it today through the GitHub API, a fetched page or a local read. INFERRED means it is my own knowledge or a search snippet I could not check.

### Top picks
1. **Pokémon data:** use the PokeAPI CSVs as the main source and pokeemerald-expansion for sprites. Use Showdown to cross-check.
2. **Map importer:** use the YATI plugin to bring our Tiled maps into Godot. Its page says it was tested on Godot 4.7.2.
3. **Golden Sun music:** render it from the ROM with agbplay, which handles Golden Sun's own variant of the GBA sound engine. Use FluidSynth offline for any MIDI + SF2 renders.
4. **Live tracing:** use mGBA, plus Lost Age save files and save states that the user supplies.
5. **Lost Age code:** our local alchemy copy already has some decompiled Lost Age world-map code (details in section 2). No public Lost Age disassembly exists outside alchemy.

### 1. Pokémon data sources (Gen 1–7 + forms)

**PokeAPI CSVs** — ADOPT as the main data source
- URL: https://github.com/PokeAPI/pokeapi (folder `data/v2/csv`)
- Licence: BSD-3-Clause. Last push 2026-10-13. VERIFIED.
- Files present (VERIFIED): `pokemon.csv`, `pokemon_species.csv`, `pokemon_forms.csv`, `pokemon_moves.csv` (10.7 MB), `pokemon_evolution.csv`, `evolution_chains.csv`, `moves.csv`, `move_meta.csv`, `type_efficacy.csv`, `pokemon_stats.csv`, `pokemon_types.csv`, `pokemon_abilities.csv`, `pokemon_egg_groups.csv`, `version_groups.csv`, `machines.csv`, `items.csv`, `encounters.csv`, `pokemon_species_names.csv`.
- Why it wins: it is the only source with every field catching and leveling need: catch rate, growth rate, base experience, EV yield, hatch counter and happiness. It also has evolution triggers, forms and learnsets per game, plus localized names.
- Conversion is easy. One saved Python script (standard csv/json modules only) can write `species.json`, `moves.json`, `learnsets.json`, `evolutions.json` and `types.json`. Typed GDScript Resource classes then load them with `JSON.parse_string`.
- Gen 1–7 filter (INFERRED):
  - species with ID up to 809;
  - forms whose `introduced_in_version_group_id` is 18 or lower (Ultra Sun/Ultra Moon);
  - learnsets where `version_group_id` = 18;
  - moves where `generation_id` is 7 or lower.
- Saves us: all hand entry of species, moves, learnsets, evolutions and types.

**PokeAPI/api-data** — SKIP
- URL: https://github.com/PokeAPI/api-data. BSD-3-Clause, last push 2026-10-13. VERIFIED.
- It is static JSON with one file per API resource, which means tens of thousands of files. The CSVs are far easier to convert. Its JSON Schema is the only extra.

**Pokémon Showdown data** — REFERENCE (cross-check, and the source for move-effect details)
- URL: https://github.com/smogon/pokemon-showdown (`data/`). MIT, last push 2026-10-13. VERIFIED.
- Main files (VERIFIED): `pokedex.ts` (538 KB), `learnsets.ts` (3.7 MB), `moves.ts` (485 KB), `typechart.ts`, `abilities.ts`, `items.ts`, `formats-data.ts`, `conditions.ts`, `FORMES.md`, and a `mods/` folder.
- Strengths (INFERRED): best form coverage (`baseSpecies`, `forme`, `otherFormes`). Learnset entries are tagged by generation, for example "7L15" means Gen 7, level 15. Moves carry structured fields: secondary effect chance, stat boosts, drain, recoil, multi-hit and priority.
- Conversion: a short Node script using the npm `pokemon-showdown` package can dump each generation to JSON.
- Gaps (INFERRED): no catch rate, growth rate or base experience. Some move effects exist only as JavaScript code, not data. Learnsets are per generation, not per game.

**veekun/pokedex** — SKIP
- URL: https://github.com/veekun/pokedex. MIT, last push 2022-07-21 (stale). VERIFIED.
- I believe PokeAPI's CSVs carry on its schema (INFERRED; PokeAPI's README doesn't mention veekun).

**pokeemerald-expansion (local)** — ADOPT for assets, REFERENCE for data
- Path: `C:\Users\aaron\Documents\UnboundHack\external\pokeemerald-expansion`. Version 1.17.2. VERIFIED.
- It has species files for Gen 1 through Gen 9 (`species_info/gen_1_families.h` … `gen_9_families.h`), level-up learnsets, and 1,423 `overworld.png` follower sprites. Those sprites cover the partner Pokémon walking on the field.
- Its data is C macros, so turning it into JSON is the hardest of the four options.
- Saves us: front, back, icon and follower sprites plus cries, linked to PokeAPI by National Dex number and form name.

### 2. Golden Sun references

**What our local goldensun-master disassembly actually is (VERIFIED)**
- Path: `C:\Users\aaron\OneDrive\Apps-Roms\goldensun-master`.
- It covers **Golden Sun 1 (USA) only** (SHA1 `5c4695205413df7db52b9a184815a07783999971`).
- It has 5,801 functions, but they are only named by address (`Func_77330`, `OvlFunc_common1_xxx`). Only 69 names are not pure address labels, and those are overlay-relative or helper names. The README's "symbolized" means these automatic labels.
- It has 97 map-code folders (3,540 functions). Its README says data has not been disassembled.
- It has 4 C tools: `unpack_overlay.c` / `pack_overlay.c` for map-code overlays and `unpack_strings.c` / `pack_strings.c` for text.
- Verdict: SKIP for porting. Alchemy has real names (for example `BattleFx_*`, `BattleParty_*`, `GetWorldMapCollision`) and C code for each map. Keep goldensun-master as an address index for emulator traces (`Func_X` sits at address `0x0800X`) and for those two tools.

**Lost Age code we already have (VERIFIED local)**
- `alchemy\games\THE LOST AGE` contains 493 .c files, 1,665 .s files and 297 MAP folders.
- `SRC\FIELD\WORLD_MAP` has `PREPARE.C`, `SCENE_EVENTS.C`, `SCENE_TABLES.C`, `STORY_ACTOR.C` and `IMPORT.S` (15 KB).
- `SRC\FIELD\COMMON\MAP\WORLD_COLLISION.C` contains a decompiled `GetWorldMapCollision`:
  - positions are fixed-point (shifted right by 17);
  - the collision grid is 64×64 cells;
  - collision tiles are 4×4-dot, 4bpp, 8 bytes each.
- `WorldMap_UpdateBobbingMarker` is also decompiled.
- There are world-map tile and palette PNGs, plus `SHIP_CABIN` and `SHIP_DECK` backdrops.
- No Lost Age C code contains Hover, Teleport or Sail, so those are most likely still assembly (INFERRED).

**Coaltergeist/goldensun-decomp** — REFERENCE
- URL: https://github.com/Coaltergeist/goldensun-decomp
- No licence file. Last push 2026-10-12, 550 commits. decomp.dev reports 27.65% decompiled. VERIFIED.
- Golden Sun 1 only. It is built on gsret's disassembly; I believe that is our goldensun-master (same ROM, same overlay layout — INFERRED).
- It uses a patched GCC 2.96 (camelot-gcc). Function and global names come from FutureFractal's Ghidra annotations.
- Map code is split into named files, one per overlay, under `src/maps/*.c`.
- Saves us: a second set of names for functions that alchemy still leaves in assembly. Read it on GitHub when needed. FutureFractal's Ghidra annotations are not published separately; I searched and found nothing.

**Coaltergeist/camelot-gcc** — SKIP
- URL: https://github.com/Coaltergeist/camelot-gcc. No licence, last push 2026-09-11. VERIFIED.
- It only matters for byte-matching builds, and we are porting.

**Lost Age disassembly or decompilation** — none exists outside alchemy
- I sorted a GitHub search for "golden sun" by last update and found none. VERIFIED.

**Zaxaerith/GoldenSunTheLostAgeRecomp** (also GoldenSunTheBrokenSealRecomp) — SKIP, or REFERENCE as a last resort
- URL: https://github.com/Zaxaerith/GoldenSunTheLostAgeRecomp
- PolyForm Noncommercial 1.0.0, last push 2026-10-08. VERIFIED.
- It machine-translates all 17,041 Lost Age cartridge functions to C++, but with no meaningful names (for example `gf_memory_transfer_arm_at_08000428`). Windows only, tested only as far as the first battle.
- Only use: reading C++ instead of assembly for the ship and world-map routines.

**wootbeer/gsrandroid** — REFERENCE
- URL: https://github.com/wootbeer/gsrandroid
- PolyForm Noncommercial, 8 commits, last push 2026-10-10 (search listing). VERIFIED.
- An Android port of a recompiled Golden Sun 1: you supply the ROM and it compiles the game on the device with TinyCC. It has touch controls, controller remapping and save states. No foldable support, no Lost Age.
- Use: playing the original side by side with ours on the Fold to compare behaviour.

**Penrim/golden-sun-collection** and **Coaltergeist/Open-GSTLA** — SKIP
- golden-sun-collection is a builder that combines Golden Sun 1 and Lost Age into one GBA ROM (MIT, last push 2026-10-13).
- Open-GSTLA has been empty since 2019.

**Golden Sun Hacking Community** — REFERENCE
- http://www.goldensunhacking.net and Discord https://discord.com/gg/4EWvPAAnyT
- The Discord link and community details come from the Golden Sun Wiki article, last edited 2023-01-21. VERIFIED.
- The forum's TLS certificate had expired today, so I could not load it. Its documentation contents are INFERRED.
- Best place to ask for Lost Age RAM addresses for the world map, ship, Hover and Teleport.

**Atrius's Lost Age Editor** (v0.4, June 2011; PokeCommunity thread 258098) — SKIP
- It is a closed .NET ROM editor. gsmagic, which we already have, is its successor (written originally by Teawater).

**goldensunwiki.net** — REFERENCE, for writing the specs of field abilities
- Licence: CC BY-SA 4.0. VERIFIED.
- The Teleport page (last edited 2023-10-19) says:
  - Teleport is Jupiter Psynergy costing 3 PP, from the Teleport Lapis found in Mars Lighthouse;
  - on the world map it moves the party and ship to large Golden Sun 1 towns, and the ship is parked at the nearest sea landing;
  - in dungeons it works only between paired floor circles (Mars Lighthouse, Islet Cave, Contigo, Yampi Desert Cave).
- Same use for the Hover, Ship and World Map pages.
- Also useful: https://goldensunwiki.net/wiki/Golden_Sun:_The_Lost_Age/Tricks,_glitches,_and_other_minutiae (INFERRED to cover debug tricks).

**Pages that failed today**
- tcrf.net's Lost Age page could not be read. A search snippet says it lists debug rooms, including two Psynergy Test rooms, which would be handy for tracing Hover and Teleport (INFERRED).
- Data Crystal's Lost Age page returned 404. SKIP.
- Almar's Guides Lost Age Action Replay codes (https://almarsguides.com/retro/walkthroughs/gba/games/goldensunthelostage/actionreplay/): REFERENCE. Cheat codes reveal RAM addresses for flags and position (INFERRED).

### 3. Tools for the later graphics, audio and map passes

**Graphics**

**Aseprite** + **godot-aseprite-wizard** — LATER, then ADOPT
- Aseprite: https://github.com/aseprite/aseprite. Source-available (paid binary or build it yourself). Last push 2026-10-13. VERIFIED.
- godot-aseprite-wizard: https://github.com/viniciusgerevini/godot-aseprite-wizard. MIT, last push 2026-08-17. VERIFIED. Godot 4 plugin; 4.7 support INFERRED.
- Saves us: writing our own sprite-sheet and animation importer.

**Pixelorama** — LATER (free alternative)
- URL: https://github.com/Orama-Interactive/Pixelorama. MIT, last push 2026-10-13. VERIFIED.
- Built with Godot and also runs on Android (INFERRED), so sprites could be edited on the Fold itself.

**LibreSprite** — SKIP unless Aseprite's cost matters
- URL: https://github.com/LibreSprite/LibreSprite. GPL-2.0, last push 2026-10-13. VERIFIED.

**Free Texture Packer** — SKIP
- URL: https://github.com/odrick/free-tex-packer. MIT, last push 2024-07-14 (stale). VERIFIED.
- Aseprite sheet export plus Godot's own import already covers this.

**Real-ESRGAN** — SKIP for pixel art
- URL: https://github.com/xinntao/Real-ESRGAN. BSD-3-Clause, last push 2024-08-06. VERIFIED.
- AI upscaling smears pixel art. At most, use it for portraits.

**waifu2x-ncnn-vulkan** — same verdict as Real-ESRGAN
- URL: https://github.com/nihui/waifu2x-ncnn-vulkan. MIT, last push 2026-04-13. VERIFIED.

**libretro glsl-shaders** — REFERENCE
- URL: https://github.com/libretro/glsl-shaders. Licence mixed (none at repo level), last push 2026-10-11. VERIFIED.
- Contains ScaleFX and xBR smoothing shaders that could be ported to Godot. The simpler recommendation is to keep the art at native resolution and use Godot's integer stretch scaling (INFERRED available since Godot 4.3).

**Audio**

**agbplay** — ADOPT for Golden Sun music
- URL: https://github.com/ipatix/agbplay. LGPL-3.0, last push 2026-09-29. VERIFIED.
- Its README lists support for Camelot's variant of the GBA sound engine and Camelot's reverb for both Golden Sun 1 and Lost Age. It exports WAV per track or per song. VERIFIED.
- Support for Golden Sun's synth instruments is INFERRED. An SF2 rip loses those instruments and the reverb.
- Saves us: accurate Golden Sun audio, straight to OGG.

**FluidSynth** — ADOPT, offline rendering only
- URL: https://github.com/FluidSynth/fluidsynth. LGPL-2.1, last push 2026-10-11. VERIFIED.
- Example: `fluidsynth -ni x.sf2 y.mid -F y.wav`, then convert to OGG with loop points set in Godot's import settings.

**Playing MIDI live inside Godot** — SKIP
- arlez80/godot-midi-player only supports Godot 3. VERIFIED.
- nonameentername/godot-fluidsynth was last pushed 2023-10 and has 0 stars. VERIFIED.

**TinySoundFont** — LATER, only if live MIDI becomes necessary
- URL: https://github.com/schellingb/TinySoundFont. MIT, last push 2026-07-19. VERIFIED. Would need wrapping as a Godot extension.

**Polyphone** — LATER
- URL: https://github.com/davy7125/polyphone. GPL-3.0, last push 2026-06-06. VERIFIED.
- For fixing loops and envelopes in the SF2s that GBA Mus Ripper produced.

**VGMusicStudio** — SKIP
- URL: https://github.com/Kermalis/VGMusicStudio. LGPL-3.0, last push 2024-07-13 (stale). VERIFIED.

**Maps**

**Tiled** — ADOPT (already in use)
- URL: https://github.com/mapeditor/tiled. Last push 2026-10-12. The API showed no standard licence ID; I believe the app is GPL-2 (INFERRED).

**YATI** — ADOPT
- URL: https://github.com/Kiamo2/YATI. MIT, last push 2026-10-05. VERIFIED.
- GDScript version 2.2.9 needs Godot 4.3 or newer; the page says it was tested on 4.7.2.
- Imports .tmj/.tmx files: all layer and object types, templates, custom properties and classes, tile collisions and animations. A runtime import package also exists.
- Saves us: writing our own Tiled-to-Godot importer.

**Debugging and tracing**

**mGBA** — ADOPT
- URL: https://github.com/mgba-emu/mgba. MPL-2.0, last push 2026-10-08. VERIFIED.
- Save states, memory search, a GDB stub and Lua scripting (INFERRED) for tracing the world-map and ship code against alchemy and goldensun-master addresses.

### 4. Local files the user could add

What exists now (VERIFIED): one Golden Sun 1 battery save, `C:\Users\aaron\Documents\UnboundHack\games\AGSE-5c469520-Golden-Sun-USA-Europe\rom\Golden Sun (USA, Europe).sav` (64 KB, story point unknown). There is no Lost Age save, and no save states anywhere under `UnboundHack\games` or `Apps-Roms`.

**Highest value**
1. **Lost Age battery saves** (.sav, 64 KB) at these points:
   - first time sailing the ship;
   - after getting the Hover Jade;
   - in or near Lemuria;
   - after getting the Wings of Anemos (the ship can fly);
   - a late-game save with the Teleport Lapis from Mars Lighthouse.
   
   One late-game save alone would unblock tracing of the world map, ship, Hover and Teleport.
2. **mGBA save states (.ss1)**, each taken just before the action:
   - walking on the Lost Age world map;
   - on the ship at sea;
   - in flight;
   - next to a Hover pad;
   - next to a Teleport circle;
   - casting Teleport on the world map;
   - Lemuria;
   - a battle about to start;
   - Golden Sun 1 world map and its boat ride.

**Useful**
3. A note of what story point the existing Golden Sun 1 save is at, or more Golden Sun 1 saves at the world map and the ship.
4. The GBA BIOS file (`gba_bios.bin`, 16 KB) from their own hardware. It makes mGBA tracing more accurate, and the Zaxaerith recomp requires it (INFERRED as optional for mGBA).
5. Optionally, a short list of the Lost Age Action Replay or GameShark codes they use (flags, position, walk-through-walls). These show RAM addresses.

### Sources
https://github.com/PokeAPI/pokeapi · https://github.com/PokeAPI/api-data · https://github.com/smogon/pokemon-showdown · https://github.com/veekun/pokedex · https://github.com/Coaltergeist/goldensun-decomp · https://decomp.dev/Coaltergeist/goldensun-decomp · https://github.com/Coaltergeist/camelot-gcc · https://github.com/Zaxaerith/GoldenSunTheLostAgeRecomp · https://github.com/wootbeer/gsrandroid · https://goldensunwiki.net/wiki/Fandom:Golden_Sun_Hacking_Community · https://goldensunwiki.net/wiki/Teleport · https://www.pokecommunity.com/threads/golden-sun-the-lost-age-editor-by-atrius-release-v-0-4-is-out.258098/ · https://github.com/adituv/gsmagic/blob/master/README.md · https://almarsguides.com/retro/walkthroughs/gba/games/goldensunthelostage/actionreplay/ · https://github.com/Kiamo2/YATI · https://github.com/mapeditor/tiled · https://github.com/ipatix/agbplay · https://github.com/FluidSynth/fluidsynth · https://github.com/schellingb/TinySoundFont · https://github.com/davy7125/polyphone · https://github.com/Kermalis/VGMusicStudio · https://github.com/arlez80/godot-midi-player · https://github.com/nonameentername/godot-fluidsynth · https://github.com/aseprite/aseprite · https://github.com/viniciusgerevini/godot-aseprite-wizard · https://github.com/Orama-Interactive/Pixelorama · https://github.com/LibreSprite/LibreSprite · https://github.com/odrick/free-tex-packer · https://github.com/xinntao/Real-ESRGAN · https://github.com/nihui/waifu2x-ncnn-vulkan · https://github.com/libretro/glsl-shaders · https://github.com/mgba-emu/mgba