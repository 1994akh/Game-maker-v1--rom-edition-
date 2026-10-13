"""Golden Sun battle rules: a small pure-Python reference implementation of the formulas, ported from the ROM code.

GS2 (The Lost Age, AGFE) is the primary target; GS1 (AGSE) uses the same formulas unless a docstring says
otherwise. Every function cites the game routine it reproduces. The full spec, with evidence levels, is in
notes/gs_battle_mechanics.md.

Integer maths follows the ARM code exactly: C division truncates toward zero (``_div``), and ``>> n`` after a
"+ (2^n - 1) if negative" bias is also truncation toward zero.

Self-test (calls the games' own routines in gbax.emu.Gba and compares):
    python -m gbax.codecs.gs_battle --selftest [GS1_ROM] [GS2_ROM]
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

# --------------------------------------------------------------------------------------------------------------
# Addresses (GS1 / GS2). "core" routines are leaf functions that the self-test calls in the emulator.
# --------------------------------------------------------------------------------------------------------------
ADDR = {
    "gs1": {
        "elem_multiplier": 0x08079B24,   # F(diff, half)
        "physical_core": 0x08079BF8,     # (max(atk-def,0) + 2*add) * F(diff,1) >> 9
        "psy_core": 0x08079C30,          # power * F(diff,0) * scale >> 16
        "heal_core": 0x08079C5C,         # power * F(2P-200,0) * scale >> 16
        "rng": 0x08079BC4, "rng_state": 0x020023A8,
        "rand100": 0x08079BE8,
        "attack_element": 0x08079C8C,
        "status_base_chance": 0x08079D7C,
        "elem_level_table": 0x08088DF8,  # 16 x (s16 power, s16 resist)
        "multiplier_table": 0x08089258,
        "flee_scale": 0x080B9200,        # literal 10000
    },
    "gs2": {
        "elem_multiplier": 0x080B02DC,
        "physical_core": 0x080B03AC,
        "psy_core": 0x080B03E0,
        "heal_core": 0x080B0408,
        "rng": 0x080B0378, "rng_state": 0x020054C8,
        "rand100": 0x080B039C,
        "attack_element": 0x080B0434,
        "crit_bonus_sum": 0x080B0460,    # sum of equipped "Criticals up" (equip effect 23) values
        "unleash_roll": 0x080B04BC,
        "status_base_chance": 0x080B0514,
        "status_chance": 0x080B075C,
        "revive_effect": 0x080B0740,
        "elem_level_table": 0x080C6644,
        "multiplier_table": 0x080C6B04,
        "elem_from_levels": 0x080B0084,
        "action_execute": 0x08120454,    # damage-type jump table at 0x08120A58
        "effect_dispatch": 0x08121480,   # effect-id jump table (effects 3..88) at *0x08121828
        "summon_bonus_block": (0x08120FE2, 0x08121106),
        "action_plan_attack": 0x08124376,  # miss / critical / multi-hit rolls
        "turn_order_enemies": 0x0811CFD0, "turn_order_sort": 0x0811D160, "round_setup": 0x0811D61C,
        "flee_chance": 0x0811CE94, "flee_run": 0x0811C66C,
        "djinn_recover_tick": 0x08124CC4, "djinn_list_add_standby": 0x080B0E04,
        "reward": 0x0812824C, "reward_distribute": 0x081284C0,
    },
}

ELEMENTS = ("Venus", "Mercury", "Mars", "Jupiter", "Neutral")

# Piecewise-linear multiplier table (x, y) at GS2 0x080C6B04 / GS1 0x08089258: 256 + y = 256 * (1 + x/200).
MULT_TABLE = ((200, 256), (100, 128), (0, 0), (-100, -128), (-200, -256))

# Elemental level -> (power, resist) at GS2 0x080C6644 / GS1 0x08088DF8 (identical in both games).
ELEM_LEVEL_TABLE = ((75, 85), (80, 90), (85, 95), (90, 100), (95, 105), (100, 110), (105, 115), (110, 120),
                    (115, 125), (120, 130), (125, 135), (130, 140), (135, 145), (140, 150), (145, 160), (150, 165))

# Fall-off by distance from the centre target (index = |offset|), percent. GS2 addresses.
SPREAD = {
    "status": (100, 60, 30, 30, 30, 30),        # 0x08128898 (status-effect chance)
    "pp_drain": (100, 50, 30, 10, 10, 10),      # 0x081288A0 (type 10)
    "heal": (100, 80, 60, 40, 20, 10),          # 0x081288B8 (type 1)
    "type5": (100, 80, 60, 40, 20, 10),         # 0x081288E8 (base damage)
    "summon": (100, 70, 40, 30, 20, 10),        # 0x08128900 (type 8)
    "type6": (100, 50, 30, 10, 10, 10),         # 0x08128918 (enemy "breath" base damage)
}

# GS2 summon bonus: + min(target max HP, 10000) * pct / 100 added to the base power (ability id -> pct).
# Emulated from the compare chain at 0x08120FE2..0x08121106. GS1 has no such code (pattern absent).
SUMMON_HP_PERCENT_GS2 = {
    380: 3, 381: 6, 382: 9, 383: 12, 384: 6, 385: 15, 386: 30,            # Venus Ramses Cybele Judgment Zagan Haures Charon
    388: 3, 389: 6, 390: 9, 391: 12, 392: 9, 394: 21,                      # Mercury Nereid Neptune Boreas Moloch Azul
    396: 3, 397: 6, 398: 9, 399: 12, 400: 6, 401: 12, 402: 7, 403: 15, 404: 40,  # Mars Kirin Tiamat Meteor Megaera Ulysses Daedalus(x2) Iris
    406: 3, 407: 6, 408: 9, 409: 12, 410: 9, 411: 15, 412: 24,             # Jupiter Atalanta Procne Thor Flora Eclipse Catastrophe
    673: 30, 683: 35, 724: 40,                                             # enemy: Star Mine, Meteor Blow, Cruel Ruin
}

# Status/effect base chance (FUN_080b0514). Negative = fixed chance that ignores levels and luck.
_BASE_CHANCE = {8: 60, 9: 60, 0x1C: 60, 0x20: 60, 0x50: 60, 0xC: 70, 0xD: 70, 0x10: 75, 0x11: 75, 0x12: 55,
                0x13: 55, 0x19: 55, 0x14: 65, 0x1F: 65, 0x15: 35, 0x22: 35, 0x16: 30, 0x17: 40, 0x52: 40, 0x55: 40,
                0x18: 45, 0x1A: 25, 0x1B: 20, 0x23: 50, 0x53: 50, 0x38: -60, 0x39: -90, 0x49: -70}


def status_base_chance(effect: int) -> int:
    """Base chance (percent) of effect id `effect`; negative means fixed (GS2 0x080B0514, GS1 0x08079D7C)."""
    return _BASE_CHANCE.get(effect, -100)


# Effect ids (byte 3 of the ability record). Names INFERRED from the abilities that carry them and their in-game
# descriptions; chances VERIFIED (emulated FUN_080b0514); status-byte offsets VERIFIED where given (unit struct).
EFFECTS = {
    0: "none", 3: "cure poison/venom (+0x131)", 4: "Restore: cure sleep, stun, delusion etc.", 5: "revive (100%)",
    6: "Attack up (one)", 7: "Attack up (party)", 8: "Attack down (one)", 9: "Attack down (party)",
    10: "Defense up (one)", 11: "Defense up (party)", 12: "Defense down (one)", 13: "Defense down (party)",
    14: "Resist up (one)", 15: "Resist up (party)", 16: "Resist down (one)", 17: "Resist down (party)",
    18: "poison (+0x131=1)", 19: "venom (+0x131=2)", 20: "delusion (+0x138)", 21: "confuse", 22: "charm",
    23: "stun (+0x13b)", 24: "sleep (+0x13c)", 25: "Psynergy seal (+0x140)", 26: "haunt", 27: "instant death",
    28: "curse: Grim Reaper countdown (+0x141)", 29: "regenerate HP", 30: "reflect", 31: "drain HP to user",
    32: "drain PP to user (switches the action to type 10 if the target has PP)", 33: "Break: remove buffs",
    34: "on success raise damage to leave the target at 1 HP", 35: "on success halve target Defense for the hit",
    36: "critical (x1.5 kind) 1/64", 37: "critical 1/32", 38: "critical 1/16", 39: "critical 1/8",
    40: "critical 1/4", 41: "12.5%: damage x2", 42: "25%: damage x2", 43: "12.5%: damage x3", 44: "25%: damage x3",
    45: "misc enemy tricks (Element Swap, Threaten...)", 46: "Defend / Granite: guard state 1 (damage /2)",
    47: "Flash / Total Defense: guard state 2 (damage x2/5)", 53: "hold a foe (Cage, Ground): goes first",
    55: "self-KO attack (user downed)", 56: "revive 60% (Quartz)", 57: "revive 90% (Dew)",
    58: "Agility down", 59: "Agility up", 60: "steal HP", 61: "heal (Djinni)", 62: "heal party (Djinni)",
    63: "restore PP (Ember)", 64: "cure status (Salt, Tonic)", 65: "60%: damage x2", 66: "Kite: act twice next round",
    67: "seal Psynergy (Djinni)", 68: "60%: damage x3", 69: "PP leech", 72: "Shade: shield (goes first)",
    73: "revive all 70%", 74: "Counter-rush (goes first)", 76: "Breath: quick heal (goes first)",
    79: "Haze: guard state 4 (no damage, goes first)", 80: "Grim Reaper (Gasp)", 81: "Lull: cease-fire",
    82: "Gale: blow away (40%)", 83: "Ulysses", 84: "Catastrophe", 85: "stun (Fire Puppet)",
    88: "Guard Aura: guard state (goes first)", 89: "70%: damage x2, 50%: x3 (Vengeance)",
    90: "bane: only works on enemy list A (47 ids at *0x080B06C4); target Defense ignored",
    91: "bane: only works on enemy list B (29 ids at *0x080B06E4); target Defense ignored",
}

# Effects whose action gets +10000 priority (acts first in the round), FUN_0811d160.
FIRST_STRIKE_EFFECTS = frozenset({72, 76, 79, 74, 46, 47, 88, 53})


def _div(a: int, b: int) -> int:
    """C integer division (truncate toward zero), as the game's divide routine."""
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


