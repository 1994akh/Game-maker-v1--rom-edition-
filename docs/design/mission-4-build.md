# Mission 4, "The Forgeheart", as built (15 Oct 2026)

What the engine plays today for mission 4 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The engine side writes each mission's final script for your yes (demo decision 1); this page is
the hand-off so the lines can be rewritten in place.
Built on Opus 5.5 while Fable 5.1 was rate-limited; the Fable model reviews it when it is back.

## The flow

1. **The handover.** After the sluice beast in Canalport, the screen fades: a Rimborn skiff carries Corvin to
   Embral Isle. The game switches to **Corvin's crew** (Corvin and Larvitar).
2. **The Forgeheart hall** (`forge_hall`, placeholder tiles from Golden Sun 1's Fuchin Temple). Arrival is a
   restoration point for Corvin's crew. The abbot sets the **Earth trial**: Move the training stone onto the mat.
3. **Tamsin** steps in once the trial is passed: a story fight (Tamsin and Riolu; a loss restarts it). Beaten, she
   says the sacred flame shrinks while the tithe grows, and **joins** with Riolu.
4. **The sanctum** (`forge_sanctum`, the brazier chamber), down the shaft that only opens with Tamsin. Corvin
   pulls the **Flame seal**; every brazier roars and **Ho-Oh** answers and judges the crew (a story fight against
   a Pokémon; a loss restarts it). Calmed, it bursts through the roof and its fire falls on the monastery.
5. **The Flame Well runs free.** Mars's top Summon (Meteor, Golden Sun's own name, kept by demo decision 17) is
   unlocked.
   **Changing (your answer, progression 20, 18 Oct):** at mission 4 Ho-Oh judges and flies off and the crew gains
   nothing legendary; the top Flame Summon unlocks with the caldera catch after the Breaking. Not built yet.
   Corvin's crew escapes past Ilse's fleet through the Galeway, and **the game returns to the hero's crew in
   Canalport**, where it stood.

Checked end to end by the engine's `tools/mission4_check`.

## Where the words live

| What | File | Where |
|---|---|---|
| The handover narration | `maps_src/canalport/events.json` | the sluice beast (slot 13), end of `scene_after` |
| Arrival | `maps_src/forge_hall/events.json` | scene `forge_arrival` |
| The abbot, before and after the trial | `maps_src/forge_hall/events.json` | slots 8 and 9 |
| The training stone | `maps_src/forge_hall/events.json` | slot 10 |
| Tamsin's challenge and joining | `maps_src/forge_hall/events.json` | slot 11: `text`, `scene_after` |
| The shaft's refusal | `maps_src/forge_hall/events.json` | the warp's `else_text` |
| The seal, Ho-Oh, the fire, the escape | `maps_src/forge_sanctum/events.json` | scene `flame_seal` |

## Built for this mission (engine)

- **Legendary judges as story fights**: a Pokémon on an Adept curve with the story's numbers (here 420 HP and two
  actions a round, proposed).
- **Top Summons wait for their legendary**: the story says calming a legendary unlocks its group's top Summon
  (§5). Each group's highest tier is locked until then; the lower tiers are always there.
- **Back to the other crew where it stood** after a handover (a scene step).

## Balance (proposed)

Measured with the engine's `tools/balance_fight.tscn` over 30 seeds:

| Fight | Crew | Attacking only | Healing and Psynergy |
|---|---|---|---|
| Tamsin (4) + Riolu (4) | Corvin 6 + Larvitar | 12 / 30 | 30 / 30 |
| Ho-Oh (420 HP, 2 actions) | Corvin 7 + Larvitar, Tamsin 7 + Riolu | 0 / 30 | 29 / 30 |

## Placeholders and proposals (not decided)

- **The monastery trials** are one Move puzzle. Tamsin's crew Psynergy (Flame) has no field use here yet.
- **Ho-Oh** has no field or battle sprite of its own beyond the Pokémon picture; the seal is a Golden Sun object.
- **The fire and the escape** are a shake, a fade and narration. The Galeway lanes chase isn't built.
- **Tamsin** wears Mia's field sprite and Garet's battle curve placeholder (her class is Guard, on Garet's row).
- **Catching Ho-Oh** is a later beat, as the story says (§5).
