**GBA decomps and ports that would cut engine work for the Golden Sun + Pokémon Android app**

## Headline: a Golden Sun decomp now exists

DESIGN.md says "No Golden Sun decomp found." That is now out of date and should be corrected. Two matching GS decomps are public:

- **PascalPixel/alchemy** covers both games. The Broken Seal (GS1) is about 90% rebuilt as matching C (7,429,580 of 8,238,924 executable bytes on 2026-10-05; decomp.dev shows 89.93%). The Lost Age (GS2) is about 4.7% (559,084 of 11,873,412). VERIFIED from its `progress/history.tsv` and decomp.dev.
  - GS1 C file counts: BATTLE 174, FIELD 281, MENU 101, SYSTEM 35. VERIFIED from the GitHub tree.
  - The headers include `PSYNERGY_MENU.H`, `DJINN_MENU.H`, `BATTLE_FORMATION.H`, `SAVE_STATE.H`, `TILEACT.C` and `FIELD/COMMON/{OBJECT,SCRIPT,EVENT,CAMERA}`. VERIFIED.
  - The C is readable, with named structs. Many files are still generic (`BATTLE4.C`, `OBJECT10.C`). VERIFIED.
- **Coaltergeist/goldensun-decomp** covers GS1 USA only, at 27.65% on decomp.dev. Its modules are field_engine, field, ui, battle and battle_anim. It also confirms GS1 uses the m4a sound engine. VERIFIED.

## Engine need → best GBA source

