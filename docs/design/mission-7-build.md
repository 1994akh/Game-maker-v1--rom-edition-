# Mission 7, "Bastion Rock", as built (15 Oct 2026)

What the engine plays today for mission 7 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The cloud chat owns the story; this page is the hand-off so the lines can be rewritten in place.
Built on Opus 5.5 while Fable 5.1 was rate-limited; the Fable model reviews it when it is back.

## The flow

1. **The hook.** Mission 7 "plays after Crew 1's first recruitment". Whichever of missions 5 (Sorrel) and 6
   (Vesper) finishes first ends with the handover: "Meanwhile, in the west Calm, Corvin's crew watches the walls of
   Bastion Rock." The game switches to **Corvin's crew** (Corvin and Tamsin).
2. **The shore** (`bastion_shore`, placeholder tiles from Golden Sun 1's Kalay Docks). The skiff ties up at the
   pier (a restoration point). The walls are too high, but the earth by the sea-gate is soft: **Scoop** (Earth
   Psynergy, Golden Sun 2's) digs a tunnel under the walls.
3. **The jail** (`bastion_jail`, Golden Sun 2's Madra jail). The tunnel comes up in the guard corridor.
   - **A guard** walks the row and sees along his heading, four cells, unless a wall is in the way. Seen, the
     crew is chased back to the tunnel. Halt (when someone has it) freezes and blinds him.
   - **The key ring** hangs at the far end; it opens **Nerissa's** cell.
   - **Nerissa joins** with Froakie, and points the crew to the fortress **ledgers**: fire, rain, harvests,
     shipped "to the Crown".
4. **The escape.** Back through the tunnel to the pier, and **Surf** out into the open Calm (Froakie can Surf),
   which plays the escape and returns the game to **the hero's crew**, where they stood.

Checked end to end by the engine's `tools/mission7_check`, starting from Corvin's note in mission 6.

## Where the words live

| What | File | Where |
|---|---|---|
| The handover narration | `maps_src/eldergrove_heart/events.json` and `maps_src/lantern_reef/events.json` | the last `when` step of each ending |
| Arrival at the shore | `maps_src/bastion_shore/events.json` | scene `bastion_arrival` |
| The escape | `maps_src/bastion_shore/events.json` | the sea warp's `scene` |
| Corvin on the guard | `maps_src/bastion_jail/events.json` | scene `jail_arrival` |
| Caught | `maps_src/bastion_jail/events.json` | `caught` |
| The cell door, Nerissa, the ledger | `maps_src/bastion_jail/events.json` | scenes `cell_door`, `nerissa_joins`; slot 12 |

## Placeholders and open points

- **"Surf out through the sea caves"** is a Surf from the pier to the open sea, then narration; the sea caves
  aren't a room.
- **The fortress** is a docks cottage standing in for the sea-gate, and Madra's jail for the cells.
- **The guards' sight** is a straight line along their heading. Golden Sun-style vision cones and Vesper's Cloak
  (crew 1's) can come later.
- **Nerissa** wears Mia's field sprite and battle curve until the graphics pass.
- **Mission 8** (the Tradewind Bazaar, after crew 1's second recruitment) is next.
