# Golden Sun 1 & 2: Psynergy, classes, Djinn and summons

Exporter: `gbax/codecs/gs_abilities.py`. Run it with `python -m gbax.codecs.gs_abilities ROM [ROM ...]`.
It writes `games/<slug>/data/abilities.json`, `classes.json`, `djinn.json` and `summons.json`, and prints the
sanity checks. Names come from `games/<slug>/text/strings.json` when that file exists. The text IDs are always
written.

**Evidence.** VERIFIED means checked against ROM bytes, the decompiled accessor, or both. INFERRED means the claim
rests on how the values line up with known abilities and names.

## How the tables are found (no hard-coded addresses)

1. The exporter finds the master file table (entry 0 = `0x08000000`, entry 1 = the table itself). From it, it
   takes the code modules (files that start with `ldr r4,=f; bx r4`) and their extents.
2. It collects every aligned ROM pointer in the literal pools of the kernel and the code modules.
3. It tests each pointer against a shape check for each table, and exactly one must match:
   - **Ability table**: records 0/1/2 start `01 05 04` (Nothing), `01 83 04` (Attack) and `04 89 04` (Defend).
   - **Class table**: record 0 is type 12 with every multiplier at 100%, and record 1 is type 1.
   - **Djinn table**: the u32 at each 12-byte step runs 300..379.
   - **Summon table**: starts with `380, 01 00 00 00`.
4. It checks each table's end against the next table the code references. The ability table ends where the enemy
   table starts, and that enemy table is code-referenced. The class table ends at the class-type table. The summon
   table ends at the class table.

`PROFILES` in the module records the addresses below. The exporter warns if a fresh discovery disagrees.

## Addresses (VERIFIED)

All tables sit in data module #5 (GS1 `0x08077000`, GS2 `0x080AD000`).

| Table | GS1 (AGSE) | GS2 (AGFE) | Record | Count |
|---|---|---|---|---|
| Abilities | `0x0807EE58` (literal at `0x08078BBC`) | `0x080B7C14` (literal at `0x080AF460`) | 16 / 12 bytes | 519 / 734 |
| GetAbility | `0x08078B9C` | `0x080AF43C` | `id &= 0x3FFF; id > 0x207 / 0x2DE -> 0` | |
| Classes | `0x08084B1C` | `0x080C15F4` | 0x54 | 203 / 244 slots (92 / 111 used) |
| Class-type grid | `0x08088DB8` | `0x080C6604` | 16 x u32 | 4x4 |
| Class selection | `0x080799B0` | `0x080B0144` (+ levels `0x080AFFAC`) | | |
| Djinn | `0x0808926C` (literal at `0x0807A0F0`) | `0x080C6BB0` (literal at `0x080B0AB4`) | 12 | 80 slots = 4 x 20 (28 / 72 used) |
| GetDjinn(elem, idx) | `0x0807A0CC` | `0x080B0A94` | | |
| Summons | `0x08084A9C` (literal at `0x080797E8`) | `0x080C150C` (literal at `0x080AFF90`) | 8 | 16 / 29 |
| GetSummon(i) | `0x080797D4` (`i < 16`) | `0x080AFF7C` (`i < 29`) | | |
| Summon menu order | `0x08084A8C` (16 bytes) | `0x080C14EC` (28 bytes, + u32 28) | | |
| Elemental data | `0x08088E38` | `0x080C6684` (24-byte records, 48 entries per gsmagic) | | |

GetAbility's bounds check is `id > max -> 0`, so the code also accepts id 519 / 734, one past the last record (that
index reads the start of the enemy table). The text layout confirms 519 / 734 records.

## Text IDs (VERIFIED against the decoded strings)

| | GS1 | GS2 |
|---|---|---|
| Ability name | 819 + id | 1447 + id |
| Ability description | 1338 + id (819 + 519) | 2181 + id (1447 + 734) |
| Class name | 1857 + id | 2915 + id |
| Item name | (not needed) | 607 + id |

The GS2 values match gsmagic (`Sub-editors/eClass.cs`: class names at `2915 + i`, `psyNames` at `1447 + i`). The
exporter re-finds the bases from the strings by looking for "Attack", "Defend" and "Cure" at ids 1, 2 and 90. Djinn
names are their ability names (300 + element\*20 + index), and summon names are ability names too (380 and up).

## Ability record

