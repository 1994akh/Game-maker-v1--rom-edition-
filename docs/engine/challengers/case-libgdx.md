**Challenger #1: libGDX 1.14.2 + Kotlin vs Godot 4.7.2**

**Verdict: libGDX doesn't beat Godot for this project.** It is better on toolchain simplicity, compile-time safety, testability and fold access. It is worse on everything this game uses heavily: many menus driven by a controller, cutscenes, Psynergy effects, the later art and music passes. The vertical slice would take about 8–10 weeks on libGDX against 6–8 on Godot. Godot's fold gap is smaller than the screening suggested (see "Case against").

## Strongest honest case for libGDX

1. **One toolchain instead of two.** On Godot, a fold plugin is a v2 Android plugin, and the Godot docs say a v2 plugin "requires the use of the Gradle build process" (VERIFIED). So Godot ends up needing the JDK, Android SDK and Gradle anyway, plus the editor and export templates. libGDX needs only the JDK, Android SDK and Gradle.
2. **Direct fold access.**
   - `AndroidApplication extends Activity` (VERIFIED).
   - `androidx.window:window-java:1.5.1` is stable (2025-11-19) and provides `WindowInfoTrackerCallbackAdapter`, which works with any Activity (VERIFIED).
   - Tabletop is `FoldingFeature` with `state == HALF_OPENED` and `orientation == HORIZONTAL` (VERIFIED).
   - That's about 60 lines in the launcher, with no plugin packaging or signal bridge.
3. **Compile-time safety.** Kotlin rejects type and null errors before the user plays a build. Typed GDScript catches less, and models often mix Godot 3 and Godot 4 APIs (INFERRED). That matters most in this "Claude writes, user play-tests" loop.
4. **Port fidelity.** TypeScript classes, enums, generics, interfaces and lambdas map almost one-to-one onto Kotlin; GDScript has no interfaces or generics (INFERRED). goldensun_html5 is MIT with 2.5 MB of TypeScript (VERIFIED). By size: battle 300 KB, windows 434 KB, game_events 333 KB, field_abilities 165 KB, Map.ts 107 KB, ControllableChar 89 KB.
5. **Test oracle.**
   - A pure-Kotlin `logic` module with JUnit runs `gradlew :logic:test` in seconds (INFERRED).
   - Golden test values come from our `re/gbax/codecs/gs_battle.py` (VERIFIED locally): `attack_damage`, `psynergy_damage`, `heal_amount`, `status_chance`, `flee_chance_x10000`, `enemy_action_priorities` and `BattleRng`.
   - Kotlin's 32-bit Int, which truncates on division, matches GBA integer maths (INFERRED).
6. **Built-in Tiled loading** (VERIFIED from `BaseTmjMapLoader.java`):
   - `TmjMapLoader` handles object templates, class properties, csv/base64 data with gzip/zlib, tile animations and per-tile collision objects.
   - It does not handle zstd or infinite maps; our exporter doesn't need either.
   - Godot needs an add-on importer for this.
7. **Small, stable, all-code projects.** The 1.x API has been stable for years; the 1.14.x breaking changes are minor (VERIFIED in CHANGES). There are no `.tscn`/`.import` files to churn. APKs are smaller and non-continuous rendering in menus saves battery (INFERRED).
8. **Active helper libraries:** Fleks ECS 2.15 (2026-08-29) and TextraTypist v2.5.0 (2026-09-10), a typing-label library that suits portrait dialogue (VERIFIED).

## Strongest honest case against libGDX

1. **We'd have to build engine features Godot already has.** Scene2D has no gamepad focus navigation (INFERRED); Godot `Control` has focus neighbours and `ui_*` actions. There is also no AnimationPlayer, Tween, AnimationTree, particle editor or cutscene tooling. "Many menus" means this cost comes back in every phase, not just the slice.
2. **Godot's fold gap is small.**
   - Godot's manifest already has `configChanges="…screenSize|smallestScreenSize|density|screenLayout|uiMode…"` (VERIFIED), so switching between the cover and inner screens is just a resize.
   - The gdx-liftoff template has only `keyboard|keyboardHidden|navigation|orientation|screenSize|screenLayout` (VERIFIED). Unless we add `smallestScreenSize|density`, folding or unfolding restarts the Activity (INFERRED). Easy to fix, but here Godot is ahead.
   - Tabletop on Godot is about 100 lines of Kotlin in a v2 plugin (`getActivity()`, `emitSignal`, VERIFIED).
