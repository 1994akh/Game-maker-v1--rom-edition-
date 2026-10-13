# Golden Sun field movement: spec for an 8-direction Pokémon-engine port

GS1 = Golden Sun (AGSE), GS2 = The Lost Age (AGFE). Addresses are GS1 unless marked GS2.
**VERIFIED** means checked against ROM bytes, decompiled code or the live run below. **INFERRED** means it's a
reading of the code that hasn't been tested.

How to re-run:

- `.venv\Scripts\python.exe tools\gs_movement\extract_constants.py` is static and covers both ROMs. It writes
  `tools\gs_movement\out\gs_movement_constants.json`.
- `.venv\Scripts\python.exe tools\gs_movement\measure_walk.py` is live and covers GS1. It copies the ROM and .sav
  to a work folder, drives mGBA through its GDB stub, then writes `walk_log.csv` (1,820 frames) and
  `walk_summary.json`. It takes about 10 minutes and deletes the ROM copy when it finishes.

## 1. Numbers to tune against

| | GS1/GS2 on foot (towns, dungeons) | Pokémon engine |
|---|---|---|
| Walk speed | **1.0 px/frame** (`0x10000`). The live run measured 1.0031 because of fixed-point rounding. | 1 px/frame |
| Run speed (B held) | **1.5 px/frame** (`0x18000`) | 2 px/frame |
| Acceleration | **0.25 px/frame²** (`0x4000`), for walking and running alike | none |
| Frames to full speed | walk **4**, run **6** | 0 |
| Deceleration | **none**: velocity is set to 0 on the first frame without input | none |
| One 16 px tile at cruise speed | walk **16 frames**, run **10.67 frames** | 16 / 8 |
| First 16 px from standing | walk **≈17.5 frames**, run **≈13.2 frames** | 16 / 8 |
| Diagonal | **normalised**: 0.707 px/frame per axis walking, 1.0607 running (= 1.5/√2). Live: running typically 1.0607 per axis (1.0630 in 2 of 6 segments); walking 0.7093 was seen for only ~4 frames before a wall (`walk_SE`) | engine-dependent |
| Diagonal tile (16,16) = 22.6 px | walk 22.6 frames, run 15.1 frames | – |
| Input directions | 8, from the d-pad (opposite directions cancel) | 4 (8 in the target engine) |
| Facing | continuous u16 angle that turns at most **22.5° (`0x1000`) per frame** toward the velocity | snaps |
| Grid | **none**: free movement on a 16.16 fixed-point pixel position; only collision uses 16 px cells | 16 px steps |

Live acceleration profile (px moved per frame, VERIFIED):

- Walking: 0.25, 0.496, 0.742, 0.988, then 1.003 steady.
- Running: 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, then 1.5 steady.

Other controllers (speed / acceleration in px/frame, VERIFIED constants):

| Controller | GS1 | GS2 | Notes |
|---|---|---|---|
| On foot | `0x0800EBEC`: 1.0/0.25, run 1.5/0.25 | `0x08027064`: identical | 8 px wall probe |
| World map | `0x0800F2F8`: 0.5/0.25, run 1.0/1.25 | `0x080279B0`: 0.5/0.25, run 1.0/0.5; `0x0802A124`: 0.5/0.25 | 7 px probe in GS1; terrain classes 5–12 are walkable (`0x080122AC`). GS2 fans out at ±30° (`0x1555`). |
| Climbing (ladders, vines) | `0x0800F7F4`: 0.5/0.25 | `0x080290F4`: 0.5/0.25 | only moves vertically; tile byte 2 must match |
| Pushing a pushable object | player 0.25/0.125; the object moves 0.25 px/frame | same | below |
| Debug (flag 0x17F + B; L in the world-map and some GS2 controllers) | 4.0/1.0 | 4.0/1.0 | developer speed-up (INFERRED) |
| GS2-only modes | – | `0x0802632C` 0.5/0.125; `0x080267BC` 1.0/0.05 (slippery?); `0x08027E20` 1.0/0.25 with 19 px probe (large vehicle?); `0x08028534` 1.25/0.5; `0x08028AAC` 1.25 + height/16 / 0.5; `0x080292FC` and `0x08029570` 0.5/0.5; `0x080298C0` 0.5 then 1.0 / 0.25 | the mode names are INFERRED |

**Porting advice.** These are recommendations, not anything Golden Sun does.

- A 1.5 px/frame run needs sub-pixel position. Use 8.8 or 16.16 fixed point, or alternate 1 px and 2 px frames;
  a tile-aligned run step then takes 11 frames.
