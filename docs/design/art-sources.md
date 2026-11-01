# Art sources: free art and tools for the art pass (1 Nov 2026)

The art pass after the 6 Nov reset fixes what [visual-survey.md](visual-survey.md) found, in its §9 order. This page
lists the free art and tools that could fill those needs. Each one was checked on 1 Nov: its page read, its licence
read word for word, its maker named, and its style judged against Golden Sun's GBA look. Nothing was downloaded or
cloned. Each download waits for your yes on the decision page, under your rule of 31 Oct (research freely; downloads
from trusted sources with your approval each time). What we must make ourselves, because nothing found fits, is in
[art-handoff.md](art-handoff.md), with a brief for each piece.

It follows the decided art rules: Golden Sun's own room tiles at 2× (art 8), LPC people from the generator (art 3-5),
Kenney fonts, frame and prompts (art 6, 14), Pixel-boy's battle backdrops (art 11), generated art only where Golden
Sun has nothing, drawn in code to its palette and 16-pixel grid with light from the top-left (open 91, 102), and an
image generator only for painted pieces. [asset-priorities.md](asset-priorities.md) is the plan of what we make and
what we reuse; the decided answers 169 to 180 are in [open-questions.md](open-questions.md).

## 1. How to read this page

- **Recommendation.** **Download**: worth bringing onto the PC; a question on the decision page asks for your yes.
  **Reference only**: worth looking at on its page, but nothing comes onto the PC. **Skip**: not wanted now.
- **Fit** is judged against Golden Sun's look: 16-pixel tiles, about 15 colours a tile, soft light from the top-left,
  hard pixel edges. **Good** sits beside Golden Sun or the LPC people with little work. **Fair** needs a recolour or a
  redraw. **Poor** is listed only in §6.
- **Licence** is as checked on the page on 1 Nov. Where the first reading was wrong, the entry says so.
- **credits.md** is the row [credits.md](../engine/resources/credits.md) gains, in the same PR that first uses the
  source. No row is added for a source we only looked at.

**Two cautions that apply to many entries.**

1. **LPC's 32-pixel art is twice as fine as Golden Sun's tiles.** A 32-px LPC tile covers one 16-px Golden Sun cell on
   screen, but with four times the pixels, so beside Golden Sun's walls and floors it reads as a finer drawing. LPC
   pieces suit what a person stands with or handles, or serve as a base we redraw at 16 px.
2. **Where the files go.** Art 9 commits only the CC0 picks, and the engine's `tools/import_assets.py` accepts CC0
   only. Committing the CC-BY, OGA-BY, CC-BY-SA and GPL picks ([LPC] Overworld, [LPC] Ship, [LPC] Rain, Sewer, Kyrise,
   Cutting and Healing) needs your yes, a new board question, and the import tool extended to those licences. Until
   then they stay in the gitignored `assets/third_party`. Edits of a share-alike piece keep that licence. Two finds
   have custom licences that forbid passing the files on: pimen's spell packs and OuBa's fog tiles. pimen's would stay
   in `assets/third_party` for good, like the ROM art. No pick is non-commercial only.

## 2. Already on the PC (not searched again)

The LPC generator (the engine's `assets/third_party/lpc` and the Universal LPC generator in the local folder), the
Kenney packs (UI, fonts, Cartography, pirate pack, light masks), the DCSS item icons, the Pokémon expansion's sprites
and item icons, Pixel-boy's battle backdrops, the fan game's parts bin (with Essentials' battle backdrops: three caves,
three indoor scenes, water by day, dusk and night, underwater), the One Piece rips, Golden Sun's ROM art, the CC0 sky
pack `sbs-seamless-sky-backgrounds`, and SpriteLib (reference only, open 183).

The engine's two CC0 libraries in the local folder, `2d-assets-main` (1,101 packs) and
`CC0-Public-Domain-Sprites-main` (76 packs), were searched too (their inventories are in
[asset-inventory](../engine/resources/asset-inventory/)). Of use: **DevWizard's Pixel Art Spells & Projectiles**
(CC0, `packs/devwizard-pixel-art-spells`): 22 hard-edged animated sheets, mostly 16-px bolts, orbs and sparks in
fire, ice, water, wind, rock, plant, light and dark, with a 32×32 splash and a 48×48 shield, for battle projectiles
(§4.11). The same library's Ninja Adventure is the old subset: it has TeaLeaf and 20 small 32×32 effect sheets, but no
Nut and none of the elemental or magic effects (§4.11).

One find in the local generator saves a make: **Commodore Ilse's naval bicorne is already there.** The generator has
`hat_bicorne_athwart_commodore` (and a trim version) under `hat/pirate/bicorne`, by bluecarrot16 with JaidynReiman's
added animations, OGA-BY 3.0, on every row the hats have. Open 179 needs only a recipe change in `lpc_recipes.json`
and a shoulder-length hair from the generator.

## 3. Before any made piece: the tools

These hold every piece we make to Golden Sun's limits. They are needed from item 5 (the world map) on.

#### Tiled Palette Quantization (tiledpalettequant): **download**

- **Link:** https://github.com/rilden/tiledpalettequant (also hosted at https://rilden.github.io/tiledpalettequant/).
- **Author:** rilden.
- **Licence:** MIT ("Copyright (c) 2022 rilden").
- **Gives:** a browser tool that cuts an image's colours to N palettes of M colours, chosen per tile, with a set tile
  size and bits per channel. Colour zero can be unique, shared or transparent, and dithering is optional.
- **Fit: good.** Set 8×8 or 16×16 tiles, 5 bits a channel, 16 palettes of 16 colours and colour zero transparent, and
  the result obeys the GBA's own rule, the limit Golden Sun's tiles live under. Plain JavaScript (index.html,
  script.js, worker.js), so it runs from a local copy with no install.
- **Size:** 210 KB. Last pushed 11 Feb 2024. No README.
- **credits.md row:** a dev tool, never shipped. "Palettes cut with rilden's tiledpalettequant (MIT)".

#### SuperFamiconv: **download**

- **Link:** https://github.com/Optiroc/SuperFamiconv (release v0.12.0-beta4, 17 Sep 2026,
  `superfamiconv_win64_v0.12.0-beta4.zip`, 405,526 bytes).
- **Author:** David Lindecrantz (Optiroc).
- **Licence:** MIT ("Copyright (C) 2005-2026 David Lindecrantz").
- **Gives:** a command-line tile converter. Its `gba` mode (8×8 tiles, 1,024 tiles, 16 subpalettes, 4 bits a pixel)
  reduces colours to native depth, packs subpalettes, removes duplicate tiles and reports counts.
- **Fit: good.** It checks the GBA colour limit (each 8×8 block within one 16-colour palette, at most 16 palettes),
  half of the tile check world-map.md §5.5 asks for. Comparing a made tile's colours and cell edges with its Golden
  Sun neighbour is a short script of our own in `tools/`. Run it as `superfamiconv convert -M gba -T 4096 -i <sheet>
  -v`: gba mode caps a sheet at 1,024 tiles, which a 376×216 still (1,269 tiles) would break on count, not colour. It
  reads only our own art, so it can run in the engine's checks with nothing from a ROM.
