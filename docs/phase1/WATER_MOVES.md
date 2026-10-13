# Phase 1: Dive, Waterfall, limited Surf and the Set-Pokémon field-move rule, sized per code base

## Bottom line

- **pokeemerald-expansion (`make firered`):** The Dive engine is already in the FRLG ROM and needs no code changes. All Dive symbols are linked in `expansion (WSL build tree)/pokefirered.map`: `TrySetDiveWarp`, `FldEff_UseDive`, `SetDiveWarpDive`, `EventScript_UseDive`, `EventScript_UseDiveUnderwater`, `Bubbles_Main`, `mus_underwater`, `gBattleEnvironmentTiles_Underwater` and `StartUnderwaterSurfBlobBobbing` (VERIFIED). What is missing is content:
  - No FRLG tileset has a dive-spot or underwater behaviour (VERIFIED by scanning every `*_frlg/metatile_attributes.bin`).
  - The Emerald underwater tileset is compiled out of FRLG builds (`src/data/tilesets/headers.h:31,506,836,1543`; `gTileset_Underwater` is not in the FRLG `.map`, VERIFIED).
  - No FRLG map has a dive/emerge connection or `MAP_TYPE_UNDERWATER` (VERIFIED: 0 matches in `data/maps/*_Frlg`; 7 Emerald maps have them).
- **Waterfall** works in the FRLG build as it is. FRLG tilesets already contain `MB_WATERFALL` metatiles (general_frlg has 3, seafoam_islands_frlg 2, mt_ember_frlg 2; VERIFIED by the scan).
- **There is no HM-free switch in the expansion.** Every "has a Pokémon for this field move" check uses `MonKnowsMove` on `gParties[B_TRAINER_PLAYER]` (VERIFIED, cited below). The only HM-related configs are `P_CAN_FORGET_HIDDEN_MOVE` (`include/config/pokemon.h:57`) and `B_CATCH_SWAP_CHECK_HMS` (`include/config/battle.h:384`). The Set-Pokémon rule is new code, but it is small because the expansion centralises field moves in `gFieldMoveInfo` and `gFieldMoveUnlocks`.
- **Limited Surf and the ship** are new code in every code base. The expansion has free metatile-behaviour slots and one clear place to block movement.
- **pokefirered:** Dive is half-dead there. The warp, connection and field-effect plumbing works, but there are no input hooks, no party-menu entry, an empty underwater transition, scripts marked unused, and a wrong `IsDiveable` range.
- **CFRU:** Dive is fully implemented. Unbound's ROM carries CFRU's Dive hooks and its "HM in bag + a party Pokémon that can learn it" rule.

---

## 1. Dive in pokeemerald-expansion, end to end (all VERIFIED unless marked)

