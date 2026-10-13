# Golden Sun battle mechanics (spec for a native rebuild)

GS2 (The Lost Age, AGFE) is the reference; GS1 (AGSE) differences are noted. Addresses are ROM addresses,
`0x08xxxxxx`. Reference implementation: `gbax\codecs\gs_battle.py`. Its self-test,
`python -m gbax.codecs.gs_battle --selftest`, calls the games' own routines in `gbax.emu.Gba` and compares them with
the Python. The current result is **2,265 comparisons, 0 mismatches** (GS1 764, GS2 1,499).

Evidence labels:

- **VERIFIED-EMU**: the game's routine was run in the emulator and matches the Python.
- **VERIFIED-CODE**: read from the decompiled or disassembled code, not emulated.
- **INFERRED**: a reasoned guess. The reason is given.

The emulator models the IWRAM divide routines as C division that truncates toward zero. They are copied to RAM at
boot: signed GS1 `0x03000380` / GS2 `0x03000528`, unsigned `0x030003F0` / `0x03000534`, reached through the ROM
stubs `0x080022EC` / `0x08002054`. That's the only modelled part.

## 1. Where the code is

| Part | GS1 | GS2 |
|---|---|---|
| Unit/stat module (export stubs at module start) | `0x08077000` | `0x080AD000` |
| Battle logic module | `0x080B5000` | `0x08118000` |
| Execute one action on one target | in `0x080B5000` module (not traced) | `FUN_08120454`; damage-type jump table `0x08120A58` (index = type+1) |
| Effect-id dispatch after damage | not traced | `FUN_08121480`; jump table `*0x08121828` for effects 3..88 |
| Action planning (miss, critical, multi-hit rolls) | `~0x080BEE00` (Ghidra-split) | `0x08124376` (part of the planner reached from `FUN_0812381c`) |

The unit struct is `0x14C` bytes, from `FUN_08016ca4(id)`. Ids `0..7` are the party and `0x80+` are enemies. Its
battle fields (VERIFIED-CODE) are:

| Offset | Field |
|---|---|
| `+0x0F` | level |
| `+0x24` | base (power, resist) × 4 |
| `+0x34` | max HP |
| `+0x36` | max PP |
| `+0x38` | HP |
| `+0x3A` | PP |
| `+0x3C` | Attack |
| `+0x3E` | Defense |
| `+0x40` | Agility |
| `+0x42` | Luck |
| `+0x43` | actions per round |
| `+0x48 + 4e` / `+0x4A + 4e` | battle Power / Resist of element e |
| `+0xD8` | 15 equipment/item slots |
| `+0xF8` | Djinn known (4 × u32 bitmasks) |
| `+0x108` | Djinn set (4 × u32) |
| `+0x118` / `+0x11C` | known / set counts |
| `+0x124` | EXP |
| `+0x129` | class (0 means enemy) |
| `+0x12B` | guard state |
| `+0x12C..+0x148` | statuses and buffs (section 7) |
| `+0x14A` | character / enemy id |

## 2. Elemental Power and Resist

**PCs** (`FUN_080b0084` GS2 / `FUN_080798e0` GS1, VERIFIED-CODE). Each element has a level in tenths, v. It comes
from the class and Djinn code (`FUN_080affac`). From v:

- `L = clamp(v // 10, 0, 15)`
- `rem = v − 10·(v // 10)`
- Power = `T[L].power + rem` and Resist = `T[L].resist + rem`

The table T is at GS2 `0x080C6644` and GS1 `0x08088DF8`. It's identical in both games (VERIFIED-EMU by reading
the ROM bytes in the self-test). L 0..15 gives:

- Power: 75, 80, …, 150 (+5 per level).
- Resist: 85, 90, …, 145, then 160, 165.

**Enemies** copy four (power, resist) pairs from their elemental-data record. The index is enemy `+0x2A`; the records
are 24 bytes at GS2 `0x080C6684 + 8`.

Equipment and buffs then give the battle values at `+0x48`.

## 3. The elemental multiplier

`F(diff, half)` (GS2 `0x080B02DC`, GS1 `0x08079B24`, VERIFIED-EMU over diff −260..260 for both modes) uses:

- `diff = attacker Power[e] − target Resist[e]`, clamped to [−200, 200]. diff is 0 for neutral (element 4) actions.
- `F = 256 + y(diff)`, where y is linear interpolation in the table at GS2 `0x080C6B04` (GS1 `0x08089258`):
  (200, 256), (100, 128), (0, 0), (−100, −128), (−200, −256).

