**Answer: yes, two engines are worth a look, but neither clearly beats Godot 4.7.2.** libGDX (Kotlin) gets the top raw score. Unity 6.6 has the best foldable support. The one real gap in Godot for this project is the fold posture API. Godot catches up there with a small Kotlin Android plugin, which is the cheaper option.

Scores are 1–5 per column: A = Android export from the command line, F = foldable/posture, G = gamepad + multi-touch, T = tilemaps incl. Tiled, U = UI/menu tooling, H = headless/automated testing, C = text files and code-first workflow, P = performance/battery, E = RPG ecosystem/docs, L = licence. Sum is out of 50.

Version and date details come from the GitHub releases API, the Unity release API, pub.dev, NuGet, GitLab, Steam News, and Construct's `versions.json`. VERIFIED means I saw it today at the listed source. INFERRED means it comes from my own knowledge or reasoning.

**The raw sums mislead.** They don't count how much engine you have to build yourself: scene editor, animation/tween system, UI framework, cutscene tooling. Godot, Unity and RPG Maker include most of that. libGDX, MonoGame, Ebitengine, raylib and Bevy leave it to you.

### Scores

| Engine | Version (last stable release) — VERIFIED | A | F | G | T | U | H | C | P | E | L | Sum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Godot (current pick, for reference) | 4.7.2 (2026-08-18) | 5 | 3 | 4 | 4 | 5 | 4 | 4 | 4 | 4 | 5 | 42 |
| Unity 6 (2D) | 6.3 LTS = 6000.3.26f1; newest non-LTS = 6000.6.5f1 (both 2026-10-08); 7000.0 is in alpha | 4 | 5 | 5 | 4 | 4 | 4 | 3 | 3 | 5 | 4 | 41 |
| libGDX (Kotlin/Java) | 1.14.2 (2026-06-05) | 5 | 5 | 4 | 5 | 3 | 5 | 5 | 5 | 3 | 5 | 45 |
| Flutter + Flame | Flutter 3.47.7 (2026-10-08); Flame 1.38.2 (2026-08-27); flame_tiled 3.1.2 (2026-07-19), 4.0.0-dev.1 (2026-10-06); gamepads 0.1.12 (2026-09-15) | 5 | 5 | 3 | 3 | 5 | 5 | 5 | 3 | 2 | 5 | 41 |
| MonoGame (+ MonoGame.Extended + Gum) | 3.8.6 (2026-10-07); Extended 6.1.1 (2026-08-18); Gum.MonoGame 2026.10.1.1 | 4 | 4 | 4 | 3 | 3 | 3 | 5 | 4 | 3 | 5 | 38 |
| FNA | 26.10 (2026-10-01) | 1 | – | – | – | – | – | – | – | – | – | n/a |
| Defold | 1.14.0 (2026-10-12) | 5 | 3 | 4 | 4 | 3 | 3 | 4 | 5 | 2 | 5 | 38 |
| Ebitengine (Go), found in this search | 2.10.5 (2026-10-09) | 4 | 4 | 4 | 3 | 2 | 4 | 5 | 5 | 2 | 5 | 38 |
| HaxeFlixel | 6.2.0 (tag 2025-12-12); Lime 8.3.2 (2026-05-13) | 4 | 2 | 4 | 4 | 2 | 3 | 5 | 4 | 3 | 5 | 36 |
| Heaps | 2.1.1 (2025-06-07); Haxe 4.3.7 | 2 | 2 | 4 | 3 | 2 | 3 | 5 | 4 | 2 | 5 | 32 |
| Axmol (cocos2d-x successor), found | 2.11.5 (2026-09-25) | 4 | 3 | 4 | 4 | 2 | 3 | 4 | 5 | 2 | 5 | 36 |
| KorGE (Kotlin), found | 6.0.0 (2025-05-16), nothing released since | 3 | 3 | 4 | 4 | 3 | 4 | 5 | 4 | 1 | 5 | 36 |
| Bevy | 0.20.0 (2026-10-08); bevy_ecs_tiled 0.13.4 (2026-08-24) | 2 | 2 | 4 | 4 | 2 | 5 | 5 | 4 | 2 | 5 | 35 |
| Cocos Creator, found | engine 3.8.8 (2025-12-16) | 3 | 3 | 3 | 4 | 4 | 2 | 3 | 4 | 3 | 4 | 33 |
| LÖVE (love-android) | 11.5 (2023-12-03); love-android 11.5a (2023-12-29); 12.0 still not tagged | 3 | 2 | 4 | 3 | 1 | 3 | 5 | 4 | 2 | 5 | 32 |
| raylib | 6.0 (2026-04-23) | 3 | 2 | 4 | 1 | 2 | 3 | 5 | 5 | 1 | 5 | 31 |
| Solar2D, found | build 3736 (2026-10-12) | 3 | 3 | 3 | 3 | 2 | 2 | 4 | 4 | 2 | 5 | 31 |
| GameMaker | monthly 2024.14.4.222 (2026-03-31); LTS 2026.0 (2026-05-21) | 3 | 1 | 4 | 2 | 3 | 1 | 3 | 4 | 4 | 4 | 29 |
| RPG Maker MZ | 1.10.0 (2026-01-30) | 2 | 1 | 3 | 2 | 4 | 1 | 3 | 2 | 5 | 4 | 27 |
| Solarus | 2.1.4 (2026-09-08; 2.1.0 on 2026-07-27) | 1 | 1 | 3 | 2 | 2 | 2 | 4 | 4 | 2 | 3 | 24 |
| Pokémon Essentials (RPG Maker XP / mkxp-z) | v21.1 (2023-07-31); mkxp-z v2.4.2 (tagged 2023-05-09, repo still active 2026-10) | 1 | 1 | 2 | 1 | 2 | 1 | 2 | 3 | 5 | 2 | 20 |
| Construct 3 | stable r495.2 (2026-08-05); beta r505 (2026-10-06) | 1 | 1 | 3 | 2 | 2 | 1 | 1 | 2 | 2 | 2 | 17 |
| Also found: GDevelop 5.6.283 (2026-09-29), Phaser 4.2.1 (2026-07-09), Redot 26.3-rc.3 (2026-10-08, a Godot fork) | | | | | | | | | | | | not scored |

