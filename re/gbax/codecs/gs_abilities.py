"""Golden Sun 1 / The Lost Age: Psynergy (ability), class, Djinn and summon tables.

Run:  python -m gbax.codecs.gs_abilities ROM [ROM ...]
Writes games/<slug>/data/{abilities,classes,djinn,summons}.json (UTF-8).

How the tables are found
------------------------
Nothing is located by a hard-coded table address. The exporter:
  1. finds the master file table (entry 0 = 0x08000000, entry 1 = the table itself) and from it the
     code modules (files that start with `ldr r4,=f; bx r4` export stubs) and their extents;
  2. collects every word-aligned u32 literal inside the kernel + code modules that points into the ROM
     (the literal pools that `ldr rX,=table` reads);
  3. tests each literal against a shape predicate for each table (below). Exactly one must match.
Table ends are checked against the next code-referenced table, so counts are not guessed either.
`PROFILES` holds the values found for the two US/EU ROMs; the exporter asserts the discovery matches.

Record layouts (see notes/gs_abilities_classes.md for evidence):
  ability   GS1 16 bytes, GS2 12 bytes
            +0 u8 target   +1 u8 flags (low nibble damage type, 0x40 usable from the menu out of battle,
                                        0x80 usable in battle; map-cast Psynergy is marked by the field id)
            +2 u8 element  +3 u8 effect  +4 u16 battle animation
            +6 u16 field-Psynergy id (GS2) / +12 u16 (GS1)   +8 u8 range  +9 u8 PP  +10 u16 power
  class     0x54 bytes: +0 u32 class type, +4 u8[4] elemental level reqs (Ve,Me,Ma,Ju),
            +8 u8[6] multipliers in 10% (HP,PP,Atk,Def,Agi,Luck), +0x10 16 x learned ability
            (GS1: u8 ability, u8 level, u16 0; GS2: u16 ability, u16 level), +0x50 u8[3] effect weaknesses
  djinn     12 bytes, 4 elements x 20 slots: +0 u32 ability, +4 u8 HP,PP,Atk,Def,Agi,Luck bonus while Set
  summon    8 bytes: +0 u32 ability, +4 u8[4] Djinn cost (Ve,Me,Ma,Ju)
"""
import argparse
import json
import re
import struct
import sys
from pathlib import Path

from gbax.rom import Rom

BASE = 0x08000000
ELEMENTS = ["Venus", "Mercury", "Mars", "Jupiter", "Neutral"]
STATS = ["hp", "pp", "attack", "defense", "agility", "luck"]
TARGETS = {0: "none (field only)", 1: "enemies", 2: "allies", 4: "self"}
# Low nibble of the flags byte. Names inferred from which abilities use each value (see notes).
DAMAGE_TYPES = {
    0: "none", 1: "healing", 2: "effect_only", 3: "added_damage", 4: "multiplier",
    5: "base_damage", 6: "base_damage_alt", 7: "djinn_effect", 8: "summon",
    9: "utility", 10: "psynergy_drain", 11: "psynergy_recovery",
}

# Values discovered for the known ROMs; the exporter recomputes and asserts them.
PROFILES = {
    "AGSE": dict(game="Golden Sun", ability_table=0x0807EE58, ability_stride=16, ability_count=519,
                 class_table=0x08084B1C, class_count=203, class_type_table=0x08088DB8,
                 djinn_table=0x0808926C, summon_table=0x08084A9C, summon_count=16,
                 text_ability_name=819, text_ability_desc=1338, text_class_name=1857, text_item_name=None),
    "AGFE": dict(game="Golden Sun: The Lost Age", ability_table=0x080B7C14, ability_stride=12, ability_count=734,
                 class_table=0x080C15F4, class_count=244, class_type_table=0x080C6604,
                 djinn_table=0x080C6BB0, summon_table=0x080C150C, summon_count=29,
                 text_ability_name=1447, text_ability_desc=2181, text_class_name=2915, text_item_name=607),
}

# Table accessors found from the literal-pool loads (decompiled; bounds as the code checks them).
GETTERS = {
    "AGSE": dict(ability="0x08078B9C: id &= 0x3FFF; id > 0x207 -> 0; table + id*16",
                 djinn="0x0807A0CC: (element<4, index<20) else slot 0; table + (element*20+index)*12",
                 summon="0x080797D4: i < 16 else NULL; table + i*8",
                 class_="0x08079AD8: table + id*0x54"),
    "AGFE": dict(ability="0x080AF43C: id &= 0x3FFF; id > 0x2DE -> 0; table + id*12",
                 djinn="0x080B0A94: (element<4, index<20) else slot 0; table + (element*20+index)*12",
                 summon="0x080AFF7C: i < 29 else NULL; table + i*8",
                 class_="literal at 0x080B0284/0x080B0294 (selection 0x080B0144)"),
}

