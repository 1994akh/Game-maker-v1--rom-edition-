**Verdict: Unity 6.6 (2D) does not beat Godot 4.7.2 for this project.** It is a credible alternative, not a better one. It wins on three things: the fold API is built in, C# ports cleanly from goldensun_html5's TypeScript, and it can run automated tests on the phone itself. It loses on three that matter more for an AI-driven, command-line workflow: the free licence can only be activated by signing in to Unity Hub, ARM64 builds require IL2CPP and are slow, and an engine migration lands in the middle of development (6.6, then 6.7 LTS as "our final release built upon Mono", then 7.0 on CoreCLR). Estimated vertical slice: 7–9 weeks, against 6–8 for Godot.

## Strongest case for Unity

1. **Fold 7 support is built in, with no Kotlin plugin.** `AndroidApplication.currentFoldingFeatures`, `onFoldingFeaturesUpdated`, `onConfigurationChanged`, `isInMultiWindowMode`, `currentWindowInsets` and `onWindowInsetsChanged` all exist. `AndroidFoldingFeature` has `bounds`, `isSeparating`, `occlusionType`, `orientation` and `state`. VERIFIED in the 6000.6 docs; the 6000.4 page has only `onConfigurationChanged`, so these arrived in 6.5.
2. **goldensun_html5 ports more cleanly to C#.** Classes, interfaces, generics, enums and lambdas map almost one-to-one from TypeScript (INFERRED). The battle, formula, Djinn and save logic can live in a plain C# assembly that doesn't reference the engine. It can be tested with `dotnet test` in seconds, without the editor or a licence, against golden JSON files produced by our Python reference (INFERRED). Godot's C# build gives the same benefit, so this edge is not unique to Unity (INFERRED).
3. **Testing is strong, including on the phone.** VERIFIED: `Unity.exe -runTests -batchmode -projectPath P -testPlatform EditMode|PlayMode|<BuildTarget> -testResults x.xml` writes NUnit XML. The docs say any BuildTarget runs PlayMode tests "on a player built for the specified platform", so `-testPlatform Android` should run them on the Fold 7.
4. **There is a new, agent-friendly Unity CLI (experimental).** VERIFIED:
   - Install with `winget install Unity.CLI`, then `unity install 6000.6.5f1 -m android --cm`.
   - It also offers `unity build`, `unity test`, `unity recompile --strict` and `--format json`.
   - Exit codes are fixed; 8 means tests ran and failed.
   - Controlling the editor needs the "Unity Pipeline package".
5. **Faster Android iteration.** VERIFIED: "Patch And Run" sends only changed scripts to the phone, using `BuildOptions.PatchPackage | AutoRunPlayer | Development`. It works only for Development builds, and the first patch is slower.
6. **Input.** VERIFIED: Input System 1.14.2 on Android supports Xbox One pads (yes), DualShock (Android 10+), DualSense (Android 12+), the touchscreen, and generic HID devices. The Player settings have an "Android Gamepad Support Level" and a choice of Activity or GameActivity entry point. INFERRED: the Backbone shows up as a standard Android gamepad.
7. **Menus are text files.** VERIFIED: UI Toolkit (UXML/USS) supports runtime data binding, UI transition animations and adaptive layout. That suits a game with many menus written by Claude.
8. **Ecosystem.**
   - VERIFIED: Unity's official MCP server lets Claude Code read and edit the scene hierarchy, components, scripts and console. It needs the AI Assistant package, a project connected to Unity Cloud, and "an active trial or subscription to Unity's AI tools beta".
   - INFERRED: Timeline, Cinemachine, 2D Tilemap, Pixel Perfect Camera and the URP 2D renderer (2D lights, Shader Graph) suit the later graphics pass. LLMs know Unity C# better than any other engine.

## Strongest case against Unity

1. **The licence needs the GUI.** VERIFIED (6.6 manual): command-line activation "doesn't support … Unity Personal". You activate by logging in to Unity Hub and return the licence by logging out. INFERRED: if that login lapses, unattended builds stop until the user signs in again.
2. **The fold API forces the non-LTS stream into an engine migration.** VERIFIED:
   - Update releases are supported only "until the next release is published". 6.3 LTS runs to December 2027, and the fold API is not in it.
   - Unity's June 2026 post: 6.7 LTS is the "final release built upon Mono". 7.0 moves to CoreCLR (.NET 10, C# 14), removes Mono, and drops domain reload.
   - 6.6 deprecates `com.unity.serialization` and builds Burst into the engine.
   - A 6.6 → 6.7 → 7.0 upgrade therefore lands mid-project, with optimisation deferred to the LTS after 7.0 in 2027.