### Key facts behind the scores

**Godot's gap (VERIFIED):**
- Godot's DisplayServer docs have no fold, hinge or posture API.
- Godot's Android library doesn't include the `androidx.window` dependency (Jetpack WindowManager).
- Tabletop posture therefore needs a custom Kotlin Android plugin, or a paid itch.io plugin I could not check.
- Switching between the cover and inner screens should still arrive as an ordinary window resize (INFERRED).

**Unity 6:**
- VERIFIED: the 6000.5 and 6000.6 docs have `AndroidApplication.currentFoldingFeatures`, `onFoldingFeaturesUpdated`, `onConfigurationChanged`, `isInMultiWindowMode` and `AndroidFoldingFeature`. `AndroidFoldingFeature` wraps WindowManager's `FoldingFeature`, including its state.
- VERIFIED: those pages return 404 for 6000.0 to 6000.4. So the 6.3 LTS has only `onConfigurationChanged`, and you'd have to use the non-LTS 6.5+ stream to get fold support.
- VERIFIED: the Unity Test Framework runs from the command line (`-runTests -batchmode -testResults`).
- INFERRED: builds run as `Unity.exe -batchmode -executeMethod`. Scenes and prefabs are YAML with GUID `.meta` files, which are fragile for an AI to edit. The Personal licence is activated through Unity Hub. Tiled maps would come in through SuperTiled2Unity. UI Toolkit menus are UXML/USS text.

**libGDX:**
- VERIFIED: `TmjMapLoader.java` exists on master, as does `AtlasTmjMapLoader`. 1.14.0 added a "Universal Tiled Map Loader" and Tiled template objects.
- INFERRED: the Android backend is an ordinary Activity, so Jetpack WindowManager is just a Gradle dependency. The headless backend plus JUnit gives full automated tests. Builds are `./gradlew android:assembleRelease`. The menu toolkit (Scene2D UI) is the weak spot.

**Flutter + Flame:**
- VERIFIED: `MediaQuery.displayFeatures` reports hinge and fold bounds plus a posture state on Android.
- VERIFIED: flame_tiled reads TMX only and calls itself "in progress".
- VERIFIED: the gamepads plugin is still pre-1.0. On Android, the app's Activity has to forward controller events to it. It does give a normalized Xbox-style button layout.

**MonoGame:**
- VERIFIED: MonoGame.Extended loads Tiled maps only as `.tmx`, through its content pipeline.
- VERIFIED: 3.8.4 fixed Android gamepad problems.
- INFERRED: Jetpack WindowManager is reachable through the Xamarin.AndroidX.Window bindings.
- FNA has no official Android target (INFERRED).

**Defold:**
- VERIFIED: `bob.jar` does resolve, build and bundle from the command line, with `--platform armv7-android`, `--bundle-format apk,aab`, keystore options and a headless engine variant.
- VERIFIED: Tiled can export Defold `.tilemap` files.
- VERIFIED: the Defold License 1.0 is based on Apache 2.0.
- INFERRED: fold posture would need a native extension, which is compiled on Defold's build server.

**Ebitengine:**
- VERIFIED: `ebitenmobile bind -target android` produces an `.aar` containing an `EbitenView`, which you put inside your own Activity. That makes WindowManager access direct (INFERRED).
- INFERRED: the UI library (ebitenui) is thin.

**Cocos Creator:** VERIFIED: the docs say command-line builds "still need the GUI environment", which is a problem for headless builds.

**GameMaker:** VERIFIED: free for non-commercial use. A new GM-CLI toolchain was announced in the Spring 2026 update. There is no headless test story.

**RPG Maker MZ:** INFERRED: Android builds go through a web export inside a WebView/Cordova wrapper, which repeats what was already rejected. The data files are JSON.

**Pokémon Essentials:** INFERRED: maps are binary Ruby Marshal `.rxdata` files, and there is no native Android build (players use the third-party JoiPlay app).

