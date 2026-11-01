# Visual survey: what looks off in the game now (1 Nov 2026)

You asked (1 Nov) for a look at the maps, places and sprites as they are in the game today, with notes on what is
visually off, so the next art pass can fix it and bring in the item art and the hero creator. This page is that survey.
It changes nothing in the game. The real choices it raised are on the decision page under "From the visual survey". A
fault with only one sensible fix is listed here and not asked.

The art rules it measures against are all decided: Golden Sun's own room tiles at 2× (art 8), LPC people from the
generator (art 3-5, art 17), Kenney fonts, frame, prompts and touch faces (art 6, 14), the UI's navy and its presets,
Pokémon battle sprites from the expansion (open 51), and generated art only where Golden Sun has nothing, drawn in code
to its palette (open 91, 102). [asset-priorities.md](asset-priorities.md) is the plan of what to make and reuse.

## 1. How the survey was made

- **The build:** engine main `cf7cf22`, with Fallhaven's rooms, the field sounds and the world map merged.
- **The pictures:** the engine's own capture tools took every room whole at one pixel per world pixel, the field as the
  cover screen draws it, and the fold shots of menus, battles and screens. They were put together into 21 contact
  sheets. Two inspections looked at each sheet once: one at the places, one at the people and the screens. A few facts
  were checked in the room files, such as what a prop is called and what it says. A second pass the same day added
  four sheets: the pictures the first pass left covered, and the inner screen (§8).
- **Where they are:** the pictures hold Golden Sun and third-party art, so they stay on the PC and never enter this
  repo. The sheets, the shots, the tools and a notes file (`sheets.md`) are in
  `C:/Users/aaron/Documents/UnboundHack/notes/visual-survey-2026-11-01`. A copy of the sheets for the phone is in
  `OneDrive/Apps-Roms/_GameMaker-builds/visual-survey-2026-11-01`.

