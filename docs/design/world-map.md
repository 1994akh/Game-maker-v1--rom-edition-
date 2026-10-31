# Halcyra: the world map

**Decided, 24 Oct** (open questions 74 to 92, every one as recommended). This page settles how the whole world is laid out, so the rooms can be joined up once and never
remapped. It covers Act I in detail and Act II, the layers and the postgame in outline. The room connections are
redone against it in the next step, not here.

You answered all nineteen questions on the decision page on 24 Oct, each as recommended, so everything here stands.
Each section names the question it builds on, in **bold**; its recommended answer is the one you chose.

The picture is `world-map/world-map.png`: the whole world on the left, the Calm and Act I on the right, and Marrow
Isle at the bottom. It is drawn from scratch from the numbers on this page (shapes and labels only, no game art), so it
can go in the public repo. The same numbers are in `world-map/world-layout.json`, and `world-map/draw_world_map.py`
redraws both.

**Your two notes of 24 Oct, built in here:**
1. "We also need areas to explore and grind for EXP, items, money, easter eggs and our side quests, not just the
   story." That is §4.
2. "If something does not work for the map right now and we do not have an alternative, you may generate those to fit
   our needs. The local maps have multiple entrances like doors, steps from a basement or cave, and villages and cities
   will have multiple local map scenes. Go as big as you need to." That is §3 (every place as scenes, with every
   entrance) and §5.5 (what we generate ourselves).
3. "One adult-only town that is only accessible in adult mode. A hidden area hinted at in rumours." That is §4.5.

**Already decided, and built on here:**
- The Lost Age's world map and sailing, with the ship handling open sea (decision log 45).
- Walk Meridia and the large islands on the world map, sail between them, and enter small islands straight from the
  ship (decision log 49).
- Map changes at the midpoint and after the ending are switched by story flags, with no timer (decision log 50).
- The airship flies on its own layer and lands only on marked pads (decision log 51).
- The Cloudreach and the Deep Shelf are each about a quarter of the Wide (decision log 52). The Hollow is recoloured
  copies of earlier rooms (decision log 53).
- Surf only on rivers, lakes and coastal shallows, for short hops. Deep sea needs the ship (decision log 44).
- The demo's Calm is sailable, built from The Lost Age's world-map pieces, with a parchment Chart (demo 27).
  Meridia's walkable map, Dustplain, Frostmarch, Hushwater and Twin Bells come after the demo (demo 19).
- Stonehollow's west gate and Canalport's south road stay shut until our own world map exists (progression 4).
- Lantern Reef is north-west of Meridia (menus N-11). Far landmarks get edge markers on the world map (menus N-10).
- Only puzzles, story and strong monsters block a route. No invisible walls, no level scaling (story.md §2).

## 1. The whole world

### 1.1 The shape

Halcyra is rings around one continent. From the middle out:

1. **Meridia**, the continent, with **the Spine** running down its middle and **the Pinnacle** on its highest peak.
   The Pinnacle is the exact centre of the world.
2. **The Calm**, a gentle inner sea, about 800 pixels wide, with a ring of islands.
3. **The Galeway**, a permanent storm ring, about 450 pixels thick.
4. **The Wide**, the outer sea, in four quarters, about 1,400 pixels wide.
5. **The Rimfalls**, the world's edge, a band of white water pouring away into mist.

The rim isn't a perfect circle. **In the east it has eaten deep into the Wide**, so the falls come in almost to the
storm. That bite is where the rim towns fell, one by one: Hale's Point, Gullstone, Kettle Bay, then Saltcombe. Fallhaven
stands at its inner end (question **Fallhaven, the storm and the Bazaar**).

Above and below are two **layers**, each its own map: **the Cloudreach** (a cloud sea above the north and north-east)
and **the Deep Shelf** (a sea floor below the south and south-east). **The Hollow** sits beside the world, reached only
through the Vault. **The Farside** lies beyond the rim, for the postgame.

From anywhere, "toward the Pinnacle" is the centre and "toward the falls" is the edge, as story.md wants.

### 1.2 Meridia

The Spine runs **north to south** down the middle (question **The Spine and the Pinnacle's river**). Its four regions sit
around it:

| Region | Where | What it is | Stars |
|---|---|---|---|
| **Frostmarch** | The north, beyond the Spine's north end | Tundra, ice caves, the monasteries, the Frozen Saint's glacier | ★★★ |
| **Brightcoast** | The east of the Spine | Farms, canals and the delta. Canalport and Saltmarsh Reach. The Doduo ranch (Act II) | ★ |
| **Dustplain** | The south, beyond the Spine's south end | Desert, sand geysers, the mines, the oasis of "Water Rights" | ★★ |
| **The Greenwild** | The west of the Spine | Forest, the giant tree, the Sourmire swamp | ★★ |
| **The Spine** | Down the middle | Peaks reached only by air (the Gem Sentinels). The Pinnacle on top | ★★★★★ / ★★★★ |

- **Size:** about 2,200 pixels east to west and 2,500 north to south. A hero running on the world map crosses it in
  under a minute.
- **The Pinnacle** stands on the Spine's highest peak at the world's centre. You can see its spire from almost
  anywhere, and the world map shows an edge marker when it is off screen. It is closed by story until Act III.
- **Rivers.** Three wide rivers run from the Spine to the sea. The living hull sails them from mission 14 (story.md §8).
  - **The Crownwater** runs east from the Pinnacle's foot to the sea at Canalport. The order keeps it with locks. Its
    ships pass Canalport's locks with a Pinnacle pass and sail up to **Crown Landing**, a river port under the peak.
    That's how the Tidewardens "rule the sea lanes from the Pinnacle", and how Ilse "sails for the Pinnacle". Nobody
    else gets through until Act III.
  - **The Eldwater** runs west through the Greenwild to the sea at the Eldergrove. The village's river landing is at
    its mouth, with the Tidewarden **coast post** (where the Greenwild pays its seed and sap) beside it.
  - **The Rimewater** runs north through Frostmarch to its north coast. Its upper reach freezes.
  - Dustplain has a dry river bed and one oasis, no sailable river.
- **Coasts.** In the demo, Meridia's coast is seen from the sea but has only two landings: Canalport and the
  Eldergrove's river landing. When Meridia's walkable map comes, its beaches become landings too.

### 1.3 The Calm

The Calm is a ring of sea between Meridia's coast and the storm. Its islands, clockwise from the north:

| Place | Where (from the Pinnacle) | Act I | Later |
|---|---|---|---|
| **Hushwater** | North-north-east, off Frostmarch's coast | A rumour ("?") on the Chart in the demo. Built after it | Island of the week, "The Silent Isle" (★) |
| **Bellstone** | North-east | Open sea | Rises at the Breaking (★★★) |
| **Marrow Isle** (home) | East-north-east, close to the storm's inner edge | Home from mission 1 | Grows into the base (§8 of story.md) |
| **Tortell's isle** | Inside Marrow Isle's reef lagoon | Seen, not reachable: the reef stops the Kestrel | Master Tortell, from the Wayfarer's first trip (mission 10) |
| **Cockle Cay** | East, south of Marrow Isle | Wild islet, open from mission 4 | Sinks at the Breaking (question **The three isles that sink**) |
| **Saltmarsh Reach** | East, the tidal bay in front of Canalport | The way in to Canalport, with reed islets | Partly drowned at the Breaking |
| **Canalport** | Meridia's east coast, at the Crownwater's mouth | Mission 3 onward | Lower town flooded (a Dive area), upper town opens |
| **Farer's Step** | South-east | Open sea | Rises at the Breaking (★★★★) |
| **Twin Bells** | South-east, between Canalport and Embral | A rumour on the Chart in the demo | Island of the week, "Low Tide" (★★) |
| **The Churn** | South, a whirlpool near the storm | Seen | A sea grotto behind it, opened with Whirlpool |
| **Embral Isle** | South, near the storm's inner edge | Crew 2 only (mission 4). Ringed by the tithe fleet's cutters after the fire | Ho-Oh's caldera (Act II) |
| **Shelfback** | South-west of Embral | Open sea | Rises at the Breaking: "the risen isle south-west of Embral" (§9b) |
| **Sandmere** | South-west | Wild islet (after the demo) | Sinks at the Breaking |
| **Bastion Rock** | West, off the Greenwild's coast | Crew 2 only (mission 7). The sea-gate turns other ships away | The order's fortress, on war footing |
| **The Eldergrove** | Meridia's west coast, at the Eldwater's mouth | From Ilse's letter after mission 4 | Mission 14, past and present |
| **Lantern Reef** | North-west, inside the north fog | Once Vesper is hired (mission 6) | Bonewhistle's ghost-ship room (Act II) |
| **Nightmarket Isle** (adult mode only) | North-west, deep in the fog beyond Lantern Reef | Not on the map. Rumours only | In adult mode, Vesper's second lane after mission 6 (§4.5) |
| **Driftholm** | North, east of the fog | Wild islet (after the demo) | Sinks at the Breaking |

- **The north fog** lies over the north-west Calm, drifting in from Westgloam through the storm. It hides Lantern
  Reef. North of Bastion Rock, it is where "no Tidewarden ship likes to follow".
- **Puzzle gates in the Calm** (story.md §2: "a few whirlpools and reefs"): Marrow Isle's reef (a Rimborn pilot, from
  mission 10), the north fog (a fog pilot, from mission 6), and the Churn (Whirlpool, Act II).

### 1.4 The Galeway

