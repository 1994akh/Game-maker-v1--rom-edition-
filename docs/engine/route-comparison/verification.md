**Verification of fit_report.md, checked 2026-10-13**

Sources: GitHub REST API (`api.github.com/repos/<owner>/<repo>`, plus its `/contents`, `/releases` and `/license` endpoints), raw README and LICENSE files, decomp.dev, and the three local clones. GitHub reports sizes in KB. All 8 repos exist and none are archived.

| # | Claim in report | Verdict | Evidence / correction |
|---|---|---|---|
| 1 | PascalPixel/alchemy decompiles both Golden Sun games: GS1 about 90%, GS2 about 4.7% | CONFIRMED | https://github.com/PascalPixel/alchemy. The `history.tsv` file on the `progress` branch shows 7,429,580 / 8,238,924 = 90.18% for GS1 and 559,084 / 11,873,412 = 4.71% for GS2 (last row 2026-10-05T13). https://decomp.dev/projects?platform=gba shows 89.93% decompiled and 89.93% fully linked. Small fix: the file is at the root of the `progress` branch, not at `progress/history.tsv`. |
| 1a | alchemy has no licence, is active, and its size | CONFIRMED | GitHub licence is null. Last push 2026-10-05 (8 days ago). HEAD is b62ae63, "Move progress publishing to CI". 241,253 KB, 144 stars, mostly Assembly, C and Rust. |
| 2 | GS1 C file counts: BATTLE 174, FIELD 281, MENU 101, SYSTEM 35 | CONFIRMED | Counted in the clone under `games/THE BROKEN SEAL/SRC/`. Also there: GRAPHICS 92, GAME 20, DEBUG 8, SOUND 8. `games/COMMON/SRC` has 91 .c files. |
| 3 | Headers PSYNERGY_MENU.H, DJINN_MENU.H, BATTLE_FORMATION.H, SAVE_STATE.H; TILEACT.C; FIELD/COMMON/{OBJECT,SCRIPT,EVENT,CAMERA} | CONFIRMED | All present in the clone. `TILEACT.C` is at `SRC/FIELD/COMMON/TILEACT.C`. |
| 4 | BATTLE_WORK.H has `enemy_classes[6]`, `sprite_slots[6]`, `enemy_units[7]`, `actions[20]`; the formation record has 5 member ids with min/max counts | CONFIRMED | The struct is `struct BattleSession` (reached through `gBattleWork`), not a struct called "BattleWork". It also has `summon_masks[6]`, `party_units[7]`, `placement[14]` and `owner_slots[8]`. `BattleFormationRecord` has `{battle_type; member_ids[5]; minimum_counts[5]; maximum_counts[5]}`, and there are 380 records (the code checks `>= 380`). |
| 4a | This means a 6-enemy cap | INFERRED (strong), not proven | There is no MAX or COUNT constant. Unit lists end with 255, so 7 entries means 6 units plus the end marker, and removed units are marked 254. Every per-enemy array has 6 entries. `party_units[7]` has the same shape, so 6 is the list size for each side. It does not prove the game ever puts 6 enemies on the field. |
| 5 | Coaltergeist/goldensun-decomp is GS1 USA only, 27.65%, with modules field_engine, field, ui, battle, battle_anim, and uses m4a | CONFIRMED | https://github.com/Coaltergeist/goldensun-decomp. decomp.dev shows 27.65%. The README lists those modules, says it uses "the stock m4a audio engine", and `src/lib` holds the m4a code. No licence. Last push 2026-10-12. 22,055 KB, 28 stars. |
| 6 | 999sian/tmc ("Project Picori") is a native Minish Cap port using SDL3 | CONFIRMED | https://github.com/999sian/tmc is a fork of zeldaret/tmc. The README names SDL3, a software PPU in `port/ppu`, and agbplay. 23 port files include `<SDL3/...>`. |
| 6a | Picori has an Android build and APK releases | CONFIRMED | Release v0.9.5 (2026-09-28) includes `tmc-multi-android-v0.9.5.apk`. `android/` is a Gradle project (minSdk 21, targetSdk 34). xmake builds `libmain.so` and Gradle only packages it. The CHANGELOG has Android fixes. The repo description only names Linux, Windows and macOS. |
| 6b | Picori is GPL-3.0 | CONFIRMED | GitHub shows NOASSERTION, but the LICENSE text is GPL-3.0. `libs/agbplay_core` is LGPL-3.0, according to THIRD-PARTY-LICENSES.md. 38,838 KB, 462 stars, last push 2026-09-28. Picori needs the user's own ROM (USA, EU or JP, checked by SHA-1). |
| 7 | jjppof/goldensun_html5 is MIT, TypeScript on Phaser 2 | CONFIRMED | https://github.com/jjppof/goldensun_html5. LICENSE.txt is MIT. The README says PhaserJS CE 2.19.0, and the source is 232 .ts files (about 64.7k lines) using TypeScript 5.9. GitHub labels it JavaScript, probably because of bundled JS such as `static/phaser.js` (INFERRED). |
| 7a | It has 14 field Psynergy files: Move, Frost, Growth, Reveal, Lash, Lift, Pound, Douse, Whirlwind, Mind Read, Retreat, Avoid, Sand, plus Wave | CONFIRMED | All are in `base/field_abilities/`, alongside the base class `FieldAbilities.ts`. |
| 7b | It has Pushable, RollingPillar, RopeDock and Breakable objects | CONFIRMED | Plus `WhirlwindSource.ts`. |
| 7c | It has about 75 event types plus tile events for climb, ice slide, rope and jump | CONFIRMED | 76 files in `base/game_events/`: 74 event types plus `GameEvent.ts` and `GameEventManager.ts`. Tile events also include Fall, Slider, Speed, Step, Teleport, Collision and EventTrigger. |
| 7d | Its battle has Djinn, Summons, EnemyAI and BattleFormulas | CONFIRMED | `base/battle/` has `Battle.ts` (1,845 lines), `BattleFormulas.ts` (214) and `EnemyAI.ts` (365). `Djinn.ts` is 146 lines. `Summon.ts` is only 17 lines, so it holds data and the summon logic is in the battle code (INFERRED). |
| 7e | It uses Tiled maps | CONFIRMED | Details are in the spot-check notes below. |
| 7f | Activity and size | NOTE | Last commit on master is 2026-01-24 (#594). The API's pushed_at is 2026-10-02, probably a push to another branch (INFERRED). 56,335 KB, 207 stars. It has an Electron desktop wrapper and no Android build. |
| 8 | NTx86/pokeemerald-sdl2pc, branch `pc_port`, runs on Windows and Linux only and has no licence | CONFIRMED | https://github.com/NTx86/pokeemerald-sdl2pc. The default branch is `pc_port`. It is a fork of plain pret/pokeemerald, not expansion. It uses SDL2 2.0.16 and builds under WSL with mingw. 522,070 KB, 41 stars, last push 2026-09-15. |
| 9 | hirata-producoes/pokemon-regionalidades runs expansion through SDL2 | CONFIRMED | https://github.com/hirata-producoes/pokemon-regionalidades. The README (in Portuguese) says it is based on expansion **1.16.3**, with an SDL2 layer in `src/platform`, a native Windows exe and a `.pak` resource pack. It is still in development, with Windows only. No licence, 0 stars, last push 2026-10-11, 232,875 KB. |
| 10 | smogon/pokemon-showdown is MIT | CONFIRMED | https://github.com/smogon/pokemon-showdown. Last push 2026-10-13, 210,359 KB. |
| 11 | PMDCollab/SpriteCollab is CC BY-NC 4.0 | CONFIRMED | https://github.com/PMDCollab/SpriteCollab. GitHub shows NOASSERTION, but LICENSE.md is Attribution-NonCommercial 4.0. There is also a `license_history/` folder, so some sprites may have had different terms over time (INFERRED). The repo is about 1.9 GB (1,920,283 KB). Last push 2026-10-13. |
| — | The Minish Cap is listed on decomp.dev | UNVERIFIABLE | The decomp.dev GBA listing as fetched showed no tmc entry. Nothing depends on this. |

**Clone paths.** Each is `git clone --depth 1` with no submodules, and nothing in them was built or run.

| Clone | Commit | Total size | Working tree | .git |
|---|---|---|---|---|
| `C:\Users\aaron\Documents\UnboundHack\external\alchemy` | b62ae63, 2026-10-05 | 148 MiB | 113 MiB, 18,948 files | 36 MiB |
| `C:\Users\aaron\Documents\UnboundHack\external\goldensun_html5` | b8b086d, 2026-01-24 | 35 MiB | 22 MiB, 624 files | 13 MiB |
| `C:\Users\aaron\Documents\UnboundHack\external\tmc-picori` (from 999sian/tmc) | bd06a63, 2026-09-28 | 32 MiB | 27 MiB, 2,368 files | 6 MiB |

**Spot-check notes**

**alchemy**
- **Layout:** `games/{COMMON, THE BROKEN SEAL, THE LOST AGE}/{SRC, INCLUDE, SOUND, TEXT}`, plus `tools/` (Rust), `recon/{tbs,tla}`, and `agbcc`, `agscc`, `psynergy`.
- **Battle code (GS1):** `SRC/BATTLE` has subfolders EFFECT (Psynergy and Djinn effects such as `DJINN_BURSTS.C` and `CASTING.C`), SUMMON, PARTY, MOTION and PRESENTATION. Most files have generic names (`BATTLE*.C`, `EFFECT*.C`).
- **Enemy selection code:**
  - `SRC/BATTLE/FORMATION_SELECT_RANDOM_AVAILABLE_MEMBER.C` picks a random formation member.
  - `BATTLE5.C` holds `BattleFormation_SelectLevelMatchedCandidate`, plus a function above it that averages the members' levels and rejects formations whose members aren't unlocked by game flags.
  - `BATTLE4.C` and `PARTY/PARTY.C` loop over `enemy_units` until they hit 255.
- **Field code (GS1):** `SRC/FIELD/COMMON` (75 .c files) holds CAMERA, EFFECT, EVENT, MAP, OBJECT, SCRIPT, TILEACT.C and per-area puzzle folders. Per-map folders use Japanese names (KOROSSEO_*, GOMA_*, and so on).
- **The Lost Age:** `games/THE LOST AGE/SRC` already has 493 .c files even though only 4.7% matches, so most of them are not finished matching C.

**goldensun_html5**
- **Map loading, step by step:**
  1. `assets/dbs/maps_db.json` lists each map with its Tiled JSON, tileset PNG, BGM, lazy-load setting and `collision_embedded` flag.
  2. `Map.load_map_assets` (`base/Map.ts:550`) loads the map with Phaser's `game.load.tilemap(..., Phaser.Tilemap.TILED_JSON)`.
  3. Collision comes from Tiled object layers, one per collision layer, using properties such as `affected_by_reveal`, `controller_variable` and `split_polygon`. Maps without `collision_embedded` load separate P2-physics JSON files instead.
  4. `mount_map` (`Map.ts:2202`) reads map properties by prefix: `tile_event/`, `npc/`, `interactable_object/` and `game_event/` are sent to `create_tile_event`, `create_npc`, `create_interactable_object` and the game-event code.
- **Sample map:** `assets/maps/madra/madra.json` is Tiled 1.9.2 (format 1.1) with layers such as ground_00, cliff_00 and buildings_00. The repo ships 5 map folders: cave, forest, madra, snowland and world_map.
- **Data:** the `assets/dbs/` folder holds abilities, classes, djinni, enemies, enemies_parties, summons, items, npc, interactable_objects and custom_field_psynergies.

**tmc-picori**
- **android/:** a Gradle app (`dev.picori.tmc`) with `TMCActivity.java` plus SDL3's Java glue under `org/libsdl/app/*` (SDLActivity, HIDDevice*, SDLControllerManager and others), 28 files in all.
- **Touch controls:**
  - `port/port_touch_controls.cpp` (800 lines, Android-only) offers either a floating joystick, which re-centres wherever you touch on the left ~45% of the screen, or a d-pad.
  - It has 6 button zones (round and pill-shaped), a settings button, and an R-button glow when R has an action available.
  - The overlay hides when a gamepad is in use (`Port_TouchControls_NotifyGamepadUsed` and `Port_TouchControls_SetGamepadAvailable`).
- **Analog movement:** `port/port_analog_movement.c` (91 lines) maps the stick angle onto the engine's 32 directions (11.25° each), which the original game only reached as 8. It is behind the `REBORN_FEAT_ANALOG_360_MOVEMENT` setting.
- **Platform layer:** `port/` has 182 entries. The key files are:
  - `port_main.c` (945 lines): the SDL3 main loop
  - `port_ppu.cpp` (1,884) plus the `ppu/` folder: the software renderer
  - `port_gpu_raster_gl.cpp`: the OpenGL renderer
  - `port_audio.c` and `port_m4a_backend.cpp` (1,101): audio through agbplay
  - `port_save.c` (811)
  - `port_asset_pak*.cpp`, `port_asset_loader*` and `port_asset_bootstrap*`: asset packs, unpacked from the ROM on first launch
  - `port_widescreen.h`: `PORT_VIEW_WIDTH` comes from `MODE1_GBA_WIDTH` and is set at build time; the header credits SAT-R/sa2 for the approach
  - `port_android_log.c`, `port_touch_controls.*` and `port_rom_picker.c`
- **Build files:** `xmake.lua` has an Android target (`build/android/<abi>/libmain.so`), pins SDL3 because an unpinned SDL3 crashed the Android build at v0.8.1, and turns RetroAchievements off on Android.
- **Not fetched:** the git submodules `libs/tmc-Android-Experimental`, `libs/VirtuaAPU` and `libs/tmc-Modern-Launcher` (all by MatheoVignaud) are empty in this shallow clone.

**Caveats**
- These folders are untrusted and nothing in them was opened or run beyond reading: alchemy's `AGENTS.md`, `.hooks`, `.cargo` and `Makefile`; tmc-picori's `android/gradle/wrapper/gradle-wrapper.jar`, `build.py`, `AGENTS.md` and `agent.txt`; and goldensun_html5's `scripts/` and `electron/`.
- The background `du` size job from the clone command may still have been running when this reply was sent. It only reads, and the sizes above come from a separate count.