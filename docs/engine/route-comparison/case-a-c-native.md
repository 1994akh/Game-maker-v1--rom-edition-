# Route A (C/C++ native): the strongest honest case

The other two routes are assumed to be **B: Godot 4** and **C: a TypeScript/WebView app built on goldensun_html5**. The folder findings name these as the three ways to wire in fold support. INFERRED.

## 0. Bottom line

- **The strongest version of Route A builds a new native engine and uses pokeemerald-expansion as a library.** It does not run expansion as the game. The other variant runs expansion on a fake GBA, the way Picori, hirata and NTx86 do. That variant is ruled out for the main line, for four VERIFIED reasons:
  - **4-battler limit.** Expansion's battle engine is hard-wired to 4 battlers. `include/constants/battle.h:59-76` defines 4 positions and `B_BATTLER_0..3`, so `MAX_BATTLERS_COUNT` is 4.
  - **Grid maps.** Its field engine is built on a tile grid of metatiles.
  - **Fixed GBA screen memory.** Picori's renderer keeps the GBA's fixed video memory: `gVram[0x18000]` (96 KB) and a 1 KB OAM in `port/port_gba_mem.h`. That blocks the planned graphics remake.
  - **32-bit pointers.** Expansion has about 265k lines of `.s`/`.inc` script data that store pointers as `.4byte` (`asm/macros/battle_script.inc:12`). That clashes with arm64's 8-byte pointers.
- **What Route A uniquely gives:**
  - Expansion's Pokémon data and pure rule functions compile directly. The data is about 123k lines in the moves and species tables, with 935 moves (VERIFIED).
  - Golden Sun logic can be ported line by line from the same language: alchemy's GS1 is about 220k lines of C (VERIFIED).
  - Picori is a proven SDL3 → Android APK shell with touch, gamepad and m4a audio (VERIFIED).
  - Fixed-point maths makes battles reproducible, and the core can be tested headless in seconds.
- **What it costs:** you write everything an engine normally gives you, including menus, the renderer, the event system and save. It is also the slowest of the three routes to a playable Golden Sun-feel slice.
- **Slice estimate:** 57–83 working days of work, about 10–14 weeks of calendar time with overlap. If work starts Mon 20 Oct 2026, the slice lands between late Dec 2026 and late Jan 2027. Confidence is about 50%.

## 1. Architecture: where each part comes from

Core rules are written in C17, so expansion's data and the ported decomp code drop straight in. The platform shell, renderer and UI are C++20.

