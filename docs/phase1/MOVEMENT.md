# Movement sizing: grid diagonal walking (Option A) vs Golden Sun-style free 8-way movement (Option B)

> **Notes from the review ([REVIEW.md](REVIEW.md)):** all three latent diagonal bugs were re-checked and confirmed. Option A is widened to **2–4 weeks**, since touch-input feel and followers usually need iteration. Before tuning A, spend 1–2 days measuring Golden Sun's walk, run and diagonal speeds with `gbax trace`, so A's timing matches Golden Sun from the start.

Base checked: pokeemerald-expansion 1.17.2 (commit `8fb02c6f`), with pret pokefirered as reference. All paths below are relative to `expansion/` unless marked `pokefirered:`. Function counts come from a rough brace-depth parser, so they are about ±10%.

## TL;DR

- **The FireRed build uses the same field code as Emerald.** VERIFIED. `make firered` only sets `GAME_VERSION := FIRERED` and `MAP_VERSION := firered` (`Makefile:7-19`). The field files contain only `IS_FRLG` switches for music, credits and intro: `field_player_avatar.c:1135,1146,1565`, `event_object_movement.c:534-550`, `field_control_avatar.c:484,527`, `bike.c:1292`, `overworld.c:1307,1342,1941`. Everything below applies to the FRLG build.
- **Option A (diagonal steps on the tile grid) is cheap, because about half of it already exists.** The expansion already has:
  - the 8-direction enum and vectors;
  - 12 diagonal movement actions;
  - animation tables with diagonal entries;
  - diagonal sideways stairs;
  - a rule that keeps the player's facing cardinal while moving diagonally.

  It also has three latent out-of-bounds bugs that will fire as soon as a diagonal reaches the collision path, so they must be fixed first. Estimate: about 900–1,500 lines across 9–11 files, **2–3 weeks**, medium confidence (about 70%).
- **Option B (free movement) is large even in its narrow "hybrid" form.** In that form only the player moves freely, while NPCs, triggers, scripts and maps stay on the grid. Estimate: about 2,100–3,700 lines, mostly new code in its own file, **6–10 weeks**, low-to-medium confidence (about 40–50%). Making every object, script and NPC move freely ("full B") is 4–6+ months and not recommended on the GBA.
- **Recommendation: build A now, keep B as a later, optional "player free mode."** About 30–40% of A carries over into B: the input layer, the facing rule, the 8-direction follower logic, the test maps and the diagonal chasers. Decide on B after play-testing A on the Fold 7. A native Android port could do free or analog movement much more cheaply later.

---

## 1. Inventory of grid assumptions

Totals across `src/` (VERIFIED by the counter script and grep):

| Pattern | Functions | Files | Hits |
|---|---|---|---|
| `currentCoords` / `previousCoords` / `initialCoords` | 173 | 19 | 597 |
| Collision API (`MapGridGetCollisionAt`, `GetCollisionAtCoords`, `GetCollisionInDirection`, `GetCollisionFlagsAtCoords`, `IsElevationMismatchAt`, `DoesObjectCollideWithObjectAt`) | 38 | 11 | 55 |
| `MapGridGetMetatileBehaviorAt` / `MapGridGetMetatileIdAt` | 127 | 26 | 175 |
| `MOVEMENT_ACTION_*` in code | 54 | 17 | 303 (916 counting tables and headers) |
| Cardinal `DIR_NORTH/SOUTH/EAST/WEST` logic | 272 | — | 574 |
| `case DIR_NORTH:` / `case DIR_EAST:` switch labels | — | 11 | 76 |

Biggest users of coordinates: `event_object_movement.c` 84 of 852 functions, `wild_encounter_ow.c` 17, `follower_npc.c` 15, `field_player_avatar.c` 13, `faraway_island.c` 8, and `trainer_see.c`, `overworld.c` and `field_effect.c` 6 each.

