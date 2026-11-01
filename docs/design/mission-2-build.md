# Mission 2, "The Drowned Boy", as built (15 Oct 2026)

What the engine plays today for mission 2 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The engine side writes each mission's final script for your yes (demo decision 1); this page is
the hand-off so the lines can be rewritten in place.
Built on Opus 5.5 while Fable 5.1 was rate-limited; the Fable model reviews it when it is back.
Fallhaven's rooms are as built on 31 Oct (engine PR #98): mission 2's `fallhaven` is merged into the lower town,
`fallhaven_lower`, which also holds mission 9, and the harbour, the cliff road, the high town and the west cove are
new. The rest of the page is the 15 Oct build.

## The flow

1. **The handover.** Mission 1 ends with Commodore Ilse handing over the Lodestar. Her last page fades to black:
   "That same night, far from Marrow Isle, the underground river gave up what it took." The game switches to
   **Corvin's crew** (crew 2: Corvin with Larvitar, his own bag and an empty purse) and moves to the sea caves.
2. **The Marrow sea caves** (`sea_caves`, placeholder Fuchin Falls Cave tiles). Corvin washes in; the spot becomes
   his crew's restoration point. A fallen stone blocks the passage north; Move slides it twice and the way opens
   to the river mouth, where a Rimborn skiff waits. A chest holds two Herbs.
3. **Fallhaven**, the cliff town on the east rim. The skiff lands at the harbour's jetty (`fallhaven_harbour`,
   placeholder Tolbi Docks tiles), and the arrival (`skiff_in`) plays there; where the homecoming (the script's
   scene 4) plays is for your answer (open 145). Corvin climbs the harbour stair into the lower town
   (`fallhaven_lower`, placeholder Bilibin tiles, in its mission 2 state, at dusk).
   - **Sael** recognises Corvin as the boy she pulled from the wreck. The ground shakes and Tanner's street falls
     into the Rimfalls (Tanner is gone from the town afterwards). Sael asks Corvin to clear the west alley.
   - A **toppled cart** blocks the alley the townsfolk need to reach the cliff road. Move clears it, and **Hask**
     arrives. The alley's top then leads up the cliff road (`fallhaven_cliff`) to the high town (`fallhaven_high`)
     and the west cove (`fallhaven_cove`), which hold only ground so far.
   - **Hask** offers to tear out every seal at once. Corvin refuses: one seal, done right, the Flame Well first.
     Hask leaves, the screen fades, and the game returns to **the hero's crew in Stonehollow**, with the hero's own
     bag and coins as they were.
4. An inn in Fallhaven lets Corvin's crew rest: the innkeeper (slot 25) stands on the lower town's plaza until the
   Leaning Gull has a room of its own.

Checked end to end by the engine's `tools/mission2_check` (every page turned by pressing confirm).

## Where the words live

All lines are placeholders written to the story's beats, in the engine's `maps_src/*/events.json`:

| What | File | Where |
|---|---|---|
| The handover narration | `maps_src/stonehollow/events.json` | Ilse (slot 14), `scene_after` |
| Washing in | `maps_src/sea_caves/events.json` | scene `washed_in` |
| The stone, the chest | `maps_src/sea_caves/events.json` | slots 9–10 |
| Arriving by skiff | `maps_src/fallhaven_harbour/events.json` | scene `skiff_in` |
| Sael and the falling street | `maps_src/fallhaven_lower/events.json` | scene `sael_street`; Sael (slot 20) `text_after` |
| The cart, Tanner, townsfolk | `maps_src/fallhaven_lower/events.json` | slots 22–24 |
| Hask's offer and the return | `maps_src/fallhaven_lower/events.json` | scene `hask_offer` |

## Built for this mission (engine)

- **Two crews** (engine PR #36): the active crew's party, bag, coins, location and last restoration point; the
  other crew waits. Bags and coins stay separate until the story merges them (flag `bags_merged`, mission 10, as
  you decided in §14 question 4); the Kin Garden is shared. A crew's first state (proposed): its lead from the
  roster at the hero's level, the partner from its first trainer row, three Herbs, no coins.
- Scene steps `crew` (switch) and `rest_point` (where a handover starts, as party-and-battle.md §1 proposes).
- People can arrive or leave mid-visit when a flag changes (Hask appears once the alley is clear).

## Placeholders and proposals (not decided)

- **No battles in mission 2 yet.** The story names Earth puzzles in the river caves; the caves have one Move
  puzzle and no random encounters. Adding a Corvin-level encounter table is an easy follow-up once the balance
  pass sets crew-2 levels.
- **Corvin's level** follows the hero's at the handover (proposed). His Larvitar is a level lower.
- **Hask and Sael** wear villager sprites; Corvin walks as Isaac's field sprite until the graphics pass.
- **Fallhaven's collapse** is one street and a shake. The story's "Corvin clears escape paths as a cliff gives
  way" is the cart puzzle for now.
- The skiff journey and Corvin sailing for the Flame Well are narration, not scenes.
