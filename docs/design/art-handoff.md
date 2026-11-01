# Art handoff: what we make ourselves, with briefs (1 Nov 2026)

This page lists every piece of art the art pass must make because nothing free fits it: 36 pieces for the demo (§2)
and 3 after it (§3). The search behind it is in [art-sources.md](art-sources.md). Each piece has its own section, in
the art pass's order (visual-survey.md §9): what it is and where it goes, its exact spec, what it must sit beside, how
it is checked, which way to make it and why, and a brief ready to paste into another model. A brief marked Code goes
only to a model that writes code, never to an image generator (open 102); only §2.30, §3.1 and §3.2 may go to an image
tool. A brief marked "Code here only" works on Golden Sun's own pictures and is used only on this PC (§1.3). A brief
assumes no knowledge of this project: it carries its own sizes, palette as hex, frame times and file names.

The rules come from the decided answers: Golden Sun's own room tiles at 2× (art 8), LPC people from the generator (art
3-5), generated art only where Golden Sun has nothing (open 91), drawn in code to its palette and 16-pixel grid with
light from the top-left, an image generator only for painted pieces (open 102), and every piece on a contact sheet for
your yes before it goes in (demo 21). The decided answers 169 to 180 (1 Nov) set several pieces below.

## 1. What every piece follows

### 1.1 The look

- **Golden Sun's rooms:** flat top-down, seen a little from the front, so walls, crates and houses show their tops and
  their front faces. The Lost Age's world map is the same view at the same 16-pixel cells.
- **16×16-pixel cells.** Our tiles are drawn at that size and shown at 2×, like Golden Sun's.
- **15-bit colour.** 32 levels a channel. In 8-bit values a level L is (L<<3)|(L>>2), that is L×8 + L÷4 (rounded
  down): 0, 8, 16, 24, 33, 41, 49, 57, 66, 74, 82, 90, 99, 107, 115, 123, 132, 140, 148, 156, 165, 173, 181, 189, 198,
  206, 214, 222, 231, 239, 247, 255. That is how our exporter writes Golden Sun's room tiles.