| Layer | Source | Reused or written |
|---|---|---|
| Android shell, main loop, input, lifecycle | Picori `port/` and `android/` (VERIFIED): `port_main.c` (945 lines), `port_touch_controls.cpp` (800), `port_analog_movement.c` (91), `port_save.c` (811), and the Gradle project with SDL3's Java glue. SDL3 is pinned at 3.4.12 there; latest is 3.4.18 (2026-10-02) | **Adapt** (GPL-3.0). **Write:** the fold/posture bridge (`androidx.window` 1.5.x; nxemu/butterfly pattern); a viewport size chosen at runtime (Picori's `port_widescreen.h` is fixed at build time); portrait layouts (Picori is `sensorLandscape`, `AndroidManifest.xml:26`); `appCategory="game"`; the back-gesture callback |
| Renderer | — | **Write:** an SDL3 sprite batch. The exported GS maps are already PNG layers per area (`layer0..2.png`, `composite.png`; VERIFIED), so the slice draws textures and y-sorted sprites. Picori's PPU is not used |
| Free movement and collision | `notes/gs_movement.md` gives exact GS numbers (VERIFIED): 16.16 position, walk 1.0 and run 1.5 px/frame, acceleration 0.25, facing turns at most 22.5° per frame, slide by trying ±22.5°, ±45° and ±67.5°. tmc gives the structure (VERIFIED): hitbox probing, corner nudge, entity state machines, update priorities | **Write**, following the spec. GS height shapes: 16 functions at `0x08011CE0–0x08011F48`, of which 5 are identified. I did not find them in alchemy by name, so port them from the ROM or decomp code (open item) |
| Maps | Our export: GS1 has 201 rooms on 186 areas, GS2 has 325 rooms; each has `.tmj`, `collision.json` and `events.json` (VERIFIED) | **Reuse.** Edit in Tiled |
| Field Psynergy | `notes/gs_field_psynergy.md` (Move is fully specified in §7, VERIFIED); alchemy `FIELD/COMMON/{EFFECT,OBJECT,MAP}`, `TILEACT.C` and 84 per-map folders; tmc `pushableStatue.c` cell-stamping pattern | **Write**, porting by reading. alchemy's C is low-level: `PUSH_AHEAD.C` reads `(u8 *)gEventWork + 0x14`. It gives exact behaviour, but it can't be pasted in |
| Battle core (14 slots) | `gbax/codecs/gs_battle.py` (531 lines; core formulas matched 2,263 emulated calls); alchemy GS1 `SRC/BATTLE` (174 files) for turn flow, targeting, formations (380 records), AI and rewards | **Write in C.** The Python file serves as the test oracle |
| Pokémon rules | Expansion (VERIFIED): `src/data/moves_info.h`, `species_info/*`, learnsets, evolutions, exp tables, `item_effects.h`; pure functions `CalculateMonStats` (`pokemon.c:1375`), `GetEvolutionTargetSpecies` (`:4405`), `CalcTypeEffectivenessMultiplier` (`battle_util.c:8366`) | **Compile as-is** behind a header shim that stubs graphics pointers and GBA attributes (INFERRED: 1–3 days). **Move effects are re-implemented** in our core: expansion's script VM can't hold 14 units. Expansion's battle scripts and its 5,417 passing tests (`~/expansion_check.log`) are the spec |
| Events and scripts | alchemy per-map C as the readable source of GS map behaviour (`map_code.bin` is Thumb code) | **Write** a small data-driven event runner |
| Save | Picori `port_save.c` (file handling only) | **Write** the two-crew format |
| Audio (late) | Picori `port_m4a_backend.cpp` (1,101 lines) plus agbplay | **Reuse.** GS1 uses m4a (VERIFIED), so native playback of GS1 songs is likely (INFERRED). MIDI+SF2 is the fallback |
| Placeholder art | Expansion PNGs: front, back, overworld and icon in 1,029 species folders; extracted GS battle sprites (both VERIFIED) | **Reuse** |

**The biggest reusable pieces:**
1. **Our own extraction** (maps, data, formulas). It works on every route.
2. **Expansion's data and pure functions.** These compile directly in C; the other routes would convert them.
3. **The Picori shell.**
4. **alchemy's GS1 code.** Exact integer maths, but it has to be re-written by reading.
5. **tmc** for the movement, entity and puzzle structure.

## 2. First playable slice on the Fold 7

| # | Work item | Days |
|---|---|---|
| S1 | CMake skeleton with desktop, Android and headless-test targets; saved build/test/deploy scripts; first APK on the Fold showing touch and Xbox input | 4–6 |
| S2 | Shell from Picori: floating joystick, gamepad, fixed 60 Hz tick, save on background, runtime viewport, posture bridge over JNI | 5–8 |
| S3 | Bake one GS1 room that has a Move target (layers, collision, heights, events) plus a placeholder hero | 3–4 |
| S4 | Renderer and camera: layers, y-sort, priority, integer scale per posture | 3–5 |
| S5 | Free 8-way and analog movement, run, slide, heights, tuned to the GS numbers; input-replay tests; 2–3 play-test rounds | 8–12 |
| S6 | Move: request from menu or shortcut, range-32 targeting, 16 px per push, cell occupancy, flag, PP cost, reset on re-entry | 5–7 |
| S7 | Headless battle core: GS formulas with differential tests against `gs_battle.py`; turn order, spread, status and crits; 4+4 line with gap closing; revive window and Rouse; GS formations from `encounters.json` groups; enemy AI priorities; partner stat conversion (party-and-battle §5); a handful of move effects; EXP and coins | 15–20 |
| S8 | Battle scene and UI: 8 fighters against up to 6; touch and pad commands for 8 actors, with Auto and repeat-last-turn; targeting; damage numbers and messages; minimal level-up screens | 10–15 |
| S9 | Field-to-battle glue, minimal save, CONTROLS.md §9 acceptance tests on the device, power and performance check | 4–6 |

**Total: 57–83 working days.** S7 runs headless while you are play-testing S5 and S6, so the calendar is about 10–14 weeks.

**Milestones, if work starts 20 Oct:**

| Milestone | Week | Date |
|---|---|---|
| M0: APK and input on the Fold | 1–2 | about 31 Oct |
| M1: walking a GS room on the phone | 4 | about 14 Nov |
| M2: Move puzzle solved | 6 | about 28 Nov |
| M3: battle core passes its differential tests | 8 | about 12 Dec |
| M4: full slice | 10–14 | 29 Dec – 26 Jan |