3. **IL2CPP only for ARM64.** VERIFIED: ARM64 is "enabled only when you set Scripting Backend to IL2CPP". INFERRED: full APK builds take minutes, against Godot's quick export packing. Patch And Run only partly helps.
4. **Install size: about 6.4 GB to download and about 18 GB on disk.** VERIFIED from the Unity release API for 6000.6.5f1 on Windows (download / installed):

   | Part | Download | Installed |
   |---|---|---|
   | Editor | 3.86 GB | 9.06 GB |
   | Android module | 1.33 GB | 5.85 GB |
   | NDK r27c | 0.78 GB | 2.36 GB |
   | JDK 17 | 0.12 GB | 0.24 GB |
   | SDK platforms, tools and command-line tools | about 0.4 GB | about 0.6 GB |

   Godot is far smaller (INFERRED).
5. **Scenes and prefabs are YAML with fileID/GUID cross-references and `.meta` files.** Claude cannot safely hand-write them (INFERRED). The workaround is one bootstrap scene, with everything built in code or generated by editor scripts run through `-executeMethod`. That throws away much of what the editor offers. Godot's `.tscn` files can be edited by hand (INFERRED).
6. **No ready-made Tiled `.tmj` importer.**
   - SuperTiled2Unity (MIT) last released 2.4.0 in July 2025. I found evidence of TMX support only, not `.tmj` (search result, not proof).
   - So we write our own `ScriptedImporter` (VERIFIED: the API registers a custom file extension), or convert to `.tmx` with the Tiled command line (INFERRED).
7. **Workflow friction (INFERRED).**
   - Batch mode won't open a project that is already open in the editor, so the user and Claude can't both have it open.
   - Every C# change triggers an editor recompile.
   - Asset Store packages need a signed-in GUI download, so we'd prefer OpenUPM or git packages listed in `manifest.json`.
   - The screening report scored Unity 3 for performance and battery, against Godot's 4.

## Architecture under Unity