That makes `F = 256·(1 + diff/200)`, from 0× to 2×. With `half`, y is divided by 2 first, giving
`256·(1 + diff/400)`, from 0.5× to 1.5×. The integer steps are exact in the Python.

## 4. Damage and healing by ability damage type

The type is the low nibble of ability byte 1 (`gs_abilities` damage types). The handlers below are in GS2
`FUN_08120454`; the entry for type t is jump-table index t+1.

| Type | Handler | Rule |
|---|---|---|
| 0 | `0x08121480` | effects only |
| 1 healing | `0x08120DCE` | 4.4 |
| 2 effect_only | `0x08121304` | no HP change, effect dispatch |
| 3 added_damage, 4 multiplier | `0x08120A8C` | 4.1 |
| 5 base_damage, 6 base_damage_alt, 8 summon | `0x08120F70` | 4.2 |
| 7 djinn_effect, 9 utility | `0x08121480` | effect only |
| 10 psynergy_drain | `0x08120CE2` | 4.5 |
| 11 psynergy_recovery | `0x08121278` | 4.6 |

Per-target values are precomputed by the planner into the action record. They are:

- `hits`: action `+0x1F+i` in GS2, `+0x1E+i` in GS1. Default 1; 0 means a miss.
- `crit`: action `+0x2D+i` in GS2, `+0x2C+i` in GS1.
- `effect landed`: action `+0x3B+i`.
- `distance`: the absolute offset from the centre target, `+0x11+i`.

### 4.1 Attack, added damage and multiplier (types 3 and 4), VERIFIED-CODE (core VERIFIED-EMU)

1. If the target's guard state is 4, there's no damage.
2. Set `Def = target Defense`. Effect 35 landing halves it; effects 90 and 91 set it to 0.
3. Compute `diff` from section 3. The element is the ability's, or for a plain Attack the weapon's (`0x080B0434`).
4. Compute the base:
   - **Type 3:** `core(Atk, Def, power, diff) = (max(Atk−Def, 0) + 2·power) · F(diff, half) >> 9`, floored at 0.
     That's `((Atk−Def)/2 + power)·(1 + diff/400)`. The core is GS2 `0x080B03AC` / GS1 `0x08079BF8`
     (VERIFIED-EMU). Attack is ability 1, type 3, with power 0.
   - **Type 4:** `core(Atk, Def, 0, diff) · power / 10`.
5. Multiply by `hits`.
6. **Critical:** multiply by 5/4 (crit 1) or 3/2 (crit 2), then add the **target's** `level/5 + 6` (GS2 `0x08120B6A`–`0x08120B7C` reads it from the target unit). Only when crit ≠ 0.
7. **Variance:** add `rand & 3` (0..3), from the battle RNG (section 9).
8. **Guard:** state 1 is ÷2, state 2 is ×2/5, state 3 is ÷10.
9. Floor the result at **1**.
10. Effect 34 landing: if damage < HP−1, set damage to HP−1, leaving the target at 1 HP.

### 4.2 Psynergy base damage (types 5, 6 and 8), VERIFIED-CODE (core VERIFIED-EMU)

1. If the guard state is 4, there's no damage.
2. **GS2 summon bonus:** `power += min(target max HP, 10000) · pct / 100`. It applies to the listed summon ids when
   the action type is 6 or 10, and always to enemy abilities 673, 683 and 724. pct comes from the compare chain at
   `0x08120FE2..0x08121106` (VERIFIED-EMU for all 735 ids) and is given in the table below.
3. Base: `power · F(diff) · 256 >> 16`, which is `power·(1 + diff/200)`. GS2 `0x080B03E0` / GS1 `0x08079C30`,
   VERIFIED-EMU.
4. Multiply by `hits`.
5. **Spread:** multiply by the percentage for the target's distance, ÷100 (table below).
6. Add `rand & 3`.
7. Apply the guard reduction as in 4.1. **There's no minimum of 1** here.

GS2 summon HP bonus (pct):

| Summons | pct |
|---|---|
| Venus, Mercury, Mars, Jupiter | 3 |
| Ramses, Nereid, Kirin, Atalanta, Zagan, Megaera | 6 |
| Daedalus (id 402) | 7 |
| Cybele, Neptune, Tiamat, Procne, Moloch, Flora | 9 |
| Judgment, Boreas, Meteor, Thor, Ulysses | 12 |
| Haures, Eclipse, Daedalus (id 403) | 15 |
| Azul | 21 |
| Catastrophe | 24 |
| Charon | 30 |
| Iris | 40 |
| Enemy abilities: Star Mine, Meteor Blow, Cruel Ruin | 30, 35, 40 |

