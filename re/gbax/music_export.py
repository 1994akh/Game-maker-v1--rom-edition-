"""MP2K ("Sappy") music export: one standard MIDI file per song plus a SoundFont 2, for a native engine.

Option A of the music task: drives the open-source GBA Mus Ripper (Bregalad; github.com/jpmac26/gba-mus-ripper,
cloned into external/gba-mus-ripper and built in WSL 'Ubuntu') song by song, so that

  * files are named by song-table index (mid/song_0001.mid),
  * the song table is walked by this module (the ripper's own walker stops at the first bad pointer and its
    sappy_detector finds the stale vanilla table in Pokemon Unbound),
  * every voicegroup becomes one bank of a single combined .sf2 (bank N = Nth voicegroup, sorted by address)
    and every MIDI selects its bank with CC0, so one SoundFont plays every song,
  * every track is also walked here by walk_track() (an independent MP2K command parser): the ripper's
    loopStart/loopEnd markers are checked against the GOTO of track 0 and added where the ripper's heuristic
    missed them, and rests after the last note (dropped by the ripper) are restored by moving end_of_track,
  * the SoundFont is built with the locally patched '-ku' flag so the filler square voice
    (01 3C 00 00 02 00 00 00 00 00 0F 00) that a few songs really play gets a preset, then validate_sf2() checks it,
  * each MIDI is re-parsed with mido and summarised in music_index.json (tracks, tempo, duration, loop markers).

The ROM is only ever opened for reading.

Usage (from C:\\Users\\aaron\\Documents\\UnboundHack):
    .venv\\Scripts\\python.exe -m gbax.music_export AGSE AGFE BPRE     # rip + index (slug prefixes or 'all')
    .venv\\Scripts\\python.exe -m gbax.music_export AGSE --index-only  # re-parse existing MIDIs only
Options: --rom PATH --table 0x08xxxxxx (override), --max-scan N, --songs 1,5,9 (subset), --no-sf2.
"""
import argparse
import csv
import json
import os
import re
import shutil
import struct
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RIPPER = ROOT / "external" / "gba-mus-ripper"
ROM_BASE = 0x08000000

GAMES = {
    "AGSE-5c469520-Golden-Sun-USA-Europe": {
        "title": "Golden Sun (USA, Europe)",
        "rom": ROOT / "games" / "AGSE-5c469520-Golden-Sun-USA-Europe" / "rom" / "Golden Sun (USA, Europe).gba",
        "table": 0x080FC684, "sf2": "golden_sun.sf2"},
    "AGFE-b5006632-Golden-Sun-The-Lost-Age-USA-Europe": {
        "title": "Golden Sun - The Lost Age (USA, Europe)",
        "rom": Path(r"C:\Users\aaron\OneDrive\Apps-Roms\Golden Sun - The Lost Age (USA, Europe).gba"),
        "table": 0x081C4530, "sf2": "golden_sun_the_lost_age.sf2"},
    "BPRE-b4776b82-Pokemon-Unbound-v2-1-1-1": {
        "title": "Pokemon Unbound v2.1.1.1",
        "rom": Path(r"C:\Users\aaron\OneDrive\Apps-Roms\Pokemon Unbound (v2.1.1.1).gba"),
        "table": 0x087FE000, "sf2": "pokemon_unbound.sf2"},
}

# Voice types the MP2K engine accepts as the first byte of a voicegroup entry (DirectSound, PSG, keysplit, drums).
VOICE_TYPES = {0x00, 0x01, 0x02, 0x03, 0x04, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x10, 0x18, 0x40, 0x80}


def wsl_path(p):
    p = str(Path(p).resolve())
    return "/mnt/" + p[0].lower() + p[2:].replace("\\", "/")


def sh_quote(s):
    return "'" + str(s).replace("'", "'\"'\"'") + "'"


def run_wsl_script(script_path, timeout):
    cmd = ["wsl", "-d", "Ubuntu", "-u", "root", "--", "bash", wsl_path(script_path)]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, errors="replace")


# ----------------------------------------------------------------------------------------------- song table
class RomView:
    def __init__(self, data):
        self.data = data
        self.size = len(data)

    def ptr(self, off):
        if off < 0 or off + 4 > self.size:
            return None
        v = struct.unpack_from("<I", self.data, off)[0]
        return v - ROM_BASE if ROM_BASE <= v < ROM_BASE + self.size else None


