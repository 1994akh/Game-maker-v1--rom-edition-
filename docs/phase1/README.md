# Phase 1: foundation — summary

Phase 1 in [DESIGN.md](../../DESIGN.md) asks for three things: choose the code base (with field Dive and the custom
battle format in mind), size 8-way movement against the grid-diagonal fallback, and do it without cosmetics. This
folder holds the investigation (2026-10-12): six research reports, an adversarial review that re-checked 19 of their
claims in the source, and a schedule.

| Document | What it covers |
|---|---|
| [CODEBASE.md](CODEBASE.md) | CFRU vs pokefirered vs pokeemerald-expansion (Emerald and FireRed targets), against every DESIGN.md requirement |
| [MOVEMENT.md](MOVEMENT.md) | Grid-diagonal walking (A) vs free 8-way movement (B): every grid assumption in the engine, work items, estimates |
| [BATTLE_FORMAT.md](BATTLE_FORMAT.md) | 1 Adept + 1 Pokémon per side on the expansion's battle engine, in 8 stages, with a test plan |
| [WATER_MOVES.md](WATER_MOVES.md) | Dive with underwater maps, Waterfall, limited Surf, the "any Set Pokémon can learn it" rule, the ship |
| [CONTROLS.md](CONTROLS.md) | Touch layouts for the Fold 7 (cover, inner, tabletop) and ordinary phones; Backbone and Xbox controllers |
| [WORLD_PROPOSAL.md](WORLD_PROPOSAL.md) | A world and story **proposal** inspired by One Piece, Golden Sun and Pokémon (for the design project to decide) |
| [REVIEW.md](REVIEW.md) | Red-team review: tries to refute the recommendation, re-checks 19 claims, ranks the remaining risks |
| [SCHEDULE.md](SCHEDULE.md) | The plan for this week and the phases after it, plus the decompiling track |

## Recommendation

**Code base: pokeemerald-expansion, pinned to a release tag and forked, building its FireRed target (`make firered`).**
The Emerald target is the fallback, decided by the end of week 1 after a test gate.

- It's the only candidate that has, in plain C: engine-level **field Dive with underwater maps**; a battle engine with
  four separate 6-slot parties, so each of the player's two battlers can switch from **its own pool** (the core of
  1 Adept + 1 Pokémon); a table-driven **gimmick framework** to build Summons on (Z-Moves and Dynamax are already
  there); Gen 1–9 switches, Megas, regional forms, DexNav, follower and overworld Pokémon; and about 6,000 automated
  tests that run headless.
- **Verified today:** `make firered` builds in WSL in under 5 minutes (32 MB ROM, 6.3 MB free with every generation
  on). The FireRed ROM links all the Dive code, and only Kanto maps.
- **Why not CFRU:** its party model caps the Adept side at 3, it has no tests, maps are edited in binary tools, and it
  can never be ported natively. Unbound's feel only matters if we kept Unbound's content, and we don't.
- **Why not pret pokefirered:** Gen 1–3 only, half-dead Dive, no gimmicks. Bringing it up to standard would recreate
  the expansion's FireRed target, which is literally how that target came about.
- **Native Android later:** the expansion is almost all C, and native SDL/Android ports already exist for its parent
  (pret pokeemerald). A port still needs 64-bit cleanup; that's long-term work, not a reason to pick another base.

**Movement: build A (8-direction walking on the tile grid) now; keep B (free movement) as a later, optional mode.**

| | A: grid diagonal | B: free 8-way (player only; NPCs, triggers and maps stay on the grid) |
|---|---|---|
| Already in the engine | 8-direction enum, 12 diagonal movement actions, diagonal animation entries, the cardinal-facing rule, diagonal stairs | The camera follows sprite pixels; the rest is new |
| Size | ~900–1,500 lines, 9–11 files | ~2,100–3,700 lines, 12–15 files |
| Calendar | **2–4 weeks** (first diagonal steps in 3–5 days) | **6–10 weeks** (5–9 after A) |
| Confidence | ~70% | ~40–50% |
| Fidelity | Golden Sun-like with a D-pad, but steppy | Close to Golden Sun |

