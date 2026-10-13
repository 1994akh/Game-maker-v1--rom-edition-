# Golden Sun 1 & 2: enemies, encounters, items and playable characters

Extractor: `gbax\codecs\gs_units.py`. Run it with
`.venv\Scripts\python.exe -m gbax.codecs.gs_units "<GS1 rom>" "<GS2 rom>"`. It writes `games\<slug>\data\`
`enemies.json`, `encounters.json` (encounter tables plus enemy groups), `items.json` and `characters.json` (PCs, EXP
table, elemental-level table, summons, raw class table). At startup it checks that a Thumb literal pool still points
at every table, and stops if one doesn't. If `text\strings.json` or `data\abilities.json` from the other extractors
exist, names are filled in; `{ART:n}` article codes are stripped.

**Evidence labels.** VERIFIED means read from the game's code (decompiled or disassembled) or checked against ROM
bytes. INFERRED means a data pattern, cross-game analogy or community docs.

## Where the tables are

All the data tables sit in code module 5 (GS1 `0x08077000`, GS2 `0x080AD000`), next to the module's accessor
functions. Both games export those accessors in nearly the same stub order: GS1 stub *n*+1 matches GS2 stub *n*.

| Table | GS1 (AGSE) | GS2 (AGFE) | Stride | Count GS1 / GS2 | How the count was found |
|---|---|---|---|---|---|
| Items | `0x0807B6A8` | `0x080B2364` | 0x2C | 269 / 461 named (324 / 516 slots) | accessor `id&0x1FF * 0x2C` VERIFIED; the slots after the named ones are identical filler |
| Abilities | `0x0807EE58` | `0x080B7C14` | **0x10** / 0x0C | 519 / 734 | decoded by `gs_abilities`; ends where the enemy table starts |
| Enemies | `0x08080EC8` | `0x080B9E7C` | **0x54** / 0x4C | 165 / 380 | VERIFIED: GS1 `cmp r5,#0xA4`; GS2 `if (0x17B < i) i = 0`. Real enemies are 1–163 / 1–378: row 0 is a "???" dummy and the last row an empty sentinel (both flagged `placeholder`) |
| Enemy elemental data | `0x08088E38` | `0x080C6684` | 0x18 | 44 / 48 | VERIFIED clamps: `0x2B` (GS1 `0x080797FC`), `0x2F` (GS2 `0x080AFFBE`) |
| PCs | `0x080844EC` | `0x080C0F4C` | 0xB4 | 8 / 8 | VERIFIED: GS1 `FUN_08078ed8` returns `pc*0xB4 + table` |
| Elemental level → power/resist | `0x08088DF8` | `0x080C6644` | 4 | 16 | VERIFIED for GS1 (`FUN_080798e0`); GS2 has identical bytes |
| EXP per level (u32, cumulative) | `0x0807A830` | `0x080B12C8` | 4 | 99 | data match plus code ref (GS1 `0x0807903E`, GS2 `0x080AF906`) |
| Summons | `0x08084A9C` | `0x080C150C` | 8 | 16 / 29 | table size; names check out (Venus, Mercury, Mars, Jupiter, Ramses, ...) |
| Classes | `0x08084B1C` | `0x080C15F4` | 0x54 | 203 / 244 | table size, exact fit |
| Enemy groups | `0x080C5C38` | `0x0812CE7C` | **0x10** / 0x18 | 380 / 660 | GS2 VERIFIED (`if (0x293 < id) id = 1`); GS1 INFERRED from table size, and the highest group the encounter tables use is 379 |
| Encounter tables | `0x0809C610` | `0x080EDACC` | 0x1C | 104 / 110 | GS1 INFERRED from the data boundary at `0x0809D170`; GS2 from gsmagic |

Code that reads them (VERIFIED):

- **Enemy accessors:** GS1 `0x080773D8` (export stub 51, `0x08077198`), GS2 `0x080AD3A8` (stub 40). Both compute
  `(battle_id-8)*stride + table`.