- Diagonal steps of (16,16) take 22–23 frames walking and about 15 running if you keep Golden Sun's normalised
  speed. Pokémon-style unnormalised diagonals would take 16 / 8 frames and feel about 41% faster.
- Ramp up over 4 / 6 frames. Stop dead on release.

## 2. RAM and object layout

- **Keys** (VERIFIED). The only KEYINPUT reader is GS1 `0x080036D4` (GS2 `0x08013A3E`).
  - Held keys go to `0x03001AE8`, new presses to `0x03001C94`, sticky presses to `0x03001AF8`. Key repeat state
    is at `0x03001B00` and `0x03001B04`, and the previous keys at `0x03001D0C`. The frame counter is
    `0x03001800`.
  - GS2 keeps them in one struct at `0x03001150`: +0 held, +4 new, +0x1C sticky.
  - Button mapping is a halfword table at `0x02000240` + `0x210`–`0x222`. Run is at +`0x21C` (GS2 +`0x23C`) and
    defaults to B.
- **D-pad to angle table**: `0x08013254` (GS2 `0x0802EC5C`), 16 u16 entries, indexed by `(keys>>4)&15`.
  - R=`0x0000`, D+R=`0x2000`, D=`0x4000`, D+L=`0x6000`, L=`0x8000`, U+L=`0xA000`, U=`0xC000`, U+R=`0xE000`.
  - None, L+R and U+D map to `0xFFFF` (idle).
  - Angles are u16 with `0x10000` = 360°. **0 = east (+x), `0x4000` = south (+z, down the screen).**
- **Field objects** (actors): 0x70-byte structs in an array pointed to by `0x03001E64`. The collision loop scans 64
  slots and the mover `0x0800D340` updates the first 14. In the live session the player's object was at
  **`0x02030EBC`** (VERIFIED). The field state is at `*(0x03001EBC)`, and its actor table at +0x14 holds slots
  0..0x42.

| Offset | Field |
|---|---|
| +0x00 | non-zero when the slot is in use |
| +0x04 | u16 counter, incremented every frame the controller runs (VERIFIED) |
| +0x06 | u16 facing angle (VERIFIED) |
| +0x08, +0x0C, +0x10 | **x, y (height, up is +), z** as s32 **16.16 fixed point in pixels** (VERIFIED: x 301.68, y 160.0, z 905.0) |
| +0x14 | floor height (16.16); collision compares against this |
| +0x20 | u16 collision radius in px |
| +0x22 | u8 collision layer (0–2) |
| +0x24, +0x28, +0x2C | velocity vx, vy, vz (16.16 px/frame) (VERIFIED) |
| +0x30 | max speed (VERIFIED) |
| +0x34 | acceleration (VERIFIED) |
| +0x38, +0x3C, +0x40 | destination x, y, z; `0x80000000` means none (VERIFIED) |
| +0x48 | gravity |
| +0x55 | bit 1 = gravity on |
| +0x56 | which axis decides arrival: `0x10` x, `0x11` y, `0x12` z |
| +0x58 (u32) | bit 0x100 = solid, 0x200 = pushable, 0x400 = larger talk radius, 0x800 = can't be talked to |
| +0x5A | bit 0 = turn to face the velocity |
| +0x64, +0x66 | footstep and dust timer (12 frames running, 18 walking) and foot toggle |

## 3. Per-frame algorithm

**Controller** `FUN_0800EBEC(obj)`, every frame (VERIFIED by decompile and live run):

1. Choose the speed: run if the mapped run button is held. Look up the angle from the d-pad table. If there's no
   direction, the frame is idle (step 6).
2. **Wall probe.** Take the point 8 px ahead along the angle (`FUN_0800447C(dist, angle, &pos)` moves a point by
   dist·cos and dist·sin, using a table at `0x08002344` believed to be a 1024-step 16.16 sine table; the verification
   pass found it deviates from sin() by up to ~74% of 1.0, so either the table is something else or the comparison
   was wrong — UNVERIFIED). Also check rays at ±22.5° and ±45°.
   The heading is accepted only if all five points pass the tile test (§4).
3. **Slide.** If the heading is blocked, try +22.5°, −22.5°, +45°, −45°, +67.5° and −67.5°, each needing its own
   five-ray fan clear. The first clear heading is used. If none is clear, the player is blocked: stop, and turn
   toward the input at 22.5° per frame.
   - Live example: holding Down+Right (`0x2000`) against a wall moved the player on heading `0x5000` (+67.5°)
     at full speed.