- **credits.md row:** a dev tool. "Tiles checked with SuperFamiconv by David Lindecrantz (MIT)".

#### Proper Pixel Art (ppa): **download**

- **Link:** https://github.com/KennethJAllen/proper-pixel-art (PyPI `proper-pixel-art`, installed with pip or uv).
- **Author:** Kenneth Allen.
- **Licence:** MIT ("Copyright (c) 2024 Kenneth Allen").
- **Gives:** a Python command (`ppa`), an API and a local web page that find the true pixel grid in a noisy "pixel
  art" image from an image generator and rebuild it at 1×, with `--color-method dominant|palette`, `-c` colour count,
  `-w` pixel width and saved YAML configs.
- **Fit: good.** It fits the engine's Python tools (like `compose_lpc.py`): one saved command per generated still, its
  config kept beside the recipe, as you prefer saved scripts. Pair it with tiledpalettequant for the per-tile palette.
  It pulls in OpenCV.
- **credits.md row:** a dev tool. "Generated pieces cleaned with Kenneth Allen's Proper Pixel Art (MIT)".

#### unfake.js: **reference only**

- **Link:** https://github.com/jenissimo/unfake.js (about 30 MB with demos).
- **Author:** the unfake.js team (jenissimo). **Licence:** MIT, but its core depends on libimagequant (GPL-3.0 or
  commercial), so a built copy of the tool carries GPL-3 terms. Output images are not affected.
- **Gives:** grid detection (fractional grids too), content-aware downscaling, quantising to a fixed palette, jaggy
  and hole clean-up, with a browser tool, a Python port and a ComfyUI node.
- **Fit: good**, but Proper Pixel Art does the same job inside our Python tools. Keep this one in mind if ppa misreads
  a grid.

#### PixelOE: **skip for now**

- **Link:** https://github.com/KohakuBlueleaf/PixelOE. **Author:** KohakuBlueleaf. **Licence:** Apache-2.0.
- **Gives:** contrast-aware pixelisation of paintings that keeps dark outlines and small highlights.
- **Why skip:** it needs PyTorch (several hundred MB). Only painted sources need it (a parchment Chart, a painted
  backdrop), and those come after the demo. Revisit then.

#### WaveFunctionCollapse: **reference only**

- **Link:** https://github.com/mxgmn/WaveFunctionCollapse. **Author:** Maxim Gumin (mxgmn). **Licence:** MIT (the
  LICENSE file says MIT; GitHub shows NOASSERTION).
- **Gives:** large seamless areas grown from one small sample, from pixel patterns or from tiles with neighbour rules.
- **Fit: fair.** It could fill the fog banks, the Stillwaters or the reef lagoon from a hand-drawn swatch, but our
  compose tool with edge tiles does the same at the Calm's sizes. Some of its bundled samples come from other games
  (Ultima IV, DCSS and others), so never reuse its samples, only our own.

## 4. By need, in the art pass's order

The numbers are visual-survey.md §9's.

### 4.1 Solid menu windows and the Chart (item 1)

Solid windows (open 169) and the Chart's panels are engine fixes: the navy fill made opaque and the windows underneath
hidden. The window frame stays the recoloured RPG-Frames border (art 14).

#### Tiny RPG - Mana Soul GUI: **download**

- **Link:** https://opengameart.org/content/tiny-rpg-mana-soul-gui (`tinyrpg_manasoulgui_v_1_0.zip`, 96.7 KB).
- **Author:** tiopalada. Posted 26 Apr 2025.
- **Licence:** CC0. The author also asks people to "refrain from using any of those resources to either feed LLM/AI
  models or to pull some cryptoshenanigans". That is a request, not a licence term; honour it by never giving these
  files to an image generator as a reference.
- **Gives:** 6 nine-slice frames, 7 animated cursors (3 vertical, 3 horizontal, 1 target), 2 mouse cursors, 10
  buttons, HP, PP and EXP bars, equipment slot frames, 2 headers, a portrait frame, an item frame, a minimap frame.
- **Fit: good.** Solid navy and purple fills with a gold trim and hard pixel corners, close to Golden Sun's solid blue
  windows and recolourable to our navy preset. The bobbing cursors and the target cursor suit Golden Sun's menu pointer
  and battle target. The HP, PP and EXP bars are drawn in code (art-handoff.md §2.23); its bars are the other way. A
  fallback frame if the RPG-Frames border looks thin on the phone.
- **credits.md row:** maker tiopalada; terms CC0; "Tiny RPG Mana Soul GUI by tiopalada (CC0)".

### 4.2 Battle (item 2)

The back sprites' palettes and the command box are engine fixes. Backdrops: Pixel-boy's twelve scenes are in, demo 30
decided Essentials' backdrops for the gaps (caves, jail, forge), and open 103 decided The Lost Age's own ship deck at
sea. Essentials has caves, indoor scenes and water, but no forge, so the forge is on the decision page.

#### Monster RPG 2 combat backgrounds: **reference only**

- **Link:** https://opengameart.org/content/14-battle-backgrounds-from-monster-rpg-2-by-matthew-smith (`bgs.zip`,
  819.5 KB, posted 15 Jul 2026). The older page https://opengameart.org/content/main-art-from-monster-rpg-2 holds the
  same set.
- **Author (corrected):** drawn by Matthew Smith, released by Nooskewl (the studio of the uploader, troutsneeze). The
  first reading credited troutsneeze alone; his 2026 page says Matthew Smith made them.
- **Licence:** CC0 (notice "Nooskewl"). The GitHub mirror LibreGamesArchive/monster-rpg-2 is an archive under zlib,
  not the author's.
- **Gives:** 14 backdrops at 240×110, made for a 240×160 game: fort, grass, jungle, keep, keep_outer, moon, mountains,
  mountains_bridge, rope_bridge, sand, underground, volc_bridge, volcano, water.
- **Fit: fair.** The only free set at the GBA's own width, so at 2× it gives 480×220 with no rescaling. "underground"
  could cover caves, "keep" and "fort" the jail and Bastion. Softer and noisier than Golden Sun, with no clean top-left
  light, and no forge or ship scene. Ask to download it only if Essentials' caves and indoor scenes fail the contact
  sheet.
- **credits.md row (if used):** "Battle backgrounds by Matthew Smith, released by Nooskewl (CC0)".

#### Pixel Ocean and Sky, Sunset Clouds Over The Sea, Moon and Sea: **reference only**

- **Links:** https://opengameart.org/content/pixel-ocean-and-sky-background,
  https://opengameart.org/content/sunset-clouds-over-the-sea-pixel-background,
  https://opengameart.org/content/moon-and-sea-pixel-art-background (zips of 56.9, 445.5 and 434.5 KB).