# --------------------------------------------------------------------------------------------------------------
# Core formulas (validated against the ROM routines by --selftest)
# --------------------------------------------------------------------------------------------------------------
def elem_multiplier(diff: int, half: bool = False) -> int:
    """Elemental multiplier in 1/256 units: 256 * (1 + diff/200), or (1 + diff/400) when half.

    diff = attacker elemental Power - target elemental Resist, clamped to [-200, 200] (so 0x..2x / 0.5x..1.5x).
    Port of GS2 FUN_080b02dc / GS1 FUN_08079b24 (piecewise-linear lookup in MULT_TABLE).
    """
    d = max(MULT_TABLE[-1][0], min(MULT_TABLE[0][0], diff))
    i = 1
    while i <= 4 and d <= MULT_TABLE[i][0]:
        i += 1
    if i == 5:
        y = MULT_TABLE[4][1]
    else:
        (x0, y0), (x1, y1) = MULT_TABLE[i - 1], MULT_TABLE[i]
        y = _div((y0 - y1) * (d - x1), x0 - x1) + y1
    if half:
        y = _div(y, 2)
    return y + 0x100


def physical_core(atk: int, defense: int, added: int, diff: int) -> int:
    """Physical damage before crits/variance: (max(atk-def, 0) + 2*added) * F(diff, half) / 512, floored at 0.

    i.e. ((Atk - Def)/2 + added) * (1 + diff/400). GS2 FUN_080b03ac / GS1 FUN_08079bf8.
    """
    base = max(atk - defense, 0)
    v = (base + added * 2) * elem_multiplier(diff, True)
    v = _div(v, 512) if v < 0 else v >> 9
    return max(v, 0)