- **Enemy unit init:** GS1 `0x08079460`, GS2 `FUN_080afbec`.
- **Battle rewards:** GS1 around `0x080C2598`, GS2 `FUN_0812824c`.
- **Enemy AI:** GS2 `FUN_08122514`.
- **Encounter roll:** GS1 `FUN_0808ae74(encounter_id)`.
- **Group setup:** GS1 `0x080C1A40`, GS2 `FUN_08127cd4`.
- **PC level-up:** GS1 `FUN_0807905c`.
- **New-game PC init:** GS1 `FUN_08078ee8`.

Text IDs:

| | GS1 | GS2 |
|---|---|---|
| Enemy name | `0x28F + enemy_index` (VERIFIED) | `0x42C + enemy_index` (VERIFIED) |
| Item name | `0x182 + item_id` | `0x25F + item_id` |

The item bases are consistent with the enemy bases: `0x182 + 269 = 0x28F` and `0x25F + 461 = 0x42C`. Names come
out right with `strings.json`.

## Enemy record

The two layouts are the same up to `+0x1D`. GS1 then has 10 extra bytes (`+0x1E..+0x27`, always zero), so every
later field is 0x0A further on.

| Field | GS2 | GS1 | Notes |
|---|---|---|---|
| name (debug) | 0x00 (15 bytes) | 0x00 | blanked with spaces in the USA release; the real name comes from text |
| level, HP, PP, Atk, Def, Agi | 0x0F u8, 0x10/12/14/16/18 u16 | same | VERIFIED (copied by unit init) |
| luck, turns, HP regen, PP regen | 0x1A–0x1D u8 | same | VERIFIED |
| battle items (4×u16) + counts (4×u8) | 0x1E / 0x26 | 0x28 / 0x30 | VERIFIED; up to 15 uses copied into the unit's inventory |
| elemental data index | 0x2A | 0x34 | VERIFIED |
| attack type | 0x2B | 0x35 | VERIFIED as read by the AI (values 0/1/2); meaning INFERRED |
| AI pattern | 0x2C | 0x36 | VERIFIED: `switch 0..6`. 0–2 pick a slot from weighted tables, 3–4 walk the slots in order, 5 is +1 |
| item-use mask | 0x2D | 0x37 | VERIFIED: bit *i* means slot *i* uses a battle item |
| abilities (8×u16) | 0x2E | 0x38 | VERIFIED; ability IDs |
| weaknesses (3×u8) | 0x3E | 0x48 | VERIFIED as a 3-entry list the game matches an effect against (classes have the same at +0x50) |
| coins | 0x42 | 0x4C | VERIFIED (corrected: an earlier version had EXP and coins swapped) |
| drop item | 0x44 | 0x4E | VERIFIED |
| drop rate code *r* | 0x46 | 0x50 | VERIFIED: drop if `rand16 < 0x20000 >> r` (GS2 subtracts 2 from *r* in one mode), so *r*=1 is always, 5 is 1/16 and 6 is 1/32 |
| EXP | 0x48 | 0x52 | VERIFIED: the GS2 reward routine `FUN_0812824c` adds enemy +0x48 into battle state +0x554, which `0x081284C0` prints with text 3206 ("You got {NUM} experience point{S}"); GS1 values match goldensunwiki.net (Mad Vermin 55 EXP / 80 coins, Killer Ape 460 / 1500) |

In the GS2 reward code, EXP and coins get a random bonus when the extra-reward flag is set:
`max(sum(level/10+1 rolls), base*3/10)`.

**Elemental data record (0x18 bytes).** u32 element at +0 (0 Venus, 1 Mercury, 2 Mars, 3 Jupiter, 4 Neutral);
four u8 levels at +4; then four (s16 power, s16 resist) pairs at +8 (VERIFIED, from the enemy branch of
`FUN_080798e0`).

Sample (GS1 enemy 1): Vermin, Lv 1, HP 20, PP 0, Atk 23, Def 7, Agi 7, Luck 2, EXP 2, coins 2, drops Herb (item 180)
at 1/16, abilities Attack/Defend/Flee.

Sample (GS2 enemy 1): Venus Djinni, Lv 12, HP 349, EXP 172, coins 201, abilities Earthquake, Spire, Gaia, Mad Growth,
Briar.

## Groups and encounters

- **GS2 group (0x18 bytes, VERIFIED).** `u16 enemy[5]` (enemy table index; battle ID = index+8), `u8 min[5]` at 0x0A,
  `u8 max[5]` at 0x0F, `u8 formation` at 0x14 (copied into the battle state at +0x42), then 3 unknown bytes. The
  number of each enemy is min plus a random amount up to max, within a budget of 6 slots (large enemies take 2).
