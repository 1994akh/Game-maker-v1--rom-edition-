# Music export: MP2K ("Sappy") songs to MIDI + SoundFont

Golden Sun (AGSE), Golden Sun: The Lost Age (AGFE) and Pokémon Unbound (BPRE) all use Nintendo's MP2K/M4A sound
engine. Every song is exported as a standard MIDI file, and each game gets one combined SoundFont 2 (`.sf2`), so a
native engine (Android: FluidSynth or TinySoundFont) can play them. Outputs are engine-neutral.
The ROMs are only ever opened for reading.

## Tool

Option A was used: **GBA Mus Ripper** by Bregalad (maintained fork <https://github.com/jpmac26/gba-mus-ripper>,
GPLv3). It is cloned into `external\gba-mus-ripper` and built in WSL (`Ubuntu`, g++). Its `song_ripper` writes the
MIDIs and its `sound_font_ripper` writes the SoundFont. `gbax\music_export.py` drives it and adds the following:

* **Song-table walk**. gbax walks the table itself and passes each song header to `song_ripper`, so files are named
  by song id (`mid\song_0001.mid`). The ripper's own `sappy_detector` finds the right table for both Golden Sun
  games but the wrong one for Unbound (see below).
* **One SoundFont per game**. Bank N is the Nth voicegroup, sorted by address. Every MIDI selects its bank with CC0
  (`song_ripper -bN`), so a single `.sf2` plays every song of the game.
* **Loop check and repair**. `walk_track()` is an independent MP2K command parser that follows the engine's rules:
  running status for commands ≥ 0xBD, PATT/PEND up to 3 levels deep, and waits W00 to W96. The ripper looks for the
  loop GOTO only in the 9 bytes before track 1, so it misses some loops. Where it does, gbax adds the
  `loopStart`/`loopEnd` markers from the track walk. Where the ripper did find a loop, its markers are checked
  against the walk.
* **Trailing rests restored**. The ripper ends the MIDI at the last note. gbax moves `end_of_track` to the tick of
  the track's FINE, so the MIDI lasts exactly as long as the song does in the game. This matters for jingles the game
  waits on.
* **Local patch `-ku`** in `sound_font_ripper.cpp` (3 small edits, marked "gbax patch"). Upstream skips the filler
  voice `01 3C 00 00 02 00 00 00 00 00 0F 00` (Square 1, 50% duty, sustain 15) as "unused". However, 15 songs
  across the three games really play notes on that voice, and the engine sounds them as a square wave. With `-ku`
  the voice gets a preset.
* **`validate_sf2()`**: a structural check of each SoundFont. It covers the RIFF/sfbk layout, pdta record sizes, the
  bag/gen index chains, preset→instrument and instrument→sample references, and sample start/loop/end positions
  inside the smpl chunk.
* **`music_index.json`**: every MIDI is re-parsed with `mido` and summarised.

## Re-running

```
cd C:\Users\aaron\Documents\UnboundHack
wsl -d Ubuntu -u root -- make -C /mnt/c/Users/aaron/Documents/UnboundHack/external/gba-mus-ripper   # once, after edits
.venv\Scripts\python.exe -m gbax.music_export all            # or: AGSE / AGFE / BPRE (slug prefixes)
.venv\Scripts\python.exe -m gbax.music_export AGSE --songs 1,2,3   # re-rip a subset
.venv\Scripts\python.exe -m gbax.music_export AGSE --sf2-only      # rebuild only the SoundFont
.venv\Scripts\python.exe -m gbax.music_export AGSE --index-only    # re-parse existing MIDIs
```

A full run of all three games takes about 3 minutes and needs `mido` in the venv. On a re-run with `--index-only`,
songs whose markers gbax added earlier are reported as "match", because the markers are now in the file. A full
re-run restores the original labels.

## Output per game (`games\<slug>\music\`)

