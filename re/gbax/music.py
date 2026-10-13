"""MP2K/M4A (Nintendo SDK "Sappy") sound data: song table, song headers, voicegroups.

Song table entry (8 bytes): song header pointer, u16 music player, u16 music player (again in some SDK versions).
Song header: u8 track count, u8 blocks, u8 priority, u8 reverb, voicegroup pointer, then one pointer per track.
"""
import csv


def _ptr(rom, off):
    v = rom.u32(off)
    return v - 0x08000000 if 0x08000000 <= v < 0x08000000 + rom.size else None


def read_song_table(rom, table_addr, limit=2048):
    songs = []
    off = table_addr - 0x08000000
    for i in range(limit):
        e = off + i * 8
        hdr = _ptr(rom, e)
        if hdr is None:
            break
        tracks = rom.data[hdr]
        vg = _ptr(rom, hdr + 4)
        track_ptrs = [_ptr(rom, hdr + 8 + 4 * t) for t in range(tracks)] if tracks <= 16 else []
        valid = tracks <= 16 and (tracks == 0 or (vg is not None and all(p is not None for p in track_ptrs)))
        if not valid:
            break
        songs.append({"index": i, "header": hdr + 0x08000000, "tracks": tracks, "priority": rom.data[hdr + 2],
                      "reverb": rom.data[hdr + 3], "voicegroup": (vg + 0x08000000) if vg is not None else None,
                      "player": int.from_bytes(rom.data[e + 4:e + 6], "little")})
    return songs


def write_song_list(rom, songs):
    path = rom.workspace / "songs.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["index", "header", "tracks", "priority", "reverb", "voicegroup", "player"])
        for s in songs:
            w.writerow([s["index"], f"0x{s['header']:08X}", s["tracks"], s["priority"], s["reverb"],
                        f"0x{s['voicegroup']:08X}" if s["voicegroup"] else "", s["player"]])
    return path