The layout is the same in both games, except that GS1 has 4 extra bytes and keeps the field id at +12.

| Off | Type | Field | Evidence |
|---|---|---|---|
| 0 | u8 | Target: 0 none (map only), 1 enemies, 2 allies, 4 self | INFERRED (Move 0, Quake 1, Cure 2, Defend 4) |
| 1 | u8 | Flags: low nibble = damage type; `0x80` usable in battle; `0x40` usable from the out-of-battle menu | INFERRED (Power Bread `0x49` is menu-only; Move `0x09` is map-only; Cure `0xC1`) |
| 2 | u8 | Element: 0 Venus, 1 Mercury, 2 Mars, 3 Jupiter, 4 Neutral | VERIFIED (Djinn and summons line up per element) |
| 3 | u8 | Effect id (status or special effect), e.g. 3 cure poison, 5 revive, 46 guard | INFERRED (from the descriptions) |
| 4 | u16 | Battle animation id (0 for items and Djinn) | INFERRED (consecutive within each series) |
| 6 (GS2) / 12 (GS1) | u16 | Field-Psynergy id (map effect) | INFERRED (examples below) |
| 8 | u8 | Range r: hits 2r−1 targets centred on the chosen one; 255 = all | INFERRED (Quake 2, Earthquake 3; summons use 6) |
| 9 | u8 | PP cost | VERIFIED (Move 2, Cure 3) |
| 10 | u16 | Power (heal amount, base damage, or ×10 multiplier for type 4) | VERIFIED (Cure 70, Cure Well 150, Pure Ply 1000) |

There is no accuracy field. Hit chance and status chance must come from code.

The field ids are:

| Id | Psynergy | Id | Psynergy | Id | Psynergy |
|---|---|---|---|---|---|
| 1 | Move | 2 | Mind Read | 3 | Ply series |
| 4 | Force | 5 | Douse | 6 | Frost |
| 7 | Lift | 8 | Reveal | 9 | Halt |
| 10 | Cloak | 11 | Carry | 12 | Growth |
| 13 | Catch | 14 | Whirlwind / Gale | 15 | Retreat |
| 16 | Avoid | 17 | Lash (GS2) | 18 | Pound (GS2) |
| 19 | Tremor (GS2) | 20 | Scoop (GS2) | 21 | Burst (GS2) |
| 22 | Parch (GS2) | 23 | Sand (GS2) | 24 | Hover (GS2) |
| 25 | Cyclone (GS2) | 26 | Blaze (GS2) | 27 | Grind (GS2) |
| 28, 29 | unnamed in the decoded text (GS2) | 30 | Teleport (GS2) | | |

The exporter's `usable_in_field` is true when flag `0x40` is set or the field id is nonzero.

Damage types (low nibble of the flags byte, INFERRED from the members of each group; the counts are non-empty GS1 / GS2 records):

| Value | Name | Examples | GS1 | GS2 |
|---|---|---|---|---|
| 1 | healing | Cure, Herb | 21 | 39 |
| 2 | effect_only | Cure Poison, Revive, Impact | 64 | 92 |
| 3 | added_damage | Attack, Ragnarok (power is added to the attack) | 73 | 178 |
| 4 | multiplier | Quick Strike, Flint (power ×10) | 12 | 47 |
| 5 | base_damage | Quake, Flare | 141 | 125 |
| 6 | base_damage_alt | only Fire/Water Breath-style enemy abilities, ids 420 and up | 26 | 46 |
| 7 | djinn_effect | Granite, Flash, Kite | 3 | 15 |
| 8 | summon | Venus...Iris | 18 | 34 |
| 9 | utility | Defend, Move | 29 | 48 |
| 10 | psynergy_drain | Crazy Voice, Fugue | 1 | 2 |
| 11 | psynergy_recovery | Psy Crystal, Ember, Ether | 3 | 6 |

Records with all bytes zero are flagged `empty`: GS1 128, GS2 102.

Id ranges in both games:

| Ids | Contents |
|---|---|
| 0 | Nothing |
| 1–2 | Attack, Defend |
| 3.. | Psynergy, grouped by element and series |
| 90–103 | Healing and support |
| 133–160 | Utility and field Psynergy (Move is 140) |
| ~162–240 | Weapon and class skills |
| 250+ | Item effects |
| 300–379 | Djinn (element\*20 + index) |
| 380+ | Summons (Venus 380) |
| 420+ | Enemy-only abilities |