Movement actions: there are 184 `MOVEMENT_ACTION_*` constants. 135 of them are per-cardinal variants (`..._UP/DOWN/LEFT/RIGHT`); only 12 are diagonal. In `event_object_movement.c`, 44 tables are indexed by `[DIR_EAST]`; 35 of those already have `[DIR_NORTHEAST]` entries (the animation tables), and the movement-action tables are the ones without.

| Area | Evidence (VERIFIED) | Grid assumption | Impact on A | Impact on B |
|---|---|---|---|---|
| Object coordinates | `struct ObjectEvent` `include/global.fieldmap.h:251-314`: `currentCoords`, `previousCoords`, `initialCoords` are tile `Coords16` (`:292-294`); `facingDirection:4` and `movementDirection:4` (`:295-296`, so 8 directions fit). `ShiftObjectEventCoords` `event_object_movement.c:3386` | One tile per object, occupying current and previous tile while moving | None; a diagonal step is still one tile | Keep the struct. Derive the player's "anchor tile" from a pixel position so the 173 readers keep working |
| Movement actions and direction tables | Tables `event_object_movement.c:1005-1290`. `dirn_to_anim` macro `:6826-6835` bounds-checks with `direction > sizeof(table)`, an off-by-one. Walk tables have 5 entries (`:1023-1064`) | Walk, run, slide and jump tables only cover `DIR_NONE..DIR_EAST` | Must add diagonal entries. Today a diagonal returns "walk down" for directions 6–8, and an uninitialised stack byte for direction 5 (INFERRED from the macro) | Bypassed for the player in free mode |
| Player step logic | `FieldGetPlayerInput` `field_control_avatar.c:142-149` reduces the D-pad to one direction (UP > DOWN > LEFT > RIGHT). `PlayerNotOnBikeMoving` `field_player_avatar.c:846-937`. `CheckForPlayerAvatarCollision` `:939-951` uses `MoveCoords`, and `sDirectionToVectors` already holds 8 directions (`event_object_movement.c:989-1003`) | One tile per step, with a tile-transition state machine (`T_TILE_CENTER`, `global.fieldmap.h:402-408`) | Input and table changes; `MoveCoords` already handles diagonals | Replace with a per-frame controller in free mode |
| Collision | `GetCollisionAtCoords` `event_object_movement.c:6418-6470`; `GetVanillaCollision` `:6372-6386`; `MapGridGetCollisionAt` `fieldmap.c:400`; `MapGridGetElevationAt` `fieldmap.c:390`; `IsElevationMismatchAt` `:9914`; object vs object `GetObjectObjectCollidesWith` `:6522`, `DoesObjectCollideWithObjectAt` `:6560` | Checks only the destination tile, using a cardinal direction | **Hazard:** `IsMetatileDirectionallyImpassable` `:6513-6520` indexes 4-entry function-pointer arrays (`:975-987`) with `direction - 1`. A diagonal calls a pointer past the end of the array: the code is VERIFIED, and the likely crash is INFERRED. Diagonals must be split into cardinal checks | New hitbox collision built on the same per-tile queries |
| Ledges | `GetLedgeJumpDirection` `:9871-9895` maps diagonals by subtracting `DIR_EAST`, so SW→S, **SE→N**, NW→W, NE→E | Cardinal jumps only | Diagonal steps onto ledges must be blocked explicitly, or SE could trigger a "jump north" (INFERRED) | Snap to the grid, then jump |
| Ice, currents, forced movement | `field_player_avatar.c:481-708` (`ForcedMovement_*`, slide) | Cardinal only | Turn diagonal input into a cardinal direction on forced tiles | Snap to the grid and hand over to the existing code |
| Sideways stairs | `GetSidewaysStairsCollision` `:6327`; checks `:6431-6469`; `directionOverwrite`; `COLLISION_SIDEWAYS_STAIRS_*` `global.fieldmap.h:390-391` | Already moves diagonally, driven by cardinal input | Refuse diagonal input on stair tiles | Snap to the grid |
| Tall grass and per-step encounters | `checkStandardWildEncounter` is set at `T_TILE_CENTER` (`field_control_avatar.c:134-140`); `CheckStandardWildEncounter` `:913`; `StandardWildEncounter` `wild_encounter.c:665`; `AllowWildCheckOnNewMetatile` `:646` | One check per tile entered | Works as is. A diagonal is one check for 1.41 tiles of distance, so slightly fewer encounters | Run it from the "anchor tile changed" bridge, or from a distance counter |
| Ground effects and step callbacks | `GetGroundEffectFlags_*` `event_object_movement.c:9638-9789`; `sPerStepCallbacks` `field_tasks.c:60-70` (ash, cracked floor, ice) | Run per tile | Works | Run from the bridge |
| Camera | `CameraUpdate` `field_camera.c:423-490` handles X and Y separately; the camera object follows the player sprite's **pixel** position (`CameraObject_UpdateMove` `event_object_movement.c:3522-3531`); slice redraw `field_camera.c:123-136`; tile crossing uses `%16` offsets (`:471-474`) | Assumes a constant speed through each 16 px | Diagonals work as is. A vanilla bug at `:463-468` sets `deltaX` in the Y branch; it only matters on mid-step reversal (INFERRED) | Rewrite tile-crossing detection to use absolute pixels. Mixed speeds can skip offset 0 and desync (INFERRED from the `%16` logic) |
| Map connections | `CameraMove` `fieldmap.c:745-780`; `GetMapBorderIdAt` `:661-698`; `SetPositionFromConnection` `:717-743` handles one axis per crossing | One seam crossing at a time | Split diagonals that cross a seam | Reused unchanged once crossing detection is fixed |
| Coordinate triggers and warps | `ProcessPlayerFieldInput` `field_control_avatar.c:161-259`; `GetCoordEventScriptAtPosition` `:1178`; `GetWarpEventAtPosition` `:1131`; `TryDoorWarp` `:1104` and `TryArrowWarp` `:942` need `dpadDirection == playerDirection`; event structs use tile x,y (`global.fieldmap.h:165-198`) | Tile-exact | Work unchanged. Each step changes y by at most 1, so a full-width horizontal trigger line cannot be skipped (and the same for columns); only a staircase-shaped trigger line could be skipped diagonally | Run from the bridge; doors are entered by pushing up |
| Signs, NPCs, BG events via the facing tile | `GetInFrontOfPlayerPosition` `:267-277`; `GetXYCoordsOneStepInFrontOfPlayer` `field_player_avatar.c:1465`; counter-talk uses `gDirectionToVectors` `field_control_avatar.c:337,398`; walk-into-sign `:1287-1291` | One tile ahead in the facing direction | Already handled: **`SetObjectEventDirection` `event_object_movement.c:3630-3652` forces the player's facing to W/E during diagonal movement ("Player interactions require cardinal facing")** while `movementDirection` keeps the diagonal | Probe point = position + facing × ~12 px, mapped to a tile |
| Spawning and despawning by view | `UpdateObjectEventsForCameraUpdate` `:3486`, `TrySpawnObjectEvents` `:2878`, `RemoveObjectEventIfOutsideView` `:2946` | Camera tile deltas | Works (both deltas are passed) | Works once camera tile tracking is fixed |
| Followers (Pokémon and NPC) | `FollowablePlayerMovement_Step` `:5790-5878` walks the follower to the player's `previousCoords` using `GetDirectionToFace` `:6245`, which returns cardinals only; `follower_npc.c` has 15 functions touching coordinates | Cardinal steps | Needs an 8-direction variant, or the follower walks an L-shape and falls behind | Breadcrumb trail of pixel positions |
| Trainer sight | `trainer_see.c:630-673` has four cardinal approach functions; `CheckForTrainersWantingBattle` `:436` | Straight lines | Works unchanged | Works on the derived tile; snap before the approach |
| Surf, Dive, bike, running | `CanStopSurfing` `field_player_avatar.c:1002`; `IsPlayerFacingSurfableFishableWater` `:1641`; Dive scripts `field_control_avatar.c:181,224`; `PlayerRun` `field_player_avatar.c:1294` (`gPlayerRunMovementActions` `event_object_movement.c:1065`); `bike.c` (1,368 lines, direction history in nibbles, `global.fieldmap.h:426`) | Cardinal | Diagonal surfing and running need table entries; mounting, dismounting and Dive stay cardinal; disable diagonals on bikes | Free surfing on allowed water; drop bikes |
| `applymovement` in scripts | `ScrCmd_applymovement` `scrcmd.c:1277`; `ScriptMovement_StartObjectMovementScript` `script_movement.c:22`; scripts are byte lists of `MOVEMENT_ACTION_*`; macros in `asm/macros/movement.inc`; diagonal use already exists (`walk_slow_diag_southwest`, `data/maps/SootopolisCity/scripts.inc:249`) | Tile steps | Works | Snap the player to a tile first, then run unchanged |
| Save data | `SaveBlock1.pos` `include/global.h:1097`; `objectEvents[]` `:1131`; `objectEventTemplates[]` `:1132` | Tile coordinates | No change | Snap on save (no format change), or add 2 bytes of pixel offset |
| Overworld wild encounters (OWE) | `MOVEMENT_TYPE_WANDER/CHASE/FLEE/WATCH/APPROACH_PLAYER_OWE` `include/constants/event_object_movement.h:88-93`; flee logic `event_object_movement.c:11902-11949`; `wild_encounter_ow.c` (1,795 lines); `WE_OWE_FLEE_DESPAWN` `include/config/wild_encounter.h:30` | Grid steps | **A ready-made base for Djinn-style "chase" encounters.** Optionally add diagonal flee steps | Chasers can stay on the grid; catch on overlap |

