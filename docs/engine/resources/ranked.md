## Resources for the Golden Sun + Pokémon Godot build: what to get and what to skip

**About the Golden Sun decompilation you uploaded:** `goldensun-master` is Golden Sun 1 only, and its functions are named only by address. Use it to look up addresses while tracing in an emulator. alchemy is still the better source for porting.

Labels: **V** means seen today, **V\*** means I re-checked it in this pass, **I** means inferred. 25 tool calls; nothing was downloaded. GitHub's API rate limit ran out partway through, so a few rows rely on the earlier reports from today.

### Corrections to the two reports
1. **Android 16 and the inner screen: the Godot report was wrong.** Godot 4.7.2 targets API 36, and its manifest marks the app as a game. Android 16 exempts games from its rule that ignores orientation and resizability locks on large screens (V\*).
   - The landscape lock is therefore respected on the inner screen, and we don't need to plan a portrait-only layout.
   - Still set `resizeableActivity="true"`. Otherwise folding or unfolding can drop the game into compatibility mode (I).
2. **GUT: install v9.7.1 from the `godot_4_7` branch.** The "latest release", v9.6.1, and the main branch are both for Godot 4.6 (V\*). The licence is MIT according to the README; the API shows none.
3. **YATI: the current version is v2.2.10** (released 2026-10-05), not 2.2.9 (V\*).
   - The README doesn't mention a post-import hook or Tiled "class" support, so plan to post-process imported maps ourselves (I).
   - Animated tiles must have evenly spaced frames in one row or column.
4. **agbplay has no stable release.**
   - Windows builds are nightly pre-releases; the latest is 2026-09-24 (V\*).
   - Exporting each instrument track to its own file only works in the old text-mode interface.
   - The README doesn't mention Golden Sun's synth instruments.
5. **arlez80/godot-midi-player works only with Godot 3.4/3.5** (V\*). The "MIDI Player 4" store listing is a separate download that I didn't re-check. Skip both.
6. **PokeAPI's Gen 1–7 filter needs one fix.** Version group 18 is Ultra Sun/Ultra Moon (V\*). Meltan and Melmetal (#808–809) first appear in Let's Go (version group 19), so the filter leaves them with no moves. Fall back to group 19 or 20 for those two (I).
7. **LimboAI v1.8.1 is built against Godot 4.7.2-stable** (V\*). The release's file list didn't load, so the claim that it ships Android libraries wasn't re-confirmed.
8. **The Android plugin template exists** (MIT, Godot 4.2+, V\*), but the first build doesn't need it. Godot already treats folding and unfolding as a window resize. **I moved it to "Get later".**

These also checked out:
- Dialogue Manager 4 requires Godot 4.6+ (V\*).
- The VirtualJoystick node is in the 4.7 docs. Its deadzone defaults to 0, so we need to set one (V\*).
- godot-open-rpg needs Godot 4.7.2 and uses Dialogic (V\*).
- Fold 7 screens are 2520×1080 (cover) and 2184×1968 (inner) (V\*).
  - Cover screen: 6× scale, showing 420×180 GBA-size pixels.
  - Inner screen, landscape: 9× scale, showing 242×218.
  - Inner screen, if portrait is ever allowed: 8× scale, showing 246×273.

### Get now (first 6 weeks: walking, a Move puzzle and one 4+4 battle on the Fold 7)
1. **Godot 4.7.2's Android build template** (built in). No plugin needed.
   - Export with the Gradle build and set `resizeableActivity="true"`.
   - Keep App Category set to Game. I believe that is the default (I).
   - React to `NOTIFICATION_WM_SIZE_CHANGED` to re-lay out the screen.
   - Use the stretch settings `viewport` / `expand` / `integer`.
   - **Saves:** a foldable plugin and any pixel-scaling addon.
2. **YATI v2.2.10.** https://github.com/Kiamo2/YATI, MIT, released 2026-10-05; tested on Godot 4.7.2 with Tiled 1.12.2 (V\*).
   - Turn off "Use multiple threads" in the editor's import settings, or Godot can freeze or crash.
   - **Saves:** writing our own importer for our .tmj maps, including collisions, custom properties and animated tiles.
