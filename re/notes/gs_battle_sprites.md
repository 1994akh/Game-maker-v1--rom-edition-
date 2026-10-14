# Golden Sun battle sprites (enemies, party, weapons, summons, Djinn)

Exporter: `python -m gbax.codecs.gs_battle_sprites ROM [ROM2 ...]` (module `gbax/codecs/gs_battle_sprites.py`).
It needs `games\<slug>\data\enemies.json` (from `gbax.codecs.gs_units`) for enemy names and battle IDs. Run from
`C:\Users\aaron\Documents\UnboundHack` with the project venv. It takes a few seconds per game.

Output in `games\<slug>\battle_sprites\`:

| File | Contents |
|---|---|
| `enemies\NNN_<name>.png` | one sheet per enemy record (all frames, 8 per row, palette swap applied, colour 0 transparent) |
| `enemies.json` | per enemy: battle ID, battle-table entry, sprite ID, palette swap, source file, frame rectangles; also the raw battle table |
| `sprites\NNNN.png` | every entry of the sprite table, unswapped (party, weapon overlays, enemy bases, summon pieces, status icons, field sprites) |
| `sprites.json` | per sprite: category, size, frame type, source (ROM list or file), frame rectangles, raw table bytes, animation scripts (raw hex), per-frame errors |
| `palette.png`, `palette.json` | the 224-colour global sprite palette |
| `index.html` | gallery: enemies, battle sprite-table entries, field entries |

## Coverage

| | GS1 (AGSE) | GS2 (AGFE) |
|---|---|---|
| Enemy records exported | 165 of 165 (163 named + `???` + 1 unnamed) | 380 of 380 (378 named + 2) |
| Distinct enemy base sprites | 52 (54 sprite IDs incl. 2nd halves) | 104 |
| Sprite-table entries (non-empty) exported | 367 of 367 | 716 of 716 |
| Frames decoded | 6,523 of 6,523 | 12,284 of 12,284 (2 are deliberately empty) |
| Party battle sprites | 5 (Isaac 300, Garet 301, Ivan 302, Mia 303, Jenna 305), 20 frames each | 8 (Isaac 490, Garet 495, Ivan 500, Mia 504, Felix 508, Jenna 513, Sheba 517, Piers 521), 20 frames each |
| Weapon overlays | 16 sheets (320–336), 20 frames each | 28 sheets (the IDs between the party sprites, 491–525) |
| Summon pieces | 13 sprites (370–390) | 25 (642–666) |
| Status icons / misc battle | 28 / 4 | 31 / 18 |

"Exported" means every frame decoded to exactly its width x height (RLE terminator reached inside the frame,
or the type-1 stream gave exactly w*h bytes). Visually checked with the Read tool: GS1 Troll (file 242, 12 frames),
Vermin / Mad Vermin (swap 5), Bat / Rabid Bat (swap 4), Death Cap, Slime Beast, Lich, Skull Warrior, Lizard King,
Living Statue, Mimic, Venus/Mars/Jupiter Djinni, all GS1 sprites 300–399; GS2 Mercury Djinni, Ruffian, Pixie
(swap 3) vs Faery (swap 0), Rat Fighter, Gargoyle, Devil Frog, Zombie, Bandit, GS2 party sprites 490–525.
All looked like clean sprites with natural colours.

## Pipeline

Addresses are GS1 / GS2. VERIFIED = read from code and confirmed by decoding; INFERRED = from data or images only.

1. **Enemy -> battle table** (VERIFIED). The enemy record's `battle_id` (already in enemies.json) indexes an
   8-byte table: GS1 `0x080C7420` (172 entries, getters `0x080C2384` / `0x080C23A0` / `0x080C23C0`, bound
   `cmp r0,#0xAB`), GS2 `0x08130D0C` (387 entries, getters `0x081280BC` / `0x081280D8` / `0x081280FC`, bound
   0x182). Out-of-range IDs return entry 0 (GS1 enemy 164 and GS2 enemy 379, both unnamed, are clamped).
   Entry: `u16 sprite id`, `u8 flags` (bit 0 read by the third getter), `u8 b3` where `(b3 >> 1) & 15` is
   the palette swap (VERIFIED), `u8 b4` (unknown; values 0x08–0x40, maybe a height offset), 3 bytes padding.
   Many enemies share a sprite and differ only by swap (Vermin swap 0, Mad Vermin swap 5).
   The GS1 caller is the battle setup function `0x080B6D30` (unit struct byte +0x128 = battle ID), which loads
   sprite IDs `0x1DC` (476) and `0x1E3` (483) as two halves (ID and ID+1): Kraken (enemy 113, 476+477) and
   Fusion Dragon (enemy 140, 483+484). Their sheets hold both halves (16 + 16 frames). GS2 has no such case
   in the code path checked.
2. **Sprite table** (VERIFIED). 20-byte entries. GS1 `0x08185024`, 512 entries; the module at `0x08185000`
   (master-table entries 17/18) exports only the getter `0x08185009` (`idx & 0xFFF`). GS2 `0x08300000`,
   716 entries, getter `0x08021918` (`idx < 0xB3*4`). Layout:
   `+0 width`, `+1 height`, `+2 flags` (0xC0/0xD9 on battle sprites; INFERRED meaning: scaled/affine),
   `+3`, `+4` (copied to object +4), `+5 number of animations` (bound check at `0x0800BA0C`), `+6..+9`
   (unknown; +8/+9 look like an anchor), `+10 frame type` (copied to object +7 at `0x0800B898`),
   `+12 frame-pointer list` (0 = frames come from a file), `+16 animation-script pointer list`.
