# Symbol-by-symbol diff: Unbound vs FireRed v1.0

Each original FireRed function or table was relocated from Rev 1 to its v1.0 address and compared with Unbound. Full list: `symbol_diff.csv`.

## Status counts

| Status | Code | Data | Unknown | Total | Bytes |
|---|---|---|---|---|---|
| unchanged | 10,501 | 9,534 | 1,455 | 21,490 | 2,344,893 |
| references moved | 295 | 573 | 19 | 887 | 540,285 |
| patched | 248 | 814 | 222 | 1,284 | 83,629 |
| hooked | 557 | 0 | 0 | 557 | 161,982 |
| hooked (unlisted) | 121 | 0 | 0 | 121 | 16,212 |
| modified | 218 | 608 | 118 | 944 | 338,930 |
| overwritten | 27 | 4,723 | 207 | 4,957 | 1,942,612 |
| differs v1.0/Rev 1 | 2 | 2 | 0 | 4 | 783 |

Statuses:
- **unchanged**: identical to vanilla after relocation.
- **references moved**: code and data intact, only pointers changed (a table or function it uses was replaced elsewhere).
- **calls redirected**: code intact except `BL` calls now going to different functions.
- **patched**: a small edit (under 16 bytes) with no branch out.
- **hooked**: CFRU or DPE redirects it to new code (named in the note).
- **hooked (unlisted)**: small `ldr`+`bx` style redirect not in the public CFRU/DPE lists, so likely Unbound-specific.
- **modified**: larger edits that keep most of the original.
- **overwritten**: more than half the bytes differ; the space was reused or the routine replaced.
- **differs v1.0/Rev 1**: the symbol changed size between versions, so it can't be compared exactly.

## By game system

Share of each system's original symbols that are still byte-identical in Unbound (after relocation). High means the pokefirered source still describes Unbound's version; low means Unbound/CFRU/DPE replaced it.

| System | Code unchanged | Data unchanged | Hooked | Patched/modified | Overwritten |
|---|---|---|---|---|---|
| Battle engine & AI | 86% of 2,976 | 90% of 2,164 | 202 | 243 | 69 |
| Pokémon data & rules | 76% of 662 | 26% of 1,630 | 78 | 71 | 1,178 |
| Trainers | 96% of 197 | 33% of 1,363 | 6 | 420 | 445 |
| Graphics & tilesets | – | 28% of 4,673 | 0 | 411 | 2,675 |
| Text & strings | 100% of 204 | 77% of 2,822 | 0 | 348 | 281 |
| Maps, overworld & scripts | 89% of 2,836 | 89% of 1,006 | 152 | 136 | 35 |
| Menus & UI | 80% of 1,586 | 80% of 775 | 127 | 174 | 54 |
| Audio | 86% of 119 | 92% of 13 | 7 | 3 | 2 |
| Core engine | 96% of 937 | 90% of 115 | 21 | 12 | 2 |
| Other | 92% of 2,452 | 94% of 1,693 | 85 | 70 | 9 |
| Unindexed (libraries, asm data) | – | – | 0 | 340 | 207 |

## Source files with the most changed symbols

| File | Changed / total | Hooked | Modified/overwritten | Refs moved |
|---|---|---|---|---|
| `src/data/graphics/pokemon.h` | 2338/2405 | 0 | 2322 | 15 |
| `src/data/pokemon/pokedex_text_fr.h` | 756/774 | 0 | 755 | 0 |
| `src/data/trainer_parties.h` | 648/742 | 0 | 369 | 0 |
| `src/data/pokemon/level_up_learnsets.h` | 411/411 | 0 | 409 | 0 |
| `src/strings.c` | 389/1189 | 0 | 213 | 6 |
| `src/graphics.c` | 252/896 | 0 | 109 | 140 |
| `src/data/graphics/trainers.h` | 232/306 | 0 | 207 | 25 |
| `src/data/object_events/object_event_graphics.h` | 151/232 | 0 | 150 | 1 |
| `src/data/object_events/object_event_graphics_info.h` | 142/154 | 0 | 102 | 3 |
| `src/battle_message.c` | 139/598 | 3 | 44 | 1 |
| `src/data/object_events/object_event_pic_tables.h` | 127/151 | 0 | 119 | 4 |
| `src/battle_script_commands.c` | 118/294 | 39 | 52 | 20 |
| `src/data/tilesets/graphics.h` | 109/128 | 0 | 101 | 8 |
| `src/data/tilesets/metatiles.h` | 105/136 | 0 | 103 | 2 |
| `src/move_descriptions.c` | 83/355 | 0 | 14 | 0 |
| `src/pokemon.c` | 72/163 | 29 | 14 | 19 |
| `src/party_menu.c` | 69/357 | 29 | 17 | 15 |
| `src/pokemon_summary_screen.c` | 66/204 | 17 | 32 | 5 |
| `src/data/graphics/items.h` | 60/466 | 0 | 16 | 36 |
| `src/data/tilesets/headers.h` | 55/68 | 0 | 9 | 44 |
| `src/event_object_movement.c` | 49/854 | 21 | 6 | 6 |
| `src/pokedex_screen.c` | 45/155 | 12 | 2 | 25 |
| `src/data/easy_chat/easy_chat_group_lifestyle.h` | 45/46 | 0 | 45 | 0 |
| `src/intro.c` | 44/193 | 1 | 21 | 18 |
| `src/region_map.c` | 43/204 | 12 | 20 | 4 |
| `src/battle_main.c` | 41/124 | 23 | 5 | 8 |
| `src/item_menu.c` | 39/132 | 15 | 0 | 2 |
| `src/data/text/quest_log.h` | 37/125 | 0 | 6 | 0 |
| `src/map_preview_screen.c` | 35/80 | 0 | 9 | 26 |
| `src/battle_anim_special.c` | 32/99 | 9 | 5 | 15 |

