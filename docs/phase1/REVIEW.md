# Red-team review of the phase-1 findings

**Verdict: the recommendation stands with changes.** No alternative code base wins. Still, several assumptions are wrong or missing. The biggest gaps are:
- **No estimate covers where the 8 Adepts and 24 Set Pokémon live.** This is a cross-cutting job and is now the top risk.
- **The FireRed build has almost no free save space by default.**
- **The FireRed target's tests are never run in CI.**
- **The battle plan conflicts with DESIGN.md on how many Adepts can be used in battle.**
- **The build order puts the Set-Pokémon field-move rule before the storage it depends on.**

Paths: `expansion/` = pokeemerald-expansion 1.17.2 (commit `8fb02c6f`), `pokefirered/` = pret pokefirered, `nm.txt` = a symbol dump (`arm-none-eabi-nm`) of today's FireRed build of the expansion (not kept).
Labels: **V** = verified in source or build output today; **I** = inferred.

---

## 1. What the findings recommend

1. **Code base:** pokeemerald-expansion, pinned to a release tag and forked. Build the FireRed target (`make firered`), with the expansion's Emerald target as the fallback.
2. **Movement:** build option A (diagonal steps on the tile grid) now, at 2–3 weeks. Option B (free movement, player only) is an optional later "free mode", at 6–10 weeks.
3. **Order:**
   1. Base setup, about 1–1.5 weeks: fork, FireRed as default, config switches, test pipeline.
   2. First code items: the Set-Pokémon field-move unlock, auto-run, and the underwater tileset.
   3. Battle stage 1 (1 Adept + 1 Pokémon), then movement A.
   4. Then Psynergy and the shared PP pool, enemy Adepts, classes, Summons; the water rules and the ship.

---

## 2. Trying to refute it

### 2.1 CFRU (how Unbound was built)
- **Strongest case:**
  - Unbound is built on it, so Unbound's feel comes for free.
  - It already has full field Dive with Unbound's rule (an HM in the bag plus a party Pokémon that can learn it), `PartyHasMonWithFieldMovePotential` (CFRU `src/overworld.c:2381-2416`).
  - It also has auto-run, DexNav and HM-in-bag.
  - The user already has an Unbound symbol diff.
- **Why it fails:**
  - **The advantage only matters if we keep Unbound's content, and we don't.** DESIGN.md:110 calls for a brand-new region, and DESIGN.md:179 says Unbound's maps, story and music aren't open (**V**).
  - **Its party model doesn't fit our format.** The battle partner gets party slots 0–2 or 3–5 of one shared 6-slot party (the battle investigator found this at CFRU `src/battle_util.c:1040-1090`; I did not re-check it). That caps the Adept side at 3 Adepts, against 8 in the design.
  - It has no tests, maps are edited in binary tools, and the code is tied to ROM addresses, so a native Android port is impossible.
- **Refuted.**

### 2.2 pret pokefirered (the vanilla FireRed decomp)
- **Strongest case:** the smallest and most stable code base, with no upstream churn to merge.
- **Why it fails:**
  - It has only Gen 1–3 Pokémon and no Megas, regional forms, DexNav or battle-gimmick framework.
  - Dive is only half there: `TrySetDiveWarp` is `static` and never called (`pokefirered/src/field_control_avatar.c:1143`, **V**).
  - Bringing the expansion's roster and battle engine into it would just recreate the expansion's FireRed target. The expansion's FireRed support came from cawtds, who did exactly that and then merged it upstream (`expansion/docs/changelogs/1.15.x/1.15.0.md:100,149`, **V**).
- **Refuted.**

### 2.3 The expansion's Emerald target (the strongest alternative)
- **Strongest case:**
  1. **Tests:** CI runs the test suite only on the default (Emerald) build. `build.yml:88` builds FireRed, but `:200` runs `make -j$(nproc) check` with no `BUILD=` setting (**V**).
  2. **Maturity:** the FireRed target first shipped in 1.15.0 with the note "FRLG is playable, but missing some features" (`1.15.0.md:151`, **V**). `how_to_frlg.md:73` warns that its build-system workarounds "might cause merge conflicts down the line" (**V**).
  3. **Dive content:** underwater tiles, maps and sprites work out of the box.
  4. **Save space:** the FireRed build's SaveBlock1 carries extra FireRed fields and has only about 116 bytes free (§2.5).
  5. **Placeholders:** every map is new anyway, and DESIGN.md:9 allows "FireRed/vanilla" placeholder art.