- **Author:** CraftPix.net 2D Game Assets (posted from the studio's own account, 2023-2024).
- **Licence:** OGA-BY 3.0 on each page. Credit CraftPix.net with a link to each page.
- **Gives:** layered pixel seascapes (sky, cloud bank, sea band, moon) by day, at sunset and by moon: 576×324 layers
  and a full 2304×1296 picture.
- **Fit: fair.** Crisp, a small palette, layers for parallax, a little more modern-indie than Golden Sun. The Lost Age's
  deck backdrop is decided (open 103), and the CC0 skies already on the PC come first. These are the fallback if
  neither reads as open sea.

### 4.3 The hero creator (item 3)

The preview is an engine fix. The kit comes from the generator (art 5): its 137 hair items cover the six styles on
both bodies, so nothing new is needed.

#### [LPC] Grace Hair, [LPC] Female Hair w Ribbon, [LPC] Summer Hair Female: **reference only**

- **Links:** https://opengameart.org/content/lpc-grace-hair, https://opengameart.org/content/lpc-female-hair-w-ribbon,
  https://opengameart.org/content/lpc-summer-hair-female.
- **Author:** thecilekli (18-21 Jul 2020). **Licence:** CC0 on all three.
- **Gives:** three long hair styles for the LPC female sheet, none in the generator.
- **Fit: fair.** Single-colour sheets drawn before LPC's palettes were standardised, so each needs mapping to the
  generator's hair ramp before the creator's shader can recolour it. Only the old sheet's rows exist (no idle, run, sit
  or emote). The Summer hair was drawn with a 4-px brush, and the Ribbon sheet had over 256 colours. Worth a look only
  if the girl hero needs a style the generator lacks.

### 4.4 Fallhaven's high town (item 4)

Nothing external. Open 171 matched it to Fallhaven with Golden Sun's own grass, hanging signs and doors.

### 4.5 The world map, the Kestrel and the Calm's pieces (item 5)

The Lost Age's world map gives the coasts, islands, mountains and the falls' edge ring, and its ship becomes the
Kestrel (open 97). What it lacks: Ketch's skiff and the Wayfarer (ours to draw), the place icons for the new islets,
the Bazaar and Lantern Reef's wrecks, and the Calm's pieces (the storm ring and its eye, the north fog and Westgloam's
fog banks, the Stillwaters, the rim's bite, Marrow Isle's reef lagoon).

#### [LPC] Overworld: **download**

- **Link:** https://opengameart.org/content/lpc-overworld-0 (`LPC Overworld.zip`, 377.4 KB). Posted 16 Aug 2019.
- **Author:** Benjamin K. Smith (BenCreating), commissioned by castelonia; grass and water after Lanea Zimmerman
  (Sharm), sand and snow after Daniel Eddeland, William.ThompsonJ, Nushio and Adrix89.
- **Licence:** CC-BY-SA 3.0 or GPL 3.0. Share-alike: anything we change from it stays CC-BY-SA.
- **Gives:** 16×16 world-map tiles: terrain in three climates, forests, mountains, rivers, rocks including water rocks,
  houses, towers, towns, castles, a ship and a sailboat, a shipwreck, docks, banners, and three animated sea creatures
  (a dolphin, an octopus, a sea serpent).
- **Fit: good** for icons, not terrain. It is the only free set with a shipwreck icon, docks and a sailboat at the
  world map's 16-px scale, and it is LPC-styled. It is simpler and lower in colour than The Lost Age's map, so take the
  wreck (Lantern Reef's icon), the docks (the Bazaar's moorings) and the water rocks (the reef lagoon), recoloured to
  the map's palette. The sea creatures are Act II's route-blocking monsters (§5.3). Its sailboat is one possible base
  for Ketch's skiff, on the decision page.
- **credits.md row:** maker "Benjamin K. Smith (BenCreating), commissioned by castelonia; after Sharm, Daniel Eddeland,
  William.ThompsonJ, Nushio and Adrix89"; terms "CC-BY-SA 3.0 (our edits stay CC-BY-SA)"; credit line, word for word:
  "[LPC] Overworld by Benjamin K. Smith, commissioned by castelonia. Grass/Water based on tiles by Lanea Zimmerman (AKA
  Sharm). Sand/Snow based on tiles by Daniel Eddeland, William.ThompsonJ, Nushio, and Adrix89."

#### Scallywag - Ships: **reference only**

- **Link:** https://foozlecc.itch.io/scallywag-ships (`Foozle_2DT0013_Scallywag_Ships.zip`, 414 KB; name your own
  price, free allowed).
- **Author:** Foozle, commissioned from Pixel Carvel. The page says no generative AI was used.
- **Licence:** "License: (Creative Commons Zero, CC0)"; "free to use and modify for all projects, including commercial
  projects". Attribution not required.
- **Gives:** top-down pirate ships with 6 flag colours, markings, animated cannons, damage states and effects, each as
  an .ase file and a tile sheet.
- **Fit: fair.** The closest free match for a mid-size hull and the only free set with damage states. Its damage
  states are a guide only: Lantern Reef's broken ends (survey §2.6) are drawn in code from the reef ship's own planks
  (art-handoff.md §2.15), since the page states no sprite sizes, facings or number of damage states and its light
  needs reworking to Golden Sun's soft top-left light.

#### [LPC] Ship: **download**

- **Link:** https://opengameart.org/content/lpc-ship (`lpc-ship.zip`, 954.5 KB). Posted 13 Feb 2022.
- **Author:** bluecarrot16, commissioned by Sander Frenken (for Herodom).
- **Licence:** CC-BY 4.0, GPL 3.0, GPL 2.0 or OGA-BY 3.0; the notice reads "License: OGA-BY 3.0+ or CC-BY 3.0+ or GPL
  2.0+". Pick OGA-BY or CC-BY, so our edits carry no share-alike. The preview's water (LPC base) and crates ([LPC]
  Containers, CC-BY-SA 4.0+) are not part of it.
- **Gives:** a modular top-down square-rigger: hull, deck, masts, sails set and furled, rigging, crow's nests, the
  captain's wheel, anchor, hatches, animated cannons, separate railings and quarterdecks for layering, a Tiled map.
- **Fit: good** for the rooms. Its separate rails and furled sails answer the Bazaar's merchant hull exactly (item 6,
  survey §2.8), and the wheel and hatches can fill the Wayfarer's deck props (item 14). At 32 px it has the people's
  density, finer than Golden Sun's ship decks, so use it as a base and redraw at 16 px where it meets Golden Sun's
  planks.
- **credits.md row:** maker "bluecarrot16, commissioned by Sander Frenken"; terms "OGA-BY 3.0"; credit line: "[LPC]
  Ship" by bluecarrot16, commissioned by Sander Frenken. https://opengameart.org/content/lpc-ship.

#### Tiny Islands - 16x16 Tilemap: **reference only**

- **Link:** https://opengameart.org/content/tiny-islands-16x16-tilemap (56.9 KB). **Author:** Majadroid (28 Mar 2021).
- **Licence:** CC0 ("Attribution is not required but appreciated").
- **Gives:** an Anno-style island set with a three-masted ship in 8 directions, a harbour, a castle and resource icons.
- **Fit: fair.** Small and plain beside Golden Sun's map. Its 8-direction ship is a useful guide to how a small hull
  reads at each facing. The Tidewarden cutters can wear The Lost Age's ship in their own colours, so it adds nothing
  the map needs.

#### Ship tileset (Sevarihk) and [LPC] Wooden ship tiles (Tuomo Untinen): **reference only**

