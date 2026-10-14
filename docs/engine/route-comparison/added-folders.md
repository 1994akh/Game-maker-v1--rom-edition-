**New folders in Apps-Roms: verdicts, plus deep-dives on tmc and butterfly**

Only tmc-master and nxemu-master are worth using, and only as references to read. Nothing is used as-is. tmc-master is the clearest spec for free 8-way movement and field puzzles. butterfly-develop is too old to add as a dependency. I only read files and ran nothing, including `install.bat` in tilemap-studio and the bundled `aoi.exe`/`clang-format.exe` in pikmin2. I wrote no files. The fit report's claims about tmc (Q16.16 position, 32-step direction, `LinearMoveUpdate`, radius-based tile collision, `collisionLayer`) are all VERIFIED in the local copy.

## 1. Table

| Folder | What it is | Licence | Verdict |
|---|---|---|---|
| **tmc-master** | zeldaret Minish Cap decomp (GBA, C plus some asm). No ROM is present; building needs `tmc.gba` sha1 `b4bd50e4…` (README). It builds a GBA ROM, not an Android app. | No licence file (VERIFIED) | **REFERENCE**, the best one for movement, collision, entities and puzzle objects (see deep-dive A). Re-implement from it rather than copying. The Android-capable fork is 999sian/tmc ("Picori"), which is not this folder. |
| **butterfly-develop** | GetStream Butterfly 1.0.2: a 1,050-line Kotlin wrapper over Jetpack WindowManager, with core, Compose and LiveData modules | Apache-2.0 | **REFERENCE.** Don't add it as a dependency. Use `androidx.window` 1.5.x directly and copy the roughly 30 lines of posture logic if wanted (see deep-dive B). |
| **nxemu-master** | Switch emulator (yuzu-derived) with an Android app: 36 Kotlin files, compileSdk/targetSdk 36, minSdk 28, NDK 26.1, arm64 only, `androidx.window` 1.3.0 | GPL-3.0 | **REFERENCE** for the native-app route, as an Android shell pattern. Files: `src/android/app/build.gradle.kts` (NDK/CMake/arm64 setup); `ui/emulation/EmulationActivity.kt` (SurfaceView at :156-174, gamepad keys and motion at :205-227); `overlay/InputOverlay.kt` (1,005 lines) with the `InputOverlayDrawable{Button,Dpad,Joystick}.kt` touch controls; `ui/settings/OverlayLayoutActivity.kt` (user-editable control layout); `utils/InputHandler.kt`. Copying code is fine for personal use, but the app becomes GPL if it is ever shared. |
| **Godot-Grid-Based-Movement-main** | GDScript for Godot 4.2/4.3 (Player.gd 189 lines, Enemy.gd 242): tile-step movement with tweened interpolation, top-down or platformer | MIT | **REFERENCE, Godot route only.** The idea worth taking is a TileSet "custom data layer" (`get_custom_data("walkable")`) to carry our Golden Sun collision and behaviour flags. Its grid-step movement does not fit; Godot's own `CharacterBody2D.move_and_slide` already gives free 8-way movement (INFERRED). |
| **tilemap-studio-master** | Rangi42's C++/FLTK desktop tilemap editor (GB/GBA/NDS/SNES and pokeemerald formats); v4.0.1 has a prebuilt release | LGPL-3.0 | **LATER** (graphics pass), and only if we stay on the C/expansion route with GBA-format UI tilemaps (town map, battle backgrounds, menus). On any native or Godot route, use Tiled, which we already export to. |
| **gba-obj-sprite-maker-main** | Browser pixel editor that outputs GBA 4bpp sprite tiles and palettes as ARM assembly data | No licence file (VERIFIED) | **NOT RELEVANT.** It outputs GBA assembly data; our pipeline is PNG, and Aseprite or LibreSprite is better for the remake. |
| **awake-master** | Game Boy (GB/GBC, not GBA) decompiler in Python 2.7; the `roms/` folder has only a JSON file | GPL-3.0 | **NOT RELEVANT.** Wrong CPU (our games are GBA ARM), and our reverse-engineering already exists in gbax. |
| **ds-decomp-main** | `dsd`, a Rust toolkit for setting up Nintendo DS decomp projects (ROM extract/build, delink, objdiff) | MIT | **NOT RELEVANT.** No DS game is in scope. |
| **oot-main** | Ocarina of Time decomp (N64/GameCube, 3D). I didn't check `baseroms/` for ROMs. | No licence file | **NOT RELEVANT.** It's 3D on N64, and its mechanics don't carry over to a 2D GBA-style game. |
| **pikmin2-main** | Pikmin 2 decomp (GameCube). It bundles `aoi.exe` and `clang-format.exe`, which should not be run. | CC0 | **NOT RELEVANT.** |
| **Il2CppDumper-master** | Reverse-engineering tool for Unity IL2CPP games (Unity 5.3–2022.2) | MIT | **NOT RELEVANT.** Neither source game uses Unity. |