## Class record (0x54 bytes)

| Off | Field | Evidence |
|---|---|---|
| 0 | u32 class type (series) | VERIFIED (compared with the selection type, 0x080B0144) |
| 4 | u8[4] elemental-level requirements (Ve, Me, Ma, Ju) | VERIFIED (`req*10 <= level[e]` in 0x080799B0 / 0x080B0144) |
| 8 | u8[6] HP, PP, Atk, Def, Agi, Luck multipliers in 10% steps (Squire 110/80/110/100/110/100) | INFERRED (gsmagic shows `i*10%`) |
| 0x10 | 16 learned Psynergy. GS2: u16 ability, u16 level. GS1: u8 ability, u8 level, u16 0 | GS2 per gsmagic; GS1 from data (all bytes 2–3 are zero, and the lists match GS2 exactly) |
| 0x50 | u8[3] effect weaknesses (effect ids, e.g. Squire 31, 60) | gsmagic label; INFERRED meaning |

The requirements are **elemental levels**, not raw Djinn counts. The game's elemental level is
`10*A[e] + B[e]`, where `A` is 4 bytes at character-struct +0x24 and `B` is 4 bytes at party-record +0x92. In
GS2 this is computed by `0x080AFFAC`. My reading is that `A` holds the innate level plus the Set Djinn and `B` is a
tenths tie-breaker (INFERRED; the source of each array wasn't traced).

**Selection algorithm (VERIFIED from the decompiled code, the same in both games):**

1. The primary element is the one with the highest level; on a tie, the lowest index wins.
2. The secondary element is the highest of the other three. If its level is below 10 (elemental level < 1), the
   secondary is the primary again.
3. `type = grid[primary*4 + secondary]`. The grid is identical in both games:

   | Primary \ secondary | Venus | Mercury | Mars | Jupiter |
   |---|---|---|---|---|
   | Venus | 1 Squire | 3 Swordsman | 4 Brute | 5 Apprentice |
   | Mercury | 8 Seer | 6 Water Seer | 9 Pilgrim | 10 Hermit |
   | Mars | 4 Brute | 3 Swordsman | 2 Guard | 5 Apprentice |
   | Jupiter | 8 Seer | 10 Hermit | 9 Pilgrim | 7 Wind Seer |

4. The game scans the classes from the last index down and takes the first one of that type whose four
   requirements are all met. If none matches, it uses class 0.

Overrides:

- **GS1**: if story flag 0x20 is set, Isaac gets class 200 and Garet class 201. pc 5 always gets class 202
  (Flame User, type 11).
- **GS2**: type 2 for Jenna (pc 5) becomes type 13 (Flame User); type 6 for Piers (pc 7) becomes type 14
  (Mariner). The items 0x1BB Mysterious Card, 0x1BC Trainer's Whip and 0x1BD Tomegathericon force types 15
  Pierrot, 16 Tamer and 17 Dark Mage.

Series (type: first class, number of classes):

| Type | Series | GS1 | GS2 |
|---|---|---|---|
| 1 | Squire | 5 | 5 |
| 2 | Guard | 5 | 5 |
| 3 | Swordsman | 13 | 13 |
| 4 | Brute | 8 | 8 |
| 5 | Apprentice | 13 | 13 |
| 6 | Water Seer | 5 | 5 |
| 7 | Wind Seer | 5 | 5 |
| 8 | Seer | 13 | 13 |
| 9 | Pilgrim | 13 | 13 |
| 10 | Hermit | 8 | 8 |
| 11 | special | 3 | – |
| 12 | NPC | 1 | 1 |
| 13 | Flame User | – | 5 |
| 14 | Mariner | – | 5 |
| 15 | Pierrot | – | 4 |
| 16 | Tamer | – | 4 |
| 17 | Dark Mage | – | 4 |

Each series takes a run of class slots (Squire is 1–5, Guard starts at about 10). The unused slots between the
runs are all zeros (`empty: true`): GS1 has 92 of 203 slots in use, GS2 111 of 244.

## Djinn record (12 bytes, VERIFIED)

The layout is `u32 ability, u8 HP, PP, Atk, Def, Agi, Luck (bonus while Set), u16 0`. Slot = element\*20 + index,
read through GetDjinn. Flint, for example, is ability 300 with HP +8, PP +4 and Atk +3.

- **GS1**: 7 used per element, 28 in total.
- **GS2**: 18 per element, 72 in total. The first 7 per element match GS1.

The unleash effect is the ability record. For example, Flint is a multiplier of 16, Granite is a Djinn effect
(guard), and Quartz is effect-only (revive). The tables hold nothing about Standby or Recovery. The Djinn timing
(recovery turns, Set/Standby state) lives in code and in the save/RAM state.

## Summon record (8 bytes, VERIFIED)

The layout is `u32 ability, u8 cost[4] (Ve, Me, Ma, Ju)`. Power, element, range (6), effect and animation come
from the ability record.

- **GS1**: Venus/Mercury/Mars/Jupiter cost 1 each (power 30), Ramses... cost 2 (60), Cybele... 3 (120), and
  Judgment... 4 (240).
- **GS2** adds:

  | Summon | Cost | Power |
  |---|---|---|
  | Zagan | Ve1 Ma1 | 50 |
  | Megaera | Ma1 Ju1 | 40 |
  | Flora | Ve1 Ju2 | 80 |
  | Moloch | Me2 Ju1 | 100 |
  | Ulysses | Me2 Ma2 | 160 |
  | Haures | Ve3 Ma2 | 270 |
  | Eclipse | Me2 Ju3 | 300 |
  | Coatlicue | Me3 Ju3 | 60, range all (heal) |
  | Daedalus | Ve3 Ma4 | 100 |
  | Azul | Ve3 Me4 | 330 |
  | Catastrophe | Ma3 Ju5 | 400 |
  | Charon | Ve8 Ju2 | 500 |
  | Iris | Me4 Ma9 | 800 |

The extra damage based on a percentage of the target's HP isn't in these tables. It's presumably in the summon
code or the effect id (Charon has effect 27); that's INFERRED and not yet traced.

## Sanity checks (all pass on both ROMs)

| Check | Result |
|---|---|
| Move costs 2 PP | OK |
| Class 1 is Squire (type 1, needs Venus level 5) | OK |
| Djinn count (GS1 28, GS2 72) | OK |
| Venus summon costs 1 Venus Djinni | OK |
| Summon count (GS1 16, GS2 29) | OK |
| Cure is ability 90: 3 PP, heals 70 | OK |
| Flint gives HP +8, PP +4, Atk +3 | OK |

Checked against goldensunwiki.net by the verification pass: all match.

- **Quake's power is 12** (Earthquake 35, Quake Sphere 65), the same in both games, as on the wiki.
- **The Squire learns only Cure at level 1**; Quake comes at level 2. The full list matches the wiki: Cure 1, Quake 2,
  Earthquake 4, Spire 6, Cure Well 10, Ragnarok 13, Quake Sphere 14, Clay Spire 20, Potent Cure 26, Stone Spire 42.
- **Move's element byte is 2 (Mars)**, as on the wiki.

Isaac's starting class being Squire also depends on his innate elemental levels, which are in the character data
and weren't extracted here.

## Sources

- gsmagic (Atrius/Teawater's editor successor), <https://github.com/adituv/gsmagic>:
  `Sub-editors/eClass.cs` gives the GS2 class table `0xC15F4` x `0x54` (244 entries), the text bases 2915 and
  1447, the class-type table `0xC6604`, and the 16 ability/level pairs. `Editors.cs` gives the elemental data
  `0xC6684` x `0x18`, the enemy table `0xB9E7C` x `0x4C`, and the item names at 607. Every address was re-checked
  against the ROM bytes and the decompiled accessors above.

## Open questions

- The field-Psynergy dispatch: which code maps field id 1..30 to map handlers. The likely place is a jump table in
  the field module; it wasn't traced.
- Effect id semantics, both status and special effects (0–~70). They need the battle code's effect switch.
- The summon damage formula (the HP-percentage bonus), and the meaning of the GS2 effect field on summons.
- Djinn recovery and standby rules (code). The tables hold only the Set bonuses and the unleash ability.
- The GS2 u16 list at `0x080C6B18` (76 ability ids: heals, Aura, some Djinn) and the u16 table at
  `0x080C6644` / GS1 `0x08088DF8` (75, 85, 80, 90 ...). Their purpose is unknown.
- Classes 200/201 in GS1 (the prologue Isaac/Garet classes, type 11) have no name in the decoded text.
