"""Golden Sun 1 / 2 battle data: enemies, enemy groups, encounters, items, playable characters.

Usage:  python -m gbax.codecs.gs_units ROM [ROM ...]

Writes UTF-8 JSON to games/<slug>/data/:
    enemies.json, encounters.json (encounter tables + enemy groups), items.json, characters.json

Every table address below was found from the code that reads it (see notes/gs_units_items.md). At run time each
address is re-checked: the script confirms a Thumb literal pool in the ROM still points at it, so a wrong ROM or a
moved table fails loudly instead of producing garbage.

If games/<slug>/text/strings.json exists (written by a separate text extractor), names are filled in from it.
"""

import json
import re
import struct
import sys
from pathlib import Path

from gbax.rom import Rom

ELEMENTS = ["Venus", "Mercury", "Mars", "Jupiter", "Neutral"]
PC_NAMES = ["Isaac", "Garet", "Ivan", "Mia", "Felix", "Jenna", "Sheba", "Piers"]  # equip-mask bit order

# Per-game layout. Offsets are ROM addresses (0x08xxxxxx). "count" = number of entries the game's own bounds
# check allows (code-verified) unless noted.
CONFIG = {
    "AGSE": {  # Golden Sun (USA/Europe)
        "items": 0x0807B6A8, "item_count": 324, "item_names_text": 0x182, "item_named": 269,
        "abilities": 0x0807EE58, "ability_count": 519, "ability_stride": 0x10,
        "enemies": 0x08080EC8, "enemy_stride": 0x54, "enemy_count": 165, "enemy_names_text": 0x28F,
        "enemy_named": 164,  # the last row is an empty sentinel with no name
        "elemental": 0x08088E38, "elemental_count": 44,
        "pcs": 0x080844EC, "pc_count": 8,
        "elvl_power": 0x08088DF8,
        "summons": 0x08084A9C, "summon_count": 16,
        "classes": 0x08084B1C, "class_count": 203,
        "groups": 0x080C5C38, "group_format": "gs1", "group_count": 380,
        "encounters": 0x0809C610, "encounter_count": 104,
        "enemy_layout": {
            "items": 0x28, "item_counts": 0x30, "elemental": 0x34, "attack_type": 0x35, "ai_pattern": 0x36,
            "item_use_mask": 0x37, "abilities": 0x38, "weaknesses": 0x48, "unk_4b": 0x4B, "coins": 0x4C,
            "drop_item": 0x4E, "drop_rate": 0x50, "exp": 0x52, "extra": (0x1E, 0x28),
        },
    },
    "AGFE": {  # Golden Sun: The Lost Age (USA/Europe)
        "items": 0x080B2364, "item_count": 516, "item_names_text": 0x25F, "item_named": 461,
        "abilities": 0x080B7C14, "ability_count": 734, "ability_stride": 0x0C,
        "enemies": 0x080B9E7C, "enemy_stride": 0x4C, "enemy_count": 380, "enemy_names_text": 0x42C,
        "enemy_named": 379,
        "elemental": 0x080C6684, "elemental_count": 48,
        "pcs": 0x080C0F4C, "pc_count": 8,
        "elvl_power": 0x080C6644,
        "summons": 0x080C150C, "summon_count": 29,
        "classes": 0x080C15F4, "class_count": 244,
        "groups": 0x0812CE7C, "group_format": "gs2", "group_count": 660,
        "encounters": 0x080EDACC, "encounter_count": 110,
        "enemy_layout": {
            "items": 0x1E, "item_counts": 0x26, "elemental": 0x2A, "attack_type": 0x2B, "ai_pattern": 0x2C,
            # EXP/coins verified from the GS2 reward code (FUN_0812824c adds +0x48 to the EXP total)
            "item_use_mask": 0x2D, "abilities": 0x2E, "weaknesses": 0x3E, "unk_4b": 0x41, "coins": 0x42,
            "drop_item": 0x44, "drop_rate": 0x46, "exp": 0x48, "extra": None,
        },
    },
}