- **Links:** https://opengameart.org/content/ship-tileset (CC-BY 4.0, 32×32, "credit me and provide a link");
  https://opengameart.org/content/lpc-wooden-ship-tiles (CC-BY 3.0, CC-BY-SA 3.0, GPL 3.0, GPL 2.0; `ship.png`, 21.7
  KB; "Wooden ship tiles by Tuomo Untinen").
- **Fit:** second build-your-own-boat kits if [LPC] Ship lacks a hull shape. On the wooden tiles' page, an edited
  preview in the comments uses RPG Maker sails, which its poster says "are not okay to use"; take only the original.

#### Pixelated animated water/clouds shader: **download**

- **Link:** https://godotshaders.com/shader/pixelated-animated-water/ (shader text, about 2 KB).
- **Author:** maGGam, combining auntygames' "Pixel Animated Water" and a 2D noise snippet.
- **Licence (corrected):** maGGam's post says CC0, but the author says it combines
  https://godotshaders.com/shader/pixel-ghibli-water/ by auntygames, which is MIT, and a noise snippet whose licence the
  page does not show. Treat it as MIT plus CC0, and keep auntygames' MIT notice with it.
- **Gives:** a Godot 4 canvas_item shader that pixelates and maps fBm noise to exactly four colours by thresholds,
  with direction, speed, octaves and pixel size.
- **Fit: fair.** Hard-edged bands from a fixed four-colour palette match open 102's "drawn in code to its palette",
  but it has no mask uniform, and its last line, `COLOR = smoothed_color * transparency`, also scales the colour,
  which moves the four greys off their 15-bit values. With a mask uniform added and that line written as
  `COLOR = vec4(c.rgb, c.a * mask_step)`, `mask_step` being 0, 0.25, 0.5 or 0.75, it keeps the three fixed alpha
  steps of art-handoff.md §1.1. Fed four greys from a Golden Sun tile and set to whole world pixels, it then draws
  moving fog banks, the storm's cloud band and the fog version of the sea backdrop (open 103).
- **credits.md row:** maker "maGGam; auntygames"; terms "CC0 and MIT"; "Pixel cloud shader by maGGam, after auntygames'
  Pixel Animated Water (MIT)".

#### Animated 2D Fog (Optional Pixelation) shader: **download**

- **Link:** https://godotshaders.com/shader/procedural-2d-fog-with-pixelation/ (shader text, about 3 KB).
- **Author:** Tennisson, after Gonkee's Godot 3 fog shader.
- **Licence:** "The shader code and all code snippets in this post are under MIT license and can be used freely."
  Gonkee's original states no licence; a small risk for personal use.
- **Gives:** a Godot 4 fBm fog with a colour, octaves, a pixelation switch and amount, a greyscale `fog_mask` that sets
  density, and direction and scroll settings.
- **Fit: fair.** The `fog_mask` is what open 176 needs at Lantern Reef: white over open water and the gaps, black over
  the decks, so the fog drifts only between the wrecks and the decks stay at full colour. But its alpha is smooth
  noise times a smooth mask (`COLOR = vec4(color.rgb, final * color.a * 0.5)`), so we snap it to 0, 25, 50 or 75 per
  cent. It also samples `fog_mask` at the unsnapped UV and pixelates by divisions of the UV (`pixelation_amount`), not
  by world pixels, so both are set per room (art-handoff.md §2.14). A known fault: it breaks at large TIME values
  with scroll noise on. Apply AlPS_208's fix from the comments (offset the two fBm calls by different constants and
  add a `fog_speed` factor). blinks' CC0 "2D Fog Overlay" (https://godotshaders.com/shader/2d-fog-overlay/) is a
  simpler fallback; it needs `repeat_enable` on its noise in Godot 4.
- **credits.md row:** maker Tennisson; terms MIT; "Fog shader by Tennisson (MIT), after Gonkee".

#### 2D Swirling Vortex Portal shader: **on the decision page, as a make-or-reuse choice**

- **Link:** https://godotshaders.com/shader/2d-swirling-vortex-portal/. **Author:** Stinkysunstep.
- **Licence:** "The shader code and all code snippets in this post are under MIT license and can be used freely."
- **Gives:** a shader that twists and scrolls a texture inside a radius, with twist, pulse, rotation and edge softness;
  tested in Godot 4.1.1 and 4.4.1.
- **Fit: fair.** No pixel-art whirlpool exists free. Twisting Golden Sun's own cyan water with it keeps the palette,
  but it resamples pixels, so it needs a pixel snap and a palette step of our own, and `edge_softness` cannot go below
  0.01. The other way is a whirlpool drawn in code as animated tiles. The decision page asks which.
- **credits.md row (if used):** "Vortex shader by Stinkysunstep (MIT)".

#### [LPC] Rain animation: **download**

- **Link:** https://opengameart.org/content/lpc-rain-animation (`rain.png`, 880 bytes). Posted 21 Dec 2020.
- **Author:** Evert. **Licence:** CC-BY 3.0, GPL 3.0 or OGA-BY 3.0. Notice: "Credit me and link back to this OGA
  entry."
- **Gives:** a tileable 10-frame rain overlay, 64×64 tiles, in LPC's palette. No background drops or splashes.
- **Fit: fair.** It tiles over the storm ring without a seam, at 64 px (four Golden Sun cells), and with the cloud band
  from the shader above it answers the survey's "the storm has no clouds or rain" (§2.10). Recolour the streaks to the
  storm's greys.
- **credits.md row:** maker Evert; terms "OGA-BY 3.0"; "Rain by Evert,
  https://opengameart.org/content/lpc-rain-animation".

#### Lightning Cloud: **reference only**

- **Link:** https://opengameart.org/content/lightning-cloud. **Author:** dorkster. **Licence:** CC-BY 3.0
  (`lightning.png`, 3 KB, made for Polymorphable).
- **Fit:** a flashing storm cloud in LPC style. The storm ring's lightning is simpler as a palette flash in code.

### 4.6 The placeholder rooms and the interiors job (item 6)

The Vault's halls, the sea caves and the Greenwild's swamp are clips from Golden Sun again. Canalport needs a foam edge,
Lantern Reef its fog (the fog shader above) and broken ends (drawn in code), the Bazaar its merchant hull ([LPC]
Ship above). The interiors job adds the sluice house and the hatchery, which no Golden Sun room gives us (open 100).

#### Zelda-like tilesets and sprites: **download**

- **Link:** https://opengameart.org/content/zelda-like-tilesets-and-sprites (`gfx.zip`, 174.8 KB). Posted 16 Feb 2017.
- **Author:** ArMM1998. **Licence:** CC0 (commenters ask for a courtesy credit).
- **Gives:** 16×16 overworld, cave and indoor sets, a character template, effects, objects and UI.
- **Fit: good.** Minish-Cap-like 16-px art with soft shading, the nearest free style to Golden Sun's rooms. A parts bin
  for cave arches and rock rims (the sea caves' mouth, the cliff road's cave mouth), indoor furniture for the made
  interiors, and crates. Golden Sun's own clips stay first (art 8, open 100). One commenter thought its trees close to
  Minish Cap's; the author disagreed and the claim was withdrawn. Leave the trees out anyway.
- **credits.md row:** maker ArMM1998; terms CC0; "Zelda-like tilesets by ArMM1998 (CC0)".

