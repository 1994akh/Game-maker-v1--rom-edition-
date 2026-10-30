# Story brief

> **The story is now written: [story.md](story.md)** (14 Oct 2026). This brief stays as the list of constraints it
> was written against. The story chat is archived (16 Oct); story questions are
> answered on the decision page ([story-questions.md](story-questions.md)).

For writing the story in the claude.ai design chat (14 Oct 2026). This is everything the story has to respect and
everything already decided about its shape. Story decisions that don't need a mechanic are yours to make there; the
engine work continues in parallel and reads only the decisions recorded in this repo.

## Where things stand

- The game is a **native Android app** (Galaxy Z Fold 7) in **Godot 4.7.2**. The first room, Sol Sanctum, already
  walks and its Move puzzle plays. Work in progress: the next field Psynergy (Frost, Growth), NPC talk, the first
  battle.
- The design source of truth is `DESIGN.md` plus `docs/design/`. `DESIGN.md` has a 14 Oct header listing what was
  superseded. `docs/CHANGELOG.md` lists every decision since 13 Oct with the reasons.
- The story has **no decided content yet** beyond the structure below. One finished draft exists as raw material:
  `docs/story/drafts/elemental-epic.md`. It predates several decisions (see its caveats), so take ideas, not text.
  `docs/design/world-map.md` is the decided world (24 Oct): the rings, every place, its rooms and how they join, and
  how you move between them. `docs/phase1/WORLD_PROPOSAL.md` is an earlier proposal it replaces: take no traversal or
  biomes from it.

## Fixed: the shape of the story (decided 13 Oct)

1. **Opening:** the hero, alone, against the rival.
2. **Then a mission played as the rival.**
3. **Recruitment:** every other Adept has their own story mission(s). Each either adds them to a crew or moves the
   story forward.
4. **Crew swapping** (switching which crew you play; moving Adepts between crews on the home island) **unlocks only
   after the crew-building missions are done.** Until then the story decides which crew you play.
5. A crew can be smaller than 4 early on. Some dungeons need both crews.

## Fixed: the cast

Two crews of four, each with an Earth lead and a Sea healer:

| | Crew 1 (the hero's) | Crew 2 (the rival's) |
|---|---|---|
| Lead | Earth: **the hero** (player-created: name, gender, pronouns, cosmetics; element always Earth) | Earth: **the rival / co-lead** |
| Healer | Sea | Sea |
| Others | Forest, Shadow | Flame, Sky |

- The hero is customised in a character creator; **name and gender are permanent**, so the story can't rename them.
  Dialogue uses `{HERO}`, `{HERO_SUBJ}`, `{HERO_OBJ}`, `{HERO_POSS}` tokens. Everyone else is a fixed character.
- **The hero starts with no Pokémon.** Partners are gained through the story.
- Element groups and their field Psynergy (what each crew can do on the map):
  - Earth: Move, Pound, Tremor, Scoop. Flame: Blaze, Burst, Force, Parch. Sea: Frost, Douse, Ply.
  - Sky: Whirlwind, Cyclone, Mind Read, Teleport (late), Retreat. Forest: Growth, Lash, Catch.
  - Shadow: Reveal, Cloak, Halt, Avoid.
  - **Crew 1 therefore has Move, Frost, Growth and Reveal from the start of its full line-up; Crew 2 has Blaze,
    Whirlwind and the Sky utilities.** Backup items cover what a crew lacks, and recruitment missions are the natural
    place to hand them out.
- HMs are now field abilities too, gated by the crew's Set Pokémon: **Cut, Rock Climb, Defog, Whirlpool, Surf,
  Dive, Waterfall.** They are free to use. Each is a puzzle verb (plants to cut, cliffs to climb, fog to clear,
  whirlpools to calm) the story can gate on.

## Fixed: the world's bones (from DESIGN.md)

- A brand-new region reminiscent of Weyard; inspiration from One Piece (crew gathering, island-hopping, a navigation
  gimmick, a big bright sea), Golden Sun and Pokémon. **Invent all names**; no One Piece, Golden Sun or Pokémon
  character or place names (Pokémon species and the six legendaries are fine).
- **Six ancient elemental sites**, each covering three types and bound to a legendary:

  | Site | Types | Legendary |
  |---|---|---|
  | Earth | Ground, Rock, Steel | Groudon |
  | Flame | Fire, Fighting, Dragon | Ho-Oh |
  | Sea | Water, Ice, Fairy | Lugia |
  | Sky | Flying, Electric, Psychic | Rayquaza |
  | Forest | Grass, Bug, Poison | Celebi |
  | Shadow | Dark, Ghost, Normal | Giratina |

- The Lost Age's **world map and sailing** (a ship handles open sea; Surf only on rivers, lakes and shallows; Dive
  opens underwater areas; Waterfall climbs marked falls).
- **Weyard-form Pokémon**: 25 families (the Gen 1–3 starters, the "popular 10" such as Greninja, Lucario, Mimikyu,
  Garchomp, Gardevoir, Gengar, Tyranitar, Decidueye, Eevee's branches) with story roles to assign.
- **Djinn-style encounters** for special Pokémon: join on contact, chase, battle first, or hidden (Reveal/Growth).
- Enemies: Golden Sun monsters and bandits (uncatchable), wild Pokémon (catchable), human trainers who fight as
  Adept + Pokémon pairs with element-limited rosters.
- Restoration points: Pokémon heal free, Adepts pay. Defeat: wake at the last restoration point, everyone restored,
  half your coins lost.

## Open, and yours to decide in the story

- The order of the recruitment missions and which Adept's mission unlocks crew swapping.
- When the crews first split and when they reunite; what each crew's chapters cover; which dungeons need both.
- Which of the "popular 10" play which roles (rival's ace, villain, companions, site guardians).
- How each legendary is met (Djinn-style "battle first", a catch, or a Summon unlock).
- Names for everything: the region, the islands, the Adepts (the hero's default name too), the factions.
- Tone: One Piece's warmth, Golden Sun's earnest moral grey, or the mix.

## Must come back as a mechanics question (don't decide these in the story)

Anything that needs a new system or changes how the game plays. Flag it in the story doc with its recommended
answer, and it gets settled here before the engine builds it:
- Walking on the world map vs ship-only; a sky layer or an undersea layer; minecarts or other vehicles.
- Time travel, a mirror world, or any mechanic where a map has two states.
- Ship upgrades (cannon, wings, hull) and what each unlocks.
- Special battle rules inside a mission (a timed sequence, a forced loss, a temporary party, fighting without
  Pokémon, a duel).
- Any new field ability beyond the table in `docs/design/field-abilities.md`, or a new puzzle object type.
- Post-game systems.

## How to hand the story back

Write it to `docs/story/story.md` in this repo (sections: logline, world, cast, sites, the mission list in order with
the crew played and what each unlocks, exploration table, decisions made, mechanics questions). The engine side reads
the mission list to know which room, Psynergy and objects to build next, so the mission list is the part that
matters most.
