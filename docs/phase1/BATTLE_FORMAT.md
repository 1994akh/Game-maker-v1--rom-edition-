# Phase 1: sizing the custom battle format (1 Adept + 1 Pokémon per side)

> **Notes from the review ([REVIEW.md](REVIEW.md)):**
> - "Option 1: up to 6 Adepts per battle" conflicts with DESIGN.md ("8 Adepts … the others swap in"). It is a scope cut only you can approve. Supporting all 8 costs about +200–400 lines and +1 week.
> - The plan covers the party only inside battle. Outside battle, `gParties[B_TRAINER_PLAYER]` appears 802 times in 76 source files (healing, items, catching, followers, evolution, …). That **party / Set-storage layer** is a separate 2–4 week item, and it should be designed before stage 1.

**Primary base:** pokeemerald-expansion 1.17.2 (`make firered`). Compared against CFRU and vanilla pokefirered.
**Legend:** **VERIFIED** means I saw it in the source tree. **INFERRED** means reasoning from the code, not yet checked.
**Paths:** `expansion/` = the pokeemerald-expansion 1.17.2 source tree (commit `8fb02c6f`).

## Summary

- **The expansion already has most of what this format needs. VERIFIED.**
  - It keeps four separate 6-slot battle parties: `gParties[MAX_BATTLE_TRAINERS][PARTY_SIZE]`, one each for player, opponent A, partner and opponent B (`expansion/include/pokemon.h:730`, `expansion/include/constants/battle.h:28-85`).
  - Each battler draws from its own party through `GetBattlerTrainer()` and `GetBattlerParty()` (`expansion/src/battle_controllers.c:3322-3346`, `expansion/src/battle_util2.c:259-274`).
  - "Full-team" multi battles (6 Pokémon per trainer) are the default, because `B_MULTI_HALF_TEAMS` is FALSE (`expansion/include/config/battle.h:398`, `expansion/src/battle_util.c:9957-10006`).
  - In a plain double battle (not a multi), the engine already lets the player control battler 2 (`expansion/src/battle_controllers.c:339-342`).
- **So the core change is small.** Add one battle flag, and make `BattleSideHasTwoTrainers()` return TRUE for it (`expansion/src/battle_controllers.c:3353-3359`). Then:
  - slot A (battler 0) switches only among Adepts in `gParties[B_TRAINER_PLAYER]`;
  - slot B (battler 2) switches only among Set Pokémon in `gParties[B_TRAINER_PARTNER]`;
  - the enemy works the same way with `OPPONENT_A` (Adepts) and `OPPONENT_B` (Pokémon).
- **Biggest structural limits:**
  - **8 Adepts don't fit a 6-slot party.** `PARTY_SIZE` is 6 (`expansion/include/constants/global.h:82`).
  - **Only 4 move slots.** `MAX_MON_MOVES` is 4 (`expansion/include/constants/global.h:136`), so an Adept carries 4 Psynergy at a time unless a custom list UI is built.
  - **Exp and post-battle evolution only cover the player party.** Both are hard-coded to `gParties[B_TRAINER_PLAYER]` (`expansion/src/battle_script_commands.c:2135+`, `expansion/src/battle_main.c:5369-5396`), so Set Pokémon in the partner party need extra work.
- **The expansion's test framework fits this format directly.** `MULTI_BATTLE_TEST` already uses `PLAYER` / `PARTNER` / `OPPONENT_A` / `OPPONENT_B` parties. A new `ADEPT_BATTLE_TEST` type is about 60 lines.
- **Total estimate:** about 2,000–3,500 changed or added lines (plus data), **about 7–11 calendar weeks**, medium-low confidence (±40%). The first playable slice takes about 1 week.

---

## 1. Battlers and parties; a separate switch pool per slot