#### 16x16 Shoreline Wave Animation Tiles: **download**

- **Link:** https://opengameart.org/content/16x16-shoreline-wave-animation-tiles (`cc0waveanimtiles16x16.png`, 1.1 KB).
- **Author:** Eldiran (the Horizon's Gate developer). Posted 26 Nov 2022. **Licence:** CC0.
- **Gives:** an animated 16×16 shoreline template: brown is replaced with the land and magenta with the water, and the
  animation steps a frame every two tiles.
- **Fit: good.** Filled with Golden Sun's own sand and the decided cyan sea (open 172), it becomes a foam edge with no
  style jump: Canalport's "meet the sand with foam" (survey §2.3) and the shore corners of item 10. madmedicsoft's
  bordered CC0 variant is in the comments.
- **credits.md row:** maker Eldiran; terms CC0; "Shoreline wave template by Eldiran (CC0)".

#### Sewer tileset: **download**

- **Link:** https://opengameart.org/content/sewer-tileset (`sewer_1.png`, 35.5 KB). Posted 6 Jul 2011.
- **Author:** MrBeast (Beast), commissioned by OpenGameArt.org.
- **Licence:** CC-BY 3.0 or GPL 2.0. Notice: "Art by MrBeast. Commissioned by OpenGameArt.org
  (http://opengameart.org)".
- **Gives:** a 16×16 sewer and dungeon set: stone walls and floors, water channels with edges, grates and walkways.
- **Fit: good.** 16-px, a small palette, SNES-RPG style: the closest free match to Golden Sun's indoor stone, and
  channelled water in stone is the sluice house's core. A parts bin, redrawn to Golden Sun's palette in code.
- **credits.md row:** maker "MrBeast, commissioned by OpenGameArt.org"; terms "CC-BY 3.0"; the notice word for word.

#### [LPC] Sawmill: **reference only**

- **Link:** https://opengameart.org/content/lpc-sawmill (100.1 KB). **Author:** bluecarrot16, Lanea Zimmerman (Sharm),
  Ivan Voirol and Sander Franken. **Licence:** CC-BY 4.0.
- **Gives:** an animated water-powered mill with its wheel and flume, a README on animating it and a Tiled example.
- **Fit: fair.** The only free animated water wheel in a top-down RPG style, but at LPC's finer density, and the
  sluice house's script needs sluice gates, not a wheel. A guide to how a turning wheel reads, if one is wanted.

#### [LPC] Farm: **reference only**

- **Link:** https://opengameart.org/content/lpc-farm (149.8 KB). **Author:** bluecarrot16, Wolthera van Hövell tot
  Westerflier (TheraHedwig) and Ivan Voirol, commissioned by Rupil.
- **Licence:** CC-BY 4.0. The author offers the parts not from Ivan Voirol's Slates (for example `barn.png`) under
  OGA-BY 3.0 or GPL 3.0 too. A correction: the windmill and water wheels were "adapted from Ivan Voirol's excellent
  Slates set", so they are CC-BY 4.0 only and need Ivan Voirol's credit.
- **Gives:** a modular barn, silos, a granary, a chicken coop with nesting boxes, beehives, sheds, fences, and animated
  windmill blades and water wheels.
- **Fit: fair.** No free hatchery exists. The coop's nesting boxes and straw are the nearest pieces to egg racks, but at
  LPC's density. The hatchery stays a Golden Sun interior with our own drawn incubators (art-handoff.md); look at the
  coop for ideas.

### 4.7 The touch controls (item 7)

Nothing external. Kenney's touch faces are in; the dark backing (open 180) is drawn in code.

### 4.8 The fonts (item 8)

Open 170 decided to redraw l, k and é in our copies of Kenney Mini 8 and Kenney Pixel 16. These are fallbacks only,
if the redraw fails on the phone.

#### Pixel Operator: **reference only**

- **Link:** https://www.dafont.com/pixel-operator.font (104 KB, version 2018.10.04-1, 241 glyphs, 15 TTFs).
- **Author:** Jayvee Enaguas (HarvettFox96). **Licence:** CC0 1.0, in the author's words: "licensed under a Creative
  Commons Zero (CC0) 1.0". DaFont's category line also says public domain, GPL or OFL; the author's statement governs.
- **Fit: good.** Proportional, with real l and k ascenders and é. The 8-px cut is close to Golden Sun's dialogue line.

#### m5x7 and m6x11: **reference only**

- **Links:** https://managore.itch.io/m5x7 (`m5x7.ttf`, 33 kB), https://managore.itch.io/m6x11 (`m6x11.ttf`, 12 kB).
- **Author:** Daniel Linssen (managore).
- **Licence:** m5x7 "Creative Commons Zero v1.0 Universal", attribution appreciated. m6x11 has no licence field, only
  "free to use with attribution", so it needs a credit line if used.
- **Fit: good.** m5x7 has Kenney Mini's small footprint with real l, k and é, so menus would keep their row heights.
  m6x11's accents are not stated.

#### Ark Pixel Font (10 px proportional, latin): **reference only**

- **Link:** https://github.com/TakWolf/ark-pixel-font (release 2026.10.25,
  `ark-pixel-font-10px-proportional-ttf-v2026.10.25.zip`, 3,952,810 bytes).
- **Author:** TakWolf. **Licence:** the fonts SIL Open Font License 1.1, the build code MIT.
- **Fit: fair.** Full pan-Latin accents and real lower case, a little taller and more modern than Golden Sun. The OFL
  file names no Reserved Font Name, so a cut-down copy may keep its name. It must stay under the OFL with TakWolf's
  copyright notice, and may not be sold on its own. The 16-px size was dropped in September 2026.

### 4.9 LPC people on the field (item 9)

The cast, the townsfolk and the hero come from the generator; Ilse's bicorne is there too (§2). Golden Sun's emote
sprite is decided for emotes (art 14).

#### LPC Character animations: push and carry: **reference only**

- **Link:** https://opengameart.org/content/lpc-character-animations-push-and-carry (185.4 KB). Posted 13 Apr 2022.
- **Author:** Evert, building on Redshrike, wulax, MrBeast, Joe White, bigbeargames, makrohn, Daneeklu, bluecarrot16
  and JaidynReiman. **Licence:** CC-BY-SA 3.0 or GPL 3.0 (Evert could not offer OGA-BY because the originals lack it).
- **Gives:** for the LPC male body only: an 8-frame push walk and a carry-overhead walk, an armless walk with the arms
  on their own sheet, and a few clothes redrawn for them.
- **Fit: fair.** Real LPC art on the same body, but the male body and a few clothes only, so each Adept's outfit would
  need its arms re-cut, and the female body the same edit. Art approval 2 found today's push reads well. Look again
  only if the sheet 07 retake shows the push or a crate carry looking wrong.

#### 16x16 Emotes for RPGs and Digital Pets, and Animated emote bubbles: **skip**

- **Links:** https://opengameart.org/content/16x16-emotes-for-rpgs-and-digital-pets (Tomcat94, CC0, "Reminescent of
  the emotes in Camelot games such as Golden Sun") and https://opengameart.org/content/animated-emote-bubbles (Romain
  Oltra, posted by Game Dev Alliance, CC0).
