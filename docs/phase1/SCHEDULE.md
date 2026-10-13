# Schedule

Estimates assume Claude Code does the coding and you play-test. They come from the phase-1 reports, widened where the
[review](REVIEW.md) said so. Two tracks run side by side:

- **Engine track:** the game itself, on pokeemerald-expansion. Runs anywhere, including cloud sessions.
- **Decompiling track:** Golden Sun and Unbound reverse-engineering with gbax. Runs **only on your PC**, because the
  ROMs never leave it.

## This week (Tue 13 – Mon 19 October 2026)

| Day | Engine track | Decompiling track (PC) | Needs you |
|---|---|---|---|
| Tue 13 | Finish the test gate: the FireRed run passed on 12 Oct (1 failure, the save-layout check); compare with the Emerald run. Create the engine fork once you OK it; FireRed as the default target; config: all `FREE_*` on, Gen 8/9 off (plus regional-form, Gigantamax, Tera decisions), DexNav on without search levels, `P_CAN_FORGET_HIDDEN_MOVE` | Golden Sun text decoding (needed to label every other table) | Answer the 6 decisions in [README.md](README.md#decisions-needed-from-you) |
| Wed 14 | Save budget written down. **Data-model spike**: Adept as a species, Set Pokémon in a reserved PC box, where Adepts 7–8 live, which party array holds what; plan for healing, items and catching | Golden Sun mechanics tables: Psynergy (power, cost, element), classes (stat multipliers, Psynergy by level), Djinn/Summons, enemies | Install Lemuroid on the Fold 7 and try the test ROM with touch, Backbone and Xbox (10–15 min) |
| Thu 15 | Battle stage 1: `BATTLE_TYPE_ADEPT`, a separate switch pool per player battler, `ADEPT_BATTLE_TEST` | Mechanics tables (continued) | — |
| Fri 16 | Battle stage 1: exp to both battlers, write-back after battle; 5–8 tests passing | Golden Sun movement measurement: walk, run and diagonal speed, acceleration, corner nudge (`gbax trace`) | ~10 min walking around in Golden Sun while the trace runs |
| Sat 17 | Movement A: fix the 3 latent diagonal bugs; 8-direction input with a grace window | (Optional) Golden Sun battle sprite trace | Optional: play into a Golden Sun battle with the trace on |
| Sun 18 | Movement A: diagonal movement tables and collision decomposition; first diagonal walking on a test map | Unbound Ghidra analysis results (reference only) | — |
| Mon 19 | Movement A: wall slide, running and auto-run; Dive placeholder map (one dive spot + one underwater map) | — | Play-test diagonal walking and the Dive map on the Fold 7 |

End of week target: a FireRed-target build where you walk diagonally, dive, and fight a 1 Adept + 1 Pokémon battle
against a trainer's pair. Everything else uses placeholder art.

**Week-1 gate (by Mon 19):** keep the FireRed target unless the FireRed-only test failures or the Dive smoke test say
otherwise. After this, maps lock the target.

## Phases after this week

| Phase | Work | Estimate |
|---|---|---|
| **1. Foundation** (finishes ~early November) | Movement A completion (followers, Surf, edge cases); party / Set-storage layer outside battle | 2–4 weeks |
| **2. Core systems** (~Nov–Feb) | Battle stages 2–7: Psynergy and the shared PP pool; enemy Adepts and Adept switching; 18-type classes; Summons with the party-wide Standby pool; wild battles; battle UI | 6–10 weeks |
| | Field Psynergy, starting with Move, Frost, Growth and Reveal (DESIGN.md's proving set); item Psynergy; shared Retreat/Avoid effects | **not sized yet** (next sizing job) |
| | Djinn-style encounters on top of the expansion's overworld-encounter behaviours (flee, chase, approach) | not sized yet |
| | Water: Set-Pokémon field-move rule (2–4 days), limited Surf (1.5–3 days) | ~1 week |
| | Ship, world-map chunks, Lodestar-style navigation, sky and undersea layers (if the world proposal is accepted) | 6–9 weeks |
| | ROM-side controls: shortcut chords, L/R Psynergy shortcuts, auto-run, quick wheel | 5–8 days |
| | Player app for the Fold 7 (LibretroDroid + mGBA core, posture-aware layouts, controllers) | 3–5 weeks, any time; independent of the ROM work |
| **3. Content** | Weyard-form data (~57 species + 14 Megas/Primal); an Act I vertical slice (~40–60 placeholder maps, ship launch) | 4–8 weeks for the slice; full world 6–12+ months part-time |
| **4. Polish** | Golden Sun tilesets, sprites, spell and Summon animations, menus, music; Weyard-form art | after content |

## Decompiling track, by priority

1. **Now (feeds phase 2):** Golden Sun text, Psynergy, class, Djinn/Summon and enemy tables; Golden Sun movement speeds.
2. **Later (feeds phase 4):** Golden Sun battle sprites (live trace), map tilesets and tilemaps with palettes, music
   (MP2K to MIDI + SoundFont), menu graphics.
3. **Reference:** Unbound's own code (Ghidra), for behaviour Unbound does differently from CFRU.

## Running work while you're away

Engine work can run as cloud sessions on the engine fork. Decompiling work can't, because the ROMs stay on your PC;
it needs the desktop app open. Scheduled sessions can be set up for either track once you've answered the
decisions above, so they build on settled design.
