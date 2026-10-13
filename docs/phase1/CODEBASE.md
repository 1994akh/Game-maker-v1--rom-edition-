# Code base recommendation (phase 1)

> **Corrections from the review ([REVIEW.md](REVIEW.md)):**
> - pokefirered *does* have `FLDEFF_USE_DIVE` and its Dive scripts. Only the input hook is dead (`TrySetDiveWarp` is static and never called). The conclusion is unchanged.
> - The `FREE_*` switches reclaim 3,860 B plus Trainer Tower, and they are **mandatory**: in the FireRed build SaveBlock1 has about 116 B free and SaveBlock2 about 84 B.
> - Turning Gen 8/9 off doesn't give a strict Gen 1–7 roster. Later evolutions of older families (e.g. Sneasler) stay unless the regional-form switches are set too.
> - Switching from the FireRed target to the Emerald target is **not** a cheap 1–3 days once real maps exist. Decide by the end of week 1, after the test gate (both `make check` runs).
> - Base setup is 1.5–2 weeks, not 1–1.5.

**Recommendation:** use **pokeemerald-expansion**, pinned to a release tag, and build its **FireRed target with `make firered`**. Fork it into our own repo. Fall back to the expansion's Emerald target if the FireRed target causes problems.

**Why:**
- **It is the only candidate that meets every DESIGN.md "function first" requirement in C source:**
  - engine-level field Dive with underwater maps;
  - the Gen 1–9 roster with per-generation switches;
  - Megas, Z-Moves and Dynamax built on a gimmick framework;
  - regional forms and region-aware evolutions;
  - DexNav, overworld Pokémon objects and follower NPCs;
  - about 6,000 automated tests, about 5,000 of them battle tests;
  - modern GCC, Porymap, CI and an active release cadence.
- **It keeps the native Android path open.** It is full C source with almost no assembly, and native SDL and Android ports already exist for its parent, pret pokeemerald.

Label key: **V** = VERIFIED (seen in code, docs or output today). **I** = INFERRED.

---

## 1. Key evidence per requirement

### R1 — Field Dive with underwater maps
- **Expansion, both targets (V):** Dive is engine-level and the FireRed target does not switch it off.
  - `TrySetupDiveDownScript` / `TrySetupDiveEmergeScript` check only `IsFieldMoveUnlocked(FIELD_MOVE_DIVE)` and the follower flag (`src/field_control_avatar.c:661-681`). `TryDoDiveWarp` is at `:1221-1239`.
  - The only FireRed switches (`IS_FRLG`) in that file are at `:484` and `:527`, outside the Dive path.
  - `FIELD_MOVE_DIVE` is an entry in the data-driven table (`src/field_move.c:104`).
- **Expansion FireRed-target gaps, cosmetic (V):**
  - The underwater player sprite falls back to Red/Green's *surf* sprite (`include/constants/event_objects.h:11,20`).
  - Emerald tilesets, including `gTileset_Underwater` (`src/data/tilesets/headers.h:506`), are compiled only in non-FireRed builds (`#if !IS_FRLG` at `headers.h:31`–`1543`).
  - So the FireRed target needs an underwater tileset ported or un-gated (**I**: 1–3 days).
- **Emerald target (V):** all of this works out of the box. There are 14 underwater map folders under `data/maps`.
- **pret/pokefirered (V):** only leftover dive-warp plumbing (`src/field_control_avatar.c:1120-1132`, `MetatileBehavior_IsDiveable`). There is no `TrySetupDiveDownScript` and no `FLDEFF_USE_DIVE` (grep found nothing). The Dive field move, scripts, field effect and underwater avatar would have to be ported from Emerald (**I**: 300–600 lines, 3–6 days).
- **CFRU (V):** has full field Dive (`src/overworld.c:2661-2747`), using Unbound's "party Pokémon that can learn it" check (`PartyHasMonWithFieldMovePotential`, `:2697`).

