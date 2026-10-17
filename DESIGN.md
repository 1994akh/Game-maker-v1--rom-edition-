# GBA Game Gumbo — Component Decisions

> Synced from the claude.ai project **GBA Game Gumbo** (`claude/component-decisions.md`). That project doc is where design decisions get made; this file is the copy Claude Code builds from.

Living log of what we're taking from **Golden Sun**, **Golden Sun: The Lost Age** and **Pokémon Unbound**. Hand this to Claude Code as the design source of truth. Last updated 2026-10-17 (the 13–16 Oct decisions are in `docs/CHANGELOG.md`; the 14 Oct header below has rows for them).

## Guiding principle: function first, cosmetics last

**Make it work first, make it pretty at the end.** Custom images, sprites and most cosmetics are the **last** thing to do, unless story or function needs them sooner. Until then, use existing FireRed/vanilla assets as placeholders.

What that means in practice:

| Build early (function) | Placeholder until the end (cosmetic) |
|---|---|
| 8-way movement, collision, world map, ship, and Surf/Dive/Waterfall rules (including underwater maps) | Golden Sun tilesets and chibi field sprites (use FireRed's) |
| Battle format, the Adept battler, Psynergy moves, Set/Standby, 18-type classes, Summons | GS spell and Summon animations (reuse existing move animations) |
| Field Psynergy and the map objects that react to it | GS-style Psynergy field effects |
| Weyard forms' **data**: types, stats, moves, abilities, evolutions, Megas, Pokédex text | Weyard forms' **art** (reuse the regular species' sprites, or a simple palette swap) |
| Menus that do something: Set/Standby screen, Psynergy menu, class display | GS-style look for menus and portrait dialogue boxes |
| Djinn-style encounters that can be found, chased, fought and joined | Their final GS-style overworld sprites (any visible placeholder works) |
| Music hooks (which track plays where) | Converting GS tracks; final music mix (use FireRed tracks) |

### Suggested build order

1. **Foundation:** choose the code base; movement (8-way, or the grid fallback); 1 Adept + 1 Pokémon battle format.
2. **Core systems:** Adept battler and Psynergy; Set/Standby and 18-type classes; Summons (with Z/Dynamax merged in); catching plus Djinn-style encounters; field Psynergy replacing most HMs; item Psynergy; Surf, Dive and Waterfall as Pokémon field moves; ship and world map.
3. **Content:** region maps on placeholder tiles; story and the six sites; Weyard form data; roster placement; DexNav and auto-run.
4. **Polish:** GS tilesets and sprites; Weyard form art; GS spell and Summon animations; GS menu and dialogue styling; music mix.

> ## Updated 14 Oct 2026: read this first
>
> Several decisions below were **superseded** after this file was written, mostly because the game is now a **native
> Android app** (no GBA limits) rather than a ROM hack. The detailed rules live in `docs/design/`; superseded rows in
> the tables below are marked **~~struck~~ → new rule** and point there. The unchanged parts (six sites, classes,
> Weyard forms, Djinn-style encounters, function-first order) still stand.
>
> | Was | Now | Where |
> |---|---|---|
> | GBA ROM hack | **Native Android app** (Galaxy Z Fold 7) in **Godot 4.7.2** | `docs/engine/README.md` |
> | 1 Adept + 1 Pokémon per side | **4 Adepts, each with a bonded partner behind them** (16 Oct) vs up to ~6 enemies | `docs/design/party-and-battle.md` §2 |
> | 8 Adepts, one on the field, others swap in | **Two crews of 4**; no swapping in battle; crews change only on the home island | `party-and-battle.md` §1, §3 |
> | Summons from the whole party | From the **active crew** (up to 8 Standby) | `party-and-battle.md` §4 |
> | Partners as separate fighters | **Bonded partners** behind their Adepts: a stat share, their moves, a one-hit shield (16 Oct) | `party-and-battle.md` §2–§3 |
> | Pokémon-style battle menus | **Golden Sun boxes over the sprites**; heroes left, enemies right; sprites scale with the line (15 Oct) | `docs/CHANGELOG.md` |
> | GBA-scale field art | **64×64 Adepts, 32-px tiles, a 480×320 picture** (15–16 Oct) | `docs/design/art-integration.md` |
> | Design questions open | **Act I (missions 1–10) built**; items, equipment, menus and progression designed and answered on the decision page (16 Oct) | `docs/design/`, `docs/CHANGELOG.md` |
> | The whole party's field Psynergy works | The **active crew's** works, with backup items for every group Psynergy | `party-and-battle.md` §7 |
> | Psynergy puzzles replace HMs; Surf/Dive/Waterfall separate | **One field-ability table**: Psynergy and the kept HMs (Cut, Rock Climb, Defog, Whirlpool, Surf, Dive, Waterfall) are the same system | `docs/design/field-abilities.md` |
> | Pokémon damage math | **Golden Sun's formulas and stat scale** for everyone; Adepts out-HP partners | `party-and-battle.md` §5 |
> | No clock | **A day/night clock** (17 Oct): four phases by walking and rest, never real time (proposed) | `docs/design/day-night-clock.md` |
> | (not covered) | **Character creator** for the hero: gender, pronouns, cosmetics; name and gender permanent | `docs/design/character-creator.md` |
> | (not covered) | **Story structure**: hero alone vs the rival → a mission played as the rival → recruitment missions → crew swapping unlocks | `party-and-battle.md` §1 |
>
> Full history: `docs/CHANGELOG.md`. Story work starts from `docs/story/BRIEF.md`.

## The concept

A ~~GBA ROM hack~~ **native Android app** set in a **brand-new region reminiscent of Weyard**. A party of **8 Adepts** fights alongside their **Pokémon**, and the Pokémon play the Djinn role. Each Adept has **3 Pokémon Set** on them: their types decide the Adept's class, one of them fights beside the Adept, and Pokémon on Standby power Summons. Each Adept's own element decides their Psynergy. As in Golden Sun, the whole party's Psynergy works on the field, solving puzzles in place of most HMs, and items grant extra Psynergy anyone can use. Water travel stays Pokémon-powered: Surf, Dive and Waterfall work as HM-style field moves. The world looks and moves like Golden Sun, with The Lost Age's sailing and world map. Battles look like Pokémon with Golden Sun spell effects. The story centers on **six ancient elemental sites**, each covering three types and bound to a legendary Pokémon.

## Decisions

### Core systems

| Area | Decision | Source |
|---|---|---|
| Platform | ~~GBA ROM hack~~ → **Native Android app, Godot 4.7.2** (14 Oct) | `docs/engine/` |
| Battle format | ~~1 Adept + 1 Pokémon per side~~ → ~~4 Adepts + 4 partner Pokémon~~ → **4 Adepts, each with a bonded partner behind them** (16 Oct); the enemy side capped as in Golden Sun | `docs/design/party-and-battle.md` §2 |
| Party | ~~8 Adepts, one on the field, the others swap in~~ → **Two crews of 4**. Crew 1 = hero (Earth), Sea, Forest, Shadow; Crew 2 = rival (Earth), Sea, Flame, Sky. You play one crew at a time; no swapping in battle (13 Oct) | `party-and-battle.md` §1 |
| Adept element | **Each Adept belongs to one of the 6 site groups** (Earth, Flame, Sea, Sky, Forest, Shadow). **Earth and Sea have two Adepts each.** Earth: the hero plus a rival or co-lead, a nod to Isaac and Felix both being Venus. Sea: ~~a second healer for when Adepts swap in and out~~ → one Sea healer per crew | Golden Sun, adapted |
| What the element does | **Decides the Adept's Psynergy, in battle and on the field.** **Set Pokémon that match the Adept's group give a bonus** (stronger Psynergy or better stats) | Golden Sun, adapted |
| Set Pokémon | **3 Pokémon Set per Adept, 24 total.** One of the three is the Adept's fighting partner at a time | Golden Sun Djinn, adapted |
| Class system | **All 18 types** get their own class lines (not collapsed into the 4 GS elements) | Golden Sun, expanded |
| Class rule | **Weighted type score** across the 3 Set Pokémon: **primary type = 1 point, secondary type = 0.5 points.** The highest total picks the class line, and stacked secondary types can tip it. **Certain type pairs unlock special classes** on top of that. See "Class scoring" below | Hybrid |
| Tie-breaker | **The type in the Adept's own element group wins; failing that, the fighting partner's primary type** | New |
| Class tiers | **Move up by Adept level**, like Golden Sun | Golden Sun |
| Class during battle | **Locked for the whole battle.** Mega Evolution, form or type changes, and partner swaps mid-battle do **not** change the Adept's class. It's recalculated after the battle | New |
| Big attacks | **One Summon system.** Z-Moves and Dynamax are merged into it; their visuals can be reused as Summon variants | GS Summons + Unbound Z/Dynamax |
| Summon cost | **1–3 Standby Pokémon by tier,** of matching types, ~~drawn from the whole party~~ → **drawn from the active crew** (up to 8) (13 Oct) | `party-and-battle.md` §4 |
| Field puzzles | ~~Psynergy puzzles replace most HMs~~ → **Psynergy and HMs are one field-ability system**; the kept HMs add new puzzle verbs (14 Oct) | `docs/design/field-abilities.md` |
| Water field moves | **Surf, Dive and Waterfall** stay Pokémon-powered, now as rows of that same table (free to use; any Set Pokémon in the active crew that can learn them) | `field-abilities.md` |
| Catching | **Both:** Poké Balls for most Pokémon; **Djinn-style encounters** for special and regional ones. See below | Hybrid |

#### Class scoring

Add up each type across the Adept's 3 Set Pokémon: **primary type +1, secondary type +0.5.** Highest total picks the class line.

- **Majority example:** Gyarados (Water/Flying), Pelipper (Water/Flying), Charizard (Fire/Flying) → Water 2, Flying 1.5, Fire 1 → **Water** class line.
- **Stacked secondaries example:** swap Gyarados for Togekiss (Fairy/Flying) → Flying 1.5, Water 1, Fire 1, Fairy 1 → **Flying** wins on three stacked secondaries.
- **Tie example:** a Sea Adept with Lapras (Water/Ice), Jolteon (Electric), Ninetales (Fire) → Water 1, Electric 1, Fire 1, Ice 0.5 → three-way tie → Water is in the Sea group, so **Water** wins.

#### Djinn-style encounters

Special and regional Pokémon are found in the world, Golden Sun style, with a **mix of encounter types**:
- **Join on contact:** reach it and it joins.
- **Chase:** it runs when spotted, and you have to corner it.
- **Battle first:** it fights you, and joins if you win.
- **Hidden:** the best ones need Psynergy just to reach or spot (e.g., Reveal to see them, Growth to climb to them).

#### Field Psynergy

**Rules (as in Golden Sun):**
- **The whole party's field Psynergy works while exploring**, not just the lead Adept's. Using it spends that Adept's PP. Which Adepts have joined so far decides what the player can do.
- **Item Psynergy:** certain items grant a Psynergy **anyone** can use (Golden Sun examples: Lifting Gem, Hover Jade). They serve two jobs:
  1. **Progression keys:** dungeon and site rewards that open the next area, as in Golden Sun.
  2. **Backups:** item versions of key group Psynergy, so no puzzle ever *requires* one specific Adept.

**Innate Psynergy by element group:**

| Group | Field Psynergy | Notes |
|---|---|---|
| Earth | Move, Pound, Tremor, Scoop | Scoop (digging) fits Ground |
| Flame | Blaze, Burst, Force, Parch | Parch (drying up water) fits Fire; Force fits Fighting |
| Sea | Frost, Douse, Ply | Ply heals outside battle |
| Sky | Whirlwind, Cyclone, Mind Read, Teleport, **Retreat** | Mind Read, Teleport and Retreat fit Psychic; Teleport comes late |
| Forest | Growth, Lash, Catch | Vine-based: Lash ties vine ropes, Catch grabs distant objects |
| Shadow | Reveal, Cloak, Halt, **Avoid** | Seeing hidden things, sneaking, freezing targets in place, slipping past wild Pokémon |

**Item-only Psynergy (anyone can use):** Lift, Carry, Hover, Grind, Sand, plus backup items for key group Psynergy.

**Retreat and Avoid vs. Escape Rope and Repel: keep both.** Retreat (escape a dungeon) and Avoid (fewer wild encounters) are Psynergy for the Adepts who have them. Escape Rope and Repel stay as items, as backups, following the same rule as item Psynergy.

#### Water field moves (HM-style)

Water travel stays with the Pokémon rather than Psynergy. These work like Unbound's HM system: **no move slot needed.** If **any Set Pokémon in the party** can learn the move, the party can use it on the field, the same party-wide rule as Psynergy.

| Move | Function | Limits |
|---|---|---|
| **Surf** | Ride a Pokémon across water | **Only on rivers, lakes and coastal shallows, for short distances.** Deep sea needs the ship |
| **Dive** | Dive at dark deep-water patches to explore underwater areas, then surface again (like Gen 3's HM08) | Dive spots sit in surfable water |
| **Waterfall** | Climb up waterfalls to reach new areas | Only marked waterfalls |

### World and story

| Area | Decision | Source |
|---|---|---|
| Region | **Brand-new region reminiscent of Weyard** | New, GS-inspired |
| Story driver | **Six ancient elemental sites** (like the lighthouses), three types each, each bound to a legendary. See table below | GS + Pokémon |
| Overworld travel | **Lost Age-style world map and sailing.** The ship handles open sea | Golden Sun: The Lost Age |
| Surf | **Limited:** works only on rivers, lakes and coastal shallows, for short distances. Deep sea needs the ship. Dive and Waterfall also stay (see "Water field moves") | Modified Pokémon |
| Movement | **Golden Sun free 8-way movement** (see risk note) | Golden Sun |

#### The six elemental sites

| Site | Types | Legendary | Adepts |
|---|---|---|---|
| Earth (Venus) | Ground, Rock, Steel | Groudon | 2 (hero + rival/co-lead) |
| Flame (Mars) | Fire, Fighting, Dragon | Ho-Oh | 1 |
| Sea (Mercury) | Water, Ice, Fairy | Lugia | 2 (healers) |
| Sky (Jupiter) | Flying, Electric, Psychic | Rayquaza | 1 |
| Forest | Grass, Bug, Poison | Celebi | 1 |
| Shadow | Dark, Ghost, Normal | Giratina | 1 |

The first four follow Golden Sun's elements: Mercury Adepts are healers (hence Fairy), and Jupiter covers wind, lightning and mind. These six groups are also the Adept elements.

### Pokémon

| Area | Decision | Source |
|---|---|---|
| Roster | **All Gen 1–7 Pokémon catchable throughout**, plus Megas (Z/Dynamax folded into Summons) | Unbound |
| Regional forms | **25 families get Weyard-style forms**, period and genre appropriate like Hisuian forms. **Whole evolution lines** change, not just final stages: **about 57 species** in all (list below). Data first, art last | New |
| Branching evolutions | **Weyard Eevee can evolve into any Eeveelution**, and **Weyard Kirlia can still become Gallade.** Only the listed branches (Umbreon, Sylveon, Gardevoir) get Weyard forms; the others evolve into their regular forms | New |
| Weyard Megas | **Weyard forms keep Mega Evolution**, as Weyard Megas: Venusaur, Charizard X and Y, Blastoise, Sceptile, Blaziken, Swampert, Lucario, Garchomp, Gardevoir, Gengar, Tyranitar, Rayquaza, plus **Primal Groudon**: **14 extra forms** | New |
| QoL | DexNav, auto-run, no HM moves taking up move slots | Unbound |

#### Weyard-form families (25 families, ~57 species + 14 Mega/Primal forms)

- **Gen 1–3 starters (9 families, 27 species):** Bulbasaur → Ivysaur → Venusaur; Charmander → Charmeleon → Charizard; Squirtle → Wartortle → Blastoise; Chikorita → Bayleef → Meganium; Cyndaquil → Quilava → Typhlosion; Totodile → Croconaw → Feraligatr; Treecko → Grovyle → Sceptile; Torchic → Combusken → Blaziken; Mudkip → Marshtomp → Swampert
- **Top 10 most popular non-legendaries (24 species), also available as story Pokémon.** Ranked by the 2020 Pokémon of the Year poll, skipping Gen 1–3 starters and Gen 8 Pokémon: Froakie → Frogadier → Greninja; Riolu → Lucario; Mimikyu; Eevee → Umbreon / Sylveon; Gible → Gabite → Garchomp; Ralts → Kirlia → Gardevoir; Gastly → Haunter → Gengar; Larvitar → Pupitar → Tyranitar; Rowlet → Dartrix → Decidueye
  - Alternates if swaps are wanted: Aegislash, Chandelure, Pikachu, Eevee
  - Flavor idea (polish phase): Weyard Mimikyu wears a homemade Djinn costume instead of a Pikachu one
- **Site legendaries (6):** Groudon, Ho-Oh, Lugia, Rayquaza, Celebi, Giratina

### Presentation (polish phase; placeholders until then)

| Area | Decision | Source |
|---|---|---|
| Art | **Golden Sun world** (tilesets, chibi field sprites); **Pokémon-style battle scenes** with GS spell effects | Mix |
| Spell visuals | Golden Sun Summon and spell animations | Golden Sun |
| UI | **Golden Sun menus and portrait dialogue boxes on the field; ~~Pokémon menus in battle~~ → Golden Sun-style boxes over the sprites in battle (15 Oct).** Menu *functions* are built early; the GS *look* comes last | Mix |
| Music | **Mix of both games**; which tracks go where is TBD | Mix |

## Not must-haves (could come back later)

- Difficulty modes (Unbound)
- Missions / Mission Log (Unbound)
- Battle Frontier / Tower / Circus (Unbound)

## Risks and technical notes for Claude Code

- **8-way free movement is the largest single job.** The Pokémon engine's maps, collision, NPC movement, warps and scripts all assume a tile grid. Fallback if it's too costly: 8-direction (diagonal) walking on the grid. Size both before building. This is function, so it belongs in phase 1.
- **4-fighter battle limit.** The Gen 3 Pokémon battle engine supports at most 2 fighters per side. The 1 Adept + 1 Pokémon format was chosen to fit it.
- **Field Psynergy is a new interaction system.** Each Psynergy needs map objects or tiles that react to it (pushable pillars, puddles that freeze, sprouts that grow into vines, hidden things that Reveal shows) plus a way to aim it (facing direction). Prove the system with a small set first, e.g., Move, Frost, Growth and Reveal, then add the rest.
- **Item Psynergy** needs items that add a Psynergy to the field menu for any Adept, and progression flags tied to them.
- **Retreat/Avoid and Escape Rope/Repel** should share one underlying effect each, so the Psynergy and item versions behave identically.
- **Djinn-style encounters** need overworld objects with behaviors (stand still, flee from the player, start a battle) and a join/catch result that adds the Pokémon without a Poké Ball. Fleeing behavior depends on the movement system, so build it after movement is settled.
- **Set Pokémon storage.** 8 Adepts × 3 Set Pokémon = 24, which fits in one 30-slot PC box's worth of save space. The normal 6-slot party won't hold them, so Set Pokémon need their own storage structure.
- **Class scoring in half-points.** The GBA has no floating-point hardware, so store type scores doubled (primary = 2, secondary = 1) and compare integers. **Compute class at battle start and freeze it until the battle ends**; recompute outside battle whenever Set Pokémon, the fighting partner, or a Pokémon's form/type changes.
- **Party-wide Standby pool.** Summons must count Standby Pokémon across all 8 Adepts, not just the one in battle.
- **Regional forms: data now, art later.** The engine handles them like Alolan/Galarian forms. Early work is types, stats, moves, abilities, evolutions, Mega data and Pokédex text for ~57 species plus 14 Mega/Primal forms, displayed with the regular species' sprites. The art pass at the end needs front and back battle sprites, a menu icon, normal and shiny palettes, and a GS-style overworld sprite for Djinn-style encounters.
- **Branching evolutions** need form-aware evolution data: a Weyard Eevee or Kirlia evolving into a non-Weyard branch has to produce the regular species.
- **Limited Surf** needs a terrain rule: Surf is allowed only on marked water types (river, lake, shallows), and deep sea blocks it.
- **Water field moves check the whole party's Set Pokémon** for one that can learn Surf, Dive or Waterfall, with no move slot used (Unbound's HM approach, adapted to Set Pokémon instead of a normal party).
- **Dive needs underwater maps.** FireRed has no field use for Dive (it was Ruby/Sapphire/Emerald only), so the chosen code base has to add it: dive-spot tiles, underwater map layers linked to the surface, and the surfacing rule. Factor this into the code-base recommendation. Waterfall already exists in FireRed.
- **No Golden Sun decomp found.** GS mechanics (Djinn, classes, Psynergy, Summons, world map, sailing) have to be rebuilt. GS art and music have to be ripped from the ROMs, but that's polish-phase work.
- **Unbound's own content isn't open.** Its maps, story and 180+ song OST aren't public. The engine pieces it's built on are: Complete FireRed Upgrade (CFRU) and Dynamic Pokémon Expansion (DPE), both on GitHub. Credit and ask before reusing anything taken directly from Unbound.
- **GS music** would need converting to the Pokémon sound engine (polish phase).
- **Code base not chosen yet.** The options are CFRU on FireRed (how Unbound was built), the FireRed decomp (pret/pokefirered), or another decomp-based expansion. Claude Code should recommend one based on the decisions above.

## Open questions (next rounds)

These are content and balance details; none of them block phase 1 (foundation) work.

- **Progression keys:** which item Psynergy does each site or dungeon award?
- **Water field moves:** how are Surf, Dive and Waterfall unlocked (story events, site rewards, or a key item)? Can the ship also dive at marked open-sea spots?
- **Special combos:** which type pairs unlock special classes, and what score do both types need (e.g., at least 1 point each)?
- **Class tiers:** how many tiers per class line, and at which levels?
- Which Z/Dynamax visuals carry over into Summons?
- Do the regular forms of the 25 families also exist in the region, or only the Weyard versions?
- What story roles do the popular 10 play (rival, villain, companions, site guardians)?
- Music split: which game's tracks go where?

## Sources

- [Pokémon Unbound thread (PokéCommunity)](https://www.pokecommunity.com/threads/pok%C3%A9mon-unbound-completed.382178/)
- [Pokémon Unbound (GameBrew)](https://www.gamebrew.org/wiki/Pokemon_Unbound_GBA)
- [Pokémon of the Year 2020 results (Bulbapedia)](https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_of_the_Year)