Coatlicue (heal) gets none. **GS1 has no HP bonus**: the `10000` cap sequence doesn't occur anywhere in GS1 code
(byte search; INFERRED absent).

Spread by distance 0..5 (VERIFIED-CODE, GS2 tables):

| Use | Table | Distance 0..5 (%) |
|---|---|---|
| Type 5 | `0x081288E8` | 100, 80, 60, 40, 20, 10 |
| Type 8 summon | `0x08128900` | 100, 70, 40, 30, 20, 10 |
| Type 6 | `0x08128918` | 100, 50, 30, 10, 10, 10 |
| Heal | `0x081288B8` | 100, 80, 60, 40, 20, 10 |
| PP drain | `0x081288A0` | 100, 50, 30, 10, 10, 10 |
| Status chance | `0x08128898` | 100, 60, 30, 30, 30, 30 |

### 4.3 Special battle modes (VERIFIED-CODE)

These come from battle type `0x02000240+0x24B` and story flags:

- Battle type 6, or flag `0x16E` with action type 6 (types 5/6/8) or 5 (types 3/4): damage is raised to the target's
  HP (a scripted kill).
- `FUN_081203a8(target)` true: the target can't drop below 1 HP.
- Battle type 6: a type 5/6/8 hit sets HP to 0.

### 4.4 Healing (type 1), VERIFIED-CODE (core VERIFIED-EMU)

A downed target (HP 0) gets nothing. Otherwise:

- Base: `heal_core(power, P) = power · F(2P − 200) · 256 >> 16`, which is `power · P / 100` (GS2 `0x080B0408` /
  GS1 `0x08079C5C`).
- P is the caster's Power in the ability's element. It's 100 for neutral abilities and for item use (action type 2).
- Then multiply by the heal spread ÷100, multiply by `hits`, add `rand & 3`, and cap at max HP.

### 4.5 PP drain (type 10), VERIFIED-CODE

- Damage: `power · F(diff)/256`, times the PP-drain spread ÷100, times `hits`, with the guard reduction applied,
  capped at the target's PP. It's subtracted from the target's PP.
- Effect 32 ("Psy Drain") switches a type 3/5 action to this handler when the target has PP.
- The user's gain goes through `0x080AD0D0` → `0x080AEA31` (INFERRED: credits the user).

### 4.6 PP recovery (type 11), VERIFIED-CODE (partly)

Uses `heal_core` on PP with the same structure as healing (`0x08121278`). The exact spread table wasn't traced.

## 5. Hit, miss, critical, multi-hit and unleash (planner GS2 `0x08124376`, GS1 `~0x080BEE00`), VERIFIED-CODE

- **Plain Attack, miss:** a miss is only possible while the target can act (no sleep `+0x13C`, stun `+0x13B`,
  `+0x145` or `+0x13A`).
  - If the attacker is deluded (`+0x138`), the attack misses when `rand8 < 0x99`, about 60%.
  - Otherwise it misses when `(rand & 31) == 0`, 1/32.
  - Flag `0x16E` forces a miss.
- **Plain Attack, critical** (target alive): a critical happens when `(rand & 31) == 0`. Otherwise it happens when
  `rand16 < X·65536/200`. X is the sum of equipped "Criticals up" values (equip effect 23; `FUN_080b0460`, export
  stub `0x080AD2C0`). Examples: Warrior's Helm 10, Hyper Boots 12, Valkyrie Mail 20. Crit kind 1 then applies
  ×5/4 + target level/5 + 6.
- **Effects 36..40** give crit kind 2 (×3/2 + target level/5 + 6) to every target with probability 1/64, 1/32, 1/16, 1/8
  and 1/4. No GS2 ability uses them; they're kept for items or unused.
- **Multi-hit effects** add to `hits` (×2 means +1) for every target:

  | Effect | Chance | Hits added |
  |---|---|---|
  | 41 | 12.5% | +1 |
  | 42 | 25% | +1 |
  | 43 | 12.5% | +2 |
  | 44 | 25% | +2 |
  | 65 | 60% | +1 |
  | 68 | 60% | +2 |
  | 89 | 70% then +1, or 50% then +2 | |