A comes first because it's playable within a week, every map authored for A stays valid for B, and B's estimate is
low-confidence. Three latent engine bugs fire as soon as a diagonal reaches collision code; they're fixed first.
Before tuning, a 1–2 day `gbax trace` measurement of Golden Sun's walk, run and diagonal speeds sets the targets.

**Dive and the battle format fit the recommendation:**
- **Dive:** zero required code in the FireRed build. One dive spot plus one underwater map is 1–2 days of content
  (mostly a placeholder underwater tileset). The "any Set Pokémon can learn it" rule is ~180–260 lines once Set
  storage exists; limited Surf is ~80–150 lines; a minimal ship is 4–8 days.
- **Battle:** ~2,000–3,500 lines over 8 stages, **7–11 weeks**. The smallest playable slice (1 Adept + 1 Pokémon vs a
  trainer's pair, player controls both) is **4–7 days**, testable from day one with a new `ADEPT_BATTLE_TEST`.

## What the review changed

- **New top risk: the party and Set-storage layer outside battle.** The player's party is referenced 802 times in 76
  source files (healing, items, catching, followers, evolution, …). Where the 8 Adepts and 24 Set Pokémon live has to
  be designed before battle or field-move code: **2–4 weeks**, starting with a data-model spike in week 1.
- **Save space is tight.** The FireRed build has ~116 bytes free in SaveBlock1, so all `FREE_*` switches are mandatory,
  the Set Pokémon go in a reserved PC box, and DexNav search levels stay off.
- **Test gate on day 1.** CI never runs the tests on the FireRed target, so we run both `make check` variants and
  compare before any map exists. The target can't be switched cheaply once maps exist.
  - **FireRed result (12 Oct, `make check BUILD=firered`, 7.5 min):**
    - 5,416 passed, 1 failed, plus 18 known-failing, 421 to-do and 9 expected-failing (5,865 total).
    - The one failure is `test/save.c:12` "SaveBlock1 is backwards compatible", which expected 15,568 bytes and found 15,756. It's the FireRed save layout being bigger than the test assumes, the same save pressure noted above. No battle or field test fails.
    - **The FireRed target passes the gate** on the battle side. The Emerald run is still to compare (it was running when this was written).
- Estimates widened: base setup 1.5–2 weeks; movement A 2–4 weeks.

## Decisions (answered 13 Oct 2026)

These replace the recommendation above where they differ. The research reports stay as written, for reference.

| # | Question | Answer | What it changes |
|---|---|---|---|
| 1 | Platform order | **Native Android app first** (Fold 7), not the ROM edition | GBA limits (32 MB ROM, SaveBlock1's ~116 B free, `FREE_*` switches) no longer drive the design. The Lemuroid/player-app plan and the ROM-side controls work are dropped for now. |
| 2 | Code base | **On hold until the Golden Sun extraction is done** | No pokeemerald-expansion fork, config or test-gate work yet. The expansion stays a candidate (as the battle/rules reference or as C code to port), next to engines built for native Android. |
| 3 | Movement | **Go straight to B** (free 8-way movement) | Movement A is not built first. On a native engine free movement is the natural default, so B's GBA-specific risks (the 40–50% confidence) mostly don't carry over. The Golden Sun speed measurement becomes more important. |
| 4 | Adepts in battle | **All 8 can swap in** | The Adept pool is 8, not 6. |
| 5 | Partner on an Adept change | **The partner swaps too**: the new Adept brings its own Set Pokémon in at once | Each Set Pokémon is tied to its Adept in battle; an Adept change replaces both battlers on that side. |
| 6 | Engine repo | **A new private repo** under your GitHub; this repo keeps the design docs | Created once the code base is chosen, after you confirm its name. |

Next, in order:
1. **Golden Sun extraction (your PC):** text, Psynergy, class, Djinn/Summon and enemy tables, movement speeds, then
   battle sprites, maps and music. This gates decision 2.
2. **Native engine options (can run in the cloud):** a report comparing ways to build the Android app (for example a
   general engine such as Godot, or C/C++ with SDL reusing pokeemerald-expansion's battle code), against DESIGN.md
   and the answers above. Proposal only; you decide.

Needed for phase 2 (from the reports; not blocking yet): Standby recovery rules, Psynergy limited to 4 in battle,
the enemy Standby pool, the default L/R Psynergy shortcuts, the wheel size, face-button layout, and the world
proposal's 14 questions.