**Caveat:** SCHEDULE.md currently holds the engine track until the GS extraction is done, so start = go-ahead.

**What you'd need to do:**
- Decide how Pokémon move power maps onto GS damage formulas. This is unspecified.
- Pick the GS1 room.
- Play-test for about 30–60 minutes per milestone.

## 3. Full game beyond the slice

| Area | Estimate (INFERRED, low confidence) |
|---|---|
| UI framework and all menus: Set and party screen, long Psynergy lists, bag, equipment, storage, Pokédex, summary, evolution, shops and restoration points, settings and remapping, a layout per posture | 10–16 weeks |
| Full battle: all GS Psynergy, Unleash/Standby/Summons, mirrored enemy trainers, catching, a curated set of Pokémon move and ability effects, items, animations | 14–22 weeks |
| Field: GS1 field Psynergy from spec; Lost Age Psynergy written from scratch (GS2 is 4.7% decompiled); NPCs and cutscenes; Surf, Dive and Waterfall; ship and world map; Djinn-style encounters | 14–22 weeks |
| Two crews, handovers, save | 3–5 weeks |
| **Engine total after the slice** | **about 9.5–15 months** |
| Content: 250–350 maps (WORLD_PROPOSAL.md:375), story missions, 57 Weyard species, trainers | The long pole, about the same on every route |

**Overall: about 2–3 years** to a finished game. Confidence is low.

**Biggest risks:**
1. **No UI toolkit in C.** Mitigation: build one small retained-mode widget layer early.
2. **"Reuse expansion's move effects" is overstated.** Effects are re-implemented, not linked.
3. **alchemy's names and offsets may be wrong**, and GS2 isn't decompiled yet.
4. **Native crashes on device are harder to debug.** Mitigation: a desktop build of the same code, HWASan builds, `ndk-stack`.
5. **Everything is bespoke**, so only Claude Code can realistically change the engine. You'd edit maps in Tiled and data in JSON.
6. **GPL and no-licence code.** Fine for personal use; the app can never be shared.

## 4. How well Claude Code can work in it on this PC

**What's on the PC now (VERIFIED by command checks):**
- **WSL Ubuntu:** gcc 15.2.0, arm-none-eabi-gcc and make; 16 cores, 15 GB RAM, 949 GB free.
- **Windows:** Python 3.13 and Git.
- **Missing:** cmake, ninja, a JDK, the Android SDK/NDK, and adb.

**Strengths:**
- Builds are command-line only, and the core tests run headless in WSL in seconds.
- Recorded input can be replayed for regression tests, as tmc does with its player macros.
- Screenshots: frames dumped to PNG on desktop, and `adb exec-out screencap -p` on the phone.
- `adb logcat` for device logs, and `adb shell input` for scripted taps.
- All assets are text or PNG.

**Weaknesses:**
- Claude Code can't judge how the game feels to play.
- GPU driver quirks.
- Gradle version churn: AGP 9.4 needs Gradle 9.6 and JDK 17+, and supports up to API 37 (VERIFIED).

**What you install:**
- **Android Studio.** It brings a JDK and the SDK manager. Through it, add:
  - SDK Platform 36 and Build-Tools
  - Platform-Tools (adb)
  - NDK r30 (`30.0.16248370`, VERIFIED latest LTS)
  - CMake
- **In WSL:** `sudo apt install cmake ninja-build` (Claude Code can run this with your approval).
- **Tiled.**
- **Not needed for this route:** Godot export templates and Node.

**Installing the APK on the Fold 7:**
1. Turn on Developer options (tap Build number 7 times).
2. Turn on Wireless debugging and run `adb pair` once, or use USB debugging.
3. Turn off Samsung **Auto Blocker** (Settings > Security and privacy). It blocks sideloading and USB commands and is reported on by default since the Fold 6; not checked on your phone.
4. Claude runs `adb install -r app-debug.apk`.

Keep one debug keystore throughout: an APK signed with a different key can't update the installed app. The alternative is to copy the APK to the phone and allow "Install unknown apps" for the file manager.

## 5. Fold 7 specifics