- **Why the FireRed target still edges it out:**
  - **It is the same engine.** The FireRed-only switches in battle and field code are narrow. The Oak/Old Man tutorial controllers at `expansion/src/battle_controllers.c:293-295` are an example (**V**).
  - **No test is FireRed-aware.** `test/` contains no `IS_FRLG`, `GAME_VERSION` or `FIRERED` (**V**, 0 matches). So battle tests should behave the same on both builds (**I**).
  - **It has bigger tilesets for the later Golden Sun art.** The primary tileset holds 640 tiles and 7 palettes, against Emerald's 512 and 6 (`expansion/include/fieldmap.h:4-10`, **V**).
  - **It matches the requested FireRed placeholder look,** and its build is already verified.
- **Correction to the codebase report:** switching target later is not a cheap 1–3 days once real maps exist.
  - Tilesets are compiled for one game only: `src/data/tilesets/headers.h:31` (`#if !IS_FRLG`), `:836` (`#else`), `:1543` (**V**).
  - The map tool drops any layout whose format doesn't match the build (`expansion/tools/mapjson/mapjson.cpp:793-795`, **V**).
  - So the choice has to be locked in week 1, after a go/no-go gate (§4).
- **New escape hatch:** the engine already handles each layout's format at runtime, through `mapLayout->isFrlg` (`expansion/src/fieldmap.c:57,412-422,469-506`, **V**).
  - Patching the map tool's filter (about 2 lines) and moving Emerald's General + Underwater tilesets out of the `#if !IS_FRLG` block could let Emerald-format underwater maps build inside the FireRed ROM. That would avoid the tile and palette re-indexing port (**I**, needs a smoke test).
  - Tileset animations and palette paths may have other FireRed switches I did not check.
- **Not refuted, but the FireRed target needs a day-1 gate.**

### 2.4 Free movement (option B) first
- **Strongest case:**
  - DESIGN.md:114 makes free 8-way movement *the* decision; grid diagonal is only the fallback (DESIGN.md:164).
  - About 60–70% of A doesn't carry over to B.
  - The feel matters most on a phone.
- **Why it fails:**
  - B's estimate is low-confidence (40–50%), and no public decomp branch has done free movement.
  - B (player-only free mode) keeps every map, trigger and script on the grid. So maps written during A remain compatible with a later B, and doing A first carries little rework risk.
  - A gives a playable build in 3–5 days.
  - A native port can do analog free movement much more cheaply.
- **Refuted, with one change:** run the 1–2 day speed measurement of Golden Sun with gbax *before* tuning A, so A's diagonal timing and input grace window already match Golden Sun.

### 2.5 Failure modes checked

**Dive in the FireRed build: works in code (V).**
- `TrySetupDiveDownScript` and `TrySetupDiveEmergeScript` check only the follower-NPC flag, `IsFieldMoveUnlocked(FIELD_MOVE_DIVE)` and `TrySetDiveWarp` (`expansion/src/field_control_avatar.c:661-685`).
- The FireRed ELF links all the Dive code: `FldEff_UseDive`, `TrySetDiveWarp`, `EventScript_UseDive` and `EventScript_UseDiveUnderwater`, `Bubbles_Main`, `gBattleEnvironmentTiles_Underwater` (nm.txt:76110, 86325, 79070, 76575, 92145, 100593).
- `gTileset_Underwater` is absent from the ELF.
- Underwater music is not overridden in the FireRed build (`expansion/src/overworld.c:1304-1307`).
- The unlock is badge 7 (`expansion/src/field_move.c:104-110`).
- `FLAG_RECEIVED_HM_DIVE = 0` in the FireRed flags file (`flags_frlg.h:1552`), but only Emerald map scripts use it, so it is harmless.

**Save space: a real constraint the findings understated (V, worked out from nm.txt plus the save layout).**
The ASLR structs are each save block plus a 128-byte buffer (`expansion/include/load_save.h:7,14-21`). SaveBlock1 gets 4 sectors and storage gets 9 (`expansion/src/save.c:60-75`); each sector holds 3,968 bytes (`expansion/include/save.h:7`).

