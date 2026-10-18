# Mission 5, "The Eldergrove", as built (15 Oct 2026)

What the engine plays today for mission 5 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The engine side writes each mission's final script for your yes (demo decision 1); this page is
the hand-off so the lines can be rewritten in place.
Built on Opus 5.5 while Fable 5.1 was rate-limited; the Fable model reviews it when it is back.

## The flow

1. **The Kestrel's chart.** After mission 4, a deckhand by the ship (Stonehollow's cove, Canalport's jetty, and
   now the Eldergrove) lists the places the story has opened: Marrow Isle, Canalport, the Greenwild. Picking one
   sails there. This is a placeholder hub for Act I until the sea map of the Calm exists (proposed).
2. **The Eldergrove village** (`eldergrove`, placeholder tiles from Golden Sun 1's Kolima). The great tree has been
   sick since spring; the villagers blame Sorrel, the one person who goes near it. The elder says so too.
3. **Sorrel joins** (with Rowlet) at the east path: prickly, honest, and the only guide into the Greenwild.
4. **The Greenwild** (`greenwild`, Kolima Forest's river). The river splits the forest; the old log bridge is
   rotten through until **Growth** binds it with a vine. A **poison swamp** on the way to the heart costs HP for
   every step (never below 1). Wild battles: Drone Bees, Spiders, Trolls and forest Kin (Seedot, Combee,
   Shroomish).
5. **The heart of the Eldergrove** (`eldergrove_heart`, Tret's clearing). At the vine-covered hollow, **Celebi**
   shows hooded founders laying seals over six Wells "so the centre may endure", then the vision breaks. A
   Tidewarden runner brings **Ilse's order**: drive the Forest seal deeper. Sorrel objects, and they do it.
   **Cut** unlocks.
6. **Back in the forest**, Cut clears a bush hiding a chest (two Nuts), if a Set Pokémon in the crew can learn Cut
   (Treecko and Torchic can; Mudkip, Eevee, Rowlet and Marill can't).

Checked end to end by the engine's `tools/mission5_check`.

## Where the words live

| What | File | Where |
|---|---|---|
| Arrival | `maps_src/eldergrove/events.json` | scene `greenwild_arrival` |
| Elder, villagers, inn | `maps_src/eldergrove/events.json` | slots 8–11 |
| Sorrel joining | `maps_src/eldergrove/events.json` | scene `sorrel_joins`; Sorrel (slot 12) `text_after` |
| The closed path east | `maps_src/eldergrove/events.json` | the warp's `else_text` |
| The rotten bridge, the sprout, the bush | `maps_src/greenwild/events.json` | scene `rotten_bridge`; slots 8–10 |
| The swamp's sting | `maps_src/greenwild/events.json` | `hazards` |
| Celebi's vision, Ilse's order, the seal | `maps_src/eldergrove_heart/events.json` | scene `celebi_vision` |
| The deckhand's line before the ship is yours | every room with a "Kestrel's mate" | `text` |

## Placeholders and open points

- **The Hive is not built.** The story's "The Hive" (§9a) is solved with Cloak and Reveal, which are Vesper's
  (mission 6). Missions 5 and 6 can be played in either order, so the Hive can't be required in mission 5. It can
  become an optional area of the Greenwild to return to after mission 6. **Decided (demo 9, 18 Oct):** an optional
  Greenwild area that opens once Vesper is in the crew, with Cloak built for it and a reward chest at the queen.
- **Ilse's runner** is narration, not a character on screen.
- **Celebi** has no sprite in the scene; the vision is told in words over a fade.
- **The swamp** is drawn as a purple tint until the graphics pass gives it tiles.
- **The chart** is a placeholder for sailing the Calm on a real sea map (story §14 question 1).
- **Sorrel** wears Jenna's field sprite and Ivan's battle curve until the graphics pass.
