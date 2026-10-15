# Asset audit, 15 Oct 2026: two CC0 libraries and the LPC generator

Three big uploads to `OneDrive\Apps-Roms` were inventoried and audited before any of it is used. Everything was
read, nothing was run. Mission work paused after mission 9 for this audit, as asked.

- **Inventory tool:** the engine's `tools/inventory_assets.py` (run with `python -I`, pointed at a library). It
  counts every pack's files by kind, reads image sizes from their headers, flags anything that isn't plain media,
  and scores each pack for this game.
- **Full per-pack inventories:** `asset-inventory/` beside this page, one CSV per library plus a shortlist page.
  They hold names, sizes, tags and sources only, no art.

## The art direction this audit uses

**Your decision (15 Oct):** Adept sprites at **64×64** pixels if possible, **32×32** if not, and anything else at
that scale where it can be.

**Proposed consequences, for the graphics pass** (nothing changes in the engine yet):
- **Tiles at 32 px.** 64-pixel characters usually stand on 32-pixel tiles; that is LPC's own pairing.
- **A bigger internal picture.** About 480×320 instead of the GBA's 240×160, so the field still shows about 15 by 10
  tiles. The Fold 7's screen has room to spare.
- **Golden Sun rooms** (16-pixel tiles) would show at double size until their areas are redrawn.

## Your question: could Adepts go to 128 pixels?

**Recommendation: draw them at 64 and show them bigger where you want, rather than drawing at 128.**

1. **LPC is drawn at 64.** There is no 128 version. At 128 it would be the same pixels doubled, with no more
   detail.
2. **Everything an Adept stands next to is 64.** The Pokémon pictures we export (1,329 species) are 64×64, as on the
   GBA, and Golden Sun's battle sheets mostly use 64-pixel frames. Adepts drawn at 128 would sit beside partners with half the detail, a mix of
   pixel sizes that looks wrong. Matching them would mean redrawing every Pokémon.
3. **The libraries stop at about 64.** Almost nothing at 128 fits the style.
4. **Art cost is the real price.** A 128 frame has four times the pixels to draw and animate, whether by hand or
   with an image model, and every Adept needs walk, cast, attack and hurt frames in four directions. Memory and APK
   size are not a problem on the Fold 7.
5. **Size on screen is free.** The engine can show any sprite at a whole-number scale, so a 64-pixel Adept can be
   128 or 256 phone pixels tall in battle without new art.

**Where 128 and up does pay:** dialogue portraits, Summons, bosses and legendaries, and title art. Those are
drawn once, not animated in four directions. Keeping each sheet's frame size as data, not a constant, lets any
sprite move up later without harm.

## What's on disk

| Library | Packs | Content | Licence | Not plain media (read only, never run) |
|---|---|---|---|---|
| `2d-assets-main` (1.6 GB) | 1,101; 194 hold no media | 53,751 images, 57 font files, **no audio** | CC0, every pack | 6 RAR archives of 3D textures, 4 Kenney HTML overview pages, 3 GDScript files and 1 Construct file in sample projects, 1 C++ file, 2 Flash sources |
| `CC0-Public-Domain-Sprites-main` (229 MB) | 76 | about 19,300 images, no fonts, no audio | CC0, every pack | 4 Node scripts that fetch packs (§9 of the folder audit) |
| `Universal-LPC-Spritesheet-Character-Generator-master` | 21 layer groups | 88,114 layer sheets (it finished syncing after §9 of the folder audit, which saw 4,300) | mixed: OGA-BY, GPL, CC-BY-SA, CC-BY; 1,011 of 13,915 credit rows are CC0 | the web app (not run); `AGENTS.md`, `CLAUDE.md` and skill folders addressed to AI agents, treated as data |

The 194 empty packs in `2d-assets` are mostly sound packs whose audio was stripped, so neither CC0 library helps
the music pass. Of its 1,101 packs, 529 are sci-fi and few fit a fantasy RPG.

## Picks by use, at the new scale

| Use | Pick | Why, and what to watch |
|---|---|---|
| **Adept field and battle sprites** | **LPC** | 64×64 frames with walk, idle, run, spellcast (Psynergy), slash, thrust, shoot, hurt, climb (vines), jump, sit and emote, in four directions. Body types (male, female, teen, child, muscular, plus elderly heads) and layered hair, eyes, clothes and gear, recoloured by palette: the layered, palette-swap plan `character-creator.md` already has for the graphics pass. The side-facing rows give battle poses. **Four directions only:** Golden Sun and the creator plan use eight, so diagonals would show the nearest side view or need drawing. Use it through our own composer reading its `sheet_definitions` JSON; their web app isn't needed. Most layers need their authors credited (`CREDITS.csv` lists them per file) |
| **Dialogue font** | **Kenney Pixel** (`2d-assets/ui/kenney-fonts`) | Has lower case and reads cleanly at 16 px. It can replace Kenney Mini Square, which is capitals only |
| **Item icons** | **Dungeon Crawl: Items & Equipment** (CC0 sprites, 646 at 32×32) | Detailed, outlined, at the tile size |
| **Battle backgrounds** | **Pixel-boy's RPG Battle System** (CC0 sprites, 24 scenes, 7 with night versions) | Clean painted scenes for areas Golden Sun has no backdrop for |
| **Battle effects** | Pixel-boy's effect sheets; para's particle bursts (128-px frames); ztn's fire and spell sheets; DevWizard's projectiles; the explosion sheets | Pokémon moves have no Golden Sun animation, so these fill a real gap |
| **Emotes** | **Kenney Emotes** (32×38) | Too big beside Golden Sun's sprites; the right size beside 64-pixel ones |
| **Menus and windows** | Kenney UI Pack (Pixel Adventure), Kenney Fantasy UI Borders, "RPG Frames" window borders, Kenney Input Prompts | 9-slice frames and buttons for the UI pass |
| **Tiles at 32 px** | Weak. The closest are Dungeon Crawl: Environments (32 px) and Kenney's Pirate Pack (64 px, ships and water) | LPC's own tilesets (CC-BY-SA, OpenGameArt) are the natural partner for LPC characters, but they aren't on disk. Downloading them needs your go-ahead |
| **Monsters** | Keep Golden Sun's and Pokémon's | Pixel-boy's battle monsters are a chunky cartoon style that clashes with LPC; Dungeon Crawl's are 32 px |
| **Portraits** | Gap | Ninja Adventure's face sets are chunky 38-px art. Portraits are where 128-pixel art pays; plan to draw or generate them |
| **Music and sound** | Gap | No audio in any of the three. §8 of the folder audit names CC0 music packs, which need downloading |

**Not useful here:** the sci-fi packs, platformer kits, vehicles, 3D models, isometric and hex tiles, and the
sketch styles.

## Next, when you say so

- **Mission 10** resumes.
- **Small and cheap now, if wanted:** swap the dialogue font to Kenney Pixel.
- **For the graphics pass:**
  - an LPC composer tool (layers, palettes and credits into one sheet per Adept);
  - the 480×320 picture with 32-pixel tiles;
  - icons, battle backgrounds, effects and emotes from the picks above;
  - portraits at 128 and up.