- **`GS.Core`** (plain C#, no engine references): stats, formulas, battle state machine, Djinn, Pokémon catching, storage and evolution, the save model, and deterministic 8-way movement and collision on the height grid. Ported from goldensun_html5 (keep its MIT notice). Tested with `dotnet test` plus golden files from the Python reference.
- **`GS.Game`** (MonoBehaviours): rendering, input, UI Toolkit screens, and an event-script runner for cutscenes driven by JSON. Timeline is optional.
- **`GS.Editor`**:
  - An `AssetPostprocessor` sets PNG import rules in code: point filtering, no compression, a fixed pixels-per-unit.
  - A `.tmj` `ScriptedImporter` produces a Tilemap prefab plus a ScriptableObject holding height and collision data.
  - JSON tables become ScriptableObjects, or are parsed at runtime.
  - `Build.cs` holds the build entry points.
- **Audio:** render MIDI with the SF2 soundfont to OGG offline using FluidSynth, the same as for Godot.

## Vertical slice

Each row is Claude coding time; a user play-test follows each milestone.

| Week | Work | Play-test |
|---|---|---|
| 1 | Toolchain (user signs in to Hub once), assemblies, `manifest.json`, `Build.cs`, adb deploy, touch and pad echo on both screens, first oracle test | APK runs on cover and inner screens |
| 2 | `.tmj` importer, sprite rules, pixel-perfect camera for 21:9 and roughly 1:1 | — |
| 3 | 8-way movement on the height grid, NPC, portrait dialogue, on-screen stick plus pad | Walk the map |
| 4 | Move Psynergy puzzle, event runner, fold and tabletop layout | Puzzle and posture |
| 5–6 | Battle core port (4 Adepts + 4 partner Pokémon vs up to 6 enemies, oracle-checked), then battle presentation and targeting | — |
| 7 | Battle UI on both screens with controller, save/load | Full battle |
| 8–9 | Fixes from play-tests, IL2CPP release performance, fold-switch edge cases | Final slice |

**Estimate: 7–9 weeks** (INFERRED). The C# port and the built-in fold API save about a week compared with Godot. Unity setup, the IL2CPP build loop and code-only scene building cost about 1.5–2 weeks.

## Building, testing and deploying from the command line on Windows

**What the user installs:**
- Unity Hub, with one sign-in.
- Either `winget install Unity.CLI` then `unity install 6000.6.5f1 -m android --cm`, or the same through Hub. This brings the JDK, SDK, NDK and platform-tools (adb) with it.
- A .NET SDK for the core tests (about 0.5 GB, INFERRED).
- FluidSynth (small, INFERRED).

**Commands:**
- **Build:**
  - `Unity.exe -batchmode -quit -projectPath . -buildTarget android -executeMethod Build.AndroidDev -logFile -`
  - or `-activeBuildProfile <profile> -build out.apk`
  - (VERIFIED flags)
- **Test:**
  - `-runTests -testPlatform EditMode|PlayMode|Android -testResults r.xml`. The docs warn that tests may not finish when combined with `-quit`.
  - `dotnet test` for `GS.Core`.
- **Deploy:** `adb install -r`, ideally over wireless adb to the Fold 7 (INFERRED).

## Fold 7 specifics

- **Cover and inner screens behave differently on Android 16.** VERIFIED: for apps targeting API 36, on screens of 600dp or more (the inner screen), Android ignores `screenOrientation`, `resizableActivity` and `min`/`maxAspectRatio`. Exceptions are games flagged through `android:appCategory`, and screens under 600dp (the cover screen). The opt-out property stops working at API 37.
- **Action:** check the merged manifest for the game category (INFERRED that Unity may not add it by default). Either way, show more of the map rather than letterboxing.
- **Switching screens:** a configuration change. Keep "Resizeable Activity" on (VERIFIED setting) and handle the change in `onConfigurationChanged`. Confirm on the phone that the activity is not restarted (INFERRED).
- **Tabletop:** `onFoldingFeaturesUpdated` reporting a half-open state with a horizontal hinge puts field or battle on top and menus and touch controls below. The API is VERIFIED; reading those values as tabletop follows Android's FoldingFeature semantics (INFERRED).
- **Frame rate:** "Optimized Frame Pacing" and "Sustained Performance Mode" are available (VERIFIED).
- **Controllers:** try both the Activity and GameActivity entry points with the Backbone (INFERRED).

## Long-term maintenance and the later passes

- **Engine upgrades:** the 6.6 → 6.7 LTS → 7.0 CoreCLR jump (VERIFIED). Static state now survives Play-mode entry (VERIFIED), and plugins may break (INFERRED).
- **Graphics pass:** strong. Re-import sprites, use the URP 2D lights and Shader Graph, Sprite Library swaps, and a pixels-per-unit change for HD art (INFERRED).
- **Music pass:** swap the OGG files and use AudioMixer snapshots. MIDI at runtime would need an Asset Store plugin (INFERRED).

## Risks and mitigations

1. **Hub login lapses and breaks builds.** Ask the user to re-login; check licence state before every build script runs.
2. **CoreCLR migration mid-project.** Keep `GS.Core` as plain C#, avoid native plugins, budget about 1 week for the 7.0 upgrade.
3. **Slow IL2CPP builds.** Use Patch And Run for daily work and full builds weekly.
4. **YAML edits go wrong.** Never hand-edit scenes; generate them from editor scripts.
5. **No `.tmj` importer.** Write our own (about 1 week).
6. **Android 16 orientation rules.** Set the game category and design for both aspect ratios.

**When to switch to Unity:** only if, in Godot's first two weeks, the Kotlin fold plugin or Backbone input proves unworkable.

The script that reads the install sizes from the Unity release API is saved at (a local scratch script, not kept).

**Sources (VERIFIED today):**
- https://docs.unity3d.com/6000.6/Documentation/ScriptReference/Android.AndroidFoldingFeature.html
- https://docs.unity3d.com/6000.6/Documentation/ScriptReference/Android.AndroidApplication.html
- https://docs.unity3d.com/6000.4/Documentation/ScriptReference/Android.AndroidApplication.html
- https://docs.unity3d.com/6000.5/Documentation/Manual/WhatsNewUnity65.html (search result)
- https://unity.com/releases/unity-6/support
- https://docs.unity3d.com/Manual/ManualActivationCmdWin.html
- https://docs.unity3d.com/6000.6/Documentation/Manual/EditorCommandLineArguments.html
- https://docs.unity3d.com/6000.6/Documentation/Manual/android-requirements-and-compatibility.html
- https://docs.unity3d.com/6000.6/Documentation/Manual/class-PlayerSettingsAndroid.html
- https://docs.unity3d.com/6000.6/Documentation/Manual/android-AppPatching.html
- https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/SupportedDevices.html
- https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html
- https://docs.unity3d.com/6000.6/Documentation/ScriptReference/AssetImporters.ScriptedImporter.html
- https://docs.unity3d.com/6000.6/Documentation/Manual/UI-system-compare.html
- https://discussions.unity.com/t/coreclr-scripting-and-serialization-update-june-2026/1723299
- https://docs.unity.com/en-us/hub/hub-cli
- https://docs.unity.com/en-us/unity-cli/unity-cli
- https://docs.unity.com/en-us/unity-cli/unity-cli-reference
- https://docs.unity.com/en-us/unity-cli/use-unity-cli
- https://unity.com/blog/unity-ai-mcp-how-to-get-started
- https://unity.com/products/unity-personal
- https://services.api.unity.com/unity/editor/release/v1/releases?version=6000.6.5f1&platform=WINDOWS&architecture=X86_64
- https://seanba.itch.io/supertiled2unity
- https://github.com/Seanba/SuperTiled2Unity
- https://developer.android.com/about/versions/16/behavior-changes-16