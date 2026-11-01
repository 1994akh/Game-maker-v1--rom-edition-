# Mission 9, "The Fall of Fallhaven", as built (15 Oct 2026)

What the engine plays today for mission 9 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The engine side writes each mission's final script for your yes (demo decision 1); this page is
the hand-off so the lines can be rewritten in place.
Built on Opus 5.5 while Fable 5.1 was rate-limited; the Fable model reviews it when it is back.
Fallhaven's rooms, the handover's night and the finale's dawn are as built on 31 Oct (engine PR #98), and the finale
has landed at `marrow_cove` since 25 Oct: the lower town also holds mission 2, and the harbour, the cliff road, the
high town and the west cove are new. The rest of the page is the 15 Oct build.

## The flow

1. **The hook.** Mission 8's escape ends with word from a Rimborn skiff: Fallhaven is falling. Corvin's crew takes
   the cliff to the archive. The hero's crew lands in the west cove (`fallhaven_cove`) at night and walks the high
   town (`fallhaven_high`) and the cliff road (`fallhaven_cliff`) down to the lower town's west alley. The script
   starts at the high town gate instead; you kept the west cove, as built (open 156).
2. **The lower town** (`fallhaven_lower`, crew 1, the whole of Golden Sun 1's Bilibin as placeholder, in its
   mission 9 state). Three households are trapped:
   - a family behind a **fallen chimney**: Move pushes it into a niche;
   - a child on a **terrace** whose steps fell: Growth on a sprout makes a vine up;
   - an **old man** who can't take the cliff path: he needs the archive's lift.
   - **Reveal** finds the archive's cellar hatch under the ash. Opening it lifts the bar on the vault door above.
3. **The archive** (`fallhaven_archive`, crew 2, McCoy's Palace as placeholder). **Sael** bars the great doors.
   - **Mind Read** on the archivist: the Ledger is in the east vault, barred from the cellar side.
   - **Whirlwind** on the lift's wind-wheel drops the lift basket to the lower town.
   - Once crew 1 has opened the hatch, the vault opens and the **Ledger of the Crown** is found.
4. **Relay stones**, one in each room, switch between the crews. Each is also a restoration point.
5. **The finale.** With everyone out and the Ledger found, the lower town's north stair climbs to the archive.
   Both crews read the Ledger: the seals drain the Wells into the Crown. The cliff goes; Sael holds the doors and
   doesn't come out. On the boats, Maren confesses she has been reporting to Vey. Ilse defies the order to turn the
   boats away and escorts them to Marrow Isle. At dawn both crews land on Marrow Cove's jetty (`marrow_cove`), where
   mission 10 begins.

Checked end to end by the engine's `tools/mission9_check`, starting from mission 8's gangway and walking from the
west cove down to the lower town.

## Relay stones (proposed mechanic)

The story says relay stones are "restoration points inside the dungeon" that switch control between the crews.
As built:
- Talking to one offers **"To <the other crew's lead>"**, **Rest**, **Pokémon** and **Leave**.
- Rest and Pokémon work as at an innkeeper (Pokémon rest free, Adepts pay; Set Pokémon change here).
- Switching keeps this crew's spot as its location and last restoration point, then loads the other crew where it
  stands.
- The switch option only appears while the other crew is somewhere.

## Where the words live

| What | File | Where |
|---|---|---|
| The hook | `maps_src/tradewind_bazaar/events.json` | the gangway warp's `scene`, the `when` step before `resume_crew` |
| Lower town arrival | `maps_src/fallhaven_lower/events.json` | scene `lower_arrival` |
| The three households | `maps_src/fallhaven_lower/events.json` | scenes `family_a`, `child_b`, `family_c` |
| The hatch | `maps_src/fallhaven_lower/events.json` | scene `hatch` |
| Sael at the doors | `maps_src/fallhaven_archive/events.json` | scene `archive_arrival`; slot 9 |
| The archivist's thought, the lift | `maps_src/fallhaven_archive/events.json` | slots 10 and 11, their events' `text` |
| The Ledger | `maps_src/fallhaven_archive/events.json` | scene `ledger` |
| The finale | `maps_src/fallhaven_archive/events.json` | scene `finale` |

## Placeholders and open points

- **Timing (decided, demo 8, 18 Oct: "soon after", played at night):** the story says Fallhaven falls "the
  night after Crew 1 deepened the Forest seal", which is mission 5. As built it falls after missions 5 to 8 are
  all done, because mission 9 needs both crews full, so story.md's line becomes "soon after".
- **Sael's death, Maren's confession and Ilse's choice** are narration over a black screen. They deserve staged
  scenes in the story pass.
- **The lower town** is the whole of Bilibin. The handover sets the clock to night, but walking still moves it on:
  nothing holds it there yet. **The archive** is a palace wing. Its high door and its lift are built as links that
  never let anyone in: their cliff-road and harbour sides are barred and for cargo until mission 9 is done, then
  rubble and a cut rope. Only the archive's own sides open then, so nobody is shut in. Both sit on the tops of its
  west and east corridors until the re-clip.
- **Crew 2's members** appear in the finale as Golden Sun heroes until the graphics pass. Wynn now wears the same
  hero in the bazaar as on her battle curve.
- **Sael** wore a small animal's sprite in mission 2's Fallhaven; she is a townswoman now in both rooms.
- Four object sprites (the ash, the hatch, the lift basket, the vault door) need exporting on a new machine:
  `python tools/export_gs_sprites.py 231 239 242 253`.
- **Mission 10** (the Two-Earth Door) is next, after the asset audit.
