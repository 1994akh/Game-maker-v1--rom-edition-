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
| Kenney fonts, input prompts, UI packs, emotes, cartography, cursor pack, pirate pack | Kenney (kenney.nl) | CC0 | Kenney Mini Square (in); Kenney Mini and Pixel in as our edited copies Halcyra Mini and Halcyra Pixel (true lowercase l, k and accents, engine PR #105); prompts, frames, icons | "Art by Kenney (kenney.nl)" | Font in the game |
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
| The DS-style 64x64 Pokémon Sprite Resource (uploaded 19 Oct) | Its contributors (no credits file in the pack) | None found | A backup for any species whose expansion battle sprite is missing or broken (open question 51, decided 24 Oct); 722 Gen I-V fronts and backs, copied as they are into the engine's gitignored assets/third_party/ds64 | "DS-style 64x64 Pokémon Sprite Resource contributors" | Approved 24 Oct, backup |
| One Piece (GBA, 2005) sprite rips (uploaded 24 Oct) | Ripped by Paddy and by Lemon for The Spriters Resource | None stated ("No credit needed" on Paddy's sheets) | A parts bin (open question 52, decided 24 Oct): the plain pirates and Navy guards, recoloured, as Act II bandit battlers; the Collections icons for the eggs; the crew and villains as reference for the spoofs' own looks | "One Piece GBA sprites ripped by Paddy and Lemon (The Spriters Resource)" | Approved 24 Oct, parts bin |
| Pokemon Naughty Version 0.2.2 | Its author(s), unnamed in the folder listing; built on Pokémon Essentials (Maruno and contributors) and RPG Maker XP assets (Enterbrain) | None found | Tilesets, overworld sprites, battle animations, audio as candidates (needed-assets decisions 1 and 3) | "Pokémon Essentials by Maruno and contributors" plus the game's author once known | Approved 16 Oct; its non-adult parts copied in as they are, 20 Oct (adult 46 and 57: engine PR #74, people and title art left out), each credited as it comes into use |
| agbplay | ipatix and contributors (github.com/ipatix/agbplay), nightly 2026-09-24 | LGPL-3.0 | Dev tool, never shipped: renders Golden Sun's room music and sound effects from your own ROM into the gitignored assets (engine PRs #80, #97) | "Music and sounds rendered with agbplay by ipatix" | Dev only |
| Godot Engine | Juan Linietsky, Ariel Manzur and contributors | MIT | The engine | "Made with Godot Engine" | In the game |
| GUT (Godot Unit Test) | bitwes | MIT | Tests (not shipped once art decision 16 is taken) | "GUT by bitwes" | Dev only |
| YATI (Tiled importer) | Roland Helmerichs | MIT | Map import | "YATI by Roland Helmerichs" | In the game |
| Tiled | Thorbjørn Lindeijer and contributors | GPL (the editor; maps are ours) | Map authoring | "Maps made with Tiled" | Dev only |
| Golden Sun: The Lost Age Editor, source (uploaded 30 Oct) | Josh "Atrius" VH (goldensunhacking.net) | GNU GPL | Reference only, never run: its data handler and scripting notes document the ROMs' compression, text and event-script opcodes, read to confirm our own extraction | "Format notes with thanks to Atrius's Golden Sun: The Lost Age Editor" | Reference, 30 Oct |
| Game Tools Collection, source (uploaded 30 Oct) | RyudoSynbios (game-tools-collection.com) | MIT | Reference only, never run: its Golden Sun ROM and save editor templates list the stat, experience, enemy-group, item and save tables with their pointers, a cross-check for our tables and the balance slice | "Table offsets cross-checked against RyudoSynbios's Game Tools Collection" | Reference, 30 Oct |
| Golden Sun decompilation, source (cloned 31 Oct with your approval) | Coaltergeist and contributors (github.com/Coaltergeist/goldensun-decomp), on gsret's disassembly | None stated | Reference only, never built or run: the matched C and the room scripts under src/maps, read beside Ghidra on our ROM (the same addresses) for timing constants, engine primitives and puzzle logic | "Golden Sun mechanics read with thanks to the goldensun-decomp project" | Reference, 31 Oct |

**Rules of the record:** a row is added before an asset enters the engine, and a row's status moves to "In the game"
in the same PR that uses it. "To find out" credit lines are chased before the credits scroll is built. Nothing from
the first five rows, or from the adult-mode uploads, enters git.