# Class selection, read from the decompiled code (see notes): extra rules that the tables don't hold.
SELECTION = {
    "AGSE": dict(function="0x080799B0 (type lookup 0x080797EE: table[primary*4+secondary])",
                 overrides=[
                     "story flag 0x20 set: Isaac (pc 0) -> class 200, Garet (pc 1) -> class 201",
                     "pc 5 -> class 202 always",
                 ]),
    "AGFE": dict(function="0x080B0144 (elemental levels from 0x080AFFAC)",
                 overrides=[
                     "type 2 and pc 5 (Jenna) -> type 13",
                     "type 6 and pc 7 (Piers) -> type 14",
                     "class-changing item 0x1BB -> type 15, 0x1BC -> type 16, 0x1BD -> type 17",
                 ],
                 override_items=[0x1BB, 0x1BC, 0x1BD]),
}


def u16(d, o):
    return d[o] | d[o + 1] << 8


def u32(d, o):
    return struct.unpack_from("<I", d, o)[0]


def hx(a):
    return f"0x{a:08X}"


# ---------------------------------------------------------------- discovery

def file_table(d):
    """Master file table: entry 0 == ROM start, entry 1 == the table's own address."""
    for o in range(0, len(d) - 8, 0x10):
        if u32(d, o) == BASE and u32(d, o + 4) == BASE + o:
            ptrs = []
            k = o
            while k + 4 <= len(d):
                v = u32(d, k)
                if not BASE <= v < BASE + len(d):
                    break
                ptrs.append(v)
                k += 4
            return BASE + o, ptrs
    raise ValueError("master file table not found")


def code_ranges(d):
    ft, ptrs = file_table(d)
    starts = sorted(set(ptrs) | {BASE + len(d)})
    mods = []
    for i in range(3, min(len(ptrs), 40)):
        a = ptrs[i] - BASE
        if d[a:a + 4] == b"\x00\x4c\x20\x47":  # ldr r4,[pc]; bx r4
            end = next(s for s in starts if s > ptrs[i])
            mods.append((ptrs[i], end))
    kernel_end = min(m[0] for m in mods) if mods else BASE + 0x10000
    return ft, [(BASE, kernel_end)] + sorted(set(mods))


def code_literals(d, ranges):
    """{target: [literal addresses]} for aligned ROM pointers inside code."""
    lits = {}
    for lo, hi in ranges:
        a, b = lo - BASE, min(hi - BASE, len(d))
        for i, (v,) in enumerate(struct.iter_unpack("<I", d[a:b - (b - a) % 4])):
            if BASE <= v < BASE + len(d):
                lits.setdefault(v, []).append(lo + 4 * i)
    return lits


def _one(cands, what):
    if len(cands) != 1:
        raise ValueError(f"{what}: expected 1 candidate, got {[hx(c) for c in cands]}")
    return cands[0]