| Piece | Where |
|---|---|
| Dive-spot behaviours | `MB_INTERIOR_DEEP_WATER`, `MB_DEEP_WATER` (`include/constants/metatile_behaviors.h:22-23`). `MetatileBehavior_IsDiveable` returns TRUE for those two plus `MB_SOOTOPOLIS_DEEP_WATER` (`src/metatile_behavior.c:829-837`). |
| No-surfacing behaviours | `MB_NO_SURFACING`, `MB_SEAWEED_NO_SURFACING` (`metatile_behaviors.h:30,47`). `MetatileBehavior_IsUnableToEmerge` (`metatile_behavior.c:839-850`). The code's own comment says emerging is allowed by default on every other underwater tile, including water doors unless `BUGFIX` is defined. |
| Tile flags | All of these are `TILE_FLAG_SURFABLE`; seaweed and deep water also have encounters (`metatile_behavior.c:26-46`). |
| Connection types | `CONNECTION_DIVE` and `CONNECTION_EMERGE` (`include/constants/global.h:226-227`). They are skipped for seamless edge scrolling (`src/fieldmap.c:880`). |
| Dive warp resolution | `SetDiveWarp` (`src/overworld.c:845-861`): it finds the dive/emerge connection and warps to the **same x,y** on the target map. The connection offset is ignored, so the surface and underwater maps must line up 1:1. With no connection it falls back to `RunOnDiveWarpMapScript` and the fixed dive warp (map script `ON_DIVE_WARP`, `include/constants/map_scripts.h:31,44`; `src/script.c:452`). |
| Map type and state | `MAP_TYPE_UNDERWATER` (`include/constants/map_types.h:11`) makes the player start in the underwater state (`overworld.c:1028`). After emerging onto surfable water the player is surfing (`overworld.c:1032`). Music is forced to `MUS_UNDERWATER` (`overworld.c:1304`). The map counts as outdoors (`overworld.c:1557`). Battle environment and transition are handled (`src/battle_setup.c:792,840`), and so is the Dive Ball (`battle_script_commands.c:7891`). |
| Weather | `WEATHER_UNDERWATER_BUBBLES` (`include/constants/weather.h:20`; `src/field_weather.c:144`). Not FRLG-gated. |
| Input | **B** while underwater runs `TrySetupDiveEmergeScript` (`src/field_control_avatar.c:181`). **A** while surfing runs `TrySetupDiveDownScript` (`:224`). Both require `IsFieldMoveUnlocked(FIELD_MOVE_DIVE)` and `TrySetDiveWarp()` returning 2 (dive) or 1 (emerge) (`:661-685`, `:1246-1265`). |
| Scripts | `EventScript_UseDive` and `EventScript_UseDiveUnderwater` (`data/scripts/field_move_scripts.inc:319-370`). They use `checkfieldmove FIELD_MOVE_DIVE`, then `bufferpartymonnick`, then `dofieldeffect FLDEFF_USE_DIVE`. They are included unconditionally (`data/event_scripts.s:1701`). |
| Field effect | `FldEff_UseDive` runs Init, then ShowMon, then TryWarp, which calls `TryDoDiveWarp` and then `DoDiveWarp` (`src/field_effect.c:2131-2175`; `field_control_avatar.c:1221-1244`; `src/field_screen_effect.c:541-550`). |
| Underwater avatar | `PlayerAvatarTransition_Underwater` sets the underwater graphics and bobbing (`src/field_player_avatar.c:1169-1175`). In the FRLG build the underwater graphics are aliased to `OBJ_EVENT_GFX_RED_SURF` (`include/constants/event_objects.h:11,20`), although `gObjectEventGraphicsInfo_BrendanUnderwater` is linked in the FRLG ROM. |
| Party menu | `FIELD_MOVE_DIVE` uses `SetUpFieldMove_Dive` and `TrySetDiveWarp` (`src/field_move.c:104-110`; `src/party_menu.c:4361-4380`). |
| Unlock | `BADGE_UNLOCK`, badge 7, in both games (`field_move.c:104-110`). In the FRLG build `FLAG_RECEIVED_HM_DIVE` is 0 (`include/constants/flags_frlg.h:1552`). |