3. **File-backed sprites** (VERIFIED). When `+12` is 0, `0x0800B6B8(slot, dest, sprite, swap)` (GS2
   `0x080227E0`; GS1 export stub `0x08009270`) looks the sprite up in a `(u16 file, u16 sprite)` list ending in a
   zero sprite (GS1 `0x08012FA0`: 54 pairs, sprites 400–486 -> files 242–295; GS2 `0x0802E91C`: 105 pairs, first
   526 -> 515 … 641 -> 619), GetFile + decompress (`0x08005340`, format 0/1). The decompressed file starts with a
   0-terminated list of u32 frame offsets relative to its start. Every GS1 enemy sprite is file-backed; in GS2
   all but sprites 538, 579, 581, 583 and 585 are (those keep their frames in ROM, type 0). GS2 file 543
   (sprite 555) lists two frames at the very end of the file; they're exported as empty frames.
4. **Palette swap** (VERIFIED). If swap n is 1..5, the loader rewrites every byte < 0xE0 of the frame data
   through the byte map at GS1 `0x080092B8 + 0x100*(n-1)` (GS2 `0x080203A8`, byte-identical). The exporter
   applies the same map to decoded pixels, which is equivalent.
5. **Frame types** (dispatcher GS1 `0x0800AE8E`, GS2 `0x08021DB6`; VERIFIED):
   - **0** (GS1 enemies, party) and **2** (GS2 enemies; GS2's dispatcher sends every type other than 1/3 to the
     same path): RLE, decoded by the ARM routine at GS1 `0x08009BB8` (copied to IWRAM). Byte `0x00` ends the
     frame, `0xE0..0xFF` skips `b - 0xDF` transparent pixels, anything else is one pixel. Pixels are row-major,
     width x height. The decoder also has fill-colour and remap modes (mode = object +5) used for flashes.
   - **3** (weapon overlays, status icons, GS1 front views, field sprites): a u16 header, then either RLE
     (header 0) or a back-referenced stream that the Thumb routine GS1 `0x0800A97C` / GS2 `0x08021940` expands
     into a buffer. That routine returns the address of the RLE stream (the ROM data itself, or the buffer).
     gbax runs it in the Unicorn emulator, then decodes the RLE.
   - **1** (summon pieces): format 0/1 compressed, exactly width*height bytes of linear 8bpp (checked
     visually; reading it as 8x8 tiles scrambles it).
6. **Palette** (VERIFIED). One 224-colour BGR555 palette shared by every sprite: GS1 `0x0800779C` (DMA'd to OBJ
   palette RAM `0x05000200`, 0xE0 halfwords, literal pool at `0x08004850`), GS2 `0x08017B10` (byte-identical).
   OBJ graphics are 8bpp; colour 0 is transparent. Indices 0xE0–0xFF never appear in decoded frames.

## Frames and animation

- Enemy files hold front and back views alternately (even = front, odd = back; INFERRED from the images: the
  camera swings behind the enemies during the party's turn). The GS1 Troll has 12 frames = 6 poses x 2 views.
- Animation scripts are in `sprites.json` as raw hex (`anims_hex`): `(frame, ticks)` byte pairs until a control
  byte, `F1` = loop back to the start, `FD`/`FE` = stop on the last frame (e.g. `00 14 02 14 04 14 FD 00` = frames
  0, 2, 4 for 20 ticks each, then hold). The frame byte indexes the sheet directly and only names even frames,
  i.e. the front views; the odd frame after each is the same pose from behind. INFERRED from the sheets and
  used as-is by the engine (GameMaker-Engine `tools/export_gs_battle_sprites.py` decodes them; 14 Oct 2026):
  script 0 idles (one frame, loop), 1 attacks (ends), 3 casts; the others aren't placed yet.
- Frame offsets/anchors inside the sheet are in `frame_rects`; the in-battle anchor is probably table bytes
  +8/+9 (e.g. 0x30, 0x20 for 64x64), INFERRED.

## Party, weapons, summons, Djinn

- **Party**: one 64x64, 20-frame sheet per character (not per class). The weapon is drawn as a separate overlay
  sprite with the same 20-frame layout. GS2 stores each character followed by its weapon overlays (Isaac 490 +
  491–494 sword/light blade/axe/mace, Garet 495 + 496–499, Ivan 500 + 501–503, Mia 504 + 505–507, Felix 508 +
  509–512, Jenna 513 + 514–516, Sheba 517 + 518–520, Piers 521 + 522–525). GS1 has the five characters at
  300–305 (304 empty) and 16 overlays at 320–336. INFERRED from images; the code that picks the overlay from
  the equipped weapon type wasn't traced.
- **Djinn**: the Djinn you fight are ordinary enemy records, exported with the enemies: GS1 sprites 433–436
  (enemies 150–161: Venus 433, Jupiter 434, Mars 435, Mercury 436), GS2 sprites 600–603 (enemies 1–58).
- **Summons**: besides the battle-effect bitmaps already solved, summons use sprite-table entries of type 1
  (GS1 370–390, GS2 642–666): 32x32 / 64x64 pieces of the big summon pictures (Thor, Ramses, Neptune, …).
  How the pieces are assembled on screen isn't decoded yet.

## Open questions

- The overlay owner/weapon-type mapping and the code that chooses party sprite + overlay (GS1 kernel
  `0x08012600` area calls the loader with sprite IDs from a struct; not followed).
- Battle-table byte 4, flag bit 0, and sprite-table bytes +2/+3/+4/+6..+9.
- Which script is which beyond 0/1/3 (hurt, down, defend?); the ROM's script interpreter; how summon pieces
  are positioned.
- GS2's IWRAM RLE routine wasn't located; GS2 output was verified by decoding (every frame terminates at
  exactly its size) and visually.
- Field sprites (category `field`) also decode; they belong to the overworld-sprite job, which can reuse
  `SpriteSet` from this module.