## 2. Deep-dive A: tmc-master (local paths are under `C:\Users\aaron\OneDrive\Apps-Roms\tmc-master\`)

Everything here was read in the code (VERIFIED) unless marked INFERRED. It can't be built without a Minish Cap ROM, and even then it only produces a GBA ROM, so it is a spec to read. Some core routines are still assembly: ice velocity is in `asm/src/player.s:492-680` and `ResetCollisionLayer` is at `asm/src/code_080043E8.s:223`.

### Player movement
- **Position.** `include/entity.h:225-227` stores x, y and z as Q16.16 fixed point. `:220` has `zVelocity` and `:221` has `speed` (Q8.8 pixels per frame).
- **Direction.** `:187` is a direction byte from 0 to 0x1F, which gives 32 directions. Eight of them are named (N=0x00, NE=0x04 … NW=0x1C) at `:70-79`. `include/player.h:116-118` defines the flags `DIR_DIAGONAL` (4), `DIR_NOT_MOVING_CHECK` (0x80) and `DIR_NONE` (0xFF).
- **Moving.** `src/physics.c:149-168` (`LinearMoveDirection`, `LinearMoveAngle`, `LinearMoveUpdate`) adds `sin[dir*8]×speed` to x and subtracts `sin[dir*8+64]×speed` from y, using a 256-step sine table.
- **Speeds.** `src/player.c:36-42`:
  - Walk 1.25 px/frame (`0x140`), about 75 px/s or 4.7 tiles/s at 60 fps (INFERRED arithmetic).
  - Roll 2.0, shield 0.75, Gust Jar 0.5, sword charge 0.875, burning 3.0, and slopes subtract 0.3125.
  - `UpdatePlayerMovement` (`src/playerUtils.c:2398`) adds `speed_modifier` and never lets speed fall below 0x20.
- **Input.** `src/code_0805EC04.c:73` (`UpdatePlayerInput`) turns the D-pad into a direction through a lookup table. The same function plays back scripted "player macros" (recorded input), which suits cutscenes.
- **For us.** Use the same model: a fixed-point or float position, a direction of 32 steps or a free angle, and a speed. An analog stick (Backbone or Xbox) just feeds an angle from `atan2`, so tmc's maths already handles it. Treat 1.25 px/frame as a placeholder; MOVEMENT.md already plans to measure Golden Sun's real walk speed with `gbax trace`.

### Tile collision, layers and heights
- **Per-tile collision.** `src/movement.c:282` (`IsTileCollision`) reads one byte per 16 px tile:
  - 0 means free.
  - Values below 0x10 are a mask of the four 8×8 quarters.
  - Other values select one of 10 shape functions (`TileCollisionFunction0-9`, `:61-257`) for diagonal and half-filled tiles.
  - 13 collision types (enum at `:14-30`) decide who is blocked by what.