**How the expansion represents them (all VERIFIED):**
- **Battler IDs and positions:** `enum BattlerId` goes from B_BATTLER_0 to 3, so `MAX_BATTLERS_COUNT` = 4 (`expansion/include/constants/battle.h:69-76`). Positions: 0 = player left, 1 = opponent left, 2 = player right, 3 = opponent right (`:59-67`).
- **Per-battler state:** `gBattleMons[MAX_BATTLERS_COUNT]` and `gBattlerPartyIndexes[MAX_BATTLERS_COUNT]` (`expansion/include/battle.h:1018,1026`).
- **Parties:**
  - `gParties[4][6]` and `gPartiesCount[4]` (`expansion/include/pokemon.h:729-730`).
  - The four parties are `B_TRAINER_PLAYER`, `B_TRAINER_OPPONENT_A`, `B_TRAINER_PARTNER` and `B_TRAINER_OPPONENT_B` (`expansion/include/constants/battle.h:78-85`). They have the values 0, 1, 2, 3, the same numbers as battlers 0–3.
  - The old `gPlayerParty` / `gEnemyParty` names were renamed in 1.16.0 (`expansion/docs/changelogs/1.16.x/1.16.0.md:109-115`).
- **Which party a battler uses:**
  - When a side has two trainers, `GetBattlerTrainer()` returns the battler number itself. Otherwise it returns the side (`battle_controllers.c:3345`).
  - `BattleSideHasTwoTrainers()` returns `BATTLE_TYPE_MULTI` for the player side, and two-opponents/link-multi for the enemy side (`:3353-3359`).
- **Per-party battle state is already sized for 4 parties:**
  - `partyState[MAX_BATTLE_TRAINERS][PARTY_SIZE]` and `activeGimmick[MAX_BATTLE_TRAINERS][PARTY_SIZE]` (`expansion/include/battle.h:477,589`).
  - The AI's party memory has the same shape (`:217`).
- **Switch checks already use the battler's own party:**
  - `CanBattlerSwitch` uses `GetBattlerParty()` plus `BattlersShareParty()` (`expansion/src/battle_script_commands.c:3307-3334`).
  - `HasNoMonsToSwitch` (`expansion/src/battle_util.c:1910+`) and the AI's `GetAILastPartyIndex` (`expansion/src/battle_ai_util.c:6186-6189`, giving 6 slots when teams are full) do the same.
  - The party menu's "Shift" path also uses `GetBattlerParty` (`expansion/src/party_menu.c:7532-7599`).
- **Existing layouts for the partner's party:**
  - `PARTY_LAYOUT_MULTI_FULL` and `PARTY_LAYOUT_MULTI_FULL_PARTNER` exist (`expansion/include/party_menu.h:13-16`), and `GetPartyAndSlotFromPartyMenuId` maps them to `gParties[B_TRAINER_PARTNER]` (`party_menu.c:8400-8440`).
  - Today the partner layout is view-only (`ACTIONS_SUMMARY_ONLY`, `party_menu.c:7518-7529`).
  - Layout choice is in `GetPartyLayoutFromBattleType()` (`party_menu.c:7482-7491`).

**How hard is it to give each player slot its own switch pool? Moderate, and mostly done already.** Plan:
1. Add `BATTLE_TYPE_ADEPT`. Bit 14 (`BATTLE_TYPE_14`) is defined but never used (`constants/battle.h:115`; a grep found no other uses).
2. Start the battle as `BATTLE_TYPE_DOUBLE | BATTLE_TYPE_ADEPT`. Do **not** set `INGAME_PARTNER`, because that hands battler 2 to the AI controller (`battle_controllers.c:330-334`). Without it, battler 2 is already player-controlled (`:339-342`).
3. In `BattleSideHasTwoTrainers` (`battle_controllers.c:3353`) and `AreMultiPartiesFullTeams` (`battle_util.c:9957`), return TRUE for Adept battles. About 6 lines.
4. In the party menu:
   - `GetPartyLayoutFromBattleType` picks by `gBattlerInMenuId`: the normal single layout for battler 0, the partner layout for battler 2.
   - `GetPartyMenuActionsTypeInBattle` allows Send Out / Shift in the partner layout.
   - About 50–100 lines in `party_menu.c`.
