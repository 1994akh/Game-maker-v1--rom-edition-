# Route C: extend goldensun_html5, ship in a Capacitor WebView. The strongest honest case

**Verdict:** Route C gets you the Golden Sun half of the game almost finished. That is the harder, less documented half. Its Pokémon half can draw on Pokémon Showdown (MIT), which is already TypeScript, so both halves are in one language. Everything is text (TypeScript, JSON, Tiled maps), so Claude Code can build, test and package it from the command line. No NDK, C toolchain or engine editor is needed.

The costs are real:
- The engine sits on a frozen 2021 Phaser CE 2.19, inside a WebView.
- The 240×160 frame is tight for an 8-against-6 battle.
- Pokémon move effects must be rewritten, because the expansion's C battle engine is not reused.

Labels: VERIFIED means I read it this session (path or URL given). INFERRED means it is not proven. I only read the third-party clones; nothing in them was installed, built or run. "Route A" below means the C route on pokeemerald-expansion with a Picori-style SDL3 Android layer. "Route B" means a Godot 4 rewrite. Both are assumed from the task text.

---

## 1. Architecture: what comes from where

**Clone:** `C:\Users\aaron\Documents\UnboundHack\external\goldensun_html5` (commit b8b086d, 2026-01-24, MIT).

| Layer | Source | Reuse / change / write | Evidence |
|---|---|---|---|
| Free 8-way field movement, collision, dash | goldensun_html5 `ControllableChar.ts` (2,224 lines), `Hero.ts`, `Collision.ts` (P2 physics, round body of radius 7) | **Reuse**, then tune | VERIFIED: `Collision.ts:81` starts P2 physics; `magic_numbers.ts` has `HERO_BODY_RADIUS = 7.0`. NPC `walk_speed: 60` (`assets/dbs/npc_db.json`) is 1.0 px/frame at 60 fps, which matches our measured GS walk of 1.0 px/frame (`notes\gs_movement.md:19`). The units are INFERRED |
| **Field Psynergy** | `base/field_abilities/`: 14 files plus the `FieldAbilities.ts` base (760 lines) | **Reuse** | VERIFIED. DESIGN.md's whole proving set (Move, Frost, Growth, Reveal) is already there. Of the 23 group Psynergy in party-and-battle §7, 11 exist: Move, Pound, Frost, Douse, Growth, Lash, Reveal, Avoid, Whirlwind, Mind Read, Retreat. Lift and Sand exist as well |
| Puzzle objects | `interactable_objects/`: `Pushable.ts` (582), `RollingPillar.ts` (508), `RopeDock.ts` (440), `Breakable.ts`, `WhirlwindSource.ts` | **Reuse** | VERIFIED. `push_pillar` in `interactable_objects_db.json` has `psynergies_info: {move: infinite, whirlwind: once}` and `pushable: true`. The cave, forest and madra_corner maps already use it |
| Events and cutscenes | `base/game_events/`: 74 event types, written as JSON inside Tiled map properties | **Reuse** | VERIFIED. `madra.json` carries a `game_events` property with branch, timer and `main_chars_join_split` events |
| Golden Sun battle | `Battle.ts` (1,845 lines; phases START, MENU, ROUND_START, COMBAT, ROUND_END, FLEE, END), `BattleStage.ts` (724, rotating camera), `EnemyAI.ts` (365), `BattleAnimation.ts` (2,275), battle windows | **Reuse and change** | VERIFIED. `MAX_CHARS_IN_BATTLE = 4` is in `battle/BattleBase.ts:34`. It is used at `Battle.ts:226,1107,1123,1608`, `MainBattleMenu.ts:117,131,303`, `BattleStatusWindow.ts:391` and `BattleSummonWindow.ts:199`. `windows/CharsStatusWindow.ts:18` has its own `MAX_CHARS_NUMBER = 4` |
| **Set/Standby Pokémon and Summons** | `Djinn.ts` (status `SET`, `STANDBY`, `RECOVERY`), summon flow at `Battle.ts:1094-1131`, Djinn menus (`MainDjinnMenu.ts`, `windows/djinn/*`, `SummonDjinnStandbyWindow.ts`) | **Reuse and change** | VERIFIED. The design says Set Pokémon follow Golden Sun's Djinn model, and this code is that model. One change is needed: recovery here uses one static list (`Djinn.djinn_in_recover`, ticked at `Battle.ts:1609-1631`), but our rule is a countdown per Adept |
| Menus | `main_menus/`: Psynergy, Djinn, Item, Status, Inn, Healer, Shop, Save | **Reuse** | VERIFIED |
| World map | `Map.ts` Mode7 filter (`Map.ts:77,201`), world-map speed constants | **Reuse** | VERIFIED. There is no ship, sailing or swimming code (grep found nothing) |
| **Damage formulas** | **our** `C:\Users\aaron\Documents\UnboundHack\gbax\codecs\gs_battle.py` (531 lines; matched the game's own routines in 2,263 emulated calls) | **Port to TypeScript**, replacing `BattleFormulas.ts` | VERIFIED. The engine's version is approximate and uses floats. `BattleFormulas.ts:101-103` returns `power + this.power_multiplier(...)`, which adds the element factor (about 1.0) instead of multiplying by it. That is a bug |
| GS content: rooms, enemies, Psynergy, classes, Djinn, sprites | our extraction under `C:\Users\aaron\Documents\UnboundHack\games\AGSE-5c469520-Golden-Sun-USA-Europe\`: 201 rooms as Tiled 1.10.2 `.tmj`, `collision.json` per area, `data\*.json`, 161 enemy battle PNGs | **Write converters** (Python, saved as reusable gbax tools) | VERIFIED. The engine ships almost no content (10 maps, 8 enemies, 7 enemy parties), but its enemy fields match GS's (`turns`, `base_level`, `base_power`, `base_resist`, `vulnerabilities`) |
| Pokémon data | smogon/pokemon-showdown `data/`: `pokedex.ts` 538 KB, `moves.ts` 485 KB, `learnsets.ts` 3.7 MB, `typechart.ts`, `abilities.ts`, `items.ts`, `conditions.ts` | **Convert data**; move effects are re-expressed by us | VERIFIED via the GitHub API: language TypeScript, MIT, pushed 2026-10-13. The move effects are callbacks tied to Showdown's own `Battle` class (INFERRED), so only the data transfers cleanly |
| Pokémon sprites | `C:\Users\aaron\Documents\UnboundHack\external\pokeemerald-expansion\graphics\pokemon\`: 1,029 folders with front, back, icon and overworld PNGs | **Reuse** | VERIFIED |
| Catch formula, evolution rules | expansion C (local), used as a reference | **Port small pieces** | INFERRED that each is about 100–200 lines |
| Input | `XGamepad.ts` (516 lines): GBA buttons, controller buttons, engine buttons `PSY1-4`, `STICK_DASHING`, zoom and mute; remappable through `init_db`; stick dead zone 0.5 (`:359`) | **Reuse**; the touch overlay calls the public `on_gamepad_down` and `on_gamepad_up` (`:394`, `:415`) | VERIFIED. **There are no on-screen touch controls.** The only tap handler is double-tap for fullscreen at `GoldenSun.ts:482` |
| Save | `Snapshot.ts` (563 lines) saves by downloading a JSON file (`:538`, `:555`) | **Change** to `@capacitor/filesystem` save slots | VERIFIED |
| Android shell | Capacitor 8: Kotlin `MainActivity`, WebView, Gradle | **Write a thin layer**: posture bridge, optional controller bridge, 60 Hz cap | VERIFIED: [Capacitor docs](https://capacitorjs.com/docs/getting-started/environment-setup) and the [android-template manifest](https://raw.githubusercontent.com/ionic-team/capacitor/main/android-template/app/src/main/AndroidManifest.xml) |
| Brand-new systems | — | **Write** | Two crews, Adept + partner pairs, the revive window and Rouse, enemy trainers that mirror the crew, catching and storage, sailing, the 12 missing field Psynergy, Fold layouts |

**References for any route:** alchemy (GS1 decomp) for exact rules such as formation selection (`BATTLE5.C`) and Djinn bursts, and tmc for the corner nudge and puzzle-object patterns.

---

## 2. First playable slice on the Fold 7

**Slice contents:** free 8-way walking on one extracted GS1 room, a Move puzzle, a battle of 4 Adepts + 4 Pokémon against up to 6 GS monsters using exact GS formulas, and touch plus controller input.

Estimates are Claude working days, followed by your play-test.

| # | Work item | Kind | Est. |
|---|---|---|---|
| S1 | Fork into the project. Install Node 22. Check the npm scripts and install with `npm ci --ignore-scripts` (upstream's `postinstall` runs husky, and `engines` pins npm ^7). Remove Electron, `gtag.js` and the CodeMirror home page. Build with webpack. Add Vitest, plus a Playwright smoke test (boot, walk, screenshot) in headless Chromium or the installed Edge | change | 1–2 |
| S2 | Capacitor 8 shell: web folder = `dist` plus `assets`; immersive fullscreen; `android:appCategory="game"`. Turn off `disableVisibilityChange = true` (`GoldenSun.ts`, VERIFIED) and pause when the app is in the background, or it keeps running hidden. Cap at 60 Hz. Build the debug APK with `gradlew` and install with `adb`. **Milestone: the stock demo runs on the Fold 7** | write (small) | 1–2 |
| S3 | Touch overlay in HTML with pointer events: a floating stick split into 8 sectors on the left, A/B/L/R/Start/Select/PSY buttons, hidden while a controller is in use (Picori's `port_touch_controls.cpp` is the design reference). It feeds `XGamepad.on_gamepad_down/up` | write | 2–4 |
| S4 | Controllers: test the WebView Gamepad API with the Xbox pad (Bluetooth) and Backbone (USB-C). If it fails or misbehaves, add a Kotlin `dispatchKeyEvent`/`dispatchGenericMotionEvent` bridge to JS that also swallows B so it can't act as Back (INFERRED risk). Map buttons per CONTROLS.md §5d | reuse + write | 1–3 |
| S5 | Screens and posture: `androidx.window` 1.5.x `WindowInfoTracker` in Kotlin sends `{posture, foldRect}` to JS. Integer canvas scale per CONTROLS.md §0 item 5 (cover 4×/6×, inner 8×, tabletop 6× on the top half). Safe-area insets | write | 2–3 |
| S6 | **Map converter**: our `.tmj` plus `collision.json` (per-cell `shape` index, `height_shapes` with `heights_8px`, three layers) to the engine's format, which uses collision **polygons** in object layers `00`/`01`/`02` (VERIFIED in `madra.json`). Also entrances and a `maps_db` entry. `@turf/turf` is already a dependency for polygon union | write | 3–5 |
| S7 | Movement feel: check walk 1.0, run 1.5 and 0.25 acceleration against `notes\gs_movement.md` | tune | 1 |
| S8 | Move puzzle: place `push_pillar`, a target spot and a story flag with `game_events`. GS's own puzzle logic is Thumb code in `map_code.bin`, so it is rebuilt as data | reuse | 1–2 |
| S9 | Port `gs_battle.py` to TypeScript. Python writes the expected results and Vitest checks them. This removes the add-instead-of-multiply bug | port | 2–3 |
| S10 | Data import: GS1 enemies, abilities, classes, Djinn and Summons to the engine's databases. Pack the 161 enemy PNGs into atlases. Use the engine's existing Isaac/Garet/Ivan/Mia as placeholder Adepts | scripts | 3–4 |
| S11 | Partner Pokémon: `PartnerMon extends Player` (`Player.ts:151`, abstract, with a `fighter_types` enum). 4 species from Showdown, scaled to GS stats per party-and-battle §5. Damaging moves map to the engine's existing ability types (`BASE_DAMAGE`, `MULTIPLIER`) plus one status move. Front and back sprites come from expansion | write | 4–6 |
| S12 | **4+4 battle:** 4 Adept/partner pairs; ally layout with each pair adjacent so spread attacks hit neighbours; a status bar for 8; the partner menu (moves and defend; Rouse, item or pass in the revive window); "fights only while its Adept can", withdraw and close the line; the end-of-turn order from §3; AI targeting across 8; up to 6 enemies. Enemy layout already scales with `enemies_count` at 40 px spacing (`BattleStage.ts:488-491`), so 6 enemies fill exactly 240 px | change + write | 7–10 |
| S13 | Save slots through `@capacitor/filesystem` | change | 1 |
| S14 | Play-test and fix rounds | — | 5–8 |

**Total: about 34–54 Claude-days, which is roughly 6–10 calendar weeks; aim for about 8.**

Suggested calendar if the route is chosen this week. Per SCHEDULE.md, engine work is on hold until the extraction is done, so the dates move with that.

| Dates | Work | Milestone |
|---|---|---|
| Week 1 (14–20 Oct) | S1–S4 | The demo on your phone with touch, Xbox and Backbone |
| Week 2 | S5–S8 | The extracted GS room walkable, with the Move puzzle working |
| Week 3 | S9–S10 | A stock 4-Adept battle against extracted GS monsters with exact formulas |
| Weeks 4–5 | S11–S12 | The 4+4 battle |
| Week 6 | S13 plus fixes | Slice done around 24 Nov (late case mid-December) |

You can play-test most rounds without installing an APK: in Edge on the PC with the Xbox pad, or in Chrome on the phone through `adb reverse`.

---

## 3. The full game beyond the slice, and the biggest risks

Calendar weeks, AI-assisted (INFERRED):

| System | Weeks | Notes |
|---|---|---|
| Unleash, Standby and Summons on the Djinn code | 2–3 | Countdown per Adept, costs by matching type, class locked in battle |
| 18-type classes, long Psynergy lists, GS-style level-up text, Pokémon popup, evolution | 3–4 | Builds on `Classes.ts` |
| **Pokémon move, ability and item effects beyond plain damage** | **6–12** | Open-ended. Do them by roster priority |
| Catching, storage, restoration points, encounters | 4–6 | Catch formula ported from expansion |
| Two crews, handovers, shared bag, save format | 2–3 | |
| Enemy trainers that mirror the crew, and their AI | 2–4 | |
| The 12 missing field Psynergy plus backup items | 3–6 | Each follows the `FieldAbilities.ts` pattern |
| Surf, Dive, Waterfall, ship, sailing | 6–10 | The Mode7 world map exists; the ship does not |
| Content: about 200 GS1 rooms plus GS2 rooms | Main cost | Map conversion is scripted, but every room's events and puzzles must be rebuilt as JSON. This is true on every route |

Systems total about 30–50 weeks. **The whole game is about 12–18 months part-time**, which agrees with SCHEDULE.md's "full world 6–12+ months" for content alone.

**Biggest risks:**
1. **The Phaser base is frozen.** The repo bundles Phaser CE 2.19.0, built 2021-08-23 (VERIFIED in `static/phaser.js`). CE 2.20.x exists ([phaser.io](https://phaser.io/news/2024/10/phaser-ce-v2201-released)) and is community-maintained. **"Upgrading Phaser" only realistically means 2.19 to 2.20.x.** Phaser 3 or 4 has a different API and no P2 physics, so moving to it would touch nearly all of the about 64.7k lines, which amounts to a rewrite (INFERRED).
2. **We would own 64.7k lines of someone else's code.** It has no tests (VERIFIED), `strictNullChecks` and `noImplicitAny` are off (VERIFIED in `tsconfig.json`), and it has one main maintainer.
3. **The 240×160 frame.** 8 allies plus 6 enemies plus a status bar for 8 is cramped. Widening the view means auditing 75 uses of `GAME_WIDTH`/`GAME_HEIGHT` across 24 files (VERIFIED count).
4. **Collision model mismatch.** GS uses heights per tile; the engine uses polygons on separate layers. How good the converter is decides how walking feels.
5. **Controllers in the Android WebView are unverified.** I found no source confirming the Gamepad API works there. The native bridge (S4) is the fallback.
6. **Pokémon move-effect breadth**, as listed in the table above.

---

## 4. How well Claude Code can work in it on this PC

**What is installed now (VERIFIED):**
- Present: git 2.55, Python 3.13, winget 1.29, Edge. 31 GB RAM and about 136 GB free on C:.
- Missing: Node, npm, Java, adb, Gradle and the Android SDK. Chrome is not installed.

**What to install** (Claude can run winget with your approval):
- **Node 22 LTS.** Capacitor 8 needs Node 22 or later (VERIFIED, Capacitor docs).
- **Android Studio 2025.2.1 or later.** Capacitor 8's minimum. It brings the JDK, so none is installed separately. Add SDK Platform 36 (Android 16) plus build tools.
- **No NDK, CMake, Godot export templates or C toolchain.** Fewer installs than either other route.

**Command-line loop** (INFERRED for exact commands):
- `npm run build`, `tsc --noEmit`, Vitest for formulas and rules, Playwright for headless boot and screenshot tests.
- `npx cap sync android`, then `android\gradlew.bat assembleDebug`, then `adb install -r app-debug.apk`.
- Desktop Edge/Chrome DevTools can attach to the debug WebView on the phone (`edge://inspect`).
- Battle rules can be tested headless against the Python reference. No other route gets that test oracle in the same language as the game.

**Getting the APK onto the Fold 7:**
1. On the phone: Settings > About phone > tap Build number 7 times, then turn on USB debugging (or Wireless debugging and pair once with `adb pair`). Accept the RSA prompt.
2. Claude then installs each build with `adb install -r`.
3. Without a cable, copy the APK through OneDrive and tap it, after allowing "Install unknown apps".
4. Also turn on "Continue apps on cover screen" for the app (CONTROLS.md §1).

---

## 5. Fold 7 specifics

- **Switching screens:** Capacitor's template activity already declares `configChanges` including `screenSize|smallestScreenSize|screenLayout|density|orientation`, with `launchMode="singleTask"` (VERIFIED). Folding and unfolding resizes the WebView instead of restarting it, so game state survives. JS re-runs the integer scaling on `resize`. Add `appCategory="game"` and don't lock orientation (Android 16 rule, VERIFIED in the folder findings).
- **Tabletop:** don't rely on the web Device Posture API. It was an origin trial in Chrome 125–128 and support in WebView is unconfirmed ([Chrome blog](https://developer.chrome.com/blog/foldable-apis-ot)). Instead, the Kotlin host sends the posture from `androidx.window` 1.5.1. Battle goes on the top half, with commands and touch controls on the bottom.
- **Controllers:** XGamepad already has Xbox-style names and remapping. The PSY1–4 engine buttons fit CONTROLS.md's semantic actions. Stick input becomes 8-way digital, which is exactly GS's 8 directions.
- **Performance:** a 240×160 WebGL game on a Snapdragon 8 Elite has a large margin. The risks are JS garbage-collection pauses and the P2 solver with many bodies (INFERRED).
- **Battery:** this is the real cost. A WebView adds renderer and GPU processes, and requestAnimationFrame follows the 120 Hz panel. Ask the window for 60 Hz and stop the game loop in the background. Still expect higher drain than a native SDL build; it has not been measured.

---

## 6. Honest weaknesses against the other two routes

**Against Route A (C on pokeemerald-expansion with an SDL3 layer):**
- Route C gives up the expansion's working Gen 1–9 move, ability and item effects, plus its catching, Pokédex and overworld-encounter code. These are rewritten in TypeScript (Showdown gives data only).
- It gives up native speed, battery life, lower input latency, and the Android APK pipeline that Picori has proven.
- It gives up possible native m4a playback of GS music.

**Against Route B (Godot 4):**
- Godot is an actively maintained engine with a first-class Android export, native controller input, tilemaps with custom data, a profiler and an editor you could use yourself.
- Route C rests on a 2021 Phaser build and a community fork, runs single-threaded JS, and needs a Kotlin/JS bridge for posture and possibly controllers.

**Specific to Route C:**
- Two runtimes to debug (Kotlin and JS).
- A fixed GBA-sized frame.
- Loose typing and no upstream tests.
- Dependence on one maintainer's design choices, such as polygon collision and the global Djinn recovery list.

**Where it still wins:**
- It is the only route where a working GS field engine and the Pokémon rules data are both MIT TypeScript.
- It starts furthest ahead on the side that has the least documentation: 11 of 23 field Psynergy, puzzle objects, 74 event types, Djinn and Summon battles, and GS menus.
- It has the fastest edit-and-play loop, and it needs the fewest installs on this PC.

Sources:
- https://github.com/jjppof/goldensun_html5 (clone at `C:\Users\aaron\Documents\UnboundHack\external\goldensun_html5`)
- https://github.com/smogon/pokemon-showdown (GitHub API `/contents/data`)
- https://capacitorjs.com/docs/getting-started/environment-setup
- https://raw.githubusercontent.com/ionic-team/capacitor/main/android-template/app/src/main/AndroidManifest.xml
- https://phaser.io/news/2024/10/phaser-ce-v2201-released
- https://developer.chrome.com/blog/foldable-apis-ot
- https://developer.mozilla.org/en-US/docs/Web/API/Navigator/getGamepads
- Local: `docs/engine/gba-sources.md`, `C:\Users\aaron\Documents\Game-maker-v1\docs\design\party-and-battle.md`, `C:\Users\aaron\Documents\Game-maker-v1\docs\phase1\CONTROLS.md`, `C:\Users\aaron\Documents\Game-maker-v1\docs\phase1\SCHEDULE.md`, `C:\Users\aaron\Documents\UnboundHack\notes\gs_movement.md`, `C:\Users\aaron\Documents\UnboundHack\notes\gs_field_psynergy.md`, `C:\Users\aaron\Documents\UnboundHack\gbax\codecs\gs_battle.py`