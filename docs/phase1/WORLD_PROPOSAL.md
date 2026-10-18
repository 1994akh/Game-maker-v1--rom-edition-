# World and story proposal: "Halcyra" (working name)

**Status: proposal only.** It was written for the claude.ai project's chat, now archived; docs/story/story.md (14 Oct) took its place. Nothing here is decided. All names are placeholders I made up. The One Piece influence shows only in structure: crew gathering, island-hopping, a compass, calm belts, a continental wall, and sky and undersea layers. No One Piece characters or places are named.

**Evidence legend:** **VERIFIED** means I read it in code or docs, cited `path:line` or by URL. **INFERRED** means it is a reasoned conclusion I did not test. Story and world content is proposal and needs no evidence. Engine claims in §6 are all marked.

Paths are relative to `expansion/` unless stated.

---

## 0. Summary

- **The world:** one ocean world split by a north–south continental wall (**the Spine**). An east–west storm band (**the Galeway**) runs across it, with calm, windless belts on each side (**the Stillwaters**). The world's edges are crumbling waterfalls (**the Rimfalls**), a Weyard-style threat. Above it is a cloud sea (**the Cloudreach**), below it an undersea plateau (**the Deep Shelf**), and at the end a mirror world (**the Hollow**, Giratina's).
- **Story spine:** six "Wells" (the elemental sites) were sealed long ago, and the world is eroding from its edges. Two factions want opposite things:
  - the sea-ruling **Tidewardens** keep the seals;
  - the edge-dwelling **Rimborn** want to break them.

  The rival Earth Adept is taken in the prologue and travels with the Rimborn. It plays out like Isaac and Felix in Golden Sun.
- **Structure:** four acts. Act I is linear and on foot (with ferries). Acts II and III are open-ish, with island-hopping and a compass that offers two or three bearings. Act IV returns home, then goes into the Hollow.
- **Crew roles double as ship upgrades:** navigator, shipwright, gunner, diver and so on. Each recruitment unlocks a new way to move.
- **Engine needs that must be planned in phases 1–2:**
  - a ship avatar state (the 8-bit avatar flags are all used);
  - world-map, sky and undersea map types;
  - a limited-Surf terrain rule;
  - flag-based unlocks for Surf, Dive and Waterfall;
  - budgets for metatile behaviors and the 16 active objects.

  Dive is already present and not FRLG-gated in the expansion.

---

## 1. Themes and story spine

### Themes