4. **Actor probe.** Take the point 4 px ahead on the chosen heading and test it against every solid actor:
   blocked when the centres are closer than (r1−2)+(r2−2) in 3D.
   - If the actor is pushable and the point 10 px beyond it (±22.5° rays) is clear, the actor is nudged 0.25 px
     and the player's speed drops to 0.25.
5. **Set the destination.** `FUN_0800D14C` sets the destination a few pixels ahead (the live run showed 6 px
   walking and 4 px running; why it differs is open). The mover then steers toward it.
6. **Idle or blocked**: clear the destination and set vx = vz = 0, so the player stops instantly (VERIFIED).

**Mover** `FUN_0800D340`, per object:

- With a destination set:
  - d = |dest − pos| in the xz plane. The routines are in RAM: fixed sqrt at `0x030001D8`, multiply at
    `0x03000118`, divide at `0x0300013C`.
  - Add **acceleration × unit(dest − pos)** to v, then clamp |v| to max speed.
  - Arrival is detected by the sign of (dest − pos) flipping on the dominant axis.
- With no destination: **friction** reduces |v| by the acceleration value each frame. For the player this never
  matters, because the controller already zeroed v.
- pos += v. Gravity applies on y while y is above the floor.
- Facing is rotated toward atan2(v) by at most `0x1000` per frame (VERIFIED: `0xC000`→`0xD000`→`0xE000`→…).
  Motion starts in the new direction at once; only the sprite turns gradually.

## 4. Collision model

Collision is a point test against a **16×16 px tile grid with per-pixel height functions**, plus circle tests
against actors. It is not tile-locked movement.

- **Cell lookup** (`FUN_080120DC`, VERIFIED):
  - Cell = `layer_base + ((x>>4) + (z>>4)*128) * 4`, so maps are 128 cells wide with 4 bytes per cell.
  - There are 3 layers. The base pointers are at `map+0x130`, `+0x160` and `+0x190`, where `map = *(0x03001E70)`;
    the default base is `0x02010000`. The object's layer is its byte +0x22.
  - Cell byte 2 = `0xFF` means solid (result 2). Otherwise byte 2 is a class or event id, which the tile-event
    probe and the ladder check use.
  - Cell byte 3 is an index into a **height-shape table** at `0x0202C000` (4 bytes per entry). The entry's
    byte 0 low nibble selects one of 16 shape functions (table `0x080134FC`, code `0x08011CE0`–`0x08011F48`).
    Bytes 1–3 are signed heights in **8 px units**.
  - Shapes seen: flat; slope along x; slope along z; diagonal slope in two segments; step at x = 8. The rest are
    INFERRED variants.
  - A shape function returns the ground height at the probe's (x&15, z&15).
- **Walkability**: diff = ground height − object floor (+0x14).
  - **diff > +8 px**: wall.
  - **diff < −12 px**: drop, also blocked.
  - Anything in between is walkable; small steps up and down are automatic and gravity smooths them. Live: y went
    160→156→152 on stairs.
- **World map** uses a different grid: 32 px cells, 32×32 cells (`>>21`), checked by `FUN_080122AC` (terrain
  classes 5–12).
- **Map container** (`FUN_0800FB38`, file = `0x128` + u16 from the 12-byte record at `0x08013784 + area*12`):

| Part | Destination | Role |
|---|---|---|
| +0x24 | `0x02010001` | then `FUN_0800F9F4`; probably tiles or tilemap staged in a scratch buffer (INFERRED) |
| +0x28 | `0x0202C000` | **height-shape table** (VERIFIED by the reader above) |
| +0x2C | `0x02010000` | **collision/height cell map**, 128 × rows × 4 bytes, then `FUN_0800FAC8` (VERIFIED as the cell map) |
| +0x30 | `0x0202D000` | `FUN_080118D8` (INFERRED: event or trigger data) |
| +0x34 | `0x0202DE00` | `FUN_08011A84` (INFERRED: event or trigger data) |
| +0x38 | – | kept as a pointer at `map+0x10` |

  Header fields:
  - Bytes 0–3 ×8 px go to `map+0xEC..0xF8` (camera or bounds, INFERRED).
  - Bytes 0xC and 0xD ×8 px give the origin. The layer-0 base is `0x02010000 + ((b[0xD]>>1)*128 + (b[0xC]>>1))*4`.
  - Bytes 0x10 and 0x11 are signed, ×`0x1000`.
  - Bytes 0x12 and 0x13 go to `map+0x12C` and `+0x12E`.