- **Why skip:** Golden Sun's own emote sprite is decided (art 14), and Ninja Adventure's 30 emote balloons come with
  that pack (§4.11) if a CC0 set is ever needed.

### 4.10 Room edges (item 10)

The shoreline template (§4.6) covers the straight grass-to-sea corners. The east columns and the camera are engine and
room fixes.

### 4.11 Battle details and effects (item 11)

Labelled HP and PP bars are drawn in code (art-handoff.md §2.23), with Mana Soul's (§4.1) the other way. Move
effects: hard-edged CC0 sheets now, Golden Sun's own later (art 12). DevWizard's CC0 projectiles are already on the PC
(§2).

#### Ninja Adventure Asset Pack (full itch edition): **download**

- **Link:** https://pixel-boy.itch.io/ninja-adventure-asset-pack (`Ninja Adventure - Asset Pack.zip`, 89 MB; name your
  own price). The page says no generative AI was used.
- **Author:** Pixel-Boy and AAA, the makers of the battle backdrops already in the game.
- **Licence:** "Creative Commons Zero v1.0 Universal"; the bundled README says "released under the Creative Commons
  Zero (CC0) license... Attribution is not required but appreciated."
- **Gives:** the full pack. The local copy is an old subset: it has TeaLeaf and 20 small 32×32 effect sheets, but no Nut
  and none of these. FX/Elemental: Flam, Ice, Plant, Rock, RockSpike, Thunder and Explosion, and (per a vendored copy on
  GitHub) Water and WaterPillar. FX/Magic: Aura, Boost, Circle, Shield, Spark, Spirit. Particles (rain, snow, leaf,
  rock, spark), projectiles, slashes, smoke. About 30 emote balloons. Items: Nut, Nut2, Seed1-3, TeaLeaf, potions, keys,
  coins, chests, scrolls, weapons. A palette file.
- **Fit: good.** One hand with the backdrops, 16-px, hard-edged, a small palette, close to Golden Sun's grid. Rock,
  Plant and Ice suit field casts (Move, Growth, Frost) better than battle-scale sheets. Nut and TeaLeaf are references
  for the Herb and Nut icons. CC0, so it can be committed. Only a few hundred kB of it is needed.
- **credits.md row:** the existing "RPG Battle System, Ninja Adventure" row (Pixel-boy and AAA, CC0) gains the effects
  and items under "What we use".

#### Pixel Magic Effects (Foozle 2DE0001): **download**

- **Link:** https://foozlecc.itch.io/pixel-magic-sprite-effects (`Foozle_2DE0001_Pixel_Magic_Effects.zip`, 101 kB).
- **Author:** Foozle, commissioned from lordfitoi. No generative AI.
- **Licence:** "License: (Creative Commons Zero, CC0)"; "Attribution not required."
- **Gives:** 10 spell animations on a 32×32 grid (Fire Ball, Molten Spear, Water, Geyser, Rocks, Earth Spikes, Wind,
  Tornado, Portal, Explosion), each with a 32×32 spell icon.
- **Fit: good.** Hard-edged, a small palette. It fills Ninja Adventure's wind gap under CC0. Tornado and Geyser read as
  Whirlwind and Douse at 2×. The icons can stand in for Psynergy icons until the ROM's are exported.
- **credits.md row:** maker "Foozle, commissioned from lordfitoi"; terms CC0; "Pixel Magic Effects by Foozle (CC0)".

#### pimen's elemental spell effects: **download, kept in third_party**

- **Links:** Fire https://pimen.itch.io/fire-spell, Ice https://pimen.itch.io/ice-spell-effect-01, Thunder
  https://pimen.itch.io/thunder-spell-effect-01, Wind https://pimen.itch.io/wind, Earth
  https://pimen.itch.io/earth-spell-effect-01, Water https://pimen.itch.io/magical-water-effect, Holy
  https://pimen.itch.io/holy-spell-effect (only "Holy VFX 01-02.rar", 14 kB, is free), Cutting and Healing
  https://pimen.itch.io/cutting-and-healing.
- **Author:** pimen (Gabriel, @PimenArt). Each page says no generative AI was used.
- **Licence:** the seven element packs, word for word: "You can use and modify this asset for personal and commercial
  purpose. Credit is not required but would be appreciated" and "You cannot resell or redistribute those sprites." A
  custom licence, not CC: these stay in the gitignored `assets/third_party/pimen`, never committed. Cutting and Healing
  is CC BY 4.0, with no such ban.
- **Gives:** one artist's hard-edged effects for every element the battle needs: a firebolt and fire breath, two ice
  effects, two thunder projectiles and a hit (with blurless versions), wind breath, projectile and hit, three earth
  effects, a water splash and spike, two holy effects, and slash and heal sheets. Canvases of 16 to 80 px.
- **Fit: good.** Crisp, unblurred pixels and a few flat colours (seen on the Holy preview), close to Golden Sun's
  Psynergy sparks and inside art 12's no-soft-render rule. Use the blurless thunder. Rar files, about 230 kB in all.
  DevWizard's CC0 projectiles, already on the PC (§2), are the way without this download.
- **credits.md row:** maker pimen; terms "pimen's licence: use and modify, no redistribution (Cutting and Healing CC BY
  4.0)"; "Spell effects by pimen"; "Cutting and Healing by pimen, CC BY 4.0".

#### RPG UI Icons: **on the decision page, as a make-or-reuse choice**

- **Link:** https://opengameart.org/content/rpg-ui-icons (`RPG_Icons_Pack_OwlishMedia.zip`, 46.3 KB). Posted 30 Jun
  2018.
- **Author:** OwlishMedia. **Licence:** CC0.
- **Gives:** 16×16 and 32×32 icons for status conditions, elements, items, medicine, weapons and armour, and pointers.
- **Fit: fair.** Small CC0 status marks at 16 px, where Golden Sun shows status marks in battle. Its preview could not
  be opened, so its style is unjudged. Golden Sun's own status marks are in the ROM, and open 91 takes Golden Sun's
  own art first, so the decision page recommends those, exported and kept local, with this download the other way.
  Its element icons are generic; Golden Sun's four come from the ROM, and Forest's and Shadow's are ours to draw
  (art-handoff.md).
- **credits.md row:** maker OwlishMedia; terms CC0; "RPG UI Icons by OwlishMedia (CC0)".

#### Spell Effects by StarsteelGaming: **skip**

- **Link:** https://opengameart.org/content/spell-effects-by-starsteelgaming (CC0, 45.3 KB). Three 64×32 projectiles on
  DB32 (Fireball, Icespear, Thundersphere), with no impacts. Ninja Adventure and pimen cover them.

### 4.12 Item icons and the bag's pockets (item 12)

Art 14 decided DCSS's 32-px icons, shown at full size in the detail box, with Herb, Nut, Mint and the balls drawn by
us. The rows today squeeze 32-px icons to about 19 px (survey §4.1). Herb, Nut and Mint (items 180, 181 and 195) are
Golden Sun's own items, and its item data gives each its own icon in the ROM (icons 117, 132 and 144), while open 91
(24 Oct, after art 14) generates art only where Golden Sun has nothing. The decision page asks which way.