## Code changes not explained by public CFRU/DPE lists (434)

Likely Unbound-specific edits, or CFRU changes made after the public version. Top 40 by bytes changed:

| Function | File | Status | Bytes changed / size |
|---|---|---|---|
| `CalculateBaseDamage` | `src/pokemon.c` | modified | 1113/2248 |
| `GetPlayerPositionOnRegionMap_HandleOverrides` | `src/region_map.c` | overwritten | 1040/1060 |
| `GetMapsecType` | `src/region_map.c` | overwritten | 652/666 |
| `GetDungeonMapsecType` | `src/region_map.c` | overwritten | 570/590 |
| `TypeCalc` | `src/battle_script_commands.c` | overwritten | 309/472 |
| `Cmd_get_ability` | `src/battle_ai_script_commands.c` | overwritten | 280/280 |
| `Cmd_if_has_move_with_effect` | `src/battle_ai_script_commands.c` | overwritten | 244/244 |
| `Cmd_get_type` | `src/battle_ai_script_commands.c` | overwritten | 240/240 |
| `ItemBattleEffects` | `src/battle_util.c` | modified | 219/4988 |
| `Cmd_if_has_move` | `src/battle_ai_script_commands.c` | overwritten | 218/218 |
| `Cmd_if_doesnt_have_move` | `src/battle_ai_script_commands.c` | overwritten | 218/218 |
| `Cmd_if_doesnt_have_move_with_effect` | `src/battle_ai_script_commands.c` | overwritten | 216/216 |
| `UpdatePartySelectionSingleLayout` | `src/party_menu.c` | overwritten | 211/264 |
| `FindMonThatAbsorbsOpponentsMove` | `src/battle_ai_switch_items.c` | modified | 171/540 |
| `Cmd_accuracycheck` | `src/battle_script_commands.c` | modified | 158/1044 |
| `Cmd_typecalc` | `src/battle_script_commands.c` | modified | 145/624 |
| `Task_NewGameScene` | `src/oak_speech.c` | modified | 145/856 |
| `Cmd_tryswapitems` | `src/battle_script_commands.c` | modified | 133/688 |
| `GetUnlockedSeviiAreas` | `src/field_specials.c` | overwritten | 131/184 |
| `Cmd_handleballthrow` | `src/battle_script_commands.c` | modified | 119/972 |
| `Cmd_get_hold_effect` | `src/battle_ai_script_commands.c` | overwritten | 117/128 |
| `TryDoForceSwitchOut` | `src/battle_script_commands.c` | overwritten | 111/200 |
| `Cmd_get_weather` | `src/battle_ai_script_commands.c` | overwritten | 108/108 |
| `Task_OakSpeech_HandleRivalNameInput` | `src/oak_speech.c` | overwritten | 102/144 |
| `PlayerHasGrassPokemonInParty` | `src/field_specials.c` | overwritten | 101/102 |
| `AI_TypeCalc` | `src/battle_script_commands.c` | modified | 95/252 |
| `PokeSum_PrintExpPoints_NextLv` | `src/pokemon_summary_screen.c` | overwritten | 94/104 |
| `CreateNPCTrainerParty` | `src/battle_main.c` | modified | 75/1004 |
| `Cmd_adjustnormaldamage` | `src/battle_script_commands.c` | modified | 71/432 |
| `CanLearnTutorMove` | `src/party_menu.c` | overwritten | 71/82 |
| `Cmd_moveend` | `src/battle_script_commands.c` | modified | 70/2600 |
| `Cmd_if_would_go_first` | `src/battle_ai_script_commands.c` | overwritten | 64/76 |
| `Cmd_if_would_not_go_first` | `src/battle_ai_script_commands.c` | overwritten | 64/76 |
| `Cmd_tryrecycleitem` | `src/battle_script_commands.c` | modified | 62/168 |
| `Cmd_damagecalc` | `src/battle_script_commands.c` | modified | 61/240 |
| `DoFieldEndTurnEffects` | `src/battle_util.c` | modified | 59/1876 |
| `PrintSkillsPage` | `src/pokemon_summary_screen.c` | modified | 58/388 |
| `Cmd_settypebasedhalvers` | `src/battle_script_commands.c` | modified | 57/184 |
| `IsMonDisobedient` | `src/battle_util.c` | modified | 56/808 |
| `AI_CalcDmg` | `src/battle_script_commands.c` | modified | 53/228 |

## Patch-list coverage

- CFRU/DPE hook entries: 664 (CFRU 624, DPE 40); vanilla symbols carrying at least one: 557