# Item types and flags, checked against the alchemy decomp and both games' tables (items and equipment reviews,
# 16 Oct): rings are type 8 and shirts type 9 (GS1's 7 rings and 3 shirts), type 7 holds special pieces (the Trident),
# 10 is GS2's class items (Mysterious Card, Trainer's Whip, Tomegathericon), 11 carried key items.
ITEM_TYPES = {
    0: "item", 1: "weapon", 2: "armor", 3: "shield/arm", 4: "helm", 5: "boots", 6: "psynergy_item",
    7: "special", 8: "ring", 9: "shirt", 10: "class_item", 11: "carried_key_item",
}
# 0x02 blocks removing a worn piece (and giving or dropping it while worn); Golden Sun pairs it with the curse bit.
ITEM_FLAGS = {0x01: "cursed", 0x02: "locked_when_equipped", 0x04: "rare", 0x08: "important", 0x10: "stackable",
              0x20: "flag20", 0x40: "flag40", 0x80: "flag80"}


class Reader:
    def __init__(self, data):
        self.d = data

    def at(self, addr):
        return addr - 0x08000000

    def u8(self, a):
        return self.d[self.at(a)]

    def s8(self, a):
        return struct.unpack_from("<b", self.d, self.at(a))[0]

    def u16(self, a):
        return struct.unpack_from("<H", self.d, self.at(a))[0]

    def s16(self, a):
        return struct.unpack_from("<h", self.d, self.at(a))[0]

    def u32(self, a):
        return struct.unpack_from("<I", self.d, self.at(a))[0]

    def raw(self, a, n):
        return self.d[self.at(a):self.at(a) + n]


def literal_refs(data, value, limit=0x400000):
    """ROM addresses of Thumb `ldr rX,[pc,#imm]` instructions whose literal equals value."""
    want = struct.pack("<I", value)
    out = []
    i = data.find(want, 0, limit)
    while i != -1:
        if i % 4 == 0:
            for back in range(4, 1024, 2):  # ldr reaches up to 1020 bytes forward
                o = i - back
                if o < 0:
                    break
                h = struct.unpack_from("<H", data, o)[0]
                if h >> 11 == 0b01001 and ((o + 4) & ~3) + (h & 0xFF) * 4 == i:
                    out.append(0x08000000 + o)
        i = data.find(want, i + 1, limit)
    return out


def load_strings(ws):
    p = ws / "text" / "strings.json"
    if not p.exists():
        return None
    obj = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(obj, dict):
        if "strings" in obj:
            obj = obj["strings"]
        if isinstance(obj, dict):
            return {int(k, 0) if isinstance(k, str) else int(k): v for k, v in obj.items()}
    if isinstance(obj, list):
        out = {}
        for i, v in enumerate(obj):
            if isinstance(v, dict):
                out[int(v.get("id", i))] = v.get("text", v.get("string"))
            else:
                out[i] = v
        return out
    return None


def load_ability_names(ws):
    """Optional: ability names from data/abilities.json (written by the Psynergy extractor), id -> name."""
    p = ws / "data" / "abilities.json"
    if not p.exists():
        return {}
    obj = json.loads(p.read_text(encoding="utf-8"))
    rows = obj.get("abilities", []) if isinstance(obj, dict) else obj
    return {int(a["id"]): a.get("name") for a in rows if isinstance(a, dict) and "id" in a}