| Block | Size in today's FireRed build | Capacity | Free |
|---|---|---|---|
| SaveBlock1 | 0x3E0C − 128 = 15,756 B | 4 × 3,968 = 15,872 B | **≈116 B** |
| SaveBlock2 | 0xFAC − 128 = 3,884 B | 3,968 B | **≈84 B** |
| PokemonStorage | 0x85E0 = 34,272 B | 9 × 3,968 = 35,712 B | **≈1,440 B** |
| SaveBlock3 | 4 B (nm.txt:4921) | 1,624 B | ≈1,620 B |

What this means:
- **The `FREE_*` switches are mandatory before any new save field,** not optional.
  - Their sum is **3,860 B plus Trainer Tower** (`expansion/include/config/save.h:8-22`), not 3,790.
  - Not all of it comes out of SaveBlock1 (**I**).
- **The 24 Set Pokémon (24 × 80 B = 1,920 B) don't fit in SaveBlock3.** The reserved-box plan is therefore required, not just convenient.
- **Adepts 7 and 8 also need a home** (also a reserved box, or a second one: 8 + 24 = 32 > 30 slots).
- **DexNav search levels need 1 byte per species** and are flagged as possibly too big for the save (`expansion/include/config/dexnav.h:5`, **V**). They would take most of SaveBlock3.

**ROM budget.**
- Used space independently confirmed: `__ewram_lma` sits at 0x099B6A28, so 0x19B6A28 bytes = **25.71 MiB used, 6.29 MiB free** (nm.txt, **V**).
- The function phase is safe.
- The polish phase is tight under the hard 32 MiB GBA ceiling: converted Golden Sun music, Summon animations and tilesets could take several MiB (**I**).
- Correction: setting Gen 8/9 to FALSE does not give a strict "Gen 1–7" roster.
  - Families are assigned to the generation of their first member, so later evolutions such as Sneasler stay (`species_enabled.h:5-8`, **V**).
  - The regional-form switches (`:35-39`) must also be decided.

**Battle-engine assumptions: nothing blocks the format (V).**
- In a non-link double battle, battler 2 is already player-controlled (`expansion/src/battle_controllers.c:339-342`).
- Which party a battler uses goes through `BattleSideHasTwoTrainers` (`:3345,3353-3359`).
- When a side has two trainers, battler 2 starts at slot 0 of its own party (`:370`), which supports the plan.
- `BATTLE_TYPE_14` is unused: its definition at `constants/battle.h:115` is the only match.

**Party architecture: new and missing from every estimate (V count, I impact).**
- `gParties[B_TRAINER_PLAYER]` appears **802 times in 76 `src` files**. Examples: party_menu 150, field_specials 37, script_pokemon_util 35, pokemon_storage_system 49, wild_encounter 13, egg_hatch 12, pokerus 16, daycare 9.
- Healing, item use, catching destination, Repel and lead-Pokémon checks, followers, overworld abilities, field poison and out-of-battle evolution all assume "the party = your Pokémon".
- With Adepts in the party and Set Pokémon in separate storage, all of these need re-targeting or switching off.
- The battle plan only covers the in-battle load and write-back. Post-battle evolution also walks only the player party (`expansion/src/battle_main.c:5369-5397`, **V**).

**Design conflict (V).**
- DESIGN.md:42 says "8 Adepts … the others swap in".
- The battle plan's recommended option 1 is a 6-Adept battle roster, because `PARTY_SIZE` is 6 (`expansion/include/constants/global.h:82`).
- That is a scope cut the user has to approve. Supporting all 8 costs +200–400 lines and about +1 week.

**Movement costs.**
- A's three latent bugs are real (table below).
- There are enough free movement-action IDs: the last one is 0xB5 and `STEP_END` is 0xFE, so 72 IDs are free (`expansion/include/constants/event_object_movement.h:273-281`, **V**).
- I widen A to **2–4 weeks**, because tuning touch input on the Fold and followers usually takes iteration (**I**).
- B stays at 6–10 weeks, low confidence.