### R2 — Battle hackability and tests
- **Expansion, C source (V):**
  - About 170k lines in `src/battle_*.c`.
  - A table-driven gimmick framework, `struct GimmickInfo` with `CanActivate`/`ActivateGimmick` (`include/battle_gimmick.h:17-28`), with separate `battle_z_move.c`, `battle_dynamax.c` and `battle_terastal.c`. A "Summon" gimmick would be a new table entry.
  - Test framework (`test/`, 968 `.c` files):
    - battle macros: 3,496 `SINGLE_BATTLE_TEST`, 953 `DOUBLE_BATTLE_TEST`, 369 `AI_SINGLE_BATTLE_TEST`, 174 `AI_DOUBLE_BATTLE_TEST`, 21 `MULTI_BATTLE_TEST`;
    - plus 920 `TEST(` cases.
  - The tests run headless through mgba-rom-test (`Makefile:228-235`, `check:` at `:362`). CI runs `make check` (`.github/workflows/build.yml:200`).
- **CFRU (V):** C compiled with devkitARM and inserted into a FireRed ROM at an offset (`README.md:84-111`), with a 759-line `hooks` file. Unbound itself has 678 hooked symbols (`reports/symbol_diff.md` status table). There is no test framework (no `test*` in the repo).
- **pokefirered (V):** the vanilla Gen 3 battle engine, matching source and no test directory.

### R3 — Roster and data
- **Expansion (V):**
  - Per-generation switches `P_GEN_1..9_POKEMON` (`include/config/species_enabled.h:9-17`).
  - `P_MEGA_EVOLUTIONS`, `P_PRIMAL_REVERSIONS`, `P_GIGANTAMAX_FORMS`, `P_TERA_FORMS` and `P_REGIONAL_FORMS` (`:23-39`).
  - Evolution conditions include `IF_REGION`/`IF_NOT_REGION`, `IF_IN_MAP`, `IF_SPECIES_IN_PARTY` and `IF_KNOWS_MOVE` (`include/constants/pokemon.h:294-320`).
  - DexNav: `src/dexnav.c`, `DEXNAV_ENABLED` (`include/config/dexnav.h:4`).
  - Overworld Pokémon objects for every species and followers (`include/config/overworld.h` "Overworld Pokémon" and "Follower Pokémon" blocks), plus follower NPCs (`src/follower_npc.c`).
  - `P_CAN_FORGET_HIDDEN_MOVE` (`include/config/pokemon.h:57`).
  - **Missing:** there is no auto-run config (grep of `include/config/` found nothing).
  - **Field moves:** unlocks go through a function-pointer table (`src/field_move.c:27-44`, `include/field_move.h`). Adding a "any Set Pokémon can learn it" unlock type is small (**I**: about 60–120 lines).
- **CFRU (V):** DexNav, `FLAG_AUTO_RUN`, Megas, Dynamax, raids, followers, and HM-in-bag usage (`src/config.h:24,54,61,74,217-218,259`). DPE was last updated 2022-01-17 and DPE-Unbound 2022-11-08 (local git log).
- **pokefirered:** Gen 1–3 only, with no Megas, Z-Moves, Dynamax or DexNav (**V**, vanilla).

### R4 — 8-way movement
- **No base has player diagonal input.** `src/field_player_avatar.c` contains 0 "diagonal" matches (**V**).
- **Expansion (V):**
  - `DIR_SOUTHWEST..DIR_NORTHEAST` (`include/constants/global.h:211-215`).
  - Diagonal movement actions `MOVEMENT_ACTION_WALK_{NORMAL,SLOW,FAST}_DIAGONAL_*` (`include/constants/event_object_movement.h:236-243,270+`), 40 "diagonal" matches in `src/event_object_movement.c`.
  - Sideways-stairs tile behaviors (`include/constants/metatile_behaviors.h:78-83`).
  - This is the best starting point for the grid-diagonal fallback.
- **pokefirered (V):** the `DIR_*` diagonal constants exist (`include/constants/global.h:114-117`), but there are 0 diagonal movement actions.
- **CFRU (V):** no overworld diagonal code; the only match is in `battle_anims.c`.
- Free movement is a new subsystem on every base; on the GBA it is cheapest in C decomp code (**I**).