- **Probing.** `:1604` (`CalculateEntityTileCollisions`) checks three points on each side of the hitbox that faces the movement, and stores the result as a bitfield. The player's hitbox is a 6×6 box with offsets {5,3,3,5} (`src/playerHitbox.c:3`).
- **Moving with sliding.** `:1697` (`ProcessMovementInternal`) maps the 32 directions onto 8 functions (`MoveNorth` at `:1742` through `MoveNorthWest` at `:2033`).
  - Corner correction: if only one front corner is blocked, the player is nudged sideways and the move is retried.
  - Diagonals slide along whichever axis is still free.
  - `ProcessMovement0..12` (`:2079-2258`) are wrappers for each collision type.
  - The player also slides along diagonal walls: `src/playerUtils.c` around 2410-2460 (`sub_08079E90`, `sub_08079F48`) turns the direction by ±45° when it touches one.
- **Layers and heights.**
  - `include/map.h` defines two 64×64 tile layers, `gMapBottom` and `gMapTop`. Each has `mapData`, `collisionData`, `tileTypes` and `actTiles` (special behaviours such as holes and jumping off walls).
  - Each entity has a `collisionLayer`: 1 bottom, 2 top, 3 both (`entity.h` enum). Collision only reads that layer's map.
  - Ladders and climbing set layer 3 (`src/player.c:3370`, `:3688`, `:3707`).
  - Height is handled separately through z: `PlayerJump` is at `player.c:833`, and ledges use `SURFACE_EDGE`.
- **Surfaces.**
  - The list of floor types (`include/player.h:184-230`) includes pit, slopes, ice, shallow and deep water, swamp, ladder, climbable wall, four conveyors, button and hole. Their handlers are the `SurfaceAction_*` functions at `player.c:3348-3792`.
  - Ice momentum is still assembly (`UpdateIcePlayerVelocity`, `AddPlayerVelocity`, `ClampPlayerVelocity`).
  - Swimming and diving (`PlayerSwimming` and `ToggleDiving`, `playerUtils.c` around 2990-3060; dive lasts 0x78 frames) are a reference for Surf and Dive with free movement.
- **For us (INFERRED).** Copy this structure: one collision byte per tile with quarter masks and slope shapes, an elevation or layer per entity, hitbox probing, and the corner nudge. That is the core of MOVEMENT.md's "Option B" (free movement) and should come to a few hundred lines in a native engine. On the Godot route, `move_and_slide` already handles the sliding, and tmc's corner nudge is the polish to add on top.

### Entity system
- **The entity record.**
  - `entity.h:171-256` is a 0x68-byte base record plus per-type fields.
  - Kinds (`:13-37`): PLAYER, ENEMY, PROJECTILE, OBJECT, NPC, PLAYER_ITEM, MANAGER.
  - Each entity also has `id`, `type` and `type2`, plus `action`/`subAction` indices into its own function tables (for example `PushableStatue_Actions[super->action](this)`).
  - Flags (`:40-48`) include `ENT_SCRIPTED`, `ENT_PERSIST` (survives room changes) and `ENT_COLLIDE`.
  - Update priorities (`:51-59`, logic in `src/entity.c:92-220`) decide which entities keep running during dialogue or cutscenes.
- **Storage and update.** There are 72 entity slots plus 32 manager slots in 9 linked lists. `UpdateEntities` is at `src/entity.c:224`, `GetEmptyEntity` at `:261` and `DeleteEntity` at `:364`. Collision between entities is in `src/collision.c` (`CollisionMain` `:63`, `IsColliding` `:185`): a 3-bit collision class is checked against a mask.
- **Room placement.** `include/room.h:97-109` (`EntityData`) holds kind, flags, id, type, type2, x, y and a sprite. It maps 1:1 onto the Tiled object layers we already export (INFERRED).
- **For us (INFERRED).** Use a data-driven entity list per map, a state machine per entity, update priorities to freeze the world under menus and text, and `ENT_PERSIST`-style flags for partner Pokémon and followers. The 72-slot limit doesn't apply to us.

### Puzzle objects (`src/object/`, 192 files)
How each maps to Golden Sun field Psynergy is INFERRED.