**Native Android port.**
- There are about 174 places that store a pointer in a 32-bit value across 32 files (`SetWordTaskArg`, `T1_READ_PTR` and similar); 100 of them are in `contest_ai.c`, which can be cut (**V** count).
- Script bytecode also embeds 4-byte pointers (**I**).
- So an arm64 port is real work for any base, but it is not a reason to pick a different decomp. CFRU is the only base it rules out.

---

## 3. Re-checked claims

| # | Claim (source report) | Checked at | Result | Correction |
|---|---|---|---|---|
| 1 | Dive input path is not FireRed-gated; only the follower flag and unlock are checked (codebase, dive-water) | `expansion/src/field_control_avatar.c:661-685` | CONFIRMED | — |
| 2 | Dive code is linked into the FireRed ROM; `gTileset_Underwater` is not | nm.txt:57073, 76110, 79070, 86325, 92145, 100593 | CONFIRMED | — |
| 3 | Dive unlock is badge 7; `FLAG_RECEIVED_HM_DIVE` is 0 in FireRed | `expansion/src/field_move.c:104-110`; `flags_frlg.h:1552` (used only in Mossdeep scripts) | CONFIRMED | Harmless |
| 4 | pokefirered has "no `FLDEFF_USE_DIVE` (grep found nothing)" (codebase) | `pokefirered/include/constants/field_effects.h:48`; `pokefirered/data/scripts/field_moves.inc:221,242` | **WRONG** | `FLDEFF_USE_DIVE` (44) and its scripts exist. Only the input hook is dead (`pokefirered/src/field_control_avatar.c:1143`, static and never called). The conclusion is unchanged |
| 5 | Battler 2 is player-controlled in a plain double; party routing goes through `BattleSideHasTwoTrainers` (battle) | `expansion/src/battle_controllers.c:339-342, 3345, 3353-3359, 370` | CONFIRMED | Line 370 also starts battler 2 at its own party's slot 0 |
| 6 | `BATTLE_TYPE_14` is unused (battle) | grep `*.c/*.h`: only `constants/battle.h:115` | CONFIRMED | — |
| 7 | Post-battle evolution walks only the player party (battle) | `expansion/src/battle_main.c:5369-5397` | CONFIRMED | — |
| 8 | `IsMetatileDirectionallyImpassable` indexes 4-entry arrays with `direction - 1` (movement) | `expansion/src/event_object_movement.c:975-987, 6513-6520` | CONFIRMED | — |
| 9 | The player's facing is forced cardinal during diagonal moves (movement) | `event_object_movement.c:3630-3652` | CONFIRMED | — |
| 10 | Ledge mapping sends SE to North (movement) | `event_object_movement.c:9871-9895`; `expansion/include/constants/global.h:206-215` (`CARDINAL_DIRECTION_COUNT` = 5) | CONFIRMED | — |
| 11 | `dirn_to_anim` off-by-one (movement) | `event_object_movement.c:6826-6835` | CONFIRMED | Direction 5 reads past the copied array; directions 6–8 fall back to entry 0 |
| 12 | SaveBlock3 can hold up to 1,624 B (codebase) | `expansion/include/global.h:257-275`; `save.c:80`; `save.h:8,24` (116 × 14) | CONFIRMED | Also: SaveBlock1 ≈116 B and SaveBlock2 ≈84 B free (§2.5) |
| 13 | `FREE_*` reclaims 3,790 B (codebase) | `expansion/include/config/save.h:8-22` | **WRONG (minor)** | 3,860 B plus Trainer Tower |
| 14 | `make check BUILD=firered` is supported; CI only builds FireRed (codebase) | `expansion/Makefile:7-21`; `1.15.1.md:37`; `build.yml:88,200` | CONFIRMED | Whether all tests pass on FireRed is UNVERIFIABLE today: running it would write into the build tree |
| 15 | "FRLG is playable, but missing some features"; build-system disclaimer (codebase) | `1.15.0.md:151`; `how_to_frlg.md:73` | CONFIRMED | — |
| 16 | 25.71 MiB of 32 MiB used (codebase) | nm.txt `__ewram_lma` = 0x099B6A28 | CONFIRMED | — |
| 17 | Emerald tilesets compiled only in non-FireRed builds (codebase, dive-water) | `headers.h:31/836/1543`; `mapjson.cpp:785-795` | CONFIRMED | But the engine handles each layout's format at runtime (`fieldmap.c:57,412-422`), so mixing formats may be possible (§2.3, **I**) |
| 18 | Setting Gen 8/9 to FALSE gives Gen 1–7 (codebase) | `species_enabled.h:5-8, 16-17, 35-39` | **PARTLY WRONG** | Later evolutions of older families stay unless the regional-form switches are also set |
| 19 | 14 PC boxes; `PARTY_SIZE` 6; `MAX_MON_MOVES` 4 | `pokemon_storage_system.h:4`; `constants/global.h:82,136` | CONFIRMED | — |

