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

Move is built (the Sol Sanctum puzzle plays). The ability table is generated next; Frost, Growth and Reveal follow,
then the HM rows. No existing code changes: the field code already treats every ability as target + range + effect.