| tmc object (VERIFIED behaviour) | Golden Sun use |
|---|---|
| `pushableStatue.c` (319 lines) writes a solid collision tile (`SPECIAL_TILE_11`) where it stands and restores the original tile when it moves. It moves at speed 0x80, supports push and pull (`PLAYER_PULL`), and reacts to holes. Related: `pushableRock.c`, `blockPushed.c`, `pushableFurniture.c`, `pushableGrave.c`, the lever files. | **Move**: the same block mechanism, triggered from a distance |
| `smallIceBlock.c` (348): when pushed it slides, speeding up from 0x20 by 0x10 per frame to a 0x200 cap, until it hits something (`:100-101`, `:214-219`), then marks its tile `SPECIAL_TILE_90`. `bigIceBlock.c` (334) is melted by fire. | **Frost** pillars, ice-slide puzzles |
| `pressurePlate.c` (183): weight = player standing on it + up to 8 puzzle entities within 16 px; `type` sets the weight needed; sets or clears a flag, optionally toggling. | Floor switches; partner Pokémon could count as weight |
| `beanstalk.c` (357) + `beanstalkSubtask.c` (1314): grows in stages, marks `SPECIAL_TILE_23` on both layers (`:267-268`), then becomes a ladder (`:284`) | **Growth** (sprout to climbable vine), the closest direct match |
| `pullableMushroom.c` (463) | **Lash**, **Catch** |
| `pot.c` / `bush.c` with the carried-entity code (`entity.h:527-537`) | **Lift**, **Carry** |
| `whirlwind.c`, `fan.c`, `fanWind.c`, `giantLeaf.c` | **Whirlwind** |
| `button.c`, `hitSwitch.c`, `eyeSwitch.c`, `lightableSwitch.c`, `trapdoor.c`, `crackingGround.c`, `lockedDoor.c` | Switches hit by Psynergy (for example Pound), state-change props |
| `lilypadLarge.c` (628) | Rideable platforms on water; a pattern for Surf or ship transitions |

The common pattern is that an object stamps a special collision tile into the map and changes state through flags. That fits our existing field-Psynergy spec directly.

## 3. Deep-dive B: butterfly-develop (local paths are under `C:\Users\aaron\OneDrive\Apps-Roms\butterfly-develop\`)

### What it gives (VERIFIED)
- **Size classes.** `WindowSize`: Compact under 600 dp, Medium 600–839 dp, Expanded 840 dp and up. The thresholds and factory can be changed through `GlobalWindowSize`. It classifies by **width only** (`butterfly/.../WindowSize.kt:81-90`).
- **Posture.**
  - `Posture.Normal`, `TableTop` (half-open with a horizontal fold) and `Book` (half-open with a vertical fold), in `FoldingFeatures.kt:74-94`.
  - Helpers include `isFlat`, `isHalfOpened`, `isVertical` and the hinge size in px or dp.
  - `postureFlow` and `windowLayoutInfo` are Flow extensions on Activity and Fragment (`FlowExtensions.kt:50`).
- **Base classes.** `WindowInfoActivity` and `WindowInfoFragmentActivity` (extend `ComponentActivity`), `WindowInfoAppcompatActivity`, and `WindowInfoFragment`. Each has an `onWindowLayoutInfoUpdated` callback.
- **Compose and LiveData.** butterfly-compose provides `rememberWindowDpSize`, `postureState`, `windowLayoutInfoState`, `LocalWindowDpSize`/`LocalPosture` and `WindowOrientation`. butterfly-livedata has LiveData adapters.

### Versions (VERIFIED, `buildSrc/.../Configuration.kt` and `Dependencies.kt`)
- The library itself: minSdk 21, compileSdk/targetSdk 32, Java 8 target.
- Build tools: Kotlin 1.7.0, Android Gradle Plugin 7.2.0, Gradle 7.4.2.
- Jetpack: **`androidx.window` 1.1.0-alpha01, exported as `api`**; Compose 1.2.0-rc03 (compiler 1.2.0); activity-compose 1.4.0; lifecycle 2.4.0; coroutines 1.6.1. These are all 2022-era versions.