def psy_core(power: int, diff: int, scale: int = 256) -> int:
    """Psynergy base damage: power * F(diff) * scale / 65536 = power * (1 + diff/200) when scale is 256.

    GS2 FUN_080b03e0 / GS1 FUN_08079c30 (callers always pass scale 256).
    """
    v = elem_multiplier(diff) * power * scale
    return (v + 0xFFFF) >> 16 if v < 0 else v >> 16


def heal_core(power: int, elem_power: int, scale: int = 256) -> int:
    """Healing: power * F(2P - 200) * scale / 65536 = power * P / 100 for P in [0, 200]. GS2 FUN_080b0408."""
    v = elem_multiplier(elem_power * 2 - 200) * power * scale
    return (v + 0xFFFF) >> 16 if v < 0 else v >> 16


class BattleRng:
    """The battle RNG (GS2 FUN_080b0378, GS1 FUN_08079bc4): 32-bit LCG, returns 16 bits.

    state = state * 0x41C64E6D + 0x3039; return (state & 0xFFFFFF) >> 8. State word GS2 0x020054C8, GS1 0x020023A8.
    rand100() = rand16 * 100 >> 16 (GS2 FUN_080b039c). Turn order, flee, AI and rewards use a second, kernel
    generator (FUN_08014878, also 16-bit) that is not reproduced here.
    """

    def __init__(self, state: int = 0):
        self.state = state & 0xFFFFFFFF

    def rand16(self) -> int:
        self.state = (self.state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
        return (self.state & 0xFFFFFF) >> 8

    def rand100(self) -> int:
        return (self.rand16() * 100) >> 16


def elemental_power_resist(level_x10: int) -> tuple[int, int]:
    """(Power, Resist) of one element for a PC from its elemental level in tenths (GS2 FUN_080b0084).

    L = clamp(level_x10 // 10, 0, 15); both values add the remainder level_x10 - 10*(level_x10//10).
    Enemies copy (power, resist) from their elemental-data record instead (0x18-byte records at GS2 0x080C6684).
    """
    q = _div(level_x10, 10)
    rem = level_x10 - q * 10
    L = max(0, min(15, q))
    p, r = ELEM_LEVEL_TABLE[L]
    return p + rem, r + rem


# --------------------------------------------------------------------------------------------------------------
# Composed rules (from the handlers in GS2 FUN_08120454; see the notes for the per-step evidence)
# --------------------------------------------------------------------------------------------------------------
@dataclass
class Unit:
    hp: int = 100
    max_hp: int = 100
    pp: int = 20
    max_pp: int = 20
    attack: int = 50
    defense: int = 30
    agility: int = 30
    luck: int = 5
    level: int = 10
    power: tuple = (100, 100, 100, 100)    # per element, battle values at +0x48 + 4e
    resist: tuple = (100, 100, 100, 100)   # +0x4A + 4e
    guard: int = 0                         # +0x12B: 0 none, 1 Defend (/2), 2 (x2/5), 3 (/10), 4 immune


def _diff(att: Unit, tgt: Unit, element: int) -> int:
    return 0 if element >= 4 else att.power[element] - tgt.resist[element]


def _guard(dmg: int, guard: int) -> int:
    if guard == 1:
        return _div(dmg, 2)
    if guard == 2:
        return _div(dmg * 2, 5)
    if guard >= 3:
        return _div(dmg, 10)
    return dmg


def attack_damage(att: Unit, tgt: Unit, element: int = 4, added: int = 0, multiplier_x10: int | None = None,
                  crit: int = 0, hits: int = 1, rand2: int = 0, defense_mode: int = 0,
                  leave_1hp: bool = False) -> int:
    """Damage of Attack / added-damage (type 3) / multiplier (type 4) abilities. GS2 0x08120A8C.

    element: weapon or ability element (Attack uses the weapon's, FUN_080b0434; 4 = neutral -> diff 0).
    multiplier_x10: ability power for type 4 (damage = core(...) * power / 10); None for type 3.
    crit: 0 none, 1 normal critical (x5/4), 2 effect-36..40 critical (x3/2); both then add the TARGET's
          level/5 + 6 (GS2 0x08120B6A-0x08120B7C reads it from the target unit, like its guard/Defense/Resist).
    hits: per-target multiplier byte (1 normally, 0 = miss, +1/+2 from effects 41-44, 65, 68, 89).
    rand2: the 2 low random bits added at the end (0..3). defense_mode: 1 halves Def (effect 35), 2 zeroes it.
    """
    if tgt.guard == 4:
        return 0
    d = tgt.defense
    if defense_mode == 1:
        d = _div(d, 2)
    elif defense_mode == 2:
        d = 0
    diff = _diff(att, tgt, element)
    if multiplier_x10 is not None:
        dmg = _div(physical_core(att.attack, d, 0, diff) * multiplier_x10, 10)
    else:
        dmg = physical_core(att.attack, d, added, diff)
    dmg *= hits
    if crit:
        dmg = _div(dmg * 5, 4) if crit == 1 else _div(dmg * 3, 2)
        dmg += tgt.level // 5 + 6
    dmg += rand2 & 3
    dmg = _guard(dmg, tgt.guard)
    if dmg <= 0:
        dmg = 1
    if leave_1hp and dmg < tgt.hp - 1:
        dmg = max(tgt.hp - 1, 1)
    return dmg


def psynergy_damage(att: Unit, tgt: Unit, power: int, element: int, damage_type: int = 5, distance: int = 0,
                    hits: int = 1, rand2: int = 0, ability_id: int | None = None, game: str = "gs2") -> int:
    """Base-damage Psynergy (type 5), enemy breath (type 6) and summons (type 8). GS2 0x08120F70.

    power: ability power (+10). For GS2 summons (and the 3 enemy abilities in SUMMON_HP_PERCENT_GS2) the power
    first gains min(target max HP, 10000) * pct / 100. distance = |offset| from the centre target (0..5).
    Unlike attacks there is no minimum of 1.
    """
    if tgt.guard == 4:
        return 0
    if game == "gs2" and ability_id in SUMMON_HP_PERCENT_GS2:
        power += _div(min(tgt.max_hp, 10000) * SUMMON_HP_PERCENT_GS2[ability_id], 100)
    dmg = psy_core(power, _diff(att, tgt, element)) * hits
    table = {5: SPREAD["type5"], 6: SPREAD["type6"], 8: SPREAD["summon"]}.get(damage_type)
    if table:
        dmg = _div(table[min(distance, 5)] * dmg, 100)
    dmg += rand2 & 3
    return _guard(dmg, tgt.guard)


def heal_amount(att: Unit, tgt: Unit, power: int, element: int, distance: int = 0, hits: int = 1,
                rand2: int = 0, from_item: bool = False) -> int:
    """HP restored by a healing (type 1) ability. GS2 0x08120DCE. 0 if the target is down.

    Uses the caster's Power in the ability's element (100 for neutral abilities and for items): power * P / 100,
    then the heal spread table, the per-target multiplier and +0..3, capped at the missing HP.
    """
    if tgt.hp == 0:
        return 0
    P = 100 if (element >= 4 or from_item) else att.power[element]
    h = _div(SPREAD["heal"][min(distance, 5)] * heal_core(power, P), 100) * hits + (rand2 & 3)
    return min(h, tgt.max_hp - tgt.hp)


def pp_drain(att: Unit, tgt: Unit, power: int, element: int, distance: int = 0, hits: int = 1) -> int:
    """PP removed by a Psynergy-drain (type 10) ability. GS2 0x08120CE2. Capped at the target's PP."""
    v = _div(SPREAD["pp_drain"][min(distance, 5)] * psy_core(power, _diff(att, tgt, element)), 100) * hits
    return min(_guard(v, tgt.guard), tgt.pp)


def status_chance(effect: int, att_level: int, tgt_level: int, tgt_luck: int, weak: bool = False,
                  distance: int = 0) -> int:
    """Percent threshold for an effect to land (GS2 FUN_080b075c, without the target-state pre-checks).

    att_level / tgt_level: elemental levels of both units in the ability's element (0 for neutral).
    chance = base + (att_level - tgt_level - luck//2) * 3 (+25 if the target lists the effect as a weakness);
    fixed-chance effects ignore all of that. The roll succeeds if rand100() <= chance * spread / 100, so even
    a chance of 0 lands 1% of the time. Effects 67, 80, 85 roll 3 times. A target with Luck >= 40 is immune to
    effects 18, 19, 26, 27, 28, 34, 80, 82.
    """
    base = status_base_chance(effect)
    if base < 1:
        c = -base
    else:
        c = base + (att_level - tgt_level - (tgt_luck >> 1)) * 3 + (25 if weak else 0)
    return _div(c * SPREAD["status"][min(distance, 5)], 100)


def critical_chance_16(crit_bonus: int) -> float:
    """Probability of a critical on a normal Attack (GS2 0x08124376): 1/32, else rand16 < bonus*65536/200.

    crit_bonus = sum of equipped "Criticals up" values (equip effect 23), FUN_080b0460.
    """
    t = _div(crit_bonus << 16, 200)
    return 1 / 32 + (31 / 32) * min(max(t, 0), 65536) / 65536


def attack_miss_chance(attacker_deluded: bool) -> float:
    """Normal Attack miss chance (GS2 0x08124376), only when the target can act (not asleep/stunned/etc.)."""
    p_del = 0x99 / 256 if attacker_deluded else 0.0
    return p_del + (1 - p_del) / 32


def unleash_chance_percent(weapon_unleash_rate: int, crit_bonus: int = 0) -> int:
    """Weapon unleash chance in percent (GS2 FUN_080b04bc): crit_bonus + 5 * rate (rate 7 -> 35%, 8 -> 40%)."""
    return crit_bonus + weapon_unleash_rate * 5


def flee_chance_x10000(party_levels: list, enemy_levels: list, failed_attempts: int) -> int:
    """Flee threshold out of 10000 (GS2 FUN_0811ce94, GS1 same structure, scale literal 10000 at 0x080B9200).

    5000 + 500*avg(party level) - 500*avg(enemy level) + 2000*attempts so far; success if rand(10000) < value.
    Boss battles (battle type 2) always fail; the party's first-strike round always succeeds. A successful roll
    still fails 1 time in 16 in the run animation (FUN_0811c66c). A failed attempt turns the round into an
    enemy ambush round (the party's actions are dropped).
    """
    pa = _div(sum(party_levels) * 500, len(party_levels))
    ea = _div(sum(enemy_levels) * 500, len(enemy_levels)) if enemy_levels else 0
    return 5000 + pa + failed_attempts * 2000 - ea


def enemy_action_priorities(agility: int, turns: int) -> list:
    """Priority of each action of an enemy with `turns` actions per round (GS2 FUN_0811cfd0)."""
    out = [agility]
    if turns == 4:
        out += [_div(agility * 5, 6), _div(agility * 4, 6), _div(agility, 2)]
    elif turns == 3:
        out += [_div(agility * 3, 4), _div(agility, 2)]
    elif turns == 2:
        out += [_div(agility, 2)]
    return out


def reward_bonus(base: int, enemy_level: int, rolls_d: int, rng) -> int:
    """Extra-reward mode of GS2 FUN_0812824c: base + max(sum of (level//10 + 1) dice, base*3//10).

    EXP (enemy +0x48) uses d4 (`rolls_d`=4); coins (+0x42) use d6. rng() must return 16 bits.
    """
    s = sum(((rng() * rolls_d) >> 16) + 1 for _ in range(enemy_level // 10 + 1))
    return base + max(s, _div(base * 3, 10))


def djinn_recovery_countdowns(n_used_by_owner: int, existing_max: int = -1) -> list:
    """Recovery countdowns given to one owner's Djinn after a summon (GS2 0x08125518 loop).

    start = max(existing countdown of this owner's Djinn) + 1, at least 2; then +1 per further Djinni. Each of
    the owner's turns decrements them (FUN_08124cc4); at 0 the Djinni is Set again (one per owner per turn).
    """
    start = max(existing_max + 1, 2)
    return [start + i for i in range(n_used_by_owner)]


# --------------------------------------------------------------------------------------------------------------
# Self-test: compare with the games' own routines
# --------------------------------------------------------------------------------------------------------------
def _selftest(gs1_path: str, gs2_path: str) -> int:
    from gbax.emu import Gba
    from gbax.rom import Rom
    from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_R2, UC_ARM_REG_R11

    def s32(v):
        return v - (1 << 32) if v & 0x80000000 else v

    from unicorn import UC_HOOK_CODE
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1

    def install_divide(emu, sdiv, udiv):
        """The divide routines live in IWRAM (copied there at boot; ROM stubs GS1 0x080022EC/0x080022F4,
        GS2 0x08002054/0x0800205C jump to them). Model them as C division: put 'bx lr' there and set r0/r1."""
        for a in (sdiv, udiv):
            emu.write(a, (0xE12FFF1E).to_bytes(4, "little"))

        def hook(uc, address, size, data):
            a, b = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
            if address == sdiv:
                q = _div(s32(a), s32(b))
                r = s32(a) - q * s32(b)
            else:
                q, r = a // b, a % b
            uc.reg_write(UC_ARM_REG_R0, q & 0xFFFFFFFF)
            uc.reg_write(UC_ARM_REG_R1, r & 0xFFFFFFFF)
        emu.uc.hook_add(UC_HOOK_CODE, hook, begin=min(sdiv, udiv), end=max(sdiv, udiv))

    divs = {"gs1": (0x03000380, 0x030003F0), "gs2": (0x03000528, 0x03000534)}
    fails, checks = [], 0
    for game, path in (("gs1", gs1_path), ("gs2", gs2_path)):
        rom = Rom.load(path)
        emu = Gba(rom)
        install_divide(emu, *divs[game])
        A = ADDR[game]
        d = rom.data
        tab = [int.from_bytes(d[A["elem_level_table"] - 0x08000000 + 2 * i:][:2], "little") for i in range(32)]
        checks += 1
        if [tuple(tab[i:i + 2]) for i in range(0, 32, 2)] != list(ELEM_LEVEL_TABLE):
            fails.append((game, "elem_level_table"))
        n = 0
        for diff in range(-260, 261, 3):
            for half in (0, 1):
                got = s32(emu.call(A["elem_multiplier"] | 1, (diff & 0xFFFFFFFF, half)))
                n += 1
                if got != elem_multiplier(diff, bool(half)):
                    fails.append((game, "mult", diff, half, got, elem_multiplier(diff, bool(half))))
        for atk in (0, 50, 137, 400):
            for de in (0, 60, 200):
                for add in (0, 30, 120):
                    for diff in (-250, -73, 0, 41, 199, 300):
                        got = s32(emu.call(A["physical_core"] | 1, (atk, de, add, diff & 0xFFFFFFFF)))
                        n += 1
                        if got != physical_core(atk, de, add, diff):
                            fails.append((game, "phys", atk, de, add, diff, got))
        for power in (12, 35, 160, 500, 2000):
            for diff in (-250, -101, -7, 0, 33, 150, 260):
                for scale in (256, 200):
                    got = s32(emu.call(A["psy_core"] | 1, (power, diff & 0xFFFFFFFF, scale)))
                    n += 1
                    if got != psy_core(power, diff, scale):
                        fails.append((game, "psy", power, diff, scale, got))
        for power in (70, 150, 1000):
            for P in (0, 50, 95, 100, 137, 210):
                got = s32(emu.call(A["heal_core"] | 1, (power, P, 256)))
                n += 1
                if got != heal_core(power, P):
                    fails.append((game, "heal", power, P, got))
        for st in (0, 1, 0x12345678, 0xDEADBEEF):
            emu.write(A["rng_state"], st.to_bytes(4, "little"))
            ref = BattleRng(st)
            for _ in range(5):
                got = emu.call(A["rng"] | 1)
                n += 1
                if got != ref.rand16() or int.from_bytes(emu.read(A["rng_state"], 4), "little") != ref.state:
                    fails.append((game, "rng", st, got))
        diffs = []
        for e in range(0, 0x5C):
            got = s32(emu.call(A["status_base_chance"] | 1, (e,)))
            n += 1
            if got != status_base_chance(e):
                diffs.append((e, got, status_base_chance(e)))
        if game == "gs2" and diffs:
            fails.append((game, "status_base_chance", diffs))
        elif diffs:
            print(f"  note: GS1 base chances that differ from GS2 (id, GS1, GS2): {diffs}")
        if game == "gs2":
            uc = emu.uc
            lo, hi = A["summon_bonus_block"]
            got = {}
            for i in range(0, 735):
                uc.reg_write(UC_ARM_REG_R11, i)
                uc.reg_write(UC_ARM_REG_R2, 0)
                uc.reg_write(UC_ARM_REG_CPSR, uc.reg_read(UC_ARM_REG_CPSR) | 0x20)
                uc.emu_start(lo | 1, hi, count=500)
                v = uc.reg_read(UC_ARM_REG_R2)
                if v:
                    got[i] = v
            n += 735
            if got != SUMMON_HP_PERCENT_GS2:
                fails.append((game, "summon_hp_percent", got))
        checks += n
        print(f"{game}: {n} emulated comparisons")
    print(f"total {checks} checks, {len(fails)} mismatches")
    for f in fails[:20]:
        print("  MISMATCH", f)
    return 1 if fails else 0


if __name__ == "__main__":
    GS1 = r"C:\Users\aaron\Documents\UnboundHack\games\AGSE-5c469520-Golden-Sun-USA-Europe\rom\Golden Sun (USA, Europe).gba"
    GS2 = r"C:\Users\aaron\OneDrive\Apps-Roms\Golden Sun - The Lost Age (USA, Europe).gba"
    if "--selftest" in sys.argv:
        rest = [a for a in sys.argv[1:] if a != "--selftest"]
        sys.exit(_selftest(rest[0] if rest else GS1, rest[1] if len(rest) > 1 else GS2))
    print(__doc__)