- **A ring of storm** about 450 pixels thick, between the Calm and the Wide. Its inner edge runs close past Marrow Isle
  in the east and Embral in the south.
- **Act I:** only Rimborn skiffs know its lanes. The lanes wind inside the storm, which is why a crossing takes two
  days though the ring isn't wide. On the map it is a storm wall that turns any ship back with a line (question **What
  keeps you out in Act I**).
- **The relay and "the eye".** The Galeway relay, the Crown's main conduit, sits inside the storm due east of Marrow
  Isle, in a calm pocket at the storm's heart: the eye. It is on the maiden voyage's way to the Narrows, which is
  why Hask's lamp waits there. At the Breaking it is blown. After that the eye is a knot of storm round a ruined
  island that only the airship can reach (story.md §8's "island inside the old Galeway eye").
- **Act II:** the ring breaks into storm fragments with lanes between them and strong monsters (★★★★). **The
  Skyspout**, the dead updraft of mission 17, stands in the broken ring to the north-north-east, under the Cloudreach.

### 1.5 The Wide

Each quarter is centred on the compass point it is named for (question **The four quarters of the Wide**).

| Quarter | Look | Places |
|---|---|---|
| **Northreach** (north) | Pack ice, aurora, sky | **The Stormspire**, a Farer tower on a rock due north, its top above the clouds (mission 19). **The lighthouse-court** (mission 13), with the four warriors' statue. **Thunderhead Atoll** (★★★★, "The Sentinel"), to the north-north-west. **The Speakers' isle** ("The Speakers of Tanarra"), to the north-east |
| **Eastwater** (east) | Rim towns and trade | **The Tradewind Bazaar**, in the open water north of the bite. **Fallhaven** at the bite's inner end, on the Fallhaven Narrows. The lost rim towns along the bite. **Ironfist Arena** (mission 15, the Glimmer Saucer), south of the bite. **Clockwork Key** ("Tuesday Again"), further south. The sea where Wynn fell, near the Bazaar |
| **Southdeep** (south) | Coral and deep water | **Silverdeep**, the giant whirl with its lighthouse, south-east (mission 18, the Deep Shelf below). **Coralreach**, due south, with Pearlhollow under it (mission 16). **The Kelpwood wreck**. **The Leviathan Shoal**, a Stillwater, to the south-south-west |
| **Westgloam** (west) | Fog | **Gloam Shore**, Vesper's drowned island with its maelstrom, due west (mission 20). **The Umbral Gate**, the black falls on the north-west rim. Fog banks, fog-runner ships, and hidden islands that only fog sight shows (mission 20) |

- **Stillwaters** are calm belts where sailing ships sit "till they're bones". The Wayfarer crosses them on her
  Flame engine. The Leviathan Shoal is the big one.
- **Landmarks you steer by** (story.md §2): the Pinnacle's spire (centre), Embral's plume (south), the Eldergrove
  tree (west), the Stormspire (north), Silverdeep's whirl and lighthouse (south-east), the Umbral Gate's black falls
  (north-west rim) and Marrow Isle's beacon (east). They match the opening's six Well lights.

### 1.6 The Rimfalls

- A band of white water all round the world. Currents push ships back, and it can't be crossed.
- **The bite** in the east brings the falls within sight of the storm. **Fallhaven** stands on the last cliff there,
  with the falls to its east and the storm to its west. Ships pass between them on the **Fallhaven Narrows**.
- **The lost rim towns** (Hale's Point, Gullstone, Kettle Bay and Saltcombe) are marked on the rim around the bite.
  After the ending the rim recedes and they come back as regrown rim isles.
- **After the Breaking** the rim moves in by one block (256 pixels) all round.
- **The Farside** (postgame) opens over the eastern rim, past the bite, when the rim recedes after the ending. It is a
  map of its own, with "Last Bearing" at its far side.

### 1.7 The layers

Each layer is its own map, drawn **on the same grid as the world**, so a spot in a layer is straight above or below
the same spot on the sea (question **Where the sky and undersea layers sit**). Each is about 2,800 pixels square, a
quarter of the Wide, as decided.

- **The Cloudreach** hangs over the north and north-east: over Northreach, the Galeway's northern arc and the north of
  Eastwater.
  - You first ride up the Skyspout (mission 17). From mission 19 the airship flies in.
  - It holds the cloud sea, sky isles, the Aerie Monastery, a sky-port town and storm-cloud reefs. The Stormspire's
    top rises through it.
  - Falling or diving through a cloud hole drops you onto the sea at the matching spot. That's how Wynn ended up in
    the sea off Eastwater as a child.
- **The Deep Shelf** lies under the south and south-east: under Southdeep and the southern storm.
  - You go down through the Silverdeep whirl with the bubble hull (mission 18). Dive spots (mission 16) lead to
    on-foot underwater rooms.
  - It holds the kelp trench, the vents, sunken ruins, Pearlhollow and two more dome towns, and the Sunken Fleet.
  - Its north edge reaches under the storm into the Calm's floor, which is how Pearlhollow's divers come and go.
  - **The Undertow tunnel** runs from its north edge under the Calm and Dustplain to beneath the Spine. Act III can
    use it as a way under the Pinnacle.
- **The Hollow** has no place on the world map. It is reached by the tear in the Marrow Vault (missions 22 and 23)
  and holds mirror copies of earlier rooms: Canalport before the flood, Fallhaven as it was, the Pinnacle.

### 1.8 Sizes and sailing times

Question **How big the world is** recommends The Lost Age's size.

| What | Size |
|---|---|
| The whole world map | 8,192 pixels square (512 by 512 squares of ground, in blocks of 256 pixels) |
| Meridia | About 2,200 by 2,500 pixels |
| Marrow Isle | About 560 by 440 pixels |
| The Calm's width | About 700 to 900 pixels, coast to storm |
| The Galeway's thickness | About 450 pixels |
| The Wide's width | About 1,400 pixels, but only about 200 at the Fallhaven Narrows |
| Each layer | About 2,800 pixels square |
| The demo's map | The middle 4,096 pixels square: Meridia, the Calm and the inside of the storm |
| The folded screen | About 373 by 160 pixels of world. A ship crosses it in five seconds |

First-visit sailing at today's ship speed (75 pixels a second; two thirds of the time if you hold run):

| Trip | Time | What the scripts say |
|---|---|---|
| Marrow Isle to Canalport | about 15 s | "Two days south across the Calm" |
| Canalport to the Eldergrove, round the south | about 60 s | "Two days west" |
| Marrow Isle to the Eldergrove, round the north | about 57 s | "Two days west" |
| The Eldergrove to Lantern Reef | about 16 s | "A day and a night north" |
| Marrow Isle to Lantern Reef | about 45 s | "A day and a night north" |
| Marrow Isle to Tortell's isle (mission 10) | about 9 s | (new) |
| The Bazaar to Fallhaven (Act II) | about 21 s | "A day and a night" |
| Marrow Isle to Fallhaven through the broken storm (Act II) | about 15 s | "Two days" by skiff lanes |
| Mission 12's walk from Dustplain to Brightcoast's north-east coast | about 52 s running | "Across the continent" |

A ring can't make the Greenwild "two days" from both Canalport and Marrow Isle. Question **The voyage lines in the
scripts** drops the day counts from voyages you sail yourself, and **Sailing back to places you know** keeps return
trips short.

### 1.9 Regions

There has been no region list, and the counts around the docs disagree. Proposed: **eight big regions**, each split
into smaller **areas**. An area sets the wild battles, the battle backdrop and the music, and the place banner fires
when you cross into a new one, with its danger stars.

| Big region | Areas (stars) |
|---|---|
| **Meridia** | Brightcoast ★, the Greenwild ★★, Dustplain ★★, Frostmarch ★★★, the Spine's peaks ★★★★★, the Pinnacle ★★★★ |
| **The Calm** | Marrow Isle ★, the Marrow highlands ★★, the east Calm ★, Saltmarsh Reach ★, the south Calm ★★, the west Calm ★★, the north Calm ★★, the north fog ★★ |
| **Northreach** | The open ice ★★★★, Thunderhead ★★★★, the Stormspire's rock ★★★★★ |
| **Eastwater** | The trade waters ★★, the Narrows ★★★, the southern isles ★★★ |
| **Southdeep** | The coral lagoons ★★★, Silverdeep ★★★★, the Leviathan Shoal ★★★★ |
| **Westgloam** | The fog sea ★★★★, the Umbral Gate ★★★★★ |
| **The Cloudreach** | Its own areas, ★★★ to ★★★★★ |
| **The Deep Shelf** | Its own areas, ★★★ to ★★★★★ |

- **The Galeway** (fragments ★★★★, the eye ★★★★★), **the Hollow** (★★★★★) and **the Farside** are special regions
  outside the eight.
- **What uses the big regions:** the Bounty Board's one rumour per region (eight), the Tumbleweed Trio's five side
  stories (Meridia, the Calm, Eastwater, Southdeep, Northreach), Wynn's chart, and the seven star orbs (Marrow Isle in
  Act I, then one each in Meridia, Northreach, Eastwater, Southdeep, Westgloam and the Cloudreach).
- **Stars** are set by hand (decided). As a guide: ★ about level 1 to 9, ★★ 8 to 16, ★★★ 15 to 24, ★★★★ 23 to 35,
  ★★★★★ 34 and up.

## 2. Act I in detail

### 2.1 Where each Act I place sits

| Place | Where | How you reach it | When | Stars |
|---|---|---|---|---|
| **Marrow Isle**: Stonehollow, the Vault, the cove | East-north-east Calm, close to the storm | Home. By ship to the cove | Mission 1 | ★ |
| **The Marrow sea caves** | Marrow Isle's east coast, on the reef lagoon | Mission 2 down the river from the Vault (Corvin). On foot from the cove's shore path after that | Mission 2 | ★ |
| **Fallhaven** | The east rim, at the Fallhaven Narrows, just outside the storm | Ketch's skiff through the storm lanes (missions 2 and 9). The Kestrel follows Ketch in mission 9 | Missions 2 and 9 only | — |
| **Saltmarsh Reach and Canalport** | Meridia's east coast, at the Crownwater's mouth, south of Marrow Isle | The Kestrel's first voyage (mission 3), then by sea through the Reach's channels | Mission 3 | ★ |
| **Embral Isle**: the Forgeheart | South Calm, near the storm | Ketch's skiff (Crew 2, mission 4). Ringed by cutters for the Kestrel | Mission 4, Crew 2 only | ★★ |
| **The Greenwild and the Eldergrove** | Meridia's west coast, at the Eldwater's mouth | By sea to the river landing | After mission 4 (Ilse's letter) | ★★ |
| **Lantern Reef** | North-west Calm, in the north fog | By sea, once Vesper pilots | Once she's hired (mission 6) | ★★ |
| **Bastion Rock** | West Calm, off the Greenwild's coast | Ketch's skiff (Crew 2, mission 7). Its sea-gate turns the Kestrel away | Mission 7, Crew 2 only | ★★ |
| **The Tradewind Bazaar** | Eastwater, north of the bite, beyond the storm | Ketch's skiff (Crew 2, mission 8) | Mission 8, Crew 2 only | ★★ |
| **The Wayfarer** | A sea cave under Marrow Isle's north cliffs, then the cove | Down the Vault's sea stair | Mission 10 | — |

### 2.2 Getting about in Act I

- **On foot.** Everyone walks inside rooms. From mission 10 (question **When Marrow Isle's west road opens**), the
  hero also walks Marrow Isle's highlands on the world map. Meridia's walkable map comes after the demo.
- **Surf.** On a Set Pokémon that learns it (Marill from mission 3, Froakie from mission 7), only on canals, rivers,
  lakes and short coastal shallows. Never across the open Calm.
- **The Kestrel** (missions 3 to 9). Ilse lends her in mission 3.
  - The first voyage, Marrow Isle to Canalport, stays a story voyage with its narration: the prologue is guided.
  - Free sailing starts when Act I opens (after mission 4). You board from Tully at a jetty, sail the Calm, and dock
    by sailing into a harbour. Tully stays with the ship, and the ship stays where you left her.
  - **Sail here** (question **Sailing back to places you know**): from Tully, any harbour you've already visited, with
    a fade.
  - The Kestrel has no restoration point. You rest at inns.
- **Crew 2's travel** is always Ketch's skiff, as story moves you don't steer: a fade, a line of narration and a new
  room. The skiff is their free restoration point. Crew 2's Map shows the Chart read-only, with their place marked.
- **Crossing the storm** in Act I is story only: Crew 2's skiff runs (missions 2, 4, 7, 8), and the Kestrel behind
  Ketch in mission 9, both ways. Her keel cracks on the way home.
- **The Wayfarer** (mission 10). She sails out of her cave and round to the cove on the morning tide.
  - Her helm works like Tully, with **Sail here** for visited harbours, and the last row "The Galeway" plays the
    maiden voyage's end card (demo 20).
  - Steering into the storm from the open sea gives Ketch's line: "Not from here. When we cross, we cross from home,
    on the morning tide."
  - With Ketch calling the lanes, she can thread Marrow Isle's reef gap to Tortell's isle (her "sea trials").
  - Ketch aboard is her free restoration point.
- **Fast travel home.** The inn's Home (menus N-13) lands at Stonehollow's inn door.

### 2.3 What stops you, in Act I

| Place | What you see | The line (to be written) | Opens |
|---|---|---|---|
| The Galeway | A storm wall all round the Calm | Tully: the order's ships turn back here, and so does she | Mission 11 (Act II) |
| Lantern Reef | A fog bank in the north-west | Tully can't see the bow from the helm | Vesper hired (mission 6) |
| Embral Isle | Tidewarden cutters across the bay | "Closed by the Commodore's order" | Act II |
| Bastion Rock | A shut sea-gate | Sergeant Pruitt's "Name! Number! Licence!" and a refusal | Act II |
| Tortell's isle | A pink roof behind a reef | Tully: "That gap's Rimborn work. Not with this keel" | The Wayfarer with Ketch (mission 10) |
| Hushwater, Twin Bells | Islands with closed landings | Their own voices: a barred reed gate, a tide over the sandbar | When they're built (after the demo) |
| The Crownwater | Canalport's locks | "No vessel up the Crownwater without a Pinnacle pass" | Act III |
| Meridia's other coasts | Cliffs and beaches, no landing | (no line, just shore) | When Meridia's walkable map comes |
| Marrow Isle's west road | The rockslide behind the west gate | The west gate's sign | Mission 10 |

## 3. Each place's rooms, and how they join

**Rooms today:** 17 are built. The approved scripts add 8 (hero_house, fallhaven_cliff, canalport_canals,
greenwild_hive, bastion_caves, wayfarer_berth, wayfarer_galley and wayfarer_quarters). This design adds 3 for the main
path and 6 optional ones, merges 2 into 1, and removes 4 links that make no sense. Your second note then makes every
place bigger than its one room: the **Scenes and entrances** list under each place below is the full set (question
**Towns as several scenes**).

**How a place is built, from your note:**
- **A place is a set of scenes.** A village has one or two outdoor scenes. A city has three or more, one per district
  (a harbour front, a lower town, an upper town). Golden Sun's towns work this way, and it is what the Fold's screen
  shows best: one district at a time, each a real place with walls you can see.
- **Every named building is its own interior scene:** inns, shops, named houses, the hatchery, halls, offices. You walk
  in through the door and see the room, the way Golden Sun does, instead of a menu over the street. Inns hold the rest
  and the save, shops the shop screen (slice 4b), houses their people and chests.
- **Under and over are scenes too:** a cellar down a stair, a cave under the town, a tower up a ladder, a cliff road
  up to a high town, a harbour down a stair.
- **Every entrance is named and runs both ways:** doors, stairs down to a cellar or cave, cave mouths, ladders, gates,
  docks, hatches and roads off a scene's edge. The data lists each pair once, and the engine makes both sides, so a
  door can never lead somewhere its other end doesn't come back from (today four links do that).
- **Sized to the story, not to today's rooms.** Where a script names a building or a district, it is a scene. Where a
  scene needs more ground than any Golden Sun area gives, it is generated (§5.5).
- **Marks:** *built* is in the engine, *approved* is in a script and not built, *new* is this page, *later* is Act II
  or after the demo. Every link below runs both ways.

### 3.1 Marrow Isle

Question **Marrow Isle's shape**. Marrow Isle is a cliff-ringed highland island (see the bottom of the picture).
North is up:
- **The Vault hill** in the middle-north. The Vault road climbs to its door from the village.
- **Stonehollow** south of the hill, in the middle-east.
- **The cove**, the island's only harbour, on the south-east, at the foot of the south road. It opens to the
  south-east, past **the beacon** on its eastern headland. The Holdfast anchors off that point.
- **The reef lagoon** along the east coast, behind a reef with one gap at its north-east end (the "reef gap" Ketch
  uses). **The sea caves** open onto it, and **Tortell's isle** sits in it.
- **The north cliffs**, with **the Wayfarer's cave** under them, below the Vault. **The North Shore Caves**, the
  ones Ilse's marines search, open further west along that coast.
- **The highlands** to the west, past the west gate and the rockslide: lakes, terraces and **Dunstan's quarry**.

| Room | What it is | Joins | Today | Change |
|---|---|---|---|---|
| `stonehollow` | The village | North gate to `vault_halls` (the Vault road). South road to `marrow_cove`. West gate to the highlands on the world map. Doors to `hero_house`, the inn and the hatchery | South road walks into Golden Sun's Vale. West edge walks onto Golden Sun's Angara map, with no gate. Tully stands at the top edge by the Vault road | South road to the new cove. West gate shut with the rockslide line until mission 10, then onto our world map (arriving at the unused entrance 2). Tully moves to the cove |
| `hero_house` (approved) | Brann's cottage on the Vault road, next to the Rivalsons' | Its door in `stonehollow`. A secret attic door to the makers' cabin | Not built | Build, with the makers' cabin as a small attic room |
| `marrow_cove` (**new**) | The cove: the jetty, the cove path, Cidrick's yard at the far end, the headland path to the beacon, and a shore path north to the sea caves | North edge to `stonehollow`'s south road. The jetty is the harbour on the world map. Shore path to `sea_caves` (from mission 2). Gangway to `wayfarer` (from mission 10's end) | Doesn't exist: every "in the cove" scene happens in the village | Build. Mission 1, 3, 9 and 10's cove scenes move here, with Tully, the Kestrel, Ketch's skiff, the beached Kestrel and the Wayfarer at anchor |
| `vault_halls` | The Vault's upper halls | South to `stonehollow`. From mission 10, the inner door's landing: the sea stair down to `wayfarer_berth`, and the warded stair (shut until mission 22) | The inner door scene puts you straight on the Wayfarer's deck | Join through the berth instead |
| `wayfarer_berth` (approved) | The sea cave under the north cliffs | Sea stair up to `vault_halls`. Gangway to `wayfarer` | Not built | Build. Empty once she moves to the cove |
| `sea_caves` | The Marrow sea caves: the river's tunnel at the south end, the river mouth on the lagoon | Story arrival from the river (mission 2). The mouth to `marrow_cove`'s shore path, on foot | Its top-right corner walks straight into Fallhaven, beyond the storm | Remove that link. Mission 2's skiff scene replaces it, as the script says |
| `marrow_quarry` (**new, optional**) | Dunstan's quarry: terraces, carts, Rimborn workers | An icon on the highlands | — | From mission 10 |
| `north_shore_caves` (**new, optional**, two rooms) | The caves the marines searched | An icon on the north coast of the highlands | — | From mission 10 |
| `tortell_isle` (**new, optional**) | A sand cay with a pink house, and the lagoon's shallows | Entered from the ship, inside the reef | — | From mission 10 |

**One name for one cave.** "The Marrow sea caves" is the room. "The river caves" is its inner, river half. "The east
caves" is what Corvin calls them. "The north shore caves" are a different place, where the marines search in vain.

**Scenes and entrances, Marrow Isle**

| Scene | Entrances |
|---|---|
| `stonehollow` (built, outdoor: the village) | North gate → the Vault road and `vault_halls`. South road → `marrow_cove`. West gate → the highlands on the world map (rockslide until mission 10). Doors → `hero_house`, `quiet_stone` (the inn), `hatchery`, `rivalsons_house`. Nell's stall and the Keeping Stone stand in the street |
| `hero_house` (approved, interior) | Door → `stonehollow`. Attic ladder → `makers_cabin` (new: the secret attic room with every maker's book) |
| `quiet_stone` (new, interior: the inn) | Door → `stonehollow`. The rest, the save, the Home warp and, from mission 10, the Rimborn's contract board. Cellar stair → `quiet_stone_cellar` (new, optional: the storeroom, a chest, the Rimborn bunks) |
| `hatchery` (new, interior) | Door → `stonehollow`. The first partner is chosen here (mission 1), and the eggs from the Kin Garden hatch here later |
| `rivalsons_house` (new, interior, optional) | Door → `stonehollow`. Gary's house: his mother, his trophies, his first lines |
| `marrow_cove` (new, outdoor: the cove) | Cove path north → `stonehollow`'s south road. The jetty is the harbour on the world map (the Kestrel, then the Wayfarer at anchor). Shore path east → `sea_caves`' mouth (from mission 2). Gangway → `wayfarer` (from mission 10's end). Headland path → the beacon (inside the scene). Door → `cidricks_yard` (new, optional: the shipwright's shed, mission 10) |
| `vault_halls` (built, the Vault's upper halls) | South door → `stonehollow`'s north gate. The crack → the underground river (story only, mission 1). Behind the inner door: sea stair → `wayfarer_berth`, warded stair → the Earth Well (Act III) |
| `wayfarer_berth` (approved, the sea cave) | Sea stair → `vault_halls`. Gangway → `wayfarer`. The cave mouth → the sea (story only) |
| `sea_caves` (built) | Mouth → `marrow_cove`'s shore path. The river tunnel at the south end → the Vault's river (story arrival, mission 2) |
| `wayfarer` (built, the deck) | Gangway → `wayfarer_berth` or `marrow_cove`'s jetty, wherever she is moored (in Act II, any harbour). Forward hatch → `wayfarer_galley` (approved). Aft hatch → `wayfarer_quarters` (approved). The chart room is inside the scene |
| The highlands (world map, from mission 10) | Icons → `marrow_quarry` (new, optional, with a door → the quarry shed), `north_shore_caves` (new, optional, two scenes joined by a tunnel, cave mouth on the north coast), the lakes (Surf). The west gate → `stonehollow` |
| `tortell_isle` (new, optional) | Landing → the ship, inside the reef. Door → `tortells_house` (new, interior: the pink house) |

### 3.2 Canalport and Saltmarsh Reach

**Saltmarsh Reach** is a wide, shallow tidal bay at the Crownwater's mouth: brown water, mudbanks, reed islets and
marked channels. Ships thread the channels to **Canalport**, which stands at the bay's head. Its harbour front faces
the Reach (the jetty, the beach, the sea dike). The lower town's canals lie behind the sea wall, and the upper town
stands on the bluff above. So both "on the sea" and "up the channels" are true, and the sluice beast came up a channel
from the open Calm.

| Room | What it is | Joins | Today | Change |
|---|---|---|---|---|
| `canalport` | The harbour front | The jetty end is the harbour on the world map. The lock stair (Surf) to `canalport_canals`. The south road, shut in the demo, later to Brightcoast on the world map | You arrive mid-room. The south road walks onto Golden Sun's Angara map after mission 3 | Arrive at the jetty end. The south road keeps its "dikes being walked" line through the demo |
| `canalport_canals` (approved) | The lower town's canals, south to north | In by Surf from the lock stair, back by the quay stair on foot | Not built | Build |
| `reach_islet` (**new, optional**) | A reed islet with a fowler's hut | Entered from the ship in the Reach | — | From mission 4 |
| `canalport_upper` (Act II) | The upper town on the bluff, with a new jetty | — | — | After the flood. The shops move here |
| The drowned lower town (Act II) | A Dive area | — | — | After the flood |

**Scenes and entrances, Canalport**

| Scene | Entrances |
|---|---|
| `canalport` (built, outdoor: the harbour front) | The jetty is the harbour on the world map. Lock stair (Surf) → `canalport_canals`. Quay stair → `canalport_canals` on foot (the way back). Doors → `tidewarden_post` (new, interior: Ilse's briefing in mission 3, the notice), `dry_boot` (new, interior: the inn, with Hake's white Wailord rumour), `harbour_office` (new, optional: Quayle and the Marill ferry). The bluff stair → `canalport_upper` (shut with a line in the demo, open in Act II). South road → Brightcoast on the world map (shut through the demo with the dikes line) |
| `canalport_canals` (approved, outdoor: the lower town) | Lock stair and quay stair → `canalport`. Doors → `canalport_shop` (new, interior: the demo's first shop), `sluice_house` (new, interior: the sluice gates, the Leather Cap), `lettie_house` (new, optional: Lettie and Barnaby). The Grand Cut, the Tanners' Swing and the Long Weir are inside the scene. The sluice beast rises in the channel outside the sluice house |
| `canalport_upper` (later, outdoor: the bluff) | The bluff stair → `canalport`. After the flood: the new jetty (the harbour), and the shops and the inn move up here, each with its door |
| `reach_islet` (new, optional) | Landing → the ship in the Reach. Door → the fowler's hut (new, interior) |
| The drowned lower town (later) | A Dive area entered from the ship over the old canals |

### 3.3 Embral Isle

A volcano island near the storm. The Forgeheart stands on the mountainside above **the bay**, where the tithe fleet
anchors. **The black-sand cove**, where Ketch hides his skiff, is round on the east side. The cove stair climbs to the
gate court.

| Room | Joins | Today | Change |
|---|---|---|---|
| `embral_cove` (**new**, small) | Ketch's skiff. The cove stair up to `forge_hall`'s gate court | Crew 2 lands straight in the gate court | Build. Arrive here in mission 4, and it is the Wayfarer's landing in Act II |
| `forge_hall` | The gate court and halls. The shaft to `forge_sanctum` | As built | Keep |
| `forge_sanctum` | The Well stair, the ward door, the seal chamber | As built (re-clip approved) | Keep |
| `embral_caldera` (Act II) | Up from the gate court to Ho-Oh's nest | — | Act II |

**Scenes and entrances, Embral Isle**

| Scene | Entrances |
|---|---|
| `embral_cove` (new, outdoor: the black-sand cove) | Ketch's skiff (story), and the Wayfarer's landing in Act II (the harbour). Cove stair → `forge_hall`'s gate court |
| `forge_hall` (built: the gate court and halls) | Gate court south → the cove stair. Doors inside the scene → `forge_kitchen` and `forge_store` (new, optional interiors: the kitchen and the tithe store, each a small room with its chest). The shaft → `forge_sanctum`. East door → `embral_caldera` (later) |
| `forge_sanctum` (built) | The shaft → `forge_hall`. The ward door and the seal chamber are inside the scene |
| `embral_caldera` (later, outdoor) | East door → `forge_hall`. Ho-Oh's nest after the Breaking |

### 3.4 The Greenwild and the Eldergrove

The Eldwater runs west to the sea. **The village** sits on the north bank at its mouth, with its river landing and
the great trunk behind the Elder's house. **The forest** runs east along the river. **The Sourmire** lies south of the
river. **The tree's heart** is not under the trunk but at its deepest root, south of the river, where the Forest Well
is. That's why you reach it the long way over the vine bridge and through the swamp. **The root-way** runs back north
under the river and comes out on the north bank by the village: a shortcut home.

| Room | Joins | Today | Change |
|---|---|---|---|
| `eldergrove` (the village) | The west edge is the river landing (the harbour on the world map, with Tully and the waystone). The east path to `greenwild` | As built | Keep. The waystone with the Snorlax stands at the landing |
| `greenwild` (the forest) | West to `eldergrove`. The south path to `eldergrove_heart`. The north path to `greenwild_hive`. Later, its east edge onto the Greenwild on the world map | Leaving south lands you at the heart's south edge, walking north. Coming back does the same in reverse | Arrive at the heart's north edge walking south, and back at the forest's south edge walking north |
| `eldergrove_heart` | From `greenwild`. The root-way to `greenwild`'s north bank | As built | Keep |
| `greenwild_hive` (approved, optional) | From `greenwild`'s north path | Not built | Build (from mission 6's pilot flag) |

**Scenes and entrances, the Greenwild**

| Scene | Entrances |
|---|---|
| `eldergrove` (built, outdoor: the village) | The river landing at the west edge is the harbour on the world map, with the waystone and the Snorlax. East path → `greenwild`. North path → `hazels_house` (new, interior). Doors → `mossbed` (new, interior: the inn), `elders_house` (new, interior: the Elder, with the root stair down to the great trunk's foot, a small scene of its own), `sorrels_hut` (new, optional), the coast post (new, optional: the Tidewarden hut by the landing) |
| `greenwild` (built, outdoor: the forest) | West → `eldergrove`. South path → `eldergrove_heart` (arrive at its north edge). North path → `greenwild_hive` (approved, optional). East edge → the Greenwild on the world map (after the demo). The vine bridge is inside the scene |
| `eldergrove_heart` (built) | North → `greenwild`. The root-way (west side) → `greenwild`'s north bank, the shortcut home once the heart is reached |
| `greenwild_hive` (approved, optional) | North path → `greenwild` |

### 3.5 Lantern Reef

One room: Marrit's rock (hut, lantern house, quay), the Last Bell broken in three, the Merrow, and the sandbar.

| Room | Joins | Today | Change |
|---|---|---|---|
| `lantern_reef` | Marrit's quay is the harbour on the world map | 17 squares wide, narrower than the folded screen, so grey shows | Re-cut wider (at least 24 squares) with sea and fog at the sides, or a fog backdrop (question **Moving between rooms**) |
| A ghost-ship room (Act II) | From the reef | — | Bonewhistle's later scene and the other hulks |

**Scenes and entrances, Lantern Reef**

| Scene | Entrances |
|---|---|
| `lantern_reef` (built, outdoor: Marrit's rock and the wreck) | Marrit's quay is the harbour on the world map. Door → `marrits_hut` (new, interior: the rest for the night decks). Door → `lantern_house` (new, optional: the lamp, a chest). The gangway to the Last Bell, the spar to the Merrow and the stern stair to the sandbar are inside the scene |
| `ghost_ship` (later) | From the Last Bell's stern: Bonewhistle's room and the other hulks (Act II) |

### 3.6 Bastion Rock

A black fortress on a rock in the west Calm. The sea-gate is on its east face. The strand runs under the north wall,
with Ketch's landing at its west end. The cave mouth opens on the north face.

| Room | Joins | Today | Change |
|---|---|---|---|
| `bastion_shore` | Ketch's skiff. The Scoop tunnel to `bastion_jail` | As built | Keep. In Act II, the strand is the landing |
| `bastion_jail` | The tunnel. The cistern grate to `bastion_caves` | As built | Keep |
| `bastion_caves` (approved) | From the cistern. The cave mouth onto the sea by Surf (story exit, mission 7) | Not built | Build |

**Scenes and entrances, Bastion Rock**

| Scene | Entrances |
|---|---|
| `bastion_shore` (built, outdoor: the strand) | Ketch's landing at the west end (story), the Wayfarer's landing in Act II. The sea-gate → `bastion_yard` (later: the fortress yard and the ledger office, shut in Act I). The Scoop tunnel → `bastion_jail` |
| `bastion_jail` (built) | The tunnel → `bastion_shore`. Doors inside the scene → `key_room`, `records_office` and `seized_store` (new, optional interiors, each one small room off the corridor, as the script names them). The cistern grate → `bastion_caves` |
| `bastion_caves` (approved) | The grate → `bastion_jail`. The cave mouth → the sea (Crew 2's Surf exit, story). The fortress stair → `bastion_yard` (later) |

### 3.7 Fallhaven

A cliff town at the inner end of the bite: the lower town above the harbour, the high town above that, the cliff road
between them, and the west cove (where the boats gather) on the cliff's west side.

| Room | Joins | Today | Change |
|---|---|---|---|
| `fallhaven` and `fallhaven_lower` | Two rooms for one lower town (missions 2 and 9), cut from overlapping parts of the same Golden Sun town, with no link between them | Two rooms | **Merge into one lower-town room** with three states: mission 2 at dusk, mission 9 at night, and fallen. The harbour stair at its south end (Ketch lands there in mission 2). The west alley's top to `fallhaven_cliff`. The north stair to the archive's great doors |
| `fallhaven_cliff` (approved) | The switchbacks from the lower town to the high town gate, with the archive's high door on the second bend | Not built | Build. In mission 9 you come down it from the west cove |
| `fallhaven_archive` | The great doors (south) to the lower town. The high door to the cliff road. The wind-wheel lift to the harbour steps. The order's cellar under the plaza's well | The finale lands you at Stonehollow's lower entrance | Land at `marrow_cove` at dawn, as the script says |
| `fallhaven_ruin` (Act II) | The cliff top, the high town's empty lanes, the west cove (the harbour on the world map), the memorial | — | After mission 9. Home of the memorial heart quest |

**Scenes and entrances, Fallhaven**

| Scene | Entrances |
|---|---|
| `fallhaven_lower` (merged, outdoor: the lower town, three states) | Harbour stair (south) → `fallhaven_harbour`. West alley's top → `fallhaven_cliff`. North stair → `fallhaven_archive`'s great doors. Doors → `leaning_gull` (new, interior: Fen's inn, the free rest until mission 2 is done), `saels_house` (new, interior), `martas` (new, optional), `wennas` (new, optional: the pickled eggs). The plaza's well → `order_cellar` (new: the order's cellar under the plaza, if the mission 9 script's cellar beat needs its own scene, else inside the archive). The east street falls inside the scene |
| `fallhaven_harbour` (new, outdoor, small) | Harbour stair → `fallhaven_lower`. Ketch's skiff lands here (mission 2). The wind-wheel lift → `fallhaven_archive`'s ledge |
| `fallhaven_cliff` (approved, outdoor: the switchbacks) | Bottom → `fallhaven_lower`'s west alley. Second bend's high door → `fallhaven_archive`. Top → `fallhaven_high` (new, outdoor: the high town gate and lanes, mission 9's way down from the west cove) |
| `fallhaven_high` (new, outdoor) | Gate → `fallhaven_cliff`. West lane → `fallhaven_cove` (new, outdoor, small: the west cove where the boats gather, the Kestrel's mooring in mission 9, and the ruin's harbour on the world map in Act II) |
| `fallhaven_archive` (built) | Great doors (south) → `fallhaven_lower`. High door → `fallhaven_cliff`. The lift → `fallhaven_harbour`. The east wing and the east vault are inside the scene |
| `fallhaven_ruin` (later, outdoor) | The cove is the harbour. The cliff top, the empty lanes and the memorial |

### 3.8 The Tradewind Bazaar

| Room | Joins | Today | Change |
|---|---|---|---|
| `tradewind_bazaar` | The Guild hull's landing is the harbour on the world map. The market hull and Hull Nine by plank and sail-bridge | As built | Keep. More hulls and the players' stage become rooms in Act II |

The run to Fallhaven at the end of mission 8 stays a story move, with a fade and its narration.

**Scenes and entrances, the Tradewind Bazaar**

| Scene | Entrances |
|---|---|
| `tradewind_bazaar` (built, outdoor: the lashed hulls) | The Guild hull's landing is the harbour on the world map. Plank → the market hull and sail-bridge → Hull Nine (inside the scene today). Doors → `guild_hall` (new, interior: the Bounty Board and the first contracts), `pursers_office` (new, interior: mission 8's Mind Read, moved indoors), `lashed_lantern` (new, interior: the inn) |
| Later hulls (Act II) | Each a scene off a plank: the players' stage hull (the Wide Players), the shop hulls, Maize's sloop the Merry Wooloo |

### 3.9 The Wayfarer

`wayfarer_berth` (approved) leads to `wayfarer` (the deck with the helm, the engine's well, the muster roll and the
chart room). Hatches lead down to `wayfarer_galley` and `wayfarer_quarters` (both approved). From mission 10's end, the
gangway leads to `marrow_cove`'s jetty. In Act II, it leads to whichever harbour she is moored at. At sea she is a ship
on the world map, and her decks are walked only in harbour.

**Scenes and entrances, the Wayfarer:** `wayfarer_berth` (approved) → `wayfarer` by the gangway; `wayfarer` →
`wayfarer_galley` and `wayfarer_quarters` (both approved) by its two hatches; the gangway → whichever harbour she is
moored at. At sea she is a ship on the world map.

### 3.10 The changes, in one list

- **New rooms on the main path (3):** `marrow_cove`, `embral_cove`, and the makers' cabin (a small attic room of
  `hero_house`).
- **New optional rooms in the demo (6, question How much optional content the demo has):** `reach_islet`,
  `cockle_cay`, `marrow_quarry`, `north_shore_caves` (two rooms) and `tortell_isle`.
- **Approved rooms still to build (8):** `hero_house`, `fallhaven_cliff`, `canalport_canals`, `greenwild_hive`,
  `bastion_caves`, `wayfarer_berth`, `wayfarer_galley` and `wayfarer_quarters`.
- **Merge:** `fallhaven` and `fallhaven_lower` into one lower-town room.
- **New outdoor scenes from your note (4):** `fallhaven_harbour`, `fallhaven_high`, `fallhaven_cove` and
  `canalport_upper` (Act II, placed now).
- **New interior scenes from your note:** on the main path or for the rest and shops, 16: `quiet_stone`, `hatchery`,
  `makers_cabin`, `tidewarden_post`, `dry_boot`, `canalport_shop`, `sluice_house`, `mossbed`, `elders_house`,
  `marrits_hut`, `leaning_gull`, `saels_house`, `guild_hall`, `pursers_office`, `lashed_lantern` and `hazels_house`
  (the demo builds the ones its missions walk into first). Optional, 18: `rivalsons_house`, `quiet_stone_cellar`,
  `cidricks_yard`, `tortells_house`, `harbour_office`, `lettie_house`, the fowler's hut, `forge_kitchen`,
  `forge_store`, `sorrels_hut`, the coast post, `lantern_house`, `key_room`, `records_office`, `seized_store`,
  `martas`, `wennas` and `order_cellar`. Golden Sun has interior tiles for most of these; the rest are generated.
- **Re-cut:** `lantern_reef` wider (or a backdrop). The approved re-cuts of `greenwild`, `forge_sanctum` and
  `wayfarer` stand.
- **Links removed:** Stonehollow's south road into Golden Sun's Vale, Stonehollow's west edge onto Golden Sun's Angara
  map, Canalport's south road onto the same spot, and the sea caves' corner walk into Fallhaven.
- **Arrivals moved:** Tully to the cove's jetty. Every harbour arrival to its jetty end. The forest and the heart
  arrive on the matching sides. The archive's finale lands at the cove.
- **Data:** `places.json` (name, region, position, harbour, doors and their sides, stars, landmark) and
  `regions.json`, as menus §8.1 planned. The Kestrel's `voyages.json` folds into `places.json`.
- **Checks to rework:** `stonehollow_check`, `world_check`, `ship_check`, `reveal_check`, `vale_exits_check` and
  `dialogue_check` all lean on the Golden Sun links today.

## 4. Off the main path: exploring, grinding and treasure

You asked (24 Oct) for areas to explore and to grind for EXP, items and money, and homes for the eggs and side
quests. This section places them.

### 4.1 What every area gets

Every area of the world gets the same small kit, so there is always something off the path:
- **A grinding spot** with a good wild table (monsters and Pokémon), a little above the main path's level, and **an
  inn or restoration point within a short walk**.
- **Treasure:** items §13's density. Towns get one or two chests and a glint. Dungeon rooms get two or three chests,
  one behind the newest verb and one behind a later one. Every region gets one Reveal cache and one Scoop dig spot.
- **One hidden, Djinn-style Kin find** (it hides, runs or battles first, and joins with no ball).
- **Kin habitats**, marked on the Chart once seen (DexNav's "Search here").
- **A home for an egg**, and a hook for a contract or a side story.

### 4.2 Act I, place by place

Levels follow progression 3: about L6–7 at mission 3, L8 at mission 5 and L10 at mission 10.

| Area | Opens | How you find it | Grinding (rest nearby) | Treasure | Kin | Eggs and quests |
|---|---|---|---|---|---|---|
| **Stonehollow and the cove** | Mission 1 | Home | None (★, the village) | The buried chest (Reveal, from mission 6). **The first star orb**: a Scoop glint under the beacon | The hatchery | Gary Rivalson, the Mercury-blue puddle, the makers' cabin and the Wanderer, the Game Boy on the shelf, the star orb (mission 1). Cidrick's yard and "A Funeral at Sea" (mission 10) |
| **The Vault's upper halls** | Mission 1 | The Vault road | Battles once Act I opens (open 18) | The lock chest, the gallery's glint, the Long Sword | — | — |
| **The sea caves** | Mission 2 (Crew 2), then on foot from the cove | The cove's shore path | L7–9 (The Quiet Stone) | The Rimborn stash, the Travel Vest | Cave Kin. **The rare Ditto** ("A wild Ditto draws near!") | The hidden-passage singers (mission 2) |
| **Saltmarsh Reach's reed islet** (new) | Mission 4 | Seen from the Reach's channels on the way to Canalport | L6–8 (The Dry Boot) | A dig glint, a fowler's chest | Water, Bug and Grass Kin. A hidden find in the reeds | A contract hook (a catch for Nell) |
| **Cockle Cay** (new) | Mission 4 | A low sandy cay south of Marrow Isle, on the way to Canalport | L7–9 (The Quiet Stone) | A chest in a wreck's ribs, a dig glint | Shore and sea-bird Kin | Sinks at the Breaking, and comes back as a Dive spot |
| **Canalport and its canals** | Mission 3 | The story | The canals, L6–8 (The Dry Boot) | The Tanners' chest, the mudbank's Great Balls, the sluice house's Leather Cap, the beach glint | Marill's canal pod | Maize, the truck, the Spigot brothers, Turvey, the white Wailord rumour at The Dry Boot, Bravado's posters, "That's rough, friend" (mission 3). The Borrius traveller on the jetty |
| **The Greenwild** | After mission 4 | The village's east path | L8–10 (the Mossbed) | The high bough, the mire glint, the stump cache (Reveal), the bush chest (Cut), the pool alcove's Circlet (Surf) | Forest, Bug and Poison Kin. Combee in the Hive | The Snorlax at the waystone, "The Hive" (mission 5) |
| **Lantern Reef** | Mission 6 | The fog, with Vesper | The night decks, L9–11 (Marrit's lantern house) | The waist chest, the Magic Rod behind the fog banks, the Merrow's chest | Ghost Kin by night. **Mimikyu** | Maestro Bonewhistle and the lantern Litwick (mission 6) |
| **The Marrow highlands** (new) | Mission 10 | Stonehollow's west gate, once the Rimborn clear the rockslide | L9–12 on the world map (The Quiet Stone) | A glint by the lakes | Ground and Rock Kin, Water Kin on the lakes (Surf) | A contract hook (a hunt) |
| **Dunstan's quarry** (new) | Mission 10 | An icon on the highlands | L10–12 | A Move and Scoop puzzle to a gear chest. The quarry carts hint at mission 22's minecart run | Rock Kin. A hidden find in the spoil heaps | Dunstan and the forty Rimborn |
| **The North Shore Caves** (new) | Mission 10 | An icon on the north coast of the highlands | L11–13, with an alpha monster at the end (The Quiet Stone) | **The Act I Zen bean** in the last chamber, and a Rimborn smugglers' cache | Cave Kin | Ilse's marines' old search camp. A crack looks down on the Wayfarer's empty cave |
| **Tortell's isle and the lagoon** (new) | Mission 10 | The Wayfarer through the reef gap, with Ketch | Sea battles kept out of the lagoon | A sunken chest in the shallows (Surf), a dig glint | Rare lagoon Kin | **Master Tortell** teaches the "Tortoise Wave" (mission 10). A contract hook (a survey) |
| **The Calm at sea** | Mission 4 | Sailing | Sea battles by area, about half the land rate (question **Battles at sea**) | — | Sea Kin by area | — |

**Crew 2's places** keep their scripted pockets: Fallhaven (Pip's fall, Linden smashing pots, Turvey's cart in
mission 9), the Forgeheart (the Elder, the Bidoof everyone loves), Bastion Rock (Old Tarrant, the Magikarp salesman,
and the confiscated-gear locker) and the Bazaar (the Bounty Board with Sabra Arn, the Tumbleweed Trio's first heist,
Captain Swallow, Turvey, and the five first contracts).

**The "Any" eggs:** the Bliss cousins at every restoration point, the Ditto in the sea caves, "Hey! Look!" anywhere on
the field, the title-screen code, and the Borrius traveller (Canalport's jetty in Act I, the Bazaar in Act II).

**A board for Crew 1** (question **A contract board for Crew 1**): the Rimborn bring a Freeport Guild board to The Quiet
Stone in mission 10, with four to six hand-written contracts that point at the places above.

### 4.3 Act I after the demo

When Meridia's walkable map comes, Act I gains the rest of what story.md calls Act I:
- **Brightcoast** on foot from Canalport's south road: farms, the Crownwater's banks, Brightcoast's grinding fields
  (★, L5–9).
- **Dustplain** (★★): "Water Rights" at the oasis and the wild Gible chase, the mines, the Cacnea that always does
  1,000 damage.
- **Frostmarch** (★★★): "The Frozen Saint" at the glacier monastery, the ice caves.
- **Hushwater** (★, "The Silent Isle", with Captain Fibber) and **Twin Bells** (★★, "Low Tide", with the lighthouse
  and Fibber's dig spots).
- **Sandmere** and **Driftholm**, the other two wild islets that sink at the Breaking (L8–11).

### 4.4 Act II, in outline

| Region | Main places | Optional places, quests and eggs |
|---|---|---|
| **Meridia** (open on foot from mission 12) | Mission 12's walk home from Dustplain, round the Spine's south end, through Brightcoast to the north-east coast | The Doduo ranch on Brightcoast's farms (**the Dodo Derby**). The tall tower with the Persian and its Zen beans (inland Greenwild). Sorrel's burned groves (heart quest, up the Eldwater with the living hull). A star orb in Dustplain's mines. Bulbasaur on the farms and Chikorita in the regrown Eldergrove (Djinn-style). Galgamash's "Big Bridge" on a long span over the Spine's northern gorge. The hidden-passage singers' tunnel on mission 12's way |
| **The Calm** | Embral's caldera (Ho-Oh), Canalport's upper town | The three risen isles ("First Footprints"): Shelfback, Bellstone ("The Trouble with Wooloo", Maize) and Farer's Step ("The Idol Run"). The three sunk isles as Dive spots. The Churn's grotto (Whirlpool). Canalport's drowned lower town (Dive) and "Down the Drain" (the Spigots). Uncle Ashby's tea stall and "Proverbs". Charmander in Embral's caldera, Squirtle at Twin Bells. Tamsin's heart quest at the Forgeheart |
| **The broken Galeway** | The Skyspout (mission 17) | Storm fragments with strong monsters. The eye (airship) |
| **Northreach** | The lighthouse-court (mission 13) | Thunderhead Atoll ("The Sentinel", a superboss later). The Speakers' isle (the language puzzle). The four warriors' statue. A star orb. Maren's charter heart quest starts here |
| **Eastwater** | Ironfist Arena (mission 15) | **The Glimmer Saucer**, the Stone Mole, Vedge, Pell and Mell, Champion Bravado, Yancy, Captain Fibber, Cyndaquil. The Bazaar as a free port ("Paid in Full", the Wide Players, "The Captain's Lunch" and "The Feast of Fools"). Clockwork Key ("Tuesday Again"). The Fallhaven ruin and its memorial (Corvin and the hero's heart quest). Captain Hake's white Wailord. A star orb |
| **Southdeep** | Coralreach (mission 16), Silverdeep (mission 18) | The Kelpwood wreck (salvage). The Leviathan Shoal ("The Lane", where Hake's whaling ends and Bonewhistle's whale waits: "The Long Wait"). Totodile at Coralreach. A star orb |
| **Westgloam** | Gloam Shore (mission 20) | Hidden islands shown by fog sight, one with a Gloam clan survivor (Vesper's heart quest). Torro's "The Wrong Way" through a fog bank. A star orb |
| **The Cloudreach** | The Aerie Monastery (mission 17), the Stormspire's top (mission 19) | "Groundbound", "The Kite Races", the pure-hearted cloud (Altaria), Tarquin and Sorak, "The Unwinnable Test", "Energize", the Dreamdeck. The seventh star orb |
| **The Deep Shelf** | The Silverdeep sanctum (mission 18) | Pearlhollow's domes (Nerissa's heart quest), "The Choir", "The Sunken Fleet" (with Tarquin), the Undertow tunnel |
| **Everywhere** | — | Free-port Bounty Boards (the Bazaar, Marrow Isle, Coralreach, Clockwork Key, Ironfist, the sky-port, a dome town). The Tidewarden towns keep notice boards with wanted posters only. Galgamash's four duels, one per quarter. The Tumbleweed Trio's five stories. Swallow's stolen ships at each port. Linden's Heart Scales. Eevee's branches as Djinn-style finds across the Wide. Rival hunter crews at sea |

**Act II's towns, sized the same way.** The Pinnacle is a city of four or five districts (the gates, the markets,
the order's precinct, the palace, the Crown's workings underneath) with interiors in each. Coralreach is a stilt town of
two scenes over the lagoon with Pearlhollow's domes below as three or four more. Ironfist has the arena, the Glimmer
Saucer (an interior of its own), the fighters' lodgings and the docks. Clockwork Key, the sky-port, Gloam Shore's
drowned streets and the lighthouse-court each get two or three scenes and their interiors. The number of scenes is set
by what the story and the side quests need there, never by what fits in one screen.

**Postgame:** the Gem Sentinels on the Spine's peaks, the MissingFall Porygon on a Rimfall ledge by the Umbral Gate,
the Dreamdeck boss rush, Galgamash's finale, the Mew sighting at Canalport's truck, the regrown rim isles, and the
Farside.

### 4.5 The hidden town (adult mode only)

Your third note: one adult-only town, reachable only in adult mode, hinted at in rumours. Question **The adult-only
hidden town**. Working name: **Nightmarket Isle**.

- **Where.** Deep in the north fog, beyond Lantern Reef, on a second lane only a Gloam pilot knows. The fog is already
  the one place "no Tidewarden ship likes to follow", so a free town hiding in it needs no new geography, and it sits
  in the demo's sea, so nothing is remapped when adult mode comes (open 32: adult mode is built after the demo).
- **Outside adult mode it does not exist.** The fog past the reef stays solid, Vesper has no second lane, and the
  island is not on the map or the Chart. The rumours still play, as colour: a place "off every chart where the
  order's writ doesn't run".
- **The rumours.** One line each in the inns (The Quiet Stone, The Dry Boot, the Mossbed, Marrit's hut, The Leaning
  Gull), a Bounty Board rumour ("a lane in the fog, and a market that opens at dusk"), and Vesper, who changes the
  subject. In adult mode, once she is hired (mission 6), asking her at the helm opens the lane.
- **What it is.** A free island town of lanterns and lashed boats whose market opens at night: the adult side
  stories and scenes decided on the adult-mode page live here, with its own inn, shop and a few houses as interior
  scenes. Everyone there is an adult by canon, as adult-mode.md's rules require (consenting adults only, no one
  written younger, never Brann, nothing with Pokémon). It also carries ordinary rewards so visiting is worth it on its
  own: a shop with rare stock, a dig spot, a Kin find and a contract or two.
- **On the map.** An icon in the fog that appears only in adult mode (a flag swap of one block, like the story's
  changes in §6). Its quay is the harbour. Scenes: `nightmarket` (the quay and market, outdoor), `nightmarket_inn`,
  `nightmarket_shop` and the houses the adult-mode decisions call for.

## 5. How the world map looks and works

### 5.1 Walk and sail, Golden Sun's way

- **One world map** you walk on land and sail at sea, as decided (decision log 45 and 49).
- **Places are icons.** A town or dungeon is a small picture on the map. Walk or sail into it and the room opens on
  the side you came from. Leave the room and you stand beside the icon on that side, facing away from it.
- **Large areas** (a forest, a desert stretch) can be entered at their edges instead, as Golden Sun does.
- **Harbours.** A place with a jetty is a harbour. Sail into its icon and you arrive at the jetty, with the ship
  moored. Talk to Tully or take the helm to set sail, and you're on the world map beside the harbour, aboard.
- **The ship stays where you left her,** drawn on the map. In Act II, landing on any beach of Meridia or a large
  island parks her there.
- **Sail here** (from the helm or Tully) goes to any harbour you have visited (question **Sailing back to places you
  know**).
- **Story moves** you don't steer (skiff runs, storm crossings, handovers) stay a fade with a line of narration.

### 5.2 What the ground is

Every square of the map carries one kind, from our layout data, whatever the art on top:

| Kind | Walk | Surf | Ship |
|---|---|---|---|
| Deep sea, open sea | No | No | Yes |
| Shallows by a coast | No | Short hops | Yes |
| Reef and mud flats | No | Short hops | No |
| River | No | Short hops | Living hull (mission 14) |
| Lake | No | Yes | No |
| Beach | Yes | — | Lands here |
| Land, forest, desert, snow | Yes | — | No |
| Hills and cliffs | No | — | No |
| Storm (the Galeway) | — | — | Act I no. Act II between fragments |
| Fog (the north fog) | — | — | With a pilot (mission 6) |
| Fog (Westgloam's banks) | — | — | Yes, but hides islands until fog sight |
| Whirlpool | — | — | With Whirlpool |
| Stillwater | — | — | With the Flame engine (the Wayfarer has it) |
| The falls | — | — | Never: the current pushes you back |

Each square also carries its **area** (§1.9), which picks the battles, backdrop and music.

### 5.3 Battles

- On land, by area, as Golden Sun does.
- At sea, by area, at about half the land rate (question **Battles at sea**), with none in harbours, the reef lagoon
  or the Reach's channels.

### 5.4 On the Fold's screens

- **Folded,** you see about 373 by 160 pixels of world (about 23 by 10 squares). **Unfolded,** about 240 by 216.
- **Flat and top-down,** as today. Far landmarks of known regions get a small marker at the screen's edge (N-10).
- **The Lodestar** dial sits at the top centre on the world map and at sea only. It has no needle in Act I, stirs at
  mission 10 and wakes at mission 12 (N-1).
- **The place banner** shows an area's name and stars at the bottom when you cross into it.
- **The sea mini-chart** is optional and off by default (N-4).
- **The Chart** (Map, then Chart, once you have a ship): Act I's page is the Calm, the middle 4,096 pixels, with edge
  markers toward Eastwater and the rim. It shows places as unknown, rumoured (?), known (name and stars), visited or
  fully explored, plus Kin habitat marks. The whole world's page comes in Act II, the Cloudreach at mission 17 and the
  Deep Shelf at mission 18.

### 5.5 How the art is made, and what we generate ourselves

Questions **How the whole world map is drawn** and **What we generate ourselves**. Your note: where nothing we have
fits, we generate what we need.

- **Two layers, kept apart.**
  - **Our layout** is our own data: what each square is, which area it's in, where each place, door and harbour is,
    and which blocks change later. It can go in the engine's repo.
  - **The art** sits on top. Where a piece of The Lost Age's world map fits (coasts, islands, mountains, the white
    edge ring with its falls), it is cut along open sea, where the water is plain so no seam shows, and arranged to
    our layout. That art stays on your machine, like the rooms' tiles. A later redraw swaps the art and moves nothing.
- **What we generate, because Golden Sun has nothing like it:** the Galeway's storm ring and its eye, the north fog
  and Westgloam's fog banks, the Stillwaters, the bite in the rim, Marrow Isle's reef lagoon, the cloud sea of the
  Cloudreach, the Deep Shelf's floor, and any interior or district a script names that no Golden Sun room gives us
  (the hatchery, the sluice house, Fallhaven's high town, the Bazaar's hulls, the Pinnacle's districts).
- **How we generate it.** Our own tiles, drawn to Golden Sun's rules so they sit next to its tiles without a join
  showing: 16-pixel cells, its palette depth and its light from the top-left, a flat top-down view. Painted by hand or
  by an image tool, then cut into tiles and checked against a Golden Sun tile beside it on the phone. Because it is
  ours, it goes in the public repo, in the engine's `assets/own`. The same rule covers place icons, the parchment Chart
  and the opening's stills.
- **Tools.** A small compose tool takes a saved recipe (which Golden Sun piece goes where, which generated piece
  where, and painted fixes) and writes the map. The world exporter reads The Lost Age's map since 31 Oct (engine PR #89),
  so the compose tool can start. A tile check tool compares a generated tile's palette and cell edges with its neighbours.
- **Icons.** Golden Sun's own town icons where one fits, exported like the other sprites. Generated ones where none
  fits.
- **First,** a flat coloured map straight from the layout, to test sizes and routes before any art goes on.

## 6. What changes later, without a remap

The map is built in **blocks of 256 pixels** (16 by 16 squares). Every later change swaps whole blocks by story flag
(decision log 50). The base map is drawn once, and every changing block has its other versions listed in the layout
from the start.

| When | What changes |
|---|---|
| **Mission 10** | The rockslide clears (Marrow's west road). The Wayfarer moves from her cave to the cove. The reef gap opens to the Wayfarer |
| **The Breaking (mission 11)** | The Galeway breaks into fragments, with the Skyspout among them, and the eye becomes a storm knot. The Calm rises: Canalport's lower town floods, its beach and dike go under, and its upper town opens. Cockle Cay, Sandmere and Driftholm sink (Dive spots from mission 16). Shelfback, Bellstone and Farer's Step rise. Embral's top blows into a caldera. The rim moves in one block all round. Tidewarden patrols sail the Calm. Bastion Rock goes on war footing |
| **Act II** | The whole sea opens (mission 12). Meridia's walkable map is already in from Act I. Rivers open to the living hull (mission 14). Dive spots open (mission 16). The Cloudreach map opens (mission 17), then the Deep Shelf map (mission 18). The airship (mission 19) flies its own layer and lands on pads placed in the layout now: beside harbours, on the Spine's peaks, on sky isles, on Rimfall ledges and at the eye. Fog sight (mission 20) shows Westgloam's hidden islands |
| **Act III** | The Crownwater's locks open to Crown Landing and the Pinnacle (mission 21). The Vault's warded stair opens (mission 22). The Hollow's mirror rooms (mission 23) |
| **Adult mode on** | One block in the north fog gains Nightmarket Isle's icon and lane (§4.5). Off, the fog is solid |
| **After the ending** | The rim recedes beyond where it began. The lost rim towns regrow as small isles. The Farside opens over the eastern rim |

Fallhaven's lower town and archive fall in mission 9 and are gone for good. The ruin room takes their place.

## 7. Moving between rooms and places

Question **Moving between rooms**. In outline:

- **Every room change fades:** a short fade out and in (about a fifth of a second each). Story scenes keep their own,
  longer fades.
- **You arrive where you'd expect.**
  - Through an edge, you arrive at the matching edge of the next room, at the same point along it where possible,
    facing the way you were walking.
  - Through a door, you arrive just outside the matching door, facing out, with a door sound.
  - By stairs, a cave or a ladder, you arrive at its other end, facing away from it.
- **No grey.** A room smaller than the screen sits in the middle of a backdrop that fits the place: sea round a ship,
  rock in a cave, sky beside the cliff road, fog at the reef, dark in a sanctum.
- **Edges you can see.** Every room's border is a real wall: cliff, sea, trees or a row of buildings. Every road
  drawn in the art leads to a real exit.
- **One look per place.** A place's rooms are cut from one Golden Sun area where possible. The tile redraw (art 18)
  makes each place one style for good.
- **The world map.** Walking into an icon fades into the room. Leaving fades back to the map beside the icon. The
  place banner shows the room's name, and on the world map the area's name and stars.
- **Docks.** Setting sail fades to the world map with the ship beside the harbour, bow out to sea. Arriving fades to
  the jetty with the ship moored and the crew stepping off. A first arrival plays its scene.
- **Music** changes only when the place changes, with a crossfade between the world map and a place.

## 8. Order of work

1. **Your answers** (done, 24 Oct).
2. **The layout data,** written once: `places.json` and `regions.json` (menus §8.1), and the world layout (the kind
   of every square, its area, places, doors with their sides, harbours, airship pads and the later blocks). A check
   tool confirms every place is reachable exactly when it should be, and every door arrives on the right side.
3. **A flat coloured world map** from the layout, to test sizes, routes and sailing times on the phone.
4. **The world map in the engine:** icons you enter by touch, doors by side, harbours and docking, the parked ship,
   closed water by flag (storm, fog, blockades, the reef), battles at sea by area, the area banner, the Calm's Chart
   page, and Sail here.
5. **The room connections, redone against this map** (the next step): the new rooms (`marrow_cove`, `embral_cove`,
   the makers' cabin), the approved ones, the Fallhaven merge, the removed Golden Sun links, the moved arrivals, the
   fades and the backdrops. The six affected checks are reworked.
6. **The Calm's art:** write the compose tool and its recipe (the exporter reads The Lost Age since 31 Oct), and place the
   icons. All of it stays on your machine.
7. **The interior scenes and the optional places** you choose for the demo: the inns, shops and houses the missions
   walk into first, then the optional ones, with their tables, chests, finds and contracts. Generated tiles where
   Golden Sun has none.
8. **The script lines and pages in §9.**
9. **After the demo:** Meridia's walkable map (Brightcoast, the Greenwild, Dustplain, Frostmarch), Hushwater, Twin
   Bells, Sandmere and Driftholm, then the Act II blocks.

## 9. Lines and pages to fix

These followed from your answers (24 Oct). Done on 30 Oct (the design repo), except the engine's placeholder line,
which waits for the traversal branch to land, since that branch edits Stonehollow's events. mission-09.md had no "west
along the rim" line left to change.

- **story.md §2:** the sketch redrawn with compass-point quarters and the bite. "The Tradewind Bazaar to Fallhaven: a
  day and a night east" becomes "south, down the rim". The line that both voyages "read the same from wherever the
  Kestrel lies" goes, and the sailing times are reworded.
- **story.md §2 and §9:** Lantern Reef "the north Calm" becomes "the north-west Calm" (menus N-11, never written back).
- **mission-08.md:** Ketch's "Fallhaven? East, to the rim" becomes "South, down the rim". Scene 15's title "East to
  the rim" becomes "Down the rim". "Ketch ran the skiff east from the Bazaar" becomes "south from the Bazaar, down the
  rim". The summary's "sails east for Fallhaven" becomes "south".
- **mission-09.md:** the Rimborn sailor's "west along the rim" becomes "west into the storm".
- **mission-05.md and mission-06.md:** the voyage narration ("two days west", "a day and a night north") becomes a
  first-arrival line with no day count. Mission 3's first voyage keeps its narration.
- **mission-01, -03, -09 and -10 scripts:** the "in the cove" scenes name `marrow_cove` as their room. Tully's cell
  moves to the jetty.
- **mission-3-build.md:** "east across the Calm" becomes "south" (the approved script says south).
- **The engine's placeholder line** in Stonehollow's voyage scene says the Kestrel sailed "east" to Brightcoast. It
  becomes "south".
- **BRIEF.md** still sends agents to `docs/phase1/WORLD_PROPOSAL.md` for traversal and biomes. That page contradicts
  story.md's rings. Point it at the world map page instead.
- **menus-and-navigation.md §8.8** sizes landmarks against Golden Sun's Angara map. Update it to the new size.

## 10. The questions on the decision page

Nineteen questions, in `questions.json`, on the decision page's Open questions tab (open questions 74 to 92):

**World map: layout**
1. The four quarters of the Wide
2. Fallhaven, the storm and the Bazaar
3. The Spine and the Pinnacle's river
4. Marrow Isle's shape
5. Where the sky and undersea layers sit

**World map: how it works and looks**
6. What keeps you out in Act I
7. Sailing back to places you know
8. The voyage lines in the scripts
9. How big the world is
10. Battles at sea
11. Moving between rooms
12. How the whole world map is drawn

**World map: places to explore**
13. How much optional content the demo has
14. When Marrow Isle's west road opens
15. A contract board for Crew 1
16. The three isles that sink

**World map: scenes and generated art**
17. Towns as several scenes
18. What we generate ourselves

**World map: the hidden town**
19. The adult-only hidden town

**Left for later, with no question now:** the names of the new islets (Cockle Cay, Sandmere, Driftholm, Shelfback,
Bellstone, Farer's Step, the Churn) are working names. Which three monsters and Kin live in each area is the
encounter-table work (demo slice 10). Where mission 12's crossing to Marrow Isle is sailed from, and who sails it, is
for mission 12's script.
