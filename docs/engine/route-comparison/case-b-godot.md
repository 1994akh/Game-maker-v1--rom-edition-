# Route B (Godot 4): the case for it

Checked 2026-10-13. VERIFIED means I saw it in code, docs, an API response or a local file in this session. INFERRED means it is my reading and has not been tested. Nothing was built or run except read-only scripts and fetching Godot's own source files.

## Summary

- **Godot's strength is the parts the C route struggles with.** On the GBA code base, free 8-way movement alone was sized at 6–10 weeks (`docs\phase1\MOVEMENT.md`, Option B). In Godot it is about a week, because it's only the field code. Android export, touch, controllers, OGG looping, saves and screen resizing are built into the engine, and there are no GBA limits on an 8-vs-6 battle, long Psynergy lists, two crews or save size.
- **Our data is already in formats Godot can use directly.** Rooms are Tiled 1.10.2 `.tmj` files with 3 tile layers plus tile-event, entrance and actor object layers (VERIFIED on `maps\rooms\room_012\room_012.tmj`). Collision is in `collision.json`, graphics are PNG, the mechanics are JSON tables, and the music is MIDI with `loopStart`/`loopEnd` markers.
- **The current engine fits the phone.** Godot 4.7.2-stable came out 2026-08-18. Its Android template targets and compiles against SDK 36 (min 24). Its activity already handles fold and unfold without restarting (`configChanges` includes screenSize, smallestScreenSize, screenLayout, density and orientation). It marks the app as a game by default, which matters for Android 16 on large screens. All VERIFIED in the 4.7.2 source.
- **The price is the Pokémon side.** All Pokémon mechanics (move effects, status, catching, evolution data) are rewritten in GDScript instead of inherited from the expansion's C battle engine.

## 1. Architecture: what comes from where

```
Game-maker-v1/game/                Godot 4.7.2 project, typed GDScript (no C#: no .NET SDK on this PC, VERIFIED)
  core/      autoloads: Db (JSON tables), GameState (flags, crews, bag, storage), Save (user://),
             InputRouter (semantic actions MOVE8/CONFIRM/PSY_n… from CONTROLS.md), Audio
  field/     GsMover (GS movement + 16 px cell collision, 3 layers, height shapes), Actor, Camera,
             Pushable/Interactables, FieldPsynergy/{Move,…}.gd, EventRunner (event DSL)
  battle/    pure-logic model (headless-testable): GsFormulas.gd, TurnEngine, EnemyAI, PartnerRules
             (revive window, Rouse), Standby/Summon; separate BattleView (sprites, menus, numbers)
  ui/        TouchOverlay, menus, Pokémon-style level-up popup, PostureLayout
  android/   FoldPosture plugin (Kotlin, androidx.window 1.5.x → posture_changed signal)
  data/ maps/  GENERATED, never hand-edited
  tests/     GUT: formula vectors, movement replays, headless battle simulations
tools/ (Python + PowerShell, saved and reusable): export_godot.py, gen_formula_vectors.py,
       render_music.py, setup_android.ps1, build_apk.ps1, install_apk.ps1, run_tests.ps1
```