**Porymap (VERIFIED, https://huderlem.github.io/porymap/manual/editing-map-connections.html):** the Connections tab has "Dive Map" and "Emerge Map" dropdowns, with no offset or direction. A "Show Emerge/Dive Maps" checkbox overlays the linked maps, with opacity sliders. The manual names no game-version restriction, so I infer it also works with the FRLG Porymap settings in `docs/tutorials/how_to_frlg.md:10-21` (INFERRED). On disk this becomes a `connections[]` entry with `"direction": "dive"` or `"emerge"` (example: `data/maps/Underwater_Route124/map.json`, plus Route124's `dive` entry).

**Does it work unchanged in `make firered`?** Yes for code, no for content.

Things to know:
- Every `MB_DEEP_WATER` tile on a map that has a dive connection is a dive spot.
- A map can have only one dive target (`GetMapConnection` returns the first match, `overworld.c:829-843`). More than one underwater area under a surface map needs one big underwater map, or `ON_DIVE_WARP` plus `setdivewarp` per coordinate.
- On an FRLG map with no dive connection, a deep-water tile does nothing harmlessly (`SetDiveWarp` returns FALSE).

**What to author for 1 dive spot + 1 underwater map in the FRLG build:**
1. **Dive-spot metatile.** Duplicate an FRLG ocean metatile in an FRLG secondary tileset, darken it, and set its behaviour to `MB_DEEP_WATER` with elevation 1 like the surrounding water. FRLG attributes are 32-bit, with behaviour in bits 0-8 and layer in bits 29-30 (`src/fieldmap.c:84-103`; `include/global.fieldmap.h:43-46`).
2. **FRLG-format underwater secondary tileset.** Either port Emerald's `gTileset_Underwater` or build a placeholder from FRLG art. Porting means re-indexing tiles and palettes: the FRLG primary has 640 tiles and 7 palettes (`include/fieldmap.h:4-6`) versus Emerald's 512 and 6, and the attributes must be rewritten to the 32-bit FRLG layout. Then add the header, graphics and metatiles entries in the `#else` (FRLG) half of `src/data/tilesets/{headers,graphics,metatiles}.h`. Behaviours to paint:
   - `MB_SEAWEED` for encounters.
   - `MB_NO_SURFACING` on every tile not under a dive spot.
   - Or adopt CFRU's stricter rule (see §4) and skip this painting.
3. **Layout entry** in `data/layouts/layouts.json` with `"layout_version": "frlg"`, `border_width` and `border_height`, and the same width and height as the surface map (`tools/mapjson/mapjson.cpp:785-830`).
4. **Underwater map** `map.json`:
   - `"region": "REGION_KANTO"`. Without it the map is dropped from the FRLG build (`mapjson.cpp:742-756`; `how_to_frlg.md:26`).
   - `MAP_TYPE_UNDERWATER`, `WEATHER_UNDERWATER_BUBBLES`, `MUS_UNDERWATER`.
   - An `emerge` connection back to the surface map.
   - An entry in an FRLG or new group in `map_groups.json`. Cross-game groups can't connect (`how_to_frlg.md:67`).
5. **Surface map:** add a `dive` connection to the underwater map.
6. Add a MAPSEC and `wild_encounters.json` water entries for seaweed.
7. **Optional, 2 lines:** point `PLAYER_AVATAR_GFX_*_UNDERWATER` at the Brendan/May underwater graphics instead of the Surf sprite (`event_objects.h:11,20`).

**Effort:** 0 required code lines (about 15 if you take the emerge-rule change). **1-2 days** calendar for a placeholder. The tileset port is the variable part. Medium confidence. It drops to under a day if you accept a crude placeholder tileset made only from FRLG art.

---

## 2. Waterfall and Surf checks, and the "any Set Pokémon can learn it" hook

**Where the checks live in the expansion (VERIFIED):**
- **Unlock layer:**
  - `IsFieldMoveUnlocked` (`include/field_move.h:40-43`) looks up `gFieldMoveUnlocks[]`, whose types are `CANT_UNLOCK`, `ALWAYS_UNLOCKED` and `BADGE_UNLOCK` (`src/field_move.c:12-44`).
  - Surf, Waterfall and Dive table entries are at `field_move.c:86-119`.
  - `.arg` is only 8 bits (`field_move.h:27`).
- **"Has a Pokémon" layer** (all use `MonKnowsMove` on the 6-slot party):
  - `PartyHasMonWithSurf` (`src/field_player_avatar.c:1616-1630`).
  - `ScrCmd_checkfieldmove` (`src/scrcmd.c:2294-2320`) sets VAR_RESULT to the party index, or to `PARTY_SIZE` if none.
  - The party-menu list shows a field move only if the Pokémon knows it (`party_menu.c:2950-2965`).
- **Context checks:**
  - `GetInteractedWaterScript`, the A-press on water for Surf and Waterfall (`field_control_avatar.c:640-659`).
  - `IsPlayerFacingSurfableFishableWater` (`field_player_avatar.c:1641-1653`) and `IsPlayerSurfingNorth`.
  - Party-menu setup: `SetUpFieldMove_Surf` (`party_menu.c:4285-4296`), `SetUpFieldMove_Waterfall` (`:4329-4344`), `SetUpFieldMove_Dive` (`:4367-4380`).
  - Scripts: `EventScript_UseWaterfall` (`field_move_scripts.inc:284-305`) and `EventScript_UseSurf` (`data/scripts/surf.inc:1-13`).
- **Show-Pokémon animation:** `FldEff_FieldMoveShowMonInit` reads `gParties[B_TRAINER_PLAYER][(u8)gFieldEffectArguments[0]]` (`src/field_effect.c:2937-2948`).
- **"Can learn" data:**
  - `CanLearnTeachableMove(species, move)` (`src/pokemon.c:5024-5035`).
  - HMs include SURF, WATERFALL and DIVE (`include/constants/tms_hms.h:56-64`).
  - Teachable learnsets are generated from the available TMs, HMs and tutors (`include/config/pokemon.h:66`).
  - Level-up learnsets: `GetSpeciesLevelUpLearnset` (`include/pokemon.h:864`).
- **Small existing bug:** `EventScript_CurrentTooFast` compares the `checkfieldmove` result to `FALSE` instead of `PARTY_SIZE` (`surf.inc:18-19`), so the check is inverted.

**Hook design (expansion):**
1. **New unlock type `FLAG_UNLOCK`** in `gFieldMoveUnlocks`. Add a `u16 unlockFlag` field, because `arg:8` cannot hold a flag ID. Set Surf, Dive and Waterfall to story or key-item flags. This also answers the open "how are they unlocked" question without code churn. About 20 lines in `field_move.h` and `field_move.c`.
2. **New `bool32 SetMonsCanUseFieldMove(enum FieldMove fm, u8 *outSetIdx)`**, for example in `field_move.c`:
   - Return FALSE if the move is locked.
   - Get the move with `FieldMove_GetMoveId(fm)`.
   - For each of the 24 Set slots (an accessor from the Set-storage work, as `BoxPokemon`), skip empty slots and eggs.
   - Return TRUE if any of `BoxMonKnowsMove`, `CanLearnTeachableMove` or a level-up-learnset hit is true.
   - About 40 lines.
3. **Repoint the callers** (about 100-150 lines in total):
   - `PartyHasMonWithSurf`.
   - `ScrCmd_checkfieldmove`: for water moves, search the Set slots; return the slot in VAR_RESULT with a new sentinel such as `SET_MON_NONE`, put the species in VAR_0x8004, and buffer the nickname into `gStringVar1` directly.
   - `FldEff_FieldMoveShowMonInit` (and `DiveFieldEffect_ShowMon`, `field_effect.c:2153-2159`): decode a "Set-slot" bit in `gFieldEffectArguments[0]` and read species, shiny and personality from Set storage.
   - Scripts `field_move_scripts.inc:286-287, 321-322, 348-349` and `surf.inc:2-3, 18-19`: replace `bufferpartymonnick` and the `PARTY_SIZE` compares. About 30 lines.
4. **Party menu:** the water moves no longer need to be in move slots, so the per-Pokémon listing in `SetPartyMonFieldSelectionActions` becomes moot. Use is by facing water and pressing A (existing code paths), or a "Surf" entry in the new Psynergy/field menu that calls `SetUpFieldMove(FIELD_MOVE_SURF)` (`field_move.h:35-38`).
5. **Data work:** Weyard forms need SURF, DIVE and WATERFALL in their teachable learnsets. My inference is that this goes through the learnset-helper JSON inputs, but I did not read `make_teachables.py` (INFERRED).

**Dependency:** this needs the Set-Pokémon storage structure (DESIGN.md:170).

**Effort:** about 180-260 lines. **2-4 days** once storage exists. Medium confidence.

---

## 3. Limited Surf: terrain rule and the ship take-over (design; code anchors VERIFIED)

**Behaviours.** Rename existing `MB_UNUSED_*` slots instead of appending, so the numbers already stored in tileset `.bin` files don't shift. There are 27 unused entries, for example `MB_UNUSED_D7..DF` (`metatile_behaviors.h:220-228`), and `MB_INVALID` is 255 (`:248`). Proposed:
- `MB_RIVER_WATER`: surfable, has encounters, fishable.
- `MB_COASTAL_SHALLOWS`: surfable. Note the existing `MB_SHALLOW_WATER` is walkable, not surfable (`metatile_behavior.c:32`).
- `MB_DEEP_SEA`: has the surfable flag so encounters, battle backgrounds and elevation all work, but it is **ship-only**.
- Optional `MB_SHIP_DOCK`.
- Keep `MB_POND_WATER` for lakes and `MB_OCEAN_WATER` for coastal water, since FRLG placeholder maps use OCEAN everywhere (general_frlg has 72 OCEAN metatiles). Deep sea is painted with duplicated ocean metatiles tagged `MB_DEEP_SEA`.
- Dive spots (`MB_DEEP_WATER`) sit only inside surfable regions.

**Code changes** (about 80-150 lines):
- Flags and predicates in `metatile_behavior.c`: the `sTileBitAttributes` entries (`:18-50`), a new `MetatileBehavior_IsDeepSea`, and the new types added to `IsSurfableFishableWater` (`:1121-1136`).
- **Movement block:** in `CheckForObjectEventCollision` (`field_player_avatar.c:964-986`), if the player is surfing, not sailing, and the target tile is deep sea, return `COLLISION_IMPASSABLE` and show a one-shot "too rough, you need the ship" message.
- **Surf start:** split `IsPlayerFacingSurfableFishableWater` (`:1641`) into a surf version that refuses deep sea and a fishing version. Callers are `field_control_avatar.c:644`, `party_menu.c:4290` and `item_use.c:329`.
- **"Short distances":** enforce this through map design. A step budget would be about 40 more lines and is a design call.

**Ship take-over.** All 8 `PLAYER_AVATAR_FLAG_*` bits are already used (`include/global.fieldmap.h:348-355`). Options:
- A separate sailing flag that runs on top of the surfing state: surfing movement, ship sprite, no surf blob, deep sea allowed.
- Or repurpose `PLAYER_AVATAR_FLAG_ACRO_BIKE` if bikes are cut, since Golden Sun has none (INFERRED as a design option).

The ship's pieces:
- Board by interacting with a ship object at a dock.
- Disembark through a ship variant of `CanStopSurfing` (`field_player_avatar.c:1002-1017`), allowed only at dock or beach tiles.
- Store the ship's map, x and y in variables so the ship object stays where it was left.
- Optional open-sea Dive from the ship: allow `TrySetupDiveDownScript` while sailing and restore the ship on emerge. About 50-80 lines.

The existing `FLAG_SYS_CRUISE_MODE` only forces walking (`overworld.c:1026`), so it is not a ship.

**Effort:**
- Terrain rule: about 80-150 lines plus tile duplication, **1.5-3 days** (medium confidence).
- Minimal ship mode: about 400-700 lines, **4-8 days** (medium-low confidence).
- World-map and sailing integration belongs to the world-map topic.

---

## 4. Comparison code bases

**pret pokefirered (VERIFIED):**
- **Functional plumbing:**
  - `SetDiveWarp`, `SetDiveWarpEmerge` and `SetDiveWarpDive`, plus `SetFixedDiveWarp` (`src/overworld.c:661-747`).
  - Initial-state handling for underwater (`:858-930`).
  - Fieldmap skipping dive/emerge connections (`src/fieldmap.c:778`).
  - `dive_warp` (`src/field_control_avatar.c:1118`).
  - `FldEff_UseDive` (`src/field_effect.c:1683-1723`) and `DoDiveWarp` (`src/field_fadetransition.c:546`).
  - Map macros accept `dive` and `emerge` (`asm/macros/map.inc:143-144`).
  - Bubbles weather code (`src/field_weather.c:83`, marked unused in `weather.h:18`).
  - `StartUnderwaterSurfBlobBobbing` (`src/field_effect_helpers.c:1083`).
- **Dead or broken:**
  - `TrySetDiveWarp` is `static` and never called (`field_control_avatar.c:1143`). There is no A or B input hook.
  - `PlayerAvatarTransition_Underwater` is empty (`src/field_player_avatar.c:736-739`).
  - There is no `FIELD_MOVE_DIVE`; the party-menu list stops at 12 entries (`include/constants/party_menu.h:34-46`).
  - The Dive scripts are commented "Unused leftover from R/S" and use `checkpartymove` (`data/scripts/field_moves.inc:209-250`).
  - `MetatileBehavior_IsDiveable` uses the range `MB_FAST_WATER..MB_DEEP_WATER` (0x11-0x12), which includes fast water (`src/metatile_behavior.c:478-483`).
  - There is no underwater tileset and no underwater player sprite.
- **Porting Emerald's Dive:**
  - Input hooks: about 40 lines.
  - `IsDiveable` fix: 2 lines.
  - Underwater transition plus a placeholder sprite: about 15 lines.
  - Party-menu Dive entry, cursor callback and description: about 40 lines.
  - Script rewrite: about 40 lines.
  - Tileset: same work as in §1.
  - Total **3-5 days**.
- Waterfall exists (`FIELD_MOVE_WATERFALL`). The HM-free hook and limited Surf would cost about the same as in the expansion, but without the `gFieldMoveInfo` and unlock tables, so the changes are more scattered (INFERRED: +1-2 days).

**CFRU / Unbound (VERIFIED):**
- **Dive is implemented:**
  - `TrySetupDiveDownScript` and `TrySetupDiveEmergeScript` (`src/overworld.c:2675-2745`).
  - Hooks `DiveCheckEmergeHook` and `DiveCheckDownHook` (`hooks:372-373`; `assembly/hooks/general_hooks.s:1010-1016`).
  - `MB_DIVEABLE = 0x12` (`include/constants/metatile_behaviors.h:15`).
  - A stricter surfacing rule: you can only emerge on a `MB_DIVEABLE` tile (`overworld.c:2752-2757`). This rule is worth copying into the expansion.
  - A real underwater transition (`overworld.c:2764-2781`).
  - Scripts in `assembly/overworld_scripts/system_scripts.s:705-733`.
- **Unbound's ROM contains these hooks.** `symbol_diff.csv` shows:
  - `ProcessPlayerFieldInput` hooked with both Dive hooks.
  - `MetatileBehavior_IsDiveable` hooked.
  - `GetInteractedWaterScript` hooked, 84% changed.
  - `GetAdjustedInitialTransitionFlags` hooked.
  - `SetPartyMonFieldSelectionActions` hooked.
- **HM-free rule:** `ONLY_CHECK_ITEM_FOR_HM_USAGE` (`src/config.h:259`, commented out by default). `PartyHasMonWithFieldMovePotential(move, item, surfingType)` (`src/overworld.c:2381-2416`) accepts a party Pokémon if it knows the move, or if the HM is in the bag and `CanMonLearnTMTutor` succeeds. The party menu adds HM entries for Pokémon that can learn them (`src/party_menu.c:967-1070`). The `#ifdef UNBOUND` branches add `FLAG_BOUGHT_ADM`, which skips the Pokémon requirement (`overworld.c:2679`; `party_menu.c:1022-1030`).
- **Adapting CFRU:** point that loop at Set storage. About 1-2 days of code, but it is hook-based binary patching.
- **Map authoring in CFRU** (INFERRED): it has no map sources, so maps are edited in binary editors (AdvanceMap or HexManiac), not Porymap. That makes the native-Android port path weaker.

---

## 5. Effort and risks per code base

| Code base | Dive + 1 underwater map | Waterfall | Set-Pokémon rule | Limited Surf (+ minimal ship) | Total for this topic |
|---|---|---|---|---|---|
| Expansion (FRLG build) | 0-15 lines code, 1-2 d content | 0 | 180-260 lines, 2-4 d | 80-150 lines, 1.5-3 d (+ ship 4-8 d) | **≈ 9-17 working days (2-3.5 weeks)**, medium confidence |
| pokefirered | about 140 lines + content, 3-5 d | 0 | 3-5 d | 2-4 d (+ ship 5-9 d) | ≈ 13-23 d |
| CFRU | exists, content only (binary tools) | 0 | 1-2 d | 2-4 d (+ ship 5-9 d, hook-based) | ≈ 9-16 d, but a weaker port path |

**Risks:**
1. **Tilesets.** Porting the underwater tileset into FRLG format (tile and palette re-indexing, 32-bit attributes) is the main unknown.
2. **Emerald's surfacing default.** It allows emerging anywhere, so you either paint everything `NO_SURFACING` or change the rule.
3. **Dive limits.** Only one dive target per map; underwater and surface coordinates must line up 1:1.
4. **8-way movement.** Diagonal steps must respect deep-sea blocking and `CanStopSurfing`, so this depends on the movement topic.
5. **Set-storage dependency.** The "can learn" rule needs teachable data for the Weyard forms.
6. **No spare avatar-flag bit** for the ship.

**What would change the estimates:**
- A ready FRLG-format underwater tileset: Dive drops to about half a day.
- Requiring diving from the ship, or a surf step budget: +1-2 days.
- The final ship being part of a Lost Age-style world map rather than local maps: moves the ship work to the world-map estimate.