- **Unleash** (`FUN_080b04bc`, reached through stub `0x080AD108` from `0x08123C0C`): PCs only. The weapon has an
  unleash ability at item `+0xE` and a rate byte at `+0xB` (7 on most weapons, 8 on Masamune, Cloud Brand,
  Atropos' Rod and Lachesis' Rule). The chance is `(X + 5·rate)` percent, rolled as
  `rand16 < chance·65536/100`. On success the Attack becomes the unleash ability.

## 6. Turn order (VERIFIED-CODE unless noted)

Round setup is `FUN_0811d61c`. Party commands come from the battle menu, `0x080381C0` in module `0x08038000`. Enemy
actions come from `FUN_0811cfd0`. Then a stable descending bubble sort on priority, `FUN_0811d160`.

- **Party priority:** set by the menu module. Raw Agility is INFERRED; the menu module wasn't decompiled.
- **Enemies:**
  - The list is shuffled with 32 random swaps.
  - Each enemy acts `+0x43` times. Priorities by number of actions:

    | Actions | Priorities |
    |---|---|
    | 2 | Agi, Agi/2 |
    | 3 | Agi, 3·Agi/4, Agi/2 |
    | 4 | Agi, 5·Agi/6, 4·Agi/6, Agi/2 |

    (`enemy_action_priorities`)
  - A sleeping or stunned enemy's actions become no-ops.
- **First-in-round actions:** +10000 priority for actions whose effect is 46, 47, 53, 72, 74, 76, 79 or 88. These
  are Defend/Granite, Flash/Total Defense, Cage/Ground, Shade, Counter-rush, Breath, Haze and Guard Aura, which
  matches the wiki's "activate first" list.
- **No random agility factor** in the normal path. A random factor (enemies `Agi/2 + rand(Agi)`, party raw Agility)
  exists only in the alternate builder `FUN_0811c3bc` (GS1 `FUN_080b8574`), used when flag `0x16A` is set.
- **Battle start** (`FUN_081197f0`):
  - 1/16: **first strike**. Enemies don't act in round 1 and fleeing always succeeds.
  - Otherwise 1/32: **ambush**. The party can't act; `max(2, 1d5)` enemies act once each.
  - Neither happens with flag `0x16E` or a special battle type.
- **Action types** (action `+0x4A`): 1 attack, 2 item, 3 defend, 5 Psynergy/ability, 6 summon, 7 (a second guard
  type), 99 flee. Action types 3 and 7 set guard state 1 and 3 when the round starts.

## 7. Status effects and effect ids

Status chance is `FUN_080b075c` (GS2, VERIFIED-CODE), called through stub `0x080AD120`.

1. **Pre-checks.** Effects 90/91 only work on the enemy ids in two lists: 47 ids at `*0x080B06C4` and 29 at
   `*0x080B06E4`. Revive effects (5, 56, 57, 73) fail on a living target. Cure effects fail if there's nothing to
   cure.
2. **Luck immunity.** Luck ≥ 40 makes the target immune to effects 18, 19, 26, 27, 28, 34, 80 and 82. PCs are
   immune to 82.
3. **Base chance.** `FUN_080b0514` (VERIFIED-EMU for ids 0..91, both games) returns a base, or a negative value for
   a fixed chance.
4. **Variable chance.**
   `chance = base + (attacker elemental level − target elemental level − targetLuck/2)·3 + 25 if the effect is in the
   target's weakness list`. The levels are in the ability's element (`FUN_080b0028`, v//10). The weakness list is
   enemy `+0x3E` or class `+0x50`.
5. **Roll.** It lands if `rand100 ≤ chance · statusSpread[distance] / 100`, so even a chance of 0 lands 1% of the
   time. Effects 67, 80 and 85 get 3 tries.

Effect table: names INFERRED from the abilities that carry them and their descriptions; base chance VERIFIED-EMU; F
means fixed. "F100" is 100%, unaffected by levels.

