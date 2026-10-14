# Engine route verdict: Golden Sun + Pokémon native app for the Galaxy Z Fold 7

**Recommendation: Route B, Godot 4.7.2 with typed GDScript, run as a hybrid.** goldensun_html5 contributes logic and design, ported under its MIT licence; nothing in it is run. `gs_battle.py` serves as the test oracle. Pokémon data comes in through Python converters. Godot wins because it is the only route that scores well on all six criteria. Route C is fast at first but builds up debt. Route A gives the best phone build but takes 2–3× longer to reach a playable slice.

## 1. Scores (1–10; for Risk, 10 = safest)

| Criterion | A: C/C++ native (SDL3) | B: Godot 4.7.2 | C: html5 in a WebView |
|---|---|---|---|
| Work saved | 4 | 7 | 8 |
| Fit with the agreed design | 8 | 8 | 5 |
| Fold 7 quality | 9 | 7 | 4 |
| Claude Code productivity on this PC | 6 | 7 | 8 |
| Maintainability and the later graphics/music passes | 5 | 9 | 3 |
| Risk | 3 | 7 | 4 |
| **Total (unweighted)** | **35** | **46** | **32** |
| Advocate's estimate to the slice | 10–14 wk (~50%) | 4–6 wk | 6–10 wk |
| My adjusted estimate | 11–15 wk | **6–8 wk** | 8–12 wk |

**Route A, C/C++ native**
- **Strengths:** best latency, battery and fold control; deterministic tests that run without a screen. Free movement, the 8-vs-6 battle and crews are all unconstrained.
- **Weaknesses:**
  - The reuse is thinner than it sounds. Pokémon move effects get rewritten anyway, because expansion's battle engine is fixed at 4 battlers (VERIFIED: the `BattlerId` enum in `include/constants/battle.h`).
  - There is no UI toolkit in C, and menus alone are sized at 10–16 weeks.
  - Only Claude could realistically change the engine.
  - It needs the most missing tools installed: NDK, cmake and ninja.

**Route B, Godot**
- **Strengths:** the engine supplies rendering, input, audio, save, UI and the Android export. There are no GBA limits on the battle, the views or the graphics remake.
- **Costs:**
  - Every Pokémon rule is rewritten and needs its own tests.
  - Reading fold posture needs a small Kotlin plugin plus a Gradle-based export.
  - Claude must avoid workflows that only work inside the editor.

**Route C, html5 in a WebView**
- **Strengths:** it has the most finished Golden Sun field and battle logic, and the fastest edit-and-play loop.
- **Weaknesses:**
  - Its foundations fight the design: a battle side capped at 4 characters, a fixed 240×160 screen, and polygon collision instead of Golden Sun's height grid.
  - The base is frozen: Phaser CE 2.19 from 2021, 64.7k lines of loosely typed code with no tests.
  - Whether controllers work in the Android WebView is unverified.
  - Battery cost is the highest of the three.

## 2. The recommendation in detail