| Piece | Source | Reuse or write |
|---|---|---|
| Rendering, tilemaps, touch and joypad input, audio, Android packaging and signing, UI controls, tweens, file I/O | Godot 4.7.2 (MIT) | Reuse as-is |
| **Maps:** GS1 has 201 rooms on 186 areas (176 render); GS2 has 325 rooms on 312 areas (301 render). Each area has PNG layers, a 16 px tileset, `collision.json` (`cell_px`, `solid_value` 255, 3 layers, `height_shapes`) and `area.json` | Our extraction, `UnboundHack\games\<slug>\maps\` (VERIFIED) | Reuse. `export_godot.py` turns each room into a `.tscn` plus TileSet `.tres`. I'd write our own small converter instead of the YATI Tiled plugin: our format is simple, collision is custom, and it avoids a third-party dependency (INFERRED) |
| **Mechanics tables:** abilities, characters, classes, djinn, encounters, enemies, field_psynergy, items, summons | `games\<slug>\data\*.json` (VERIFIED) | Reuse as-is |
| **Battle sprites:** GS1 165 enemy sheets; party sheets are 64×64 with 20 frames plus weapon overlays | `battle_sprites\` (VERIFIED from `notes\gs_battle_sprites.md`) | Reuse as placeholders |
| **Pokémon sprites:** front, back, icon and overworld `.png` plus `.pal`, about 1,029 folders | `external\pokeemerald-expansion\graphics\pokemon\` (VERIFIED) | Reuse as placeholders |
| **Damage formulas** | `gbax\codecs\gs_battle.py`, 531 lines. Physical/Psynergy/heal cores, elements, status chance, crits, flee, enemy action priority, Djinn recovery. It matched the game in 2,263 emulated calls (per `party-and-battle.md` §5) | Port to GDScript. The Python generates JSON test vectors, so the port is checked call-for-call |
| **Movement constants and live trace:** walk 1.0 and run 1.5 px/frame, accel 0.25, 8 px five-ray probe, slide at ±22.5°/45°/67.5°, facing turns 22.5° per frame. Plus a 1,820-frame `walk_log.csv` | `notes\gs_movement.md`, `tools\gs_movement\` (VERIFIED) | Port. Replay the trace as a regression test |
| **Field-ability, pushable and event architecture:** `FieldAbilities.ts` 760 lines, `MoveFieldPsynergy.ts` 386, `Pushable.ts` 582 (dock tiles, after-push events), 74 event types, `Battle.ts` 1,845, `EnemyAI.ts` 365, menus | `external\goldensun_html5` (MIT; VERIFIED line counts) | Port the design, and code where useful. **Not** its collision: it uses P2-physics polygons (`Collision.ts`), while we have the real GS cell grid |
| Exact GS behaviour (battle flow, formation selection) and GS1 per-room script logic (per-map folders such as `KOROSSEO_*`) | alchemy GS1, about 90% matching C; no licence | Reference only |
| Corner nudge, pushable statues stamping a solid tile, pressure-plate weight, Picori-style floating joystick | tmc / Picori | Reference only: tmc has no licence and Picori is GPL. Copy the design, not the code |
| Species stats, types, learnsets, evolutions, moves | expansion `src\data\pokemon\species_info\gen_*_families.h` and moves data; Showdown (MIT) as a second spec | A Python converter (new) and the effects themselves (new) |
| 8-vs-6 battle with partners, crews, catching on GS scale, classes, Fold UI, event DSL, save format | — | **Write** (no source covers these on any route, per `fit_report.md`) |

## 2. First playable vertical slice on the Fold 7

**Map: GS1 room 12, Sol Sanctum (area 12).** It is 51×33 tiles with 13 actors and 29 events. Its Move events target actors 9, 11, 13 and 15 (flags 0x80B–0x80E) and actor 10 (flag 0x816), all VERIFIED from `field_psynergy.json`. The notes say actor 9 must reach cell (31, 9). The Move rules are VERIFIED in `gs_field_psynergy.md` §7:
- a hand object appears on the target;
- only the 4 pure d-pad directions count;
- the game tests the cells 16 px and 32 px ahead;
- the statue slides one 16 px cell at 0.2 px/frame, with a 15-frame wait;
- then the room's phase-0 script checks the position and sets the flag.

**Known catch:** event actor ids don't match the exported actor list. There is probably an offset of 8 for party slots (`gs_maps.md`). Exported actors 1–8 are sprite 201 and actor 9 is sprite 202, so I still have to confirm which statue event "actor 9" means. I'll do that from the composite image and the room's map code at 0x02009575, which takes about half a day.

| # | Work item | Days (Claude) |
|---|---|---|
| 0 | Toolchain install scripts and a hello-world APK on the Fold | 0.5–1 |
| 1 | `export_godot.py`: room `.tmj` + area tileset/collision → Godot scene with 3 layers, priorities and actors. Copy the data tables | 2–3 |
| 2 | GsMover: acceleration, 8 directions plus analog angle, five-ray fan, slide, layers, height shapes, Y-sort, camera. GUT replay against `walk_log.csv` | 3–5 |
| 3 | Input: InputMap for Xbox/Backbone; touch overlay (floating stick on the left, A/B/L/R/Menu/Psy); hide the overlay when a gamepad is used | 2–3 |
| 4 | Move: Psynergy shortcut, hand, push, cell check, flag set; puzzle stays solved after re-entering the room; minimal save | 2–3 |
| 5 | Battle logic: Adept and partner model (HP clamp formula from §5), GsFormulas port plus vectors, turn order, enemy AI, revive window and Rouse, victory/EXP and GS-style level-up text. Headless simulations | 5–7 |
| 6 | Battle view: 8 vs up to 6 layout, command menus for touch and controller, sprites, damage numbers, an encounter group from `encounters.json`, Pokémon-style level-up popup | 4–6 |
| 7 | Fold layouts: cover portrait/landscape and inner screen, re-laid-out on resize; 60 fps cap | 1–2 |
| 8 | Fixes from play-tests | 3–5 |
| — | Stretch goal: tabletop posture plugin (needs the Gradle export) | 1–2 |

**Calendar:** about **4–6 weeks, most likely 5**, assuming daily Claude sessions and a play-test every 2–3 days.
- Week 1: setup, map import and walking. Play-test 1.
- Week 2: controls, Fold layouts and Move. Play-test 2.
- Week 3: battle logic.
- Week 4: battle view. Play-test 3.
- Week 5: fixes and stretch goals.

Your part is about 1 hour of one-time phone setup plus 4–6 play-tests of 30–60 minutes. Confidence is medium (about 60% for 6 weeks or less). The biggest unknowns are how faithful the height-shape collision is and how readable a 14-sprite battle is on the cover screen.

## 3. The full game beyond the slice

Rough figures for systems with placeholder art. All INFERRED.

| System | Estimate |
|---|---|
| Event DSL modelled on html5's 74 event types. GS room scripts are Thumb code with no decompiler, so events are rewritten per room (GS1's alchemy C helps) | 3–5 wk, plus content per room |
| Remaining field Psynergy (html5 has 14 to port) and Lost Age ones (Hover, Scoop, Cyclone, Parch, Burst, Teleport) designed from scratch, because GS2 is only 4.7% decompiled | 4–8 wk |
| Menus: Psynergy, Set/Standby, items, equipment, status, shops, inns, storage | 6–10 wk |
| Species/move importer from expansion headers | 1–2 wk |
| **Move effects, status and items re-expressed on GS formulas** (a curated Gen 1–7 pool; full coverage costs far more; Pokémon abilities, if wanted, add more) | 6–16 wk |
| Catching, storage, evolution, two crews, restoration points, save format | 4–6 wk |
| Summons, Unleash, Standby, 18-type classes; enemy trainers that mirror the crew | 5–8 wk |
| Surf, Dive and Waterfall in free movement, underwater layers | 3–5 wk |
| World map: exporter first, because its format differs and isn't exported yet; then ship and sailing | 5–9 wk |
| Djinn-style encounters | 1–2 wk |
| Music: MIDI+SF2 → OGG with loop points via FluidSynth, mapped to Godot's `loop_offset`; then sound effects | 1–2 wk |
| Fold polish: controller remapping, touch layout editor, settings | 2–3 wk |

**Total: about 7–12 months** to feature-complete with placeholder art. Content (maps, story missions, balancing) comes on top: 6–12+ months part-time, as `SCHEDULE.md` already says. The graphics remake is cheaper here than on a GBA base, because there are no 4bpp, palette or VRAM limits.

**Biggest risks:**
1. Rewriting Pokémon mechanics and their tests without the expansion's test suite.
2. Event authoring for every room, plus the open actor-id mapping.
3. Lost Age systems have no source code.
4. A large GDScript code base. Mitigation: static typing, pure-logic classes, and test gates.
5. Godot 4.x changes between versions. Mitigation: pin 4.7.2 and upgrade only at milestones.
6. The extra complexity of the Gradle build and the posture plugin.

## 4. How well Claude Code can work in it on this PC

**What is installed now** (VERIFIED):
- Python 3.13, git and gh.
- .NET runtimes only, no SDK.
- WSL Ubuntu, running.
- **Missing:** Godot, Java/JDK, adb, the Android SDK and Node.

**What to install.** I can script all of this into `tools\setup_android.ps1` once you approve. Downloads total about 3–5 GB.

| Item | Why |
|---|---|
| `Godot_v4.7.2-stable_win64.exe.zip` (82 MiB) | Editor and command-line engine |
| `Godot_v4.7.2-stable_export_templates.tpz` (1,222 MiB) | Required for export; extracted to `%APPDATA%\Godot\export_templates\4.7.2.stable\` |
| OpenJDK 17, e.g. Temurin | Godot docs recommend 17. Godot reads `JAVA_HOME` (VERIFIED in `export.cpp`) |
| Android cmdline-tools, platform-tools, build-tools 35.0.1, `platforms;android-36` | The docs list Platform 35, but the 4.7.2 Gradle template compiles against 36. Godot reads `ANDROID_HOME` (VERIFIED) |
| NDK r28b and CMake 3.10.2 | Listed in the docs. Probably unused by a plain APK export (INFERRED) |
| GUT test addon, copied into the project | Headless tests |
| scrcpy (optional) | Mirrors the phone on the PC. Godot 4.7.2 has scrcpy editor settings (VERIFIED) |
| Not needed | Node, .NET SDK |

**Command-line workflow.** All of these flags are VERIFIED in the [Godot command-line docs](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html):
- `godot --headless --import` imports assets.
- `godot --headless -d -s addons/gut/gut_cmdln.gd -gdir=res://tests -gexit` runs the tests.
- `godot --headless --export-debug "Android" build/game.apk` builds the APK.
- `--install-android-build-template` sets up the Gradle build.
- `--doctool` dumps the exact 4.7.2 API to XML. I can check API names against it, which protects against changes between 4.x versions.