### R5 — Save space
- **Expansion (V):**
  - SaveBlock3 lives in the spare bytes at the end of each save sector, up to 1,624 bytes (`include/global.h:257-275`, `src/save.c:80`).
  - The `FREE_*` switches can reclaim 3,790 bytes (`include/config/save.h`).
  - The FireRed target's SaveBlock1 carries Emerald fields plus FireRed-only fields: Trainer Tower, rival name, Route 5 daycare (`include/global.h:1205-1213`).
  - There are 14 PC boxes (`include/pokemon_storage_system.h:4`). The 24 Set Pokémon can live in a reserved box at almost no extra save cost (**I**).
- **CFRU (V):** expands the save by "parasitic" use of spare sector space plus sectors 30/31 (`src/save.c:17-118`, "Frees up 0xEC4 bytes").
- **pokefirered:** vanilla layout, which we would extend ourselves (**I**).

### R6 — ROM budget
Measured on today's FireRed build of the expansion (**V**, from `romsize.sh` and `cries.sh`):
- **Used:** 25.71 MiB of 32 MiB, with 6.29 MiB free.
- **Cries:** 9.00 MiB, the largest item. Gen 8 cries are 0.76 MiB and Gen 9 cries 1.04 MiB.
- **Species graphics:** about 3.6 MiB. Gen 8 and Gen 9 are about 0.29 MiB each.
- **If Gen 8 and 9 are switched off:** at least about 2.4 MiB more free space, so about 8.7 MiB free (**I**, not rebuilt). `P_CRIES_ENABLED` notes that cries are over 25% of the ROM (`include/config/pokemon.h:52`).
- **Weyard data:** 57 species plus 14 Mega/Primal forms reusing existing sprites is small (**I**).
- **Other bases:** CFRU and DPE also fit in 32 MiB, as Unbound shows. pokefirered builds a 16 MB ROM by default (**I**).

### R7 — Toolchain
- **Expansion (V):**
  - Modern GCC (`-std=gnu17 -DMODERN=1`, `Makefile:159`). gcc 14.2.1 was verified today.
  - Debug menus `DEBUG_OVERWORLD_MENU` and `DEBUG_BATTLE_MENU` (`include/config/debug.h:5,11`).
  - CI builds the Emerald, FireRed and LeafGreen targets (`build.yml:53,88,123`).
  - mdbook docs, including a FireRed guide (`docs/tutorials/how_to_frlg.md`).
  - Release cadence: a minor release every 3 months and a patch at least monthly (`docs/team_procedures/schedule.md:5-9`). Releases 1.16.0 → 1.17.1 came out May 29 → Sep 29. The local HEAD is from 2026-10-12.
- **pokefirered (V):** agbcc by default, with modern GCC optional (`Makefile:38`). Porymap has a pokefirered mode. Last commit 2026-09-26.
- **CFRU (V):** devkitARM plus `python scripts/make.py`, XSE-style scripts (`xse_commands.s`) and a PDF/DOCX manual. Last commit 2025-01-24. It has no Porymap support because the maps live in the ROM binary (**I**).
- **License:** none of the three has a LICENSE file (**V**). This is fine for personal use.

### R8 — Native Android path
- **Expansion (V):** 384 C files in `src`, only 5 `.s` files, and 4 C files with inline asm. That makes a platform layer feasible.
- **Existing native ports of pret pokeemerald (V, web):**
  - NTx86/pokeemerald-sdl2pc (Windows/Linux);
  - fuddlesworth/pokeemerald-native (Windows/Linux/macOS);
  - ZallaxDev/pokeemerald-3Ds-dualscreen (3DS);
  - psspssr/pokeemerald-3Ds-dualscreen-thor, an Android port with dual-screen touch menus and controller support. It is **armeabi-v7a only**, Android 9+, and in beta.
- **No native port of the expansion or of pokefirered was found (I** — the search was not exhaustive).
- The Z Fold 7 most likely needs arm64 (**I**). That means 64-bit cleanup is still unsolved even in the existing Android port.
- **CFRU:** a binary patch over a FireRed ROM, so it can only run under emulation (**I**, structural).

