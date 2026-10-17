# Mission 6, "Lantern Reef", as built (15 Oct 2026)

What the engine plays today for mission 6 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The cloud chat owns the story; this page is the hand-off so the lines can be rewritten in place.
Built on Opus 5.5 while Fable 5.1 was rate-limited; the Fable model reviews it when it is back.

## The flow

1. **Vesper, for hire.** After mission 4, a fog pilot waits on Canalport's beach. She'll take the crew into Lantern
   Reef for fifty coins (or whatever the purse holds), **joins** with Gastly, and the reef goes on the Kestrel's
   chart. ("Vesper pilots you in", the story's gate.)
2. **Lantern Reef** (`lantern_reef`, placeholder tiles from Golden Sun 1's Tolbi-bound ship, its hull broken in
   three by painted sea). Fog hangs over everything.
3. **Reveal planks.** The planks between the wreck's pieces are there but unseen. Reveal finds each one, and once
   found it stays (a plank seen is a plank known).
4. **The Halt boom.** A loose boom swings across the mid deck. Halt stops it for about ten seconds.
5. **Corvin's note** at the stern: "Ask your Commodore where the tithe goes." Reading it unlocks **Defog**.
6. **Defog** clears the reef's fog for good, if a Set Pokémon in the crew can learn it (Torchic and Rowlet can).
7. **Easter eggs** (§9a): Mimikyu, seen only with Reveal at the bow; Maestro Bonewhistle, conductor of the
   drowned orchestra; a Litwick in an old lantern. Wild battles: Golden Sun's ghosts and skeletons, and Gastly,
   Shuppet and Litwick.

Checked end to end by the engine's `tools/mission6_check`.

## Where the words live

| What | File | Where |
|---|---|---|
| Vesper's price and joining | `maps_src/canalport/events.json` | scene `vesper_pilot` |
| Arrival, Vesper's advice | `maps_src/lantern_reef/events.json` | scene `reef_arrival` |
| Corvin's note and Defog | `maps_src/lantern_reef/events.json` | slot 11: `text`, `scene_after`, `text_after` |
| The boom, the eggs | `maps_src/lantern_reef/events.json` | slots 10, 12–14 |

## Placeholders and open points

- **"Night-only decks"** (story §7) aren't built: there is no day and night yet. The wreck is always walkable.
  The clock is decided (17 Oct); [day-night-clock.md](day-night-clock.md) §2 proposes how the decks use it.
- **Defog banks** are one room-wide fog. Defog is optional here because only some Pokémon learn it; the story's
  rule that "mandatory puzzles use only Crew 1's Psynergy" holds (Reveal and Halt are Vesper's).
- **The graveyard** is one wreck; more hulks around it can come with the graphics pass.
- **Mimikyu** wears a placeholder sprite and can't be caught yet; the story calls it a "find".
- **Vesper** wears Jenna's field sprite and Jenna's battle curve until the graphics pass.