3. **The physics port costs about the same either way.** goldensun_html5's `Collision.ts` uses Phaser P2 bodies, collision groups per layer, contact normals quantised to 8 directions, and Turf.js (VERIFIED). Godot's physics layers and `move_and_slide` are a closer match. On libGDX we'd use Box2D (gdx-box2d, last push 2025-10, VERIFIED) or write our own polygon collider.
4. **The Kotlin layer has gone quiet.** KTX's last release is 1.13.1-rc1 (2025-02-03), and its develop branch was last touched 2025-06-28 (VERIFIED). Plan on plain libGDX called from Kotlin.
5. **Audio.** libGDX `Music` has no loop-start point (INFERRED); Godot's OGG streams have `loop_offset`. For GS and Pokémon intro+loop tracks we'd need split files or our own streaming player.
6. **Art pass.** libGDX has no built-in 2D lights, normal maps or visual editor (INFERRED), so the user can't tweak layouts or animations by hand later.
7. **Controllers.** gdx-controllers 2.2.4 (2025-06-08) maps buttons on Android "if possible", and the Features wiki says "Vibration is not supported by operating system" there (VERIFIED).

## Architecture on libGDX

- **`logic/`** (pure Kotlin, JVM only):
  - kotlinx.serialization models for the JSON tables (GS units, abilities, Djinn; Pokémon Gen 1–7 species, moves, learnsets, evolutions).
  - The battle state machine, ported from goldensun_html5 `battle/` with formulas checked against `gs_battle.py`.
  - Collision and height rules read from the `gs_maps.py` collision JSON (`cell_px` 16, per-layer grids, `height_shapes`; VERIFIED locally).
  - Save model.
- **`core/`** (libGDX): screen stack, `TmjMapLoader` plus a custom renderer that interleaves sprites with map layers, Scene2D UI with TextraTypist dialogue, an input-action layer, and audio.
- **`android/`**: launcher, fold bridge, manifest fixes.
- **`lwjgl3/`**: a Windows build of the game for fast iteration.
- **`tools/`**: Gradle tasks for TexturePacker atlases, MIDI+SF2 → OGG via FluidSynth, and data validation.

## Vertical slice: work items and calendar

The estimate assumes the user play-tests 2–3 times a week.

| Week | Work |
|---|---|
| 1 | Toolchain, hand-written Gradle multi-module project (gdx-liftoff is a "GUI application", VERIFIED), manifest fixes, first APK over wireless adb, input actions (touch stick, controllers, keyboard) |
| 2 | Framework we'd otherwise get from Godot: screen stack, tween/sequence runner, asset/atlas pipeline, UI skin with gamepad focus navigation, portrait dialogue |
| 3–4 | Field: TMJ rendering with layer priority, collision port with GS wall-sliding, 8-way movement (ControllableChar/MainChar), stairs and height tile events, NPCs, camera |
| 5 | Move puzzle: port MoveFieldPsynergy plus interactable objects, cast effect |
| 6–8 | 4+4 battle: turn order, Attack / one Psynergy / Defend / one Pokémon move, pseudo-3D stage (PerspectiveCamera + DecalBatch, INFERRED), battle menus, golden-value tests, return to the field |
| 9 (+1 buffer) | Fold layouts, controller hot-plug, pause/save, fixes from play-testing |

Total: **8–10 weeks**, against 6–8 for Godot. Most of the extra time is the week-2 framework and the menu/animation work in the battle weeks.

## Fold 7 specifics

- **Layouts.** In tabletop, the top half of the inner screen is about 2184×984 (≈2.2:1, INFERRED from the resolution). That is close to the cover screen's 21:9, so one landscape game-view target covers both, and the bottom half can hold touch controls or battle menus. Inner flat (2184×1968) gets side panels or extra map.
- **Manifest.**
  - Add `smallestScreenSize|density|uiMode` to `configChanges`.
  - Keep `android:appCategory="game"` (the liftoff template sets it, VERIFIED).
  - On Android 16, games are exempt from the large-screen orientation override, and the opt-out property goes away at API 37 (VERIFIED).
  - Use `sensorLandscape`.
- **Fold events.** `resize(w, h)` recomputes the viewport. The WindowManager listener passes posture and hinge bounds to the game via `Gdx.app.postRunnable`. The callback adapter is deprecated in 1.6.0-alpha03 but fine on 1.5.1 (VERIFIED).
- **Controllers.** Backbone (USB-C) and Xbox (Bluetooth) should appear as standard Android gamepads (INFERRED). Hide the touch overlay while one is connected. For rumble, call Android's `InputDevice` vibrator directly.

