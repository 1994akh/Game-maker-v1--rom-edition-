"""Golden Sun 1/2 field Psynergy: tables, map-event decoder and reference rules.

Usage (from C:\\Users\\aaron\\Documents\\UnboundHack):
    .venv\\Scripts\\python.exe -m gbax.codecs.gs_field [gs1|gs2|all]

Writes games\\<slug>\\data\\field_psynergy.json for each game. Inputs (read-only):
  * the ROM (ability table, targeting table, effect-handler tables are read from ROM bytes / code),
  * games\\<slug>\\data\\abilities.json and items.json (names; gs_abilities / gs_units exports),
  * games\\<slug>\\maps\\rooms\\*\\events.json (map-code event tables; gs_maps export),
  * games\\<slug>\\text\\strings.json (Mind Read and other text-id events).

Spec and evidence: notes\\gs_field_psynergy.md.  Addresses are ROM addresses (0x08xxxxxx).
"""
import glob
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GAMES = {
    "gs1": dict(
        slug="AGSE-5c469520-Golden-Sun-USA-Europe",
        rom=os.path.join(ROOT, "games", "AGSE-5c469520-Golden-Sun-USA-Europe", "rom", "Golden Sun (USA, Europe).gba"),
        ability_table=0x0807EE58, ability_stride=16, ability_count=519, field_off=12,
        # targeting: {s16 field_id, s16 range_px} pairs, -1 terminated; default range 16 px (0x0808DDB8)
        range_table=0x0809E686, range_format="pairs",
        # per-field-id effect routines: jump tables indexed by field_id-1 (16 entries)
        effect_empty_table=0x08096838, effect_target_table=0x0809698C, effect_count=16,
        code=dict(
            cast="0x0808E680 (request value: ability | caster<<10 | 0x2000 end-of-effect; from field state +0x17E)",
            end_of_effect_cast="0x0808E5D8 (phases 3 then 2, no PP; e.g. 0x0808E118 calls it with 0x2090 = Reveal ends)",
            event_search="0x0808E4B4(phase_type, field_id, &target)",
            actor_target="0x0808DF1C(player_slot, field_id)",
            range_lookup="0x0808DDB8(field_id)",
            tile_ahead="0x0808BD24 (cell byte 2, 16 px ahead along facing)",
            flag_test="0x0808D428 (FFFF always; bit 0x1000 -> active while set; else active while clear)",
            cast_visual="0x08096FB0(ability, 0) -> 0x080970F8(player, target) -> 0x0809728C",
            effect_empty="0x08096810 (jump table 0x08096838)",
            effect_target="0x08096960 (jump table 0x0809698C)",
            effect_after="0x08096AB0 (Mind Read only)",
            effect_end="0x08097194",
            run_event="0x08096B28(event, caster, target): script<0x10000 -> text box, else call script(caster, target)",
            shortcut="0x0800EAF8 (buttons at key map 0x02000240+0x218/+0x21A -> stored values at +0x220/+0x222) -> 0x0800EA60",
            item_use="0x0808E23C(item | holder<<10, ...) from field state +0x180",
            field_loop="0x0808C4F8 (reads requests +0x17E cast, +0x180 item)",
            move_dpad_table="0x0809F0F8 (4 directions only; diagonals = 0xFFFF)",
        ),
    ),
    "gs2": dict(
        slug="AGFE-b5006632-Golden-Sun-The-Lost-Age-USA-Europe",
        rom=r"C:\Users\aaron\OneDrive\Apps-Roms\Golden Sun - The Lost Age (USA, Europe).gba",
        ability_table=0x080B7C14, ability_stride=12, ability_count=734, field_off=6,
        # targeting: 8-byte records {s16 field_id, s16 range_px, s16 vertical_px, s16 cone}, the -1 record is the default
        range_table=0x080EFF28, range_format="records8",
        # per-field-id effect routines: compare chains (cmp rX,#id / bne / bl handler)
        effect_empty_chain=0x080DB4B8, effect_target_chain=0x080DB670,
        effect_after_table=0x080DB8A0,  # FUN_080DB884: jump table on field_id-8, 21 entries
        code=dict(
            cast="0x080CE61C (same request encoding as GS1)",
            end_of_effect_cast="0x080CE574 (phases 3 then 2)",
            target_resolve="0x080CE31C(field_id): tile id / actor|0x100 / 0x200 anywhere / -1",
            event_search="0x080CE458(phase_type, field_id, target)",
            actor_range="0x080CDAC0(field_id, player, actor); record lookup 0x080CDA58",
            flag_test="0x080CCD48",
            cast_visual="0x080DC410(ability, 0) -> 0x080DC62C(player, target)",
            effect_empty="0x080DB4B8 (compare chain)",
            effect_target="0x080DB670 (compare chain)",
            effect_end_of_effect="0x080DB884 (jump table 0x080DB8A0; ids 8,10,16,23,24,28)",
            run_event="0x080CEAFC",
            shortcut="0x08026E60 -> 0x08026DD0 (two call sites = two shortcut slots)",
        ),
    ),
}

