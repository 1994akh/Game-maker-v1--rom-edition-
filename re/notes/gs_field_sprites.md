# Golden Sun field sprites (player, party, NPCs, objects) and their animations

GS1 = Golden Sun (AGSE), GS2 = The Lost Age (AGFE). **VERIFIED** = read from ROM code (capstone /
goldensun-master disassembly) or from alchemy's decompiled C where it matches the ROM; **INFERRED** = from images or
data only.

Exporter: `python -m gbax.codecs.gs_field_sprites ROM [ROM2 ...]` (module `gbax/codecs/gs_field_sprites.py`). Run
from `C:\Users\aaron\Documents\UnboundHack` with `.venv\Scripts\python.exe`. It takes a few seconds per game. It
reuses `SpriteSet` (sprite table, frame decoding, palette) from `gs_battle_sprites` and reads
`games\<slug>\maps\rooms\*\events.json` (from `gs_maps`) to link map actors to sprites.

```
.venv\Scripts\python.exe -m gbax.codecs.gs_field_sprites "games\AGSE-5c469520-Golden-Sun-USA-Europe\rom\Golden Sun (USA, Europe).gba" "C:\Users\aaron\OneDrive\Apps-Roms\Golden Sun - The Lost Age (USA, Europe).gba"
```

Output in `games\<slug>\field_sprites\`:

| File | Contents |
|---|---|
| `NNNN.png` | sheet for sprite-table entry NNNN: all frames in a grid (5 columns for facing kind 5, 3 for kind 3, else 8), real palette, colour 0 transparent. If any animation shows a frame mirrored, a second block below (`mirrored_block_y`) holds every frame flipped horizontally at the same grid position. |
| `NNNN.json` | record fields, frame rectangles, facing table, and **animations expanded per direction**: `walk_s`, `walk_se`, …, each frame with `region` [x, y, w, h] in the sheet (already pointing at the mirrored copy when needed), `flip_h`, `duration` in 60 Hz frames; `fps` 60, `loop`, `loop_start` (frame index the loop returns to), `end` (`loop`/`hold`/`next`/`hide`), `next` (name of the chained animation), `script_hex` |
| `sprites.json` | index: id, name, category, size, frame count, facing kind, animation count, number of map actors using it; coverage |
| `palette.json` | the 224-colour global OBJ palette (same as the battle sprites) |
| `index.html` | gallery; each card plays `walk_s` (or the first animation) at 60 FPS from the sheet + JSON regions |

Godot: a SpriteFrames converter can make one animation per JSON animation, one AtlasTexture per frame `region`,
animation speed 60 FPS, per-frame duration = `duration`, `loop` = `loop`. `loop_start > 0` (an intro before the
loop) needs splitting into two animations, and `next` needs an `animation_finished` hook.

## Coverage

| | GS1 | GS2 |
|---|---|---|
| Field sprites exported (sprite-table entries outside the battle groups + every id a map actor uses) | 251 | 511 |
| Frames decoded to exactly w x h | 5,170 / 5,170 | 9,799 / 9,799 |
| Animation scripts parsed | 1,430 | 2,716 |
| Directional animations after expansion | 7,828 | 16,170 |
| Expanded animations with an out-of-range frame | 14 (all GS1 sprite 1, see below) | 31 (sprites 1, 3, 32, 36) |
| Map actor sprite ids linked | 160 / 160 | 309 / 309 |
| Categories (INFERRED rule, below) | 6 party, 125 person, 120 object | 8 party, 237 person, 266 object |
| Facing kinds in use | 5: 13, 3: 118, 1: 40, 11: 76, 2: 3, 22: 1 | 5: 25, 3: 221, 1: 114, 11: 135, 2: 8, 20: 7, 22: 1 |

Visually checked with the Read tool: GS1 sprites 0–51 (first frame), Isaac's sheet and all 8 `walk_*`/`run_*`
directions (each row shows one consistent direction; west rows are mirrors of east); GS2 sprites 0–39, Felix
`walk_e/s/sw/n`, `run_w`, NPC 16 `walk_s/e/w`. All looked like clean sprites with natural colours.

Party sprites (INFERRED from the sheets): GS1 0 Isaac, 1 Garet, 2 Ivan, 3 Mia, 5 Jenna, 6 Felix (an NPC-style
kind-3 sprite in GS1); 4 is empty. GS2 0 Isaac, 1 Garet, 2 Ivan, 3 Mia, 4 Felix, 5 Jenna, 6 Sheba, 7 Piers.
Category rule (INFERRED): `party` = the list above, `person` = facing kind 3/4/5/6/8/88 with at least 3
animations, `object` = everything else (chests, emotes, doors, effects, Djinn, statues …).

## Sprite record (VERIFIED; alchemy `tools/ags/src/sprite.rs`, `GRAPHICS/SPRITE/SPRITES.TSV`, and the ROM)

20 bytes at GS1 `0x08185024 + 20*id` (512 entries), GS2 `0x08300000 + 20*id` (716):
`+0 width`, `+1 height`, `+2 u16 scale` (0x100 = 1.0), `+4 facing kind` ("draw"), `+5 number of animations`,
`+6 s8 adjust_x`, `+7 s8 adjust_y`, `+8 box_x`, `+9 box_y` (alchemy's names; `FieldObject_Create` takes the
contact radius from the record, INFERRED to be one of these), `+10 codec` (0 RLE, 1 LZ, 3 back-referenced RLE —
decoded by `gs_battle_sprites`), `+12 frame list*` (null-terminated), `+16 animation list*` (n pointers).
Several sprites share another sprite's animation list (alchemy's `animations` column), which is why some lists
reference frames a sprite does not have.

Map actors (VERIFIED, alchemy `FieldObject_Create`, GS1 kernel ~`0x0800C4xx`): actor sprite value `v`:
`v & 0xFFF` = sprite-table id; `v >> 12` = 0 single sprite, 2 two-part (ids `id` and `id+1` drawn as layers).
New objects face `0x4000` (south). No exported actor uses the two-part form.

## Animation scripts (VERIFIED)

Interpreter: alchemy `Sprite_ComposeAnimationFrame` (`GRAPHICS/RENDER/COMPOSE_ANIMATION_FRAME.C`, GS1 kernel,
facing-table literal at `0x0800AD48`); GS2 at `0x08021AF0` (opcode jump table `0x08021B30`, kind jump table
`0x08021BE8`). A script is byte pairs `(op, arg)`; a layer's timer counts in 1/16 frames and drops by its step,
which `Animation_SetWorkEntry` sets to `0x10` — so **`arg` is a duration in game frames (60 Hz)**.

| op | meaning |
|---|---|
| `0x00`–`0xEE` (and `0xFB`) | show frame `op` (+ facing offset) for `arg` frames |
| `F0 k` | set the facing kind for the following frames (`F0 11` = no facing: cast/emote poses) |
| `F1 x` | hold the current frame forever (stop) |
| `F5 n` | keep the current frame `n` more frames |
| `FD p` | jump to byte offset `p` (loop; `FD 00` = loop the whole script) |
| `FE a` | switch to animation `a` (bit 7: keep the cursor) |
| `FF n` | hide the sprite for `n` frames |
| `EF x` | hide and end the script |
| `F2`, `F3` | GS1 no-op; GS2 stores `arg` in object bytes +0x17 / +0x16 |
| `FC` | GS1 no-op; GS2 calls `0x081C0010(arg)` (INFERRED: a sound effect) |
| `F4`, `F6`–`FA` | no-op |

Ends seen: GS1 607 hold, 508 loop, 313 chain, 2 hide; GS2 1,219 / 950 / 547 / 0.

Animation numbers (shared list layout of person sprites): 0 `still` (one frame + hold; INFERRED), 1 `idle`
(ANIM_STAND, look-around loop), 2 `walk`, 3 `nod`, 4 `shake_head` (alchemy `FIELD_EVENT.H`), 5 `run`, 8 `push`
(on-foot controller GS1 `0x0800EBEC`: run button held → speed 0x18000 + anim 5, else 0x10000 + anim 2; anim 8
while pushing; VERIFIED in the goldensun-master disassembly, `rom_ebec.s`), 11 `hammer`, 19 `sprawled` (alchemy
names). The controller also uses 9 and 0x16 (probably climbing; not named). Other numbers are exported as
`anim_NN`. Timings: GS1 Isaac walk 6 poses x 6 frames, run 6 x 4; GS2 Felix walk 6 x 7, run 6 x 5; NPCs often
6 x 9.

## Facing (VERIFIED)

Facing is the actor's u16 angle (0 = east, 0x4000 = south). The kind picks a table; the table entry for the angle
sector gives `frame = base + (entry & 7)` and **bit 7 = draw mirrored horizontally**.

| kind | GS1 table | GS2 table | sector | frames per pose | layout |
|---|---|---|---|---|---|
| 5 (party, main NPCs) | `0x080130AC` | `0x0802EB04` (64 sectors) | GS1 angle>>12, GS2 >>10 | 5 | 0 SE, 1 E, 2 NE, 3 S, 4 N; SW/W/NW = mirrored SE/E/NE |
| 3 (most NPCs) | `0x0801309C` | `0x0802EAE4` | >>12 | 3 | 0 front-diagonal, 1 side, 2 back-diagonal; E=1, SE=0, S=0 mirrored, SW/W=1 mirrored, NW=2 mirrored, N/NE=2 |
| 8 | `0x080130BC` | `0x0802EB44` | (angle+0x1000)>>13 | 8 | S 0, SE 1, E 2, NE 3, N 4, NW 5, W 6, SW 7 (no mirroring) |
| 1 | `0x0801307C` | `0x0802EAC4` | >>13 | 1 | mirrored on the west half |
| 2 / 20 | `0x08013094` | `0x0802EADC` | >>13 | 2 | front / back, each mirrored on one side |
| 22 | `0x0801308C` | `0x0802EAD4` | >>13 | 2 | like 2 with the other mirror |
| 4, 6, 88 | `0x080130CC`, `0x0801310C`, `0x080130C4` | — (GS2 treats them as "no facing") | | 4 / 6 / mixed | unused by field sprites |
| anything else (e.g. 11, 0x11) | — | — | | 1 | no facing |

So the player and main characters have **5 drawn directions and 8 facings** (3 mirrored). GS2's kind-5 table is
finer (64 sectors) and, for the few sectors just west of due south/north, mirrors the S/N frame; at the 8 compass
angles both games give the same frames. The exporter samples the 8 compass angles (what the player shows after
turning); `NNNN.json` also carries the raw table (`facing.values`, `sector_shift`) for NPCs turned to other angles.

## Palette (VERIFIED)

Field sprites are 8bpp OBJs drawn with the same 224-colour global palette as the battle sprites (GS1 `0x0800779C`,
GS2 `0x08017B10`); alchemy's SPR_NNN.PNG pictures are drawn with the same "system palette". Colour 0 is
transparent. No per-sprite palettes.

## Open questions

- Out-of-range frames: GS1 Garet (sprite 1) anims 22–28 (`5a f0 f1 00`) and a few GS2 entries reference frames
  beyond the sprite's own list (their animation list is borrowed from a sprite with more frames). They are
  exported with `region: null`; the game presumably never plays them for these sprites.
- Names of party animations beyond 0–5/8/11/19 (cast, jump, climb, surprised …); look at which numbers the
  Psynergy cast routine and room scripts pass to `Actor_SetAnimation`.
- Exact meaning of `adjust_x/adjust_y/box_x/box_y` for the draw anchor (the actor position is the feet).
- Two-part actors (`v >> 12 == 2`) and the GS2 `F2`/`F3`/`FC` opcodes' effects.
- World-map sprites, the boat, and Psynergy effect sprites created by code (not map actors) are exported as
  ordinary entries but not identified.
