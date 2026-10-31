# Field abilities: Psynergy and HMs as one system

**Decided (14 Oct 2026):** Pokémon's HM field moves and Golden Sun's field Psynergy are **one system**. Both are "an
ability used on the tile or object in front of you, gated by whether someone in the active crew has it." Redundant
HMs are dropped; the ones that add a new puzzle verb are kept as abilities alongside Psynergy. Engine work is
identical for both, so this costs nothing extra to build.

## One table

Every field ability is a row with the same fields, whether it came from Golden Sun or Pokémon:

| Field | Meaning |
|---|---|
| id | A name (`move`, `frost`, `cut`, `rock_climb`…) |
| source | **psynergy** (an element group's Adepts have it) or **hm** (a Set Pokémon in the crew can learn the move) |
| group / move | The element group, or the Pokémon move id |
| target | `actor` (an object in front), `tile` (the cell ahead), `area` (around the player), `self` |
| range_px | How far ahead it looks (Golden Sun's per-Psynergy ranges: 16, 32 or 48) |
| objects | The object kinds it acts on (puddle, sprout, pushable, cracked rock, plant, cliff, fog…) |
| effect | The state change (slide a cell, become ice, grow a vine, remove, light, reveal, climb, surf…) |
| cost | PP for Psynergy; **free for HMs** (see Cost) |
| unlock | Story flag, item, or "innate" |

The Golden Sun rows are **generated from the extraction** (`field_psynergy.json`: targeting, range, object types and
event counts for all 30 Psynergy). The HM rows are written by hand in a small overlay. Nothing in the engine
distinguishes the two at run time.

## Which HMs stay

| HM | Verdict | Why |
|---|---|---|
| Strength | **Dropped**: it is Move | Same verb: push a heavy object one cell |
| Flash | **Dropped**: Reveal / Blaze cover it | Lighting a dark room is Reveal's view mode or Blaze on torches |
| Rock Smash | **Merged into Burst** | Same verb: break the cracked rock ahead |
| Cut | **Kept** | Clear a plant blocking a path. Growth's opposite: a new verb |
| Rock Climb | **Kept** | Scale a marked cliff face. Nothing in Golden Sun climbs; it enables vertical dungeons |
| Defog | **Kept** | Clear fog hiding a route. Pairs with Reveal (which shows hidden things but doesn't clear them) |
| Whirlpool | **Kept** | Calm a whirlpool so the ship or Surf can pass. A sea-route gate the ship design needed |
| Surf, Dive, Waterfall | **Kept** (already decided) | Water travel stays Pokémon-powered |
| Fly, Teleport (Pokémon) | **Dropped** | Teleport is Sky Psynergy; one fast-travel system is enough |

## Gating: who can use it

One check, two sources:
- **Psynergy:** usable if any Adept in the **active crew** belongs to its element group (and has learned it).
- **HM:** usable if any **Set Pokémon in the active crew** can learn the move (no move slot used). This is the rule
  already chosen for Surf, Dive and Waterfall, applied to every HM.
- **Items** (Lifting Gem, Orb of Force, the new backup items from the party rules) grant a Psynergy to anyone, as
  before.

The stranding rule from the party rules still holds: a restoration point won't unset the last Pokémon that can use
an unlocked water move, and the same protection extends to any HM a crew's current area needs.

## Cost

- **Psynergy** costs the casting Adept's PP, as in Golden Sun.
- **HMs are free.** A Pokémon is doing it for you. This keeps partner Pokémon useful on the field even when they're
  not the one fighting, and it mirrors Pokémon, where HMs never had a field cost.

## What it means for puzzles

Each ability is a puzzle family: a marked object or tile kind that reacts to exactly that verb. Rooms gate on which
verbs the active crew has, so the kept HMs add four new families (plants to cut, cliffs to climb, fog to clear,
whirlpools to calm) on top of Golden Sun's. Area design uses the per-crew coverage table in the party rules, now
with HMs counted as another source a crew can bring.

## Engine status

Built (16 Oct): the generated table (`tools/export_field_abilities.py` plus the `data_src/field_abilities_hm.json`
overlay), crew gating (`CrewAbilities`, `Room.crew_can_cast`), and Move, Frost, Growth, Reveal, Halt, Scoop, Whirlwind,
Mind Read, Cut, Defog and Surf across missions 1–9. Not built: Rock Climb, Whirlpool, Dive, Waterfall, and item
Psynergy (its gate never fires today, items-and-economy.md §14).

Built (31 Oct, engine PR #90, from the 24 Oct reports and decisions 67–73, 118–121), how every field cast and
puzzle plays:

- **The cast (70, 118, 119, 121).** Every Psynergy cast first checks it can happen, then the hero turns to the 4-way
  aim and holds the raised-hand pose with a glow at the hand for half a second (Earth amber, Sea blue, Flame red, Sky
  violet; Forest leaf green, Shadow deep indigo with a pale lilac rim), then pays the PP and the effect plays; the
  field takes no input until the effect ends. An HM move (Cut, Defog, Surf) shows the Set Pokémon's icon popping up
  beside the hero with a small hop instead of a glow, Surf's just before the hop onto the water. L or R with nothing
  in front plays a quarter-second pose with a grey puff, no PP and no words.
- **PP only on success.** A cast is refused before any payment when its verb has no handler yet (Douse, Ply, Force,
  Lift, Carry, Catch), when its target's event is done (an event is active until its flag is set, so a solved block
  can't be moved off its target and a charged wheel doesn't charge again), when Halt meets no moving patrol, and when
  nothing reacts; a `text_only` reaction and an `else_text` (an event waiting on a flag) speak for free. R tries
  Reveal before Defog.
- **Aim.** Casts aim as Golden Sun aims: the facing snapped to 4 ways, the actor on the cell 16 px ahead first, else
  the nearest in the row's cone within its range plus the object's radius less 2, so a hero who has walked up against
  a pool or a sprout (17–24 px off) can cast on foot. A Psynergy object blocks only its own cell.
- **Move (120).** Steered freely from any side the hero stands on, with the stick or the pad past half its throw; a
  block never slides onto the hero, and never stops on a way out, an entrance or a step scene's cells; an event may
  allow only some directions (`dirs`), name several sockets (`targets`: the Vault's keepers seat either), or wait on
  a flag (`if_flag`, the cart before Sael). Golden Sun's hand rides the block. A seated block takes no more pushes.
- **Resets (71).** An unsolved puzzle resets when the room is left and entered again; a solved one stays solved, a
  filled pit stays filled, and a partial step may be a temporary map flag (`temp`). Saves no longer carry pushed
  cells. A room rebuilt with its Frost or Growth done shows the settled pose at once.
- **Effects.** Frost's snow and flash before the freeze, Growth's leaves before the grow, Scoop's dig and the earth
  sinking before the hole is painted, Cut's slash, Whirlwind's swirl with the sail swinging and fading and the wheel
  jittering, Blaze's flicker (a lit brazier keeps a flame), Mind Read's ring, Halt's ripple, Defog's veil thinning,
  a block dropping into its pit, an amber tint and a shake on a socket. Gates open after their effect.
- **Climb (67), pillars (68), water (69), ledges (72).** A grown vine is climbed facing it at half walking speed,
  hands alternating, and can be stopped or backed down part way; frost pillars are hopped one per press; onto the
  water and back is a quarter-second hop with a splash; a one-way ledge is hopped down and never climbed back. A
  frozen pool that plugs a breach (Canalport's two tide pools, `pillar: false`) is never hopped, so the flood band
  waits for both breaches as mission 3's script has it, and Frost first makes a way to hop at the Long Weir.
- **Guards and patrols.** A guard sees 20 px either side of his line and nothing behind him; walls and solid things
  (a pushed crate) block his sight. A patrol with `knocks_back` (the reef's boom) shoves the hero back with a short
  hop; a halted one doesn't. A scene may play once when a flag is set in the room (`trigger: "flag"`).
- **The Start menu** casts the chosen Adept's field Psynergy, who pays, so Retreat and Avoid are reachable there.
- **The checks (73)** walk the hero by input along real paths, and `test_demo_puzzles` plays every built puzzle (every
  Move block and every Psynergy and HM event in the demo's rooms) from its pre-state, with its glow or icon;
  `test_puzzle_recoverable` holds every Move block to a state a player can recover from.