**Solarus:** VERIFIED: the 2025 retrospective says the Android port was still in development. The engine is built for Zelda-style action games, not turn-based battles.

**Bevy:** INFERRED: every release breaks the API, the Android toolchain is rough, and the UI is minimal.

**Audio, all engines:** INFERRED: none plays MIDI with an SF2 soundfont natively. Pre-render the music to OGG with FluidSynth whichever engine you pick.

### The two strongest challengers

1. **libGDX with Kotlin.** It scores highest for this way of working: plain code with no editor, Gradle builds from the command line, full headless tests, built-in `.tmj` loading, direct Jetpack WindowManager access for tabletop posture, and the best battery use. The cost is that you build the menu framework, tweens, animation and cutscene tooling yourself on top of Scene2D UI, and its RPG ecosystem is smaller.
2. **Unity 6.6 (2D).** It is the only engine here with a built-in fold-posture API, and it has the best controller and touch input and the biggest RPG ecosystem. C# is easy for an AI to write. Against that, the editor-centred workflow, YAML scenes with `.meta` files, slow batch builds, Hub licence activation and the non-LTS requirement for fold support all count against it.

Next tier: Flutter + Flame (best for menus and foldables, but gamepad support is immature and Tiled support is TMX-only), then MonoGame + Gum, Defold and Ebitengine.

### Clearly worse for this project

- **FNA:** no official Android target.
- **Construct 3:** browser editor, event sheets, WebView runtime, cloud builds. No command-line or AI-friendly workflow.
- **RPG Maker MZ:** WebView runtime with GUI-editor maps; this is the same path already rejected for goldensun_html5.
- **Pokémon Essentials / mkxp-z:** RPG Maker XP with binary maps, no native Android, and core releases frozen since 2023.
- **GameMaker:** GUI-centred, its command-line tools are only just arriving, no headless tests, and no Tiled pipeline.
- **Solarus:** action-RPG engine whose Android port is still unfinished.
- **LÖVE:** last release December 2023, and no UI toolkit.
- **raylib:** C with no tilemaps or UI; same problems as the rejected C/SDL3 route.
- **Bevy:** frequent breaking changes, immature Android support, weak UI.
- **Heaps:** Android build through HashLink/C is painful.
- **Cocos Creator:** command-line builds need a GUI session, and it is editor-centric.
- **KorGE:** no release in about 17 months.
- **GDevelop:** no-code editor.
- **Phaser + Capacitor:** another WebView approach.
- **Redot:** a Godot fork that adds nothing for this project.

### Sources
- https://services.api.unity.com/unity/editor/release/v1/releases
- https://docs.unity3d.com/6000.6/Documentation/ScriptReference/Android.AndroidFoldingFeature.html
- https://docs.unity3d.com/6000.3/Documentation/ScriptReference/Android.AndroidApplication-onConfigurationChanged.html
- https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html
- https://api.github.com/repos/{defold/defold, libgdx/libgdx, MonoGame/MonoGame, FNA-XNA/FNA, MonoGame-Extended/Monogame-Extended, love2d/love, love2d/love-android, raysan5/raylib, bevyengine/bevy, HeapsIO/heaps, HaxeFlixel/flixel, openfl/lime, Maruno17/pokemon-essentials, mkxp-z/mkxp-z, hajimehoshi/ebiten, cocos/cocos-engine, korlibs/korge, 4ian/GDevelop, godotengine/godot, axmolengine/axmol, coronalabs/corona, phaserjs/phaser, Redot-Engine/redot-engine}/releases
- https://raw.githubusercontent.com/libgdx/libgdx/master/CHANGES
- https://libgdx.com/wiki/graphics/2d/tile-maps
- https://raw.githubusercontent.com/godotengine/godot/master/platform/android/java/lib/build.gradle
- https://docs.godotengine.org/en/stable/classes/class_displayserver.html
- https://lunatik-games.itch.io/godot-android-foldable-screen
- https://pub.dev/packages/flame
- https://pub.dev/packages/gamepads
- https://docs.flame-engine.org/latest/bridge_packages/flame_tiled/flame_tiled.html
- https://api.flutter.dev/flutter/widgets/MediaQueryData/displayFeatures.html
- https://storage.googleapis.com/flutter_infra_release/releases/releases_windows.json
- https://www.monogameextended.net/docs/features/tiled/
- https://azuresearch-usnc.nuget.org/query?q=MonoGameGum
- https://defold.com/manuals/bob/
- https://doc.mapeditor.org/en/stable/manual/export-defold/
- https://ebitengine.org/en/documents/mobile.html
- https://docs.cocos.com/creator/3.8/manual/en/editor/publish/publish-in-command-line.html
- https://gitlab.com/api/v4/projects/solarus-games%2Fsolarus/releases
- https://solarus-games.org/news/2026-03-05-solarus-in-2025-a-retrospective/
- https://gms.yoyogames.com/update-win.rss
- https://gamemaker.io/blog/update-spring-2026
- https://gamemaker.io/en/get
- https://editor.construct.net/versions.json
- https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1096900