def discover(d):
    ft, ranges = code_ranges(d)
    lits = code_literals(d, ranges)
    found = {"file_table": ft, "code_ranges": [(hx(a), hx(b)) for a, b in ranges]}

    def rec(a, n=16):
        return d[a - BASE:a - BASE + n]

    # Ability table: record 0 "Nothing" (01 05 04), 1 "Attack" (01 83 04), 2 "Defend" (04 89 04).
    cands = []
    for v in lits:
        for st in (12, 16):
            if v - BASE + 3 * st < len(d) and rec(v, 3) == b"\x01\x05\x04" and \
                    rec(v + st, 3) == b"\x01\x83\x04" and rec(v + 2 * st, 3) == b"\x04\x89\x04":
                cands.append((v, st))
    ab, st = _one(cands, "ability table")
    # End: the next code-referenced table at a record boundary that starts with ASCII text
    # (the enemy table, whose records begin with a space-padded name).
    ends = sorted(v for v in lits if v >= ab + 256 * st and (v - ab) % st == 0
                  and 0x20 <= d[v - BASE] < 0x7F and 0x20 <= d[v - BASE + 1] < 0x7F)
    found.update(ability_table=ab, ability_stride=st, ability_count=(ends[0] - ab) // st,
                 ability_refs=[hx(x) for x in lits[ab]], ability_end_ref=hx(ends[0]))

    # Class table: record 0 = type 12, no requirements, all multipliers 100%; record 1 type 1.
    sig = b"\x0c\x00\x00\x00\x00\x00\x00\x00" + b"\x0a" * 6
    cl = _one([v for v in lits if rec(v, 14) == sig and u32(d, v - BASE + 0x54) == 1], "class table")
    # Class-type table: 16 u32 in 1..16, code-referenced, directly after the class table.
    ct = _one([v for v in lits if v > cl and (v - cl) % 0x54 == 0 and v - cl < 0x54 * 400
               and all(1 <= u32(d, v - BASE + 4 * i) <= 16 for i in range(16))], "class type table")
    found.update(class_table=cl, class_count=(ct - cl) // 0x54, class_type_table=ct,
                 class_refs=[hx(x) for x in lits[cl]], class_type_refs=[hx(x) for x in lits[ct]])

    # Djinn table: 80 x 12-byte records whose u32 runs 300..379.
    dj = _one([v for v in lits if v - BASE + 960 <= len(d) and
               all(u32(d, v - BASE + 12 * i) == 300 + i for i in range(80))], "djinn table")
    found.update(djinn_table=dj, djinn_refs=[hx(x) for x in lits[dj]])

    # Summon table: 8-byte records, first = (380 "Venus", cost 1/0/0/0).
    sm = _one([v for v in lits if u32(d, v - BASE) == 380 and rec(v + 4, 4) == b"\x01\x00\x00\x00"],
              "summon table")
    n = 0
    while 300 <= u32(d, sm - BASE + 8 * n) < found["ability_count"] and sum(rec(sm + 8 * n + 4, 4)) <= 16:
        n += 1
    found.update(summon_table=sm, summon_count=n, summon_refs=[hx(x) for x in lits[sm]],
                 summon_end_is_class_table=(sm + 8 * n == cl))
    return found


# ---------------------------------------------------------------- text

def load_text(rom):
    p = rom.workspace / "text" / "strings.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def clean(s):
    return None if s is None else re.sub(r"\{[0-9A-F]{2}\}", "", s).strip()


def text_bases(T, prof, n_ab):
    """Locate ability-name text by content ("Attack","Defend" at ids 1,2); fall back to the profile."""
    b = dict(ability_name=prof["text_ability_name"], ability_desc=prof["text_ability_desc"],
             class_name=prof["text_class_name"], item_name=prof["text_item_name"], verified=False)
    if T:
        hits = [int(k) - 1 for k, v in T.items() if v == "Attack" and T.get(str(int(k) + 1)) == "Defend"
                and T.get(str(int(k) + 89)) == "Cure"]
        if len(hits) == 1:
            b["ability_name"] = hits[0]
            b["ability_desc"] = hits[0] + n_ab
            b["class_name"] = hits[0] + 2 * n_ab
            b["verified"] = T.get(str(b["class_name"] + 1)) == "Squire"
    return b


# ---------------------------------------------------------------- export