| Sheet | What it shows |
|---|---|
| 01 | Marrow Isle: Brann's cottage, Stonehollow by day and night, the Vault's upper halls, Marrow cove by day and night, the sea caves |
| 02 | Fallhaven's lower town in each state (mission 2 at dusk, after the street falls, mission 9 at night, fallen by day and night) and the archive |
| 03 | Fallhaven's harbour, cliff road, high town and west cove, each by day and night |
| 04 | Canalport by day and night, the Forge hall, the Forge sanctum, the Wayfarer's deck |
| 05 | The Eldergrove village, the Greenwild and the Eldergrove's heart, each by day and night |
| 06 | Lantern Reef and Bastion's strand by day and night, the Bastion jail, the Tradewind Bazaar by day and night |
| 07 | The field as the cover screen draws it, with the touch controls on |
| 08 | The dialogue box, the opening's still, a list question, the place and objective banners |
| 09 | The title, the Start menu, the Items list and a 16-kind bag sample, Said, a long choice list, the are-you-sure box |
| 10 | Settings, save files, the pause box, the ask box, the debug menu, Remap controls, the controller test |
| 11 | The Pokémon menu, its row and pick list, the nickname entry, Skip scene, the Kestrel's Set sail list |
| 12 | Battles: the first command, battle words, four Adepts with partners, six enemies, the sluice beast |
| 13 | Pokémon battles (a wild Greenwild battle, Ho-Oh's judgement, Corvin's and Tamsin's fights): covered, taken again as 22 |
| 14 | The hero creator, and the top of the LPC hero's frame contact: tiles 2 to 4 covered, taken again as 23 |
| 15 | WorldMapTest, the debug flat map |
| 16 | The world map in the game: aboard, on foot, by day and night, and at the fog and storm edges |
| 17 | The Chart from the Start menu, in Sail mode, a place's details, and the whole world zoomed out |
| 18-20 | The LPC cast and townsfolk looks from `compose_lpc.py`, every facing |
| 21 | The item icon art: the DCSS atlas and the expansion's Poké Ball and Great Ball |
| 22-25 | The second pass (§8): sheet 13 and sheet 14's covered tiles again, the field and the screens on the inner screen |

**Gaps the first pass left.** A Set sail chart left open by the capture before covered all four pictures on sheet 13
and three of the four on sheet 14. The second pass took those seven again with every list closed (sheets 22 and 23,
§8). Check in play that the list can't stay open across a scene change. No LPC person is on the field yet (§3), so
their size against Golden Sun's tiles can only be checked once slice 6 puts them there. Take sheet 07 again then.

**Severity.** High: seen at once, or it breaks a room's look. Medium: noticed when you look. Low: a detail.

## 2. Places

### 2.1 Marrow Isle

| Room | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| Brann's cottage (`hero_house`) | The two rooms are joined by a strip of green carpet across black space, with no walls. Dark cone-shaped wedges sit in the walls where the strip meets each room, and on the outer walls. | hole | Medium | A back room through a door, or a walled hallway (on the decision page). Golden Sun's door-opening tiles in place of the wedges. |
| Stonehollow | A yellow-topped grey post at the foot of the west cliff looks like a placeholder marker. It is most likely the Memorial stone. | placeholder | Medium | A Golden Sun monument or gravestone sprite. |
| Stonehollow | The small blue oval east of the falls is the Blue puddle, which is meant (a story clue: it hasn't rained in a week). It reads as a stray blob. | placeholder | Low | A hard-edged puddle sprite in Golden Sun's style, still startling blue. |
| Stonehollow | At the bottom edge the camera shows black past the map, a third of the screen. At the top edge the hero stands in the black above the drawn tiles. | hole | Medium | Clamp the camera to the room, centring rooms smaller than the view. Block the top row or give it tiles. |
| The Vault's upper halls (`vault_halls`) | Flat purple slabs pasted on a repeating blue-brick fill, with no walls, wall tops, edges or depth. Only the statues, the pits, the rail, the boulder and the log are real art. The room is meant to be a clip of Sol Sanctum, so the clip has lost its wall and edge tiles. | placeholder | High | Clip it again from Sol Sanctum at 2× with its walls and edges. Keep the placed statues, pits, rail, boulder and log, and the sandstone entrance at the south. |
| Marrow cove | A black column runs down the whole east edge. At the north-west corner the grass runs straight into the sea with no shore. The water round the jetty's west posts is a darker block, clearer at night. | hole, seam | Medium | Fill the last column or trim the room and camera by one tile. Golden Sun shore or cliff-face tiles at the corner. Draw the posts over the common sea layer. |
| The sea caves (`sea_caves`) | The sand floor floats in pure black with a glowing purple-and-green moss rim and no rock walls, so the black reads as a hole. The orange orb in the north alcove is the cave mouth's light (the room's notes call it that), but it reads as an item. | placeholder | High | Clip it again from Fuchin Falls Cave with rock walls and wall tops round the floor and water edges round the pool. Keep the statue in the water and the pool's shape. Draw the mouth as an opening with daylight. |
| The sea caves | A row of green checkered grass runs along the bottom edge and up the east edge, outside the cave. A square of different brown dirt sits in the north-east corner of the floor. | stray tile | Medium | Remove the grass row and column, or fill them with rock. Repaint the patch with the floor's own sand. |

### 2.2 Fallhaven

| Room | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| The lower town (`fallhaven_lower`) | A person-shaped figure by the west house is all white or grey, beige at dusk and bright white by day, like a person with no palette. It is probably the relay stone, whose sprite also stands in the archive. | colour | Medium | Check the relay stone's sprite and give it a stone, not a figure. |
| The archive (`fallhaven_archive`) | The same white figure stands in the top-right room. | colour | Medium | As above. |
| The harbour (`fallhaven_harbour`) | At the north-west corner the grass meets the sea in a straight line with no shore. | seam | Medium | Golden Sun shore or cliff-face tiles. |
| The cliff road (`fallhaven_cliff`) | The cave mouth in the middle ledge is a plain black box with no rock rim. Down the east side, narrow strips of cliff and grass repeat, as if stitched together. | seam | Low | Golden Sun's cave entrance with a rock arch. One continuous cliff face down the east side. |
| The high town (`fallhaven_high`) | The grass is a pale mint beside the lime green of the cliff road and harbour, so the colour jumps when you walk up. Round yellow-and-black signs by the doors read as hazard signs. One door is purple among orange ones. | colour | High | On the decision page: match Fallhaven or keep Lunpa's look. |
| The high town | Small crates and boxes are scattered at random over the open grass. | stray tile | Medium | Gather them against walls, or remove them. |
| The west cove (`fallhaven_cove`) | At night the beach sand goes concrete grey. Its sea is deep royal blue where most rooms' sea is bright cyan. | colour | Low | The night tint and the sea colour, both on the decision page. |

### 2.3 Canalport and the Forge

| Room | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| Canalport | A side-on picture of sky, clouds and the sea's horizon fills the top-down town's north half, over a flat empty sand field. The west grass ends in a straight vertical line against the sky. | style mismatch | High | Top-down open sea from Golden Sun water tiles, meeting the sand with foam and a shore edge. A cliff or shore edge for the grass. Beach props (rocks, nets, boats) on the sand. |
| Canalport | The canal is a straight bar of square water tiles with every tile edge showing as a grid line, and no banks. | seam | High | Seamless animated Golden Sun water, with stone bank edges from Alhafra's own harbour, and a bridge or stepping stones where people cross. |
| Canalport | A one-tile pale stone strip stands alone north of the canal and ends at nothing. A pale green rectangle lies under the hero at the entrance. Both match the room's two under-actor patches, so that layer is the likely cause. | stray tile | Medium | Check the under-actor patches' tiles. Make the strip a real jetty with posts and an end, or remove it. |
| Canalport | A clump on the sand by the entrance is rainbow-coloured (pink, blue, yellow, green), likely a flower or coral tile on the wrong palette. | colour | Medium | Give it its right palette. |
| The Forge hall (`forge_hall`) | The two pits on the cobbled floor are smooth blurred ovals with gradient edges. | style mismatch | Medium | Golden Sun pit tiles with hard edges and a rim. |

### 2.4 The Wayfarer

| Room | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| The deck (`wayfarer`) | The starboard gangplank runs out into open sea and ends in the water. A yellow pole sticks out past the port rail. | stray tile | Medium | Show the gangplank only at a dock. Remove the pole, or stow it as an oar inside the rail. |
| The deck | The deck's objects are the helm, the engine, the chart table with the Lodestar, and the muster roll. Two of them use stand-in sprites: a bright green lattice and a clock face, off the deck's palette. | placeholder | Medium | A glass-and-fire engine and a chart table with the Lodestar in its cradle, in the deck's colours. |

### 2.5 The Eldergrove

| Room | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| The village (`eldergrove`) | Dark teal see-through rectangles with hard square edges lie on the grass north of the middle crates and beside the fence pen, like shade drawn as boxes. | layer | Medium | Find their layer and remove them, or use Golden Sun's soft tree-shade tiles under the canopies. |
| The Greenwild (`greenwild`) | A large grey-purple see-through box lies on the grass south of the stream. It is most likely the poison swamp (the room's hazard cells) drawn as a flat box. | placeholder | High | Draw the swamp with Golden Sun's swamp tiles and hide the debug box. |
| The heart (`eldergrove_heart`) | In the south clearing the teal shade meets the lime grass in square blocks that don't follow the trees. | seam | Low | Golden Sun's grass-edge tiles, or a shade that follows the canopy. |

### 2.6 Lantern Reef

| Room | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| Lantern Reef (`lantern_reef`) | One pale veil lies over the whole room, so the decks, people and water look faded. At night the room turns a flat grey-blue. The fog is meant (Defog clears it); how it should look is on the decision page. | colour | High | As decided. Until then, a lighter veil. |
| Lantern Reef | The wreck is the planned placeholder (a Golden Sun ship broken in three by painted sea, with Reveal's planks between), but the cuts are clean straight lines, so it looks like a cut picture rather than a broken hull. | style mismatch | High | Jagged broken ends with splintered planks on each piece. More hulks round it can come with the graphics pass, as mission-6-build.md says. |
| Lantern Reef | A grey strip runs down the full east edge. At night a blue oval and a dark plank appear on the rear decks and read as a puddle and a stray beam. The oval may be the old lantern's Litwick glow. | hole | Medium | Fill or trim the east column. A hard-edged glow sprite for the lantern, if that is what it is, and remove the stray plank. |

### 2.7 Bastion Rock

| Room | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| The north strand (`bastion_shore`) | It looks like a copy of Marrow cove: the same jetty and jars, the same thatched house and cliffs. Nothing says fortress. | style mismatch | Medium | Its look is on the decision page. |
| The north strand | The same faults as Marrow cove: a black east column, the straight grass-to-sea corner, the darker water block by the jetty. A small blue oval lies south of the house. | hole, seam | Medium | The cove's fixes. Check what the oval is meant to be. |
| The jail (`bastion_jail`) | It reads as Brann's cottage (sandy walls, green carpet) with rows of bars added, not as a jail. It is meant to be Madra's jail. The west exit is a plain black opening. | style mismatch | Medium | Clip Madra's cell block again: stone floor and walls, real cell doors. |

### 2.8 The Tradewind Bazaar

| Room | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| The Bazaar (`tradewind_bazaar`) | A rectangle of open sea sits inside the hull at the bow, with a beige sail piece in it. It is the planned gap to the merchant's hull that Whirlwind's spar bridges, but it reads as a hole through one ship. The dragon prow is cut off by the room's east edge. | hole | High | In the interiors job: the merchant's hull as a separate hull with its own rail, the furled sail on its deck, the whole prow inside the room. |
| The Bazaar | One hull and a few people: no stalls, awnings or goods, so it reads as unfinished for a market. A grey plank lies across the starboard rail by the gangplank. | placeholder | Medium | The lashed hulls the mission calls for, with stalls, awnings, crates and goods. Place or remove the plank. |
| The Bazaar | At entrance 0 (mission 8) the hero arrives standing on open water beside the gangway. | other | Medium | Move entrance 0 onto the gangway. |

### 2.9 Across many rooms

| Where | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| Every open-sea room | Bright cyan sea in five rooms, deep royal blue in two, so the ocean looks like two seas. | colour | Medium | One open-sea water (on the decision page). |
| Every outdoor room at night | One flat blue tint: sand goes grey, thatch stays bright yellow, and no window or lamp lights up. | colour | Low | On the decision page. |
| Exits in six rooms | Smooth white-gold gradient glows beside the pixel art (Brann's cottage, the jail, the Forge hall and sanctum, the sea caves). | style mismatch | Low | On the decision page. |

### 2.10 The world map and the Chart

| Screen | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| The world map | Every square is one flat colour (light green land, beige sand, brown mountains, cyan shallows, blue sea), the coast is stair-stepped, and places are plain coloured squares. This is planned: the art stays flat until world-map step 6. | placeholder | High | Step 6: The Lost Age's world-map pieces, the generated fogs and storm ring, Golden Sun's town icons. |
| The world map | The Kestrel is a plain brown block. | placeholder | High | The ships job: a small ship with 4 or 8 facings and a wake. |
| The world map | The north fog is near white, while the fog sea and the Galeway are mid grey, and the storm has no clouds or rain. On the white fog the joystick ring almost vanishes. | placeholder | Medium | Step 6's fogs and storm ring. A dark outline on the joystick ring. |
| The world map at night | Sand and cliffs turn the same grey as the fog edges, so beaches read as fog. | colour | Medium | A night tint that keeps land in its own hues, darker and bluer. |
| The world map | The ship draws over the end of the "Canalport" label. On foot the hero is about two squares tall beside one-square towns. | layer | Low | Draw labels above the ship. The size gap closes once town icons replace the squares, since Golden Sun also draws its full field sprite on its map. |
| The Chart | The Start menu and party panel show through the Chart: "Follow the story" and two HP rows inside the details pane, and "Close / Send report / Debug" and Eevee's row under it. The area banner peeks out under the header, and the old banner's text ghosts in the header bar. | layer | High | Solid panels over a full dim layer. Hide the Start menu, the party panel, the area banner and the place labels while the Chart is open. |
| The Chart | The map disc is a small thumbnail beside a large, mostly empty details box. The map is flat (two greens split by a straight line, straight rivers), places are plain squares, and "?", "*" and "**" stand for unknown places, stars and Visited. | placeholder, scale | Medium | The layout is on the decision page. The look is decided: the terrain grid with Kenney Cartography icons now, real star glyphs and a ship marker, a painted chart later. |
| WorldMapTest (debug) | The "Tortell's Isle" label runs under the R button. The flat blocks are fine for a debug map. | other | Low | Keep labels clear of the L and R buttons. |

## 3. People and sprites

| What | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| Everyone on the field | No LPC person is on the field yet. The cast table maps 27 LPC looks, but no room row names a cast id, and the hero comes from a Golden Sun sprite (blue tunic, red sash). Rowan's LPC look and the townsfolk looks appear only on the contact sheets. | missing | Medium | Slice 6: cast ids in each room's events and the hero on the LPC sheet. Then take sheet 07 again to check height against doors and tiles, the foot shadow, and colours under the night tint. |
| Partner Pokémon in battle | Every back sprite uses its shiny palette: Treecko is mint behind Rowan, Torchic's back is yellow, Mudkip's purple, Eevee's silver and Pikachu's orange. Every front sprite is right. The expansion's back pictures carry the shiny palette. | colour | High | Import the back sprites again with each species' normal palette. Keep the shiny palette for real shinies only, and add a test that front and back share a palette. |
| The hero in battle | Always Golden Sun's Isaac (blue tunic, yellow scarf, gold shoulders), whatever the creator chose. It won't match the LPC hero on the field. | style mismatch | Medium | Slice 7: LPC battle rows from the creator's look. |
| Battle with six enemies | Every enemy drops to half size, as art 10 decided for five or more, but the last one is cut off by the right edge and the name labels float at uneven heights. | scale | Medium | A two-row staggered line that stays inside the view. Labels at a fixed offset from each sprite's top. |
| Tamsin, Nerissa, the Merchant (LPC) | Tamsin's red fringe falls over her eyes in the front and side views and reads as a red mask. Nerissa (east and south-east) and the Merchant (side views) have the same problem. | other | Medium | A hair style with the fringe above the eyes in `lpc_recipes.json`, or the fringe moved up a pixel. |
| Archivist, Rimborn townswoman, Innkeeper, Captain Sael (LPC) | The Archivist's glasses read as one yellow blob. The townswoman's grey cap sits on her curls like a bowl. From behind, the Innkeeper's bun is a dark ball and Sael's braids read as a grey cloak. | other | Low | Thinner glasses, a lower or recoloured cap, a lighter bun, shorter or parted braids. |
| Commodore Ilse (LPC) | Her pointed blue hat reads as a wizard's hat, and from behind her hair is a grey sheet down to the floor. | other | Low | On the decision page. |
| Maestro Bonewhistle (LPC) | His face reads as a skull under a black mop of hair. That is meant: he is a skeleton. | — | — | No change. |
| Every LPC look, the diagonals | The diagonal facings reuse the side frames, so walking up-left or up-right shows the face. Art 3 decided this. | other | Low | No change now. |

## 4. Items and the character designer

### 4.1 Item art

**What exists.** The DCSS atlas (`assets/ui/item_icons.png`, 512×384, about 180 icons of 32 px: amulets, armour,
helmets, gloves, boots, shields, food, potions, rings, staves, swords, axes and maces). The expansion's 767 item
pictures of 24 px in `assets/pokemon/items` (balls, berries, mints, held items). Transparency is right in both.

**What is off.**

| What | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| Herb, Nut and Mint (items 180, 181, 195) | No icon. Only Potion's row in the bag has one, so the list looks half-finished. | missing | Medium | Draw them, as art 14 decided, in code to Golden Sun's palette. |
| The bag | The 16-kind sample shows only Herb, Nut, Potion and Mint, even scrolled. The Poké Balls, the key item, the weapons and the armour never appear, so their icons can't be seen in the game. | missing | Medium | The six decided pockets (items 17), each listing what the bag holds. Then take the bag sample again. |
| Icon styles | DCSS's soft-shaded, many-coloured 32-px icons sit beside the expansion's flat 24-px balls. In the bag the potion is squeezed to about 19 game px, with a black tail on its right. | style mismatch | Low | Art approval 4 already says icons show at full size in the item detail box, not squeezed into rows. In rows, one size scaled by whole numbers. Trim the potion's tail. |
| The Poké Ball | Its top is orange, from the expansion's own colours, and reads wrong next to the red potions. | colour | Low | The balls are to be drawn (art 14); draw them red. |

**What to bring in next.** Draw Herb, Nut, Mint and the balls (art 14, open 102). Wire the six pockets and the full-size
detail box. Then the weapons and armour from DCSS fill the Gear pocket. This is asset-priorities.md §2.8.

### 4.2 The hero creator

**What exists.** Rows for Name, Gender, Pronouns, Voice, Skin (6), Hair (10), Eyes (6), Outfit (3), Colour A and B (10
each) and Accessory. `compose_lpc.py` makes a full LPC Rowan sheet (8 facings, idle and walk).

**What is off.**

| What | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| The preview box | Empty when the creator opens, and with every look after it (sheet 23): the hero is drawn above the top of the screen (§8.2). | missing | High | §8.2's fix. The preview already loads again on every change. |
| The cosmetics | Changing Skin, Hair, Eyes, Outfit, the colours or the Accessory changes nothing on screen. Only Gender swaps the preview's sprite, to another Golden Sun one, and not even that shows until §8.2's fix. | missing | High | Art 5's pre-composed sheets with colour keys and the palette shader, used in the preview, on the field and in battle. |
| The value column | Choices show as "<1/6>" and "<1/10>" with no swatch or name, starting at a different x on each row. It reads like a debug list. | placeholder | Medium | Swatches for skin, hair, eyes and the colours. Names for hair styles, outfits and accessories. One value column, with left and right arrows you can tap. |
| The touch controls | The joystick and A and B draw over the creator. | layer | Medium | Hide them while it is open. |
| Portraits | None. | missing | Low | After the demo (asset-priorities.md §1.7). |

**What to bring in next.** The hero kit from the LPC generator (asset-priorities.md §2.1, art 5): the six styles, three
outfits and three accessories on both bodies, keyed for the colours. A girl hero on the female body does not exist yet
(only "hero" on the male body), so it is part of the kit. Then the hero's battle rows (asset-priorities.md §2.5).

## 5. Screens and UI

| Screen | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| Stacked menus (Settings, save files, debug, Remap, controller test, Said, nickname entry, the Chart, the ask box) | Windows are see-through, so the window underneath shows through as ghost text ("Text speed: Normal", "Resume", "Rowan L9 HP 69/69"). Slivers of the lower window also show where two boxes overlap by a few pixels. | layer | High | On the decision page. Either way, snap stacked windows so they don't overlap. |
| Battle with three or four Adepts | The command box sits on top of the party. The back Adepts (Sorrel, Vesper) and their partners are hidden, and the rest pile on top of each other. | layer | High | Move the command box and the target list to a strip along the bottom, or to the right below the enemies, until the decided Golden Sun icon row comes (B-1). Spread the party on a diagonal with each partner behind its Adept. |
| Every battle | No background: a flat dark green. | placeholder | High | Art 11's Pixel-boy scenes, and The Lost Age's ship deck at sea (asset-priorities.md §2.6). |
| The battle party box and the status pane | HP and PP are bare numbers with no labels or bars, "*" is a separator, "EXP -" shows a dash, "Repeat -" sits in the command list, and there are no faces. | placeholder | Medium | Labelled HP and PP bars like Golden Sun's, real EXP or an EXP bar, Repeat greyed out, faces when portraits come. |
| The Pokémon menu and its pick list | Text only ("*Treecko L5"), with no icon, HP bar or sprite, and "*" for partner. | missing | Medium | The expansion's menu icons (asset-priorities.md §2.8), an HP bar, a small partner badge. |
| The dialogue box | No speaker faces, only the name tag. | missing | Low | Portraits after the demo (asset-priorities.md §1.7). Leave room for the slot. |
| The title screen | "HALCYRA" in the menu font on flat navy, with a two-row box. | placeholder | Medium | Demo 25's painted title card: the Wayfarer under the Pinnacle, a drawn logo, sea and cloud parallax (asset-priorities.md §1.3). |
| The opening's still | Flat navy with a heading and "The world from above, out to its rim", with no picture. | placeholder | Medium | The painted still (asset-priorities.md §1.3). |
| Text in the menu font | Lowercase l and k are small capitals, so "Fallhaven" reads "Fauhaven" and "Stonehollow" reads "Stonehouow". | other | Medium | On the decision page. The dialogue box does use Kenney Pixel 16 (art 6), and it draws l and k the same way (§8.3). |
| Touch controls | The grey A and B and the thin grey joystick ring almost vanish over bright grass. The joystick and A and B draw over the Pokémon menu, the creator and the INN sign. | other | Medium | A dark backing disc at about half opacity with a light outline. Hide the joystick while a full-screen menu or the creator is open. |
| The cover screen's scale | The sheet shows the 746×320 view stretched by 3.375 to fill 2520×1080, so pixel columns come out uneven: Stonehollow's grass shows bands that will shimmer when scrolling. | scale | Low | art-integration.md §3b settled 3× with thin bars (141 and 60 px). Check on the phone and scale by exactly 3. |
| The Start menu and the pause box | Both show the "Send report" and "Debug" rows. | other | Low | Right for the playtest builds (open 34). Hide them behind the debug flag in a release build. |

## 6. Adult mode

Adult mode has nothing on screen to survey yet. The only built piece is the world map's hidden town, which shows only
while the adult flag is set, and nothing in the game sets it; it is drawn as the test map's debug marker. Everything
else is unbuilt, and no adult art is in the engine or in any repo. The inventory of what exists and what each piece will
need visually is text only, kept on the PC outside every repo, and its questions are on the private decision page.

## 7. What already looks right

Keep these as they are.

- **Stonehollow** by day: the Golden Sun Vale tiles (cliffs, waterfall and river, rope bridge, thatched houses, autumn
  trees) read as true Golden Sun. By night the blue tint reads as night without hiding anything.
- **Fallhaven's cliff road** by day and night: cliff and ledge tiles, lime grass that matches the harbour, consistent
  boulders and paths.
- **Fallhaven's harbour**: the jetty with jars, the wooden stairs up the cliff, the fence and the red tree.
- **The fallen west cove**: broken pier sections in the water, the wreck, the beach and the cliffs read clearly as a
  ruined harbour.
- **The high town's well** and the log-palisade gate with blue double doors at the south.
- **The Eldergrove village**: tree-trunk houses with doors, the INN sign, barrels and crates, the fence pen and the
  forest border.
- **The Greenwild**: the stream with log bridges, the cliff lips and the mixed red, green and blue trees.
- **The Eldergrove's heart**: the two giant trunks with vines and the dense forest frame.
- **The Forge sanctum**: railing walls, four fire braziers, the statue on its platform, the red rug. **The Forge hall**
  apart from its pits: railing walls, banners, cobbled floor, wooden platform.
- **The Wayfarer**: the Golden Sun ship hull and deck read well from above.
- **The Tradewind Bazaar's hull**: the ship with its dragon prow, the sterncastle and the gangplank down to the bottom
  edge.
- **Canalport's south-west**: the pale green stone tower, statues, cliffs, stalls and ruins share one palette.
- **Indoor rooms** stay untinted at night.
- **The world map's UI**: the area-name pills, the Lodestar dial, the place labels in the Kenney font, the night tint
  switching on. **The Chart's framework**: the round disc with its fog ring, and the Sail menu (Set sail, Sleep,
  Details, Back) in the navy panels with white frames.
- **Golden Sun's enemy battle sprites** (Vermin, Horned Ghost, Undead, Bone Fighter, Thief) are crisp, and the sluice
  beast's two halves join with no visible seam.
- **The hero's Golden Sun battle sprite** and the following Treecko, Torchic and Mudkip on the field, in their normal
  colours and at a scale that fits.
- **The dialogue box**: navy fill, white double border, name tag, next-page arrow, two-line pages that read well. The
  place and objective banners are short and centred, and the red "!" emote reads clearly.
- **Short lists and questions** (Trade whom?, Yes/No, the move-forget list) are clean, and pausing dims the field.
- **The Kenney prompts**: the hand, the A and B faces, and the L, R and Start buttons look the same everywhere.
- **The LPC cast and townsfolk** on the contact sheets: clearly different colours for each person, the same outline and
  shading weight throughout, children drawn smaller, readable walk and idle frames, and Rowan's spiky gold hair and
  yellow scarf echoing Isaac.
- **Item art transparency**: no background squares in the bag.

## 8. Second pass (1 Nov): the retakes and the inner screen

The first pass left seven pictures covered and took nothing on the Fold's inner screen. A second pass the same day, on
the same build, took them on four more sheets. One inspection looked at each new sheet once, and the causes below were
checked in the engine's code and files.

| Sheet | What it shows |
|---|---|
| 22 | Sheet 13 again with every list closed, at the cover: the Greenwild's wild battle, Ho-Oh's judgement, Corvin's and Tamsin's fights |
| 23 | Sheet 14's tiles 2 to 4 again, at the cover: the creator's default look, Girl, and the boy with every cosmetic changed |
| 24 | The field on the inner screen: Stonehollow, the lower town, the arrivals at Canalport, the Eldergrove and Lantern Reef, the world map off the cove |
| 25 | The inner screen's screens: a villager's words, the Start menu, a full battle, the Chart |

The inner screen draws a 480×432 view at 4×, a whole number, so its pixel columns come out even, which the cover's
stretch does not (§5). Against the cover's 746×320 view it shows 112 more rows and 266 fewer columns.

### 8.1 Pokémon battles (sheet 22)

| What | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| Partner Pokémon from behind | The retake bears out §3: Treecko is mint, Torchic yellow and Eevee silver. Corvin's Larvitar is pale green from the front in mission 1 and olive from behind in mission 4, when his crew is yours. It is the whole back set, not only the starters: in the files Riolu's, Combee's and Ho-Oh's backs are off too, and a rough check of each picture's main colour flags about two in three of the 1,309 species. The foes' fronts (Combee, Ho-Oh, Larvitar, Riolu) look right. | colour | High | §3's fix for every species at once: export every back again with the normal palette, and run the front-and-back palette test over the whole set. |
| The command window | It covers the party with only two Adepts too. In the wild battle and Ho-Oh's, Maren is hidden but for a wisp of hair, and Eevee's back is half under it. | layer | High | §5's fix: move it off the party. |
| Corvin and Tamsin | Both rivals are drawn as Golden Sun's Thief, the engine's stand-in for every trainer's Adept (enemy 22), so they look alike and like the Thief an ordinary battle sends (sheet 25). On the field they are LPC people. | placeholder | Medium | Slice 7's LPC battle rows (assets §2.5) for the rivals too, facing the party. |
| Corvin on your side (mission 4) | Corvin's crew borrows Isaac's battle sheet, the same as the hero's, so your Corvin looks exactly like Rowan. | placeholder | Medium | Slice 7's LPC rows for every Adept. Until then, borrow a sheet the hero doesn't use. |
| The foes' names | "Corvin" and "Tamsin" sit across their partners' heads, since each partner stands just behind and above its Adept. | layer | Low | Place a trainer's name above the taller of the pair. |

The wild battle has the plain green of every battle (§5's backdrops).

### 8.2 The hero creator (sheet 23)

| What | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| The preview | Empty with every look: the default boy, Girl, and the boy with skin 4, hair 7, eyes 5, outfit 3, colours 6 and 9 and the Headband. The rows take each value, so the creator holds the look, but the frame shows only its fill. The code shows why: the field sprite sets its own height every physics tick (`FieldActorSprite.set_air`, y 0 when nothing walks it), so the preview the creator places in the frame jumps to the top of the screen and draws above it. A speck at the top edge, straight above the frame, is all of it that shows. | missing | High | Put the preview in a holder node placed in the frame, with the sprite at the holder's origin, and add a test that the preview draws inside the frame. Then take sheet 23 again to judge Girl and the cosmetics. |

Gender steps Pronouns to She, as it should. The rows' other faults stand as §4.2 and §5 found them: the value column
starts at a different x on each row, and "Girl", "Colour" and "Talkative" show the small-capital l.

### 8.3 The inner screen (sheets 24 and 25)

| Where | What is off | Kind | Severity | Suggested fix |
|---|---|---|---|---|
| A full battle | The enemies stand top right, level with the foot of the status box. The party stands bottom right, and the command window covers most of it: only a red-haired Adept and the edges of the partners show. The left half below the status box is empty but for the stick. On a tall view the code stacks the party below the enemies and starts its line right of the stick, and only the enemies' line keeps clear of the command window. | layer | High | Make the command window an obstacle for the party's line, as it is for the enemies'. On the inner screen, stand the party across the empty left half above the stick. The decided icon row (B-1) replaces the window later. |
| Canalport's arrival (entrance 0) | The view opens on open sea, with the hero at the top end of a pale green strip that runs out into the water, sand and the rainbow clump below, and none of the town in sight. The strip is §2.3's under-actor patch. | stray tile | High | Move entrance 0 onto the town's ground, facing the town, so the first view shows the town on both screens. Then §2.3's fixes for the patch and the north. |
| The Chart | As on the cover (§2.10), the Start menu's rows ghost through, and a line under the header "The Calm" is cut off. Here the disc is a small square in the middle with an empty pane each side, and the Start menu's window, which runs to the bottom edge on this screen, peeks out under the Chart at the bottom left. | layer, scale | High | §2.10's fix: solid panels over a full dim layer, with the Start menu hidden. The layout is on the decision page. |
| The touch controls on the field | They are the same size in view pixels on both screens, so here the stick's ring is nearly a quarter of the view's width (a seventh on the cover) and about a fifth bigger on the glass. Where the camera stops at a room's edge the hero walks beside them: at the Eldergrove's arrival he stands just above the stick. L, A and B almost vanish over the Eldergrove's trees and Stonehollow's falls, as §5 found over grass. | layer | Medium | How they sit on this screen is on the decision page. Either way, §5's dark backing. |
| The Start menu | Both windows run the full height of the view. The rows fill the top half of a window down the left to the bottom edge, and the status window top right (the objective, the coins, Rowan's line) is two thirds empty. Both are see-through, so the falls show through them (§5). | scale | Medium | Size each window to its rows on every screen. |
| The words | The box across the top reads well in Kenney Pixel at 16, the dialogue font art 6 chose. But Kenney Pixel also draws l and k as small capitals: "bLows bubbLes", "MudKip". | other | Medium | The font question on the decision page now covers both fonts. |
| "Pokémon" in the menus (sheets 22 and 25) | The menu font's é is a capital, so the Start menu's row and the battle's command read "PokÉmon". | other | Medium | Draw a small é in our copy of the font, with l and k (on the decision page). |

Lantern Reef shows §2.6's veil and the world map §2.10's brown block for the Kestrel, as on the cover. The area banner
and the Lodestar's dial sit clear of the picture's middle.

**What looks right on the inner screen.**

- **The whole-number 4×:** Golden Sun's tiles are crisp, with no uneven columns.
- **More of each place round the hero:** Stonehollow's falls and cliffs, the lower town's houses and well, and the
  Eldergrove's root-trees with their doors read as true Golden Sun.
- **No black band** past a room's edge in the six field pictures. The edge shots (fold 27 and 28) were not taken on
  this screen.
- **The stick hides** while the Start menu is open, and the words read comfortably at 16.

**Still to take.** Stonehollow's top and bottom edges, the creator, the bag, Settings and the save files on the inner
screen; sheet 23 once the preview draws; sheet 07 once slice 6 puts LPC people on the field.

## 9. The order to fix things in the next art pass

High first, then by how often you see it. Where a fix belongs to a row of asset-priorities.md, the row is named as
"assets" and its number.

**High, most seen first**

1. **Solid menu windows**, once you choose, and the Chart's see-through panels, with the Chart's layout once you
   choose. Every menu shows it. On the inner screen, windows sized to their rows (§8.3). An engine fix, no asset row.
2. **Battle:** the back sprites on their normal palette for every species, not only the starters (§8.1, a fix to the
   Pokémon sprites already in, assets §3), the battle backgrounds (assets §2.6, art 11), and the command box moved off
   the party, which it covers from two Adepts up, with the party in the inner screen's empty left half (§8.3; the icon
   row later, B-1).
3. **The hero creator's preview,** which draws above the screen (a small engine fix, §8.2), **then its cosmetics:** the
   first screen of a new game (assets §2.1, art 5).
4. **Fallhaven's high town colour**, once you choose: a hub from mission 2 on (assets §1.1 names the high town).
5. **The world map's art and the Kestrel:** every voyage (assets §1.2, §1.4, §1.5 and §2.3: world-map step 6).
6. **The placeholder rooms, in mission order:** the Vault's halls (mission 1, clip Sol Sanctum again), the sea caves
   (mission 2, clip Fuchin Falls Cave again), Canalport's north, canal and arrival (mission 3, entrance 0: §8.3), the
   Greenwild's swamp (mission 5), Lantern Reef's fog and broken ends (mission 6), the Bazaar's bow (mission 8, assets
   §1.1's Bazaar hulls). These are clip and tile fixes in the rooms' own files, except the Bazaar.

**Medium, most seen first**

7. **Touch controls** that vanish over bright ground and draw over full-screen menus, and their size on the inner
   screen once you choose (§8.3). Always on screen.
8. **The fonts' l, k and é**, once you choose: every place banner, the words and "Pokémon" (§8.3).
9. **LPC people on the field**, the Adepts and the hero first, then the townsfolk together (assets §2.1, slice 6, art
   3). Then take sheet 07 again for size, shadow and night colour, and fix the LPC faces (Tamsin, Nerissa, the
   Merchant).
10. **Room edges:** Stonehollow's camera, the east-edge columns, the shore corners and the jetty's water block
    in Marrow cove, Bastion's strand and Lantern Reef.
11. **Battle details:** labelled HP and PP bars, the six-enemy line, Pokémon icons in the menus (assets §2.8), LPC
    battle rows for the hero, the rivals and Corvin on your side (assets §2.5, §8.1).
12. **Item icons and the bag's pockets** (assets §2.8, art 14).
13. **The title card and the opening's still** (assets §1.3).
14. **Room details:** the relay stone's sprite, Canalport's under-actor patches and rainbow clump, the Eldergrove's
    shade boxes, the Forge pits, the Wayfarer's gangplank and props, Bastion's strand (once you choose) and jail (assets
    §2.2, Golden Sun's interiors), Brann's cottage (once you choose, assets §2.2), the Bazaar's stalls and its entrance,
    Lantern Reef's east strip, the high town's crates, the Stonehollow memorial stone, the sea colour (once you choose).

**Low**

15. The night tint and lights and the exit marks (both once you choose), the cover screen's exact 3× scale, the world
    map's labels over the ship, the debug map's label, the smaller LPC look fixes in `lpc_recipes.json` and Ilse's hat
    (once you choose), the cliff road's cave mouth and east strips, the Eldergrove heart's shade edges, the drawn red
    Poké Ball, and the foes' names over their partners (§8.1).