Build details:
- The export creates a debug keystore with `keytool` automatically (VERIFIED, `_create_editor_debug_keystore_if_needed`).
- A plain APK export doesn't use Gradle (`gradle_build/use_gradle_build` defaults to false, VERIFIED). Gradle comes in only with the posture plugin; then Gradle and AGP 8.6.1 are downloaded on the first build.

**How I'd check my own work:**
- run the game windowed on Windows at Fold window sizes;
- save screenshots from a debug autoload, or record frames with Movie Maker mode (INFERRED);
- replay recorded inputs;
- on the phone, read `adb logcat` and grab screens with `adb exec-out screencap -p`.

**Weak spot:** editor-only workflows such as painting TileSets or animation tracks. To avoid them, all resources are generated from data. Godot's `.tscn` and `.tres` files are text, so I can write and diff them.

**Installing the APK on the Fold 7:**
- **Recommended:** turn on Developer options (tap Build number 7 times) and then Wireless debugging. Pair once with `adb pair`. After that, `tools\install_apk.ps1` runs `adb install -r` over Wi-Fi. A USB-C cable with USB debugging also works.
- **Alternative:** copy the APK to the phone and tap it, after allowing "Install unknown apps" once.
- **Keep the same keystore and back it up.** Updates install over the old version and keep your saves only if they are signed with the same key.