5. Audit the shared-party assumptions that sit outside `BattleSideHasTwoTrainers`. **INFERRED** size: about 20 places compare party indexes with the partner battler (10 in `battle_script_commands.c`, 3 in the player controller, 2 each in `battle_util.c` and the AI util). Example: `SelectedMonHasVolatile` assumes battler 2 is party slot 1 (`expansion/src/item_use.c:1185-1191`). There are also about 30 core `BATTLE_TYPE_MULTI` checks in `battle_main.c` (14), `battle_script_commands.c` (11) and `battle_util.c` (5) to review.

**Gaps to design around:**
- **8 Adepts vs 6 slots.**
  - Option 1: up to 6 Adepts per battle (a "front line", like The Lost Age's 4+4). No engine work.
  - Option 2: a custom Adept switch list that reads all 8 from storage and swaps the chosen one into a free or fainted party slot. About 200–400 lines plus risk.
  - Recommendation: Option 1 for now.
- **Changing Adepts should change slot B's pool.** **INFERRED** approach: slot B's party holds the active partner plus the new Adept's 3 Set Pokémon (4 or fewer, so it fits in 6). On an Adept switch-in:
  - write the old Set Pokémon back to storage;
  - reload the other slots;
  - reset `partyState[B_TRAINER_PARTNER][i]`.
  - The current partner stays on the field until it switches or faints. Forcing an immediate partner swap means two switch-ins from one action, which is about 2× the work.
  - **This is a design question.**
- **The partner party is never written back after a battle.** Multi partners are throwaway (`FillPartnerParty` zeroes it, `expansion/src/battle_partner.c:26-49`). Needs:
  - a load at battle start and a write-back at battle end (HP, status, PP, exp, moves);
  - exp for slot B: `Cmd_getexp` uses `gParties[B_TRAINER_PLAYER]` throughout, with 23 `expGetterMonId` references, all in `battle_script_commands.c` (VERIFIED);
  - post-battle evolution: `TryEvolvePokemon` only walks the player party (`battle_main.c:5369-5396`, VERIFIED).

## 2. The Adept as a species (recommended) or a new struct

**Recommendation: make the Adept a species (`struct Pokemon`), with an `isAdept` flag.**
- Everything in the battle engine takes `struct Pokemon` / `struct BattlePokemon`: switching, healthboxes, controllers, the party menu, the summary screen, the AI and the tests.
- A new struct would need new code down every one of those paths.
- `struct SpeciesInfo` has a spare `padding4:8` (`expansion/include/pokemon.h:497`) for `isAdept:1`. VERIFIED.
- Base stats, types, abilities, growth rate and level-up learnset (Psynergy learned by level) all come for free.

What breaks, and how to fence it off:

| Area | What to do | Status |
|---|---|---|
| Pokédex | `natDexNum = NATIONAL_DEX_NONE`; guard `HandleSetPokedexFlag` (`expansion/src/pokemon.c:5654`) | Guard location VERIFIED; behaviour INFERRED |
| Evolution | `.evolutions = NULL`, so no evolutions | INFERRED |
| Catching | Enemy Adepts only appear in trainer battles, where balls are blocked. Add an Adept check in `GetBallThrowableState` as a backstop (`expansion/src/item_use.c:1137`) | INFERRED |
| Trade / PC / daycare | `cannotBeTraded` exists (`pokemon.h:490`); give Adepts the no-eggs egg group; keep Adepts in their own storage, not the PC | VERIFIED field; rest INFERRED |
| Exp / levels | Adepts sit in `gParties[B_TRAINER_PLAYER]`, so `Cmd_getexp` already gives them exp | VERIFIED |
| Summary screen | Works as is; a "Class" page comes later | INFERRED |
| Held items | Decide by design; block the party menu "Give" for Adepts if needed | INFERRED |
| Transform / Sketch / Mimic / Skill Swap / Role Play on an Adept | Decide immunities, because they interact with the shared-PP mirror (see §3) | INFERRED |
| Sprites | `SpeciesInfo` needs a front and back pic plus an icon; copy an existing species' art as a placeholder | VERIFIED fields (`pokemon.h:442-446`) |
| Enemy Adept class | `TrainerMon` has no spare field. Either reuse `teraType:5` (Tera isn't in the design) or add a `Class:` field to `tools\trainerproc\main.c` | VERIFIED struct (`expansion/include/data.h`, struct TrainerMon) |

The 8 player Adepts can each be their own species. Enemy Adepts can use about 6 generic per-element species, with class set by trainer data.

## 3. Psynergy paid from one shared Adept PP pool

**Where PP is checked and spent (all VERIFIED):**
- **Deduction:** `CancelerPPDeduction`, `expansion/src/battle_move_resolution.c:997-1052`. It does `pp[movePosition] -= ppToDeduct`, adds the Pressure extra, then writes back to the party mon.
- **Selection blocks:**
  - `battle_util.c:1586-1597`: "no PP" message.
  - `CheckMoveLimitations` `MOVE_LIMITATION_PP`, `battle_util.c:1634`. This is also used by the AI and by Struggle.
- **Other PP edits:**
  - Spite / Grudge: `battle_script_commands.c:6388-6414`
  - Eerie Spell: `battle_set_effect.c:780-788`
  - Leppa Berry: `battle_hold_effects.c:885`
  - AI switch logic reads `pp == 0`: `battle_ai_switch.c:2689`
  - Z-move check: `battle_z_move.c:180`
  - Move-menu PP display: `battle_controller_player.c:1674-1695`
- About 71 `.pp[` / `currentPP[` references across `src\battle*.c`.

**Cleanest hook (INFERRED design): a "PP mirror".**
- Keep the real pool in a battle-side table, for example `gBattleStruct->adeptPP[MAX_BATTLE_TRAINERS][PARTY_SIZE]` (current and max). That covers enemy Adepts too.
- After any change to the pool, call `SyncAdeptPPMirror(battler)`, which sets `gBattleMons[b].pp[i] = pool / PsyCost(move[i])`, capped at 127.
- Every existing `pp == 0` check (selection, AI, limitations, Struggle) then stays correct without touching it.
- Code changes needed:
  - an Adept branch in `CancelerPPDeduction` that charges `cost × (1 + Pressure count)` to the pool and skips the per-move write-back;
  - Spite, Eerie Spell, Leppa and Ethers either work on the pool or don't affect Adepts;
  - the move menu shows "PP pool/max · cost";
  - write the pool back to Adept storage at battle end.
- Size: about 200–350 lines.
- Add a `psyCost` byte to the move data, or reuse `.pp` as the cost for Psynergy moves.

## 4. Summons on top of the gimmick system (merging Z-Moves and Dynamax)

**The Z-Move system is a good template (VERIFIED):**
- `enum Gimmick` and `struct GimmickInfo` hold `CanActivate`, `ActivateGimmick`, the trigger sprite and trainer-slide hooks (`expansion/include/battle_gimmick.h:6-28`). The table is `expansion/src/data/gimmicks.h:20-29`.
- `AssignUsableGimmicks` gives each battler the first gimmick it can use (`expansion/src/battle_gimmick.c:20-34`).
- Active state is stored per party, not per battler, so it already handles split parties (`:54-63`).
- Z-Moves: `CanUseZMove` checks the Z-Power Ring, once-per-trainer use and the held crystal (`expansion/src/battle_z_move.c:113-142`). `GetUsableZMove` maps a move slot to a Z-move (`:144-160`). `IsViableZMove` / `AssignUsableZMoves` mark which slots can upgrade (`:167-215`). `MoveSelectionDisplayZMove` swaps the menu text (`:262+`). The type-based Z-move comes from `gTypesInfo[type].zMove` (`:245-260`).
- Player toggle: R button / `gimmick.playerSelect` (`expansion/src/battle_controller_player.c:910-917, 2112-2123`).

**Reuse plan (INFERRED):**
- Add `GIMMICK_SUMMON` at the end of the enum, with a `gGimmicksInfo` entry.
- `CanUseSummon(battler)`:
  - true only for an Adept;
  - true only if at least one Summon is affordable;
  - **no once-per-battle rule.** Don't call `HasTrainerUsedGimmick`. (Z-Moves have that limit at `battle_z_move.c:129`; Summons repeat as long as Standby Pokémon last.)
- `GetUsableSummon(battler, slot)`: take the slot's Psynergy type and return the highest tier the Standby pool can pay. Summon moves are new `MOVE_` entries (18 types × 1–3 tiers). Reuse the Z/Max animations as placeholders.
- `ActivateSummon`: mark the paid Standby Pokémon as spent, plus a recovery timer if the design wants the Golden Sun behaviour.
- **Party-wide Standby cost check:**
  - Counting needs to read Adept/Set storage (8 × 3 entries with a Set/Standby/Recovering state), not `gParties`.
  - Take a snapshot into `gBattleStruct` at battle start, spend from the snapshot, write back at the end.
  - Enemy pool: the trainer's benched Pokémon in `OPPONENT_B`, or a small per-trainer type-count table.
- **UI trigger:** the existing R-toggle and trigger sprite, then the Z-style move-name swap showing cost ("2× Fire Standby").
- **Retiring Z and Dynamax:** never give the player the Z-Power Ring or Dynamax Band. Both are item-gated (`battle_z_move.c:119-122`; `CanDynamax` checks the band, `expansion/src/battle_dynamax.c` around line 82). Mega stays for the partner Pokémon.
- Size: about 500–800 lines plus move data.

## 5. Class: computed before battle, frozen during it

**Where the stats come from (VERIFIED):**
- Stats are built in `CalculateMonStatsCont` (`expansion/src/pokemon.c:1380-1440`; the stat formula is at 1414-1419 and HP at 1433-1434).
- They are copied into battle by `PokemonToBattleMon` (`pokemon.c:3366-3409`; types are set from species at 3400-3401).
- In-battle form changes recompute stats through `RecalcBattlerStats` (`expansion/src/battle_util.c:9594`).

**Plan (INFERRED):**
1. **Store class on the Adept itself, not recomputed in battle.** The design is "recompute outside battle when Set Pokémon / partner / form change", so the stored value is always current at battle start.
   - `RecomputeAdeptClass()` is the only function that writes it. It refuses to run if `gMain.inBattle`.
   - Call it once more at battle start as a safety net.
   - Where to store it: the contest-ribbon bits, which this game won't use (5 categories × 3 bits, `pokemon.h` substruct around lines 202-206), or the spare `unused_04:5` / `unused_06:3` bits (around 155-157). Or keep it in the Adept storage record.
2. **Stat effect:** in `CalculateMonStatsCont`, if the species is an Adept, multiply each stat by `classMult[class][tier][stat] / 100`. Because the class is a stored value, Mega or form changes on the partner and `RecalcBattlerStats` can't change it.
   - Max PP comes from the class too.
   - The Psynergy available is a class/element/level list, and 4 of them are loaded into the move slots outside battle.
3. **Element bonus** ("Set Pokémon that match the Adept's group make Psynergy stronger"): a modifier in `CalcMoveBasePowerAfterModifiers` (`battle_util.c:6475`) or next to STAB (`GetSameTypeAttackBonusModifier`, `:7337`).
4. **Type-changing moves** (Soak, Roost, Burn Up) only change `gBattleMons[].types`, never the stored class.
5. **Scoring** is pure integer C: doubled scores (primary 2, secondary 1), then the tie-break rules. About 80 lines plus tables.

Size: about 300–500 lines plus class data.

## 6. AI

**Moves are just moves. VERIFIED.**
- The AI scores moves from `gBattleMons[].moves[4]` using the normal damage calc and limitations (`BattleAI_ChooseMoveIndex`, `expansion/src/battle_ai_main.c:579`).
- With the PP mirror (§3), an enemy Adept that can't afford a Psynergy sees it as unusable automatically.
- Class multipliers are already inside the stats, so the AI's damage simulation is correct.

**Switching:** `ShouldSwitch` and the switch-candidate code use `GetBattlerParty` / `GetAILastPartyIndex` (`battle_ai_switch.c:1420,1540,2612,2646`). So an enemy Adept would only switch to Adepts and an enemy Pokémon only to Pokémon. VERIFIED by reading. I'd turn off AI switching for Adepts at first through AI flags. INFERRED.

**Summons:** copy `IsConsideringZMove` / `ShouldUseZMove` (`expansion/src/battle_ai_util.c:5078-5114`) and `ReconsiderGimmick` (`battle_ai_main.c:441-445`) as `ShouldUseSummon`, plus a bit of cost and value logic. About 100–150 lines.

**Enemy Adept + Pokémon from one trainer (INFERRED design):**
- In `DoTrainerBattle` (`expansion/src/battle_setup.c:490-499`), build the trainer's party once.
- Put mons with `isAdept` into `gParties[OPPONENT_A]` and the rest into `gParties[OPPONENT_B]`.
- Set `opponentB = opponentA` so name strings resolve to the same trainer.
- Then check the intro and send-out text paths (`expansion/src/battle_message.c:2638,2707`; `battle_main.c:3220,3242`; `battle_interface.c:1314-1334`).
- Risk: the intro may read "X and X want to battle".

## 7. Battle UI

- **Action menu:** `HandleInputChooseAction` (`battle_controller_player.c:234`). The menu text is one string, `gText_BattleMenu` (`expansion/src/battle_message.c:1475`), drawn at `battle_controller_player.c:2010`. For an Adept, swap "Battle" for "Psynergy". About 20 lines. The expansion already asks battler 0 then battler 2 in a player-controlled double. INFERRED from the controller setup.
- **Move menu:** `HandleInputChooseMove` (`:677`). PP display is in `MoveSelectionDisplayPPString` / `PPNumber` (`:1674-1695`); show pool and cost. The Summon toggle reuses the gimmick trigger (§4). Type display (`:1697`) and effectiveness (`:2429`) work unchanged.
- **Target selection:** `HandleInputChooseTarget` (`:413`). The standard doubles targeting needs no change.
- **Party / switch screens:** see §1.4. Per-slot layouts reuse `PARTY_LAYOUT_MULTI_FULL(_PARTNER)`. A custom 8-Adept list would only be needed for Option 2.
- **Psynergy beyond 4 slots:** a scrolling Psynergy list would conflict with Disable, Encore, choice-lock, Mimic and similar effects that use slot indexes. Recommendation: keep 4 slots chosen per class until much later.

Size: about 150–300 lines.

## 8. Test framework: usable from day one

**What exists (VERIFIED):**
- `make check` runs a headless test ELF through `mgba-rom-test-hydra` (`expansion/Makefile:362-365`). Prebuilt `tools\mgba\mgba-rom-test` and `mgba-rom-test.exe` are present.
- Battle-test types and party macros: `SINGLE`, `DOUBLE`, `MULTI`, `TWO_VS_ONE`, `ONE_VS_TWO` (plus AI versions), and `PLAYER` / `PARTNER` / `OPPONENT_B` (`expansion/include/test/battle.h:977-992, 1029-1033`).
- `MOVE(..., gimmick:, target:, allowed:)` and `SWITCH(battler, idx)` (`:375-377, 1139, 1157`).
- 21 `MULTI_BATTLE_TEST`s exist, for example `expansion/test/battle/ability/commander.c:928`.
- The runner sets flags per test type (`expansion/test/test_runner_battle.c:504-523`).
- Player battler 2 runs on a recorded controller, so scripted moves work for it (`battle_controllers.c:335-338`).
- Gimmick tests exist to copy: `expansion/test/battle/gimmick/zmove.c`, `dynamax.c`.

**INFERRED:**
- Tests for the FireRed build would run as `make check BUILD=firered` (Makefile:7). Some tests may depend on Emerald data; if so, run the battle tests on the Emerald build, which has the same battle engine.
- Adding an `ADEPT_BATTLE_TEST` type means a macro in `include\test\battle.h` plus a runner case setting `TRAINER | DOUBLE | BATTLE_TYPE_ADEPT`. About 60–80 lines.

Sample outline:
```c
ADEPT_BATTLE_TEST("Psynergy spends the Adept's shared PP pool")
{
    GIVEN {
        PLAYER(SPECIES_ADEPT_HERO) { Moves(MOVE_QUAKE, MOVE_CURE); }   // battler 0, Adepts party
        PARTNER(SPECIES_GOLEM); PARTNER(SPECIES_STEELIX); PARTNER(SPECIES_ONIX); // battler 2, Set Pokémon
        OPPONENT(SPECIES_WOBBUFFET); OPPONENT(SPECIES_WYNAUT);          // stage 1: one trainer's pair
    } WHEN {
        TURN { MOVE(playerLeft, MOVE_QUAKE, target: opponentLeft); MOVE(playerRight, MOVE_TACKLE, target: opponentRight); }
    } SCENE {
        ANIMATION(ANIM_TYPE_MOVE, MOVE_QUAKE, playerLeft);
    } THEN {
        EXPECT_EQ(GetAdeptPP(B_TRAINER_PLAYER, 0), ADEPT_START_PP - GetPsyCost(MOVE_QUAKE));
    }
}
```

Other early tests:
- `SWITCH(playerRight, 1)` brings in a Set Pokémon, never an Adept. The reverse holds for `playerLeft`.
- With the pool below the cost, `MOVE(playerLeft, MOVE_QUAKE, allowed: FALSE)`.
- The partner Mega-evolves (`gimmick: GIMMICK_MEGA`) and the Adept's stats are unchanged (frozen class).
- `gimmick: GIMMICK_SUMMON` uses up N Standby Pokémon of the right type, and fails when there are too few.
- Exp after a KO reaches the slot-B Set Pokémon.
- An enemy Adept that can't afford its Psynergy picks another move (an `AI_` variant).

## 9. Comparison: CFRU and vanilla pokefirered

| | pokeemerald-expansion | CFRU | pokefirered (vanilla) |
|---|---|---|---|
| Parties | 4 × 6 `gParties` (VERIFIED) | Only `gPlayerParty` / `gEnemyParty`. The partner gets slots 0-2 / 3-5 of the same 6 through `LoadPartyRange` (`...\Complete-Fire-Red-Upgrade\src\battle_util.c:1040-1090`, VERIFIED), so each player slot gets only 3 | Only `gPlayerParty` / `gEnemyParty` |
| In-game partner / split pools | Yes, with full teams | Yes, halves only | No. `BATTLE_TYPE_INGAME_PARTNER` doesn't exist (0 files); link multi only (71 refs) — VERIFIED |
| Gimmick framework | Table-driven (Mega, Z, Dynamax, Tera) | Mega, Z, Dynamax as separate modules (`mega.c`, `set_z_effect.c`, `dynamax.c`, VERIFIED) | None |
| How code gets in | Normal C source build | Compiled C/ASM patched into the FireRed binary through hooks (`hooks` file is 759 lines, plus `bytereplacement\` and `functionrewrites\`, VERIFIED). Vanilla RAM symbols and layout are fixed | Normal C source build |
| Tests | Headless battle tests (VERIFIED) | None (no `test` directory, VERIFIED) | None (VERIFIED) |
| Relative effort for this format | 1× | **About 1.5–2.5×** (INFERRED). Giving slot B its own party means redirecting a vanilla RAM array that compiled FireRed code reads directly, and every bug is debugged in an emulator by hand | **About 2–3×** (INFERRED). Split parties, the gimmick and Summon framework, and Gen 4–7 mechanics all have to be built |
| Path to a native port later | Best: plain C, deterministic tests that work as a spec | Worst: logic tied to ROM addresses | Plain C, but much more left to build |

---

## Staged plan

The first stage is the smallest playable slice. Calendar times assume an AI-assisted solo developer (Claude Code writes the code, the user play-tests).

| Stage | What | Main files / functions | Lines (approx.) | Calendar | Risks |
|---|---|---|---|---|---|
| 0 | Fork the expansion into a project repo; `make firered` and `make check` passing | Makefile, CI script | ~0 | 0.5–1 day | Some tests may assume Emerald data (INFERRED) |
| **1 (smallest playable slice)** | 1 Adept + 1 Pokémon (player controls both) vs a trainer's Pokémon pair from one party. Fixed Adept species, Set Pokémon copied from storage into the partner party, per-slot switching, exp to both, write-back after battle | `constants/battle.h:115` (new flag); `BattleSideHasTwoTrainers` and `AreMultiPartiesFullTeams` set TRUE for the player side; `SpeciesInfo.isAdept` and one Adept species (placeholder art); battle-start and end hooks (`battle_setup.c` `DoTrainerBattle`, `battle_main.c` `HandleEndTurn_FinishBattle`); `party_menu.c:7482-7529`; `Cmd_getexp`; `ADEPT_BATTLE_TEST` with 5–8 tests | 350–500 | **4–7 days** | Hidden shared-party assumptions (about 20 sites); exp state machine; HP/PP write-back |
| 2 | Psynergy moves plus the shared PP pool | Move data (`psyCost`); `CancelerPPDeduction`; PP mirror; Spite/Eerie/Leppa/Ether; PP display; save the pool | 300–500 (+ data) | 4–7 days | Interactions (Pressure, Mimic, Transform) |
| 3 | Enemy Adept + Pokémon; changing Adepts with the slot-B pool reload; 6-Adept battle roster | `DoTrainerBattle` split; opponent-side `BattleSideHasTwoTrainers`; message, intro and healthbox paths; Adept switch-in reloads `gParties[B_TRAINER_PARTNER]` and resets `partyState`; AI flags | 400–700 | 1–2 weeks | Highest risk: double-switch semantics, intro text, `partyState` desync |
| 4 | 18-type classes (frozen), tiers, element bonus | `RecomputeAdeptClass` (outside battle only); class field; `CalculateMonStatsCont` multipliers; max PP; class Psynergy loadout; damage-calc bonus | 300–500 (+ class tables) | 1–1.5 weeks | Balance; where to store class bits |
| 5 | Summons (Z and Dynamax merged in) with the party-wide Standby pool | `GIMMICK_SUMMON` (`battle_gimmick.h`, `data/gimmicks.h`); `GetUsableSummon`, display, `ActivateSummon` (copying `battle_z_move.c`); Standby snapshot; AI `ShouldUseSummon` | 500–800 (+ moves) | 1.5–2.5 weeks | Unresolved Set/Standby rules; enemy Standby source |
| 6 | Wild battles: Adept + partner vs 1 wild (the missing slot is handled by the existing empty-slot code, `battle_main.c:3429-3437`) or vs 2 (`WILD_DOUBLE_BATTLE`, 14 refs); catching rules; running away | `battle_setup.c` wild start; `item_use.c:1142` "two Pokémon" rule | 100–250 | 3–5 days | Catching with two Pokémon out |
| 7 | Battle UI pass: Psynergy label, pool display, Summon cost text, class on the summary screen; optional 8-Adept list | `battle_controller_player.c`, `battle_message.c`, `pokemon_summary_screen.c`, `party_menu.c` | 200–500 | 1 week (+1 for 8-Adept) | Text box space |

**Total:** about 2,000–3,500 lines plus data, **7–11 weeks**, medium-low confidence.

**What would change the estimate:**
- **Shorter:**
  - Adept switch leaves the current partner on the field.
  - 6-Adept battle roster.
  - Summons cost Standby Pokémon with no recovery timers.
  - 4-slot Psynergy.
- **Longer:**
  - Forced partner swap when Adepts change.
  - All 8 Adepts selectable in battle.
  - A scrolling Psynergy list.
  - Bugs in the player-controlled split-party path that the upstream multi tests don't cover.
  - Merging upstream expansion releases.

**Open design questions that block stages 3 and 5:**
1. When the Adept changes, does the partner swap at once?
2. Is the battle roster 6 Adepts or all 8?
3. Can a Standby Pokémon be the fighting partner, and do spent Standby Pokémon recover after N turns?
4. Is Psynergy capped at 4 in battle?
5. Where does an enemy's Standby pool come from?

**Native-port note (INFERRED):** keep all Adept, class and Summon logic in new files (for example `src\adept_battle.c` and `src\adept_class.c`) behind thin hooks. That keeps upstream merges easy, and the tests become a portable spec for a later native Android build.