### R9 — Reuse of what we have
- **Expansion:**
  - The WSL toolchain and today's FireRed build are reused directly (**V**).
  - FireRed placeholder assets are in the FireRed target: 419 `*_Frlg` map folders and the FRLG tilesets (**V**).
  - CFRU, DPE and Unbound code becomes readable reference for behavior, for example the HM-potential check (**I**).
- **CFRU:** reuses Unbound engine knowledge 1:1, but nothing else carries over.

---

## 2. Comparison table

| Criterion | (a) CFRU+DPE on FireRed v1.0 | (b) pret/pokefirered | (c1) Expansion, Emerald target | (c2) Expansion, FireRed target **(rec.)** | (d) Others |
|---|---|---|---|---|---|
| 1 Dive and underwater maps | Yes, full (overworld.c:2661-2747) | Warp plumbing only; port 3–6 days | Yes, with tiles and sprites | Engine yes; underwater tileset is Emerald-only (headers.h:31,506), sprite falls back to Red surf (event_objects.h:11) — 1–3 days | cawtds/pokefirered (2025 thread): FRLG-exclusive features broken; author later merged FRLG upstream (1.15.0.md:100,149) |
| 2 Battle engine | C plus 759 hooks; no tests | Gen 3 vanilla; no tests | C, gimmick table, about 5k battle tests in CI | Same engine; `make check BUILD=firered` supported (1.15.1.md:37), not in CI | — |
| 3 Roster and QoL | Gen 1–8 (DPE), Megas, Z, Dynamax, DexNav, auto-run, HM-in-bag | Gen 1–3 | Gen 1–9 switches, regional forms, region-aware evolutions, DexNav, followers; no auto-run | Same as c1 | — |
| 4 8-way movement | Nothing | Direction constants only | Diagonal movement actions and sideways stairs | Same as c1 | — |
| 5 Save | Parasitic plus sectors 30/31 | Vanilla | SaveBlock3 1,624 B + `FREE_*` 3,790 B | Same; SaveBlock1 is fuller (FireRed fields) | — |
| 6 ROM | Fits (Unbound) | 16 MB default | Similar to c2 | 25.71/32 MiB with all gens; about 8.7 MiB free with Gen 8/9 off (I) | — |
| 7 Tooling | devkitARM/python, binary maps, no CI | agbcc/modern, Porymap | gcc 14, Porymap, debug menus, CI, docs, monthly releases | Same; Porymap needs FireRed settings (how_to_frlg.md:11-61) | — |
| 8 Native port | Emulator only | C; no known port | C; Emerald ports exist for pret | C; same as c1 (I) | Emerald SDL/Android ports, pret-based only |
| 9 Reuse | Unbound knowledge 1:1 | FireRed assets | Hoenn placeholders | FireRed placeholders and today's verified build | — |

---

## 3. Recommendation details

- **Fork:** start from the latest release tag (1.17.1, or 1.17.2 once it is tagged) into the project repo. Build on the WSL ext4 filesystem, not inside `external/`.
- **Make FireRed the default target:** follow `how_to_frlg.md:75-110` (Makefile defaults plus the mapjson default-region patch).
- **Config switches to flip first:**
  1. `species_enabled.h:16-17`: set `P_GEN_8_POKEMON` and `P_GEN_9_POKEMON` to `FALSE`. Consider `P_TERA_FORMS` and `P_GEN_9_MEGA_EVOLUTIONS` (`:27,29`). Decide `P_GIGANTAMAX_FORMS` together with the open Summon-visuals question.
  2. `dexnav.h:4,9-11`: set `DEXNAV_ENABLED TRUE` and assign its flag and variables.
  3. `save.h`: turn on every `FREE_*` for Mystery Gift, Union Room, Trainer Hill/Tower, record mixing and so on.
  4. `pokemon.h:57`: set `P_CAN_FORGET_HIDDEN_MOVE TRUE`.
  5. Optional: `overworld.h` `OW_FOLLOWERS_ENABLED`, and assign `OW_FLAG_NO_COLLISION` for debugging.