3. **GUT v9.7.1.** https://github.com/bitwes/Gut, branch `godot_4_7`, MIT; last push 2026-08-18 (V\*).
   - **Saves:** a test runner. It runs from the command line and writes JUnit reports, which covers checking the Golden Sun formulas against our Python reference.
4. **The built-in VirtualJoystick and TouchScreenButton** (in Godot itself, V\*). Use them for 8-way movement plus A/B/L/R/Psynergy buttons.
   - **Saves:** any touch-control addon.
5. **PokeAPI CSVs.** https://github.com/PokeAPI/pokeapi, folder `data/v2/csv`, BSD-3, pushed 2026-10-13 (V\*).
   - One saved Python script converts the CSVs to JSON.
   - **Saves:** typing in data for the battle's partner and enemy Pokémon, and later the whole Gen 1–7 roster plus Megas.
6. **godot-open-rpg (read only).** https://github.com/gdquest-demos/godot-open-rpg, MIT code, needs 4.7.2 (V\*).
   - **Saves:** design time on the battle turn order, the battler/action structure and overworld triggers.
7. **mGBA.** https://github.com/mgba-emu/mgba, MPL-2.0, pushed 2026-10-08 (V, earlier report).
   - **Saves:** guessing how the original behaves. Save states let us compare our Move puzzle and battle timing frame by frame.

### Get later
**Content phase**
- **Dialogue Manager v4.1.0.** MIT, pushed 2026-10-13, needs Godot 4.6+ (V\*). A script turns our extracted Golden Sun text into its dialogue files; we build a Golden Sun-style text box.
- **LimboAI v1.8.1.** MIT (V\*). Behaviour for partner Pokémon and field enemies.
- **Showdown data.** https://github.com/smogon/pokemon-showdown, MIT (V). Cross-checks move effects.
- **Coaltergeist/goldensun-decomp.** No licence, pushed 2026-10-12, Golden Sun 1 only (V\*). Gives names for functions alchemy still leaves in assembly.
- **luvdis.** Already on disk at `Apps-Roms\luvdis-main` (MIT). Your Lost Age ROM is in the same folder, so luvdis can produce a Lost Age disassembly. The references report found no public one. **Saves:** an address map for tracing the world map, ship, Hover and Teleport.
- **goldensunwiki.net.** CC BY-SA (V). Rules for Teleport, Hover and the ship.
- **Godot-Android-Plugin-Template.** https://github.com/m4gr3d/Godot-Android-Plugin-Template, MIT (V\*). Only if we use the hinge, for example tabletop posture.
- **Only if needed:**
  - gdUnit4 (MIT, V) for scripted touch or UI tests.
  - godot_input_helper (MIT, V) as a reference for switching button icons per controller.
  - godot-statecharts (MIT, V) for the player's field states.

**Graphics pass**
- **Aseprite with godot-aseprite-wizard.** The wizard is MIT, pushed 2026-08-17 (V); 4.7 support is (I). **Saves:** writing our own sprite-sheet and animation importer.
- **Pixelorama** (MIT, V): a free alternative to Aseprite.
- **phantom-camera** (MIT, V): only if we recreate Golden Sun's rotating battle camera.

**Audio pass**
- **agbplay nightly.** LGPL-3.0, Windows build (V\*). Renders Golden Sun 1 and Lost Age music straight from the ROMs, with Camelot's sound engine and reverb.
- **FluidSynth CLI.** LGPL-2.1 (V). Renders our MIDI + SF2 files offline to OGG with loop points.
- **Polyphone.** GPL-3.0 (V). Fixes the soundfonts.