---

## 4. Corrected recommendation

**Code base:**
- Keep pokeemerald-expansion, pinned to a release tag and forked, building the FireRed target. Keep the Emerald target as a fallback, **decided by the end of week 1**.
- **Day-1 go/no-go gate:**
  - Run `make check BUILD=firered` and `make check`, saved as scripts, and compare the failures.
  - If any battle test fails only on FireRed, or Dive or the save breaks in a smoke test, switch to the Emerald target before any map content exists.

**Movement:** option A first; option B as a later optional mode only after play-testing A on the Fold 7.

**Order:**
1. **Week 1, base setup.**
   - Fork and make FireRed the default.
   - Run the test gate.
   - Config: **all `FREE_*` on (mandatory)**; Gen 8/9 off, plus a decision on the regional-form, Gigantamax, Tera and fusion switches; DexNav on, with search levels off; `P_CAN_FORGET_HIDDEN_MOVE`.
   - Write down a save budget.
2. **Days 3–7, a data-model spike before any battle or field-move code:**
   - Adept-as-species.
   - Set storage in a reserved box; Adepts 7–8 location.
   - Which party array holds Adepts vs Pokémon, and a party-menu, heal and catching plan.
   - **User decisions needed:**
     1. Can all 8 Adepts be used in battle, or 6?
     2. Does the partner swap at once when the Adept changes?
3. **Battle stage 1** (4–7 days), with `ADEPT_BATTLE_TEST`.
4. **Movement A** (2–4 weeks; the Golden Sun speed measurement first).
5. **Water:**
   - Dive placeholder (0.5–2 days; try the mixed-format layout first).
   - The Set-Pokémon field-move rule (2–4 days, now *after* Set storage).
   - Limited Surf (1.5–3 days).
6. Battle stages 2–5, then the ship and the world map.

**Estimate changes:**
- Base setup grows from 1–1.5 weeks to **1.5–2 weeks**.
- New line item: the party / Set-storage layer outside battle, **2–4 weeks** (**I**, medium-low confidence).
- Movement A grows to **2–4 weeks**.
- Battle stays at 7–11 weeks, plus about 1 week if all 8 Adepts can be used in battle.

## 5. Remaining risks, ranked

1. **Party and Set-storage architecture.** Unsized and cross-cutting (802 references to the player party). It decides how battle write-back, field moves, menus, healing and catching work.
2. **The 8-vs-6 Adept scope conflict** with DESIGN.md:42, plus the open battle design questions (partner swap, Standby recovery) that block stages 3 and 5.
3. **FireRed-target maturity.** Tests aren't run on it in CI, it is about 7–8 months old, and its build approach may cause merge conflicts later. The gate above mitigates this, but the target is locked once maps exist.
4. **Upstream churn against our battle edits.** Keep our code in new files with thin hooks, and merge only at minor releases.
5. **Movement:** A's feel with touch input; B is low-confidence if it is ever wanted.
6. **Save headroom.** Manageable only with `FREE_*`, a reserved box and no DexNav search levels.
7. **ROM space in the polish phase** (Golden Sun music, Summon animations, tilesets) under the hard 32 MiB limit.
8. **Dive tileset.** Low: the mixed-format route needs to be proven, or a crude placeholder works.
9. **Native port.** 64-bit cleanup is needed and no port of the expansion exists. Long-term only.

**What would change the verdict:**
- Battle tests failing only on FireRed, or the mixed-format experiment showing hidden FireRed switches in tileset code: switch to the Emerald target.
- The user requiring all 8 Adepts *and* a forced partner swap: the battle timeline grows by about 2–3 weeks, though the code-base choice stays.