| file | content |
|---|---|
| `mid\song_NNNN.mid` | one MIDI per song with tracks. NNNN is the song-table index. Type 0, 24 PPQN (one MP2K tick = one MIDI tick). |
| `<game>.sf2` | `golden_sun.sf2`, `golden_sun_the_lost_age.sf2` or `pokemon_unbound.sf2` |
| `music_index.json` | per entry: id, status (song/empty/invalid), header, tracks, priority, reverb, player, voicegroup, bank, file, notes, channels, programs, first tempo, tempo changes, ticks, duration_s, loop_start/end tick+s, loop_target, loop_check, track0_end (goto/fine), mp2k_ticks, end_padded_ticks. Also: detector output, banks list, sf2 check, coverage. |
| `_logs\` | `rip.sh` (the exact WSL commands), `rip.log`, `detect.sh`, `sf2_instruments.txt` (the ripper's verbose dump of every voicegroup entry) |

MIDI conventions:

* Flags are `-rc -gs -sv -lv`. Channel 10 is avoided, and a GS sysex marks channel 10 as non-drum. Drum kits are
  ordinary presets in the game's bank. Vibrato (MP2K LFO/MOD) is simulated with real-time controllers. Volume and
  velocity are linearised so the result sounds like the game.
* Reverb comes from the song header and is sent as CC91. Bank select is CC0, set to the `bank` field.
* Loop markers are `loopStart` and `loopEnd` (meta *marker*). The duration is the intro plus one pass of the loop
  body. To loop in an engine, seek to `loopStart` when playback reaches `loopEnd`.

## Coverage

All three MP2K song tables are VERIFIED. Both Golden Sun tables also match `sappy_detector`. The Unbound table is
VERIFIED by code: the m4a literal pools at 0x081DD11C, 0x081DD150, 0x081DD19C, 0x081DD1F0 and 0x081DD224 each
reference 0x087FE000, and nothing references the vanilla table 0x084A32CC that `sappy_detector` reports.

| | GS1 (AGSE) | GS2 (AGFE) | Unbound (BPRE) |
|---|---|---|---|
| song table | 0x080FC684 | 0x081C4530 | 0x087FE000 |
| m4a engine (detector) | 0x080FA318 | 0x081C1FB4 | 0x081DD0E8 |
| mixing rate / main vol / polyphony | 21024 Hz / 15 / 8 | 31536 Hz / 15 / 10 | 13379 Hz / 12 / 12 |
| table entries walked | 312 | 800 | 527 |
| songs with tracks → MIDI parsed by mido | **260 / 260** | **403 / 403** | **519 / 519** |
| empty (0-track) entries | 52 | 397 | 1 (id 0) |
| invalid entries | 0 | 0 | 7 (327, 469, 471, 473–475, 518) |
| voicegroups = SF2 banks | 2 (0x080FBA78, 0x080FC138) | 2 (0x081C3714, 0x081C3DE0) | 20 (0x0848ABB0 … 0x090567C4) |
| SF2 size / presets / instruments / samples | 7.1 MB / 211 / 87 / 133 | 8.3 MB / 252 / 124 / 171 | 16.8 MB / 2257 / 515 / 774 |
| validate_sf2 problems | 0 | 0 | 0 |
| (bank, program) used by a MIDI but missing from the SF2 | 0 | 0 | 0 (6+3+6 before `-ku`) |
| looping songs (track 0 ends in GOTO) | 79 (61 ripper markers matched, 18 added) | 143 (119 matched, 24 added) | 234 (221 matched, 13 added) |
| non-looping (FINE) | 181 | 260 | 285 |
| tracks disagreeing on loop end | 0 | 0 | 0 |
| MIDI length == track-walk length | 260 / 260 (40 end-padded) | 403 / 403 (63 padded) | 519 / 519 (155 padded) |
| total duration (one pass) | 60 min | 113 min | 257 min |

Cross-checks (VERIFIED):

* For every song, the walker's tick count equals the MIDI's tick count.
* For every looping song, the walker's loop start and end equal the ripper's markers, wherever the ripper emitted
  them.
* On Unbound outliers (songs 290, 338, 485 and 461), per-channel note counts in the MIDI equal the walker's per-track
  note counts.

Song kinds by music player (the `player` field of the song table, VERIFIED from ROM; the meaning is INFERRED):

* **GS1 and GS2.** Player 1 is background music: GS1 has 45 songs, 42 of which loop, lasting 10 to 182 s. GS2 has 98
  songs, 95 of which loop. Player 0 holds 13 short jingles in each game. Players 2–7 are sound effects.
* **Unbound.** These follow pokefirered's player numbering. Player 0 is BGM (231 songs, 225 loop). Player 1 is SE1
  (209). Players 2 and 3 are SE2 and SE3 (70 and 9).

## Unbound specifics

* `songs.csv` (from `gbax.music`) lists 327 rows, because the scan stopped at the first bad entry, id 327. The table
  continues after it: ids 328–526 hold **193 more well-formed songs**. Of those, 178 are looping player-0 BGM, mostly
  on the expansion voicegroups at 0x0904B234–0x090567C4, which is Unbound's expanded soundtrack. They are walked and
  exported. `in_songs_csv: false` marks them in the index.
  * VERIFIED: each has a valid header, voicegroup and track data, and its tracks parse to FINE or GOTO.
  * INFERRED: that the game plays them.
* The invalid entries are not songs:
  * id 327 points to 0x0918B340, which holds non-header bytes.
  * id 469 claims 222 tracks.
  * ids 471, 473–475 and 518 point to the filler address 0x08AAAAAA.
* `sappy_detector` reports the vanilla FireRed table 0x084A32CC. Ignore it; it is stale data.

## Known issues / approximations

* **PSG instruments** (GB square 1/2, wave and noise) are approximated with the ripper's pre-rendered samples
  (`psg_data.raw`). Sweep, exact noise and duty-cycle envelopes are not reproduced.
* **Golden Sun synth instruments**, GS's custom engine voices, are approximated with the ripper's
  `goldensun_synth.raw`. Each GS SoundFont contains 3 square, 1 saw and 1 triangle sample. They are close, not
  exact.
* MP2K details that MIDI and SF2 cannot express exactly are approximated by the ripper:
  * the pseudo-echo,
  * the MP2K envelope shape (MP2K envelopes are per-frame multiplicative, while SF2 envelopes are in dB),
  * LFO types other than vibrato,
  * mixing-rate aliasing.
* **Very short SFX.** After end-padding, five songs last less than 0.05 s: GS1 118 and 119, GS2 118 and 119, and
  Unbound 246. They are click-like sound effects; GS1 118, for example, is N01 key 0x6C, W01, N01, W01, FINE. In-game,
  the sample's release tail is what you hear. For sound effects, a game engine may prefer to render WAVs once from
  MIDI + SF2.
* **`rip.log` exit codes.** `SONG n 120`-style codes are not errors: `song_ripper` returns the voicegroup address as
  its exit status, so the shell sees its low byte. A timeout would show as 124. That value cannot occur here,
  because no voicegroup address ends in 0x7C, and none was seen.
* **Ripper quirks.** The `-v <file>` form is broken, so verbose output is redirected to a file. `song_ripper`'s
  internal 100 000-tick guard was never hit, because every MIDI length equals the walker's length.
* **No audible render.** Nothing was played back: fluidsynth is not installed. Validation is structural, plus
  agreement between the ripper and the independent walker.

## Playback in a native engine (suggestion)

* Load the game's `.sf2` into FluidSynth (LGPL; an Android build exists) or TinySoundFont (header-only C, MIT).
* Play `song_NNNN.mid`. When playback passes the `loopEnd` marker tick, seek to the `loopStart` tick.
* Banks are already selected in-file with CC0, so the engine needs no per-song SoundFont logic.
* Song ids match the in-game song numbers. These are the IDs that map headers and scripts use.