| Id | Base | Meaning | Id | Base | Meaning |
|---|---|---|---|---|---|
| 3 | F100 | cure poison/venom | 4 | F100 | Restore (sleep, stun, delusion…) |
| 5 | F100 | revive | 6/7 | F100 | Attack up one/party |
| 8/9 | 60 | Attack down one/party | 10/11 | F100 | Defense up |
| 12/13 | 70 | Defense down | 14/15 | F100 | Resist up |
| 16/17 | 75 | Resist down | 18 | 55 | poison (`+0x131`=1) |
| 19 | 55 | venom (`+0x131`=2) | 20 | 65 | delusion (`+0x138`) |
| 21 | 35 | confuse | 22 | 30 | charm |
| 23 | 40 | stun (`+0x13B`) | 24 | 45 | sleep (`+0x13C`) |
| 25 | 55 | Psynergy seal (`+0x140`) | 26 | 25 | haunt |
| 27 | 20 | instant death (Charon) | 28 | 60 | Grim Reaper curse (`+0x141`) |
| 29 | F100 | regenerate | 30 | F100 | reflect |
| 31 | 65 | drain HP | 32 | 60 | drain PP (type 10 switch) |
| 33 | F100 | Break (remove buffs) | 34 | 35 | leave target at 1 HP |
| 35 | 50 | halve Defense for the hit | 36–40 | – | crit kind 2, 1/64..1/4 |
| 41–44, 65, 68, 89 | – | multi-hit (section 5) | 45 | F100 | misc (Element Swap, Threaten…) |
| 46 | F100 | Defend/Granite, guard 1 (÷2) | 47 | F100 | Flash/Total Defense, guard 2 (×2/5) |
| 53 | F100 | hold a foe (goes first) | 55 | F100 | self-KO attack |
| 56 | F60 | revive 60% (Quartz) | 57 | F90 | revive 90% (Dew) |
| 58/59 | F100 | Agility down/up | 60 | F100 | steal HP |
| 61/62/70/71/76 | F100 | Djinn heals | 63/77/78 | F100 | restore PP |
| 64 | F100 | cure status | 66 | F100 | Kite: act twice next round |
| 67 | F100 | seal Psynergy (3 tries) | 69 | F100 | PP leech |
| 72 | F100 | Shade | 73 | F70 | revive all 70% |
| 74 | F100 | Counter-rush | 79 | F100 | Haze, guard 4 (no damage) |
| 80 | 60 | Grim Reaper (Gasp, 3 tries) | 81 | F100 | Lull (cease-fire) |
| 82 | 40 | Gale | 83 | 50 | Ulysses |
| 84 | F100 | Catastrophe | 85 | 40 | stun (Fire Puppet, 3 tries) |
| 88 | F100 | Guard Aura | 90/91 | F100 | bane vs listed enemies, Defense ignored |

**Buffs** (VERIFIED-CODE from the AI usefulness checks in `FUN_0811f66c`):

- Attack: turns at `+0x132`, level at `+0x133`.
- Defense: `+0x134` / `+0x135`.
- Resist: `+0x136` / `+0x137`.
- Levels are capped at ±4.
- `+0x12C..+0x12F` are further positive buffs that Break also clears.

**Losing a turn** (`FUN_0812381c`): `+0x145`, sleep and stun skip the turn. Bit 0 of `+0x130` skips 1/4 of turns.