## Command-line build, test and deploy on Windows

- **Installs:**
  - Temurin JDK 21: about 180 MB download (INFERRED). gdx-liftoff recommends JDK 21; Gradle 8.10+ needs 17+ (VERIFIED).
  - Android command-line tools: 155.7 MB (VERIFIED), then `sdkmanager` for platform-tools, an API 36 platform and build-tools, about 1–1.5 GB (INFERRED).
  - Gradle and dependency caches: about 0.7–1 GB (INFERRED).
  - FluidSynth: about 30 MB.
  - Android Studio (1.5 GB, VERIFIED) is optional.
  - Total is about 2.5–3 GB. Godot with a fold plugin needs the same plus its editor and export templates (about 1.2 GB, INFERRED).
- **Commands:** `gradlew :logic:test`, `gradlew :lwjgl3:run`, `gradlew :android:installDebug`, `adb pair`/`adb connect` for wireless, `adb logcat`, `adb exec-out screencap -p`. Release builds use `assembleRelease` with an uncommitted `keystore.properties`. WSL isn't needed.

## Long-term maintainability and later passes

- **Graphics.** Replacing PNGs regenerates the atlases with no code changes. Lighting and HD effects mean hand-written GLSL. Godot's 2D lights, shaders and AnimationPlayer are stronger here.
- **Music.** Render to OGG in either engine; libGDX also needs loop handling (see audio above).
- **Code.** All Kotlin, so refactors are checked by the compiler.
- **Release cadence.** Releases come about 2–3 times a year (1.14.0 on 2025-10-19, 1.14.1 on 2026-05-18, 1.14.2 on 2026-06-05; VERIFIED), from a small maintainer team.

## Risks, ranked

1. The framework-building cost (UI focus navigation, cutscene runner, effects) recurs in every phase.
2. A missing fold `configChanges` entry restarts the Activity and loses game state.
3. Porting the P2-based collision so movement *feels* like Golden Sun.
4. KTX is dormant.
5. Audio loop points.
6. No editor for the user during the art pass.

**Switch trigger:** move to libGDX only if, in Godot's first 2 weeks, GDScript type or API errors keep producing play-test regressions, or the Gradle-build export with the fold plugin turns out to be flaky.

**Ideas worth taking into the Godot plan anyway:**
- An engine-free logic layer tested against golden values from `gs_battle.py`.
- The Kotlin fold plugin on day 1.
- `appCategory="game"` with `sensorLandscape`.

## Sources

- https://github.com/libgdx/libgdx/releases (via `gh api`: 1.14.2 on 2026-06-05)
- https://raw.githubusercontent.com/libgdx/libgdx/master/CHANGES
- https://raw.githubusercontent.com/libgdx/libgdx/master/backends/gdx-backend-android/src/com/badlogic/gdx/backends/android/AndroidApplication.java
- https://raw.githubusercontent.com/libgdx/libgdx/master/gdx/src/com/badlogic/gdx/maps/tiled/TmjMapLoader.java
- https://raw.githubusercontent.com/libgdx/libgdx/master/gdx/src/com/badlogic/gdx/maps/tiled/BaseTmjMapLoader.java
- https://raw.githubusercontent.com/libgdx/gdx-liftoff/master/README.md
- https://raw.githubusercontent.com/libgdx/gdx-liftoff/master/src/main/kotlin/gdx/liftoff/data/platforms/Android.kt
- https://raw.githubusercontent.com/libgdx/gdx-controllers/master/README.md
- https://github.com/libgdx/gdx-controllers/wiki/Features
- https://github.com/libktx/ktx (releases and commits via `gh`)
- https://github.com/tommyettinger/textratypist
- https://github.com/Quillraven/Fleks
- https://github.com/libgdx/gdx-box2d
- https://developer.android.com/guide/topics/large-screens/make-apps-fold-aware
- https://developer.android.com/jetpack/androidx/releases/window
- https://developer.android.com/about/versions/16/behavior-changes-16
- https://developer.android.com/studio
- https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html
- https://github.com/godotengine/godot/blob/master/platform/android/java/app/dataLib/src/main/AndroidManifest.xml
- https://github.com/jjppof/goldensun_html5 (licence, language sizes and tree via `gh`)
- https://raw.githubusercontent.com/jjppof/goldensun_html5/master/base/Collision.ts
- Local: `C:\Users\aaron\Documents\Game-maker-v1\re\gbax\codecs\gs_battle.py` and `gs_maps.py`