def classify_entry(rv, hdr):
    """Return (status, info) for a song header at file offset hdr. status: song / empty / invalid."""
    if hdr is None or hdr + 8 > rv.size:
        return "invalid", {}
    d = rv.data
    ntr, blocks, prio, reverb = d[hdr], d[hdr + 1], d[hdr + 2], d[hdr + 3]
    info = {"tracks": ntr, "priority": prio, "reverb": reverb}
    if ntr == 0:
        vg = rv.ptr(hdr + 4)
        info["voicegroup"] = vg + ROM_BASE if vg is not None else None
        return "empty", info
    if ntr > 16 or hdr % 4:
        return "invalid", info
    vg = rv.ptr(hdr + 4)
    tps = [rv.ptr(hdr + 8 + 4 * t) for t in range(ntr)]
    if vg is None or vg % 4 or any(t is None for t in tps):
        return "invalid", info
    if d[vg] not in VOICE_TYPES or any(d[t] < 0x80 for t in tps):
        return "invalid", info
    info["voicegroup"] = vg + ROM_BASE
    info["track_ptrs"] = [t + ROM_BASE for t in tps]
    return "song", info


def walk_song_table(rv, table, csv_rows, max_scan=2048, gap_stop=16):
    """Walk the table entry by entry. Unlike a plain walker, an invalid entry is recorded and skipped; the walk
    ends at a pointer outside the ROM or after `gap_stop` consecutive invalid entries past songs.csv."""
    entries, bad_run = [], 0
    base = table - ROM_BASE
    for i in range(max_scan):
        e = base + 8 * i
        hdr = rv.ptr(e)
        if hdr is None:
            break
        status, info = classify_entry(rv, hdr)
        ms, me = struct.unpack_from("<HH", rv.data, e + 4)
        entries.append({"id": i, "header": hdr + ROM_BASE, "status": status, "player": ms, "player2": me,
                        "in_songs_csv": i < csv_rows, **info})
        bad_run = bad_run + 1 if status == "invalid" else 0
        if i >= csv_rows and bad_run >= gap_stop:
            break
    while entries and entries[-1]["status"] == "invalid" and entries[-1]["id"] >= csv_rows:
        entries.pop()
    return entries


# ----------------------------------------------------------------------------------------------- MP2K track walker
# W00..W96 (0x80..0xB0) wait lengths in MP2K ticks (24 ticks per quarter note = the ripper's MIDI PPQN)
WAIT_TICKS = list(range(25)) + [28, 30, 32, 36, 40, 42, 44, 48, 52, 54, 56, 60, 64, 66, 68, 72, 76, 78, 80, 84, 88,
                                90, 92, 96]
XCMD_ARGS = {0x01: 4, 0x0C: 2, 0x0D: 4}            # other XCMD sub-commands take one byte


def walk_track(data, start, max_cmds=500000):
    """Walk one MP2K track as the engine does (running status for commands >= 0xBD, PATT/PEND up to 3 deep) and
    return {"end": "fine"|"goto"|"error", "ticks": ticks until FINE/GOTO, "loop_start_tick": tick at which the main
    track first reached the GOTO target (None if no loop), "notes": note commands executed}. Independent of the
    ripper: used to check / add its loopStart and loopEnd markers."""
    rv = RomView(data)
    pos, tick, last, notes, stack, seen = start, 0, None, 0, [], {}

    def res(end, **kw):
        return {"end": end, "ticks": tick, "notes": notes, "loop_start_tick": None, **kw}

    for _ in range(max_cmds):
        if not stack:
            seen.setdefault(pos, tick)
        if pos >= len(data):
            return res("error", why="ran off the ROM")
        b = data[pos]
        if b < 0x80:
            if last is None:
                return res("error", why=f"data byte without running status at 0x{pos + ROM_BASE:08X}")
            cmd = last
        else:
            cmd = b
            pos += 1
            if cmd >= 0xBD:
                last = cmd
        if cmd <= 0xB0:
            tick += WAIT_TICKS[cmd - 0x80]
        elif cmd == 0xB1:                                # FINE
            return res("fine")
        elif cmd == 0xB2:                                # GOTO
            tgt = rv.ptr(pos)
            return res("goto", loop_start_tick=seen.get(tgt),
                       loop_target=f"0x{tgt + ROM_BASE:08X}" if tgt is not None else None)
        elif cmd == 0xB3:                                # PATT
            tgt = rv.ptr(pos)
            if tgt is None or len(stack) >= 3:
                return res("error", why="bad PATT")
            stack.append(pos + 4)
            pos = tgt
        elif cmd == 0xB4:                                # PEND (ignored outside a pattern, as in the engine)
            if stack:
                pos = stack.pop()
        elif cmd == 0xB5:                                # REPT: never emitted by mid2agb
            return res("error", why="REPT")
        elif cmd == 0xB9:                                # MEMACC
            pos += 3
        elif 0xBA <= cmd <= 0xC5 or cmd == 0xC8:         # PRIO TEMPO KEYSH VOICE VOL PAN BEND BENDR LFOS LFODL MOD MODT TUNE
            pos += 1
        elif cmd == 0xCD:                                # XCMD
            pos += 1 + XCMD_ARGS.get(data[pos], 1)
        elif cmd == 0xCE:                                # EOT [key]
            if data[pos] < 0x80:
                pos += 1
        elif cmd >= 0xCF:                                # TIE / N01..N96 [key [vel [gate+]]]
            notes += 1
            for _ in range(3):
                if data[pos] < 0x80:
                    pos += 1
                else:
                    break
        else:
            return res("error", why=f"unknown command 0x{cmd:02X}")
    return res("error", why="command limit")