**GS1 differences:** effects 73, 80, 82, 83 and 85 are fixed 100% in GS1 (they're GS2 additions). All other base
chances are identical (VERIFIED-EMU).

## 8. Djinn: Set, Standby, Recovery and summons (GS2, VERIFIED-CODE)

**State.** Per unit, the `+0xF8` known and `+0x108` set bitmasks. Per side, there's a Djinn list from
`0x080AD000`/`FUN_080ad348`, with entries at `+8` (4 bytes each: element, index, owner, state) and the count at
`+0x128`. The state byte means:

| State | Meaning |
|---|---|
| `0xFF` | Standby (counts toward summons; `FUN_080b0ef4` counts them per element) |
| `0xFE` | just spent on a summon |
| `n > 0` | recovering, turns left |

**At battle start** (`FUN_08118eb0`), every known-but-unset Djinni is added as Standby.

**Unleash.**
- The Djinni's ability record runs: types 4, 7 and others, for example Flint is a ×1.6 multiplier.
- The Djinni is removed from the unit's set mask (`0x080AD160`) and appended as Standby (`FUN_080b0e04`).
- Stats and class are recomputed. **The class changes immediately** (`FUN_080ad008` → class selection
  `0x080B0144`).

**Summon.**
- It needs `cost[e]` Standby Djinn of each element (summon record `u8 cost[4]`).
- The chosen Standby Djinn become `0xFE`.
- Then, **per owner**, they get recovery countdowns `start, start+1, …`, where `start` is the owner's highest
  existing countdown + 1, at least 2 (loop at GS2 `0x08125518`, `djinn_recovery_countdowns`).

**Recovery.**
- Each time an owner's turn comes up, their countdowns drop by 1 (`FUN_08124cc4`; owner alive).
- A Djinni at 0 is **Set again**, with the message and a class recompute.
- So each Adept regains **one Djinni per turn, starting on their second turn after the summon**. INFERRED from the
  countdown arithmetic; not observed live.
- Between battles, `FUN_08124bfc` does the same tick for all owners.

**Summon damage** uses section 4.2: type 8, the caster's Power in the summon's element, the summon spread and the
GS2 HP bonus.

## 9. Randomness

The **battle RNG** (`FUN_080b0378` GS2, state `0x020054C8`; `FUN_08079bc4` GS1, state `0x020023A8`; VERIFIED-EMU):

- `state = state·0x41C64E6D + 0x3039`
- `rand16 = (state & 0xFFFFFF) >> 8`
- `rand100 = rand16·100 >> 16`

It's used for damage variance, criticals, misses, status, unleash and Djinn picks.

The **kernel RNG** `FUN_08014878` (16-bit output; checked by emulation, range `0x18..0xFFFD`) is used for the enemy
shuffle, target choice, flee, the battle-start roll and rewards. Its algorithm isn't reproduced.

## 10. Fleeing (GS2 `FUN_0811ce94` + `FUN_0811c66c`; GS1 `FUN_080b90f8`, same structure, scale 10000), VERIFIED-CODE

1. If it's the first-strike round, the flee succeeds.
2. If it's a boss battle (battle type 2), it fails.
3. Otherwise compute
   `p = 5000 + 500·avg(party levels) − 500·avg(enemy levels) + 2000·(previous attempts this battle)` (out of
   10000). It succeeds if `rand(10000) < p`, and the attempt counter (`+0x46`) increments.
   - On failure, the round becomes an ambush round.
   - On success, the run still fails 1 time in 16 ("But they can't get away!").

## 11. Rewards (GS2 `FUN_0812824c`, distribution `FUN_081284c0`; GS1 `FUN_080c24f0`)

**Per enemy defeated:**
- EXP: enemy `+0x48` (GS2) is added to battle state `+0x554`.
- Coins: enemy `+0x42` is added to `+0x550`.
- The kill is recorded as flag `0x600 + id`.

**Extra-reward mode** (battle state `+0x850` nonzero; GS2 only, INFERRED absent in GS1):
- EXP becomes `base + max(Σ(level/10 + 1)×1d4, 3·base/10)`.
- Coins become `base + max(Σ(level/10 + 1)×1d6, 3·base/10)`.

**Item drop.** The chance is `rand16 < 0x20000 >> r`, where r is the drop rate code (r − 2 in extra mode). The
dropped item replaces the cheapest of 4 candidate slots if it's worth more.

**EXP distribution.**
- Members in the battle get the **full** total each; it isn't divided.
- In GS2, party members outside the battle get **half** (`>> 1`).
- GS1 has a single branch (4-member party), at battle state `+0x534`.

Enemy record fields are in `gs_units_items.md`.

## 12. How each part was validated

| Item | Method | Result |
|---|---|---|
| F(diff), physical, Psynergy and heal cores (both games) | emulated vs Python over grids (174 + 216 + 70 + 18 per game) | all match |
| Battle RNG (both games) | emulated, 4 seeds × 5 draws, value and state | all match |
| Status base chances (ids 0..91, both games) | emulated `0x080B0514` / `0x08079D7C` | GS2 matches; GS1 differs only on GS2-only effects |
| GS2 summon HP% (735 ids) | emulated the compare chain | matches the table |
| Elemental level table (both games) | ROM bytes | identical |
| Wiki cross-check | <https://goldensunwiki.net> (Avalanche, Spout) | same forms: Psynergy `base·(1 + (Pow−Res)/200)`, physical-elemental `((Atk−Def)/2 + add)·(1 + (Pow−Res)/400)` |

The wiki's Avalanche example (base 160, Power 150, Resist 50) gives `psy_core(160, 100) = 240` (VERIFIED by the
Python, which the emulator matches).

## Open questions

- Party turn priority is set in the battle-menu module (`0x08038000`), which wasn't decompiled. Raw Agility is
  INFERRED; check whether there's a random factor.
- GS1's action executor and its jump tables weren't traced individually. Its leaf formulas are identical
  (VERIFIED-EMU), and its planner has the same miss and critical rolls.
- Exact PP-recovery (type 11) spread, the user-side PP gain of drains, and the meaning of `+0x145` and of the
  0x130 bit.
- The Djinn recovery timing is from code reading. A live check in mGBA (summon with 3 Djinn, count the turns) would
  confirm "one per turn from the second turn".
- What sets the extra-reward flag `+0x850`.