- **GS1 group (0x10 bytes, VERIFIED read at `0x080C1A40`).** `u8 formation`, `u8 enemy[5]` at 1, `u8 min[5]` at 6,
  `u8 max[5]` at 0x0B.
- **Encounter table (0x1C bytes, both games; VERIFIED in GS1 `FUN_0808ae74`).** `u16 rate`, `u16 target_level`,
  `u16 group[8]` at 4, `u8 weight[8]` at 0x14.
  - The game takes the party's average level minus `target_level`, clamped to 0–5, which scales the encounter step.
  - It then picks a group by weight.
  - Entries with rate 0 are scripted or debug (GS2 #1 lists the Venus Djinni groups).
- Sample, GS1 encounter 1 (rate 37, level 1): Vermin×2–3 (weight 4), Bat×2–3 (8), Wild Mushroom×1–3 (8), mixed (4).
- **Per-area mapping isn't extracted.** The encounter ID is passed to `FUN_0808ae74` by the map or area code (module 6
  or the map scripts), so it belongs with the map pass.

## Item record (0x2C bytes, same in both games)

| Field | Offset | Notes |
|---|---|---|
| price | 0x00 u16 | |
| type | 0x02 u8 | 0 item, 1 weapon, 2 armor, 3 shield/armlet, 4 helm, 5 boots, 6 Psynergy item, 8/9/10/11 = rings, shirts, class items etc. (INFERRED; checked against which types carry attack or defense) |
| flags | 0x03 u8 | 0x08 important (all Psynergy items), 0x10 stackable (Herb); the other bits are INFERRED |
| equip mask | 0x04 u8 | bit order Isaac, Garet, Ivan, Mia, Felix, Jenna, Sheba, Piers (VERIFIED: GS2 sets bit 7 on items GS1 leaves 0, e.g. Long Sword `0x13` becomes `0x93`) |
| icon | 0x06 u16 | |
| attack | 0x08 u16 | |
| defense | 0x0A u8 | |
| unleash rate | 0x0B u8 | |
| use type | 0x0C u8 | VERIFIED: 1 means usable, with the ability at +0x28 (GS2 AI). Observed values: 1 consumable, 2 reusable (may break), 3 Psynergy items, 0 none |
| unleash ability | 0x0E u16 | |
| element | 0x14 u32 | 4 = none |
| equipped effects | 0x18 | 4 × (u8 type, s8 value, 2 pad) |
| use ability | 0x28 u16 | |

Checks against well-known values (all match): Long Sword 200 coins, Atk 14; Herb 10 coins; Gaia Blade 17000 coins,
Atk 135, unleashes Titan Blade; Swift Sword Atk 104, unleashes Sonic Smash.

**Psynergy items.** The type-6 items grant the use-ability Psynergy while held. Item and ability IDs are VERIFIED,
and the names are from text and abilities.json.

- **GS1 (8):**

  | Item | Grants (ability ID) |
  |---|---|
  | 200 Orb of Force | Force (142) |
  | 201 Douse Drop | Douse (33) |
  | 202 Frost Jewel | Frost (24) |
  | 203 Lifting Gem | Lift (143) |
  | 204 Halt Gem | Halt (145) |
  | 205 Cloak Ball | Cloak (146) |
  | 206 Carry Stone | Carry (147) |
  | 207 Catch Beads | Catch (148) |

- **GS2 (17):** the same eight with the same IDs, plus these nine:

  | Item | Grants (ability ID) |
  |---|---|
  | 198 Lash Pebble | Lash (133) |
  | 199 Pound Cube | Pound (134) |
  | 208 Tremor Bit | Tremor (135) |
  | 209 Scoop Gem | Scoop (136) |
  | 210 Cyclone Chip | Cyclone (137) |
  | 213 Burst Brooch | Burst (151) |
  | 214 Grindstone | Grind (152); equip mask `0x11`, so Isaac and Felix only |
  | 215 Hover Jade | Hover (153) |
  | 217 Teleport Lapis | Teleport (156) |

- **Sand** (GS2 ability 139, utility) isn't granted by any item, so it must come from a class.
- Ability IDs are shared between the games.

