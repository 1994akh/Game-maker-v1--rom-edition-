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


from .gs_maps import flag_scope  # noqa: E402


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


# ---------------------------------------------------------------------------------------------------------------
# GS2 (Lost Age) field-Psynergy handlers, 14 Oct second pass (notes\gs_field_psynergy.md section 12).
# Routines from the compare chains 0x080DB4B8 (empty) / 0x080DB670 (targeted) and the end-of-effect table 0x080DB8A0.
# "target" routines of ids 18-26 are 8-byte wrappers that store the target and fall into the "empty" routine.
# Engine helpers named below (GS2, Ghidra decompile, VERIFIED unless the field says INFERRED):
#   0x080CE31C target resolve, 0x080CE458 event search (phase word, field id, target), 0x080CEAFC run event,
#   0x080CDA84 position ahead within the field id's range, 0x080CDAC0 actor range test, 0x080DBB78 terrain cell,
#   0x080DC10C spawn effect object (sprite id), 0x081C0010 sound, 0x08013560 wait n frames, 0x080E8B44 screen shake.
# ---------------------------------------------------------------------------------------------------------------
GS2_EFFECT_HIT_RULE = (
    "GS2 phase-5 (effect-hit) events are looked up once when the effect starts (0x080CE458(0x50000005, field id, "
    "0x080CE31C target)) and then RUN EVERY FRAME while the effect animates: 0x080CEAFC(event, stage, frame). "
    "stage is the effect's own progress value; frame counts up and the last call passes 999 (Burst) or the loop "
    "ends when the effect task reports 999. The script is a per-frame callback, not a one-shot: a rebuild should "
    "give it on_effect_frame(stage, frame) and on_effect_end(). VERIFIED call sites: Pound 0x080E5D5C, Scoop "
    "0x080E68D0, Burst 0x080E572C, Parch 0x080E7844, Hover 0x080E9AF4, Grind 0x080E92B4, Cyclone helper 0x080E249C.")