- **Engine:** Godot 4.7.2 (VERIFIED: release tag 4.7.2-stable, published 2026-08-18). Pin this version.
- **Golden Sun behaviour:** port the design, and code where useful, from html5's `FieldAbilities.ts`, `MoveFieldPsynergy.ts`, `Pushable.ts`, its 74 event types, its battle phases and its Djinn/Summon flow. MIT allows copying; keep the notice.
- **Not taken from html5:** its collision (P2 polygons) and its formulas. Its `BattleFormulas.ts` adds the element factor where Golden Sun multiplies by it.
- **Formulas:** port `gs_battle.py` to GDScript. Python generates JSON test vectors, so the port is checked call for call.
- **Collision:** a custom mover on our cell grid (`collision.json`) using the numbers in `notes\gs_movement.md`. tmc's corner nudge is added as polish.
- **Pokémon data:** a Python converter from expansion headers or Showdown (Claude's call). Effects are re-expressed on Golden Sun formulas as a curated set.
- **Rejected sub-hybrid:** a C battle core inside Godot through GDExtension. It doubles the toolchains and gains nothing, because the formula code is small.
- **Fallback trigger:** the Week-1 device gate below. If folding and unfolding, or the controllers, can't be made to work in Godot within about 2 days, reconsider Route A's SDL3 shell.

## 3. What you must decide or do

**Decisions**
1. **Choose the route.** This also lifts decision #2 ("code base on hold", `docs\phase1\README.md:81`).
   - `SCHEDULE.md` and `CODEBASE.md` still describe the expansion engine track and will need rewriting.
   - `DESIGN.md` still says no Golden Sun decomp exists.
2. **Name the new private engine repo** (decision #6).
3. **Accept the slice contents:**
   - GS1 room 12 (Sol Sanctum, Move puzzle);
   - placeholder Isaac/Garet/Ivan/Mia sprites;
   - 4 placeholder partner species;
   - a provisional rule for how a Pokémon move's power maps onto Golden Sun damage. This is unspecified today. My proposal is to treat a damaging move as base-damage Psynergy, power = move power × k, with tuning later.

**Installs (I script them in `tools\setup_android.ps1` once you approve; about 3 GB)**
- `Godot_v4.7.2-stable_win64.exe.zip` (86.0 MB) and `Godot_v4.7.2-stable_export_templates.tpz` (1,281.3 MB). Sizes VERIFIED from the GitHub API; hashes checked against `SHA512-SUMS.txt`.
- Temurin JDK 17.
- Android cmdline-tools, platform-tools (adb), build-tools and `platforms;android-36`. Android Studio works instead if you prefer a GUI.
- The GUT test add-on, copied into the project.
- Optional: scrcpy (shows the phone screen on the PC), and Tiled if you want to look at maps yourself.
- Not needed: NDK, Node, .NET SDK. The NDK is probably unused for a plain export (INFERRED).

**Phone setup (about 1 hour, once)**
- Turn on Developer options (tap Build number 7 times), then Wireless debugging, and pair once. USB debugging also works.
- Check that Samsung Auto Blocker isn't blocking USB commands or sideloading.
- Turn on "Continue apps on cover screen" for the app.
- Keep one signing key throughout and back it up. An APK signed with a different key can't update the installed app or keep its saves.

**Play-tests:** about 30–60 minutes every 2–3 working days.

## 4. First two weeks

Week 1 starts the day after you give the go-ahead; the dates below assume Monday 19 October.

| Day | Work | Check |
|---|---|---|
| 1 | Run the installs. Create the repo and project skeleton: autoloads `Db`, `GameState`, `Save`, `InputRouter`, plus GUT. Export a hello-world APK from the command line and install it with adb. | **Gate 0 on the device:** folding and unfolding resizes the app without a restart or black screen; Xbox and Backbone show up as joypads; multi-touch works. Godot's template manifest defaults to `screenOrientation="landscape"` and `resizeableActivity="false"` (VERIFIED), so this also proves the project settings override them. |
| 2 | `tools\export_godot.py`: `room_012.tmj` plus the area's `collision.json`, tileset and PNG layers → `.tscn`, with actors and entrances. Resolve the actor-id offset (about half a day). | Desktop screenshot matches `composite.png`. |
| 3–4 | `GsMover`: walk 1.0 and run 1.5 px/frame, acceleration 0.25, facing turns up to 22.5° per frame, five-ray probe, slide at ±22.5°/45°/67.5°, the 3 layers, the 5 known height shapes, y-sort, camera, fixed 60 Hz tick. | GUT replay of `walk_log.csv` passes within tolerance. |
| 5 | `InputRouter` with the semantic actions from `CONTROLS.md`. Touch overlay: floating stick plus A/B/L/R/Menu/PSY buttons, hidden while a pad is in use. Integer scaling per screen. | **Play-test 1:** walking feel on the cover and inner screens, with touch, Xbox and Backbone. |
| 6 | Fixes from play-test 1. Re-layout on `size_changed`, 60 fps cap, immersive mode. | — |
| 7–8 | Move Psynergy as specified in `gs_field_psynergy.md` §7: hand object, 4 directions only, cells checked 16 and 32 px ahead, 0.2 px/frame slide, 15-frame wait, flag set. Pushable cell stamping. Room re-entry keeps the puzzle solved. Minimal JSON save. | GUT tests, then **play-test 2:** the Move puzzle on the phone. |
| 9–10 | `gen_formula_vectors.py` and `GsFormulas.gd`. Unit model (Adept + partner, with the §5 HP clamp), turn order, enemy action priorities, one encounter group from `encounters.json`. Also a mock-up of the cover-screen layout for an 8-vs-6 battle. | Formula vectors pass. A headless 4+4-vs-N battle runs to the end. |

**End of week 2:** you can walk room 12 on the Fold and solve the Move puzzle by touch or controller. The battle core passes its formula checks without a screen.

**Weeks 3–6 to the slice:**
- revive window, Rouse, withdraw and close-the-line, spread hitting neighbours, EXP;
- the battle screen for each posture, with touch and controller commands for 8 actors, plus Auto and repeat-last-turn;
- field-to-battle glue;
- the Pokémon-style level-up popup and Golden Sun level-up text;
- stretch goal: the tabletop posture plugin.

The slice should land around late November to mid-December.

## 5. Candid uncertainties

**Re-checked this session (VERIFIED)**

html5:
- `MAX_CHARS_IN_BATTLE = 4` (`base\battle\BattleBase.ts:34`) and `MAX_CHARS_NUMBER = 4` (`base\windows\CharsStatusWindow.ts:18`).
- The formula bug: `psynergy_damage` returns `power + power_multiplier`, while `gs_battle.py` `psy_core` computes power × (1 + diff/200).
- Phaser CE v2.19.0, built 2021-08-23.
- `strictNullChecks` and `noImplicitAny` are off; there is no test setup; about 64.7k lines.
- The `postinstall` script runs husky, and `engines` pins npm ^7.
- `disableVisibilityChange = true` at `base\GoldenSun.ts:198`.
- Screen-size constants: I count 90 uses in 24 files, against the advocate's 75. Probably a different counting method; same conclusion.

Our files and the reference repos:
- Our exported `room_012.tmj`: Tiled 1.10.2, 51×33 tiles, 3 tile layers, 23 tile events, 8 entrances, 13 actors. The advocate's figure of "29 events" probably counts `events.json`.
- GS2 has 325 exported rooms; `gs_battle.py` is 531 lines.
- Picori uses `sensorLandscape` and a view width set at build time.
- Godot's template manifest has `appCategory="game"` and `configChanges` including screenSize, smallestScreenSize, density, screenLayout and orientation.

**Not verified**
- Godot's behaviour when folding and unfolding a Fold 7. I found no reports either way, which is why Gate 0 exists.
- Whether the Android WebView supports the Gamepad API. No source found; this is Route C's risk.
- That GUT works with 4.7.2.
- Whether the posture plugin forces the Gradle export, or whether Godot's `JavaClassWrapper` could avoid it (INFERRED).
- Auto Blocker's state on your phone.

**Inherited from our notes and not re-run**
- The "2,263 emulated calls" match for `gs_battle.py`.
- The 6-enemy cap (strongly inferred from array sizes, not proven).
- Only 5 of the 16 Golden Sun height shapes are identified. This limits how faithful collision is on every route.

**Estimates:** all the timelines come from each route's own advocate. I added buffer to B and C for the cover-screen battle UI and the collision work, which neither priced.

**Biggest design risk on any route:** whether 14 fighters plus a command menu are readable on the 21:9 cover screen. That is why the layout mock-up is in week 2.

Sources:
- [Godot 4.7.2-stable release (GitHub API)](https://api.github.com/repos/godotengine/godot/releases/tags/4.7.2-stable)
- [Godot 4.7.2 Android template manifest](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/platform/android/java/app/src/main/AndroidManifest.xml)
- [MDN: Navigator.getGamepads()](https://developer.mozilla.org/docs/Web/API/Gamepad)
- [web.dev: Gamepad API](https://web.dev/gamepad?authuser=6)
- [GodotAndroidFoldableScreen plugin](https://lunatik-games.itch.io/godot-android-foldable-screen)
- [Godot forum: Android embedding and black bars](https://forum.godotengine.org/t/godot-android-embedding-shows-black-bars-in-horizontal-split-screen-how-to-fully-fill-the-area/113637)

Local files read: `docs/engine/gba-sources.md`, `C:\Users\aaron\Documents\Game-maker-v1\docs\design\party-and-battle.md`, `C:\Users\aaron\Documents\Game-maker-v1\docs\phase1\{README,SCHEDULE,CONTROLS}.md`, `C:\Users\aaron\Documents\UnboundHack\gbax\codecs\gs_battle.py`, `C:\Users\aaron\Documents\UnboundHack\external\goldensun_html5\base\`, `C:\Users\aaron\Documents\UnboundHack\external\pokeemerald-expansion\include\constants\battle.h`, `C:\Users\aaron\Documents\UnboundHack\external\tmc-picori\android\app\src\main\AndroidManifest.xml`, `C:\Users\aaron\Documents\UnboundHack\games\AGSE-5c469520-Golden-Sun-USA-Europe\maps\rooms\room_012\room_012.tmj`.