class GsUnits:
    def __init__(self, rom):
        self.rom = rom
        self.cfg = CONFIG.get(rom.code)
        if not self.cfg:
            raise SystemExit(f"{rom.code}: not Golden Sun 1 (AGSE) or 2 (AGFE)")
        self.r = Reader(rom.data)
        self.evidence = {}
        self.strings = load_strings(rom.workspace)
        self.ability_names = load_ability_names(rom.workspace)

    def aname(self, aid):
        return self.ability_names.get(aid) if aid else None

    def name(self, text_id):
        if self.strings is None or text_id is None:
            return None
        s = self.strings.get(text_id)
        return re.sub(r"\{ART:\d+\}", "", s).strip() if isinstance(s, str) else s  # drop article codes

    # ---------- verification ----------
    def verify(self):
        c = self.cfg
        for key in ("items", "abilities", "enemies", "elemental", "pcs", "elvl_power", "summons", "classes",
                    "groups", "encounters"):
            refs = literal_refs(self.rom.data, c[key])
            self.evidence[key] = {"address": f"0x{c[key]:08X}", "code_refs": [f"0x{x:08X}" for x in refs[:6]]}
            if not refs:
                raise SystemExit(f"{key}: no code literal points at 0x{c[key]:08X}; wrong ROM/revision?")
        self.evidence["exp_table"] = self.find_exp_table()

    def find_exp_table(self):
        """EXP-to-level table: u32 cumulative EXP, starts 0, 24, 67, 144 in both games (data match + code ref)."""
        pat = struct.pack("<4I", 0, 24, 67, 144)
        i = self.rom.data.find(pat, 0, 0x400000)
        while i != -1 and i % 4:
            i = self.rom.data.find(pat, i + 1, 0x400000)
        if i == -1:
            return None
        addr = 0x08000000 + i
        refs = literal_refs(self.rom.data, addr)
        return {"address": f"0x{addr:08X}", "code_refs": [f"0x{x:08X}" for x in refs[:6]]}

    # ---------- tables ----------
    def elemental(self):
        c, r = self.cfg, self.r
        out = []
        for i in range(c["elemental_count"]):
            a = c["elemental"] + i * 0x18
            out.append({
                "id": i,
                "element": r.u32(a),
                "element_name": ELEMENTS[r.u32(a)] if r.u32(a) < 5 else None,
                "levels": {ELEMENTS[e]: r.u8(a + 4 + e) for e in range(4)},
                "power": {ELEMENTS[e]: r.s16(a + 8 + e * 4) for e in range(4)},
                "resist": {ELEMENTS[e]: r.s16(a + 10 + e * 4) for e in range(4)},
            })
        return out

    def enemies(self):
        c, r, L = self.cfg, self.r, self.cfg["enemy_layout"]
        elem = self.elemental()
        out = []
        for i in range(c["enemy_count"]):
            a = c["enemies"] + i * c["enemy_stride"]
            items = [r.u16(a + L["items"] + 2 * k) for k in range(4)]
            counts = [r.u8(a + L["item_counts"] + k) for k in range(4)]
            rate = r.u16(a + L["drop_rate"])
            text_id = c["enemy_names_text"] + i if i < c["enemy_named"] else None
            e = {
                "id": i, "battle_id": i + 8, "name_text_id": text_id, "name": self.name(text_id),
                "placeholder": i == 0 or i >= c["enemy_named"],  # row 0 is a "???" dummy, the last an empty sentinel
                "level": r.u8(a + 0x0F), "hp": r.u16(a + 0x10), "pp": r.u16(a + 0x12),
                "attack": r.u16(a + 0x14), "defense": r.u16(a + 0x16), "agility": r.u16(a + 0x18),
                "luck": r.u8(a + 0x1A), "turns": r.u8(a + 0x1B), "hp_regen": r.u8(a + 0x1C),
                "pp_regen": r.u8(a + 0x1D),
                "battle_items": [{"item": it, "count": n} for it, n in zip(items, counts) if it],
                "elemental_id": r.u8(a + L["elemental"]),
                "attack_type": r.u8(a + L["attack_type"]),
                "ai_pattern": r.u8(a + L["ai_pattern"]),
                "item_use_mask": r.u8(a + L["item_use_mask"]),
                "abilities": [r.u16(a + L["abilities"] + 2 * k) for k in range(8)],
                "ability_names": [self.aname(r.u16(a + L["abilities"] + 2 * k)) for k in range(8)],
                "weaknesses": [r.u8(a + L["weaknesses"] + k) for k in range(3)],
                "unk": r.u8(a + L["unk_4b"]),
                "exp": r.u16(a + L["exp"]), "coins": r.u16(a + L["coins"]),
                "drop_item": r.u16(a + L["drop_item"]), "drop_rate_code": rate,
                "drop_chance": (min(0x20000 >> rate, 0x10000) / 0x10000) if r.u16(a + L["drop_item"]) else 0,
            }
            if L["extra"]:
                lo, hi = L["extra"]
                e["unk_1e"] = r.raw(a + lo, hi - lo).hex()
            eid = e["elemental_id"]
            if eid < len(elem):
                e["elemental"] = {k: elem[eid][k] for k in ("element_name", "levels", "power", "resist")}
            out.append(e)
        return out

    def groups(self):
        c, r = self.cfg, self.r
        out = []
        for i in range(c["group_count"]):
            if c["group_format"] == "gs1":  # 16 bytes: u8 formation, u8 enemy[5], u8 min[5], u8 max[5]
                a = c["groups"] + i * 0x10
                enemies = [r.u8(a + 1 + k) for k in range(5)]
                mins = [r.u8(a + 6 + k) for k in range(5)]
                maxs = [r.u8(a + 11 + k) for k in range(5)]
                g = {"id": i, "formation": r.u8(a)}
            else:  # 24 bytes: u16 enemy[5], u8 min[5], u8 max[5], u8 formation, 3 unknown
                a = c["groups"] + i * 0x18
                enemies = [r.u16(a + 2 * k) for k in range(5)]
                mins = [r.u8(a + 10 + k) for k in range(5)]
                maxs = [r.u8(a + 15 + k) for k in range(5)]
                g = {"id": i, "formation": r.u8(a + 0x14), "unk_15": r.raw(a + 0x15, 3).hex()}
            g["slots"] = [{"enemy": e, "min": mn, "max": mx} for e, mn, mx in zip(enemies, mins, maxs)
                          if mn or mx]
            out.append(g)
        return out

    def encounters(self):
        c, r = self.cfg, self.r
        out = []
        for i in range(c["encounter_count"]):
            a = c["encounters"] + i * 0x1C
            gids = [r.u16(a + 4 + 2 * k) for k in range(8)]
            weights = [r.u8(a + 0x14 + k) for k in range(8)]
            out.append({"id": i, "rate": r.u16(a), "target_level": r.u16(a + 2),
                        # weight-0 entries are kept: whether the game can ever pick them is unverified
                        "groups": [{"group": g, "weight": w} for g, w in zip(gids, weights) if g or w]})
        return out

    def items(self):
        c, r = self.cfg, self.r
        out = []
        for i in range(c["item_count"]):
            a = c["items"] + i * 0x2C
            t, fl = r.u8(a + 2), r.u8(a + 3)
            text_id = c["item_names_text"] + i if i < c["item_named"] else None
            mask = r.u8(a + 4)
            effects = []
            for k in range(4):
                et, ev = r.u8(a + 0x18 + 4 * k), r.s8(a + 0x19 + 4 * k)
                if et:
                    effects.append({"effect": et, "value": ev})
            el = r.u32(a + 0x14)
            out.append({
                "id": i, "name_text_id": text_id, "name": self.name(text_id),
                "price": r.u16(a), "type": t, "type_label": ITEM_TYPES.get(t),
                "flags": fl, "flag_labels": [v for b, v in ITEM_FLAGS.items() if fl & b],
                "equippable_by": [PC_NAMES[b] for b in range(8) if mask >> b & 1], "equip_mask": mask,
                "unk_05": r.u8(a + 5), "icon": r.u16(a + 6),
                "attack": r.u16(a + 8), "defense": r.u8(a + 0x0A),
                "unleash_rate": r.u8(a + 0x0B), "unleash_ability": r.u16(a + 0x0E),
                "unleash_name": self.aname(r.u16(a + 0x0E)),
                "use_type": r.u8(a + 0x0C), "unk_0d": r.u8(a + 0x0D),
                "element": el, "element_name": ELEMENTS[el] if el < 5 else None,
                "equip_effects": effects,
                "use_ability": r.u16(a + 0x28), "use_ability_name": self.aname(r.u16(a + 0x28)),
                "unk_2a": r.u16(a + 0x2A),
                "named": i < c["item_named"],
            })
        return out

    def ability_brief(self, aid):
        """Raw ability record (16 bytes in GS1, 12 in GS2; decoded by gs_abilities)."""
        c = self.cfg
        if not (0 < aid < c["ability_count"]):
            return None
        return self.r.raw(c["abilities"] + aid * c["ability_stride"], c["ability_stride"]).hex()

    def psynergy_items(self, items):
        out = []
        for it in items:
            if it["type"] == 6:
                out.append({"item": it["id"], "name": it["name"], "use_ability": it["use_ability"],
                            "grants_psynergy": it["use_ability_name"], "equip_mask": it["equip_mask"],
                            "ability_raw": self.ability_brief(it["use_ability"])})
        return out

    def characters(self):
        c, r = self.cfg, self.r
        pr_table = [{"level": k, "power": r.s16(c["elvl_power"] + 4 * k),
                     "resist": r.s16(c["elvl_power"] + 4 * k + 2)} for k in range(16)]
        exp = []
        ex = self.evidence.get("exp_table") or self.find_exp_table()
        if ex:
            a = int(ex["address"], 16)
            prev = -1
            for k in range(100):
                v = r.u32(a + 4 * k)
                if v < prev or v > 10_000_000:
                    break
                exp.append(v)
                prev = v
        pcs = []
        for i in range(c["pc_count"]):
            a = c["pcs"] + i * 0xB4
            stat = lambda off: [r.u16(a + off + 2 * k) for k in range(6)]
            base_el = [r.u8(a + 0x92 + e) for e in range(4)]
            items = [r.u16(a + 0x98 + 2 * k) & 0x1FF for k in range(13)]
            pc = {
                "id": i, "name": PC_NAMES[i],
                "present": any(r.raw(a + 0x50, 0x48)),
                "stat_anchors_lv0_20_40_60_80_100": {
                    "hp": stat(0x50), "pp": stat(0x5C), "attack": stat(0x68), "defense": stat(0x74),
                    "agility": stat(0x80), "luck": [r.u8(a + 0x8C + k) for k in range(6)],
                },
                "base_elemental_x10": dict(zip(ELEMENTS, base_el)),
                "base_elemental": {
                    ELEMENTS[e]: {"level": v // 10,
                                  "power": pr_table[min(v // 10, 15)]["power"] + v % 10,
                                  "resist": pr_table[min(v // 10, 15)]["resist"] + v % 10}
                    for e, v in enumerate(base_el)},
                "start_level": r.u16(a + 0x96),
                "start_items": [x for x in items if x],
                "unk_00_4f_nonzero": any(r.raw(a, 0x50)),
            }
            pc["start_item_names"] = [self.name(c["item_names_text"] + x) if x < c["item_named"] else None
                                      for x in pc["start_items"]]
            pcs.append(pc)
        return {"pcs": pcs, "elemental_level_table": pr_table, "exp_table": exp,
                "summons": self.summons(), "classes_raw": self.classes_raw()}

    def summons(self):
        c, r = self.cfg, self.r
        out = []
        for i in range(c["summon_count"]):
            a = c["summons"] + i * 8
            out.append({"id": i, "ability": r.u32(a), "ability_name": self.aname(r.u32(a)),
                        "djinn_needed": {ELEMENTS[e]: r.u8(a + 4 + e) for e in range(4)}})
        return out

    def classes_raw(self):
        """Class table (0x54 each). Decoded fields: type, elemental-level requirement, stat multipliers (x10%),
        3 weakness bytes at +0x50. The 0x10..0x4F block (ability list) is kept as raw u16 words."""
        c, r = self.cfg, self.r
        out = []
        for i in range(c["class_count"]):
            a = c["classes"] + i * 0x54
            out.append({
                "id": i, "class_type": r.u32(a),
                "element_levels": {ELEMENTS[e]: r.u8(a + 4 + e) for e in range(4)},
                "stat_pct": dict(zip(["hp", "pp", "attack", "defense", "agility", "luck"],
                                     [r.u8(a + 8 + k) * 10 for k in range(6)])),
                "words_10_4f": [r.u16(a + 0x10 + 2 * k) for k in range(32)],
                "weaknesses": [r.u8(a + 0x50 + k) for k in range(3)],
            })
        return out

    # ---------- driver ----------
    def run(self):
        self.verify()
        ws = self.rom.workspace / "data"
        ws.mkdir(parents=True, exist_ok=True)
        c = self.cfg
        meta = {"rom": self.rom.code, "sha1": self.rom.sha1, "tables": self.evidence,
                "names_from": "text/strings.json" if self.strings else None}
        enemies = self.enemies()
        items = self.items()
        files = {
            "enemies.json": {**meta, "count": len(enemies), "stride": c["enemy_stride"],
                             "elemental_table": self.elemental(), "enemies": enemies},
            "encounters.json": {**meta, "encounters": self.encounters(), "groups": self.groups()},
            "items.json": {**meta, "count": len(items), "named_count": c["item_named"],
                           "psynergy_items": self.psynergy_items(items), "items": items},
            "characters.json": {**meta, **self.characters()},
        }
        for fn, obj in files.items():
            (ws / fn).write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")
        return ws, {k: (len(v.get("enemies", v.get("items", v.get("pcs", v.get("encounters", []))))))
                    for k, v in files.items()}


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    for path in argv:
        rom = Rom.load(path)
        ws, counts = GsUnits(rom).run()
        print(f"{rom.code}: wrote {ws}  {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