PHASES = {
    0: "main: runs after the cast animation (the puzzle script / Mind Read text)",
    1: "pre: runs before the targeted animation",
    2: "end-of-effect (second): run by the 0x2000 end-of-effect cast",
    3: "end-of-effect (first): run by the 0x2000 end-of-effect cast",
    4: "Reveal view: looked up by GS1 0x080984C0 with field id 8 (objects shown while Reveal is active)",
    5: "effect-hit: looked up by the effect routine when the visual lands (Frost 0x080992A4, Force 0x08098FBE, Reveal 0x0809840A)",
    8: "GS2 override (0x80000005): checked first by 0x080CE61C; if found it replaces the normal cast",
}


def _rom(path):
    with open(path, "rb") as f:
        return f.read()


def _u16(b, a):
    return struct.unpack_from("<H", b, a - 0x08000000)[0]


def _s16(b, a):
    return struct.unpack_from("<h", b, a - 0x08000000)[0]


def _u32(b, a):
    return struct.unpack_from("<I", b, a - 0x08000000)[0]


def read_abilities(g, rom):
    """{ability_id: dict(field_id, pp, element)} for abilities with a field id (from ROM bytes)."""
    c = GAMES[g]
    out = {}
    for i in range(c["ability_count"]):
        a = c["ability_table"] + i * c["ability_stride"]
        fid = rom[a - 0x08000000 + c["field_off"]]
        if fid:
            out[i] = dict(field_id=fid, element=rom[a - 0x08000000 + 2], pp=rom[a - 0x08000000 + 9],
                          target=rom[a - 0x08000000], flags=rom[a - 0x08000000 + 1])
    return out