| Need | Source | What we'd take |
|---|---|---|
| Free 8-way movement, collision, heights | **zeldaret/tmc**, plus the GS1 field code in alchemy | tmc stores position as Q16.16 fixed point, with a 32-step direction byte (8 named directions). `LinearMoveUpdate` moves by sine table × speed. `movement.c` has one routine per direction plus radius-based tile-collision functions. `collisionLayer` handles heights. VERIFIED in `include/entity.h`, `src/physics.c`, `src/movement.c`. GS1's object/motion and camera code gives GS's own feel (reference). |
| Pushable and puzzle objects | tmc `src/object/` (192 files) and GS1 map code | tmc: pushableRock, pushableStatue, pressurePlate, button, bigIceBlock, frozenFlower, beanstalk, trapdoor. VERIFIED. GS1: `KOROSSEO_KABE/PUSH_AHEAD.C`, `KOROSSEO_MARUTA/PUSH.C` (Colosso pushing and logs). VERIFIED by name; contents not read. |
| Field Psynergy that changes the map | alchemy GS1 | `FIELD/COMMON/EFFECT`, `TILEACT.C` (tile actions, Psynergy Stone, chests) and per-dungeon puzzle code. VERIFIED. Psynergy that first appears in The Lost Age (Hover, Scoop, Cyclone, Parch, Burst, Teleport) isn't usable yet, because GS2 is about 5% done. INFERRED for which Psynergy belongs to which game. |
| NPCs, scripts, cutscenes, dialogue | alchemy GS1 script/event code; tmc `script.c`, `cutscene.c`, `cutsceneOrchestrator.c` | Reference. We already have pokeemerald-expansion's script engine. |
| Menus | alchemy GS1 (Psynergy, Djinn, equipment, item, shop and inn menu headers) | Reference for the Set/Standby screen (GS's Djinn menu) and the Psynergy menu. |
| Battle, 4+4 vs about 6 | alchemy GS1 battle code | Turn flow, Djinn release, Summon casting, action resolution. **This also settles our open enemy-cap to-do:** `BATTLE_WORK.H` has `enemy_classes[6]`, `sprite_slots[6]`, `enemy_units[7]` (6 plus a terminator) and `actions[20]`; `BattleFormationRecord` has 5 member ids with min/max counts. VERIFIED fields; that this means a 6-slot cap is INFERRED. We can also check our `gs_battle.py` against the real C. |
| Catching, storage, evolution | expansion (already have); **pret/pmd-red** | pmd-red `dungeon_mon_recruit.c`: a Pokémon that joins after battle, which fits our Djinn-style "battle first" encounters. VERIFIED file. |
| Partner Auto tactics | pmd-red `dungeon_ai_leader.c`, `dungeon_ai_movement.c`, `dungeon_ai_attack.c`, `dungeon_ai_item_weight.c` | Reference for ally AI. VERIFIED files. |
| World map, ship, Surf/Dive/Waterfall | expansion for Surf/Dive/Waterfall (already have) | No usable ship or sailing source: TLA is about 5% decompiled. |
| Save | alchemy `SYSTEM/SAVE`, tmc `save.c`, Picori `port_save.c` | Reference only. Our two-crew save format is new. |
| Music and SFX | Picori `port_m4a_backend` + agbplay; sa2 `shared/audio` | GS1 uses m4a (VERIFIED), so the original GS sequences could probably play natively without the MIDI/SF2 conversion (INFERRED). |
| Touch and controller on Android | **999sian/tmc (Project Picori)** | SDL3, `android/` Gradle project, `port_touch_controls.cpp`, `port_analog_movement.c`, a widescreen header, GL renderer, software PPU, asset packs. Android APK releases are in its CHANGELOG. VERIFIED. |

## Top 5 by work saved

1. **alchemy (GS1 decomp)**: mainly a **reference**, with selective **code to port** (formulas, battle flow, field-object behaviour).
   - Saves the most because it is Golden Sun's real field, battle, Djinn and menu logic.
   - Risks:
     - The code is tightly tied to the GBA (overlays, IWRAM, VRAM).
     - Names are partly placeholders, and the AI-generated naming may be wrong.
     - It is still changing.
     - TLA (sailing, Hover) isn't there yet.
     - There is no licence file, which is fine for personal use.
   - Use Coaltergeist's GS1 decomp to cross-check.
2. **Project Picori + zeldaret/tmc**: **code to port** for the Android platform layer (SDL3, touch, analog stick, renderer, audio, asset packs). **Reference** for movement, collision, heights and puzzle objects.
   - Risks: Picori is GPL-3.0, so fine for personal use but our app would become GPL if ever shared. Its software PPU keeps a GBA-shaped renderer, which suits a C engine and not Godot. tmc itself has no licence.
3. **pokeemerald SDL2 PC ports** ([NTx86/pokeemerald-sdl2pc](https://github.com/NTx86/pokeemerald-sdl2pc), branch `pc_port`; [Kurausukun/pokeemerald](https://github.com/Kurausukun/pokeemerald/tree/pc_port)): **code to port**, but only if we build natively on pokeemerald-expansion.
   - [hirata-producoes/pokemon-regionalidades](https://github.com/hirata-producoes/pokemon-regionalidades) already runs expansion through SDL2 on Windows. VERIFIED from its README.
   - Risks: Windows/Linux only, so Android glue is extra work; no licence file. Expansion's grid-based maps also still need tmc-style free movement grafted on.
4. **pret/pmd-red**: **reference** for ally AI, recruit-after-battle and Pokémon cutscene scripting. **Assets** are limited to Gen 1–3 portraits and 8-direction sprites.
   - Low porting value, because its world is a grid dungeon. No licence file.
5. **SAT-R/sa2 (Sonic Advance 1 and 2)**: **reference**, and proof that one decomp can target SDL, Win32, PS2 and PSP at 426×240 widescreen. VERIFIED.
   - Its `src/platform/pret_sdl` code comes from Kurausukun's pokeemerald `pc_port`. VERIFIED.
   - Mostly duplicates #2 and #3; useful mainly as a clean layout for a multi-target platform layer.

Not in the top 5: Fire Emblem 8 (laqieer/fireemblem8u, 100%) is reference only for multi-unit menus and AI targeting, and GS1's battle UI already covers 4 vs 6. The other 100% projects on decomp.dev (Wario Land 4, Kirby, KH:CoM, Klonoa) don't fit our needs.

## What no GBA source covers (we write it)

- **The battle:** 8 player fighters against about 6, with Adept/partner pairs, the revive window and Rouse, withdrawing and closing the line, Unleash from benched Set Pokémon, a Summon pool per crew, the locked 18-type class, GS-scale stats for Pokémon, and enemy trainers that mirror the crew. GS1 gives the 4-vs-6 skeleton and expansion gives Pokémon move effects; merging them is ours.
- **Crews:** two crews, handovers, a shared bag, per-crew restoration points, and the save format for all of it.
- **Sailing:** ship and world-map sailing, plus Surf, Dive and underwater layers working in a free-movement engine.
- **Lost Age Psynergy:** Hover, Scoop, Cyclone, Parch, Burst, Teleport and the like (not decompiled yet).
- **Fold 7 UI:** cover-screen and inner-screen layouts and touch-first menus.

## Non-GBA open source that may save more

**jjppof/goldensun_html5** (MIT, TypeScript on Phaser 2) is a working GS-style engine:
- 14 field Psynergy files: Move, Frost, Growth, Reveal, Lash, Lift, Pound, Douse, Whirlwind, Mind Read, Retreat, Avoid, Sand, plus a Wave effect.
- Pushable, RollingPillar, RopeDock and Breakable objects.
- About 75 data-driven event types (dialogue, camera, Djinn, battle, party join) and tile events (climb, ice slide, rope, jump).
- Battle with Djinn, Summons, EnemyAI and BattleFormulas.
- It uses Tiled maps, which we already export.

All of that is VERIFIED from its file tree. If the engine is Godot or C#, this is the biggest single saver, ahead of any GBA decomp, with alchemy supplying exact numbers.

Other options:
- **Godot 4** (MIT): the whole Android, touch, tilemap, audio and save layer. Not checked today.
- **smogon/pokemon-showdown** (MIT, VERIFIED): Gen 1–9 move, ability and item effects if we leave the C expansion code.
- **PMDCollab/SpriteCollab** (CC BY-NC 4.0, VERIFIED): 8-direction overworld sprites and portraits for all generations, suiting Djinn-style encounters and portrait dialogue.
- **Solarus** (Zelda-like engine with Android; GPL, INFERRED; moved to GitLab) fits less well.

The trade-off: the C route keeps expansion's battle effects but has to bolt on free movement and an Android layer (Picori pattern). The Godot route gets movement, field Psynergy and Android almost free, but has to re-express Pokémon move effects.

## Sources

- https://decomp.dev/projects?platform=gba
- https://github.com/PascalPixel/alchemy
- https://github.com/Coaltergeist/goldensun-decomp
- https://github.com/zeldaret/tmc
- https://github.com/999sian/tmc
- https://www.timeextension.com/news/2026/05/zelda-minish-cap-gets-natively-ported-to-pc
- https://github.com/SAT-R/sa2
- https://github.com/NTx86/pokeemerald-sdl2pc
- https://github.com/Kurausukun/pokeemerald/tree/pc_port
- https://github.com/hirata-producoes/pokemon-regionalidades
- https://github.com/pret/pmd-red
- https://github.com/laqieer/fireemblem8u
- https://github.com/jjppof/goldensun_html5
- https://github.com/smogon/pokemon-showdown
- https://github.com/PMDCollab/SpriteCollab

Local files read: `C:\Users\aaron\Documents\Game-maker-v1\DESIGN.md` and `C:\Users\aaron\Documents\Game-maker-v1\docs\design\party-and-battle.md`. None of these sources are mentioned anywhere in the project yet.