GS2_FIELD_SPEC = {
    7: dict(name="Lift", routines=dict(target="0x080DDDA0", empty="0x080DDEA8"),
            effect="Same code as GS1 (same sounds 0x86/0x82, 15-frame waits, constants; only relocated): two hands "
                   "(effect object 0x2A1; GS1 0x11D) raise the boulder actor 24 px (empty cast: 14 px and drop). "
                   "The phase-0 script then moves or removes it.",
            differences="GS2 targets only actors that have a Lift event (GS1 any nearest actor); range 17 px. "
                        "GS1 7 events, GS2 19 (all phase 0) on sprite 329.",
            html5="LiftFieldPsynergy: destination_y_pos (default tile_y - 2) and destination_collision_layer "
                  "(default +1) are per-object data; in the ROM the script decides where the rock goes."),
    11: dict(name="Carry", routines=dict(target="0x080DF1FC", empty="0x080DF6F4"),
             effect="Same code as GS1 (sounds 0x87/0x83/0x82/0x72/0xAF, 15/10-frame waits): hand object 0x2A1 lifts "
                    "the actor and sets it down 16 px (0x100000) steps away along the facing.",
             differences="GS2 has 7 events (2 phase 1 'pre', 5 phase 0) vs GS1 18; GS2 event-only targeting."),
    13: dict(name="Catch", routines=dict(target="0x080E03C4", empty="0x080E03CC"),
             effect="Same code as GS1 (sounds 0x8A/0x84/0x72, waits 1/10/15/20): hand object 0x116 flies to the far "
                    "actor (range 49 px, dy 48) and pulls it back. GS1 has one extra call 0x08096C80(0xD7).",
             differences="GS2: 2 events only."),
    17: dict(name="Lash", routines=dict(target="0x080E0978", empty="0x080E09C0"),
             acts_on="rope post actors (sprite 407) listed in the ROPE TABLE",
             effect="Target routine looks the actor up in the rope table *(0x0300009C)+0x0C: 8 records x 0x20 bytes "
                    "{s16 post_a, s16 post_b, ..., +0x10 s16 segments drawn, +0x1C active}; filled by room scripts. "
                    "Not listed -> fail flag (+0x20 = 1): the lash hand (object 0x16B) rises and falls, nothing tied. "
                    "Listed -> rope index/posts stored at field state +0xD31..+0xD33; the hand rises 16 frames, "
                    "sound 0x84, then a per-frame task; on contact sound 0x200 and 0x080D92D4(rope, post_a, post_b) "
                    "draws the rope from post A to post B 8 px above them in distance-proportional segments, "
                    "sound 0x18B.",
             timing="10 + 16 frames rise, 6-frame pause, rope drawn over the following task frames",
             persistence="the phase-0 Lash script sets the event's flag; room init re-ties ropes from flags "
                         "(flag scope per event in rooms[].events[].flag_scope)",
             html5="LashFieldPsynergy + RopeDock objects (is_starting_dock, dest_x/dest_y, tied): same model "
                   "(a pair of docks); html5 keeps the pairing on the dock object, the ROM in the rope table."),
    18: dict(name="Pound", routines=dict(target="0x080E5D54", empty="0x080E5D5C"),
             acts_on="pillar actors (sprites 406, 411) ahead, range 33 px, cone 45 deg, dy 12",
             effect="Effect object 0x160 (fist) above the target; aborted if another solid actor (flag byte +0x59 "
                    "bit 0) overlaps the hit point (0x080DBE80). Phase-5 event per frame with (hit stage, frame). "
                    "The script sinks the pillar (82 of 85 events are phase 5).",
             persistence="usually a 0x2xx/0x3xx flag: pillars pop back up on re-entry (see flag_scope_counts)",
             html5="PoundFieldPsynergy shrinks the sprite, sets collision on tiles of events 'active at direction' "
                   "and allow_jumping_over; the ROM does the height change in the per-frame script."),
    19: dict(name="Tremor", routines=dict(target="0x080E8DB0", empty="0x080E9090"),
             acts_on="actors (range 33, cone 45 deg, dy 16)",
             effect="Horizontal screen shake 0x080E8B44(mode 1), sound 0x98, 10-frame waits; no effect-hit lookup. "
                    "The phase-0 event on the targeted actor (10 of 11) runs after the shake: loose objects fall. "
                    "INFERRED purpose"),
    20: dict(name="Scoop", routines=dict(target="0x080E68C8", empty="0x080E68D0"),
             acts_on="tile ahead 16 px (dirt spots; vertical 0)",
             effect="Effect object 0x161 digs; sounds 0x8A, 0x84, 0x72. With a phase-5 event: per-frame call "
                    "(stage, frame) where stage = 1 only at frame 30 and 2 only at frame 50 (else 0). With no "
                    "event but diggable ground (state +0x1938 == 1): at frame 24, 0x080E716C pops object 0x1E9 "
                    "with a random find (75%: one of 16 u16 entries of the table at literal 0x080E7234; "
                    "else coins). INFERRED: the random-find details",
             reference="gs2_scoop_stage(frame)"),
    21: dict(name="Burst", routines=dict(target="0x080E5724", empty="0x080E572C"),
             acts_on="tile ahead 16 px (cracked rock)",
             effect="Explosion effect, sound 0x82; phase-5 event per frame (stage, frame), last call frame = 999. "
                    "62 events: 38 phase 5, 12 phase 0, 12 phase 8 (override)."),
    22: dict(name="Parch", routines=dict(target="0x080E783C", empty="0x080E7844"),
             acts_on="water cell 32 px ahead (range 33, vertical 0)",
             effect="0x080CDA84 gives the point ahead; 0x080DBD5C(x, z, layer) tests the cell (water); "
                    "0x080DBDC8 reads its event id -> phase-5 lookup. Outcome 0 = nothing there, 1 = water but no "
                    "event, 2 = event. Sounds 0x8C, 0x82, 0x21E. All 15 events phase 5: the script lowers the "
                    "water / changes tiles."),
    23: dict(name="Sand", routines=dict(target="0x080E4A2C", empty="0x080E4A34", end_of_effect="0x080E4730"),
             acts_on="anywhere; works only on sand terrain",
             effect="0x080DBCD8(x, z) = terrain cell kind 2 (0x080DBB78) under the player; state +0xD48 = 1 when "
                    "NOT on sand (fail animation). The player spins (+0x2000 facing per frame, 40 frames, sound "
                    "0x236); at frame 60 the sprite becomes 0xFB (sand mound), sound 0x88. "
                    "End of effect 0x080E4730: phase-4 event lookup (0x40000005) for the cell, run with "
                    "(event, +0x18, -1); the leader's sprite comes back from state +0x214, lifted 10 px, sounds "
                    "0x220/0x21B. 55 events: 28 phase 0 (sand spots that do something while sanded), 27 phase 4 "
                    "(where you surface).",
             html5="SandFieldPsynergy: tile property allow_sand + a separate sand collision layer; ROM uses a "
                   "terrain kind and phase-4 events instead of a second collision map."),
    24: dict(name="Hover", routines=dict(target="0x080E9AEC", empty="0x080E9AF4", end_of_effect="0x080E9DB4"),
             acts_on="anywhere (6 events)",
             effect="Phase-5 lookup at the start; player anim 5, raised, sound 0x82. Fails (sound 0xF6, comes "
                    "down in 32 frames) when 0x080DBCC0 rejects the cell or a solid actor overlaps. Otherwise the "
                    "phase-5 script runs once (event, +0x18, +0x1A) and the hover task runs until it ends. "
                    "End of effect 0x080E9DB4 (the 0x2000 cast): sinks the player to the ground, at most 60 frames, "
                    "sound 0x84, then 2 x 20-frame settles; phase-2 events (2) run then.",
             persistence="none (state only while floating)"),
    25: dict(name="Cyclone", routines=dict(target="0x080E306C", empty="0x080E3074"),
             acts_on="grass/bush cells around the player (no actor targeting; range 1, cone 0)",
             effect="Whirl object 0x118 on the player, BG whirl distortion (0x080E2A68), sounds 0x88/0xCF; the "
                    "helper 0x080E249C (called 3 times) checks terrain cells (0x080DBB78) and looks up the "
                    "phase-5 events of the cut cells (all 140 events are phase 5). INFERRED: radius."),
    26: dict(name="Blaze", routines=dict(target="0x080E3CFC", empty="0x080E3D04"),
             acts_on="torch actors (sprites 364, 365, 418, 419, 489), range 17, dy 64",
             effect="Looks for a torch actor among the 80 slots (0x080CDAC0); flame objects 0x16E/0x16F, sounds "
                    "0xBA, 0xCF, 0x18B. Looks up phase 6 (0x60000005) and phase 2 (0x20000005) events: phase 6 "
                    "= the torch is lit, phase 2 = already lit / end. 47 events: 21 phase 1, 11 phase 2, "
                    "7 phase 0, 8 phase 6."),
    27: dict(name="Grind", routines=dict(target="0x080E92B4", empty="0x080E97C8"),
             acts_on="rock actor (sprite 424) or tile, range 33, cone 45 deg",
             effect="Vertical screen shake 0x080E8B44(mode 2), sounds 0xEE/0x186; 0x080E9250 scrolls map rows "
                    "(DMA) for the grinding look; phase-5 event per frame (8 of 19 events), phase 0 for 11."),
    30: dict(name="Teleport", routines=dict(target="0x080E7818", empty="0x080E781C"),
             acts_on="the cell UNDER the player (0x080CB144) - teleport pads",
             effect="No engine effect: the routine only calls 0x080CDF5C (a getter) and returns. Everything is the "
                    "phase-0 script of the pad (14 events): it warps to the paired pad."),
}