- **First code items:**
  - a "Set Pokémon can learn" unlock type in `src/field_move.c` and `include/field_move.h` (about 60–120 lines);
  - an auto-run toggle in `field_player_avatar.c` (about 40–80 lines);
  - a port of the underwater tileset into the FireRed target.

**Effort to finish the base setup** (AI-assisted, with the user play-testing):
- repo, FireRed default and config flips: about 1–2 days;
- test pipeline (`make check` for both targets, saved as scripts): about 1 day;
- new-region skeleton with a lake, a dive spot and an underwater map: about 2–3 days;
- **Total: about 1–1.5 weeks, confidence medium-high.**

**Comparable estimates for the other bases:**
- Emerald target: about 3–6 days.
- CFRU: about 1–2 weeks to a reproducible build. After that, each custom system costs about 1.5–2× as much (**I**).
- pokefirered: 3–6+ months to reach the expansion's level (**I**, low confidence).

**What would change these estimates:** FireRed-target regressions or the announced build-system rework (`how_to_frlg.md:73`), the Porymap version, and cross-generation evolution data breaking when Gen 8/9 is switched off.

## 4. Top risks and mitigations
1. **The FireRed target is less mature.** It was flagged "FRLG is playable, but missing some features" (`1.15.0.md:151`) and CI only builds it. *Mitigation:* pin a release tag, run both `make check` variants locally, and treat the Emerald target as the fallback (1–3 days to re-tile placeholder maps).
2. **Upstream churn conflicts with our battle edits.** For example, `battle_script_commands.c` alone is 12,417 lines. *Mitigation:* put our code in new files, use marked minimal hooks into upstream files, and merge only at minor releases.
3. **ROM space,** with cries at 9 MiB. *Mitigation:* the Gen 8/9 and form switches; budget Golden Sun music and tiles before the polish phase.
4. **Save space.** *Mitigation:* the `FREE_*` switches, keeping Set Pokémon in a reserved box, and fixed-width types in the new save structs.
5. **The native port is unproven for the expansion and needs arm64.** *Mitigation:* custom code goes only through the existing graphics and sprite APIs, with no pointer-size assumptions; play the ROM in an emulator on the Fold meanwhile.

## 5. What we lose versus the alternatives
- **vs CFRU:**
  - Unbound's exact mechanics and feel, and its finished auto-run and HM-in-bag behavior (to rebuild: small).
  - The Unbound engine knowledge carries over only as reference.
- **vs pokefirered:**
  - A smaller, simpler matching code base with faster builds.
  - A "pure FireRed" lineage.
- **vs the Emerald target:**
  - Full test coverage of the exact build we ship.
  - Ready-made underwater tiles, maps and sprites.
  - No FireRed Porymap quirks.

Sources:
- [pokeemerald-expansion releases](https://github.com/rh-hideout/pokeemerald-expansion/releases)
- [PokéCommunity: FireRed decomp expansion thread (cawtds/pokefirered)](https://www.pokecommunity.com/threads/is-there-an-expansion-project-for-the-pokefirered-decomp-project.533164/latest)
- [GBAtemp: multi-platform Emerald port](https://gbatemp.net/posts/10883415/)
- [PokéCommunity: Emerald PC port](https://www.pokecommunity.com/threads/pok%C3%A9mon-emerald-pc-port-the-project-you-missed.541024/)
- [NTx86/pokeemerald-sdl2pc](https://github.com/NTx86/pokeemerald-sdl2pc)
- [fuddlesworth/pokeemerald-native](https://github.com/fuddlesworth/pokeemerald-native)
- [ZallaxDev/pokeemerald-3Ds-dualscreen](https://github.com/ZallaxDev/pokeemerald-3Ds-dualscreen)
- [psspssr/pokeemerald-3Ds-dualscreen-thor](https://github.com/psspssr/pokeemerald-3Ds-dualscreen-thor)
- [Skeli789/Complete-Fire-Red-Upgrade](https://github.com/Skeli789/Complete-Fire-Red-Upgrade)
- [GitHub repo search results](https://api.github.com/search/repositories?q=pokeemerald+port+in:name,description&sort=stars&per_page=15)