def set_loop_markers(path, start_tick, end_tick):
    """Replace loopStart/loopEnd markers in a MIDI file with ones at the given absolute ticks (in its first track)."""
    import mido
    mf = mido.MidiFile(str(path))
    for ti, tr in enumerate(mf.tracks):
        t, evs = 0, []
        for msg in tr:
            t += msg.time
            if msg.type == "marker" and msg.text in ("loopStart", "loopEnd"):
                continue
            evs.append([t, msg])
        if ti == 0:
            eot = [e for e in evs if e[1].type == "end_of_track"]
            body = [e for e in evs if e[1].type != "end_of_track"]
            body += [[start_tick, mido.MetaMessage("marker", text="loopStart")],
                     [end_tick, mido.MetaMessage("marker", text="loopEnd")]]
            body.sort(key=lambda e: e[0])                # stable: existing events at the same tick stay first
            last = body[-1][0] if body else 0
            evs = body + [[max(last, eot[0][0] if eot else 0), eot[0][1] if eot else mido.MetaMessage("end_of_track")]]
        new, prev = mido.MidiTrack(), 0
        for t, msg in evs:
            new.append(msg.copy(time=t - prev))
            prev = t
        mf.tracks[ti] = new
    mf.save(str(path))


def pad_midi_end(path, end_tick):
    """Move the first track's end_of_track to end_tick (absolute) if it is earlier."""
    import mido
    mf = mido.MidiFile(str(path))
    tr, t = mf.tracks[0], 0
    for i, msg in enumerate(tr):
        t += msg.time
        if msg.type == "end_of_track":
            if t < end_tick:
                tr[i] = msg.copy(time=msg.time + end_tick - t)
                mf.save(str(path))
            return


# ----------------------------------------------------------------------------------------------- detector
def run_detector(rom_path, work):
    script = work / "detect.sh"
    script.write_text(f"{sh_quote(wsl_path(RIPPER / 'out' / 'sappy_detector'))} {sh_quote(wsl_path(rom_path))}\n",
                      newline="\n")
    out = run_wsl_script(script, 120).stdout
    res = {"raw": out.strip()}
    for key, pat in (("engine_offset", r"detected at offset (0x[0-9a-f]+)"), ("song_table", r"Song table located at: (0x[0-9a-f]+)"),
                     ("main_volume", r"Main Volume: (\d+)"), ("polyphony", r"Polyphony: (\d+)"),
                     ("sample_rate", r"Sampling rate: (\d+)"), ("song_levels", r"song levels: (\d+)")):
        m = re.search(pat, out)
        if m:
            v = int(m.group(1), 0)
            res[key] = v + ROM_BASE if key in ("engine_offset", "song_table") else v
    return res


