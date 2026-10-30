# Mission 3, "Highwater", as built (15 Oct 2026)

What the engine plays today for mission 3 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The engine side writes each mission's final script for your yes (demo decision 1); this page is
the hand-off so the lines can be rewritten in place.
Built on Opus 5.5 while Fable 5.1 was rate-limited; the Fable model reviews it when it is back.

## The flow

1. **Stonehollow, after mission 2.** Commodore Ilse has news: Canalport is flooding and the old sluice house has
   gone quiet. **Maren joins** (with her Eevee), and the Kestrel carries them south across the Calm.
2. **Canalport** (`canalport`, placeholder tiles from Golden Sun 2's Alhafra beach). The Kestrel ties up at the
   stone jetty. The sea is pouring across the beach through two breaches beside the tide pools.
3. **Frost.** Maren's Frost turns each breach's pool into an ice pillar. Once both are frozen the flood drains:
   the water band becomes sand and the town beyond can be reached.
4. **The harbourmaster** at the Tidewarden post thanks the crew and gives the hero **a Pokémon that can Surf**
   (Marill, a placeholder), which unlocks **Surf**. Your decision (15 Oct): crew 1's Surf comes from a gift in
   Canalport, because Treecko, Torchic and Eevee can't learn it.
5. **Surf.** Facing the sea from the beach, A steps onto the water. The sluice house on the cliff to the west is
   reached only by water.
6. **The sluice beast** (a story fight; a loss restarts it). Afterwards the sluice gates open, the lower town
   drains, and **the Kestrel is the crew's: the Calm is open** (the ship flag the world map uses).

Checked end to end by the engine's `tools/mission3_check` (every page turned by pressing confirm).

## Where the words live

All lines are placeholders written to the story's beats, in the engine's `maps_src/*/events.json`:

| What | File | Where |
|---|---|---|
| Ilse's news, Maren joining, the voyage | `maps_src/stonehollow/events.json` | scene `to_canalport`; Ilse (slot 16) `text_after` |
| Arriving, Maren on the breaches | `maps_src/canalport/events.json` | scene `harbour` |
| The tide pools | `maps_src/canalport/events.json` | slots 8–9 |
| The harbourmaster and the gift | `maps_src/canalport/events.json` | slot 10: `text`, `scene_after`, `text_after` |
| Townsfolk, the inn | `maps_src/canalport/events.json` | slots 11, 12, 14 |
| The sluice beast and the ending | `maps_src/canalport/events.json` | slot 13: `text`, `scene_after` |

## Built for this mission (engine)

- **Field Psynergy belongs to the active crew** (the decided rule in party-and-battle.md §7, now enforced): Frost
  needs a Mercury Adept, Reveal a Shadow one, Growth a Forest one. The hero alone has Move.
- **Surf** in our rooms: a water layer, entered facing the water with A when Surf is unlocked and a Set Pokémon
  in the crew can learn it.
- **Story bosses** from Golden Sun enemies scaled to the story's level. The sluice beast is Kraken's sheet at
  level 8 (proposed). Measured over 30 seeds with the hero at 7 and Maren (19 Oct, after the battle and items rules): attacking only
  wins 7 times; healing with Maren and using Psynergy wins all 30.
- **Recruits bring their story partner** from the cast table (Maren: Eevee).
- **Map changes by flag**: a room can open cells and repaint its tiles once flags are set (the drained flood).
  This is the mechanism story §14 question 5 asked for (map variants by flag), at the scale of a room.

## Placeholders and proposals (not decided)

- **Saltmarsh Reach** (the story's route into Canalport) isn't built; the Kestrel docks in Canalport directly.
- **Canalport is one beach room.** The lower town is shut ("still under water") until the sluice opens, and then
  leads to the world map placeholder. The canals themselves are not drawn yet.
- **Marill** is the canal Kin the Tidewardens give, a canal Water type that learns Surf, kept by demo
  decision 15 (18 Oct).
- **The beast** wears a Sol Sanctum statue's field sprite and Kraken's battle sheet.
- **Balance:** the beast expects the player to heal and use Psynergy; plain attacking loses. With the retry rule
  that teaches rather than locks, but it is worth a look in the balance pass.