- **About 15 colours a tile.** Each 8×8 block (the GBA's own tile) uses one 16-colour palette with colour 0
  transparent, and a sheet uses at most 16 such palettes. Take ramps from the Golden Sun tile a piece sits beside
  first (§1.6), and add a hue only where none fits.
- **Light from the top-left.** Highlights on top and left edges, shade on bottom and right, cast shadows down and to
  the right, in soft ramps of two to four steps.
- **Outlines.** Ground tiles have none. Objects and sprites take a dark outline from their own darkest shade, never
  pure black. Item icons and badges take a near-black outline, as Golden Sun's item icons do. LPC layers keep LPC's
  own outline.
- **Hard edges.** Alpha 0 or 255 only: no anti-aliasing, gradients or blur, and dithering only where the Golden Sun
  neighbour dithers. Fog, glows and Psynergy may use up to three fixed alpha steps (25, 50 and 75 per cent), the way
  the GBA blends.
- **Time and facings.** Frame times are in ticks, 60 to a second (4 ticks 67 ms, 5 ticks 83 ms, 6 ticks 100 ms, 8
  ticks 133 ms, 10 ticks 167 ms, 12 ticks 200 ms, 15 ticks 250 ms, 20 ticks 333 ms, 30 ticks 500 ms, 60 ticks 1 s).
  Any sprite with facings has one row per facing, in the engine's order: e, se, s, sw, w, nw, n, ne
  (`GsSpriteFrames.DIRS`). A 4-facing sprite uses e, s, w, n.

### 1.2 Sizes and files

- **The picture** is 480×320. The cover screen shows a 746×320 view at 3× and the inner screen a 480×432 view at 4×
  (art-integration.md §3b). Golden Sun's tiles show at 2× in that picture, the LPC people 1:1, the UI at 2×.
- **Our own art** goes in the engine's `assets/own/<kind>/`, each sheet with a JSON beside it that lists its cells, as
  `assets/ui/*.json` do. The kinds used below: `tiles`, `world`, `ships`, `icons`, `effects`, `shaders`, `ui`,
  `battle`, `stills`, `portraits`. Stills are already read from `assets/own/stills/<name>.png` (`data_src/stills.json`).
- **The JSON beside a sheet** has the shape of `assets/ui/prompts.json`: `{"tile": [16, 16], "columns": 8, "cells":
  {"<name>": [x, y, w, h]}}`, cells left to right and top to bottom. An animated piece names its cells
  `<name>_<facing>_<frame>` (or `<name>_<frame>` with no facings), frames from 0, and adds `"ticks": {"<name>": N}`,
  its frame time. Each brief repeats the shape.
- **Recipes.** Each piece drawn in code has a saved recipe, `tools/own_art/<name>.json`, drawn by one saved script,
  `tools/draw_own.py`, written in the first art job. Any piece can then be drawn again.
- **Golden Sun stays local.** A piece made by recolouring or rearranging Golden Sun's own art stays in the gitignored
  `assets/gs`; only its recipe (a colour map, a mask) is ours. A piece built on a share-alike source keeps that
  licence, noted in its JSON and in credits.md.

### 1.3 Three ways to make a piece

1. **Drawn in code here, by our generator** (`tools/draw_own.py`): tiles, icons, ships, effects, glyphs and shaders.
   The palette and grid come out exact and nothing drifts (open 102). This is the default, and every brief marked Code
   asks for a script that places each pixel, never for a generated picture.
2. **An image tool reachable here:** Canva's generate-image (through the Canva connector; it takes uploaded pictures
   as references) or Magic Patterns' generate_image (up to five pictures at once, with reference pictures). Figma's
   generate_image is reachable too, but spends Figma AI credits. Only for painted pieces (decision 23, open 102): the
   stills (§2.30), the portraits (§3.1) and the painted Chart (§3.2). Output goes through Proper Pixel Art (the grid),
   tiledpalettequant (the palette) and SuperFamiconv (the check), then a hand clean-up. Those three tools wait for
   your yes (art-sources.md §3). Send image tools only our own art and LPC sheets as references, never Golden Sun's
   art, and never the Mana Soul pack (its author's request). Describe Golden Sun's look in words instead.
3. **Another model, outside this session:** a model with image generation when a painted piece needs one character
   held the same across many pictures (the portraits), or when the tools here keep drifting; a model that writes code
   for a Code brief. Paste the brief as it stands. Never send Golden Sun's art to another model either: a brief marked
   "Code here only" stays on this PC. Where such a brief must go outside, replace the supplied tiles with their colours
   as hex values (§1.6) and their cell sizes.

### 1.4 How every piece is checked

1. **The tile check:** `superfamiconv convert -M gba -T 4096 -i <sheet> -v` passes: no 8×8 block over 16 colours, at
   most 16 palettes. (`-T 4096` lifts gba mode's cap of 1,024 tiles, which a 376×216 still's 1,269 tiles would break
   on count, not colour.) That is half of the tile check world-map.md §5.5 asks for. The other half, comparing a made
   tile's colours and cell edges with its Golden Sun neighbour, is a short script of our own in `tools/`.
2. **A contact sheet** (`tools/contact_sheet.py`) shows the piece at 2× beside the Golden Sun tile or LPC person it
   sits with, on both Fold views (the cover's 746×320 at 3×, the inner 480×432 at 4×), by day and by night where the
   place has a night. Animated pieces also get a frame strip.
3. **Your yes:** the sheet is sent to you for a yes or a redo, and goes onto the decision page, before the piece is
   wired in (demo 21, open 102).

Each section below says "the standard check" for these three steps and adds what is particular to it.

### 1.5 Not on this page

These need no new art: engine fixes or decided reuse.

- **Engine fixes:** solid windows with the ones underneath hidden and windows sized to their rows (open 169: the navy
  fill made opaque); the back sprites' palettes, the command box, the party's line and the six-enemy line; the
  creator's preview, swatches and arrows; the camera and the room edges' east columns; the stick hidden over
  full-screen menus.
- **Reuse:** Commodore Ilse's bicorne is in the LPC generator (`hat_bicorne_athwart_commodore`, OGA-BY 3.0); nod and
  shake head are composed from LPC rows (art 2); the Chart's ship marker is Kenney Cartography's ship; Pokémon icons
  and followers come from the expansion; the hero kit comes from the generator (art 5).
- **Golden Sun clips:** Fallhaven's high town (open 171), Brann's back room (open 173), the Vault's halls, the sea
  caves, the Greenwild's swamp, the Bastion jail, Canalport's banks and jetty, the relay stone and the memorial stone.

### 1.6 Palettes

Every ramp below runs dark to light and is already 15-bit. The Golden Sun ones were sampled on 1 Nov from the local
exports (The Lost Age's world map, and our rooms rendered from their Golden Sun clips with `tools/render_room.py`);
the library ones are snapped to the nearest 15-bit level. A colour is only a value, so these may go in any brief.

The Lost Age's world map (what the world map's pieces sit beside):

- **Map deep sea:** `#1831ce #1842d6 #1852d6 #1863e7`
- **Map shallow sea:** `#1873f7 #1884f7 #189cf7 #18adff #18bdff #18def7`
- **Map foam:** `#84efe7 #bdeff7 #f7f7f7`
- **Map sand:** `#ced68c #e7de9c #efe7ad #f7efad #fff7de`
- **Map grass:** `#528c5a #5ace6b #6bde63 #7bef52`
- **Map cliff:** `#4a296b #5a4a73 #736352 #947352 #ad8c73 #c6b594 #e7cea5`
- **Map sea rock** (blue-greys): `#5a527b #636363 #8494a5 #94adbd #a5b5bd #b5c6ce`
- **Map slate** (the cliffs' blue shade and the darkest stone): `#31425a #396394 #637b94`
- **Map falls:** `#7bbdde #8cb5f7 #a5d6de #deeff7 #eff7ff #f7f7f7`

Golden Sun's rooms (from the room each piece sits in):

- **Cyan sea** (open 172; the water of Golden Sun 1's ship room 109 at Lantern Reef and the Wayfarer, as at Marrow
  cove): `#0884f7 #089cf7 #08adf7 #10b5ff #21ceff #42e7ff #73f7ff #9cf7ff`; Marrow cove's shore foam adds `#deffff`
- **Ship deck** (room 109: Lantern Reef, the Wayfarer): `#4a3118 #7b4a21 #bd8442 #de9c5a #efc67b #f7d68c #ffde94`
- **Ship hull** (room 109): `#6b4a31 #845a39 #a57342 #b57b42 #dead6b #f7ce84`
- **Lemurian ship** (The Lost Age's room 42: the Bazaar): hull `#6b3939 #844a42 #9c5a42 #b5734a #c68452`, deck
  `#c6a594 #dec68c #e7ce8c #e7de8c`, rail `#a59c9c #bdbdb5 #dedece #ffffe7`
- **Grass** (Stonehollow and Marrow cove): `#296339 #29944a #52c663 #7bf731 #adff52 #ceff5a`
- **Thatch gold** (Stonehollow's roofs): `#844a18 #9c5a08 #bd7300 #d69410 #efbd21 #ffde29 #ffef39 #ffff6b`
- **River blue** (Stonehollow's river): `#005a94 #006ba5 #007bb5`
- **Cove sand** (Marrow cove): `#bdb56b #d6c663 #e7d663 #efe763`
- **Jetty wood** (Marrow cove): `#945229 #ad7339 #bd844a #dea54a #e7bd63 #f7d663 #ffef73 #ffff84`
- **Cove earth** (Marrow cove's cliffs): `#633929 #845239 #946339 #ad8c5a #c6b55a #d6c66b`
- **Vault stone** (the Vault halls' blue-grey bricks): `#314294 #4252ad #637bad #7b94a5 #9cad9c #b5c694 #d6de8c`
- **Vault violet** (the Vault halls' floor): `#391852 #4a2163 #5a2973 #6b3184 #7b3994`
- **Canal water** (Canalport, from The Lost Age's Alhafra): `#00a5de #18b5ce #39bdbd #6bc6ad`
- **Canal stone** (Canalport): `#637b94 #849c94 #a5bd94 #b5d694 #bdef94 #d6ffa5 #f7ffb5`
- **Forge red** (the Forge sanctum's walls): `#843142 #b51042 #d61831 #f70821 #ff1818`
- **Fire** (the Forge sanctum's braziers): `#210000 #521000 #843900 #b54a00 #f77310 #ffe763 #ffffad`
- **Iron** (the Bastion jail's bars): `#182121 #293131 #31424a #949c94`; its darkest, `#182121`, is our near-black
  outline
- **House wood** (Brann's cottage, from The Lost Age's Madra houses): `#946b31 #b58442 #d69c52 #efad5a #f7bd39
  #ffe79c`

Ours and the libraries:

- **Red potion** (DCSS `potion/ruby`, snapped): `#840000 #9c0000 #bd0000 #de0000`, light `#ff8484 #ffbdbd`
- **Blue potion** (DCSS `potion/brilliant_blue`, snapped): `#000084 #00009c #0000bd`, light `#a5a5de`
- **Ilse's navy** (her LPC coat, snapped): `#292142 #31296b #394aad #426bc6`
- **The UI** (`src/ui/ui_style.gd`, drawn by the engine, not 15-bit): navy `#141433`, border `#e6e6f2`, edge
  `#6f6f6f`; the navy snapped to 15-bit is `#101031`
- **Kenney's key prompts** (`assets/ui/prompts.png`, CC0, kept as they are): `#434a5f #707485 #959ab1 #dce1e7 #ffffff`

## 2. The pieces, in the art pass's order

### 2.1 The sea backdrop's night and fog versions (item 2)

**What and where.** Open 103 made The Lost Age's ship-deck battle backdrop the backdrop for fights at sea, with a
night version tinted to match Pixel-boy's nights and a fog version for the north fog. Open 98 makes night at sea
darker.

**Spec.**
- No new drawing: both are made from the exported day picture, at its own canvas size.
- **Night:** a fixed colour map applied to the day picture: a 32-level lookup table, one entry per 15-bit level (32
  slices of 32×32, a 1024×32 PNG), sampled with nearest filtering, so every output stays on the 32 levels and no two
  shades merge. Darker and bluer, the deck's wood kept warm (open 177), any lantern on the deck lit. Match it by eye to
  Pixel-boy's `beach_night.png`, but brighter than his murkiest nights (art approval 5).
- **Fog:** the pixel cloud shader (art-sources.md §4.5) in four greys sampled from the backdrop's own sky, drawn over
  the sea and sky only, through a mask that keeps the deck and rail at full colour. Add a mask uniform and write
  `COLOR = vec4(c.rgb, c.a * mask_step)`, not `c * transparency`, so the four greys keep their 15-bit values. Drift 4
  world px a second. Until the backdrop is exported, the greys are the map sea rock's `#636363 #8494a5 #a5b5bd
  #b5c6ce`.
- **Frames:** none. The fog drifts in the shader.
- **Files:** the backdrop stays in `assets/gs`. Ours: `assets/own/battle/sea_night_lut.png` and
  `assets/own/battle/sea_fog_mask.png`.

**Sits beside.** The Lost Age's deck backdrop by day, Pixel-boy's beach scene by night.

**Check.** The standard check, with the three versions side by side and an Adept and a partner standing on each.

**Made by:** code here: a table and a mask drawn by the generator, over a picture we already have.

```text
Brief (Code here only: the supplied picture is Golden Sun's and never leaves this PC. Code, not an image tool: the
table and mask are made by the game's own generator, tools/draw_own.py, open 102): write a Python script (Pillow
only, no image generator) that makes a night and a fog version of a Game Boy Advance battle background of a ship's
deck at sea (supplied: a top-down deck in the foreground, sea and sky behind). Do not redraw it. Night: a colour
lookup table with one entry per 15-bit level, 32 slices of 32x32 (a 1024x32 PNG), read with nearest filtering. It
makes the picture darker and bluer while warm hues (reds, oranges, browns, yellows) keep their hue and lose only half
as much brightness, so wood stays warm. Every output colour must be 15-bit (each channel one of 32 levels: 0, 8, 16,
24, 33, 41 ... 247, 255). Fog: a black-and-white mask PNG the size of the picture, white over sea and sky, black over
the deck and rail, with hard edges. The fog's four greys: #636363 #8494a5 #a5b5bd #b5c6ce. No frames.
Files: assets/own/battle/sea_night_lut.png and assets/own/battle/sea_fog_mask.png. Deliver the script, its recipe
as tools/own_art/sea_backdrop.json, the two PNGs, and a before and after picture of both versions.
```

### 2.2 The forge's battle backdrop (item 2)

**What and where.** Demo 30 gave the battle's gaps to Essentials' backdrops, but Essentials has no forge, so fights in
the Forge hall and sanctum (mission 4) have none. The decision page asks how to make it; the recommended way is
below.

**Spec.**
- **Canvas:** 640×480, the same as Pixel-boy's scenes, drawn at 1× in the picture with its horizon clamped.
- **Built from the Forge sanctum's own Golden Sun tiles at 2×** (32 px a tile on the canvas): its railing walls and
  banners as the back wall, from the top down to the horizon line; two fire braziers on the wall's foot (the
  sanctum's own, flickering 4 frames at 8 ticks, 133 ms); its cobbled floor below the horizon to the bottom edge; the
  red rug running away from the viewer down the middle.
- **Horizon** at the same height as in Pixel-boy's `castle_court_day.png` (`horizon_y` in
  `data_src/battle_backdrops.json`), so the battlers stand the same way.
- **Palette:** the tiles' own colours and no others (it composes, it draws nothing): among them forge red and fire
  (§1.6).
- **Day only:** indoors has no night.
- **Files:** it is Golden Sun's art, so the pictures stay local, `assets/gs/battle/forge_0.png` to `forge_3.png`
  (one per flicker frame); the recipe is ours, `tools/own_art/forge_backdrop.json`.

**Sits beside.** The Forge hall and sanctum rooms, Pixel-boy's castle court, Golden Sun's enemy sprites at 2×.

**Check.** The standard check, with the sluice beast and Ho-Oh's judgement standing on it.

**Made by:** code here, by the generator from the room's own tiles, so the fight looks like the room it starts in.

```text
Brief (Code here only: the supplied tiles are Golden Sun's and never leave this PC. Code, not an image tool: composed
by the game's own generator, tools/draw_own.py, open 102): write a Python script (Pillow only, no image generator)
that composes a 640x480 battle background for a fire temple's inner hall from the supplied tile pieces only (wall
with railings and banners, two fire braziers, cobbled floor, a red rug), each tile shown at 2x (32 pixels). The back
wall fills the top part down to the horizon line (given in pixels). The floor fills the rest, with the rug running
from the bottom centre toward the wall. The braziers sit at the wall's foot, a third in from each side, with their
own 4-frame flicker at 8 ticks (133 ms) a frame. No colours beyond the tiles' own. Hard pixel edges, no blur, no
perspective scaling of the tiles. Files: assets/gs/battle/forge_0.png to forge_3.png, one per flicker frame. Deliver
the script, its recipe as tools/own_art/forge_backdrop.json (the tile placement), and the four PNGs it writes.
```

### 2.3 The Kestrel, recoloured (item 5)

**What and where.** The Kestrel is a Tidewarden cutter that Ilse lends in mission 3. Open 97 made her The Lost Age's
ship sprite, recoloured as a cutter, on the world map. The ship sprite has not been identified in the export yet
(UnboundHack's `notes/gs_field_sprites.md`), so finding it is the first step.

**Spec.**
- The Lost Age's ship frames and facings as the export holds them, mapped to the engine's facing order, at the
  sprite's own frame time (20 ticks, 333 ms, like the skiff and the Wayfarer, if the export gives none). If it has
  fewer than 8 facings, the missing diagonals use the nearest side row (art 3's rule).
- **Recolour only, no redraw:** the hull a darker tarred brown (ship hull's and ship deck's darkest: `#4a3118
  #6b4a31 #845a39`), the sails off-white (the Lemurian rail's `#bdbdb5 #dedece #ffffe7`) with one Tidewarden-blue band,
  a blue pennant at the masthead. The blue is Ilse's navy, the blue of her LPC coat: `#31296b #394aad #426bc6`. The
  order's sigil (a wave beneath a closed ring) goes on the mainsail only if the sail has at least 5×5 clear pixels.
- **Files:** the frames stay in `assets/gs`; the colour map is ours, `assets/own/ships/kestrel_recolour.json`.

**Sits beside.** The Lost Age's world-map sea and coasts, Ketch's skiff (§2.4) and the Wayfarer (§2.5) at the same
scale.

**Check.** The standard check, with the three ships side by side on the map's sea in all facings.

**Made by:** code here, by the generator: a colour map over a sprite we have.

```text
Brief (Code here only: the supplied sprite is Golden Sun's and never leaves this PC. Code, not an image tool: the
recolour is made by the game's own generator, tools/draw_own.py, open 102): write a Python script (Pillow only, no
image generator) that recolours a Game Boy Advance world-map ship sprite (supplied, all facings) into a navy cutter.
Keep every pixel and the outline, change only colours, with no more colours than the original. Hull, dark to light:
#4a3118 #6b4a31 #845a39. Sails: #bdbdb5 #dedece #ffffe7, with one band across the mainsail in #31296b #394aad
#426bc6. A small pennant at the top of the mast in #394aad #426bc6. The frames keep their own timing. File:
assets/own/ships/kestrel_recolour.json, a map of old colour to new colour as {"#rrggbb": "#rrggbb"}. Deliver the
script, the JSON and the recoloured sheet (kept local).
```

### 2.4 Ketch's skiff (item 5)

**What and where.** Ketch, a Rimborn pilot, runs Corvin's crew through the Galeway's lanes in a small dark skiff (the
opening's last still brings it home). Open 97: drawn by us. The decision page asks whether to start from nothing or
from LPC Overworld's sailboat; the recommended way is from nothing.

**Spec.**
- **Frame:** 16×16 (one map cell). **Facings:** 8, one row each in the order e, se, s, sw, w, nw, n, ne.
- **Frames:** 2 a facing, 20 ticks (333 ms) each: frame 1 at rest, frame 2 one pixel lower (a bob). Sheet 32×128.
- **Look:** a long, narrow, low hull of dark tarred wood (a three-step dark brown, the Golden Sun ship's darkest
  wood), one small patched lateen sail in grey-brown canvas, a single hooded figure of 2 by 3 pixels at the stern.
  Dark outline from the near-black iron.
- **Palette:** hull `#4a3118 #6b4a31 #845a39`; sail (map cliff) `#736352 #947352 #ad8c73`, patch `#c6b594`; figure
  `#31424a`; outline `#182121`.
- **Files:** `assets/own/ships/skiff.png` and `skiff.json`. The wake is §2.6.

**Sits beside.** The Kestrel (§2.3), The Lost Age's world-map sea, the storm ring (§2.8).

**Check.** The standard check, with the skiff on calm sea and inside the storm ring, where it must still read.

**Made by:** code here, by the generator: a small sprite with an exact palette.

```text
Brief (Code, not an image tool: this piece is drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, a tiny sailing skiff for a
Game Boy Advance world map in the style of Golden Sun: The Lost Age (2002), seen from above at a slight front angle.
Frame 16x16 pixels, 8 facings (east, south-east, south, south-west, west, north-west, north, north-east), 2 frames
each (the second frame one pixel lower, a bob), 20 ticks (333 ms) a frame. Sheet 32x128: columns are the 2 frames,
rows the 8 facings in that order. A long, narrow, low hull of dark tarred wood, one small patched lateen sail in
grey-brown canvas, one hooded figure (2 by 3 pixels) at the stern. Light from the top-left. Palette, dark to light
(15-bit; add a colour only where none fits, and list it): hull #4a3118 #6b4a31 #845a39, sail #736352 #947352 #ad8c73,
patch #c6b594, figure #31424a, outline #182121 (never pure black). Hard pixel edges, no anti-aliasing. Transparent
background. Files: assets/own/ships/skiff.png and skiff.json, as {"tile": [16, 16], "columns": 2, "cells":
{"skiff_e_0": [0, 0, 16, 16], "skiff_e_1": [16, 0, 16, 16], ...}, "ticks": {"skiff": 20}}. Deliver the script, its
recipe as tools/own_art/skiff.json, and the PNG and JSON it writes.
```

### 2.5 The Wayfarer on the world map (item 5)

**What and where.** The Wayfarer is the Farer ship found under Marrow Isle in mission 10, sailing the Calm from then
on. Open 97: drawn by us with her own silhouette and the six marks, since no Golden Sun ship resembles her. Story.md
§8: pale grey wood that seems alive and asleep, sails folded along her sides like wings, an engine of six glass
chambers with only the Flame chamber alight. The decision page asks whether to start from a free hull; the
recommended way is from nothing.

**Spec.**
- **Frame:** 32×32 (2×2 cells). If The Lost Age's ship frame proves larger than 32 px, the Wayfarer takes that frame
  size instead. **Facings:** 8, in the engine's order. **Frames:** 2 a facing (a one-pixel bob), 20 ticks (333 ms).
  Sheet 64×256.
- **Look:** a long, low hull with a raised, swept-back prow and stern, like a bird at rest; pale grey wood in four
  steps with a faint blue-green cast; two long folded sails lying along her sides like closed wings; no raised sail; a
  row of six pale gold marks along the bow rail, one pixel each; a warm orange glow of 2×2 pixels at the stern,
  flickering on frame 2 (the Flame chamber).
- **Palette:** wood (map sea rock and falls) `#8494a5 #a5b5bd #b5c6ce #deeff7`, outline `#5a527b`; folded sails
  `#a5d6de #eff7ff`; marks `#ffde29`; glow `#f77310`, `#ffe763` on frame 2.
- **Files:** `assets/own/ships/wayfarer.png` and `wayfarer.json`. The wake is §2.6.

**Sits beside.** The Kestrel and the skiff at the same scale, The Lost Age's map, the Wayfarer's deck room (the Golden
Sun hull that reads well from above, survey §7).

**Check.** The standard check, with all three ships in a row in all facings, so each reads as its own ship at a glance.

**Made by:** code here, by the generator: her silhouette is ours and must hold exactly at 32 px.

```text
Brief (Code, not an image tool: this piece is drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, a mysterious ancient ship
for a Game Boy Advance world map in the style of Golden Sun: The Lost Age (2002), seen from above at a slight front
angle. Frame 32x32 pixels, 8 facings (east, south-east, south, south-west, west, north-west, north, north-east), 2
frames each (the second one pixel lower, a bob), 20 ticks (333 ms) a frame. Sheet 64x256: columns are the frames,
rows the facings in that order. A long, low hull with a raised, swept-back prow and stern, like a bird at rest. Pale
grey wood with a faint blue-green cast. Two long folded sails lying along her sides like closed wings, no sail raised.
Six tiny pale gold marks in a row along the bow rail. A 2x2 warm orange glow at the stern that brightens on frame 2.
Light from the top-left. Palette, dark to light (15-bit; add a colour only where none fits, and list it): wood
#8494a5 #a5b5bd #b5c6ce #deeff7, outline #5a527b (never pure black), sails #a5d6de #eff7ff, marks #ffde29, glow
#f77310 then #ffe763 on frame 2. At most 15 colours plus transparent per 8x8 block. Hard pixel edges. Transparent
background. Avoid anything that looks like a pirate ship or a Viking longship. Files: assets/own/ships/wayfarer.png
and wayfarer.json, as {"tile": [32, 32], "columns": 2, "cells": {"wayfarer_e_0": [0, 0, 32, 32], ...}, "ticks":
{"wayfarer": 20}}. Deliver the script, its recipe as tools/own_art/wayfarer.json, and the PNG and JSON it writes.
```

### 2.6 The ships' wake (item 5)

**What and where.** The survey's ships job asks for a small ship "with 4 or 8 facings and a wake". Golden Sun's map
draws foam behind a moving ship; ours needs one for all three hulls.

**Spec.**
- Two sizes: 16×16 for the skiff, 32×32 for the Kestrel and the Wayfarer.
- **Frames:** 4 a facing, 8 ticks (133 ms) each, a V of foam behind the stern that opens and fades; frame 4 the
  smallest. **Facings:** 8, in the engine's order. Sheets 64×128 and 128×256.
- **Colours:** the lightest step of The Lost Age's map sea and its foam, the sea it is drawn on: `#18def7 #84efe7
  #f7f7f7`. Drawn under the hull, only while the ship moves.
- **Files:** `assets/own/ships/wake_16.png`, `wake_32.png`, with `wake_16.json` and `wake_32.json`.

**Sits beside.** The Lost Age's sea tiles, the three ships.

**Check.** The standard check, with a frame strip of each ship turning a full circle.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: this piece is drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, the foam wake behind a
moving ship on a Game Boy Advance world map in the style of Golden Sun: The Lost Age. Two sizes: 16x16 and 32x32
pixels. For each, 8 facings (east, south-east, south, south-west, west, north-west, north, north-east) as rows and 4
frames as columns, 8 ticks (133 ms) a frame: a V of foam trailing behind the stern that widens and fades, the fourth
frame the smallest. The ship itself is not drawn, only the foam, placed where the stern would be. Colours: #18def7
#84efe7 #f7f7f7 only (15-bit). Hard pixel edges. Transparent background. Files: assets/own/ships/wake_16.png (64x128)
and wake_32.png (128x256), each with a JSON as {"tile": [16, 16], "columns": 4, "cells": {"wake_e_0": [0, 0, 16,
16], ...}, "ticks": {"wake": 8}}. Deliver the script, its recipe as tools/own_art/wake.json, and the PNGs and JSONs
it writes.
```

### 2.7 Place icons Golden Sun lacks (item 5)

**What and where.** Asset-priorities §1.5: Golden Sun's own town icons everywhere they fit, our own for the new
islets, the Tradewind Bazaar and Lantern Reef's wrecks. The demo needs Cockle Cay, Tortell's isle (seen inside the
lagoon), the Bazaar and Lantern Reef; Sandmere, Driftholm, Shelfback, Bellstone and Farer's Step come after it.

**Spec.**
- **Islets:** 32×32 (2×2 cells) each: Cockle Cay a low sandy islet with scrub and a shell beach; Tortell's isle an
  islet with a small round hut. The later islets the same size, each with one feature of its own.
- **The Bazaar:** 48×32 (3×2 cells): ships lashed side by side with striped awnings on their decks, seen from above.
- **Lantern Reef:** 48×48 (3×3 cells): three broken hulls on rocks, with one warm lantern pixel, made to sit inside
  the north fog (§2.9).
- Drawn onto the map's sea: the sea round each icon is left transparent so The Lost Age's water shows.
- **Palette** from The Lost Age's map: map sand, map cliff and map grass; wood from the ship hull, as the map shows no
  wood near enough; awnings forge red, canal water's teal and thatch gold, with the Lemurian rail's cream; the lantern
  `#ffe763`. LPC Overworld's wreck and docks can be the base if you approve that download (art-sources.md §4.5).
- **Frames:** none.
- **Files:** `assets/own/world/icons.png` and `icons.json`.

**Sits beside.** The Lost Age's own town and island icons, its coasts, the fog.

**Check.** The standard check, with each icon beside a Golden Sun town icon on the map, by day and by night.

**Made by:** code here, by the generator: small map pieces on an exact palette.

```text
Brief (Code, not an image tool: this piece is drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, world-map place icons for a
Game Boy Advance game in the style of Golden Sun: The Lost Age (2002), seen from above at a slight front angle, on
16x16-pixel cells. (1) Two 32x32 islets: a low sandy islet with green scrub and a pale shell beach, and an islet with
a small round hut. (2) A 48x32 floating market: three or four ships lashed side by side, striped awnings (red, teal,
gold) on their decks. (3) A 48x48 reef of three broken shipwrecks on dark rocks, with one warm yellow lantern pixel.
The sea around each icon is transparent. Light from the top-left. Objects take an outline from their own darkest
shade, not black. Palette, dark to light (15-bit; add a colour only where none fits, and list it): sand #ced68c
#e7de9c #efe7ad #f7efad #fff7de; rock #4a296b #5a4a73 #736352 #947352 #ad8c73 #c6b594 #e7cea5; scrub #528c5a #5ace6b
#6bde63 #7bef52; wood #6b4a31 #845a39 #a57342 #b57b42 #dead6b; awnings #b51042 #f70821, #18b5ce #39bdbd, #efbd21
#ffde29, with cream #dedece #ffffe7; lantern #ffe763. At most 15 colours plus transparent per 8x8 block. Hard pixel
edges. No frames. Files: assets/own/world/icons.png and icons.json, as {"tile": [16, 16], "columns": 8, "cells":
{"cockle_cay": [x, y, 32, 32], "tortell_isle": [...], "bazaar": [...], "lantern_reef": [...]}}. Deliver the script,
its recipe as tools/own_art/world_icons.json, and the PNG and JSON it writes.
```

### 2.8 The Galeway's storm ring and its eye (item 5)

**What and where.** The Galeway is a ring of storm about 450 px thick between the Calm and the Wide (world-map.md
§1.4). In Act I it is a wall that turns ships back; inside it, due east of Marrow Isle, is the eye, a calm pocket
where the Galeway relay stands. The survey found it mid grey with no clouds or rain (§2.10).

**Spec.**
- **Storm water:** 16×16 tiles, a dark slate sea with whitecaps, greyer than The Lost Age's deep sea, 4 frames at 15
  ticks (250 ms). An edge set where it meets the Calm's water (The Lost Age's map sea): 4 sides, 4 outer corners, 4
  inner corners, 4 variants of the straight edges, animated with the water.
- **Cloud band:** an overlay drawn by the pixel cloud shader (art-sources.md §4.5) in four greys from dark slate to
  pale grey, masked to the ring, its edge stepped over 2 cells, drifting clockwise at 6 world px a second. Add a mask
  uniform and write `COLOR = vec4(c.rgb, c.a * mask_step)`, not `c * transparency`, so the greys keep their 15-bit
  values.
- **Rain:** over the ring only, Evert's LPC rain recoloured to the storm's greys if you approve it, or 1-pixel streaks
  drawn in code.
- **Lightning:** every 4 to 9 seconds the cloud band's palette jumps to its two lightest steps for 4 ticks (67 ms),
  twice.
- **The eye:** a round pocket about 9 cells across of the Calm's own water, walled by the cloud band's darkest grey.
  The relay is a 32×32 icon at its centre, with no frames: a ring of dark standing stones with a faint gold light.
- **Palette:** storm water (map slate and sea rock) `#31425a #396394 #637b94 #8494a5`, whitecaps `#b5c6ce #f7f7f7`;
  the Calm's edge in map deep sea and map shallow sea; cloud band `#31425a #637b94 #8494a5 #b5c6ce`; stones `#5a527b
  #636363 #8494a5`, their light `#ffde29 #ffff6b`.
- **Files:** `assets/own/world/storm_tiles.png` and `storm_tiles.json`, `storm_mask.png`, `relay_icon.png`; the shader
  in `assets/own/shaders/` with its MIT notice.

**Sits beside.** The Lost Age's open sea and coasts, the fog (§2.9), the ships.

**Check.** The standard check, plus the joystick ring over the storm on both screens (it must stay visible, §2.20).

**Made by:** code here: tiles by the generator on an exact palette, and a shader with a fixed four-colour palette.

```text
Brief (Code, not an image tool: these tiles are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, a storm-sea tileset for a
Game Boy Advance world map in the style of Golden Sun: The Lost Age (2002), top-down, 16x16-pixel tiles. (1) Storm
water: a dark slate-grey sea with small white wave crests, 4 frames that loop at 15 ticks (250 ms) a frame. (2) Edge
tiles where the storm water meets the open sea: 4 straight sides, 4 outer corners, 4 inner corners and 4 more
straight-edge variants, each animated with the same 4 frames. (3) A 32x32 icon of a ring of dark standing stones with
a faint gold light at the centre, seen from above, with no frames. Light from the top-left. Palette, dark to light
(15-bit; add a colour only where none fits, and list it): storm water #31425a #396394 #637b94 #8494a5, crests #b5c6ce
#f7f7f7; open sea #1831ce #1842d6 #1852d6 #1863e7 and #1884f7 #18adff #18def7; stones #5a527b #636363 #8494a5, light
#ffde29 #ffff6b. At most 15 colours plus transparent per 8x8 block. Hard pixel edges, no blur. The tiles must join
with no visible seam. Files: assets/own/world/storm_tiles.png and storm_tiles.json, as {"tile": [16, 16], "columns":
4, "cells": {"storm_0": [0, 0, 16, 16], "storm_edge_n_0": [...], ...}, "ticks": {"storm": 15}}, and
assets/own/world/relay_icon.png. Deliver the script, its recipe as tools/own_art/storm.json, and the PNGs and JSON it
writes.
```

### 2.9 The north fog, and Westgloam's fog banks after the demo (item 5)

**What and where.** The north fog lies over the north-west Calm and hides Lantern Reef until a fog pilot (mission 6).
Westgloam's banks lie over the Wide's west and hide islands until fog sight (Act II), so they come after the demo.
The survey found the north fog near white beside the mid-grey fog sea, with the joystick ring vanishing on it
(§2.10).

**Spec.**
- **An overlay, not tiles:** the pixel cloud shader with four mid greys (no near-white), at 1 world px, drifting 3
  world px a second from the north-west. Add a mask uniform and write `COLOR = vec4(c.rgb, c.a * mask_step)`, not `c *
  transparency`, so the four greys keep their 15-bit values.
- **The mask:** one pixel per map cell, white where the world layout marks fog, its edges stepped over 2 cells in the
  three alpha steps.
- **Palette:** the north fog `#637b94 #8494a5 #a5b5bd #b5c6ce` (map slate and sea rock).
- **Westgloam's banks (after the demo):** the same shader in a bluer grey, `#637bad #7b94a5 #94adbd #a5b5bd`, slower,
  as separate banks over open sea, each hiding the islands under it until fog sight.
- **Frames:** none. The fog drifts in the shader.
- **Files:** `assets/own/world/fog_mask.png`, the shader's four colours in `assets/own/world/fog.json`; after the demo,
  `westgloam_mask.png`.

**Sits beside.** The Lost Age's sea, the storm ring's greys, Lantern Reef's icon inside it.

**Check.** The standard check, by day and by night (the night tint must not turn beaches the fog's grey, §2.35), and
the joystick ring over the fog on both screens.

**Made by:** code here: a shader with a fixed palette, as open 102 asks.

```text
Brief (Code, not an image tool: this fog is drawn in code by the game itself, a shader, open 102): write a fog
overlay for a Game Boy Advance-style world map (Golden Sun: The Lost Age look, 16x16-pixel cells), as a Godot 4
canvas_item shader. It draws drifting fog from fBm noise mapped to exactly four fixed mid-grey colours by thresholds
(no smooth blending), pixelated to whole map pixels, moving from the north-west at a set speed. Its density comes
from a mask texture with one pixel per 16x16 cell (white = fog), imported with nearest filtering. At the mask's edges
the fog thins in three hard alpha steps (75, 50, 25 per cent) over two cells. Write COLOR = vec4(colour.rgb,
alpha_step), never a colour multiplied by an alpha, so the four colours stay exactly: #637b94 #8494a5 #a5b5bd #b5c6ce
(15-bit). No frames: it moves in the shader. Files: assets/own/shaders/fog_map.gdshader and
assets/own/world/fog.json ({"colors": ["#637b94", "#8494a5", "#a5b5bd", "#b5c6ce"]}). Deliver the .gdshader file
with its uniforms named, the JSON, and a still picture of it running.
```

### 2.10 The Churn's whirlpool (item 5)

**What and where.** The Churn is a whirlpool in the south of the Calm, near the storm, seen in Act I and opened with
Whirlpool in Act II (world-map.md §1.3). No pixel-art whirlpool exists free. The decision page asks: animated tiles
drawn in code, or the vortex shader over Golden Sun's water. The recommended way is below. If The Lost Age's map has a
whirlpool among its pieces, that comes first (open 91).

**Spec.**
- **Size:** 48×48 (3×3 cells). **Frames:** 8 at 6 ticks (100 ms), a clockwise spiral turning one step a frame. Sheet
  384×48.
- **Colours:** The Lost Age's map sea, which the Calm is drawn from: pale foam arms (map shallow sea's lightest and
  map foam) spiralling into a centre of the map deep sea's darkest blue, `#1831ce`. Its outer ring matches the
  open-sea tile it is set in, so no seam shows.
- **Files:** `assets/own/world/whirlpool.png` and `whirlpool.json`.

**Sits beside.** The Lost Age's open sea, the storm ring's edge.

**Check.** The standard check, with a frame strip and the whirlpool set into the open sea on the map.

**Made by:** code here, by the generator: exact palette, hard edges, no resampling.

```text
Brief (Code, not an image tool: this piece is drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, an animated whirlpool for a
Game Boy Advance world map in the style of Golden Sun: The Lost Age (2002), top-down. 48x48 pixels, 8 frames side by
side (a 384x48 sheet) that loop at 6 ticks (100 ms) a frame: a clockwise spiral of pale foam arms turning into a dark
blue centre, each frame turned one step on. The outer edge must be plain open sea that joins the sea tile around it
with no seam. Palette, dark to light (15-bit; add a colour only where none fits, and list it): deep sea #1831ce
#1842d6 #1852d6 #1863e7, shallow sea #1884f7 #18adff #18def7, foam #84efe7 #f7f7f7. At most 15 colours plus
transparent per 8x8 block. Hard pixel edges, no blur, no glow. Files: assets/own/world/whirlpool.png and
whirlpool.json, as {"tile": [48, 48], "columns": 8, "cells": {"whirlpool_0": [0, 0, 48, 48], ...}, "ticks":
{"whirlpool": 6}}. Deliver the script, its recipe as tools/own_art/whirlpool.json, and the PNG and JSON it writes.
```

### 2.11 Marrow Isle's reef lagoon (item 5)

**What and where.** Marrow Isle's reef ring encloses a lagoon with Tortell's isle inside it. The Kestrel can't cross
the reef; a Rimborn pilot opens it from mission 10 (world-map.md §1.3). No reef or lagoon tiles exist in Golden Sun's
style.

**Spec.**
- **16×16 tiles:** lagoon water (a lighter turquoise over sand, 4 frames at 15 ticks, 250 ms, matched to The Lost
  Age's sea once its animation is read from the ROM, since the export has none yet), the reef (pink-brown coral heads
  and grey rock, foam breaking on the outer side, 4 frames at 15 ticks), sand bars, and two edge sets (lagoon to reef,
  reef to open sea), each with 4 sides, 4 outer and 4 inner corners.
- **Palette:** lagoon `#18bdff #18def7 #84efe7 #bdeff7` over map sand; coral (map cliff) `#736352 #947352 #ad8c73`;
  rock (map sea rock) `#5a527b #636363 #8494a5 #a5b5bd`; foam `#f7f7f7`; the open sea in map deep sea.
- LPC Overworld's water rocks can be the base if you approve that download.
- **Files:** `assets/own/world/reef_tiles.png` and `reef_tiles.json`.

**Sits beside.** The Lost Age's sea and Marrow Isle's coast, Tortell's isle icon (§2.7).

**Check.** The standard check, with the whole lagoon composed on the map.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: these tiles are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, a reef and lagoon tileset
for a Game Boy Advance world map in the style of Golden Sun: The Lost Age (2002), top-down, 16x16-pixel tiles. (1)
Lagoon water: light turquoise over pale sand, 4 looping frames. (2) Reef: pink-brown coral heads and grey rocks with
white foam breaking on the outer side, 4 frames. (3) Sand bars. (4) Edge tiles from lagoon to reef and from reef to
deep open sea: 4 sides, 4 outer corners and 4 inner corners each. Every animation 15 ticks (250 ms) a frame. Light
from the top-left. Palette, dark to light (15-bit; add a colour only where none fits, and list it): lagoon #18bdff
#18def7 #84efe7 #bdeff7, sand #ced68c #e7de9c #efe7ad #f7efad, coral #736352 #947352 #ad8c73, rock #5a527b #636363
#8494a5 #a5b5bd, foam #f7f7f7, deep sea #1831ce #1842d6 #1852d6 #1863e7. At most 15 colours plus transparent per 8x8
block. Hard pixel edges. Tiles must join with no seam. Files: assets/own/world/reef_tiles.png and reef_tiles.json,
frames in columns, as {"tile": [16, 16], "columns": 4, "cells": {"lagoon_0": [0, 0, 16, 16], ...}, "ticks":
{"lagoon": 15, "reef": 15}}. Deliver the script, its recipe as tools/own_art/reef.json, and the PNG and JSON it
writes.
```

### 2.12 The rim's bite (item 5)

**What and where.** The Rimfalls are a band of white water all round the world; The Lost Age's white edge ring with
its falls draws them. In the east the bite brings the falls within sight of the storm, and Fallhaven stands on the
last cliff there (world-map.md §1.6). The edge ring has no inward notch, so its turning pieces are ours.

**Spec.**
- **16×16 tiles:** the inner and outer corners where the falls' band turns inward and back, at 90° and 45°, and a
  cliff piece where Fallhaven's cliff meets the falls.
- Every colour, the frame count and the timing taken from The Lost Age's own falls tiles: map falls and map cliff.
  The export holds no animation for them yet, so until it is read from the ROM the corners use 4 frames at 10 ticks
  (167 ms). Where one of its tiles mirrored fits a corner, use it.
- **Files:** the mirrored Golden Sun tiles stay in `assets/gs`; our new corners in `assets/own/world/rim_bite.png` and
  `rim_bite.json`.

**Sits beside.** The Lost Age's falls ring and its open sea.

**Check.** The standard check, with the whole bite composed and animated.

**Made by:** code here, by the generator from the ring's own palette.

```text
Brief (Code here only: the supplied tiles are Golden Sun's and never leave this PC. Code, not an image tool: drawn in
code by the game's own generator, tools/draw_own.py, open 102): write a Python script (Pillow only, no image
generator) that extends a Game Boy Advance world map's edge-of-the-world waterfall band (supplied tiles, 16x16
pixels) with the pieces it lacks: inner and outer corners where the band turns inward into a notch and back out, at
90 and 45 degrees, and one piece where a sea cliff meets the falls. Use only the supplied tiles' colours (falls
#7bbdde #8cb5f7 #a5d6de #deeff7 #eff7ff #f7f7f7, cliff #4a296b #5a4a73 #736352 #947352 #ad8c73), their frame count
and their frame time (4 frames at 10 ticks, 167 ms, until the falls' own is known), so the new tiles animate in step.
Hard pixel edges, no blur. Files: assets/own/world/rim_bite.png and rim_bite.json, frames in columns, as {"tile":
[16, 16], "columns": 4, "cells": {"bite_inner_90_0": [0, 0, 16, 16], ...}, "ticks": {"bite": 10}}. Deliver the
script, its recipe as tools/own_art/rim_bite.json, and the PNG and JSON it writes.
```

### 2.13 Shore foam edges (items 6 and 10)

**What and where.** Canalport's beach needs the sea to "meet the sand with foam" (survey §2.3), and Marrow cove,
Fallhaven's harbour and Bastion's strand have grass running straight into the sea at a corner (§2.1, §2.2, §2.7).

**Spec.**
- **16×16 tiles**, built on Eldiran's CC0 shoreline template if you approve it (its own layout and frame count),
  filled with the sand of Marrow cove's Golden Sun tiles, or its grass for the grass corners, and the decided cyan sea
  (open 172). Foam in white and the sea's two lightest steps.
- Without the template: 4 straight sides, 4 outer corners, 4 inner corners and 4 straight-edge variants, 4 frames at
  15 ticks (250 ms), the frame stepping on every second tile.
- **Palette:** cove sand `#bdb56b #d6c663 #e7d663 #efe763`; grass `#296339 #29944a #52c663 #7bf731 #adff52`; cyan sea
  `#089cf7 #08adf7 #10b5ff #21ceff #42e7ff #73f7ff`; foam `#9cf7ff #deffff`.
- **Files:** `assets/own/tiles/shore_foam.png` and `shore_foam.json`.

**Sits beside.** Marrow cove's and Canalport's Golden Sun sand and sea tiles.

**Check.** The standard check, with Canalport's north beach and the four corners rebuilt.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: these tiles are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, an animated shoreline foam
tileset in the style of Golden Sun (Game Boy Advance, 2001), top-down, 16x16-pixel tiles. Pieces: 4 straight edges, 4
outer corners, 4 inner corners and 4 variants of the straight edges, where sand (or grass) meets bright cyan sea with
a thin band of white foam that rolls in and out over 4 frames at 15 ticks (250 ms) a frame. Light from the top-left.
Palette, dark to light (15-bit; add a colour only where none fits, and list it): sand #bdb56b #d6c663 #e7d663
#efe763, grass #296339 #29944a #52c663 #7bf731 #adff52, sea #089cf7 #08adf7 #10b5ff #21ceff #42e7ff #73f7ff, foam
#9cf7ff #deffff. At most 15 colours plus transparent per 8x8 block. Hard pixel edges, no blur. The tiles must join
each other and plain sand and sea tiles in those colours with no seam. Files: assets/own/tiles/shore_foam.png and
shore_foam.json, frames in columns, as {"tile": [16, 16], "columns": 4, "cells": {"sand_n_0": [0, 0, 16, 16], ...},
"ticks": {"sand": 15, "grass": 15}}. Deliver the script, its recipe as tools/own_art/shore_foam.json, and the PNG
and JSON it writes.
```

### 2.14 Lantern Reef's fog (item 6)

**What and where.** Open 176: a light drifting fog over the water and between the wreck's pieces, with the decks at
full colour, gone after Defog. Today one pale veil fades the whole room (survey §2.6).

**Spec.**
- Tennisson's pixel fog shader (art-sources.md §4.5) over the room, with AlPS_208's TIME fix.
- **Alpha in three steps:** change its last line to `COLOR = vec4(color.rgb, min(floor(final * color.a * 4.0) / 4.0,
  0.75))`, so the alpha takes only 0, 25, 50 or 75 per cent (`final` already carries the mask). With the colour's
  alpha at 0.6 the fog never passes 50 per cent, thin enough that the water shows through.
- **`fog_mask`:** one pixel per 16-px cell, white over water and the gaps, black over the decks and the jetty.
  Imported with nearest filtering and sampled at the snapped `grid_uv`, not the raw UV.
- **Pixelation:** on, at 2 world px. `pixelation_amount` divides the UV, not world pixels, so make it a vec2 set to
  the room's size in world px ÷ 2 (136 × 232 for the reef's 272×464), so the blocks are 2×2 world px.
- **Colour:** `#9cf7ff`, the room's own lightest water colour. Drift 3 world px a second.
- **Night:** the same fog under the night tint. **Defog:** a 60-tick (1 s) fade, then gone for good.
- **Files:** `assets/own/effects/lantern_reef_fog_mask.png`; the shader in `assets/own/shaders/fog_pixel.gdshader`
  with its MIT notice.

**Sits beside.** The reef's Golden Sun ship pieces and water, the LPC people on the decks.

**Check.** The standard check, by day and night, before and after Defog, with Vesper on a deck at full colour.

**Made by:** code here: a shader and a mask.

```text
Brief (Code, not an image tool: this fog is drawn in code by the game itself, a shader, open 102): set up a drifting
fog for one top-down Game Boy Advance-style room (Golden Sun look, 16x16-pixel cells, 17 by 29 cells, 272x464 px)
using a Godot 4 canvas_item fog shader with a density mask (Tennisson's MIT "Animated 2D Fog", supplied as text).
Make the mask: a PNG with one pixel per 16x16 cell, white over open water and the gaps between three wrecked ship
pieces, black over the ships' decks and the jetty (which cells are which is supplied as a text grid of our own room
data). Import it with nearest filtering and sample it at the snapped grid UV. Fog colour #9cf7ff (15-bit) with its
alpha at 0.6. Change the last line to COLOR = vec4(color.rgb, min(floor(final * color.a * 4.0) / 4.0, 0.75)), so the
fog takes only 0, 25, 50 or 75 per cent alpha. Make pixelation_amount a vec2 of 136 by 232, so each fog block is 2x2
pixels. Slow drift, 3 pixels a second. Fix the shader's known fault at large TIME values by offsetting its two noise
samples by different constants and adding a fog_speed factor. A Defog fade of 60 ticks (1 s) ends it. Files:
assets/own/effects/lantern_reef_fog_mask.png and assets/own/shaders/fog_pixel.gdshader. Deliver the mask PNG, the
shader and a still picture.
```

### 2.15 Lantern Reef's broken hull ends and the lantern's glow (items 6 and 14)

**What and where.** The reef's wreck is a Golden Sun ship broken in three, but its cuts are clean straight lines
(survey §2.6). At night a blue oval reads as a puddle; it is probably the old lantern's glow.

**Spec.**
- **Broken ends:** 16×16 overlay tiles laid along each cut: jagged plank ends of uneven length (2 to 6 px), one or two
  splinters, the dark inside of the hull and a rib or two showing. Both sides of each cut, with 4 variants a side so
  no two neighbours repeat. All in the ship's own wood ramp. No frames.
- **Debris:** 16×16 floating props for the gaps: three planks, a barrel, a crate lid. No frames.
- **The lantern's glow:** 32×32, 4 frames at 10 ticks (167 ms): two hard rings of warm yellow at 50 and 25 per cent
  round the lantern, flickering by one pixel. It replaces the blue oval.
- **Palette:** ship deck `#4a3118 #7b4a21 #bd8442 #de9c5a #efc67b #f7d68c #ffde94`; ship hull `#6b4a31 #845a39
  #a57342 #b57b42 #dead6b #f7ce84`; the hull's dark inside `#182121 #4a3118`; the glow `#ffe763`.
- **Files:** `assets/own/tiles/wreck_ends.png` and `wreck_ends.json`, `assets/own/effects/lantern_glow.png` and
  `lantern_glow.json`.

**Sits beside.** The reef's Golden Sun ship pieces, its water, the fog (§2.14).

**Check.** The standard check, with the three pieces rebuilt, by day and night.

**Made by:** code here, by the generator: overlays in the ship's own colours.

```text
Brief (Code, not an image tool: these pieces are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, broken-hull overlay tiles in
the style of Golden Sun (Game Boy Advance, 2001), top-down, 16x16 pixels, to lay along the straight cut edges of a
wooden ship broken into pieces. For each side of a cut (fore and aft), 4 variants: jagged plank ends of uneven length
(2 to 6 pixels), one or two splinters, the dark inside of the hull and a rib showing. Also 16x16 floating debris
(three planks, a barrel, a crate lid), and a 32x32 lantern glow of 4 frames at 10 ticks (167 ms) a frame: two
hard-edged rings at 50 and 25 per cent opacity that flicker by one pixel. Light from the top-left. Palette, dark to
light (15-bit; add a colour only where none fits, and list it): deck planks #4a3118 #7b4a21 #bd8442 #de9c5a #efc67b
#f7d68c #ffde94, hull #6b4a31 #845a39 #a57342 #b57b42 #dead6b #f7ce84, dark inside #182121, glow #ffe763. At most 15
colours plus transparent per 8x8 block. No blur. Files: assets/own/tiles/wreck_ends.png and wreck_ends.json, as
{"tile": [16, 16], "columns": 8, "cells": {"end_fore_0": [0, 0, 16, 16], ...}}, and
assets/own/effects/lantern_glow.png and lantern_glow.json ({"tile": [32, 32], "columns": 4, "cells": {"glow_0": [0,
0, 32, 32], ...}, "ticks": {"glow": 10}}). Deliver the script, its recipe as tools/own_art/wreck_ends.json, and the
PNGs and JSONs it writes.
```

### 2.16 The Bazaar's lashed hulls (item 6)

**What and where.** At the Tradewind Bazaar's bow a rectangle of open sea sits inside the hull; it is the gap to the
merchant's hull that Whirlwind's spar bridges, but it reads as a hole through one ship. The dragon prow is cut off by
the room's east edge (survey §2.8). The fix, from the survey: the merchant's hull as a separate hull with its own
rail, the furled sail on its deck, the whole prow inside the room.

**Spec.**
- **The merchant's hull:** a second hull beside the main ship across the gap, which stays open sea. Its deck from the
  Golden Sun ship's own deck tiles. Ours: its side planking facing the gap with a waterline, and its rail along the
  gap (16×16: a run, two ends and a post, posts every 16 px).
- **The furled sail:** a 48×16 prop on its deck, furled canvas with ties on a boom, the boom's shadow down and to the
  right.
- **Lashings:** a rope across the gap at each end (16×16, 2 variants), and fenders hung on both hulls (16×16).
- **The prow:** the room widened so the Golden Sun prow sits whole inside it.
- **Palette:** the Lemurian ship: hull `#6b3939 #844a42 #9c5a42 #b5734a #c68452`, deck `#c6a594 #dec68c #e7ce8c
  #e7de8c`, rail and canvas `#a59c9c #bdbdb5 #dedece #ffffe7`; rope in the deck's tans; the cyan sea at the waterline.
- **Frames:** none.
- [LPC] Ship's rails and furled sails are the base if you approve that download, redrawn at 16 px.
- **Files:** `assets/own/tiles/bazaar_hull.png` and `bazaar_hull.json`.

**Sits beside.** The Bazaar's Golden Sun ship and its deep blue water, now the decided cyan (open 172), the LPC
people, Whirlwind's spar.

**Check.** The standard check, with Wynn crossing the spar and the hero at the gangway (entrance 0).

**Made by:** code here, by the generator, on the Golden Sun ship's own palette.

```text
Brief (Code, not an image tool: these pieces are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, ship pieces in the style of
Golden Sun (Game Boy Advance, 2001), top-down at a slight front angle, 16x16-pixel tiles, so a second merchant ship
can sit beside a larger ship across a gap of open water. Pieces: the merchant hull's side planking seen from above
with a waterline (a run and two ends), its deck rail along the gap (a run, two ends, a post), a 48x16 furled sail on
a boom lying on deck with rope ties and a shadow down and to the right, a rope lashing that spans the gap (2
variants), and a hanging fender. Light from the top-left. Palette, dark to light (15-bit; add a colour only where none
fits, and list it): hull #6b3939 #844a42 #9c5a42 #b5734a #c68452, deck and rope #c6a594 #dec68c #e7ce8c #e7de8c, rail
and canvas #a59c9c #bdbdb5 #dedece #ffffe7, sea at the waterline #089cf7 #10b5ff #42e7ff. At most 15 colours plus
transparent per 8x8 block. Hard pixel edges. No frames. Files: assets/own/tiles/bazaar_hull.png and bazaar_hull.json,
as {"tile": [16, 16], "columns": 8, "cells": {"plank_run": [0, 0, 16, 16], "sail_furled": [x, y, 48, 16], ...}}.
Deliver the script, its recipe as tools/own_art/bazaar_hull.json, and the PNG and JSON it writes.
```

### 2.17 The Bazaar's stalls and goods (item 14)

**What and where.** The Bazaar reads as one hull and a few people, with no stalls, awnings or goods (survey §2.8).
Golden Sun's own crates and barrels come first; these fill the market's own look.

**Spec.**
- **Stalls:** 32×32 (2×2 cells): a striped awning seen from above with its front valance, a counter below, in four
  colour sets (red and cream, teal and cream, gold and brown, violet and cream).
- **Goods:** 16×16 each: a fish basket, bolts of cloth, pots, a fruit crate, rope coils, a lantern stand.
- **A hanging lantern:** 16×16 (lit at night, §2.35).
- **Palette:** awnings forge red `#b51042 #d61831 #f70821`, teal `#18b5ce #39bdbd #6bc6ad`, thatch gold `#d69410
  #efbd21 #ffde29`, vault violet `#4a2163 #6b3184 #7b3994`, cream (the Lemurian rail) `#bdbdb5 #dedece #ffffe7`, brown
  `#844a42 #9c5a42`; counters and baskets in the Lemurian deck and jetty wood; pots in cove earth; fish in map sea
  rock; fruit fire `#f77310` and grass `#7bf731`; the lantern iron and fire.
- **Frames:** none.
- **Files:** `assets/own/tiles/market.png` and `market.json`.

**Sits beside.** The Bazaar's Golden Sun decks, Golden Sun's crates and barrels, the LPC merchant and townsfolk.

**Check.** The standard check, with the deck dressed as the mission's market.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: these props are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, floating-market props in
the style of Golden Sun (Game Boy Advance, 2001), top-down at a slight front angle, to stand on a wooden ship deck.
(1) Four 32x32 market stalls: a striped awning seen from above with its front edge hanging down, a counter beneath,
in red and cream, teal and cream, gold and brown, violet and cream. (2) 16x16 goods: a fish basket, bolts of cloth,
clay pots, a fruit crate, a coil of rope, a lantern on a stand. (3) A 16x16 hanging lantern. Light from the top-left,
outlines from each object's own darkest shade. Palette, dark to light (15-bit; add a colour only where none fits, and
list it): red #b51042 #d61831 #f70821, teal #18b5ce #39bdbd #6bc6ad, gold #d69410 #efbd21 #ffde29, violet #4a2163
#6b3184 #7b3994, cream #bdbdb5 #dedece #ffffe7, brown #844a42 #9c5a42, wood #945229 #ad7339 #bd844a #dea54a #e7bd63,
pots #633929 #845239 #946339 #ad8c5a, fish #636363 #8494a5 #a5b5bd, fruit #f77310 #7bf731, lantern #182121 #31424a
#ffe763. At most 15 colours plus transparent per 8x8 block. Hard pixel edges. Transparent background. No frames.
Files: assets/own/tiles/market.png and market.json, as {"tile": [16, 16], "columns": 8, "cells": {"stall_red": [0,
0, 32, 32], "fish_basket": [...], ...}}. Deliver the script, its recipe as tools/own_art/market.json, and the PNG and
JSON it writes.
```

### 2.18 The sluice house (interiors job)

**What and where.** Canalport's old sluice house holds the sluice gates (and the Leather Cap); the sluice beast rises
in the channel outside, and after the fight the gates open and the lower town drains (mission-3-build.md). No Golden
Sun room has one (open 100).

**Spec.**
- **Walls and floor:** clipped from a Golden Sun stone interior, one style for the place.
- **Ours, 16×16 unless stated:** a stone-edged water channel across the room, with water flowing (4 frames at 10
  ticks, 167 ms) in Golden Sun's indoor water ramp; two sluice gates over the channel (32×48 each: a wooden gate in an
  iron frame, a closed state and an open state raised 24 px); a winch wheel (4 frames turning at 6 ticks, 100 ms,
  played as the gates open); an iron drain grate; wet stone stains (3 variants).
- **Palette:** the stone of the interior it is clipped into; until that is chosen, vault stone `#314294 #4252ad
  #637bad #7b94a5 #9cad9c #b5c694`; water (Canalport's canal) `#00a5de #18b5ce #39bdbd #6bc6ad`; gates in house wood
  `#946b31 #b58442 #d69c52 #efad5a`; iron `#182121 #293131 #31424a #949c94`.
- The Sewer tileset is the parts bin if you approve it, redrawn to Golden Sun's palette.
- **Files:** `assets/own/tiles/sluice_house.png` and `sluice_house.json`.

**Sits beside.** The Golden Sun stone interior it is clipped into, Canalport's Golden Sun water, the LPC people.

**Check.** The standard check, with the gates shut and open and Maren at the winch.

**Made by:** code here, by the generator: tiles on an exact palette (open 102).

```text
Brief (Code here only: the supplied stone tiles are Golden Sun's and never leave this PC. Code, not an image tool:
drawn in code by the game's own generator, tools/draw_own.py, open 102): write a Python script (Pillow only, no image
generator) that draws, pixel by pixel, an indoor sluice-house tileset in the style of Golden Sun (Game Boy Advance,
2001), top-down at a slight front angle, 16x16-pixel tiles, matching the supplied grey stone wall and floor tiles.
Pieces: a stone-edged water channel (straight, corners, ends) with flowing water over 4 frames at 10 ticks (167 ms);
two 32x48 sluice gates (a heavy wooden gate in an iron frame over the channel), each in a closed and an open state,
the open one raised 24 pixels; a 16x16 winch wheel in 4 turning frames at 6 ticks (100 ms); an iron drain grate;
three wet stone stains. Light from the top-left, outlines from each object's own darkest shade. Palette, dark to
light (15-bit; add a colour only where none fits, and list it): stone #314294 #4252ad #637bad #7b94a5 #9cad9c #b5c694
(or the supplied tiles' own), water #00a5de #18b5ce #39bdbd #6bc6ad, wood #946b31 #b58442 #d69c52 #efad5a, iron
#182121 #293131 #31424a #949c94. At most 15 colours plus transparent per 8x8 block. Hard pixel edges, no blur. Files:
assets/own/tiles/sluice_house.png and sluice_house.json, as {"tile": [16, 16], "columns": 8, "cells": {"channel_0":
[0, 0, 16, 16], "gate_closed": [x, y, 32, 48], ...}, "ticks": {"channel": 10, "winch": 6}}. Deliver the script, its
recipe as tools/own_art/sluice_house.json, and the PNG and JSON it writes.
```

### 2.19 The hatchery (interiors job)

**What and where.** Keeper Brann's hatchery in Stonehollow, where the first partner is chosen in mission 1 and the
Kin Garden's eggs hatch later (world-map.md §3.1). No Golden Sun room has one, and no free set does (open 100).

**Spec.**
- **Walls and floor:** clipped from a Golden Sun house interior, with its own desk, shelves and stove where they fit.
- **Ours:** incubators (32×32: a straw-lined wicker basket under a small brass lamp, one egg showing, the lamp's glow
  2 frames at 30 ticks, 500 ms, in two alpha steps); egg racks (32×16: wooden shelves holding six eggs in pastel
  colours); nest boxes with straw (16×16); a feed sack (16×16).
- **Palette:** house wood `#946b31 #b58442 #d69c52 #efad5a #f7bd39 #ffe79c`; straw and brass in thatch gold `#9c5a08
  #d69410 #efbd21 #ffef39`; eggs `#ffbdbd #a5a5de #bdeff7 #ceff5a #fff7de`; sack (cove sand) `#bdb56b #d6c663
  #e7d663`; the glow `#ffe763`.
- **Files:** `assets/own/tiles/hatchery.png` and `hatchery.json`.

**Sits beside.** The Golden Sun house interior, Brann's LPC look, the expansion's Pokémon on the field.

**Check.** The standard check, with Brann at the racks and the three starters' balls on the table.

**Made by:** code here, by the generator.

```text
Brief (Code here only: the supplied floor and wall tiles are Golden Sun's and never leave this PC. Code, not an image
tool: drawn in code by the game's own generator, tools/draw_own.py, open 102): write a Python script (Pillow only, no
image generator) that draws, pixel by pixel, props for a small creature hatchery inside a cottage, in the style of
Golden Sun (Game Boy Advance, 2001), top-down at a slight front angle, matching the supplied wooden floor and wall
tiles. (1) A 32x32 incubator: a straw-lined wicker basket under a small brass lamp, one egg showing, the lamp's warm
glow in 2 frames at 30 ticks (500 ms), as two hard-edged rings at 50 and 25 per cent opacity. (2) A 32x16 egg rack:
wooden shelves with six eggs in pastel colours. (3) A 16x16 nest box with straw. (4) A 16x16 feed sack. Light from
the top-left, outlines from each object's own darkest shade. Palette, dark to light (15-bit; add a colour only where
none fits, and list it): wood #946b31 #b58442 #d69c52 #efad5a #f7bd39 #ffe79c, straw and brass #9c5a08 #d69410
#efbd21 #ffef39, eggs #ffbdbd #a5a5de #bdeff7 #ceff5a #fff7de, sack #bdb56b #d6c663 #e7d663, glow #ffe763. At most 15
colours plus transparent per 8x8 block. Hard pixel edges. Transparent background. Files:
assets/own/tiles/hatchery.png and hatchery.json, as {"tile": [16, 16], "columns": 8, "cells": {"incubator_0": [0, 0,
32, 32], ...}, "ticks": {"incubator": 30}}. Deliver the script, its recipe as tools/own_art/hatchery.json, and the PNG
and JSON it writes.
```

### 2.20 The touch controls' backing (item 7)

**What and where.** Open 180: build Touch size's Auto, keep the controls over the picture, and give them a dark
backing. The grey A, B and joystick ring vanish over bright grass, trees, falls and white fog (survey §5, §2.10).

**Spec.**
- Behind the stick's ring and behind A, B, L and R: a filled disc in the UI's navy (#141433) at 50 per cent, 4 view
  px wider than the control, drawn on whole view pixels with no anti-aliasing.
- The stick's ring gains a 1-px light outline (#e6e6f2, the UI's border colour) outside its own grey.
- Sizes follow Touch size Auto, so the controls keep about the cover's size on the glass on both screens.
- Drawn by the engine; no image file and no frames.

**Sits beside.** Kenney's touch faces, over Stonehollow's falls, the Eldergrove's trees, bright grass and the fog.

**Check.** The standard check, on both screens, over the four grounds named.

**Made by:** code here, by the engine: two shapes and two colours.

```text
Brief (Code, not an image tool: this backing is drawn in code by the game's engine, open 102): in a Godot 4
pixel-art game, write the GDScript drawing code for a dark backing behind on-screen touch controls (a joystick ring
and round A, B, L and R buttons): a filled circle in navy #141433 at 50 per cent opacity, 4 pixels wider than each
control, drawn on whole pixels with no anti-aliasing; and a 1-pixel light outline (#e6e6f2) round the joystick ring.
These are the UI's own colours, kept as they are. Sizes come from a per-screen setting. No image file and no frames.
File: the code goes in the engine's touch overlay, src/ui/touch_overlay.gd. Deliver the drawing code and pictures of
the controls over bright green grass and over white fog.
```

### 2.21 The fonts' l, k and é, and the new glyphs (item 8)

**What and where.** Open 170: l, k and é redrawn as true lower case in our own copies of both fonts, keeping their size
and spacing. Kenney Mini (menus, 8 px, a 10-px line) and Kenney Pixel (dialogue, 16 px, a 12-px line) draw l and k as
small capitals ("Fauhaven") and é as É ("PokÉmon"). The Chart needs real stars and a visited mark for "*", "**" and
"?" (survey §2.10), and the Pokémon menu a small partner badge for "*" (survey §5).

**Spec.**
- **l:** one stem as tall as each font's own b, d and h. **k:** the same ascender stem, its arms within the font's own
  x-height. **é:** the font's own e with a two-pixel acute in the rows above the x-height. Each keeps the old glyph's
  advance width unless the stem cannot fit; É stays capital.
- **In `ui_glyphs.ttf`,** on Kenney Mini's grid and line metrics: ★ (U+2605) and ☆ (U+2606), each as wide as a digit;
  ✓ (U+2713) for visited; ◉ (U+25C9), a small ringed dot, for the partner badge (the engine draws it in gold).
- **Palette:** none: a font's glyphs carry no colour, and the engine colours each one. No frames.
- **Files:** `assets/fonts/kenney_mini_halcyra.ttf` and `kenney_pixel_halcyra.ttf` (renamed copies; Kenney is CC0),
  and `ui_glyphs.ttf` rebuilt by `tools/make_ui_glyphs.py`. A saved script, `tools/patch_fonts.py` (fontTools), makes
  the copies.

**Sits beside.** Every place banner, the dialogue box, the Start menu's "Pokémon" row, the Chart.

**Check.** The standard check's contact sheet at the game's sizes on both screens: "Fallhaven", "Stonehollow", "blows
bubbles", "Mudkip", "Pokémon" and a row of stars. No tile check (fonts are vectors of pixels).

**Made by:** code here: three glyphs per font on an existing pixel grid, by a saved fontTools script.

```text
Brief (Code, not an image tool: these glyphs are made in code by the game's own font script, tools/patch_fonts.py
with fontTools, open 102): write a Python script with fontTools that edits two pixel fonts (supplied TTFs, Kenney's
CC0 fonts, drawn on a pixel grid). In each, redraw lowercase l as a single-pixel stem as tall as the font's own b, d
and h; lowercase k with the same tall stem and its arms within the height of the font's own x; and é as the font's
own lowercase e with a two-pixel acute accent above it. Keep each glyph's advance width and the font's line metrics
unless a stem cannot fit. Leave every other glyph unchanged. Rename the fonts. Then add to a small glyph font on the
same grid: a filled star (U+2605) and a hollow star (U+2606) as wide as a digit, a tick (U+2713) and a small ringed
dot (U+25C9). Glyphs carry no colour and have no frames. Files: assets/fonts/kenney_mini_halcyra.ttf,
kenney_pixel_halcyra.ttf and ui_glyphs.ttf. Deliver the script as tools/patch_fonts.py, the TTFs, and a picture of
each at its size.
```

### 2.22 The hero on the Surf mount (item 9)

**What and where.** Asset-priorities §1.4: the hero on the Surf mount, today a coloured box. Demo 26 decided the
expansion's surf-blob mount under the rider, and Crew 1's Surf is Marill's gift in Canalport (placeholder Marill).

**Spec.**
- The mount's own sprite frames and facings from the expansion, at the mount's own frame time. The rider is each LPC
  look's sit row, cut at the hips, set so the hips sit 2 px inside the mount's back and moving with the mount's bob.
- 8 facings by art 3's rule (the diagonals on the side rows).
- **Palette:** none new: the two sheets' own colours.
- Composed per look by `compose_lpc.py`, so every Adept and the creator's hero get one. The output is gitignored like
  every LPC output (art 9); only the offsets are ours, `data_src/surf_offsets.json`.

**Sits beside.** Canalport's canals, Marrow cove's sea, the partner follower (hidden while surfing, demo 29).

**Check.** The standard check, with Maren and the hero surfing in all facings.

**Made by:** code here: a composite of two sheets we have, no drawing.

```text
Brief (Code, not an image tool: this composite is made in code by the game's own LPC composer, compose_lpc.py, open
102): write a Python function (Pillow only) that composites a rider onto a swimming mount for a top-down pixel-art
game. Inputs: the mount's sprite sheet (its own facings and a 2-frame bob, at its own frame time) and the rider's LPC
sitting rows (64x64 frames). For each facing, cut the rider at the hips, place the hips 2 pixels inside the mount's
back, and move the rider with the mount's bob. Diagonal facings use the side rows. No new pixels or colours, no
scaling. File: data_src/surf_offsets.json, the offset table as {"<facing>": [x, y]}. Deliver the function, the JSON
and a contact sheet.
```

### 2.23 HP, PP and EXP bars (item 11)

**What and where.** The battle party box and status pane show HP and PP as bare numbers, "*" as a separator and
"EXP -" as a dash (survey §5). The fix: labelled HP and PP bars like Golden Sun's, and a real EXP bar. Mana Soul's
bars, if you approve that download, are the other way.

**Spec.**
- In UI pixels (the UI is at 2×): each bar 40×3 inside a 1-px dark frame (42×5), with "HP" or "PP" in Kenney Mini to
  its left and the numbers kept.
- **HP fill:** green above half, yellow from a half to a quarter, red below, each in two steps (the top row lighter).
  **PP fill:** blue in two steps. **EXP:** a 1-px gold bar under the PP bar, 40 px long. The empty part is the
  frame's dark.
- **Palette:** green `#29944a` with `#7bf731` on top; yellow `#d69410` with `#ffde29`; red `#9c0000` with `#de0000`;
  blue `#1863e7` with `#18adff`; EXP gold `#ffde29`; frame `#101031` (the UI's navy, snapped).
- Drawn by the engine; no image file and no frames.

**Sits beside.** The navy windows, Kenney Mini, the party's LPC battlers.

**Check.** The standard check's contact sheet: the party box at full, half and low HP, on both screens.

**Made by:** code here, by the engine.

```text
Brief (Code, not an image tool: these bars are drawn in code by the game's engine, open 102): write the GDScript
drawing code for HP, PP and EXP bars in a Game Boy Advance-style battle menu (Golden Sun look) in Godot 4, on whole
pixels at the UI's own pixel size: each bar 40x3 pixels inside a 1-pixel dark frame, labelled "HP" or "PP" in the
menu's pixel font with the numbers kept beside it. HP fill green above half, yellow down to a quarter, red below,
each two shades with the lighter on top. PP fill blue, two shades. EXP a 1-pixel gold line under the PP bar. Palette
(15-bit, darker shade first): green #29944a #7bf731, yellow #d69410 #ffde29, red #9c0000 #de0000, blue #1863e7
#18adff, EXP #ffde29, frame #101031. No gradients, no image file, no frames. File: the code goes in the battle
scene's status box, src/battle/battle_scene.gd. Deliver the drawing code and a picture at full, half and low HP.
```

### 2.24 Forest's and Shadow's element badges (item 11)

**What and where.** Every Adept belongs to one of six groups: Earth, Flame, Sea, Sky, Forest and Shadow. The first four
follow Golden Sun's elements, whose symbols come from the ROM; Forest and Shadow have no symbol anywhere. No free
badges in Golden Sun's style exist (art-sources.md §4.11).

**Spec.**
- The same size, outline and shading as Golden Sun's own four element symbols in the export, side by side with them.
  If those are 8×8, draw at 8×8; deliver 16×16 as well.
- **Forest:** a two-leaf sprout on green. **Shadow:** a thin crescent on cold silver-grey (silver, not violet, so
  Shadow never reads as Sky; the opening's colours).
- A round badge, a near-black outline, a three-step ramp lit from the top-left, a light glyph in the middle, unless
  Golden Sun's four take another shape, in which case match theirs.
- **Palette:** Forest `#29944a #52c663 #7bf731`, its sprout `#ceff5a`; Shadow (map sea rock) `#636363 #8494a5
  #b5c6ce`, its crescent `#f7f7f7`; outline `#182121`.
- **Frames:** none.
- **Files:** `assets/own/icons/elements.png` and `elements.json` (keys `forest`, `shadow`).

**Sits beside.** Golden Sun's Venus, Mars, Mercury and Jupiter symbols, the Psynergy menu, the status screen.

**Check.** The standard check, with all six badges in a row on the navy window.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: these badges are drawn in code by the game's own generator, tools/draw_own.py, open
102. Code here only when Golden Sun's four symbols are supplied: they never leave this PC. Sent outside, the brief
goes without them): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, two element
badges for a Game Boy Advance RPG in the style of Golden Sun (2001), to sit in a row with four existing ones (if
supplied, match their size, outline and shading exactly). Without them: round badges, 16x16 and 8x8 pixels, a
near-black outline, a three-step colour ramp lit from the top-left, a light symbol in the middle. Forest: a two-leaf
sprout on green. Shadow: a thin crescent on cold silver-grey (not purple). Palette, dark to light (15-bit; add a
colour only where none fits, and list it): Forest #29944a #52c663 #7bf731, sprout #ceff5a; Shadow #636363 #8494a5
#b5c6ce, crescent #f7f7f7; outline #182121. At most 15 colours plus transparent. Hard pixel edges. Transparent
background. No frames. Files: assets/own/icons/elements.png and elements.json, as {"tile": [16, 16], "columns": 4,
"cells": {"forest": [0, 0, 16, 16], "shadow": [16, 0, 16, 16], "forest_8": [32, 0, 8, 8], "shadow_8": [40, 0, 8,
8]}}. Deliver the script, its recipe as tools/own_art/elements.json, and the PNG and JSON it writes.
```

### 2.25 Field Psynergy shapes (item 11)

**What and where.** Golden Sun's own field casts have no free match: Move's giant hand, Catch, Lift, Growth's vine,
Douse's rain cloud, Frost's ice pillar, Reveal's lens, Whirlwind's leaf spiral, and Pound and Scoop for mission 1's
puzzles. The decision page asks whether to export Golden Sun's own for the demo (recommended), draw them in code, or
use Ninja Adventure and Foozle stand-ins. This section is the drawn way, for any shape the export can't give.

**Spec.**
- **Move, Catch, Lift:** a giant hand, 32×32, 6 frames at 4 ticks (67 ms) (grow from the caster, reach, push or pull
  or lift, hold, fade, gone); rows e, s, w, n (casts snap to 4 facings, art 3).
- **Growth:** a vine climbing 16×48, 6 frames at 5 ticks (83 ms). **Douse:** a cloud of 32×16 with rain below, in a
  32×32 frame, 4 frames at 6 ticks (100 ms). **Frost:** an ice pillar rising from a puddle, 16×32, 5 frames at 5
  ticks (83 ms). **Whirlwind:** a leaf spiral 32×32, 6 frames at 4 ticks (67 ms). **Reveal:** a lens ring widening
  round the caster to 96×96, 8 frames at 4 ticks (67 ms). **Pound:** a falling stone fist 32×32, 5 frames at 5 ticks
  (83 ms). **Scoop:** a digging hand with spraying sand 32×32, 5 frames at 5 ticks (83 ms).
- **Colours:** a Psynergy violet-blue for the hands and the lens at one 50 per cent alpha step, the element's own
  colours for the rest.
- **Palette:** violet-blue (vault stone and map falls) `#314294 #4252ad #637bad #8cb5f7`; vine grass `#29944a #52c663
  #7bf731 #adff52`; cloud `#8494a5 #a5b5bd #b5c6ce` with rain `#42e7ff #9cf7ff`; ice (map falls) `#7bbdde #a5d6de
  #eff7ff`; leaves `#29944a #7bf731 #adff52`; stone fist (map sea rock) `#5a527b #636363 #8494a5 #a5b5bd`; sand (cove
  sand) `#bdb56b #d6c663 #e7d663 #efe763`.
- **Files:** `assets/own/effects/psynergy_field.png` and `psynergy_field.json`.

**Sits beside.** Golden Sun's rooms, the LPC caster, the pushed boulders and pillars.

**Check.** The standard check, with a frame strip of each cast on its puzzle object.

**Made by:** code here, by the generator, if the board chooses drawing; otherwise exported from the ROM and kept
local.

```text
Brief (Code, not an image tool: these effects are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, field-magic effects for a
Game Boy Advance RPG in the style of Golden Sun (2001), top-down, on 16x16-pixel cells. (1) A giant translucent hand,
32x32, 6 frames at 4 ticks (67 ms) (grows from the caster, reaches, pushes, holds, fades, gone), in 4 facings as
rows: east, south, west, north. Violet-blue, drawn as one 50 per cent transparent layer with hard edges. (2) A green
vine climbing, 16x48, 6 frames at 5 ticks (83 ms). (3) A small rain cloud with rain, 32x32, 4 frames at 6 ticks (100
ms). (4) An ice pillar rising from a puddle, 16x32, 5 frames at 5 ticks. (5) A spiral of leaves on the wind, 32x32, 6
frames at 4 ticks. (6) A ring of light widening to 96x96, 8 frames at 4 ticks. (7) A stone fist falling and striking,
32x32, 5 frames at 5 ticks. (8) A hand digging with spraying sand, 32x32, 5 frames at 5 ticks. Light from the
top-left. Palette, dark to light (15-bit; add a colour only where none fits, and list it): hand and ring #314294
#4252ad #637bad #8cb5f7, vine and leaves #29944a #52c663 #7bf731 #adff52, cloud #8494a5 #a5b5bd #b5c6ce, rain #42e7ff
#9cf7ff, ice #7bbdde #a5d6de #eff7ff, stone #5a527b #636363 #8494a5 #a5b5bd, sand #bdb56b #d6c663 #e7d663 #efe763. No
blur, no glow gradients. Transparent background. Files: assets/own/effects/psynergy_field.png and
psynergy_field.json, frames left to right, as {"tile": [16, 16], "columns": 8, "cells": {"move_e_0": [0, 0, 32, 32],
...}, "ticks": {"move": 4, "growth": 5, "douse": 6, "frost": 5, "whirlwind": 4, "reveal": 4, "pound": 5, "scoop":
5}}. Deliver the script, its recipe as tools/own_art/psynergy_field.json, and the PNG and JSON it writes.
```

### 2.26 Herb, Nut and Mint (item 12)

**What and where.** Items 180, 181 and 195 have no icon, so the bag looks half-finished (survey §4.1). Art 14: drawn by
us, in code to Golden Sun's palette. But they are Golden Sun's own items, and its item data gives each its own icon in
the ROM (icons 117, 132 and 144), while open 91 (24 Oct, after art 14) generates art only where Golden Sun has
nothing. The decision page asks which way; this section is the drawn way.

**Spec.**
- Each at 16×16 (the bag's rows) and 32×32 (the detail box), drawn at each size, not scaled.
- **Herb:** three green leaves tied with a tan string. **Nut:** a brown nut with a lit top-left. **Mint:** a sprig of
  pale blue-green leaves with a white highlight.
- A near-black outline, as Golden Sun's item icons have, and a three-step ramp lit from the top-left.
- **Palette:** Herb (grass) `#29944a #52c663 #7bf731`, string (cove sand) `#bdb56b #d6c663`; Nut (cove earth)
  `#633929 #845239 #946339 #ad8c5a`; Mint (canal water) `#18b5ce #39bdbd #6bc6ad`, highlight `#ffffff`; outline
  `#182121`.
- **Frames:** none.
- Ninja Adventure's Nut and TeaLeaf, and Shikashi's herbs, are references only.
- **Files:** `assets/own/icons/items16.png` and `items32.png`, with `items16.json` and `items32.json` (keys `herb`,
  `nut`, `mint`).

**Sits beside.** DCSS's potion and the bag's other icons, the expansion's ball pictures, Kyrise's icons if approved.
On the contact sheet they are also compared with Golden Sun's own Herb, Nut and Mint icons.

**Check.** The standard check, with the bag's Items pocket and the detail box on both screens.

**Made by:** code here, by the generator, if the board keeps art 14's way.

```text
Brief (Code, not an image tool: these icons are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, three item icons for a Game
Boy Advance RPG in the style of Golden Sun (2001), each at 16x16 and at 32x32 pixels (draw each size, do not scale):
a healing herb (three green leaves tied with a tan string), a brown nut, and a sprig of pale blue-green mint with a
white highlight. Near-black outline, a three-step colour ramp lit from the top-left. Palette, dark to light (15-bit;
add a colour only where none fits, and list it): herb #29944a #52c663 #7bf731, string #bdb56b #d6c663, nut #633929
#845239 #946339 #ad8c5a, mint #18b5ce #39bdbd #6bc6ad, highlight #ffffff, outline #182121. At most 15 colours plus
transparent. Hard pixel edges. Transparent background. No frames. Files: assets/own/icons/items16.png and
items32.png, icons left to right in that order, each with a JSON as {"tile": [16, 16], "columns": 3, "cells":
{"herb": [0, 0, 16, 16], "nut": [16, 0, 16, 16], "mint": [32, 0, 16, 16]}}. Deliver the script, its recipe as
tools/own_art/items.json, and the PNGs and JSONs it writes.
```

### 2.27 The capture balls (item 12)

**What and where.** The expansion's Poké Ball has an orange top that reads wrong beside the red potions (survey §4.1),
and art 14 has the balls drawn by us. The demo sells and finds Poké Balls and Great Balls.

**Spec.**
- Each at 16×16 and 32×32, drawn at each size.
- **Poké Ball:** a red top, a white bottom, a black band and a white button. **Great Ball:** a blue top with two red
  marks, a white bottom, the band and button.
- The red in three steps, matched to DCSS's red potion so they read as one red. A near-black outline, lit from the
  top-left.
- **Palette:** red (the red potion) `#9c0000 #bd0000 #de0000`, shine `#ff8484`; blue (the blue potion) `#000084
  #00009c #0000bd`, shine `#a5a5de`; white (the Lemurian rail) `#bdbdb5 #dedece #ffffff`; band and outline `#182121`.
- **Frames:** none.
- **Files:** the same atlases as §2.26 (keys `poke_ball`, `great_ball`).

**Sits beside.** DCSS's red potion, the expansion's other balls.

**Check.** The standard check, with the Balls pocket and the detail box.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: these icons are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, two capture-ball item icons
for a Game Boy Advance RPG, each at 16x16 and at 32x32 pixels (draw each size): (1) a ball with a bright red top
half, a white bottom half, a black band round the middle and a white button; (2) the same with a blue top half
carrying two red marks. Near-black outline, a three-step ramp per colour, lit from the top-left. Palette, dark to
light (15-bit; add a colour only where none fits, and list it): red #9c0000 #bd0000 #de0000, shine #ff8484, blue
#000084 #00009c #0000bd, shine #a5a5de, white #bdbdb5 #dedece #ffffff, band and outline #182121. Hard pixel edges.
Transparent background. No frames. Files: added to assets/own/icons/items16.png and items32.png, with cells
"poke_ball" and "great_ball" in their JSONs ({"tile": [16, 16], "columns": 5, "cells": {"poke_ball": [48, 0, 16, 16],
"great_ball": [64, 0, 16, 16]}}). Deliver the script, its recipe as tools/own_art/balls.json, and the PNGs and JSONs
it writes.
```

### 2.28 One-key Tab and Enter prompts (art approval 6)

**What and where.** Kenney's pixel prompt pack has no one-key Tab or Enter (Tab is two tiles wide, Enter an L shape
two rows tall). Art approval 6: draw our own one-key Tab and Enter in the pack's style when the prompts are wired in.

**Spec.**
- 16×16 each, the same key face, frame and legend colours as Kenney's one-key prompts in `assets/ui/prompts.png`
  (sampled: `#434a5f #707485 #959ab1 #dce1e7 #ffffff`, kept as they are, like the rest of the pack). Tab's legend
  "TAB" in 3×5 letters; Enter's a return arrow.
- **Frames:** none.
- **Files:** `assets/own/ui/prompts_extra.png` and `prompts_extra.json` (cells `key_tab`, `key_enter`).

**Sits beside.** Kenney's keyboard and pad prompts.

**Check.** The standard check's contact sheet beside Kenney's other keys.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: these prompts are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, two keyboard key prompts,
16x16 pixels each, matching a supplied CC0 pixel-art key prompt set (Kenney's) exactly: copy its key shape, frame,
fill and legend colours, which are #434a5f #707485 #959ab1 #dce1e7 #ffffff. A Tab key with "TAB" in 3x5-pixel
capitals, and an Enter key with a return-arrow legend. Hard pixel edges. Transparent background. No frames. Files:
assets/own/ui/prompts_extra.png (32x16) and prompts_extra.json, as {"tile": [16, 16], "columns": 2, "cells":
{"key_tab": [0, 0, 16, 16], "key_enter": [16, 0, 16, 16]}}. Deliver the script, its recipe as
tools/own_art/prompts_extra.json, and the PNG and JSON it writes.
```

### 2.29 The Halcyra logo (item 13)

**What and where.** Decision 25 (you chose the alternative): the title is the logo over a live scene, Stonehollow at
dusk. Today "HALCYRA" is the menu font on flat navy (survey §5). The decision page asks how to make the logo; the
recommended way is drawn in code. Image generators garble lettering (Magic Patterns' own tool says so).

**Spec.**
- "HALCYRA" in capitals, 160×40 UI pixels (320×80 in the picture), hand-placed letters about 20 px tall, not a font.
- A gold ramp of four steps from dark amber to pale gold, lit from the top-left, a 1-px near-black outline, and a 2-px
  drop shadow down and to the right in deep navy, so it reads over Stonehollow's warm dusk sky.
- **Palette:** gold (thatch gold) `#9c5a08 #d69410 #ffde29 #ffff6b`; outline `#182121`; shadow `#101031`.
- **Frames:** none.
- **Files:** `assets/own/ui/logo_halcyra.png`; its recipe in `tools/own_art/logo_halcyra.json`.

**Sits beside.** Stonehollow at dusk, the title menu in Kenney Mini on the navy window.

**Check.** The standard check, over the live scene on both screens.

**Made by:** code here, by the generator, letter by letter, because image tools can't spell.

```text
Brief (Code, not an image tool: this logo is drawn in code by the game's own generator, tools/draw_own.py, open 102):
write a Python script (Pillow only, no image generator, no font) that hand-places, pixel by pixel, a pixel-art game
logo, the word HALCYRA in capitals, 160x40 pixels, in the spirit of Golden Sun's (2001) gold title lettering: letters
about 20 pixels tall with gently flared ends, a four-step gold ramp from dark amber to pale gold lit from the
top-left, a 1-pixel near-black outline and a 2-pixel deep-navy drop shadow down and to the right. It must read over a
warm orange and violet dusk sky. Palette, dark to light (15-bit; add a colour only where none fits, and list it):
gold #9c5a08 #d69410 #ffde29 #ffff6b, outline #182121, shadow #101031. Hard pixel edges, no anti-aliasing.
Transparent background. No frames. File: assets/own/ui/logo_halcyra.png. Deliver the script, its recipe as
tools/own_art/logo_halcyra.json (each letter's pixels), and the PNG it writes.
```

### 2.30 The opening's six stills (item 13)

**What and where.** The opening (docs/story/scripts/opening.md) is six painted stills with a page of narration each,
before the creator: Halcyra from above, the sealing, the Tidewardens, the falling rim, Marrow Isle, Keeping Night.
Decision 23: painted with an image generator, reduced to the game's palette and pixel size, cleaned by hand, each on
a contact sheet first. The end card is a card over black in the scripts (scripts README), so it needs no painting.

**Spec.**
- **Canvas: 376×216 art pixels, shown at 2× (752×432 in the picture),** so one still covers the cover's 746×320 view
  and the inner 480×432 view at whole numbers. Both views show only the centre 240×160 art pixels (x 68 to 308, y 28
  to 188). Keep each focal point inside that, and in the top two-thirds of it (y 28 to 135), since the message box
  covers the bottom third. In the painting's own terms: the middle 64 per cent of the width (18 to 82 per cent from
  the left), and between 13 and 62 per cent of the height from the top. An engine note: `still.gd` today scales a
  480×320 picture to cover the view, not by a whole number on the cover; it must crop instead, and its slow push-in
  becomes a slow pan on whole pixels.
- **One palette across all six,** within the GBA's limits (8×8 blocks, 16 palettes of 16 colours, 5 bits a channel):
  warm for the island and the festival, cooler for the rim. The reduction keeps these anchors from §1.6: the cyan sea
  `#08adf7 #42e7ff`, map deep sea `#1842d6`, grass `#29944a #7bf731`, cove sand `#e7d663`, thatch gold `#ffde29`, map
  sea rock `#8494a5 #b5c6ce`, map falls `#eff7ff`, fire `#f77310`, and the UI navy `#101031` for night.
- **No text.** No faces on still 2's figures. Nothing from later acts (no Farer ships, no Crown, no sky-sailors).
- **Parallax layers** as their own PNGs: still 1's cloud ring, still 4's mist, still 6's lanterns.
- **Frames:** none: stills, panned by the engine.
- **Files:** `assets/own/stills/opening_1.png` to `opening_6.png` (`data_src/stills.json`), layers as
  `opening_1_clouds.png`, `opening_4_mist.png` and `opening_6_lanterns.png`.

**Sits beside.** The navy message box and Kenney Pixel over the bottom third, the creator that follows.

**Check.** The standard check, with each still under its own narration page on both screens, and the six side by side
so the palette reads as one sequence.

**Made by:** an image tool here (Canva's generate-image, or Magic Patterns' generate_image for several at once), then
Proper Pixel Art, tiledpalettequant and a hand clean-up. They are painted pieces (decision 23, open 102). If the tools
here can't hold one look across the six, another model outside this session, with this brief.

```text
Brief (an image tool: these are painted pieces): paint six illustrations for the opening of a fantasy game, then they
will be reduced to Game Boy Advance pixel art at 376x216, so paint with clear shapes, strong silhouettes and simple
light, in the look of Golden Sun (2001): bright, storybook, soft light from the top-left. Wide format (16:9). No text,
no letters, no logos. One palette across all six: warm for the island scenes, cooler for the world's edge. Anchor
colours: bright cyan sea #08adf7 #42e7ff, deep sea #1842d6, grass #29944a #7bf731, sand #e7d663, gold #ffde29, storm
grey #8494a5 #b5c6ce, falls white #eff7ff, fire #f77310, night navy #101031. The game shows only part of each picture.
Keep every named subject inside the middle 64 per cent of the width (18 to 82 per cent from the left) and between 13
and 62 per cent of the height from the top. Leave the outer edges and the bottom third as plain sea, sky or stone.
1. A world seen from high above, tilted like a map, drawn small enough that its rim and all six lights sit inside the
middle band: a green continent with a mountain spine and a tiny white spire on the highest peak, a calm turquoise sea
of islands round it, a ring of grey storm cloud, a darker sea beyond, and at its edge a ring of white water pouring
away into pale nothing. Six faint points of light: amber in the east, red on a volcanic island in the south, blue at
a whirlpool in the south-east, violet at a tower in the clouds in the north, green at a giant tree in the west, cold
silver at black falls on the north-west edge. Morning light.
2. Six robed, hooded figures with no visible faces stand in a ring before six great stone doors, each rimmed with its
light (amber, red, blue, violet, green, silver) narrowing to a thin seam as it closes. Behind each door, just
suggested, the edge of something enormous: a wing, a coil, a ridge of horn. Dark stone, like an old temple carving.
3. A white city climbing a mountain top, its spire in full sun above green terraces. Below, on a broad river, a line
of ships with white-and-blue sails, each marked with a wave beneath a closed ring. In front, a barge carrying braziers
of fire, barrels of rain and sheaves of harvest upriver. Bright, clean, a little too perfect.
4. A cliff town on the world's edge at dusk: half a street hangs over the drop, one house tilts on stilts toward white
mist where the sea pours away. Ropes and chains hold the rest to the rock. Lamplit windows, cold blue-grey elsewhere.
Small loaded boats push off below; far out, a ship with lit sails turns a little boat back.
5. An island of highland lakes, stone terraces and pale quarries in a calm sea at dusk; a stone village on the
terraces; a road climbing north to a dark doorway in the hillside; a beacon tower on the eastern headland; deep under
the hill, the faintest amber glow.
6. The village square at night, strung with paper lanterns, villagers in festival colours dancing round a tall
standing stone, drummers at its foot, a dark road climbing into the hills behind. A small skiff right of centre,
inside that middle band, on black water below the cliffs, its sail furled and no lights, one hooded figure in it.
Deep blue night, warm lantern gold, the skiff nearly black.
Deliver each as a separate image. For 1, 4 and 6, also deliver the cloud ring, the mist and the lanterns as their own
layers on transparency. They become assets/own/stills/opening_1.png to opening_6.png, with opening_1_clouds.png,
opening_4_mist.png and opening_6_lanterns.png. No frames.
```

### 2.31 Stonehollow's blue puddle (item 14)

**What and where.** The small blue oval east of the falls is the Blue puddle, a story clue (it hasn't rained in a
week), but it reads as a stray blob (survey §2.1). The fix: a hard-edged puddle in Golden Sun's style, still startling
blue.

**Spec.**
- 32×16 (2×1 cells): a flat puddle in a blue brighter than any water round it, a 1-px lighter rim on its top-left
  edge, a darker inner edge bottom-right, a 2-frame glint at 60 ticks (1 s).
- **Palette:** the puddle (map shallow sea, bluer than Stonehollow's river `#005a94 #006ba5 #007bb5`) `#1863e7
  #1884f7 #18adff`, rim `#18def7`, glint `#f7f7f7`; the grass it lies on, Stonehollow's `#29944a #52c663 #7bf731
  #adff52`.
- **Files:** `assets/own/tiles/props.png` and `props.json` (cell `blue_puddle`).

**Sits beside.** Stonehollow's Golden Sun grass and path, the falls.

**Check.** The standard check, by day and by night.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: this prop is drawn in code by the game's own generator, tools/draw_own.py, open 102):
write a Python script (Pillow only, no image generator) that draws, pixel by pixel, a puddle for a top-down Game Boy
Advance RPG in the style of Golden Sun (2001), 32x16 pixels, lying on green grass: flat, oval but pixel-stepped, a
startling bright blue (bluer than any water nearby), a 1-pixel lighter rim on its top-left edge, a darker inner edge
at the bottom-right, and a small white glint that shows on frame 2 of 2, at 60 ticks (1 s) a frame. Palette, dark to
light (15-bit; add a colour only where none fits, and list it): puddle #1863e7 #1884f7 #18adff, rim #18def7, glint
#f7f7f7. The grass round it, for the preview only: #29944a #52c663 #7bf731 #adff52. Hard pixel edges. Transparent
background. Files: assets/own/tiles/props.png (64x16, two frames) and props.json, as {"tile": [16, 16], "columns": 4,
"cells": {"blue_puddle_0": [0, 0, 32, 16], "blue_puddle_1": [32, 0, 32, 16]}, "ticks": {"blue_puddle": 60}}. Deliver
the script, its recipe as tools/own_art/blue_puddle.json, and the PNG and JSON it writes.
```

### 2.32 The Wayfarer's engine and chart table (item 14)

**What and where.** On the Wayfarer's deck the helm, the engine, the chart table with the Lodestar and the muster roll
stand; two use stand-in sprites, a bright green lattice and a clock face (survey §2.4). Story.md §8: six glass chambers
round a brass heart, only the Flame chamber alight; a brass cradle cut to the Lodestar's shape, the Farer's Log beside
it.

**Spec.**
- **The engine:** 32×32: a ring of six small glass domes round a brass core, seen from above at a slight front angle;
  the Flame chamber lit orange-red (4 frames at 8 ticks, 133 ms), the other five dark glass with a highlight.
- **The chart table:** 32×32, no frames: a wooden table with a parchment chart, a brass cradle holding the Lodestar (a
  smooth round stone with a faint glow), the Log as a closed book beside it.
- **Palette:** the deck room's own Golden Sun wood: ship deck `#4a3118 #7b4a21 #bd8442 #de9c5a #efc67b` and ship hull
  `#6b4a31 #845a39 #a57342`; brass (thatch gold) `#9c5a08 #d69410 #efbd21 #ffde29`; dark glass (iron) `#182121
  #293131 #31424a`, highlight `#8494a5`; flame (fire) `#843900 #f77310 #ffe763`; parchment (map sand) `#e7de9c
  #efe7ad #fff7de`; Lodestar (map sea rock) `#8494a5 #b5c6ce`, glow `#eff7ff`; the Log (the Lemurian hull) `#6b3939
  #844a42`.
- [LPC] Ship's wheel and hatches are the base for any other deck prop, if you approve that download.
- **Files:** `assets/own/tiles/wayfarer_props.png` and `wayfarer_props.json`.

**Sits beside.** The Wayfarer's Golden Sun deck, the LPC crew.

**Check.** The standard check, by day and by night.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: these props are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, two ship's-deck props for a
top-down Game Boy Advance RPG in the style of Golden Sun (2001), 32x32 pixels each, seen from above at a slight front
angle. (1) An ancient engine: a ring of six small glass domes round a brass core; one dome glows orange-red with a
4-frame flicker at 8 ticks (133 ms), the other five are dark glass with a small highlight. (2) A chart table, no
frames: a wooden table with a parchment chart on it, a brass cradle holding a smooth round stone with a faint glow, a
closed book beside it. Light from the top-left, outlines from each object's own darkest shade. Palette, dark to light
(15-bit; add a colour only where none fits, and list it): wood #4a3118 #7b4a21 #bd8442 #de9c5a #efc67b and #6b4a31
#845a39 #a57342, brass #9c5a08 #d69410 #efbd21 #ffde29, glass #182121 #293131 #31424a, highlight #8494a5, flame
#843900 #f77310 #ffe763, parchment #e7de9c #efe7ad #fff7de, stone #8494a5 #b5c6ce, glow #eff7ff, book #6b3939 #844a42.
At most 15 colours plus transparent per 8x8 block. Hard pixel edges. Transparent background. Files:
assets/own/tiles/wayfarer_props.png and wayfarer_props.json, as {"tile": [32, 32], "columns": 5, "cells":
{"engine_0": [0, 0, 32, 32], ..., "chart_table": [128, 0, 32, 32]}, "ticks": {"engine": 8}}. Deliver the script, its
recipe as tools/own_art/wayfarer_props.json, and the PNG and JSON it writes.
```

### 2.33 Bastion's sea-gate (item 14)

**What and where.** Open 175: keep the docks but add a grey stone fort wall and sea-gate above Bastion's strand, from
Golden Sun's stone tiles. Mission 7 turns on walls too high to climb and soft earth by the sea-gate. The wall comes
from Golden Sun's clips; the gate is ours only if no Golden Sun gate fits.

**Spec.**
- **The sea-gate:** 48×48 (3×3 cells): an arched opening in the wall's own grey stone, a dark iron portcullis grid (two
  steps) let down into the water, closed only (it turns ships away).
- **The soft earth:** a 16×16 mud tile by the gate, darker and wetter than the strand's sand, 3 variants.
- **Palette:** the wall's own stone; until its clip is chosen, vault stone `#314294 #4252ad #637bad #7b94a5 #9cad9c
  #b5c694`; portcullis (iron) `#182121 #31424a`; mud (cove earth) `#633929 #845239 #946339`, its wet shine `#ad8c5a`;
  the water below in the cyan sea.
- **Frames:** none.
- **Files:** `assets/own/tiles/bastion_gate.png` and `bastion_gate.json`.

**Sits beside.** The Golden Sun stone wall, the strand's sand and jetty, the cyan sea.

**Check.** The standard check, with the strand rebuilt so it reads as a fortress.

**Made by:** code here, by the generator, in the wall's own colours.

```text
Brief (Code here only: the supplied wall tiles are Golden Sun's and never leave this PC. Code, not an image tool:
drawn in code by the game's own generator, tools/draw_own.py, open 102): write a Python script (Pillow only, no image
generator) that draws, pixel by pixel, a fortress sea-gate for a top-down Game Boy Advance RPG in the style of Golden
Sun (2001), 48x48 pixels, seen from above at a slight front angle, matching the supplied grey stone wall tiles: an
arched opening in the stone, a dark iron portcullis grid let down into the water, closed. Also three 16x16 tiles of
soft, wet, dark earth to lie beside it on a sandy shore. Light from the top-left. Palette, dark to light (15-bit; add
a colour only where none fits, and list it): stone #314294 #4252ad #637bad #7b94a5 #9cad9c #b5c694 (or the supplied
tiles' own), iron #182121 #31424a, mud #633929 #845239 #946339, shine #ad8c5a, water #089cf7 #10b5ff #42e7ff. At most
15 colours plus transparent per 8x8 block. Hard pixel edges. No frames. Files: assets/own/tiles/bastion_gate.png and
bastion_gate.json, as {"tile": [16, 16], "columns": 6, "cells": {"sea_gate": [0, 0, 48, 48], "mud_0": [48, 0, 16,
16], ...}}. Deliver the script, its recipe as tools/own_art/bastion_gate.json, and the PNG and JSON it writes.
```

### 2.34 The wanted poster (item 14)

**What and where.** Demo 11: wanted posters with terrible portraits on Tidewarden notice boards, from mission 8.

**Spec.**
- **The poster:** a 16×16 prop: a pale paper sheet pinned at the top, a crude face sketch in its top half, a red bar
  and two grey lines for text (nothing readable). It hangs on Golden Sun's notice boards.
- **The close-up,** if a scene shows one: 64×64, a deliberately terrible portrait of the wanted person, lopsided and
  hurried, drawn after the portraits (§3.1).
- **Palette:** paper (map sand) `#e7de9c #efe7ad #fff7de`; pin `#182121`; sketch (map cliff) `#736352`; red bar (the
  red potion) `#bd0000`; text lines (map sea rock) `#8494a5`.
- **Frames:** none.
- **Files:** `assets/own/tiles/props.png` and `props.json` (cell `wanted_poster`).

**Sits beside.** Golden Sun's notice boards and walls.

**Check.** The standard check.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: this prop is drawn in code by the game's own generator, tools/draw_own.py, open 102):
write a Python script (Pillow only, no image generator) that draws, pixel by pixel, a 16x16 pixel-art wanted poster to
hang on a wall in a top-down Game Boy Advance RPG (Golden Sun style): a pale paper sheet pinned at the top, a crude
face sketch in its top half, a red bar and two short grey lines below for text (nothing readable). Light from the
top-left. Palette, dark to light (15-bit; add a colour only where none fits, and list it): paper #e7de9c #efe7ad
#fff7de, pin #182121, sketch #736352, red bar #bd0000, lines #8494a5. Hard pixel edges. Transparent background. No
frames. Files: added to assets/own/tiles/props.png, with the cell "wanted_poster" in props.json ({"tile": [16, 16],
"columns": 4, "cells": {"wanted_poster": [x, y, 16, 16]}}). Deliver the script, its recipe as
tools/own_art/wanted_poster.json, and the PNG and JSON it writes.
```

### 2.35 Warm night: the tint, lit windows and town lamps (item 15)

**What and where.** Open 177: a night tint that keeps sand and wood warm, with lit windows and lamps in the towns drawn
in code. Today one flat blue tint turns sand concrete grey, leaves thatch bright yellow and lights nothing (survey
§2.9). On the world map, beaches and cliffs turn the fog's grey (§2.10); open 98 makes night at sea darker, with
Marrow Isle's beacon and the Pinnacle lit.

**Spec.**
- **The tint:** a 32-level lookup table, one entry per 15-bit level (32 slices of 32×32, a 1024×32 PNG), sampled with
  nearest filtering, so every output stays on the 32 levels and no two shades merge. A script makes it from one rule:
  darker and bluer overall, but hues from about 15° to 60° (sand, wood, thatch, skin) keep their hue and lose half as
  much brightness and colour; land never ends as the fog's grey. A canvas shader applies it to outdoor rooms and the
  world map, never indoors. At sea, a second, darker table.
- **Lit windows:** for every window tile in the town tilesets in use (Stonehollow, Fallhaven, Canalport, the
  Eldergrove, the Bazaar), a matching 16×16 overlay that fills the panes with warm yellow in two steps and spills a
  cell of light below at 25 per cent, shown at dusk and night.
- **Lamps:** Golden Sun's own lamp posts where its town tiles have them. Ours where not: a 16×32 post (dark iron, a 6×6
  glass lantern on top) and the hanging lantern (§2.17). Each lamp's light is a stepped texture (64×64, three hard
  rings) for Godot's PointLight2D, in place of Kenney's smooth light masks.
- **The beacon and the Pinnacle** on the world map: 16×16 glows, 4 frames at 10 ticks (167 ms).
- **Palette:** panes (thatch gold) `#efbd21 #ffef39`, spill `#ffe763`; post (iron) `#182121 #293131 #31424a
  #949c94`, glass (fire) `#ffe763 #ffffad`; rings `#ffe763`; beacons (fire) `#b54a00 #f77310 #ffe763 #ffffad`.
- **Files:** `assets/own/effects/night_lut.png`, `night_sea_lut.png`, `light_rings_64.png`,
  `assets/own/tiles/window_glow_<tileset>.png`, `assets/own/tiles/lamps.png`, `assets/own/world/beacons.png`, each
  sheet with its JSON.

**Sits beside.** Every outdoor room and the world map at night, Pixel-boy's night backdrops.

**Check.** The standard check, with Stonehollow, the fallen west cove, Canalport and the world map at night on both
screens, beside the same places by day.

**Made by:** code here, by the generator: a table, overlays and small sprites.

```text
Brief (Code here only: the supplied window tiles are Golden Sun's and never leave this PC. Code, not an image tool:
drawn in code by the game's own generator, tools/draw_own.py, open 102): write a Python script (Pillow only, no image
generator) that makes a night look for a top-down Game Boy Advance-style game (Golden Sun look, 16x16-pixel tiles).
(1) A colour lookup table with one entry per 15-bit level, 32 slices of 32x32 (a 1024x32 PNG), read with nearest
filtering, that makes everything darker and bluer but keeps warm hues (about 15 to 60 degrees: sand, wood, thatch,
skin) in their own hue, losing only half as much brightness and colour, so sand never turns grey. Every output colour
15-bit (each channel one of 32 levels: 0, 8, 16, 24, 33, 41 ... 247, 255). (2) For each supplied window tile, a
matching 16x16 overlay that fills the panes with warm yellow (#efbd21 #ffef39) and spills light one cell below at 25
per cent opacity (#ffe763). (3) A 16x32 iron lamp post (#182121 #293131 #31424a #949c94) with a small glass lantern
(#ffe763 #ffffad). (4) A 64x64 light texture of three hard-edged rings in #ffe763, for a 2D point light. (5) A 16x16
beacon glow (#b54a00 #f77310 #ffe763 #ffffad), 4 frames at 10 ticks (167 ms). No smooth gradients. Files:
assets/own/effects/night_lut.png, night_sea_lut.png and light_rings_64.png, assets/own/tiles/window_glow_<tileset>.png
and lamps.png, assets/own/world/beacons.png, each sheet with a JSON as {"tile": [16, 16], "columns": 4, "cells":
{"<name>": [x, y, w, h]}, "ticks": {"beacon": 10}}. Deliver the script, its recipe as tools/own_art/night.json, the
PNGs and JSONs it writes, and before-and-after pictures.
```

### 2.36 Exit markers (item 15)

**What and where.** Open 174: keep a marker on doorways that lead out (Brann's cottage, the Bastion jail, the Forge
hall and sanctum, the sea caves), redrawn as hard-edged pixel art in Golden Sun's palette. Today they are smooth
white-gold glows.

**Spec.**
- 16×16, laid on the exit's floor cell: three small chevrons pointing out of the room, pale gold and white with a 1-px
  dark edge, 4 frames at 12 ticks (200 ms) stepping one pixel outward and back.
- **Facings:** rows e, s, w, n (the way out). A two-cell doorway uses two.
- **Palette:** pale gold (thatch gold) `#efbd21 #ffef39 #ffff6b`, white `#ffffff`, edge `#844a18`.
- **Files:** `assets/own/tiles/exit_marker.png` and `exit_marker.json`.

**Sits beside.** Golden Sun's door openings and floors in the six rooms named.

**Check.** The standard check, with each of the six exits on both screens.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: this marker is drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, an exit marker for a
top-down Game Boy Advance RPG in the style of Golden Sun (2001): 16x16 pixels, to lie on a floor tile at a doorway:
three small chevrons pointing out through the door, pale gold and white with a 1-pixel dark edge, in 4 frames at 12
ticks (200 ms) a frame that step one pixel outward and back. Four rows for the four ways out: east, south, west,
north. Palette, dark to light (15-bit; add a colour only where none fits, and list it): edge #844a18, gold #efbd21
#ffef39 #ffff6b, white #ffffff. Hard pixel edges, no glow. Transparent background. Files:
assets/own/tiles/exit_marker.png (64x64) and exit_marker.json, as {"tile": [16, 16], "columns": 4, "cells":
{"exit_e_0": [0, 0, 16, 16], ...}, "ticks": {"exit": 12}}. Deliver the script, its recipe as
tools/own_art/exit_marker.json, and the PNG and JSON it writes.
```

## 3. After the demo

### 3.1 Portraits

**What and where.** Decision 24: a 64×64 portrait with three expressions beside the message box for the 8 Adepts
(Rowan, Corvin, Maren, Tamsin, Sorrel, Vesper, Nerissa, Wynn) and Ilse, Brann, Sael and Hask; the hero's drawn per
body and hair style with colour keys, so the creator's shader recolours them; everyone else a name tag. Also the
battle pane's faces (survey §5) and the wanted posters' close-ups (§2.34). The decision page asks: the LPC portrait
kit as the base, or the image generator (decision 23).

**Spec.**
- 64×64, head and shoulders, three-quarter view facing the text (to the right when the portrait sits left of the
  box). Three expressions: neutral, happy, upset.
- Each person matches their LPC look: hair, colours, clothes, Ilse's bicorne.
- The hero: 2 bodies × 6 hair styles, with skin, hair and eyes each in their own exact colours, so the creator's keys
  (art 5) can recolour them.
- Soft shading lit from the top-left, an outline from each area's darkest shade, not black. Transparent background.
- **Palette:** each person's own LPC sheet colours, snapped to 15-bit after the reduction (Ilse's navy, for one, is
  `#292142 #31296b #394aad #426bc6`). No frames.
- **Files:** `assets/own/portraits/<id>_<neutral|happy|upset>.png`.

**Sits beside.** The navy message box and name tag, the person's LPC sheet.

**Check.** The standard check, with each portrait beside the box on both screens and beside the person's walking
sprite.

**Made by:** per the board. The kit way: Nila122's layered heads, repainted for the top-left light, with the
expressions drawn by hand in code. The generator way: Canva's generate-image with the person's LPC sheet as the
reference, then cleaned; or another model outside this session if the faces drift between expressions.

```text
Brief (an image tool: these are painted pieces): make dialogue portraits for a Game Boy Advance-style RPG, in the soft,
warm look of Golden Sun's (2001) character faces. Each portrait 64x64 pixels, head and shoulders, three-quarter view
facing right, on a transparent background. For each person, three expressions with the same face, hair and clothes:
neutral, happy, upset. Match the supplied sprite sheet for each person (our own LPC sheets) for hair, colours and
clothes, using that sheet's own colours (Ilse's coat, for one, is #292142 #31296b #394aad #426bc6). Soft shading lit
from the top-left, outlines from each area's own darkest shade (never pure black). 15-bit colours only (each channel one
of 32 levels: 0, 8, 16, 24, 33, 41 ... 247, 255), at most 15 colours plus transparent per 8x8 block. Hard pixel edges,
no anti-aliasing. For the player character, keep skin, hair and eyes each in their own exact set of colours, never
shared, so they can be recoloured later. No frames. Deliver one PNG per person per expression, named <id>_neutral.png,
<id>_happy.png and <id>_upset.png, for assets/own/portraits/.
```

### 3.2 The painted Chart

**What and where.** Demo 27 and open 178: the Chart is the terrain grid with Kenney Cartography icons now, a parchment
map painted once later. Open 178 puts the map on the left side at full height.

**Spec.**
- The Calm, Act I's page (the middle 4,096 world px), as a round chart from `docs/design/world-map/world-map.png`
  and the world layout.
- **Two exports from one painting:** 216×216 art pixels for the inner screen and 160×160 for the cover, each shown at
  2× (432 and 320 in the picture), each reduced from the painting on its own, not from each other.
- Parchment browns and a faded sea green-blue, a compass rose, a sea serpent in the Galeway, rhumb lines and an empty
  cartouche. No text: the engine draws names and icons over it.
- **Palette anchors** for the reduction: parchment (map cliff and map sand) `#ad8c73 #c6b594 #e7cea5 #fff7de`; sea
  (canal water) `#39bdbd #6bc6ad`; ink (ship deck) `#4a3118`. No frames.
- Old Parchment Paper (CC0) as the base and Carta Marina as the reference (art-sources.md §5.2).
- **Files:** `assets/own/ui/chart_calm_432.png` and `chart_calm_320.png`.

**Sits beside.** The navy panels, the Kenney Cartography icons.

**Check.** The standard check, on both screens with the details strip open.

**Made by:** an image tool here, with our own world-map picture as the reference, then PixelOE or Proper Pixel Art and
tiledpalettequant.

```text
Brief (an image tool: this is a painted piece): paint an old sea chart on parchment of a round region of sea with
islands (outline supplied, our own map), in the manner of a 16th-century marine chart: brown parchment, faded
green-blue sea, inked coastlines with hatching, a compass rose, thin rhumb lines from it, a sea serpent in a band of
storm round the edge, an empty decorative cartouche. Anchor colours: parchment #ad8c73 #c6b594 #e7cea5 #fff7de, sea
#39bdbd #6bc6ad, ink #4a3118. No text or letters anywhere. Square format. It will be reduced to Game Boy Advance
pixel art at 216x216 and 160x160 (assets/own/ui/chart_calm_432.png and chart_calm_320.png), so keep the shapes bold
and the detail large. No frames. Deliver one square image.
```

### 3.3 The Stillwaters (item 5, seen from Act II)

**What and where.** Calm belts in the Wide where sailing ships sit "till they're bones"; the Wayfarer crosses them on
her Flame engine, and the Leviathan Shoal is the big one (world-map.md §1.5). They lie outside the Calm, in Act II, so
they wait until the Wide is drawn.

**Spec.**
- **16×16 tiles:** flat glassy water, lighter and greener than the open sea, 2 frames at 60 ticks (1 s) (one faint
  sheen line shifting); an edge set against the open sea (4 sides, 4 outer and 4 inner corners).
- **Props:** a bleached derelict hull (32×32) and a broken mast (16×16), no frames.
- **Palette:** glassy water (map shallow sea and foam) `#18def7 #84efe7 #bdeff7`, sheen `#f7f7f7`; the open sea in map
  shallow sea `#1884f7 #18adff #18bdff`; bleached wood (map cliff and sand) `#736352 #ad8c73 #c6b594 #e7cea5 #fff7de`.
- **Files:** `assets/own/world/stillwater.png` and `stillwater.json`.

**Sits beside.** The Lost Age's open sea.

**Check.** The standard check.

**Made by:** code here, by the generator.

```text
Brief (Code, not an image tool: these tiles are drawn in code by the game's own generator, tools/draw_own.py, open
102): write a Python script (Pillow only, no image generator) that draws, pixel by pixel, a becalmed-sea tileset for a
Game Boy Advance world map in the style of Golden Sun: The Lost Age (2002), top-down, 16x16-pixel tiles: flat, glassy
water, lighter and greener than open sea, with 2 slow frames at 60 ticks (1 s) a frame (one faint sheen line
shifting); edge tiles against the open sea (4 sides, 4 outer corners, 4 inner corners); a 32x32 bleached, half-sunk
derelict hull and a 16x16 broken mast, with no frames. Light from the top-left. Palette, dark to light (15-bit; add a
colour only where none fits, and list it): glassy water #18def7 #84efe7 #bdeff7, sheen #f7f7f7, open sea #1884f7
#18adff #18bdff, bleached wood #736352 #ad8c73 #c6b594 #e7cea5 #fff7de. At most 15 colours plus transparent per 8x8
block. Hard pixel edges. Files: assets/own/world/stillwater.png and stillwater.json, as {"tile": [16, 16], "columns":
4, "cells": {"still_0": [0, 0, 16, 16], ...}, "ticks": {"still": 60}}. Deliver the script, its recipe as
tools/own_art/stillwater.json, and the PNG and JSON it writes.
```

### 3.4 Later acts

Each gets a section of its own when its act is built: the Cloudreach's cloud sea, the Deep Shelf's floor, the
Pinnacle's districts, Silverdeep's giant whirl, the broken Galeway's storm fragments, a storm-at-sea battle backdrop, a
ruins backdrop, and the map sprites for Act II's sea monsters (LPC Overworld's creatures, recoloured).

## 4. Not needed for the demo

Nothing found fits these, but nothing in the demo needs them: merchant headwear for the Bazaar (turbans and head-wraps,
none in the generator), children's clothes and rows beyond walk, idle, hurt, jump, sit and slash, crew work animations
(hauling, rowing, swabbing), and marines' extras (a shako, a marine's coat). The townsfolk and marines already have
looks from the generator.