## 5. Fold 7 specifics

**Switching screens.** The 4.7.2 activity handles size and orientation changes itself (VERIFIED), so folding and unfolding resizes the window instead of restarting the app. The game re-lays itself out on `size_changed` (INFERRED). Settings needed:
- `display/window/size/resizable=true` in the project, which sets `resizeableActivity` (mapping VERIFIED);
- "Continue apps on cover screen" on for this app (from `CONTROLS.md`).

**Scaling.** Use integer scaling as in `CONTROLS.md` §6 (cover 4× portrait / 6× landscape, inner 6–8×). Unlike the GBA, the view can widen: cover landscape at 6× shows about 420 logical px instead of 240 (INFERRED).

**Tabletop.** Godot has no built-in fold or hinge API; my search found none (INFERRED). A small Android plugin (v2, Kotlin, `androidx.window` 1.5.x, about 30 lines of posture logic in the Butterfly pattern) sends the posture and hinge rectangle to the game. In tabletop, the field or battle goes on the top half and the controls or command menu on the bottom. Without the plugin, the flat inner layout still works.

**Controllers.** Xbox and Backbone pads should show up as standard Godot joypads (INFERRED). The Backbone fits only on the folded phone, per `CONTROLS.md`. Hide the touch overlay on joypad input, and show a controller test screen.