pokefirered reference (VERIFIED):
- It has the diagonal `DIR_*` constants (`pokefirered: include/constants/global.h:114-117`) and vectors (`pokefirered: src/event_object_movement.c:903-913`).
- It has no diagonal movement actions: grep for `DIAGONAL` is empty, and it has 172 `MOVEMENT_ACTION_` references in total.
- Its input and collision are identical: single-direction D-pad (`pokefirered: src/field_control_avatar.c:148-154`) and the same 4-entry `IsMetatileDirectionallyImpassable` (`:4889-4891`).

The expansion is strictly further along.

## 2. Existing diagonal support

In the expansion (VERIFIED):
- **Direction enum** `DIR_SOUTHWEST..DIR_NORTHEAST` at `include/constants/global.h:204-216`. Vectors include diagonals plus 4 two-wide entries used for stairs (`event_object_movement.c:989-1003`).
- **12 diagonal movement actions**: `WALK_NORMAL_DIAGONAL_*` `0x8C-0x8F`, `WALK_SLOW_DIAGONAL_*` `0x90-0x93`, `WALK_FAST_DIAGONAL_*` `0xAE-0xB1` (`include/constants/event_object_movement.h:236-243,271-274`). They are implemented with `InitMovementNormal(..., DIR_NORTHWEST, ...)` (`event_object_movement.c:7193-7207`).
- **Animation tables** map diagonals to side-facing sprites (for example NW → `ANIM_STD_GO_WEST`, `:804`), and `gFaceDirectionMovementActions` maps diagonals to `FACE_LEFT`/`FACE_RIGHT` (`:1005-1015`). Sprites stay 4-directional.
- **The player's facing is forced cardinal on diagonals** (`:3630-3652`).
- **Sideways stairs** (ghoulslash's feature, already merged) move the player diagonally.
- **What's missing:** diagonal input, diagonal run/surf/bike actions, diagonal-safe collision, and 8-direction followers. Nothing in `docs/` mentions diagonal or 8-way player movement (grep VERIFIED).

On the web I found no public pokeemerald, pokefirered or expansion branch that adds 8-way player movement or pixel/free movement.
- [Sideways stairs (PokéCommunity)](https://pokecommunity.com/threads/sideways-stairs.435887/) is already in the expansion, so its quality is effectively production-grade. Its author made diagonal facing left/right, which is the same rule as above.
- "Grindrunning For Easier Diagonal Movement" in the [Simple Modifications Directory](https://www.pokecommunity.com/threads/simple-modifications-directory.416647/) makes the player auto-turn when running into a wall. The page returned 403, so I'm judging it from the search snippet only: a small hack, useful as the "wall-slide" idea, not a diagonal system.
- [Archipelago's Emerald ROM changes](https://git.hollymcfarland.com/monorail/Archipelago/src/commit/e33ea0147bd19bcf4b03bb2cd25ff1d18aaa89f8/worlds/pokemon_emerald/docs/rom%20changes.md) give input priority to the most recently pressed direction, which is worth copying for input feel.
- I found no public documentation of Golden Sun's field movement or collision format.

## 3. Option A: diagonal steps on the tile grid

**Rules:**
- **Input:** UP+LEFT and the other pairs become diagonals in `FieldGetPlayerInput`, with a 2–4 frame grace window at tile centre so a slightly staggered press doesn't produce a one-tile cardinal step, plus last-pressed priority. It works the same from a D-pad, an analog stick mapped to the D-pad, or a touch joystick.
- **Collision for a diagonal step (dx, dy):**
  - Check the horizontal neighbour with the cardinal H direction.
  - Check the vertical neighbour with the cardinal V direction.
  - Check the destination as reached from each neighbour, using cardinal directions only, so diagonals never reach the 4-entry arrays or the ledge mapper.
  - **No corner-cutting:** both neighbours must be passable and free of objects (no squeezing between two NPCs).
  - If the diagonal is blocked, **slide** on whichever single component is free (wall-sliding, the Grindrunning idea).
- **Refuse diagonals** onto or off ledges, sideways stairs, forced-move tiles (ice, currents, spinners), map connection seams, door and arrow warp tiles, and any step where the two neighbours' elevations differ from the current elevation (bridges, stairs). In those cases the player steps the cardinal component.
- **Facing:** already cardinal via `SetObjectEventDirection`. Treat a diagonal whose horizontal component matches the current facing as "same direction", so there's no turn-in-place stutter.
- **Speed:** a diagonal step moves 16 px on both axes in the same frames, which is 1.41× faster. Optionally stretch diagonal steps to about 22 frames with a sub-pixel pattern.
- **Followers** use an 8-direction `GetDirectionToFace` and step diagonally into the player's previous tile.
- **Unchanged:** NPCs, trainers, scripts, triggers, warps, encounters, connections and the camera.
- **Surf:** diagonal on surfable water; mounting, dismounting, Dive and Waterfall by cardinal facing.
- **Ship on the world map:** a Surf-style avatar with 8-direction steps.
- **Bikes:** diagonals disabled, or bikes removed (Golden Sun has none).

| # | Work item | Files / functions | Rough lines |
|---|---|---|---|
| A1 | 8-direction input, grace window, last-pressed priority, config flag | `field_control_avatar.c` `FieldGetPlayerInput` (105-159); `include/config/overworld.h` | 40–60 |
| A2 | Diagonal entries in the walk/run/slow/run-slow/in-place/surf tables; new `PLAYER_RUN_DIAGONAL_*` ×4 (+ `WALK_FASTER` ×4 only if bikes stay); fix the `dirn_to_anim` off-by-one | `include/constants/event_object_movement.h`; `event_object_movement.c:1005-1290, 6826-6845` + action functions; `src/data/object_events/movement_action_func_tables.h`; `asm/macros/movement.inc` | 250–400 (mostly boilerplate) |
| A3 | `GetDiagonalCollision()` decomposition with the refusal rules above; asserts so no diagonal reaches `IsMetatileDirectionallyImpassable` or `GetLedgeJumpDirection` | `event_object_movement.c` `GetCollisionAtCoords` 6418; `field_player_avatar.c` `CheckForPlayerAvatarCollision` 939, `CheckForObjectEventCollision` 964 | 150–250 |
| A4 | Wall slide | `field_player_avatar.c` `PlayerNotOnBikeMoving` 846 | 40–80 |
| A5 | Player state machine: turning, running and auto-run, surfing, DexNav creeping on diagonals | `field_player_avatar.c` 714-937, 1294 | 60–120 |
| A6 | (optional) Diagonal speed normalisation | `event_object_movement.c` `NpcTakeStep` 10632 + new step table | 60–100 |
| A7 | 8-direction followers (Pokémon and NPC) | `event_object_movement.c` 5790, 6245; `follower_npc.c` | 80–150 |
| A8 | Forced movement and ice: convert to cardinal | `field_player_avatar.c` 481-708 | 20–40 |
| A9 | Surf, Dive, Waterfall rules | `field_player_avatar.c` 1002, 1641 | 20–40 |
| A10 | Bikes: refuse diagonals, or drop bikes | `bike.c` | 10–20 |
| A11 | (optional) Diagonal flee/chase for OWE and Djinn | `event_object_movement.c` 11902-11949; `wild_encounter_ow.c` | 80–150 |
| A12 | Test map (corners, ledges, stairs, ice, bridges, seams, doors, trainers, followers) plus mGBA Lua scripted-input checks | `data/maps/...`, test script | map work + ~100 |

**Total:** about 900–1,500 lines across 9–11 files. Functions changed: about 25–40 (INFERRED).

**Calendar:** walking diagonally on a test map in 3–5 days; edge cases and play-testing bring it to **2–3 weeks**. Confidence medium (about 70%).

**What would change the estimate:**
- keeping bikes (+2–3 days);
- requiring speed normalisation (+1–2 days);
- many ice or forced-movement puzzles;
- maps heavy on bridges or elevation changes;
- upstream expansion changes to field code (merge conflicts).

**Risks:**
- an uncaught diagonal reaching the 4-entry function-pointer arrays (crash);
- follower lag;
- staircase-shaped trigger lines being skipped (a map-authoring rule fixes this);
- the 1.41× diagonal speed feeling off.

## 4. Option B: free 8-way movement

**Recommended form: the hybrid, "free player, grid world".** NPCs, OWE and Djinn objects, boulders, triggers, warps, scripts and maps stay on tiles.

**Position:**
- Add a fixed-point player position (s32, 24.8) plus velocity.
- Walk about 1 px/frame, run about 2 px/frame, diagonals scaled by 181/256 (≈0.707) in integer maths.
- The player's `currentCoords` becomes a derived **anchor tile** under the feet, so the 173 coordinate-reading functions keep working.

**Collision:**
- A feet hitbox (about 10×6 px) is tested against the existing per-tile queries: `MapGridGetCollisionAt`, elevation, the directional-block behaviours applied per crossed tile edge with cardinal directions, and object tiles (current and previous coordinates).
- Resolve X and Y separately, which gives natural wall-sliding, plus a corner nudge of 4 px or less.
- No true slopes: elevation stays per tile, with transition tiles as now.

**Tile-change bridge:** when the anchor tile changes, run the existing step pipeline:
- step scripts, coordinate events and warps;
- wild encounters (or a 16 px distance counter, so nobody can farm encounters by jittering across a tile edge);
- per-step callbacks, ground effects, DexNav, OWE despawn.

**Snap-to-grid bridge:** auto-walk 8 px or less to the tile centre before any of these, then resume free mode:
- script locks and `applymovement`;
- trainer approaches;
- ledge jumps, ice and forced tiles, sideways stairs;
- warps, battles, saves;
- Psynergy casts on grid puzzles.

This is how all existing grid content keeps working.

**Other pieces:**
- **Interactions:** probe point = position + 8-direction facing × 12 px, mapped to a tile, falling back to the cardinal direction.
- **Camera:** replace the `%16` crossing detection with absolute-pixel tile tracking; reuse `CameraMove` for connections.
- **Walk animation** driven by distance travelled.
- **Followers:** a breadcrumb trail of pixel positions.
- **Surf:** free movement on allowed water (the "limited Surf" terrain rule is just a collision class).
- **Ship:** free movement on sea tiles.
- **Djinn chases:** chasers stay on the grid (OWE flee); you catch one when your hitbox overlaps its tile.

| # | Work item | Files / functions | Rough lines |
|---|---|---|---|
| B1 | Fixed-point controller, 8-direction input, speeds, sprite placement, derived anchor tile | new `src/field_free_move.c`; `field_player_avatar.c` `PlayerStep` 360, `MovePlayerAvatarUsingKeypadInput` 444 (bypassed in free mode) | 500–800 |
| B2 | Hitbox vs tile collision, elevation, directional blocks, objects, corner nudge | new; calls `fieldmap.c:390,400`, `event_object_movement.c:6513, 6522, 9914` | 300–500 |
| B3 | Tile-change event bridge | `field_control_avatar.c` 105-259 | 150–300 |
| B4 | Snap-to-grid bridge (scripts, trainers, ledges, ice, stairs, warps, battle, save, Psynergy) | new + hooks in `scrcmd.c`, `trainer_see.c`, `field_player_avatar.c` | 250–400 |
| B5 | Camera tile tracking rewrite | `field_camera.c` 360-490 | 80–150 |
| B6 | Interaction probe, doors, arrow warps, water | `field_control_avatar.c` 267, 942, 1104; `field_player_avatar.c` 1465 | 100–200 |
| B7 | Distance-driven walk cycle | `event_object_movement.c` animation helpers | 100–200 |
| B8 | Follower breadcrumb trail | `event_object_movement.c` 5790; `follower_npc.c` | 200–350 |
| B9 | Surf, Dive, Waterfall and ship in free mode | `field_player_avatar.c`, `field_effect.c` | 150–300 |
| B10 | Elevation, bridges and sprite priority in free mode | `event_object_movement.c` `UpdateObjectEventElevationAndPriority` 9944 | 100–200 |
| B11 | Debug overlay (hitbox, anchor tile), test maps, tuning | new | 150–250 |

**Total:** about 2,100–3,700 lines across 12–15 files. About 60–90 player-path functions are bypassed or adapted (INFERRED).

**Calendar:** **6–10 weeks**, or about 1 week less if A is done first. Confidence low-to-medium (about 40–50%).

**Biggest risks:**
- tuning the feel;
- edge cases on bridges and elevation;
- snap transitions that look jerky;
- unknown code among the ~170 coordinate readers that assumes the player is tile-aligned;
- regression-testing every future cutscene.

**Full B** (sub-tile NPCs, pathing and movement scripts): 4–6+ months, 10k+ lines. Not recommended.

**What Golden Sun itself offers:** `notes\golden_sun.md` says nothing about field movement. It only locates the map loader `FUN_0800fb38` and the map container offsets (+0x24..+0x38, "found, not yet extracted"), with no collision or height layer identified. With no decomp, reversing GS's movement code would not give reusable code. A cheap measurement would still help tune B or A6, about 1–2 days: use `gbax trace` to find the player's X/Y in RAM, then record walk and run speed, diagonal speed, acceleration and corner-nudge behaviour. I believe GS uses pixel positions and has diagonal-facing field sprites, but that is from memory and UNVERIFIED.

## 5. How movement interacts with the rest of the design

- **Aiming field Psynergy:** Golden Sun-style puzzles (Move pillars, Frost puddles, Growth sprouts) sit on tiles. Aim at the **cardinal** facing tile in both options; A already keeps the facing cardinal. Area Psynergy (Reveal) doesn't need aiming. 8-direction aiming isn't needed for function. In B, cast after a snap to the grid.
- **Djinn-style chases:** the expansion's OWE flee, chase and approach movement types are a strong base for the chase encounter type. "Corner it" works naturally on a grid with dead ends. In A, add diagonal flee steps (A11) so cornering is fair against a diagonal-moving player. B doesn't change the chasers.
- **Analog stick and touch joystick on the phone:** GBA input is digital; emulators map an analog stick or touch stick to D-pad bits, diagonals included (INFERRED, standard behaviour). A works directly. B gets 8 directions at a fixed speed, which is what GS on the GBA had anyway. Analog magnitude is only possible in a native port. The grace window (A1) matters most for touch overlays, where diagonal presses are imprecise. Backbone and Xbox D-pads and sticks both arrive as D-pad bits.
- **Ship on the world map:** A gives the ship 8-direction tile steps, which is adequate at world-map scale. B gives smoother sailing. Either way, reuse the Surf avatar state (`PLAYER_AVATAR_STATE_SURFING`, `global.fieldmap.h:340`).
- **Future native port:** A keeps every rule tile-based, so a port can mirror the C code 1:1 and then add free or analog movement natively, where floats, no VRAM limits and real analog input make B much cheaper. B's fixed-point controller would also port cleanly. Neither option blocks the port; A plus native free movement is the cheapest overall path (INFERRED).
- **Save data and auto-run:** A needs no save change. B snaps to the grid on save. Auto-run goes through `PlayerRun`, so A needs the diagonal run actions (A2).

## 6. Side by side

| | **A: grid diagonal** | **B: free 8-way, hybrid (player only)** |
|---|---|---|
| Already in the expansion | Enum, vectors, 12 diagonal actions, diagonal animation entries, cardinal facing rule, diagonal stairs, OWE chasers | The camera already follows sprite pixels; everything else is new |
| Main work | Input, tables, diagonal collision decomposition, followers | New controller, hitbox collision, tile-event bridge, snap bridge, camera, animation, followers, surf |
| Files touched | 9–11 | 12–15 (most new code in one new file) |
| Functions changed | ~25–40 | ~60–90 bypassed or adapted, plus new modules |
| Rough lines | 900–1,500 | 2,100–3,700 |
| Calendar (AI-assisted solo, user play-tests) | **2–3 weeks** | **6–10 weeks** (≈5–9 after A) |
| Confidence | Medium (≈70%) | Low-to-medium (≈40–50%) |
| Main risks | Out-of-bounds pointer if a diagonal leaks into collision; follower lag; 1.41× diagonal speed | Feel tuning, bridges and elevation, snap jank, hidden tile-alignment assumptions, cutscene regressions |
| Golden Sun fidelity | Diagonal walking on a grid; GS-like with a D-pad, but steppy | Close to GS |
| Native-port path | Ports 1:1; add free movement natively | Ports cleanly; base for analog |

## 7. Recommendation

1. **Build A in phase 1.**
   - Fix the three latent bugs first: the `dirn_to_anim` bounds check, the 4-entry directional-block arrays indexed with `direction - 1`, and the `GetLedgeJumpDirection` diagonal mapping.
   - Then do A1–A5 and A7–A9. A6 and A11 are optional.
   - Author all maps and scripts on the grid; that is compatible with both options.
2. **Play-test A on the Fold 7** with touch, Backbone and Xbox input. If it feels "Golden Sun enough", stop there.
3. **If not, add B later as an optional player free mode** layered on A. The input layer, facing rule, 8-direction followers, OWE diagonals, test maps and snap rules carry over. Spend 1–2 days on the GS speed measurement first. Don't attempt full B on the GBA; free movement for every object belongs in the native port.

Sources:
- [Sideways stairs (PokéCommunity)](https://pokecommunity.com/threads/sideways-stairs.435887/)
- [Simple Modifications Directory (PokéCommunity)](https://www.pokecommunity.com/threads/simple-modifications-directory.416647/) (403 to the fetcher; summarised from the search snippet)
- [Archipelago Emerald ROM changes](https://git.hollymcfarland.com/monorail/Archipelago/src/commit/e33ea0147bd19bcf4b03bb2cd25ff1d18aaa89f8/worlds/pokemon_emerald/docs/rom%20changes.md)