# ----------------------------------------------------------------------------------------------- MIDI check
def summarise_midi(path):
    import mido
    mf = mido.MidiFile(str(path))
    tempo, abs_t, sec = 500000, 0, 0.0
    tempos, markers, notes, chans, programs, banks = [], {}, 0, set(), set(), set()
    events = []
    for tr in mf.tracks:
        t = 0
        for msg in tr:
            t += msg.time
            events.append((t, msg))
    events.sort(key=lambda x: x[0])
    last = 0
    ch_bank, used = {}, set()
    for t, msg in events:
        if msg.type == "control_change" and msg.control == 0:
            ch_bank[msg.channel] = msg.value
        elif msg.type == "program_change":
            used.add((ch_bank.get(msg.channel, 0), msg.program))
        sec += mido.tick2second(t - last, mf.ticks_per_beat, tempo)
        last = t
        if msg.type == "set_tempo":
            tempo = msg.tempo
            tempos.append(round(mido.tempo2bpm(tempo), 2))
        elif msg.type in ("marker", "text") and msg.text in ("loopStart", "loopEnd"):
            markers[msg.text] = (t, round(sec, 3))
        elif msg.type == "note_on" and msg.velocity > 0:
            notes += 1
            chans.add(msg.channel)
        elif msg.type == "program_change":
            programs.add(msg.program)
        elif msg.type == "control_change" and msg.control == 0:
            banks.add(msg.value)
    return {"type": mf.type, "midi_tracks": len(mf.tracks), "ppqn": mf.ticks_per_beat, "ticks": last,
            "duration_s": round(sec, 3), "tempo_bpm_first": tempos[0] if tempos else 120.0,
            "tempo_changes": len(tempos), "notes": notes, "channels": sorted(chans), "programs": sorted(programs),
            "banks": sorted(banks), "_presets_used": sorted(used),
            "loop_start_tick": markers.get("loopStart", (None,))[0], "loop_start_s": markers.get("loopStart", (None, None))[1],
            "loop_end_tick": markers.get("loopEnd", (None,))[0], "loop_end_s": markers.get("loopEnd", (None, None))[1]}


def sf2_contents(path):
    """Minimal SF2 reader: preset (bank, program) -> name, and sample names (from pdta phdr / shdr)."""
    data = Path(path).read_bytes()
    out = {"presets": {}, "samples": []}
    for tag, size in (("phdr", 38), ("shdr", 46)):
        i = data.find(tag.encode())
        if i < 0:
            continue
        n = struct.unpack_from("<I", data, i + 4)[0] // size
        for k in range(n - 1):                         # last record is the terminal "EOP"/"EOS"
            rec = data[i + 8 + k * size:i + 8 + (k + 1) * size]
            name = rec[:20].split(b"\0")[0].decode("latin-1")
            if tag == "phdr":
                prog, bank = struct.unpack_from("<HH", rec, 20)
                out["presets"][(bank, prog)] = name
            else:
                out["samples"].append(name)
    return out