def export(rom_path):
    rom = Rom.load(rom_path)
    d = rom.data
    prof = PROFILES.get(rom.code)
    if prof is None:
        raise SystemExit(f"{rom.code}: not a known Golden Sun ROM ({sorted(PROFILES)})")
    f = discover(d)
    mismatch = {k: (hx(f[k]) if k.endswith("table") else f[k], hx(v) if k.endswith("table") else v)
                for k, v in prof.items() if k in f and f[k] != v}
    if mismatch:
        print(f"WARNING {rom.code}: discovery differs from profile: {mismatch}", file=sys.stderr)
    T = load_text(rom)
    nab, st = f["ability_count"], f["ability_stride"]
    tb = text_bases(T, prof, nab)

    def txt(i):
        return None if (T is None or i is None) else T.get(str(i))

    def ab_name(a):
        return clean(txt(tb["ability_name"] + a)) if 0 <= a < nab else None

    meta = dict(game=prof["game"], rom_code=rom.code, rom_sha1=rom.sha1, generator="gbax.codecs.gs_abilities",
                text_bases=tb, text_source=("text/strings.json" if T else None))

    # Abilities
    abilities = []
    for i in range(nab):
        o = f["ability_table"] - BASE + i * st
        r = d[o:o + st]
        fl = r[1]
        field_id = u16(r, 12) if st == 16 else u16(r, 6)
        rng = r[8]
        e = dict(id=i, name_text_id=tb["ability_name"] + i, desc_text_id=tb["ability_desc"] + i,
                 name=ab_name(i), name_raw=txt(tb["ability_name"] + i), description=txt(tb["ability_desc"] + i),
                 target=r[0], target_name=TARGETS.get(r[0], f"?{r[0]}"),
                 flags=fl, damage_type=fl & 0x0F, damage_type_name=DAMAGE_TYPES.get(fl & 0x0F, f"?{fl & 15}"),
                 usable_in_battle=bool(fl & 0x80), usable_from_menu=bool(fl & 0x40),
                 usable_in_field=bool(fl & 0x40) or field_id != 0,
                 element=r[2], element_name=ELEMENTS[r[2]] if r[2] < 5 else f"?{r[2]}",
                 effect=r[3], animation=u16(r, 4), field_psynergy_id=field_id,
                 range=rng, targets=("all" if rng == 255 else (2 * rng - 1 if rng else 0)),
                 pp=r[9], power=u16(r, 10), raw=r.hex())
        e["empty"] = not any(r)
        abilities.append(e)
    G = GETTERS[rom.code]
    rom_ab = dict(table=hx(f["ability_table"]), stride=st, count=nab, code_literals=f["ability_refs"], getter=G["ability"],
                  end=f["ability_end_ref"], layout_note="GS1 adds 4 bytes; field id at +12 instead of +6")
    out = rom.workspace / "data"
    out.mkdir(exist_ok=True)

    def write(name, obj):
        (out / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")

    write("abilities.json", dict(meta, source=rom_ab, enums=dict(targets=TARGETS, damage_types=DAMAGE_TYPES,
                                                                  elements=ELEMENTS), abilities=abilities))

    # Classes
    cl, ncl = f["class_table"], f["class_count"]
    pairs = [d[cl - BASE + c * 0x54 + 0x10 + 4 * k:cl - BASE + c * 0x54 + 0x14 + 4 * k]
             for c in range(ncl) for k in range(16)]
    u8_pairs = sum(1 for p in pairs if p[2] or p[3]) == 0 and sum(1 for p in pairs if p[1]) > 0 \
        and st == 16  # GS1: 1-byte ability + 1-byte level (all bytes 2-3 are zero)
    classes = []
    for c in range(ncl):
        o = cl - BASE + c * 0x54
        r = d[o:o + 0x54]
        learned = []
        for k in range(16):
            p = r[0x10 + 4 * k:0x14 + 4 * k]
            a, lv = (p[0], p[1]) if u8_pairs else (u16(p, 0), u16(p, 2))
            if a:
                learned.append(dict(ability=a, level=lv, name=ab_name(a)))
        classes.append(dict(id=c, name_text_id=tb["class_name"] + c, name=clean(txt(tb["class_name"] + c)),
                            type=u32(r, 0),
                            elemental_levels=dict(zip(ELEMENTS[:4], r[4:8])),
                            multipliers_pct={s: r[8 + j] * 10 for j, s in enumerate(STATS)},
                            psynergy=learned, effect_weaknesses=list(r[0x50:0x53]), empty=not any(r), raw=r.hex()))
    series = {}
    for c in classes:
        if not c["empty"]:
            series.setdefault(c["type"], []).append(c["id"])
    ct = f["class_type_table"]
    grid = [[u32(d, ct - BASE + 4 * (row * 4 + col)) for col in range(4)] for row in range(4)]
    sel = dict(SELECTION[rom.code])
    if sel.get("override_items") and tb["item_name"] is not None:
        sel["override_item_names"] = [clean(txt(tb["item_name"] + i)) for i in sel["override_items"]]
    write("classes.json", dict(
        meta, source=dict(table=hx(cl), stride=0x54, count=ncl,
                          used=sum(1 for c in classes if not c["empty"]), code_literals=f["class_refs"], getter=G["class_"],
                          learned_pair_format="u8 ability,u8 level,u16 0" if u8_pairs else "u16 ability,u16 level",
                          class_type_table=hx(ct), class_type_code_literals=f["class_type_refs"]),
        selection=dict(sel, rule=("levels[e] = 10*elemental_level[e] (+ tenths); primary = element with the "
                                  "highest level (lowest index on ties); secondary = highest of the other three, "
                                  "or primary again if its level < 10; type = type_table[primary][secondary]; "
                                  "class = highest-index class of that type whose 4 requirements r satisfy "
                                  "r*10 <= levels[e]; none -> class 0"),
                       type_table_rows_primary_cols_secondary=dict(zip(ELEMENTS[:4],
                                                                       [dict(zip(ELEMENTS[:4], g)) for g in grid]))),
        series={str(t): dict(first_class=classes[ids[0]]["name"], classes=ids) for t, ids in sorted(series.items())},
        classes=classes))

    # Djinn
    dj = f["djinn_table"]
    djinn = []
    for i in range(80):
        o = dj - BASE + 12 * i
        a = u32(d, o)
        bonus = dict(zip(STATS, d[o + 4:o + 10]))
        A = abilities[a] if a < nab else {}
        djinn.append(dict(slot=i, element=ELEMENTS[i // 20], index=i % 20, ability=a, name=ab_name(a),
                          used=any(bonus.values()), set_bonus=bonus,
                          unleash=dict(damage_type=A.get("damage_type_name"), effect=A.get("effect"),
                                       power=A.get("power"), range=A.get("range"), target=A.get("target_name"),
                                       description=A.get("description"))))
    used = [x for x in djinn if x["used"]]
    write("djinn.json", dict(meta, source=dict(table=hx(dj), stride=12, slots=80, per_element=20,
                                               code_literals=f["djinn_refs"], getter=G["djinn"]),
                             counts=dict(total=len(used), **{e: sum(1 for x in used if x["element"] == e)
                                                             for e in ELEMENTS[:4]}),
                             djinn=djinn))

    # Summons
    sm, nsm = f["summon_table"], f["summon_count"]
    summons = []
    for i in range(nsm):
        o = sm - BASE + 8 * i
        a = u32(d, o)
        cost = dict(zip(ELEMENTS[:4], d[o + 4:o + 8]))
        A = abilities[a]
        summons.append(dict(index=i, ability=a, name=ab_name(a), cost=cost, total_djinn=sum(cost.values()),
                            power=A["power"], element=A["element_name"], range=A["range"],
                            damage_type=A["damage_type_name"], effect=A["effect"], animation=A["animation"],
                            description=A["description"]))
    write("summons.json", dict(meta, source=dict(table=hx(sm), stride=8, count=nsm, code_literals=f["summon_refs"], getter=G["summon"],
                                                 ends_at_class_table=f["summon_end_is_class_table"]),
                               summons=summons))
    return rom, f, abilities, classes, djinn, summons


def checks(rom, f, abilities, classes, djinn, summons):
    """Sanity checks against well-known facts."""
    by = {a["name"]: a for a in abilities if a["name"]}
    res = []

    def chk(what, ok, got):
        res.append(f"{'OK  ' if ok else 'FAIL'} {what}: {got}")

    mv = by.get("Move")
    chk("Move costs 2 PP", mv is not None and mv["pp"] == 2, mv and mv["pp"])
    chk("class 1 is Squire", classes[1]["name"] in ("Squire", None), classes[1]["name"])
    n = sum(1 for x in djinn if x["used"])
    chk("Djinn count (GS1 28 / GS2 72)", n == (28 if rom.code == "AGSE" else 72), n)
    v = summons[0]
    chk("Venus summon costs one Venus Djinni", v["cost"] == {"Venus": 1, "Mercury": 0, "Mars": 0, "Jupiter": 0},
        (v["name"], v["cost"]))
    chk("summon count (GS1 16 / GS2 29)", len(summons) == (16 if rom.code == "AGSE" else 29), len(summons))
    cure = abilities[90]
    chk("ability 90 = Cure, 3 PP, heals 70", cure["pp"] == 3 and cure["power"] == 70, (cure["name"], cure["pp"],
                                                                                       cure["power"]))
    flint = djinn[0]
    chk("Flint: HP+8 PP+4 Atk+3", flint["set_bonus"]["hp"] == 8 and flint["set_bonus"]["pp"] == 4
        and flint["set_bonus"]["attack"] == 3, (flint["name"], flint["set_bonus"]))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("roms", nargs="+")
    a = ap.parse_args(argv)
    for p in a.roms:
        rom, f, ab, cl, dj, sm = export(p)
        print(f"{rom.code} {rom.slug}")
        for k in ("ability_table", "class_table", "class_type_table", "djinn_table", "summon_table"):
            print(f"  {k:17s} {hx(f[k])}")
        print(f"  abilities {f['ability_count']} x {f['ability_stride']}  classes {f['class_count']}  "
              f"summons {f['summon_count']}  djinn {sum(1 for x in dj if x['used'])}/80 slots")
        for line in checks(rom, f, ab, cl, dj, sm):
            print("  " + line)
        print(f"  -> {rom.workspace / 'data'}")


if __name__ == "__main__":
    main()