- **Screen switching:** one Activity with `configChanges` set (screenSize, smallestScreenSize, screenLayout, orientation and others). SDL3 sends a resize event and the C layout code recomputes. Turn on "Continue apps on cover screen" for the app.
- **Orientation:** with targetSdk 36, Android ignores orientation locks on screens 600 dp and wider unless the app declares `android:appCategory="game"`, so declare it (VERIFIED, Android docs).
- **Posture:** `WindowInfoTracker` in the Java `SDLActivity` subclass reads the posture and passes `{state, orientation, hinge rect}` to C in one JNI call.
  - **Tabletop:** field or battle in the top half; commands and controls in the bottom half, outside the hinge band.
  - **Book:** field on one side, party or menu on the other.
- **Viewport:** a world view sized at runtime. Examples: about 373×160 logical pixels on the 21:9 cover screen and about 240×216 on the inner screen, at integer scale (INFERRED).
- **Controllers:** SDL3's gamepad API handles hot-plug for Xbox over Bluetooth and the Backbone. The Backbone works only with the phone folded; unfolded or tabletop play needs Bluetooth. Picori already hides the touch overlay while a gamepad is in use (VERIFIED).
- **Performance and battery:** a native 2D game is a light load for the Snapdragon 8 Elite (INFERRED). Cap at 60 Hz with `setFrameRate`, and skip redraws when nothing changes in menus. Measure with Android Studio's Power Profiler; I have no figures yet.
- **Build:** arm64-v8a only. Whether the 8 Elite can run 32-bit code at all is unverified.
- **Back gesture:** with targetSdk 36, register `OnBackInvokedCallback` and make it open the pause menu.

## 6. Honest weaknesses against the other two routes

- **Against Godot:** Godot gives tilemaps, a UI system, animation, audio, save helpers and Android export for free. Route A writes all of these, and menus alone are 10–16 weeks. Godot also lets you edit scenes yourself.
- **Against TypeScript/WebView:** goldensun_html5 (MIT) already runs a GS-style engine (VERIFIED): 14 field Psynergy, pushable objects, 74 event types, battle with Djinn and Summons, and Tiled maps. A slice there could be 1.5–3× faster (INFERRED). Route A wins on latency, battery, controller handling and fold control.
- **Reuse is smaller than the route description implies:**
  - Expansion contributes data and pure functions, not its battle engine.
  - Picori contributes its shell, not its renderer.
  - alchemy contributes exact behaviour, not code you can paste.
- **The most code to own and the highest engineering risk.** The payoff is determinism, exact GS maths, no engine lock-in, and a small native APK.

## Sources

**Local:**
- `docs/engine/gba-sources.md`
- `C:\Users\aaron\Documents\Game-maker-v1\docs\design\party-and-battle.md`
- `C:\Users\aaron\Documents\Game-maker-v1\docs\phase1\{CODEBASE,CONTROLS,SCHEDULE,MOVEMENT,WORLD_PROPOSAL}.md`
- `C:\Users\aaron\Documents\UnboundHack\notes\{gs_movement,gs_maps,gs_field_psynergy}.md`
- `C:\Users\aaron\Documents\UnboundHack\gbax\codecs\gs_battle.py`
- `C:\Users\aaron\Documents\UnboundHack\games\AGSE-5c469520-Golden-Sun-USA-Europe\{maps,data,battle_sprites}`
- `C:\Users\aaron\Documents\UnboundHack\external\{alchemy,tmc-picori}`
- WSL: `~/pokeemerald-expansion` (HEAD 8fb02c6f) and `~/expansion_check.log`

**Web:**
- https://api.github.com/repos/hirata-producoes/pokemon-regionalidades/contents/src/platform — 15 files, including `sdl2.c` (97 KB), `bios.c` and `dma.c`
- https://api.github.com/repos/libsdl-org/SDL/releases/latest
- https://developer.android.com/ndk/downloads
- https://developer.android.com/build/releases/gradle-plugin
- [9to5google: Samsung Auto Blocker and sideloading](https://9to5google.com/2024/07/23/samsung-galaxy-sideloading-android-apps/)
- [TechRadar: Auto Blocker](https://www.techradar.com/phones/your-samsung-galaxy-phone-is-getting-a-big-security-update-heres-how-to-use-it)
- [Android Authority: One UI 8.5 Auto Blocker](https://www.androidauthority.com/one-ui-8-5-auto-blocker-auto-turn-on-apk-teardown-3599873)
- [Qualcomm: Snapdragon 8 Elite](https://www.qualcomm.com/products/mobile/snapdragon/smartphones/snapdragon-8-series-mobile-platforms/snapdragon-8-elite-mobile-platform) — 32-bit support not confirmed