def validate_sf2(path):
    """Structural SoundFont 2 check (no synth needed): RIFF/sfbk layout, pdta record sizes, bag/gen index chains,
    instrument and sample references, and every sample's start/loop/end inside the smpl chunk."""
    data = Path(path).read_bytes()
    u32 = lambda o: struct.unpack_from("<I", data, o)[0]
    problems, chunks = [], {}
    if data[:4] != b"RIFF" or data[8:12] != b"sfbk":
        return {"ok": False, "problems": ["not a RIFF sfbk file"]}
    if u32(4) + 8 != len(data):
        problems.append(f"RIFF size {u32(4) + 8} != file size {len(data)}")
    pos = 12
    while pos + 8 <= len(data):
        size = u32(pos + 4)
        if data[pos:pos + 4] == b"LIST":
            sub, end = pos + 12, pos + 8 + size
            while sub + 8 <= end:
                ssz = u32(sub + 4)
                chunks[data[sub:sub + 4].decode("latin-1")] = (sub + 8, ssz)
                sub += 8 + ssz + (ssz & 1)
        pos += 8 + size + (size & 1)
    recsz = {"phdr": 38, "pbag": 4, "pmod": 10, "pgen": 4, "inst": 22, "ibag": 4, "imod": 10, "igen": 4, "shdr": 46}
    for k, r in recsz.items():
        if k not in chunks:
            problems.append(f"missing {k}")
        elif chunks[k][1] % r:
            problems.append(f"{k} size {chunks[k][1]} not a multiple of {r}")
    if "smpl" not in chunks or problems:
        return {"ok": False, "problems": problems + ([] if "smpl" in chunks else ["missing smpl"])}
    n = {k: chunks[k][1] // r for k, r in recsz.items()}
    rec = lambda k, i: chunks[k][0] + i * recsz[k]
    smpl_points = chunks["smpl"][1] // 2

    def check_chain(hdr, hdr_off, bag, gen, ref_oper, ref_limit, what):
        for i in range(n[hdr] - 1):                    # last header is the terminal record
            b0, b1 = (struct.unpack_from("<H", data, rec(hdr, j) + hdr_off)[0] for j in (i, i + 1))
            if not b0 <= b1 <= n[bag] - 1:
                problems.append(f"{hdr}[{i}] bag range {b0}-{b1}")
                continue
            for b in range(b0, b1):
                g0, g1 = (struct.unpack_from("<H", data, rec(bag, j))[0] for j in (b, b + 1))
                if not g0 <= g1 <= n[gen] - 1:
                    problems.append(f"{bag}[{b}] gen range {g0}-{g1}")
                    continue
                for g in range(g0, g1):
                    oper, amount = struct.unpack_from("<HH", data, rec(gen, g))
                    if oper == ref_oper and amount >= ref_limit:
                        problems.append(f"{what} {i} references {amount} >= {ref_limit}")
    check_chain("phdr", 24, "pbag", "pgen", 41, n["inst"] - 1, "preset")      # gen 41 = instrument
    check_chain("inst", 20, "ibag", "igen", 53, n["shdr"] - 1, "instrument")  # gen 53 = sampleID
    for i in range(n["shdr"] - 1):
        st, en, ls, le, rate = struct.unpack_from("<5I", data, rec("shdr", i) + 20)
        if not (st <= en <= smpl_points and rate > 0):
            problems.append(f"sample {i} start/end {st}-{en} outside smpl ({smpl_points}) or rate {rate}")
        elif (ls, le) != (0, 0) and not st <= ls <= le <= en:
            problems.append(f"sample {i} loop {ls}-{le} outside {st}-{en}")
    return {"ok": not problems, "presets": n["phdr"] - 1, "instruments": n["inst"] - 1, "samples": n["shdr"] - 1,
            "sample_points": smpl_points, "problems": problems[:20], "problem_count": len(problems)}


# ----------------------------------------------------------------------------------------------- main export
def export_game(slug, cfg, args):
    ws = ROOT / "games" / slug
    out = ws / "music"
    mid_dir, logs = out / "mid", out / "_logs"
    logs.mkdir(parents=True, exist_ok=True)
    rom_path = Path(args.rom) if args.rom else cfg["rom"]
    data = rom_path.read_bytes()                       # read-only
    rv = RomView(data)
    table = int(args.table, 0) if args.table else cfg["table"]
    csv_path = ws / "songs.csv"
    csv_rows = sum(1 for _ in open(csv_path)) - 1 if csv_path.exists() else 0

    det = run_detector(rom_path, logs)
    entries = walk_song_table(rv, table, csv_rows, args.max_scan)
    songs = [e for e in entries if e["status"] == "song"]
    if args.sf2_only:
        songs = []
    elif args.songs:
        want = {int(x) for x in args.songs.split(",")}
        songs = [e for e in songs if e["id"] in want]
    vgs = sorted({e["voicegroup"] for e in entries if e["status"] == "song"})
    bank_of = {v: i for i, v in enumerate(vgs)}
    rate = det.get("sample_rate") or 22050
    mvol = det.get("main_volume") or 15
    print(f"[{slug}] table 0x{table:08X}: {len(entries)} entries walked, "
          f"{sum(e['status'] == 'song' for e in entries)} songs, {len(vgs)} voicegroups; detector table "
          f"{hex(det.get('song_table', 0))}, {rate} Hz, main volume {mvol}")

    if not args.index_only:
        if mid_dir.exists() and not (args.songs or args.sf2_only):
            shutil.rmtree(mid_dir)
        mid_dir.mkdir(parents=True, exist_ok=True)
        sr, sfr = wsl_path(RIPPER / "out" / "song_ripper"), wsl_path(RIPPER / "out" / "sound_font_ripper")
        lines = ["#!/bin/bash", f"ROM={sh_quote(wsl_path(rom_path))}", f"OUT={sh_quote(wsl_path(out))}"]
        for e in songs:
            lines.append(f"timeout 30 {sr} \"$ROM\" \"$OUT/mid/song_{e['id']:04d}.mid\" 0x{e['header'] - ROM_BASE:X} "
                         f"-rc -gs -sv -lv -b{bank_of[e['voicegroup']]} > /dev/null 2>&1; echo \"SONG {e['id']} $?\"")
        if not args.no_sf2:
            # -v must come last: the ripper's "-v <file>" form is broken, so verbose goes to stdout -> log file
            # -ku (local patch, see notes/music_export.md): keep the filler square voice some songs really play
            lines.append(f"timeout 600 {sfr} \"$ROM\" \"$OUT/{cfg['sf2']}\" -s{rate} -mv{mvol} -ku "
                         + " ".join(f"0x{v - ROM_BASE:X}" for v in vgs)
                         + " -v > \"$OUT/_logs/sf2_instruments.txt\" 2>&1; echo \"SF2 $?\"")
        script = logs / "rip.sh"
        script.write_text("\n".join(lines) + "\n", newline="\n")
        res = run_wsl_script(script, 3600)
        (logs / "rip.log").write_text(res.stdout + "\n--- stderr ---\n" + res.stderr, encoding="utf-8")

    sf2 = out / cfg["sf2"]
    sfc = sf2_contents(sf2) if sf2.exists() else {"presets": {}, "samples": []}
    ok = 0
    missing_total = 0
    index_songs = []
    for e in entries:
        rec = {k: e.get(k) for k in ("id", "status", "in_songs_csv", "tracks", "priority", "reverb", "player")}
        rec["header"] = f"0x{e['header']:08X}"
        rec["voicegroup"] = f"0x{e['voicegroup']:08X}" if e.get("voicegroup") else None
        if e["status"] == "song":
            rec["bank"] = bank_of[e["voicegroup"]]
            f = mid_dir / f"song_{e['id']:04d}.mid"
            if f.exists() and f.stat().st_size > 0:
                try:
                    walks = [walk_track(data, p - ROM_BASE) for p in e["track_ptrs"]]
                    w = walks[0]
                    rec["track0_end"] = w["end"] if w["end"] != "error" else f"error: {w.get('why')}"
                    rec["mp2k_ticks"] = max(x["ticks"] for x in walks)
                    gotos = {x["ticks"] for x in walks if x["end"] == "goto"}
                    if len(gotos) > 1:
                        rec["loop_tracks_disagree"] = sorted(gotos)
                    s = summarise_midi(f)
                    if w["end"] == "goto" and w["loop_start_tick"] is not None:
                        rec["loop_target"] = w["loop_target"]
                        if (s["loop_start_tick"], s["loop_end_tick"]) == (w["loop_start_tick"], w["ticks"]):
                            rec["loop_check"] = "ripper markers match track walk"
                        else:
                            rec["loop_check"] = ("markers added from track walk" if s["loop_start_tick"] is None else
                                                 f"ripper markers {s['loop_start_tick']}-{s['loop_end_tick']} "
                                                 "replaced from track walk")
                            set_loop_markers(f, w["loop_start_tick"], w["ticks"])
                            s = summarise_midi(f)
                    elif w["end"] == "fine":
                        rec["loop_check"] = "no loop (FINE)" + (" but ripper markers kept" if s["loop_start_tick"]
                                                                  is not None else "")
                    else:
                        rec["loop_check"] = "track walk inconclusive; ripper markers kept"
                    if all(x["end"] != "error" for x in walks) and s["ticks"] < rec["mp2k_ticks"]:
                        # the ripper drops rests after the last note; keep them so the MIDI lasts as long as in-game
                        rec["end_padded_ticks"] = rec["mp2k_ticks"] - s["ticks"]
                        pad_midi_end(f, rec["mp2k_ticks"])
                        s = summarise_midi(f)
                    rec.update(s)
                    rec["file"] = f"mid/{f.name}"
                    used = rec.pop("_presets_used")
                    miss = [f"{b}:{p}" for b, p in used if (b, p) not in sfc["presets"]]
                    if miss:
                        rec["missing_presets"] = miss
                        missing_total += 1
                    if rec["notes"] == 0:
                        rec["warning"] = "no notes"
                    ok += 1
                except Exception as ex:  # noqa: BLE001 - record and continue
                    rec["error"] = f"parse failed: {ex}"
            else:
                rec["error"] = "ripper produced no file"
        index_songs.append(rec)

    n_song = sum(e["status"] == "song" for e in entries)
    smp = sfc["samples"]
    synth = {k: sum(1 for s in smp if s.startswith(k)) for k in ("Square", "Saw", "Triangle")}
    index = {
        "game": cfg["title"], "slug": slug, "rom": str(rom_path),
        "tool": "GBA Mus Ripper (Bregalad) song_ripper + sound_font_ripper, driven by gbax.music_export",
        "song_table": f"0x{table:08X}", "songs_csv_rows": csv_rows,
        "detector": {k: (f"0x{v:08X}" if k in ("engine_offset", "song_table") else v) for k, v in det.items() if k != "raw"},
        "sample_rate": rate, "main_volume": mvol,
        "soundfont": cfg["sf2"] if sf2.exists() else None,
        "soundfont_bytes": sf2.stat().st_size if sf2.exists() else 0,
        "soundfont_presets": len(sfc["presets"]), "soundfont_samples": len(smp),
        "soundfont_check": validate_sf2(sf2) if sf2.exists() else None,
        "soundfont_gs_synth_samples": synth,
        "banks": [{"bank": i, "voicegroup": f"0x{v:08X}",
                   "songs": sum(1 for e in entries if e.get("voicegroup") == v and e["status"] == "song")}
                  for i, v in enumerate(vgs)],
        "midi_flags": "-rc (avoid ch10) -gs (GS sysex: no drum channel) -sv (vibrato as CC) -lv (linear volume); "
                      "bank select CC0 = 'bank' field; markers loopStart/loopEnd",
        "coverage": {"entries_walked": len(entries), "songs": n_song,
                     "empty_0_tracks": sum(e["status"] == "empty" for e in entries),
                     "invalid_entries": sum(e["status"] == "invalid" for e in entries),
                     "songs_beyond_songs_csv": sum(1 for e in entries if e["status"] == "song" and not e["in_songs_csv"]),
                     "midi_ok": ok, "songs_with_missing_presets": missing_total,
                     "with_loop": sum(1 for s in index_songs if s.get("loop_start_s") is not None),
                     "loop_check": dict(sorted(Counter(re.sub(r" \d+-\d+ ", " N-M ", s["loop_check"])
                                                       for s in index_songs if s.get("loop_check")).items())),
                     "loop_tracks_disagree": sum(1 for s in index_songs if s.get("loop_tracks_disagree")),
                     "end_padded": sum(1 for s in index_songs if s.get("end_padded_ticks")),
                     "midi_ticks_equal_track_walk": sum(1 for s in index_songs
                                                        if s.get("ticks") is not None and s["ticks"] == s["mp2k_ticks"])},
        "songs": index_songs,
    }
    (out / "music_index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    print(f"[{slug}] MIDI ok {ok}/{n_song}; sf2 {'ok' if sf2.exists() else 'MISSING'} "
          f"({index['soundfont_bytes']} bytes, {len(sfc['presets'])} presets, {len(smp)} samples, synth {synth}); "
          f"loops {index['coverage']['with_loop']}; songs with presets missing from sf2: {missing_total}\n"
          f"  loop check: {index['coverage']['loop_check']}; tracks disagreeing on loop end: "
          f"{index['coverage']['loop_tracks_disagree']}\n  sf2 check: {index['soundfont_check']}")
    return index


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("games", nargs="+", help="slug prefixes (AGSE, AGFE, BPRE) or 'all'")
    ap.add_argument("--rom")
    ap.add_argument("--table")
    ap.add_argument("--max-scan", type=int, default=2048)
    ap.add_argument("--songs", help="comma-separated song ids (subset re-rip)")
    ap.add_argument("--index-only", action="store_true")
    ap.add_argument("--no-sf2", action="store_true")
    ap.add_argument("--sf2-only", action="store_true", help="rebuild only the SoundFont (keeps MIDIs)")
    a = ap.parse_args(argv)
    if not (RIPPER / "out" / "song_ripper").exists():
        sys.exit("build the ripper first: wsl -d Ubuntu -u root -- make -C " + wsl_path(RIPPER))
    for raw in ("psg_data.raw", "goldensun_synth.raw"):   # sound_font_ripper looks for these next to itself
        if not (RIPPER / "out" / raw).exists():
            shutil.copy2(RIPPER / raw, RIPPER / "out" / raw)
    sel = list(GAMES) if "all" in a.games else [s for s in GAMES if any(s.startswith(p) for p in a.games)]
    for slug in sel:
        export_game(slug, GAMES[slug], a)


if __name__ == "__main__":
    main()