**Performance and battery.**
- GBA-scale 2D is trivial for this phone (INFERRED).
- The real cost is the 120 Hz panel. Cap the game at 60 fps, and optionally ask Android for 60 Hz from the same plugin (INFERRED).
- Use the Compatibility (OpenGL ES 3) renderer for lighter 2D, or Mobile/Vulkan if shaders need it (INFERRED).
- Immersive mode is on by default and edge-to-edge is off (VERIFIED).

## 6. Honest weaknesses compared with the other two routes

I'm assuming the other routes are:
- **Route A:** C on pokeemerald-expansion with an SDL3 Android layer, the Picori pattern;
- **Route C:** goldensun_html5 (TypeScript) in an Android WebView.

**Compared with A:**
- Godot gives up the expansion's roughly 170k lines of battle C and about 5,000 CI battle tests (`CODEBASE.md`).
- It also gives up the move, ability and item effects; Dive, followers, DexNav and overworld encounters; and the Porymap/poryscript tools. Everything Pokémon is rewritten and retested.
- If you want deep Pokémon fidelity, A is stronger on that axis. A pays instead with 6–10 weeks of hybrid free movement, an 8-vs-6 battle on a GBA engine, save-space limits, and an Android port of the expansion that nobody has built yet.

**Compared with C:**
- html5 already runs a GS field and battle engine. C could have something walking in days, while Godot has to port the parts we need into GDScript, which takes weeks.
- C's own costs are Phaser CE 2.19 (old), WebView performance and input latency, and still needing a Kotlin host.

**Godot-specific costs:**
- 1.2 GB of export templates, plus JDK and SDK setup.
- A Gradle build just to read the hinge posture.
- An AI developer has to avoid editor-only workflows.
- No GBA-exact effects: blending and mosaic would need shaders.
- A long-lived GDScript code base needs strict structure to stay maintainable.

Sources:
- [GitHub releases API, godotengine/godot (4.7.2-stable, assets)](https://api.github.com/repos/godotengine/godot/releases/tags/4.7.2-stable)
- 4.7.2 `config.gradle`, `src/main/AndroidManifest.xml`, `export/export_plugin.cpp` and `export/export.cpp` at raw.githubusercontent.com/godotengine/godot/4.7.2-stable/platform/android/…
- [Exporting for Android (4.7 docs)](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html)
- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [Godot forum: targeting the latest SDK](https://forum.godotengine.org/t/how-to-target-latest-android-sdk/142631)
- [Godot Android library docs](https://docs.godotengine.org/en/4.5/tutorials/platform/android/android_library.html)
- [YATI](https://github.com/Kiamo2/YATI)
- [GUT CLI notes (third-party)](https://tessl.io/registry/testland/godot-gut-tests/files/references/cli.md)
- [Godot MIDI Player 4](https://godotengine.org/asset-library/asset/1667)
- [FluidSynthGodot](https://noisy-gate.itch.io/fluidsynthgodot)

Local files read:
- `docs/engine/gba-sources.md`
- `C:\Users\aaron\Documents\Game-maker-v1\docs\design\party-and-battle.md`
- `C:\Users\aaron\Documents\Game-maker-v1\docs\phase1\{CODEBASE,CONTROLS,MOVEMENT,SCHEDULE}.md`
- `C:\Users\aaron\Documents\UnboundHack\notes\{gs_maps,gs_movement,gs_field_psynergy,gs_battle_sprites,music_export}.md`
- `C:\Users\aaron\Documents\UnboundHack\gbax\codecs\gs_battle.py`
- `C:\Users\aaron\Documents\UnboundHack\games\AGSE-5c469520-Golden-Sun-USA-Europe\{maps,data}\`
- `C:\Users\aaron\Documents\UnboundHack\external\goldensun_html5\base\`