| Theme | Source of inspiration | How it shows up |
|---|---|---|
| Found family / crew gathering | One Piece | Each Adept joins at the end of their own island arc and brings a crew role that upgrades the ship |
| Elemental balance and a world-scale threat | Golden Sun (lighthouses; Weyard's edge eroding into Gaia Falls) | Six sealed Wells; the Rimfalls creep inward, swallowing edge islands |
| Moral ambiguity | Golden Sun: The Lost Age (the "villains" had a point) | The Rimborn are right that the world is dying and wrong about how to save it; the Tidewardens keep order but hide the truth |
| Legendaries as forces of nature | Pokémon | Each Well is bound to a legendary that wakes, judges, and must be calmed |
| Freedom of the sea | One Piece / The Lost Age | Open sailing, hidden islands, a compass that offers choices |

The edge-erosion motif is GS canon. The Rimfalls are where Weyard's seas pour off the world, and they creep inward as Alchemy is lost. Source: [Golden Sun Wiki: Gaia Falls](https://goldensunwiki.net/wiki/Gaia_Falls).

### Factions (proposal)

- **The Tidewardens.** A naval order that rules the sea lanes from **the Pinnacle**, a capital on top of the Spine. Their founding mandate is to keep the Wells sealed. They license or hunt Adepts, which gives the island-liberation arcs. Their leader, the **Grand Warden**, secretly wants the Wellstones to wake Groudon and raise the Spine. That would save the centre and let the edges fall. He is the final antagonist.
- **The Rimborn.** Refugees from the crumbling edges, who fill the role the Proxians play in Golden Sun. A duo of Rimborn Adepts leads the raids on the sites and serves as recurring site bosses. The rival Earth Adept travels with them in good faith.
- **Optional third party: free sailors and pirates.** Neutral islands, the Tradewind Bazaar, bounty-style side content.

### Story spine (4 acts)

| Act | Setting | Beats | Recruits | Sites |
|---|---|---|---|---|
| **Prologue / I: "Adrift"** (linear) | Dawnward Upper Sea: Hearthland and nearby isles | A quake opens the Keystone Vault under Mt. Keystone. The Rimborn steal the six Wellstones and take the rival. The hero is swept out. Ferries and Surf come first. A prison break at a Tidewarden fortress. The Rimborn try to ignite the Cinder Spire, and Ho-Oh wakes. The party claims the **Heartstone**, an engine stone for the ancient ship the **Wayfarer** (like the Black Orb that powers the Lemurian Ship). | Hero (Earth), Maren (Sea healer), Tamsin (Flame) | **Flame: Cinder Spire** (Ho-Oh) |
| **II: "The Galeway"** (open: 3 main arcs in any order, plus 4 optional isles) | The Galeway's eastern half and the Dawnward Lower Sea | Ho-Oh's Rainbow Wing parts the Stormwall. The Lodestar compass offers three bearings. Island arcs (bazaar, giant tree, ghost-ship reef) and free-sail side isles give item Psynergy. The act ends at the Ascending Locks: Waterfall climbs over the Spine. | Wynn (Sky, navigator), Sorrel (Forest, shipwright), Vesper (Shadow, lookout) | **Forest: Eldergrove Heart** (Celebi) |
| **III: "Deep and High"** (open: Sea and Sky in either order) | Duskward Seas, the Deep Shelf and the Cloudreach | At the Rimward Camps the party learns the truth: the edges are falling. Dive unlocks at Coralreach. A bubble-coated ship descends to the Deep Shelf. The Rimborn duo falls, and the rival defects, bringing ship Wings. An updraft lifts the ship into the Cloudreach. | Nerissa (Sea healer 2, diver), Corvin (Earth rival/co-lead) | **Sea: Silverdeep Sanctum** (Lugia); **Sky: Stormspire** (Rayquaza) |
| **IV: "The Crown and the Hollow"** | The Pinnacle, Hearthland, the Rim | Infiltrate the Pinnacle. The Grand Warden takes the Red Orb to the Keystone Vault, and Groudon turns Primal; Rayquaza intervenes. Teleport arrives. He flees through the Umbral Gate into the Hollow. Final battle. The Wells flow again and the Rimfalls recede. | — | **Earth: Keystone Vault** (Groudon / Primal Groudon); **Shadow: Umbral Gate / the Hollow** (Giratina) |
| **Postgame (optional)** | Hidden island | Collecting every **Bearing Shard** reveals **the Last Bearing**, a "final island" with superbosses | — | — |

This mirrors Golden Sun's structure: a robbed shrine in the prologue (like Sol Sanctum), then a return to the home mountain at the climax (like Mt. Aleph).

---

## 2. World map outline

### Shape (schematic)

```
                 N   ~ ~ ~  R I M F A L L S  (crumbling edge)  ~ ~ ~
   DUSKWARD UPPER SEA            ║ S ║        DAWNWARD UPPER SEA  (Act I: Hearthland)
   (Rimward Camps, Umbral Gate)  ║ P ║
 ========== Stillwater ==========║ I ║========== Stillwater ==========
 ≈≈≈≈≈≈≈≈ G A L E W A Y ≈≈≈≈≈≈≈≈≈║ N ║≈≈≈≈≈≈≈≈ G A L E W A Y ≈≈≈≈≈≈≈≈  (Act II, east half)
 ========== Stillwater ==========║ E ║========== Stillwater ==========
   DUSKWARD LOWER SEA       Ascending Locks   DAWNWARD LOWER SEA (optional isles)
   (Coralreach, Pearlhollow)     ║   ║
                 S   ~ ~ ~  R I M F A L L S  ~ ~ ~
 Layers:  ABOVE = Cloudreach (via the Skyspout updraft)   BELOW = Deep Shelf (bubble-coat dive)
          BESIDE = the Hollow (mirror world, via the Umbral Gate)
```

### Navigation gimmicks

| Gimmick | How it plays | Engine idea |
|---|---|---|
| **Lodestar compass** | A HUD needle on the world map points to the current bearing. Inside the Galeway it "sets" to a new island only after the current island's story beat (the recharge idea). At branch islands it shows 2–3 needles, and the player picks the order. | Sprite arrow plus a bearing table (§6) |
| **The Murk** | Fog banks in the Galeway hide islands. An island appears only when the Lodestar holds its bearing, or Vesper's lookout skill (Reveal) pierces the fog. | World-map metatile swap on load by flag (INFERRED standard map-script technique) |
| **Bearing Shards** | Collectible fixed pointers (Djinn-style hiding places, side quests) that each reveal one optional island in the Murk; all of them reveal the Last Bearing | Flags plus Murk swaps |
| **Stormwall** | A storm barrier at the Galeway's edge. The Rainbow Wing (Ho-Oh) parts it. | Ship-blocking behavior, cleared by flag |
| **Stillwaters** | Windless calm belts with leviathan-class sea encounters at high level. Only the Heartstone engine moves the ship; Surf is impossible. A soft danger gate, not a hard one. | Ship-only water behavior; tougher encounter table |
| **The Spine** | A continental wall, crossed three ways in story order: **(1)** Act II, the Ascending Locks (a river-stair of giant waterfalls and currents up and over the wall); **(2)** Act III, the Undertow Gate (an undersea tunnel in the Deep Shelf); **(3)** Act III, the sky. | Waterfall, Dive, and sky layer |
| **Rimfalls** | The world edge. The ship cannot sail over it, and strong currents push it back. Story islands near the edge erode between acts (map variants). | Same as GS: "you can't sail over it" ([Gaia Falls](https://goldensunwiki.net/wiki/Gaia_Falls)); current behaviors |
| **Sky layer (Cloudreach)** | The Skyspout updraft lifts the winged ship onto a sailable cloud sea, with sky isles and wind currents | World-map chunk with a sky map type |
| **Undersea layer (Deep Shelf)** | The bubble-coated ship sinks at marked deep-sea spots and sails the sea floor. Local Dive spots lead to on-foot underwater maps. | Dive connections; underwater map type |
| **Ship upgrades = crew roles** | Gunner: cannon breaks ice floes and rock walls. Shipwright: hull lets the ship sail up wide rivers. Lookout: sees through the Murk. Diver: bubble coat. Rival: Wings to fly over reefs and low land, and to enter the updraft. Navigator: reads the Lodestar. Doctor: rest aboard. | Ship upgrade flags (§6) |

Two of these are direct Golden Sun precedents:
- In The Lost Age, the Wings of Anemos let the ship fly briefly over land and water.
- The ship's cannon clears ice walls.

Sources: [Golden Sun Wiki: Lemurian Ship](https://goldensunwiki.net/wiki/Lemurian_Ship), and the Golden Sun Universe "Wings of Anemos" page summarised in the same search.

### Locations (29)

| # | Name | Type | Biome / setting | Sea or layer | Act | Main traversal |
|---|---|---|---|---|---|---|
| 1 | Hollowmere | Home village | Highland lakes, terraced farms | Dawnward Upper | I | Walk/run, Move |
| 2 | Mt. Keystone / Keystone Vault | **EARTH SITE** (prologue entry; full dungeon in Act IV) | Mountain caverns, then magma chamber | Dawnward Upper | I / IV | Move, Pound, Tremor, Scoop, Lift; rising-lava set piece |
| 3 | Delvers' Hollow | Mining town and mines | Quarries, steel works, rail tunnels | Dawnward Upper | I | **Minecarts**, cracked floors, Pound switches |
| 4 | Saltmarsh Reach | Route | River delta and reed marsh | Dawnward Upper | I | **Surf intro** (river), currents |
| 5 | Canalport | City | Canal city with tides; lower districts flood at high tide | Dawnward Upper | I | Surf in canals; day/night tide variants |
| 6 | Bastion Rock | Dungeon | Tidewarden sea fortress (prison break) | Dawnward Upper | I | Guard patrol timing, Blaze/Burst, Frost |
| 7 | Cinder Isle / Cinder Spire | **FLAME SITE** | Volcano, ash fields, fighting monastery, dragon cliffs, burned bell tower | Dawnward Upper | I | Parch/Blaze/Force, lava-flow timing, Lift |
| 8 | Keelhaven | Shipwright cove | Dry dock and the derelict Wayfarer | Dawnward Upper | I | **Ship obtained** |
| 9 | Stormwall | World feature | Perpetual thunderstorm barrier | Galeway edge | II gate | Ship + Rainbow Wing |
| 10 | Tradewind Bazaar | Town (hub) | Floating market of lashed ships | Galeway | II | Lash ropes between hulls, Catch |
| 11 | Eldergrove / Eldergrove Heart | **FOREST SITE** | Giant tree, canopy bridges, poison swamp, bug hive; past/present versions | Galeway | II | Growth, Lash, Catch; Celebi time-shift |
| 12 | Lantern Reef | Dungeon | Ghost-ship graveyard, fog, night-only areas | Galeway | II | Reveal, Halt, Cloak; day/night |
| 13 | Dunesea | Desert isle | Dunes, sand geysers, sandstorm, buried ruins | Dawnward Lower | II (optional) | **Sand** item reward, Scoop, quicksand |
| 14 | Frostfang Isle | Dungeon | Glacier, ice caves | Dawnward Lower | II (optional) | **Ice slides**, Frost, thin ice |
| 15 | Ironfist Arena | Town set piece | Colosseum tournament island | Dawnward Lower | II (optional) | Tournament; **Carry** reward |
| 16 | Thunderhead Atoll | Route | Storm plains, metal ruins | Galeway | II (optional) | Conveyor/spin tiles, **Hover** reward |
| 17 | Lockhaven / Ascending Locks | Town + dungeon | Giant water-stair up the Spine | The Spine | II→III | **Waterfall**, currents, Lift + Hover/Carry |
| 18 | The Pinnacle | Capital | Tidewarden city on top of the Spine | The Spine | III–IV | Infiltration: Cloak, Halt, Mind Read |
| 19 | Rimward Camps | Town | Refugee settlements at the edge | Duskward Upper | III | Story reveal; eroding variants |
| 20 | The Rimfalls | World feature | World-edge waterfalls | Edges | All | Ship pushed back by currents |
| 21 | Coralreach | Lagoon town | Coral lagoon, stilt houses | Duskward Lower | III | **Dive unlock** |
| 22 | Pearlhollow | Undersea city | Bubble-dome city | Deep Shelf | III | On-foot underwater; Deep Shelf hub |
| 23 | Kelpwood Trench | Undersea route | Kelp forests, vents, sunken ruins | Deep Shelf | III | Ship undersea, Dive, currents |
| 24 | Silverdeep Sanctum | **SEA SITE** | Ice caverns under the sea, fairy grottoes | Deep Shelf | III | Frost/Douse, Dive, Grind |
| 25 | Skyspout | World feature | Vertical updraft | Galeway (Duskward) | III | Winged ship rises to the Cloudreach |
| 26 | Aerie Monastery | Sky town | Sky isles, Psychic monastery | Cloudreach | III | Wind currents, Whirlwind/Cyclone |
| 27 | Stormspire | **SKY SITE** | Tower above the clouds | Cloudreach | III | Spin/wind tiles, Mind Read, Teleport pads |
| 28 | Umbral Gate / the Hollow | **SHADOW SITE** | Mirror world: inverted copies of earlier places | Hollow | IV | Reveal, Halt, Cloak; mirror puzzles |
| 29 | The Last Bearing | Postgame island | Ancient ruin | Hidden | Post | Everything |

---

## 3. Traversal variety

### Every way to move, and where it appears

| Method | Where | Engine basis |
|---|---|---|
| Walk / auto-run | Everywhere (auto-run is a DESIGN.md QoL item) | Existing |
| 8-way movement, or diagonal grid fallback | Everywhere. **Rule: every puzzle is grid-aligned** so both movement options work | Diagonal directions exist (`include/constants/global.h:212-215` VERIFIED) |
| Ledges and diagonal hops (GS pillar jumps) | Cinder Spire, Stormspire | `MB_JUMP_*` incl. NE/NW/SE/SW (`include/constants/metatile_behaviors.h:61-68` VERIFIED) |
| Ladders, climbable vines and walls | Eldergrove (Growth vines), Delvers' Hollow | `MB_LADDER` (`metatile_behaviors.h:102` VERIFIED); vine/wall climbing needs new behaviors |
| Tightropes (Lash) | Tradewind Bazaar, Eldergrove canopy | New behavior (INFERRED) |
| Ice sliding, thin/cracked ice | Frostfang, Silverdeep | `MB_ICE`, `MB_THIN_ICE`, `MB_CRACKED_ICE` (`metatile_behaviors.h:37,43,44` VERIFIED) |
| River and sea currents | Saltmarsh, Ascending Locks, Kelpwood, the Rim | `MB_*_CURRENT`, `MB_FAST_WATER` (`metatile_behaviors.h:49,85-88` VERIFIED) |
| Wind and conveyor tiles | Stormspire, Thunderhead | `MB_SPIN_*` (`metatile_behaviors.h:89-93` VERIFIED) |
| Deep sand, quicksand, mud slopes | Dunesea | `MB_DEEP_SAND`, `MB_SAND`, `MB_MUDDY_SLOPE` (`metatile_behaviors.h:11,38,213` VERIFIED) |
| Cracked floors (fall to the floor below) | Keystone Vault, Lantern Reef | `MB_CRACKED_FLOOR`, `MB_CRACKED_FLOOR_HOLE` (`metatile_behaviors.h:107,215` VERIFIED) |
| Multi-level bridges | Canalport, Eldergrove | `MB_BRIDGE_OVER_POND_*` (`:118-130`); 16 elevation levels (`include/global.fieldmap.h:9`) VERIFIED |
| **Minecarts** | Delvers' Hollow, Keystone Vault | Scripted ride first (`src/cable_car.c` is a precedent, VERIFIED to exist); a player-driven version could reuse the rail behaviors `MB_*_RAIL` (`:216-219` VERIFIED) |
| Ferries (before the ship) | Act I | `src/seagallop.c` ferry precedent (VERIFIED exists) |
| **Surf** (rivers, lakes, coastal shallows only) | Saltmarsh, Canalport canals, Eldergrove pools, lagoons | Existing Surf plus a terrain rule (§6) |
| **Waterfall** | Ascending Locks; backtrack spots in Acts I–II | Existing; north-only (§6) |
| **Dive** (on foot) | Coralreach, Kelpwood, Act I/II backtrack spots | Existing Dive code (§6) |
| **Ship** (open sea) | World map, all seas | New (§6) |
| Ship: cannon, hull (rivers), Murk sight, bubble coat, Wings | Acts II–IV | Ship upgrade flags |
| Sky sailing | Cloudreach | New layer |
| Undersea sailing | Deep Shelf | New layer |
| Teleport | Late Act IV (DESIGN.md: "Teleport comes late", `DESIGN.md:88`) | Fast travel plus teleport pads |
| Retreat / Escape Rope | Dungeons | DESIGN.md `:94` |
| Field Psynergy that changes terrain | Move, Pound, Tremor, Scoop, Blaze, Burst, Force, Parch, Frost, Douse, Growth, Lash, Catch, Whirlwind, Cyclone, Reveal, Cloak, Halt (DESIGN.md `:83-90`) | Field Psynergy investigator's scope |
| Item Psynergy | Lift, Carry, Hover, Grind, Sand (DESIGN.md `:92`) | As progression keys, see below |
| Tides / night-only paths | Canalport, Lantern Reef | Day/night tint and times of day (`include/config/overworld.h:92-102` VERIFIED) |
| Past/present versions | Eldergrove (Celebi) | Map variants by flag (content, not engine) |
| Mirror world | The Hollow | Mirrored copies of earlier maps (cheap content reuse) |

### Gating order (open-ish)

```
ACT I (linear)
 Hollowmere ─Move─► Delvers' Hollow (minecarts) ─► Saltmarsh [SURF unlocked: story event]
  ─► Canalport ─► Bastion Rock [+Tamsin: Blaze/Burst/Force/Parch]
  ─► Cinder Spire (FLAME) ⇒ Heartstone (ship), LIFT item, Rainbow Wing ─► Keelhaven: sail

ACT II (any order)            Rainbow Wing parts the Stormwall
 Lodestar: 3 bearings ─┬─ Tradewind Bazaar [+Wynn]
                       ├─ Eldergrove (FOREST) [+Sorrel] ⇒ WATERFALL unlocked, Growth backup
                       └─ Lantern Reef [+Vesper] ⇒ Murk sight
 Free-sail optional isles (any order): Dunesea ⇒ SAND · Ironfist ⇒ CARRY
                                       Thunderhead ⇒ HOVER · Frostfang ⇒ Frost backup
 GATE to Act III: Ascending Locks needs WATERFALL + LIFT + (HOVER or CARRY)

ACT III (Sea and Sky in either order)
 Rimward Camps (story) ─► Coralreach [+Nerissa] ⇒ DIVE unlocked, ship bubble coat
    ─► Deep Shelf ─► Silverdeep (SEA) ⇒ GRIND, Silver Wing
 Corvin's arc ⇒ [+Corvin], ship Wings ─► Skyspout ─► Cloudreach ─► Stormspire (SKY) ⇒ Teleport (Wynn)

ACT IV
 The Pinnacle (infiltration) ─► Keystone Vault (EARTH; Red Orb / Primal Groudon)
   ─► Umbral Gate (needs Silver Wing to calm the edge maelstrom) ─► the Hollow (SHADOW; Giratina) ─► end
```

**Design rules that keep it open-ish:**
1. In Act II, an island's *mandatory* puzzles use only:
   - Act I Psynergy (Earth, Sea, Flame);
   - the island's own recruit;
   - items obtainable before that island.
2. Every group Psynergy needed on a mandatory path has a backup item. This follows DESIGN.md's rule that no puzzle requires one specific Adept (`DESIGN.md:79`). Examples: Sprout Seed (Growth), Truth Lens (Reveal), Rime Shard (Frost), Gust Fan (Whirlwind), Ember Flint (Blaze), Rain Drop (Douse).
3. Gates ask for "N keys from a pool" where possible, as at the Locks.
4. **Backtracking rewards:** place Dive spots, Waterfalls, Sand pits, Hover gaps and Grind rocks in Act I/II maps. They hide Djinn-style Pokémon, Bearing Shards and items, as Golden Sun's revisits do. Golden Sun used item Psynergy as hard keys (Orb of Force, Cloak Ball, Burst Brooch) and also as conveniences ([Golden Sun Wiki: utility Psynergy items](https://goldensunwiki.net/wiki/List_of_Utility_Psynergy_items)).

---

## 4. Settings variety

| Region | Biomes | Set pieces | Weather (existing in engine) |
|---|---|---|---|
| Hearthland (Earth) | Highland lakes, quarries, mines, mountain caverns, magma chamber | Prologue quake splits the village; Act IV rising lava and Primal Groudon; minecart chase | Sunny, drought (Act IV) |
| Dawnward Isles | Marsh delta, canal city, sea fortress, fishing villages | Canal city floods at high tide; prison break; ferry crossings | Rain, downpour |
| Cinder Isle (Flame) | Volcano, ash plains, fighting monastery, dragon roost cliffs, burned bell tower | Rimborn ignite the Spire; Ho-Oh's rainbow; monastery trial battles | Volcanic ash |
| Galeway | Storm seas, floating bazaar, giant tree, ghost-ship reef, storm atoll | Stormwall parting; bazaar heist; ghost-ship captain boss | Thunderstorm, fog |
| Eldergrove (Forest) | Canopy, roots, poison swamp, bug hive | Celebi past/present: the same grove 500 years ago | Shade, fog |
| Dawnward Lower | Desert, glacier, colosseum | Sandstorm chase for Weyard Gible; tournament arc | Sandstorm, snow (`src/field_weather.c:134` has a working snow handler, VERIFIED) |
| The Spine | Water-stair locks, wall-top capital | Climbing the waterfalls; infiltrating the Pinnacle | Rain |
| Duskward / Rim | Crumbling cliffs, refugee camps, edge waterfalls | Truth reveal; an island collapses between acts | Shade |
| Deep Shelf (Sea) | Kelp forest, vents, sunken city, undersea ice caves, fairy grottoes | Bubble-coated ship descent; Lugia in the trench | Underwater bubbles |
| Cloudreach (Sky) | Cloud sea, sky isles, monastery, storm tower | Updraft launch; Rayquaza's descent to stop Primal Groudon (Act IV) | Thunderstorm; cloud BG needs new work |
| The Hollow (Shadow) | Inverted, discoloured copies of earlier places | Mirror versions of past puzzles; Giratina; final boss | Fog |

The weather list is VERIFIED in `include/constants/weather.h:6-26`.

**Town cultures between sites,** so towns don't repeat: highland village, mining town, canal city, fortress, shipwright cove, floating bazaar, tree village, desert caravanserai, colosseum town, wall-top capital, refugee camp, lagoon stilt-town, bubble-dome city, sky monastery.

---

## 5. Adepts, legendaries and the popular 10

### The 8 Adepts (names are placeholders)

| Adept | Group | Joins | Island arc | Crew role / ship upgrade | Suggested starting partner |
|---|---|---|---|---|---|
| Hero (player-named, default "Arlen") | Earth | Start | Prologue | Captain | Player's choice of Weyard Bulbasaur, Charmander or Squirtle; or Weyard Eevee |
| Maren | Sea (healer 1) | End of prologue | Lake shrine | Doctor: rest aboard to heal | Weyard Eevee → Sylveon (Fairy fits the Sea group) |
| Tamsin | Flame | Act I (Bastion Rock) | Deserting Tidewarden cadet | Gunner: cannon breaks ice and rock | Weyard Riolu → Lucario |
| Wynn | Sky | Act II (Tradewind Bazaar) | Cartographer in debt | Navigator: Lodestar; later Teleport | Weyard Ralts → Gardevoir/Gallade |
| Sorrel | Forest | Act II (Eldergrove) | Tree-village outcast | Shipwright: hull to sail up rivers | Weyard Rowlet → Decidueye |
| Vesper | Shadow | Act II (Lantern Reef) | Last of the clan who sealed the Umbral Gate | Lookout: sees through the Murk | Weyard Froakie → Greninja, or Gastly → Gengar |
| Nerissa | Sea (healer 2) | Act III (Coralreach) | Pearl-diver from the lagoon | Diver: bubble coat | Weyard Totodile or Mudkip line |
| Corvin | Earth (rival/co-lead) | Act III (after the Rimborn duo falls) | Travelled with the Rimborn; Felix-like | Ship Wings | Weyard Larvitar → Tyranitar (Rock/Dark scores toward Earth) |

### The six legendaries

| Legendary | Site | Story role | Canon hook |
|---|---|---|---|
| Ho-Oh | Cinder Spire | Wakes when the Rimborn ignite the Spire. It judges the party and grants a Rainbow Wing, which parts the Stormwall. | Rainbow Wing: new key item (no `ITEM_RAINBOW_WING` constant found in `include/constants/items.h`, VERIFIED by grep) |
| Celebi | Eldergrove Heart | Time-shifts the grove between past and present; shows the original sealing | — |
| Lugia | Silverdeep Sanctum | Guards the deep. Its Silver Wing calms the edge maelstrom around the Umbral Gate. | Silver Wing: new key item |
| Rayquaza | Stormspire | Descends in Act IV to stop Primal Groudon | Canon: quells Groudon |
| Groudon | Keystone Vault | The Grand Warden uses the Red Orb to make it Primal and raise the Spine | `ITEM_RED_ORB` exists (`include/constants/items.h:379` VERIFIED); Primal Groudon is in DESIGN.md's Weyard Megas (`DESIGN.md:136`) |
| Giratina | Umbral Gate / Hollow | The Hollow is its domain. The Warden flees there; final dungeon. | `ITEM_GRISEOUS_ORB` exists (`include/constants/items.h:503` VERIFIED) |

**How a legendary joins (options):**
- (a) DESIGN.md's "Battle first" Djinn-style encounter (`DESIGN.md:70`);
- (b) a normal Poké Ball catch;
- (c) it becomes a top-tier Summon unlock in its group.

### Popular-10 Weyard families: role options

| Family | Option A | Option B |
|---|---|---|
| Froakie → Greninja | Vesper's partner (Water/Dark covers Sea and Shadow) | Tidewarden spymaster's ace |
| Riolu → Lucario | Tamsin's partner; Weyard Mega Lucario | Ironfist Arena champion's ace |
| Mimikyu (Djinn costume, `DESIGN.md:144`) | Hidden encounter in Lantern Reef (needs Reveal) | Crew mascot that follows the party |
| Eevee → Umbreon / Sylveon | Hero's first companion | Maren (Sylveon) and Vesper (Umbreon) |
| Gible → Garchomp | Dunesea chase encounter (needs Sand) | Rimborn duo leader's ace; Weyard Mega Garchomp |
| Ralts → Gardevoir / Gallade | Wynn's partner | Aerie Monastery guardian |
| Gastly → Gengar | Umbral Gate guardian | Ghost-ship captain boss at Lantern Reef |
| Larvitar → Tyranitar | Corvin's partner; Weyard Mega Tyranitar as rival ace | Grand Warden's ace |
| Rowlet → Decidueye | Sorrel's partner | Eldergrove guardian |
| Starter families (9) | Pick 1 of 3 (Bulbasaur, Charmander or Squirtle lines) | The other 6 as hidden Djinn-style finds by theme: Chikorita (Eldergrove), Cyndaquil (Cinder), Totodile (Deep Shelf), Treecko (Cloudreach), Torchic (Ironfist), Mudkip (Ascending Locks marsh) |

---

## 6. What the world structure demands from the engine (phases 1–2)

### 6.1 Map layers and map types

| Need | Engine fact | Status |
|---|---|---|
| Layers: **Surface** (local maps plus world map), **Deep Shelf**, **Cloudreach**, **Hollow** | `mapType` is a u8 in `MapHeader` (`include/global.fieldmap.h:236`). Existing types include `MAP_TYPE_UNDERWATER` and `MAP_TYPE_OCEAN_ROUTE` (`include/constants/map_types.h:6-15`). | VERIFIED |
| New types: **`MAP_TYPE_WORLD`** (ship, sea encounters, small-scale tiles) and **`MAP_TYPE_SKY`**. The Hollow can be a normal type plus weather/palette. | Adding enum values is cheap. The header also has 2 unused flag bits (`global.fieldmap.h:246`), usable for things like "ship allowed". | VERIFIED (fields); INFERRED (approach) |
| Height within a map (bridges, pillars, multi-level dungeons) | 16 elevation levels per tile (`global.fieldmap.h:9`); 3 BG layer types per metatile (`:52-56`) | VERIFIED |

### 6.2 World-map scale

- **Per-map size limit:** `(width+15) × (height+14) ≤ 10240` cells.
  - Check: `src/fieldmap.c:170-173`.
  - Constants: `include/fieldmap.h:15,23-25`.
  - VERIFIED.
  - Example chunk: 96×64 metatiles uses 111×78 = 8,658 cells, which fits.
- **Proposed layout, about 10 world chunks:**
  - Surface: 6 chunks (Dawnward/Duskward × Upper/Galeway/Lower);
  - Deep Shelf: 2;
  - Cloudreach: 1–2.

  Chunks link with normal N/S/E/W connections (`include/constants/global.h:219-227`, VERIFIED).
- **Connected maps are drawn with the current map's tilesets.** `FillConnection` copies the neighbour's metatile IDs (`src/fieldmap.c:232-240`), while tiles and attributes come from `gMapHeader` (`fieldmap.c:485-516, 1012-1022`). VERIFIED code; the conclusion is INFERRED. **So every chunk in one layer must share one tileset pair.**
- **Town/fly map:** a 28×15 grid (`src/region_map.c:42-43`) with switchable pages. FRLG has Kanto plus 3 Sevii pages (`region_map.c:350-370`, `src/regions.c:5-52`). Proposal: 4 pages (Dawnward, Duskward, Cloudreach, Deep Shelf).
  - Map-section ids are u8 (`global.fieldmap.h:234`); 209 are defined now (`src/data/region_map/region_map_sections.json`).
  - The new region replaces them, so there is plenty of room.
  - VERIFIED.

### 6.3 Ship mechanics

| Need | Engine fact | Status |
|---|---|---|
| A "ship" avatar state, and later "minecart" | `PlayerAvatar.flags` is a **u8 with all 8 bits used**: foot, mach bike, acro bike, surfing, underwater, controllable, forced move, dash (`global.fieldmap.h:348-355, 412`). Options: repurpose the two bike bits (the GS design has no bikes) or widen to u16. **Decide in phase 1, alongside the movement work.** | VERIFIED |
| Restore the state on load | `GetAdjustedInitialTransitionFlags(..., metatileBehavior, mapType)` (`src/overworld.c:190`) rebuilds surfing/underwater from the tile and map type. Add "world map + water tile ⇒ ship". | VERIFIED signature; INFERRED approach |
| Water classes: Surf-ok (river, lake, shallows) vs ship-only (ocean, deep); reef (needs Wings); Stillwater; Stormwall; Murk; updraft; dock | 240 behaviors are defined (`metatile_behaviors.h:5-244`, counted). `MB_INVALID = UCHAR_MAX` (`:248`). Emerald-format attributes are 8-bit (`global.fieldmap.h:39`), leaving **15 free values**. FRLG-format layouts use 9 bits (`global.fieldmap.h:43`, `src/fieldmap.c:85`), and layouts carry an `isFrlg` switch (`fieldmap.c:57, 412-422`). About 80 names are Hoenn/Kanto-specific or unused (secret base, trick house, gyms…) and can be repurposed. | VERIFIED |
| Anchored ship (disembark on the world map, ship stays) | Object event at saved coordinates: 2–3 vars | INFERRED |
| Sea encounters, plus "hover to avoid" | In The Lost Age, hovering on the world map avoided monster encounters ([Lemurian Ship](https://goldensunwiki.net/wiki/Lemurian_Ship)). Map that to the Avoid/Repel effect. | VERIFIED (GS); INFERRED (port) |
| Currents pushing the ship (Rimfalls, maelstrom) | Current behaviors exist for surfing (`metatile_behaviors.h:85-88`); the ship would reuse them | INFERRED |

### 6.4 Water field moves

| Need | Engine fact | Status |
|---|---|---|
| Surf checks Set Pokémon that *can learn* it | `PartyHasMonWithSurf` loops the 6-slot party and requires `MonKnowsMove(MOVE_SURF)` (`src/field_player_avatar.c:1616-1630`). Rewrite against Set storage and a can-learn test. | VERIFIED |
| Waterfall | Works only while surfing **north** (`field_control_avatar.c:653`, `field_player_avatar.c:1633-1639`). **Level-design rule: waterfalls climb up the screen**, or the code must be extended (relevant if free 8-way movement lands). | VERIFIED |
| Dive / undersea | Shared code, **not FRLG-gated**: `TrySetupDiveDownScript` / `TrySetupDiveEmergeScript` (`src/field_control_avatar.c:661-681`, `1221-1235`), `SetDiveWarp` (`src/overworld.c:865-870`), `CONNECTION_DIVE/EMERGE` (`include/constants/global.h:226-227`; `src/fieldmap.c:880`). | VERIFIED |
| Dive implications | **Corrected after review:** the FireRed ROM links only the 41 Kanto (`*_Frlg`) map groups and no Hoenn ones (checked in `pokefirered.map`). `include/constants/map_groups.h` is a committed header that lists both regions, so it doesn't show what gets built. So the FireRed build has no working Dive example maps; the first dive spot is new content (see WATER_MOVES.md). Dive passes x,y through, so each underwater map must line up with its surface map's coordinates (same size or aligned area). A ship dive at open-sea spots (a DESIGN.md open question, `:188`) is the same mechanism between world chunks. | INFERRED |
| Unlock by story flag rather than badge | `gFieldMoveUnlocks` supports only `CANT_UNLOCK`, `ALWAYS_UNLOCKED`, `BADGE_UNLOCK` (`include/field_move.h:13-19`; `src/field_move.c:31-41`). Surf, Dive and Waterfall are badge-mapped (`field_move.c:86-119`). Add a `FLAG_UNLOCK` type (about 30–60 lines), or map site flags to badge flags. | VERIFIED |

### 6.5 Budgets that affect level design

- **Objects:** 16 active object events (`include/constants/global.h:95`) and 64 templates per map (`:100`), VERIFIED.
  - These slots are shared by pushable pillars, Djinn-style encounters, NPCs, and overworld wild encounters (`WE_OW_ENCOUNTERS`, `include/config/wild_encounter.h:20`).
  - **Rule:** about 10 movable objects or fewer per screen. Prefer metatile-swap puzzle elements.
- **Flags:**
  - The FRLG layout has `FLAGS_COUNT = 0x900` (`include/constants/flags_frlg.h:1492`).
  - The Emerald layout has 375 `FLAG_UNUSED_*` (`include/constants/flags.h`).
  - The new region frees most Hoenn/Kanto story flags.
  - Rough need (INFERRED): about 300 hidden items + about 150 Djinn-style encounters + about 200 story/puzzle/Murk/Bearing flags, which is roughly 650.
- **Other helpers that already exist:**
  - map preview screens for site intros (`include/config/map_preview_screen.h`);
  - follower NPCs, which could show a crewmate (`include/config/follower_npc.h:5`);
  - day/night tint for tides and night isles (`include/config/overworld.h:102`).

  VERIFIED.
- **Native-port friendliness (INFERRED):** keep world data as data tables (JSON → C) rather than hard-coded scripts, so a later native app can reuse it. That covers the island table, bearings, unlock graph, ship-upgrade flags and encounter tables. The 10,240-cell chunk limit is GBA-only; a chunked world design ports cleanly.

### 6.6 Effort (world-structure engine work only)

This excludes the 8-way movement, field Psynergy and Set storage, which other investigators cover.

| Work item | Files / functions | ~Lines | Calendar | Confidence |
|---|---|---|---|---|
| `FLAG_UNLOCK` for field moves; Surf/Dive/Waterfall checks against Set Pokémon | `field_move.c/.h`, `field_player_avatar.c` (`PartyHasMonWithSurf`), `field_control_avatar.c` | 80–150 | 1–2 days (after Set storage exists) | High |
| Limited-Surf terrain rule | `metatile_behavior.c` (surfable checks), `field_control_avatar.c` | 50–100 | 1–2 days | High |
| Ship avatar: board, disembark, movement, sprite, save/restore, anchored ship | `field_player_avatar.c`, `field_control_avatar.c`, `overworld.c` (`:190`), `event_object_movement.c`, object graphics, scripts | 600–1,000 | 2–3 weeks | Medium-low |
| Ship upgrades and world obstacles (reef, Stillwater, Stormwall, cannon targets, Murk) | `metatile_behavior.c`, map scripts, flags | 200–400 | ~1 week | Medium |
| Lodestar HUD and bearing table | New `src/lodestar.c`, sprite, data table | 250–400 | 3–5 days | Medium |
| World map type: encounters, music, name pop-ups, region-map pages | `map_types.h`, `wild_encounter.c`, `overworld.c`, `region_map.c`, `regions.c` | 150–300 | 3–5 days | Medium |
| Undersea world and ship dive at sea spots | Dive connection paths above | 150–300 | 3–5 days | Medium |
| Sky layer: updraft transition, sky map type, cloud BG | `overworld.c`, `field_weather*.c` or BG code, scripts | 200–400 | ~1 week | Low-medium |
| Minecart: scripted (A) vs player-driven on rails (B) | Scripts / `field_player_avatar.c` | A: ~0 code; B: 300–500 | A: 1–2 days; B: 1–1.5 weeks | A high; B low |

**Total: roughly 6–9 calendar weeks** of AI-assisted engine work for the world structure. Confidence is medium-low.

**What would change the estimate:**
- Free 8-way movement means ship and minecart movement must be rewritten for it (+1–3 weeks).
- If the hero can walk on the world map Golden Sun-style, rather than world-map-is-ship-only with towns as warps, add +1–2 weeks.
- A full sailable Cloudreach vs a few sky maps.
- Reusing Emerald's underwater tilesets vs building new ones.

**Content dominates the schedule** (INFERRED):
- 29 locations come to about 250–350 maps: towns with interiors, 6 multi-floor sites, 20–30 routes, about 10 world chunks, 10–20 underwater maps.
- At about 1–3 hours per placeholder map with events and scripts, that is about 400–900 hours, or 6–12+ months part-time. Confidence is low.
- The biggest variable is who draws the maps: the user in Porymap, or Claude generating layouts by script, which is fast but crude.
- **Recommendation:** build an **Act I vertical slice** (locations 1–8, about 40–60 maps, ship launch included) as the proving ground. That is about 4–8 weeks after the phase 1–2 systems exist.

---

## 7. Questions for you to decide

1. **Tone:** lighthearted adventure (One Piece) or Golden Sun's earnest, morally grey tone? Or the proposed mix?
2. **World shape:** is the Spine × Galeway cross with sky, undersea and mirror layers right, or do you want a simpler single archipelago?
3. **Rival:** should Corvin get a playable perspective chapter, like The Lost Age switching to Felix? (More content.)
4. **Openness:** is "3 arcs in any order" in Act II and "Sea or Sky first" in Act III the right amount of freedom?
5. **Water-move unlocks:** Surf by story event in Act I, Waterfall after the Forest site, Dive at Coralreach in Act III. Agree? And should the ship dive at marked open-sea spots?
6. **World-map walking:** can the hero walk on the world map (Golden Sun style), or is the world map ship-only with towns as warps? (A big engine-scope difference.)
7. **Sky layer depth:** a full sailable Cloudreach, or a handful of sky maps reached by updraft?
8. **Legendaries:** do they join by "battle first" Djinn-style, by Poké Ball, or as Summon unlocks? Can they be Set Pokémon?
9. **Starter:** pick 1 of 3 Weyard Gen 1 starters, or Weyard Eevee as the hero's first partner?
10. **Popular-10 roles:** choose A or B per family in the §5 table.
11. **Minecarts:** scripted rides, or player-driven rails?
12. **The Hollow:** are mirrored copies of earlier maps acceptable as the final world?
13. **Names:** keep these placeholders as working names, or supply your own?
14. **Postgame:** do you want the Last Bearing island and Bearing Shards?

### Sources
- `DESIGN.md` (lines cited inline)
- [Golden Sun Wiki: Lemurian Ship](https://goldensunwiki.net/wiki/Lemurian_Ship)
- [Golden Sun Wiki: List of Utility Psynergy items](https://goldensunwiki.net/wiki/List_of_Utility_Psynergy_items)
- [Golden Sun Wiki: Gaia Falls](https://goldensunwiki.net/wiki/Gaia_Falls)
- [Golden Sun Universe: Lemurian Ship](https://goldensun.fandom.com/wiki/Lemurian_Ship) and [Wings of Anemos](https://goldensun.fandom.com/wiki/Wings_of_Anemos) (search summary only; direct fetch returned HTTP 402)
- Expansion source files cited as `path:line` (repository root `expansion/`)