#### Kyrise's Free 16x16 RPG Icon Pack v1.3: **download**

- **Link:** https://kyrise.itch.io/kyrises-free-16x16-rpg-icon-pack (`Kyrises_16x16_RPG_Icon_Pack_V1.3.zip`, 879 kB;
  v1.2 is on https://opengameart.org/content/kyrises-free-16x16-rpg-icon-pack). No generative AI.
- **Author:** Kyrise. **Licence:** CC BY 4.0 ("© 2018 by Kyrise is licensed under CC BY 4.0").
- **Gives:** 350+ sprites (70+ designs), each as 16, 32 and 48 px PNGs: swords, staves, bows, shields, books, helmets,
  hats, armour, gloves, boots, potions, fruit, fish, keys, rings, amulets, gems, scrolls, coins, flowers, leaves.
- **Fit: good.** Saturated 16-bit colour, a black outline on each icon and simple top-lit shading, close to Golden Sun's
  own black-outlined 16-px item icons. Its 16-px base lets the rows show one size at a whole-number scale, with its
  32-px copy in the detail box. On OGA commenters asked whether 7Soul1's icons were reused; Kyrise answered "My icon
  pack has only icons made by me". Whether it replaces DCSS where both have an icon is on the decision page.
- **credits.md row:** maker Kyrise; terms "CC BY 4.0"; credit line, word for word: "Kyrise's Free 16x16 RPG Icon Pack |
  Graphics made by Kyrise: https://kyrise.itch.io/".

#### Shikashi's Fantasy Icons Pack v2: **reference only**

- **Link:** https://shikashipx.itch.io/shikashis-fantasy-icons-pack (1.9 MB). **Author:** Matt Firth (shikashipx), many
  shapes based on game-icons.net. **Licence:** "Creative Commons Attribution v4.0 International"; credit both "Matt
  Firth (shikashipx)" and "game-icons.net" (the page calls game-icons CC BY 4.0; game-icons.net is CC BY 3.0).
- **Gives:** 284 icons at 32×32, among them herb, herb1 and herb2, a potion ladder, foods and keys.
- **Fit: fair.** Cleaner and flatter than Golden Sun. The only free set with named herb icons: a reference for drawing
  Herb and Mint.

#### 496 pixel art icons for medieval/fantasy RPG: **skip**

- **Link:** https://opengameart.org/content/496-pixel-art-icons-for-medievalfantasy-rpg (CC0, 1.5 MB, Henrique
  Lazarini (7Soul1), compiled by gnola14). At about 34×34 they sit off our grid, and DCSS already fills the Gear
  pocket.

### 4.13 The title and the opening's stills (item 13)

The title is the logo over a live Stonehollow at dusk (decision 25's alternative), so it needs a drawn logo, not a
painting. The opening's six stills are painted with an image tool (decision 23), then cleaned with the tools in §3.

#### The Cannon Shot: **reference only**

- **Link:** https://www.rijksmuseum.nl/en/collection/SK-C-244. **Author:** Willem van de Velde II, about 1680,
  Rijksmuseum SK-C-244. **Licence:** public domain (Public Domain Mark 1.0).
- **Fit: fair.** A calm sea, soft high light and a big sky: a prompt anchor ("calm sea, Dutch marine light") for
  stills 3 to 5, or a reference image for an image tool. Not GBA art: whatever comes from it still goes through the
  clean-up and the palette step. Its download size was not checked (the page offers a download; a login may be
  needed).

### 4.14 Room details (item 14)

#### LPC castle: **reference only**

- **Link:** https://opengameart.org/content/lpc-castle (`lpc_castle.png`, 24.5 KB). **Author:** Evert, with Lanea
  Zimmerman (Sharm)'s wood and Xenodora's rounded towers. **Licence:** CC-BY 3.0.
- **Gives:** 32×32 castle walls, towers, arched doorways, a portcullis and a drawbridge.
- **Fit: fair.** Bastion's fort wall stays Golden Sun's grey stone (open 175). Its portcullis and gateway show how a
  sea-gate reads from above, if Golden Sun's clips lack one; we would redraw it at 16 px from Golden Sun's stone.

The Wayfarer's helm, hatches and rails can come from [LPC] Ship (§4.5), and the high town's crates from Zelda-like
(§4.6).

### 4.15 The low items (item 15)

#### LPC Lamp Posts Rework: **reference only**

- **Link:** https://opengameart.org/content/lpc-lamp-posts-rework (133.9 KB). **Author:** AntumDeluge and mold, from
  originals by Curt, Lanea Zimmerman (Sharm) and William.Thompsonj. **Licence:** CC-BY 3.0, GPL 3.0, GPL 2.0 (the body
  adds OGA-BY 3.0); the reworker's own changes CC0. Notice: "Created by Curt, Lanea Zimmerman (Sharm),
  William.Thompsonj, & mold".
- **Fit: fair.** Street lamps at LPC's density. Open 177 decided lamps and lit windows drawn in code; these show shapes
  that read at that size. Kenney's light masks (already on the PC) give the glow's shape.

## 5. After the demo

### 5.1 Portraits and the wanted posters

Decision 24: a 64×64 portrait with three expressions for the 8 Adepts and Ilse, Brann, Sael and Hask, and the hero's
per body and hair style, colour-keyed for the creator's shader. Decision 23 makes them with an image generator; the
kits below are another way, on the decision page.

#### 64x64 Portrait (LPC portrait builder): **on the decision page, as a make-or-reuse choice**

- **Link:** https://opengameart.org/content/64x64-portrait (`Portrait.zip`, 2.8 MB). Posted 10 Jul 2016.
- **Author:** Nila122. **Licence:** CC-BY-SA 3.0 or OGA-BY 3.0 (OGA-BY added with the author's permission on 25 Sep
  2022, per a moderator). Pick OGA-BY 3.0, so our edits carry no share-alike. No notice: credit Nila122 with a link.
- **Gives:** a layered 64×64 head-and-shoulders kit made for LPC: 7 skins (each with noses, mouths, eyes, ears, brows
  and wrinkles), 31 hairs with 31 recolours, facial hair, headwear, eye colours and backgrounds.
- **Fit: good** in size and build. Decision 24's size exactly, and layered, so the hero's portrait can follow the
  creator's hair with colour keys. Its black outlines and flat cel shading are harder than Golden Sun's soft faces, so
  the light needs repainting from the top-left and the second and third expressions drawing by hand. Also the quickest
  way to make the wanted posters' "terrible portraits" (demo 11).
- **credits.md row (if used):** maker Nila122; terms "OGA-BY 3.0"; "Portrait parts by Nila122,
  https://opengameart.org/content/64x64-portrait".

#### [LPC] Portraits Remix: **reference only**

- **Link:** https://opengameart.org/content/lpc-portraits-remix (251.1 KB). **Author:** Sebastian "Basxto" Riedel and
  Diana "diana23570" Paymurzina. **Licence:** CC-BY 4.0.
- **Fit: fair.** Its emotion set on LPC's own colour ramps is the part decision 24 needs, but it has one hair style per
  body and a 96-px frame. Caution: it says it was "Originally based on"
  https://opengameart.org/content/portraits-and-emotions, which is now unpublished, so its base's licence could not be
  read. A guide for expressions, not a source to commit.

#### Character portrait kit: **reference only**

- **Link:** https://opengameart.org/content/character-portrait-kit (58 KB). **Author:** Dezra's Dragons. **Licence:**
  CC-BY 4.0, CC-BY 3.0 or OGA-BY 3.0; credit "Dezra's Dragons" with a link to
  https://opengameart.org/users/dezrasdragons.
- **Fit: fair.** Soft shading with 2 to 4 colours a part, nearer Golden Sun's depth than outlined kits, at 32, 48 and
  64 px (a 32-px face would suit the battle pane). A base kit, not finished faces, and no naval hats.

#### Anime Portrait for LPC characters (sets 1 and 2): **reference only**

- **Links:** https://opengameart.org/content/anime-portrait-for-lpc-characters (CC-BY-SA 3.0, 17 PNGs),
  https://opengameart.org/content/lpc-anime-portrait-2 (CC-BY 3.0, 4 PNGs). **Author:** ZeNeRIA29, commissioned by
  ZaPaper for PlayCraft. Credit "Portrait graphics created by PlayCraft".
- **Fit: fair.** The only CC busts painted from LPC sprites, near Golden Sun's character art in style, but
  high-resolution paintings of other people's characters: style and pose references for the image-generator route.

### 5.2 The painted Chart

Demo 27 and open 178: the terrain grid with Kenney Cartography icons now, a parchment Chart painted once later.

#### Old Parchment Paper: **reference only for now**

- **Link:** https://opengameart.org/content/old-parchment-paper (`parchment.png`, 388 KB; `parchment_alpha.png`, 397.3
  KB). **Author:** cron. **Licence:** CC0.