def gs2_scoop_stage(frame):
    """Stage value passed to Scoop's phase-5 script on effect frame `frame` (GS2 0x080E68D0, VERIFIED)."""
    return 1 if frame == 30 else 2 if frame == 50 else 0


FLAG_SCOPES = {
    "visit": "0x80-0xDF: cleared on every room entry",
    "room": "0x200-0x2FF: cleared on every room entry (puzzle resets when the room is re-entered)",
    "place_group": "0x300-0x3FF: cleared when entering a room of another place group (room table byte 2)",
    "view": "0x164/0x165: set by Scene_AssignViewFlags for camera-streamed actors",
    "saved": "everything else: kept and saved (the 0x200-byte flag block at 0x02000040 is in the save)",
    "source": "VERIFIED GS1 0x0808AB74 / GS2 0x080C9C38 (Scene_ResetFlagsOnEnter; alchemy SRC/FIELD/COMMON/FIELD4.C)"}

# Object kind by the Psynergy that targets a sprite (INFERRED labels; the field ids are VERIFIED event data).
KIND_BY_FIELD = {1: "pushable (Move: pillar, statue, log, crate)", 6: "puddle (Frost -> ice pillar)",
                 12: "sprout (Growth -> vine)", 7: "boulder (Lift)", 11: "carryable (Carry)",
                 4: "Force target (pillar, tree, bell)", 5: "Douse target", 13: "far item (Catch)",
                 14: "Whirlwind target (leaves, bush)", 9: "Halt target (moving object)", 3: "Ply target",
                 17: "rope post (Lash)", 18: "pillar (Pound)", 19: "Tremor target", 26: "torch (Blaze)",
                 27: "rock (Grind)", 2: "NPC (Mind Read)"}


def object_kind(field_ids):
    fids = {int(k): v for k, v in field_ids.items()}
    puzzle = {k: v for k, v in fids.items() if k != 2}
    if puzzle:
        return KIND_BY_FIELD.get(max(puzzle, key=puzzle.get), f"field id {max(puzzle, key=puzzle.get)}")
    return KIND_BY_FIELD[2] if fids else None


def _collision(base, area, cache):
    if area not in cache:
        p = os.path.join(base, "maps", "areas", f"area_{area:03d}", "collision.json")
        cache[area] = load_json(p) if os.path.exists(p) else None
    return cache[area]