## 5. Interaction probe (A button)

`FUN_0800EAF8` turns new presses of the mapped buttons into request flags in the field state; A becomes +0x172.
The field loop `FUN_0808C4F8` then tries these in order (VERIFIED by decompile):

1. **Actors** (`FUN_0808DDEC`). Pick the nearest actor that passes all of these:
   - |dy| ≤ 48 px (`0x2FFFFF`);
   - 3D distance **< 32 px** (multiplied by 10/13 when flag 0x400 is set, so 41.6 px);
   - **distance < 12 px, or bearing within ±67.5° (±`0x2FFF`) of facing**;
   - flag 0x800 not set.

   If that actor has an event (`FUN_0808D5A4`), it runs. GS2 uses the same literal pool (`0x080CDA4C`,
   `0x080D4CC0`).
2. **Tile event** (`FUN_0808CE74`). Take the cell **16 px ahead along facing**; its byte 2 is the event id.
   - Ids `0xF2`–`0xF7` also need the ground there to be within [y, y+64 px].
   - Other ids are looked up as type-3 events.
   - `FUN_0808BD24` is the same 16 px probe and returns the raw id.

## 6. Field Psynergy and jumping (partly INFERRED)

Field Psynergy itself is specified in `gs_field_psynergy.md` (cast `0x0808E680`, targeting in 4 directions with
per-Psynergy ranges, type-5 room events). Two guesses made here earlier were wrong (corrected by that pass):

- **`FUN_0808EF70`** is not a Psynergy cast: it spawns the "item pops out of a chest" sprite. It takes the point
  16 px ahead along facing, snaps it to its 16 px cell (`& 0xFFF00000`), adds 8 px, and spawns an effect object
  (type 0x16) there, 16 px up, falling with vy 2 px and gravity 0.25.
- **`FUN_08012B2C`** is not Psynergy targeting. It builds rays (kind 0x14: two 40 px rays along the facing angle and
  its opposite; other kinds 56 px) depending on a byte in the map header; its purpose is still **open**.
- **Gap and pillar hop** (`FUN_08093C00`):
  1. Snap facing to 4 directions (`(a+0x2000)&0xC000`) and start from the cell centre.
  2. The point 16 px ahead must not be a wall, and 32 px ahead must be walkable.
  3. Jump 2 cells at max 3 px/frame, accel 2, vy 4 px/frame, chaining while the landing cell id is `0xF9`.
  4. Pillars and objects to hop to are found by `FUN_08093AF8`: nearest within 40 px, and either < 24 px or
     within ±67.5° of facing.

## 7. Live session (GS1, mGBA 0.10.5 via GDB; VERIFIED)

- **Boot**: 4,598 frames of scripted A/Start taps from the in-game save until the on-foot controller ran.
- **Measurement**: then 1,820 logged frames. For each of 8 directions, without and with B: 40 frames of input,
  12 idle frames, 40 frames in the opposite direction, 12 idle frames.
- **Result**: every unobstructed segment matched the constants above. Segments that ran into walls show the
  deflection and stop behaviour.
- **Coverage caveat (from the verification pass)**: the save point was hemmed in. Walking reached steady speed only
  going east and west; south, south-west, south-east, north and north-east were blocked, and north-west slid along a
  wall. Running east and west was blocked. The steady-speed figures for those directions therefore come from the
  constants in code, not the live log; a second run in an open area would confirm them.

Sample rows from `walk_SE`, input Down+Right walking (`dpos` = px moved that frame):

| i | facing | vx | vz | dpos |
|---|---|---|---|---|
| 1 | `0x7000` | 0.1767 | 0.1767 | 0.25 |
| 4 | `0x4000` | 0.6988 | 0.6988 | 0.988 |
| 6 | `0x2000` | 0.7093 | 0.7093 | 1.003 |

`run_SE` levels off at vx = vz = 1.0630 (|v| = 1.503); across all diagonal run segments the typical value is
1.0607 (= 1.5/√2), with 1.0630 in only 2 of 6.

## Open questions

- Why the destination is 6 px ahead when walking and 4 px when running, when the wall probe is 8 px.
- What map container part +0x24 is, and what parts +0x30 and +0x34 hold.
- The full list of 16 height shapes.
- What `FUN_08012B2C`'s rays are for (map-header byte driven; not Psynergy targeting).
- GS2 equivalents of the collision and talk functions: the literal pools match, but the functions weren't
  decompiled. GS2's sine table also isn't at a matching byte pattern.
- How many sprite directions the walk animation uses (`FUN_0800C300`).