def read_targeting(g, rom):
    """Targeting parameters per field id. GS1 vertical/cone values are code constants of 0x0808DF1C."""
    c = GAMES[g]
    a = c["range_table"]
    rows = {}
    if c["range_format"] == "pairs":
        while _s16(rom, a) != -1:
            rows[_s16(rom, a)] = dict(range_px=_s16(rom, a + 2))
            a += 4
        default = dict(range_px=16, vertical_px=8, cone_near=0x1800, cone_far=0x1000)
        vert = {13: 48, 5: 64, 2: 16}            # 0x0808DF1C: Catch 0x300000, Douse 0x400000, Mind Read 0x100000
        for fid, r in rows.items():
            r["vertical_px"] = vert.get(fid, 8)
            r["cone_near"] = 0x2000 if fid == 2 else 0x1800
            r["cone_far"] = 0x2000 if fid == 2 else 0x1000
        for fid in vert:
            rows.setdefault(fid, dict(range_px=16, vertical_px=vert[fid], cone_near=0x1800, cone_far=0x1000))
        rule = ("range: nearest actor with dist < range (dist = sqrt(dx^2+dz^2) px; actors with flag 0x1000 count "
                "dist*2/3); |dy| <= vertical; if dist > 11 px the bearing must be within cone of facing snapped "
                "to 4 directions ((facing+0x2000)&0xC000); cone_near if dist <= 19 px else cone_far; actors with "
                "flag 0x800 are skipped. Picks any actor (not only actors that have an event).")
    else:
        while True:
            fid, rng, vert, cone = struct.unpack_from("<4h", rom, a - 0x08000000)
            if fid == -1:
                default = dict(range_px=rng + 1, vertical_px=vert, cone_near=cone & 0xFFFF,
                               cone_far=(cone * 2 // 3) & 0xFFFF)
                break
            rows[fid] = dict(range_px=rng + 1, vertical_px=vert, cone_near=cone & 0xFFFF,
                             cone_far=(cone * 2 // 3) & 0xFFFF)
            a += 8
        rule = ("0x080CDAC0: |dy| <= vertical (Pound, id 18, compares floor heights +0x14 instead); dist <= range "
                "(x1.5 for actors with flag 0x1000); dist < 12 px always hits; else the bearing must be within "
                "cone of the 4-way facing, cone*2/3 when dist > 19 px. Only actors that HAVE a Psynergy event for "
                "this field id are candidates (0x080CE31C); a tile event on the tile ahead wins over actors.")
    return dict(table=f"0x{c['range_table']:08X}", default=default, by_field_id=rows, rule=rule)


def read_effect_handlers(g, rom):
    """field_id -> {'empty': addr, 'target': addr}: the per-Psynergy visual/effect routines."""
    c = GAMES[g]
    out = {}
    if "effect_empty_table" in c:
        for i in range(c["effect_count"]):
            out[i + 1] = dict(empty_case=f"0x{_u32(rom, c['effect_empty_table'] + 4 * i):08X}",
                              target_case=f"0x{_u32(rom, c['effect_target_table'] + 4 * i):08X}")
        # the call made by each case (first BL in the case block)
        for fid, d in out.items():
            for k in ("empty_case", "target_case"):
                d[k.replace("_case", "_routine")] = _first_bl(rom, int(d[k], 16))
        return out
    for key, addr in (("empty_routine", c["effect_empty_chain"]), ("target_routine", c["effect_target_chain"])):
        for fid, tgts in _compare_chain(rom, addr).items():
            if tgts:
                out.setdefault(fid, {})[key] = f"0x{tgts[0]:08X}"
    for i in range(21):
        tgt = _u32(rom, c["effect_after_table"] + 4 * i)
        bl = _first_bl(rom, tgt)
        if bl:
            out.setdefault(i + 8, {})["end_of_effect_routine"] = bl
    return out


def _first_bl(rom, addr, limit=24):
    a = addr & ~1
    for _ in range(limit):
        h1 = _u16(rom, a)
        if (h1 & 0xF800) == 0xF000:
            h2 = _u16(rom, a + 2)
            if (h2 & 0xF800) == 0xF800:
                o = ((h1 & 0x7FF) << 12) | ((h2 & 0x7FF) << 1)
                if o & 0x400000:
                    o -= 0x800000
                return f"0x{a + 4 + o:08X}"
        if (h1 & 0xF800) == 0xE000 or h1 == 0x4770:   # b / bx lr: end of the case block
            return None
        a += 2
    return None


def _compare_chain(rom, start, n=420):
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    ins = list(md.disasm(rom[start - 0x08000000:start - 0x08000000 + n * 2], start))
    res = {}
    for i, x in enumerate(ins[:-1]):
        if x.mnemonic == "cmp" and "#" in x.op_str and ins[i + 1].mnemonic == "bne":
            imm = int(x.op_str.split("#")[1], 0)
            bls = []
            for y in ins[i + 2:]:
                if y.mnemonic in ("b", "pop", "cmp"):
                    break
                if y.mnemonic == "bl":
                    bls.append(int(y.op_str.strip("#"), 0))
            res.setdefault(imm, bls)
        if x.mnemonic == "pop" and "pc" in x.op_str:
            break
    return res


def decode_event(e, abilities, game):
    """Decode one Psynergy event (map-code event-table row, type & 0xF == 5)."""
    t, b1, b23, ev_id, flag = e["type"], e["b1"], e["b2_3"], e["id"], e["flag"]
    raw = next((e[k] for k in ("script", "text_id", "value", "pointer") if k in e), 0)
    script = int(raw, 16) if isinstance(raw, str) else int(raw or 0)
    ab = abilities.get(b1, {})
    kind = "anywhere" if t & 0x80 else ("actor" if t & 0x10 else "tile")
    d = dict(type=f"0x{t:02X}", ability=b1, field_id=ab.get("field_id"), target_kind=kind,
             target_id=None if kind == "anywhere" else ev_id & 0xFF,
             phase=(b23 >> 12) & (0xF if game == "gs2" else 0x7), phase_raw=b23 >> 12,
             suppress_generic_animation=bool(ev_id & 0x400),
             silent_cast=bool(ev_id & 0x200) if game == "gs2" else None,
             facing_required=(f"0x{ev_id & 0xF000:04X}" if ev_id & 0x800 else None),
             id_raw=f"0x{ev_id:04X}")
    if flag == 0xFFFF:
        d["condition"] = "always"
    elif flag & 0x1000:
        d["condition"] = f"while flag 0x{flag:X} is set"
    else:
        d["condition"] = f"until flag 0x{flag:X} is set"
    d["flag"] = flag
    if script < 0x10000:
        d["text_id"] = script
    else:
        d["script"] = f"0x{script:08X}"
    return d


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def export(g):
    c = GAMES[g]
    rom = _rom(c["rom"])
    base = os.path.join(ROOT, "games", c["slug"])
    abil_json = {a["id"]: a for a in load_json(os.path.join(base, "data", "abilities.json"))["abilities"]}
    abilities = read_abilities(g, rom)
    items = load_json(os.path.join(base, "data", "items.json"))
    items = items["items"] if isinstance(items, dict) else items
    sp = os.path.join(base, "text", "strings.json")
    strings = load_json(sp) if os.path.exists(sp) else {}
    targeting = read_targeting(g, rom)
    handlers = read_effect_handlers(g, rom)

    psy = {}
    for aid, a in sorted(abilities.items()):
        fid = a["field_id"]
        p = psy.setdefault(fid, dict(field_id=fid, abilities=[], items=[], events=0, events_by_kind={},
                                     events_by_phase={}, rooms=set(), examples=[]))
        p["abilities"].append(dict(id=aid, name=abil_json.get(aid, {}).get("name"), pp=a["pp"],
                                   element=a["element"], usable_in_battle=bool(a["flags"] & 0x80)))
    for it in items:
        ua = it.get("use_ability")
        if ua in abilities:
            psy[abilities[ua]["field_id"]]["items"].append(dict(id=it["id"], name=it.get("name"),
                                                                 type=it.get("type"), use_type=it.get("use_type"),
                                                                 grants=ua))
    rooms_out, n_ev, n_unmatched = [], 0, 0
    for f in sorted(glob.glob(os.path.join(base, "maps", "rooms", "*", "events.json"))):
        r = load_json(f)
        evs = []
        for e in r.get("events", []):
            if e["type"] & 0xF != 5:
                continue
            d = decode_event(e, abilities, g)
            n_ev += 1
            if d["field_id"] is None:
                n_unmatched += 1
            if "text_id" in d and str(d["text_id"]) in strings:
                d["text"] = strings[str(d["text_id"])]
            evs.append(d)
            p = psy.get(d["field_id"])
            if p is not None:
                p["events"] += 1
                p["events_by_kind"][d["target_kind"]] = p["events_by_kind"].get(d["target_kind"], 0) + 1
                p["events_by_phase"][str(d["phase_raw"])] = p["events_by_phase"].get(str(d["phase_raw"]), 0) + 1
                p["rooms"].add(r["room"])
                if len(p["examples"]) < 3 and "script" in d:
                    p["examples"].append(dict(room=r["room"], room_name=r.get("name"), **d))
        if evs:
            rooms_out.append(dict(room=r["room"], name=r.get("name"), events=evs))
    for fid, p in psy.items():
        p["rooms"] = sorted(p["rooms"])
        p["name"] = p["abilities"][0]["name"] if p["abilities"] else None
        h = handlers.get(fid, {})
        p["effect_routines"] = h
        p["targeting"] = targeting["by_field_id"].get(fid, dict(targeting["default"], note="default"))
    out = dict(game=g, rom_code=c["slug"][:4], generator="gbax.codecs.gs_field",
               spec="notes/gs_field_psynergy.md", code=c["code"], phases=PHASES,
               targeting_rule=targeting["rule"], targeting_table=targeting["table"],
               targeting_default=targeting["default"],
               coverage=dict(field_ids=len(psy), psynergy_events=n_ev, events_with_known_field_id=n_ev - n_unmatched,
                             rooms_with_events=len(rooms_out),
                             field_ids_with_effect_routines=sum(1 for v in psy.values() if v["effect_routines"])),
               field_psynergy=[psy[k] for k in sorted(psy)], rooms=rooms_out)
    path = os.path.join(base, "data", "field_psynergy.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    return path, out["coverage"]


# ---------------------------------------------------------------------------------------------------------------
# Reference rules for a native rebuild (engine-neutral; positions in px, angles u16 with 0x10000 = 360°, 0 = east,
# 0x4000 = south).  These mirror the game code named in each docstring.
# ---------------------------------------------------------------------------------------------------------------

def snap4(facing):
    """Psynergy aims along the facing snapped to 4 directions ((a + 0x2000) & 0xC000). GS1 0x080970F8."""
    return (facing + 0x2000) & 0xC000


def angle_diff(a, b):
    d = (a - b) & 0xFFFF
    return d - 0x10000 if d >= 0x8000 else d


def pick_actor_target(player, actors, tgt, gs2_candidates=None):
    """GS1 0x0808DF1C / GS2 0x080CDAC0.  player/actors: dicts with x, y, z, facing, flags.
    tgt: dict(range_px, vertical_px, cone_near, cone_far). gs2_candidates: set of actor indexes that have an event
    for this field id (GS2 only). Returns the chosen actor index or None."""
    import math
    best, best_d = None, None
    for i, a in actors.items():
        if a is player or a.get("flags", 0) & 0x800:
            continue
        if gs2_candidates is not None and i not in gs2_candidates:
            continue
        if abs(a["y"] - player["y"]) > tgt["vertical_px"]:
            continue
        d = math.hypot(a["x"] - player["x"], a["z"] - player["z"])
        if a.get("flags", 0) & 0x1000:
            d = d * 2 / 3
        if d >= tgt["range_px"] or (best_d is not None and d >= best_d):
            continue
        if d > 11:
            bearing = int(math.atan2(a["z"] - player["z"], a["x"] - player["x"]) / (2 * math.pi) * 0x10000) & 0xFFFF
            cone = tgt["cone_near"] if d <= 19 else tgt["cone_far"]
            if abs(angle_diff(bearing, snap4(player["facing"]))) >= cone:
                continue
        best, best_d = i, d
    return best


def match_event(events, field_id, phase, target, facing):
    """GS1 0x0808E4B4 / GS2 0x080CE458. events: decoded events (decode_event) whose condition already holds.
    target: ('actor', index) | ('tile', cell_event_id) | None. Returns the first matching event or None."""
    for e in events:
        if e["field_id"] != field_id or e["phase"] != phase:
            continue
        if e["facing_required"] is not None:
            if abs(angle_diff(int(e["facing_required"], 16), facing)) > 0x17FF:
                continue
        if e["target_kind"] == "anywhere":
            return e
        if target and e["target_kind"] == target[0] and e["target_id"] == target[1] & 0xFF:
            return e
    return None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    which = argv[0] if argv else "all"
    for g in (["gs1", "gs2"] if which == "all" else [which]):
        path, cov = export(g)
        print(g, path, json.dumps(cov))


if __name__ == "__main__":
    main()