## Playable characters (0xB4 bytes each)

Indices 0–7 are Isaac, Garet, Ivan, Mia, Felix, Jenna, Sheba, Piers. GS1 has only Isaac, Garet, Ivan, Mia and Jenna
filled in; Felix, Sheba and Piers are zero.

| Field | Offset | Notes |
|---|---|---|
| (zero) | 0x00–0x4F | unused in both games |
| HP, PP, Atk, Def, Agi anchors | 0x50, 0x5C, 0x68, 0x74, 0x80 | 6 × u16 each |
| luck anchors | 0x8C | 6 × u8 |
| base elemental | 0x92 | 4 × u8, ×10 scale |
| start level | 0x96 | u16 |
| starting items | 0x98 | 13 × u16, masked `0x1FF` |

**Stat curve (VERIFIED, GS1 `FUN_0807905c`).** Anchor *k* is the stat at level 20·*k*; anchor 0 is the level-1
value. On reaching level *L*: `b = clamp(L/20, 0, 4)` and `gain = (anchor[b+1] - anchor[b] + rand(0..19)) / 20`,
so each level gains 1/20 of the bracket delta, rounded at random.

**Elemental level (VERIFIED, `FUN_080797fc` / `FUN_080798e0`).** `v = djinn_level*10 + base_byte`; level = v/10.
Power = `table[level].power + v%10` and resist = `table[level].resist + v%10`. The level table runs (75,85) at 0,
(80,90) at 1, and so on in steps of 5, up to (150,165) at 15.

Each PC's base bytes are 54 for their own element and 1–3 for the others. Isaac, for example, starts at Venus
level 5 with power 104 / resist 114, and Mercury 78/88, Mars 76/86, Jupiter 77/87.

**Starting class.** There's no class field; the class comes from elemental levels and the class table
(`classes_raw` in characters.json).

**Starting items.** The new-game init gives every item in the list and tries to equip each one (VERIFIED: an
add-then-equip loop over 13 entries).

| PC | Start level | Starting items |
|---|---|---|
| GS1 Isaac | 1 | Machete, Cotton Shirt, Padded Gloves, Herb ×3 |
| GS1 Mia | 10 | Witch's Wand, Travel Robe, Leather Gloves, Wooden Cap, Herb, Antidote, Elixir |
| GS2 Felix | 5 | Short Sword, Cotton Shirt, Padded Gloves, Herb ×2, Shaman's Rod, Mythril Bag |
| GS2 Isaac | 28 | Great Sword, Steel Armor, Knight's Shield, Knight's Helm (the defaults when no save is transferred) |

**Isaac's anchors** (same in both games): HP 30/182/334/486/638/790, PP 20/80/130/170/210/250,
Atk 13/86/162/237/313/388, Def 6/38/69/102/134/166, Agi 8/86/163/241/318/396, Luck 3.

**EXP table** (both games): 0, 24, 67, 144, 283, 519, … up to 8,056,360 at level 99.

## Open questions

- **Class records** are decoded by `gs_abilities` (see `gs_abilities_classes.md`): the Psynergy list is u8 ability +
  u8 level in GS1 and u16 + u16 in GS2, which matches the Squire's known learn levels. (An earlier guess here,
  `ability | level<<9`, was wrong.)
- **Enemy fields still unnamed.** The weakness codes (e.g. 24, 32, 69), the attack-type values, and the GS2 group
  bytes `+0x15..0x17`.
- **Equipped-effect type IDs** (1, 15, 18, 19, …) aren't named.
- **Item type labels** for types 7–11 are guesses.
- **Encounter counts.** GS1's 104 isn't code-bounded. GS2's 110 comes from gsmagic and matches a clean data boundary.
- **Area to encounter-table mapping:** needs the map/script pass.
- **Enemy battle sprites** aren't linked yet; the enemy record has no graphics field, so sprites are probably
  indexed by battle ID in module 12.
- **Elemental damage formula constants:** not extracted (optional).

Sources: gsmagic by adituv (<https://github.com/adituv/gsmagic>, `Editors.cs`) supplied the GS2 enemy, elemental,
group and encounter addresses and the 607/1068 text bases. All of those were confirmed against the ROM code above.