### Why only a reference
- Current `androidx.window` is **1.5.1 stable (19 Nov 2025)** (VERIFIED, [release notes](https://developer.android.com/jetpack/androidx/releases/window)). It now has:
  - a built-in `WindowSizeClass` with Large and XLarge breakpoints (1.5.0);
  - `supportedPostures` (1.4.0);
  - `WindowMetrics.widthDp`/`heightDp`.
- Butterfly's exported alpha dependency would clash with that and need excluding.
- Width-only classification is a poor fit for the tall cover screen and the near-square inner screen.
- `hingePxSize` decides by the device's screen orientation rather than the fold's orientation (`FoldingFeatures.kt:48-51`). That could give wrong hinge sizes; INFERRED.

### Fold 7 behaviour (INFERRED unless marked)
- **Cover screen:** no fold feature is reported, so posture is Normal and the size is Compact. Android's docs class the outer screens of large foldables as narrower than 600 dp (VERIFIED, [Android docs](https://developer.android.com/develop/adaptive-apps/guides/app-orientation-aspect-ratio-resizability)).
- **Inner screen, flat:** the fold reports FLAT, so posture is Normal and the size is Medium or Expanded.
- **Inner screen, half-open with the fold horizontal:** posture is TableTop (Samsung's Flex Mode). That suits the battle well: the field on the top half and the command menu or touch controls on the bottom.
- **Book posture:** field on one side, party or menu on the other, or ignore it.
- **Switching between screens** is a configuration change. Declare `configChanges` for screenSize, smallestScreenSize, screenLayout and orientation so the game isn't restarted.
- **Android 16 (targetSdk 36)** ignores orientation and resizability locks on screens 600 dp and wider, **except for games** flagged with `android:appCategory="game"` (VERIFIED, same Android docs). So declare it.

### How it plugs into each engine route (INFERRED)
- **Native Activity (C/C++ through SDL3 like Picori, or GameActivity/NativeActivity):**
  - Call `WindowInfoTracker.getOrCreate(activity).windowLayoutInfo(activity)` and `WindowMetricsCalculator` from Kotlin. SDL's Activity is a plain `Activity`, so either use a coroutine scope or the `window-java` callback adapter.
  - Pass size class, posture and the fold rectangle to C through one JNI call.
  - Menus can be a Compose layer over the SurfaceView, the same layering as nxemu's `InputOverlay.kt` (which imports `WindowMetricsCalculator`, VERIFIED).
- **Godot:**
  - Write a Godot 4.2+ Android plugin v2: an Android library depending on `org.godotengine:godot:<version>` with a `GodotPlugin` subclass ([Godot docs](https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html)).
  - In it, use `getActivity()` with `androidx.window` and emit a `posture_changed` signal to GDScript. This needs a Gradle-build export.
  - Size class needs no plugin; read it from `get_viewport().size`.
  - A paid itch.io plugin also exists ([Godot Android Foldable Screen](https://lunatik-games.itch.io/godot-android-foldable-screen)); I couldn't check its source.
- **WebView:**
  - The host Kotlin Activity watches `windowLayoutInfo` and pushes `{posture, foldRect, sizeClass}` into the page with `evaluateJavascript` or a WebMessage.
  - CSS media queries handle size by themselves.

### Minimums for our app
- Butterfly itself needs minSdk 21 and lifecycle-runtime-ktx 2.4.0 or later.
- The `androidx.window` release page doesn't state a minSdk.
- The Fold 7 runs Android 16, so the app should target SDK 36. Something like nxemu's minSdk 28 is reasonable (INFERRED).

Sources:
- https://github.com/zeldaret/tmc
- https://github.com/999sian/tmc
- https://developer.android.com/jetpack/androidx/releases/window
- https://developer.android.com/develop/adaptive-apps/guides/app-orientation-aspect-ratio-resizability
- https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html
- https://lunatik-games.itch.io/godot-android-foldable-screen
- Local: `docs/engine/gba-sources.md`, `C:\Users\aaron\Documents\Game-maker-v1\docs\phase1\MOVEMENT.md`, `C:\Users\aaron\Documents\Game-maker-v1\docs\phase1\CODEBASE.md`