def resolve_target(d, e, r, base, coll_cache, spr_dir, res, obj_types):
    """Attach the event's target object: the actor row (placement table or script-spawned table) for actor events,
    the collision cells carrying the event id for tile events."""
    kind = d["target_kind"]
    if kind == "anywhere":
        res["anywhere"] += 1
        return
    if kind == "actor":
        res["actor"] += 1
        ref = e.get("actor")
        if not ref:
            d["target"] = dict(resolved=False, slot=e.get("actor_slot", d["target_id"]))
            return
        if ref["source"] == "party":
            d["target"] = dict(resolved=True, slot=ref["index"], party_member=True)
            res["actor_resolved"] += 1
            return
        rows = r.get("actors", []) if ref["source"] == "placements" else [
            a for a in r.get("actors_spawned", []) if a.get("table") == ref.get("table")]
        a = next((x for x in rows if x["index"] == ref["index"]), None)
        if a is None:
            d["target"] = dict(resolved=False, slot=e.get("actor_slot"))
            return
        res["actor_resolved"] += 1
        png = os.path.join(spr_dir, f"{a['sprite_id']:04d}.png")
        d["target"] = dict(resolved=True, slot=a["slot"], source=a["source"], table=a.get("table"), row=a["index"],
                           sprite=a["sprite"], sprite_id=a["sprite_id"],
                           sprite_png=os.path.relpath(png, base).replace("\\", "/") if os.path.exists(png) else None,
                           x=a["x"], y=a["y"], z=a["z"], tile=a["tile"], angle=a["angle"],
                           condition=a["condition"], behavior=a.get("behavior"))
        t = obj_types.setdefault(a["sprite_id"], dict(field_ids={}, events=0, rooms=[], sprite_png=d["target"]["sprite_png"]))
        if d["field_id"] is not None:
            t["field_ids"][str(d["field_id"])] = t["field_ids"].get(str(d["field_id"]), 0) + 1
        t["events"] += 1
        if r["room"] not in t["rooms"]:
            t["rooms"].append(r["room"])
        return
    res["tile"] += 1
    col = _collision(base, r.get("area"), coll_cache) if r.get("area") is not None else None
    cells = []
    for L in (col or {}).get("layers", []):
        for y, row in enumerate(L["event"]):
            for x, v in enumerate(row):
                if v == d["target_id"]:
                    cells.append([L["layer"], x, y])
    if cells:
        res["tile_resolved"] += 1
        xs, ys = [c[1] for c in cells], [c[2] for c in cells]
        d["target"] = dict(resolved=True, cells_layer_x_y=cells[:64], n_cells=len(cells),
                           bbox_tiles=[min(xs), min(ys), max(xs) + 1, max(ys) + 1],
                           note="tile coords are per collision layer window (collision.json grid_x/grid_y)")
    else:
        d["target"] = dict(resolved=False, tile_event_id=d["target_id"])


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
    res = dict(actor=0, actor_resolved=0, tile=0, tile_resolved=0, anywhere=0)
    obj_types, coll_cache = {}, {}
    spr_dir = os.path.join(base, "battle_sprites", "sprites")
    for f in sorted(glob.glob(os.path.join(base, "maps", "rooms", "*", "events.json"))):
        r = load_json(f)
        evs = []
        for e in r.get("events", []):
            if e["type"] & 0xF != 5:
                continue
            d = decode_event(e, abilities, g)
            d["flag_scope"] = flag_scope(d["flag"])
            resolve_target(d, e, r, base, coll_cache, spr_dir, res, obj_types)
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
                fs = d.get("flag_scope")
                fs = fs.get("scope", str(fs)) if isinstance(fs, dict) else str(fs)
                p.setdefault("flag_scope_counts", {})[fs] = p.get("flag_scope_counts", {}).get(fs, 0) + 1
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
        if g == "gs2" and fid in GS2_FIELD_SPEC:
            p["gs2_handler_spec"] = GS2_FIELD_SPEC[fid]
    out = dict(game=g, rom_code=c["slug"][:4], generator="gbax.codecs.gs_field",
               spec="notes/gs_field_psynergy.md", code=c["code"], phases=PHASES,
               targeting_rule=targeting["rule"], targeting_table=targeting["table"],
               targeting_default=targeting["default"],
               coverage=dict(field_ids=len(psy), psynergy_events=n_ev, events_with_known_field_id=n_ev - n_unmatched,
                             rooms_with_events=len(rooms_out),
                             field_ids_with_effect_routines=sum(1 for v in psy.values() if v["effect_routines"])),
               field_psynergy=[psy[k] for k in sorted(psy)], rooms=rooms_out)
    out["coverage"]["targets"] = res
    out["flag_scopes"] = FLAG_SCOPES
    if g == "gs2":
        out["effect_hit_callback"] = GS2_EFFECT_HIT_RULE
    out["object_types"] = [dict(sprite_id=k, kind=object_kind(v["field_ids"]), **v)
                           for k, v in sorted(obj_types.items())]
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
