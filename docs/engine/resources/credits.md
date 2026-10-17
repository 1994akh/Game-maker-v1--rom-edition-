# Credits tracking

**Your rule (16 Oct):** the local folder's materials may be used with or without licence terms, with your approval
per item where needed, and every maker is tracked so the end-credits scroll can name them. This page is that record.
The in-game Credits screen (menus-and-navigation.md §10) reads a committed `data_src/credits.json` built from it.
"Status" says whether a source is in the game yet.

| Source | Maker | Terms | What we use or plan to use | Credit line | Status |
|---|---|---|---|---|---|
| Golden Sun and Golden Sun: The Lost Age | Camelot Software Planning; Nintendo | Personal use of your own copies; content never enters git | Maps, field and battle sprites, text, tables, formulas; music and effects planned | "Golden Sun and Golden Sun: The Lost Age by Camelot Software Planning, published by Nintendo" | In the game |
| Pokémon Unbound | Skeli and the Unbound team | Personal use; content never enters git | The game's base and references; catching formula | "Pokémon Unbound by Skeli and team" | Referenced |
| pokeemerald-expansion | RHH (Rom Hacking Hideout) and contributors | Open source (see its licence file) | Species, learnset, move and evolution data; Pokémon pictures; item icons, ball art, menu icons and overworld sprites planned | "pokeemerald-expansion by the Rom Hacking Hideout" | In the game |
| Pokémon | Nintendo, Creatures Inc., GAME FREAK | Personal use | Pokémon names, pictures and data through the above | "Pokémon © Nintendo, Creatures Inc., GAME FREAK inc." | In the game |
| Kenney fonts, input prompts, UI packs, emotes, cartography, cursor pack, pirate pack | Kenney (kenney.nl) | CC0 | Kenney Mini Square (in), Kenney Pixel and Mini (planned), prompts, frames, icons | "Art by Kenney (kenney.nl)" | Font in the game |
| Dungeon Crawl Stone Soup tiles | The DCSS contributors | CC0 | Item icons; dungeon tiles for a prototype | "Dungeon Crawl Stone Soup tiles" | Planned |
| RPG Battle System, Ninja Adventure | Pixel-boy and AAA | CC0 | Battle backgrounds and effect sheets | "Pixel-boy (Sanctumpixel)" | Planned |
| Pixel art spells | DevWizard | CC0 | Projectiles, the shield, status sparkles | "DevWizard" | Planned |
| CC0 explosions and fire | (per pack.json) | CC0 | Blast and Summon impacts | per pack | Planned |
| RPG Frames window borders; 16×16 RPG items; treasure chests | OpenGameArt authors (per 2d-assets pack notes) | CC0 | Window frames, icon gap-fillers, chest props | per pack | Planned |
| Universal LPC Spritesheet Character Generator | Many authors; `CREDITS.csv` lists each layer | OGA-BY, CC-BY-SA, CC-BY, GPL, CC0 per layer; 3,263 layers uncredited | Adept, hero, rival and townsfolk sprites, the hero kit (art decision 3, to talk over) | One line per author used, generated from CREDITS.csv by the composer | Pending the decision |
| LPC base tilesets | OpenGameArt authors | CC-BY-SA | 32-px tiles (art decision 8, to talk over; needs a download with your go-ahead) | per author | Not on disk |
| Ultimate Hentai SFX Pack Free | Kentaro | Credit Kentaro; commercial and non-commercial use; don't resell; editing allowed | Adult-mode sounds | "Sound effects by Kentaro" | Approved 16 Oct, planned |
| Character animation sets (`animations`, `pixelated animations`) | Unknown: no terms file in the folder | None found | Adult-mode sprite base (needed-assets decision 2) | To find out; "Character animations: [maker]" | Approved 16 Oct, pending the decision |
| miniNSFWAssets | Unknown: no terms file | None found | Adult-mode small sprites, redrawn at 64 | To find out | Approved 16 Oct, pending |
| Character and Scene Cards | Unknown; the cards may name their authors in embedded data | None found | Portrait references | To find out | Approved 16 Oct, reference only |
| Pokemon Naughty Version 0.2.2 | Its author(s), unnamed in the folder listing; built on Pokémon Essentials (Maruno and contributors) and RPG Maker XP assets (Enterbrain) | None found | Tilesets, overworld sprites, battle animations, audio as candidates (needed-assets decisions 1 and 3) | "Pokémon Essentials by Maruno and contributors" plus the game's author once known | Approved 16 Oct, candidates |
| Godot Engine | Juan Linietsky, Ariel Manzur and contributors | MIT | The engine | "Made with Godot Engine" | In the game |
| GUT (Godot Unit Test) | bitwes | MIT | Tests (not shipped once art decision 16 is taken) | "GUT by bitwes" | Dev only |
| YATI (Tiled importer) | Roland Helmerichs | MIT | Map import | "YATI by Roland Helmerichs" | In the game |
| Tiled | Thorbjørn Lindeijer and contributors | GPL (the editor; maps are ours) | Map authoring | "Maps made with Tiled" | Dev only |

**Rules of the record:** a row is added before an asset enters the engine, and a row's status moves to "In the game"
in the same PR that uses it. "To find out" credit lines are chased before the credits scroll is built. Nothing from
the first five rows, or from the adult-mode uploads, enters git.