- **Fit: fair.** A clean base for the painted Chart, but photo-like, so its noise must be flattened and its colours cut
  to the palette, or it clashes with the Cartography icons and the navy panels. Ask to download it when the Chart is
  painted.

#### Carta Marina (1539): **reference only**

- **Link:** https://commons.wikimedia.org/wiki/File:Carta_Marina.jpeg (5,016×3,715, 5.22 MB). **Author:** Olaus
  Magnus; the page asks for a credit to the James Ford Bell Library, University of Minnesota. **Licence:** public
  domain (Public Domain Mark 1.0; Wikimedia warns reuse may be restricted outside the US).
- **Fit: good** as a reference: sea monsters, ships, compass roses, rhumb lines, a framed title. Hand-copied ornaments
  (a rose, a sea serpent at the Galeway, a cartouche) carry no licence risk.

### 5.3 Act II's monsters

Act II's strong monsters block routes in the broken Galeway (world-map.md §1.4), and its sea battles need creatures
Golden Sun's enemy list lacks. All of these wait for Act II; none is needed for the demo.

- **[LPC] Overworld's sea creatures** (§4.5, CC-BY-SA 3.0): a dolphin, an octopus and a sea serpent on the 16-px map
  grid, for a monster coiled in a storm lane. They come with that download.
- **64x64 Creature Sprites** (https://opengameart.org/content/64x64-creature-sprites, Kiovenn, CC-BY 4.0, 54.8 KB):
  10 front-facing battlers, among them a mermaid, a spiked squid, a fish skeleton, a mimic and a ghost. More saturated
  and outlined than Golden Sun's enemies. **Reference only.**
- **[LPC] Monsters** (https://opengameart.org/content/lpc-monsters, Charles Sanchez, bagzie and bluecarrot16, CC-BY-SA
  3.0 or GPL 3.0, 78.1 KB) with **[LPC] Monster Death Animations**
  (https://opengameart.org/content/lpc-monster-death-animations, CC-BY-SA 3.0 or GPL 3.0, 76.2 KB): slimes, bats,
  worms, eyeballs and flowers with attacks, more Act I wildlife than Act II threats. **Reference only.**
- **[LPC] Golem** (https://opengameart.org/content/lpc-golem, Stephen "Redshrike" Challener with William.Thompsonj,
  CC-BY 4.0 among others, three sheets of 12 to 28 KB): by LPC's first artist, big and slow, a route-blocking strong
  monster. **Reference only.**
- **[LPC] bears, deer, lions and more** (https://opengameart.org/content/lpc-bears-deer-lions-and-more, tapatilorenzo
  with Sevarihk's shark, CC-BY 4.0, work not from Sevarihk also CC0, 421.3 KB): a 160×160 shark that swims and
  submerges, a giant rat, bears. Sevarihk's fin-only shark:
  https://opengameart.org/content/shark-sprites-animated-4-directional (CC-BY 4.0). **Reference only.**
- **LPC Frogman** (https://opengameart.org/content/lpc-frogman, Redshrike and Evert, CC-BY 3.0 or OGA-BY 3.0): a
  trident frogman with a crowned variant, a reef or swamp brute. Its greens are off LPC's palette. **Reference only.**

## 6. Dropped

- **Nidhoggn's Backgrounds** (https://opengameart.org/content/backgrounds-3, CC0): soft 1104×621 paintings far above
  our resolution, a poor fit. Commenters warn that recoloured copies are resold on itch.io.
- **OuBa's 16x16-Cartoon Fog Tileset** (https://ouba.itch.io/cartoon-fog-tileset): labelled CC0, but its own page adds
  "You can't: Resell, repackage, or redistribute the asset, even if modified" and bans use in game-making tools or code
  templates. The fog shaders in §4.5 do the job in code, as open 102 asks.
- **Pipoya's Vehicle & Ship Sprites:** the best-looking small ships (32×32, 4 and 8 directions), but paid ($14.80) and
  "Not redistribute or resell".
- **CaptainSkolot's 4 Tempestuous Sea Backgrounds** and its Sea & Ocean Pack (at least $4.99 each), and **ansimuz's
  Forest Ruins Battle Background LITE** (https://ansimuz.itch.io/forest-ruins, $2.79, no licence stated): paid.
- **JoesAlotofthings' RPG Maker whirlpool** (CC-BY 4.0): a soft particle glow, not pixel art.
- **Chasersgaming's RPG Pirate Ship Tile Set** (CC0): 8×8 NES style, a layout reference at most. The Lost Age's own
  ship interiors stay the source.
- **Kutejnikov's Background with ruins** (CC0): a 1920×1080 monochrome painting, not pixel art.
- **Kenney's pirate pack hulls** (already on the PC): flat vector art at 66×113 that doesn't read as pixel art beside
  The Lost Age's map. Asset-priorities §1.4's "adapt Kenney's pirate pack where a hull fits" finds no hull that fits.
- **Spell Effects by StarsteelGaming**, **the 496 RPG icons**, **Tomcat94's and Imanor's emotes** and **PixelOE**: see
  their entries above.

## 7. On the decision page

Under "From the art sources research", 24 questions: one for each of the 16 downloads above, asking for your yes with
its licence and what it fills, and 8 make-or-reuse choices: battle's status marks (Golden Sun's own or RPG UI Icons),
Herb, Nut and Mint (Golden Sun's own icons or drawn by us), the bases for the skiff and the Wayfarer, the Churn's
whirlpool, the forge's battle backdrop, the field Psynergy shapes for the demo, how the logo is made, and how the
portraits are made.