### Files you could add
1. **mGBA save states (.ss1) for Golden Sun 1**, one next to a Move-pillar puzzle and one just before a battle starts. These unblock the frame-by-frame comparison for the first build. The `.sav` you already have can't be loaded into a chosen spot the way a save state can.
2. **A Lost Age `.sav` from late in the game**, with the Teleport Lapis, Hover and Wings of Anemos. It unblocks tracing the world map, ship, Hover and Teleport. The ROM is already on disk, but there are no Lost Age saves.
3. **A note of the story point of your existing Golden Sun 1 save.**
4. **Optional:** the GBA BIOS dumped from your own hardware, for more accurate mGBA traces, and any Lost Age Action Replay codes you use, which reveal memory addresses.

### Skip
- **Tiled's built-in Godot export:** it drops custom properties on objects.
- **vnen's Tiled importer:** Godot 3 only.
- **Dialogic 2:** still alpha, built for visual novels, and hard to generate content for.
- **Playing MIDI live in Godot (arlez80 and the other MIDI add-ons):** Godot 3, unproven, or heavy on a phone's CPU.
- **Lunatik foldable plugin:** paid, and supports Godot 4.1 at most.
- **Third-party virtual joysticks and SDL_GameControllerDB:** the built-in node covers the joystick, and Godot doesn't use SDL on Android.
- **Beehave:** overlaps LimboAI.
- **godot-ci and setup-godot:** only matter if we set up CI; local exports are enough.
- **Pokémon and Golden Sun Godot clones and other turn-based addons:** licence problems, outdated Godot versions or very little real code.
- **PokeAPI api-data and veekun:** the CSVs are easier to use, and veekun is stale.
- **camelot-gcc:** only matters for byte-matching builds, and we are porting.
- **Zaxaerith recomp:** machine-made C++ with no names; a last resort only.
- **gsrandroid:** Golden Sun 1 only and "super beta". Use it only if you want the original on the Fold for side-by-side play.
- **golden-sun-collection, Open-GSTLA, Atrius's editor, GoldenSunHacking/Psynergy:** combining ROMs, empty, or covered by gsmagic and our own extraction.
- **Real-ESRGAN and waifu2x:** they smear pixel art.
- **Free Texture Packer, LibreSprite, VGMusicStudio:** stale or already covered by other tools.
- **SaveMadeEasy and safe-resource-loader:** we're writing our own versioned JSON saves.
- **Folders on disk that don't fit:**
  - Godot-Grid-Based-Movement does grid movement and expects a `TileMap` node, but our design uses free 8-way movement.
  - awake, Il2CppDumper, ds-decomp, oot, pikmin2 and gba-obj-sprite-maker are unrelated.

Sources: [YATI](https://github.com/Kiamo2/YATI) · [GUT](https://github.com/bitwes/Gut) · [Dialogue Manager](https://github.com/nathanhoad/godot_dialogue_manager) · [LimboAI v1.8.1](https://github.com/limbonaut/limboai/releases/tag/v1.8.1) · [VirtualJoystick docs](https://docs.godotengine.org/en/stable/classes/class_virtualjoystick.html) · [Godot 4.7.2 AndroidManifest](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/platform/android/java/app/src/main/AndroidManifest.xml) · [Godot 4.7.2 config.gradle](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/platform/android/java/app/config.gradle) · [Android 16 behaviour changes](https://developer.android.com/about/versions/16/behavior-changes-16) · [Fold 7 specs (Wikipedia)](https://en.wikipedia.org/wiki/Samsung_Galaxy_Z_Fold_7) · [Fold 7 specs (TechRadar)](https://www.techradar.com/phones/samsung-galaxy-phones/samsung-galaxy-z-fold-7-specs) · [PokeAPI version_groups.csv](https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/version_groups.csv) · [agbplay](https://github.com/ipatix/agbplay) · [agbplay releases](https://github.com/ipatix/agbplay/releases) · [arlez80 MIDI player](https://github.com/arlez80/godot-midi-player) · [Android plugin template](https://github.com/m4gr3d/Godot-Android-Plugin-Template) · [godot-open-rpg](https://github.com/gdquest-demos/godot-open-rpg) · [gsrandroid](https://github.com/wootbeer/gsrandroid) · [goldensun-decomp](https://github.com/Coaltergeist/goldensun-decomp)