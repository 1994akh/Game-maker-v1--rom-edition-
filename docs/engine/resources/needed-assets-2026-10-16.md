# Needed assets, 16 Oct 2026

What the game still needs to look and sound finished, after your art answers of 16 Oct (the decision page). For
each need: what we have, where it stands, and how we get it. Everything here is personal-use content; nothing taken
from the ROMs or the local pokeemerald-expansion checkout goes into git (`assets/gs`, `assets/pokemon`,
`assets/music` and `data/` stay gitignored).

## 1. What is on disk today

| Source | What | Where |
|---|---|---|
| Golden Sun 1 (ROM, exported) | 369 field-sprite sheets, 312 map files, the battle sheets (enemies and party), the text bank | `assets/gs/gs1/`, `data/` |
| Golden Sun 2 (ROM, exported) | 1,635 files: maps, field and battle sprites, nothing used yet | `assets/gs/gs2/` |
| Pokémon (expansion, exported) | 1,329 species' 64×64 pictures, front and back | `assets/pokemon/sprites/` |
| pokeemerald-expansion checkout (not exported yet) | 619 item icons, ball sprites, every species' 32×32 menu icon and overworld (follower) sprite, the battle-animation sheets, battle backgrounds, the evolution scene, field effects | `UnboundHack/external/pokeemerald-expansion/graphics/` |
| CC0 libraries (OneDrive) | 2d-assets (fonts, UI, 53k images), CC0-Public-Domain-Sprites (76 packs) | `OneDrive/Apps-Roms/` |
| LPC generator (OneDrive) | 88,114 layer sheets, mixed licences, each layer credited in `CREDITS.csv` | `OneDrive/Apps-Roms/Universal-LPC-...` |
| Our own | 17 rooms' maps and events, one UI font plus the ▶▼ glyph font | `assets/own/`, `assets/fonts/` |
| 16 Oct uploads (OneDrive, not yet used) | Two character animation sets (1,000 frames each, one pixel-art), a small adult sprite set, 26 character and scene cards, an RPG Maker Pokémon fan game (18,655 images, 1,836 sounds and tracks) and an 11-sound adult SFX pack. Inventory: [local-folder-audit-2026-10-16.md](local-folder-audit-2026-10-16.md) | `OneDrive/Apps-Roms/` |
| Audio | **No audio code.** The first sound files arrived on 16 Oct (the SFX pack and the fan game's tracks); nothing plays them yet | — |

## 2. Ready to wire: on disk, decided, no decision pending

| Need | Pick (your answer) | Source | Next step |
|---|---|---|---|
| Message-box and narration font | Kenney Pixel 16 (art 6) | 2d-assets, CC0 | Copy into `assets/fonts`, antialiasing off; UiStyle switches it; boxes hold 3 lines |
| Menu font with lower case | Kenney Mini 8 (art 6) | 2d-assets, CC0 | Same copy; same 10-px line as today, so no layout change |
| Item icons | DCSS 32×32 mapped per item (art 14) | CC0 sprites | `data_src/item_icons.json`, one atlas; the side panel at 240, rows at 480 |
| Icons DCSS lacks (Herb, Nut, Mint, the balls) | "Drawn" (art 14) | The expansion's `graphics/items/icons` (619) and `graphics/balls` cover the Pokémon-side items at 24 px; the Golden Sun ones need drawing or the ROM's icon sheet (not exported) | Export the expansion icons; draw or export the 5 Golden Sun ones |
| Battle backgrounds | Pixel-boy's 12 day/night scenes (art 11) | CC0 sprites | `battle_backdrops.json`; needs the 480 picture (art 1) to fit |
| Button prompts | Kenney input-prompts-pixel (art 14) | 2d-assets, CC0 | `prompt_glyphs.gd`; touch faces and menu footers |
| Window frames | RPG Frames `fantasy_tiny` recoloured navy (art 14) | 2d-assets, CC0 | UiStyle 9-slice styles |
| Emotes | Golden Sun's sprite 21 (art 14) | ROM, **not exported yet** | Run `export_gs_sprites.py` for id 21; the emote step then plays it with no code change. Kenney's pixel emotes for extra kinds |
| Chart icons | Kenney Cartography (menus 18/19) | 2d-assets, CC0 | The sea Chart's first look; a painted chart comes in the art pass |
| Cursor and chests at 2× | Kenney cursor pack; OGA chests | 2d-assets, CC0 | After the 480 switch |
| Tamsin's field look | Golden Sun sprite 3 now (art 15) | exported | One cast.json entry |

## 3. Waiting on a talk item

| Need | What it waits on | What we have | If the answer is no |
|---|---|---|---|
| Adept, hero and rival sprites at 64 px (field and battle) | **art 3** (adopt LPC), **art 4** (the boy's body), **art 17** (eye credits) | LPC layers on disk; the composer tool half-written (the "lpc-composer wip" stash); recipes for the 8 Adepts drafted | Keep Golden Sun's sprites at 2× for now, or draw/generate our own (the Aseprite AI tool needs an NVIDIA GPU this PC lacks) |
| 18 townsfolk looks | art 3 | LPC child, elderly and adult bodies | Golden Sun's townsfolk at 2× |
| Hero creator kit (you accepted art 5: 108 key-coloured sheets plus a palette shader) | art 3 | LPC hair, outfits, accessories, palettes | art 5 needs a different kit source |
| Weapons shown in battle | **equip 13** | Golden Sun's own weapon overlays (exported); LPC weapon layers later | Nothing shows |
| 32-px tiles | **art 8** | Only DCSS dungeon tiles (flat top-down, prototype only). The LPC base tilesets are on OpenGameArt, CC-BY-SA, **not on disk: a download needs your go-ahead** | Golden Sun's tiles stay at 2× |
| Move and Psynergy effects | **art 12** | Hard-edged CC0 sheets (Pixel-boy fx, DevWizard spells, explosions) on disk; the expansion's `battle_anims` (the Pokémon moves' own effect sheets, 16-bit style); Golden Sun's Psynergy effects (ROM, not decoded) | Pokémon moves keep playing with no effect, as today |
| A smaller APK | **art 16** | — | 52.9 MB stays (it was 62.7) |

## 4. Gaps with no pick yet

| Need | Status | Best route |
|---|---|---|
| **Music and sound** | No code; the 16 Oct uploads brought the first files | Three routes, all personal-use: extract Golden Sun's and Unbound's tracks from the ROMs (the m4a tools in the tmc port, rendered to OGG offline); use the fan game's 1,836 OGG tracks and sounds; or download CC0 packs (Not Jam, alkakrab; a download needs your go-ahead). Decision 1 below, then an audio pass |
| The Kestrel, the Wayfarer, Surf | Coloured boxes in the engine | Draw at 64/128 px (one ship each, four facings) or adapt Kenney's pirate pack (64 and 128 px, smooth style, weak fit) |
| Halcyra's world map | Golden Sun's Angara map at 2× stands in; Stonehollow's west gate opens onto it (progression 4, talk) | Draw it, or build it from tiles once the tile source is decided |
| The sea Chart's painted look | Icons only (§2) | The art pass |
| Dialogue portraits | None in any library at the right style. Golden Sun has none; Unbound's trainer mugshots are 64 px | Draw or generate at 128+, the one place higher resolution pays |
| Summon, boss and title art | Golden Sun's Summon sprites are in the ROM (not exported); the title is a text label | Export Golden Sun's Summons; draw the title |
| Pokémon in menus | Text only today | Export the expansion's 32×32 menu icons (`graphics/pokemon/<species>/icon.png`), one afternoon of tooling |
| Pokémon field followers | No code and no decision | The expansion's `overworld.png` per species exists; followers need their own feature decision first |
| Golden Sun item icons | Every item row has an icon index; no sheet exported | Export the ROM's icon sheet as an alternative to DCSS, or only the 5 gaps |
| Evolution screen art | A dialogue page today (progression 14 accepted: a "Which way?" choice) | The expansion's `evolution_scene` graphics if a screen is wanted |

## 5. Licences and credits

- CC0 picks are committed (art 9) with their credits in `data_src/credits.json`; a Credits screen is on the menus
  page's list of screens still to specify.
- LPC output is gitignored and rebuilt from committed recipes; every layer needs its author credited, and 3,263 LPC
  files carry no credit (the adult eyes among them), which is art 17.
- Golden Sun, Unbound and expansion content never enters git.

**Your rule (17 Oct):** anything in the local folder may be used where it is better for the story or in quality, with your per-item approval and every maker tracked for the credits scroll.

## 6. Suggested order, once the talk items are settled

1. Fonts, icons, prompts, frames and emotes: all on disk, all decided, no picture change needed.
2. Export the expansion's Pokémon menu icons and ball art; export Golden Sun's sprite 21 and Summons.
3. The LPC composer and the 8 Adepts, if art 3 is a yes, then the hero kit.
4. The 480×320 switch (art 1), then backgrounds, battle scales and effects.
5. Tiles and area redraws, area by area.
6. An audio pass, after its decision.

## 7. Decisions for you

Answered on the decision page: accepted items are marked **Decided** with the date, the rest **To talk over**.

Recommended first. The alternatives are in brackets.
1. **Decided (17 Oct):** **Music and sound route.** Recommended: Golden Sun's and Unbound's own tracks and sounds, extracted from the ROMs
   and rendered to OGG offline, with the fan game's library as the fallback where a track is missing; the SFX pack
   you added for the adult-mode sounds. [The fan game's audio as the main source; CC0 downloads only.]
2. **Decided (17 Oct):** **The 16 Oct animation sets as the adult-mode sprite base.** They are a full character (idle, walk, crawl, combat,
   expressions, adult clips) at one size, in a pixel version and a smooth one. Recommended: adopt the pixel version,
   resampled to the 64×64 standard, for the adult-mode variant sprites and scenes. [Use them only as pop-up art;
   don't use them.]
3. **Decided (17 Oct):** **The fan game's 32-px tiles as the tile source.** The RPG Maker game carries 32×32 Pokémon-style tilesets and
   autotiles, the size the art plan wants and nothing else on disk has. Recommended: evaluate them beside the LPC
   base tilesets (art decision 8) in the Phase 2 tile spike. [Ignore them; LPC tiles only.]
4. **Decided (17 Oct):** **Pokémon menu icons and ball art from the expansion.** Recommended: export the 32×32 menu icons and the ball
   sprites now, for the Pokémon screens and the item icons. [Text-only menus until the art pass.]
