# Golden Sun world map and sailing (GS1 + GS2)

Module `gbax\codecs\gs_worldmap.py`. Output goes to `games\<slug>\worldmap\`. The world map is GS1 area 1 / room 2,
and the GS2 world map is also room 2. `gs_maps` exports it as a 1-metatile stub, because it uses a different format.

Re-run (about 8 s for GS1 and 40 s for GS2; it reads the `gs_maps` room export for entrances, warps and actors when
that export exists):

```
.venv\Scripts\python.exe -m gbax.codecs.gs_worldmap "games\AGSE-5c469520-Golden-Sun-USA-Europe\rom\Golden Sun (USA, Europe).gba"
.venv\Scripts\python.exe -m gbax.codecs.gs_worldmap "C:\Users\aaron\OneDrive\Apps-Roms\Golden Sun - The Lost Age (USA, Europe).gba"
```

Options: `--out DIR`, `--no-tmj`.

## Outputs (`worldmap\`)

| File | Content |
|---|---|
| `composite.png`, `composite_quarter.png` | The back layer with the front layer drawn over it, at 1 px per screen px. GS1 is 4096×5120 and GS2 is 8192×8192. Each cell uses the graphics variant of its own region, see below |
| `layer_back.png`, `layer_front.png` | The two BG layers as RGBA. Colour 0 is transparent |
| `worldmap.tmj` + `tileset.png` | Tiled map with 16 px cells. Tile layers `back` and `front`; object layers `events` (step cells with warp target and room name), `entrances` (arrival points) and `actors` (placed icons with a static position). GS1 has 4,671 unique metatile images and GS2 has 12,842 |
| `terrain_classes.png` | 8-bit grey, one pixel per 2×2 px, value = terrain class 0–15 (the game's `GetWorldMapCollision`). `terrain_preview.png` is a colourised copy |
| `regions.png`, `events.png` | One pixel per 16 px cell: region kind, and back-layer event id |
| `cells.json` | Flat per-cell arrays: `kind`, `flag31`, `event_back`, `variant` (GS2 also has `flag30`) |
| `worldmap.json` | Format facts, variants and files, behaviour table, movement, encounter rules and zones, a per-region summary, events, entrances, actors, warps and verification lines |

## Format

All of this is VERIFIED from alchemy's GS1 C (`FIELD\COMMON\MAP\MAP5.C`, `MAP6.C`) and checked against the ROM
bytes. GS2 is VERIFIED by Ghidra decompile or capstone, as noted in each row.

| Item | GS1 | GS2 |
|---|---|---|
| Scene setup | `Map_InitializePerspectiveScene`, literal pool `0x08010CC4`. Mode 2: BG3 (back) uses screen `0x06004000` and chars `0x06008000`; BG2 (front) uses `0x06005000` and `0x0600C000`. Both are 512×512 affine, 8bpp | same layout (`FUN_0802B878` writes the same VRAM) |
| Chunk table | file `0xD4`: 2×320 u32 offsets from the file start, 16×20 chunks. All 640 are non-zero | file `0x197`: 2×1024 offsets, 32×32 chunks. 1,079 of 2,048 are non-zero; 0 means an empty chunk, which `FUN_0802B878` clears |
| Chunk | byte-LZ with no format byte (`Resource_DecodeByteLz`), 0x400 B = 16×16 cells × u32 | same |
| Cell u32 | bits 0–15 metatile; 16–23 event id; 24–30 region kind; 31 flag | bits 0–15 metatile; 16–23 event id (255 = solid, `0x0802DA88` → walk and ship checks); 24–29 kind; 31 flag |
| Metatile | file `0xD5`, 4,386 × 4 B: 8bpp tile numbers TL, TR, BL, BR. Screen row = 64 B (`Map_WriteLayerCellTile`) | file `0x198`, 10,980 metatiles |
| Variant table | `0x080132CC`, 2×6 file ids: palette (byte-LZ, 448 B), banks 0–3 (8 KB each), layer data (16 KB, `gMapLayerData`, purpose open) | `0x0802ED34`, 4×9 ids: palette, animation, collision, banks 0–3, 2 animated banks |
| Variant choice | the kind under the player: 21 → 1, else 0 (`WorldMap_LoadGraphics`) | `FUN_0802BE4C`: kind/10 → 3:3, 2:2, 4:1, else 0. The division helper is INFERRED; gsmagic agrees |
| Banks per layer | back = banks 0–1, front = banks 2–3 | same |
| Collision | file `0xD7`, 4 KB, shared by both variants. Bytes 0–0x7FF are back-layer tiles, 0x800–0xFFF front-layer tiles. 8 B per 8×8 tile = 4 rows × 2 B, 4 bpp, low nibble on the left | per variant (variant field 2). Getter `0x0802DAC0` is the same code |
| Class lookup | front tile nibble if non-zero, else back tile nibble if non-zero, else **7** | same |
| Other files | `0xD6` animation, 930 B, loaded to `0x0202D000` | `0x199`, 38 B (open) |

**Coordinates.** World positions are 16.16 in units of 0.5 image pixel. The evidence: the collision getter takes
`x>>17` as screen pixels, and the block index is `x>>21` per 16 px cell. Divide entrance and actor x and z by 2 to
get pixels. Check: 71 of 81 GS1 entrances (and 71 of 87 in GS2) land on walkable classes 5–12.

**Streaming.** The game keeps a 2×2-chunk window (32×32 cells) and wraps it with `&31`. `Map_SetWindowCellTile`
can put **any** chunk into a window slot. The chunks outside the real world are story replacements and test
pieces. In GS1 these are chunk rows 16–19, for example an alternate Vale/Mt Aleph area; in GS2 they are the top-left
blocks. Which chunk replaces which, and on which flag, comes from room-2 scripts (INFERRED purpose; open).

**Rendering note.** The game swaps the whole palette and tiles when the player crosses into another variant's
region, and sea and river tiles animate. The export uses each cell's own variant and frame 0, which is the right
picture for a static port.

## Terrain classes and behaviour

- Walking: classes **5–12** are walkable.
  - GS1 `CheckWorldMapCollisionRange`.
  - GS2 `0x0802DB64`, which first refuses event id 255. VERIFIED.
- GS2 ship, `0x0802DB88` (VERIFIED by disassembly):
  - refuses cells with event 255;
  - requires the ship-state byte `*(0x0300006C) + 0xD3A` to be 0, 1 or 2;
  - then allows classes **1–4 and 6**.
- GS2 raised ship, `0x0802DBD0` (VERIFIED code; meaning INFERRED):
  - Below 4 px height (obj+0xC < 0x40000), the allowed classes are 1–4 and 6.
  - Otherwise the allowed classes depend on the same state byte:
    - 0 → 1–6;
    - 1 → 1–8;
    - 2 → 1–8 and 10;
    - other values → 4–8 and 10.
  - This looks like the Hover and Wings of Anemos upgrades letting the ship pass shallows, reefs and low land.
- Class meanings (INFERRED from the behaviour keys and the preview):
  - 1–3: sea, deep to shallow.
  - 4: shallows, reefs and rivers. Rivers on land show as class 4.
  - 5–12: land kinds. 9 is forest (key 2) and 6 is shore (key 7; the ship and walking both allow it).
  - 13: the impassable ring at the world's edge (GS2).
  - 14, 15: blocked mountains and cliffs.

**Behaviour key** = `table[group + class]`:
- GS1 `GetWorldMapTerrainBehavior`, table `0x0801353C`, 3×16. Group 0x10 if bit 31, 0x20 if kind == 21.
- GS2 `0x0802DC48`, table `0x0802F004`, 5×16. Group 0x10 if bit 31, 0x20 if kind > 40, 0x40 if kind == 36,
  0x30 if kind is 12 or 15.
- The key picks the encounter rule and the battle background (`BattleFx_SelectResultPointer`).

Tables, by class 0–15:

- GS1 group 0: `0 0 0 0 0 1 7 1 1 2 1 1 1 1 0 0`
- GS1 group 0x10: `0 0 0 0 0 4 7 1 1 6 1 1 1 1 0 0`
- GS1 group 0x20: `0 0 0 0 0 5 5 5 5 6 5 5 5 5 0 0`
- GS2 group 0: `0 8 8 8 10 1 7 1 1 2 1 1 1 1 0 0`
- GS2 group 0x20: `0 9 9 9 9 5 5 5 5 6 5 5 5 5 0 0`
- GS2 group 0x40: `0 9 9 9 9 11 11 11 11 12 11 11 11 11 0 0`
- GS2 groups 0x10 and 0x30 are group 0 with class 5 → 4 and 3 respectively.

## Encounters

The lookup is VERIFIED: alchemy `BattleFx_LookupResult` and `Encounter_SelectEnemyGroup` for GS1, and GS2
`FUN_080C9F2C`.

1. The game finds the region and the behaviour key at the leader's position.
2. It walks the 8-byte rules `{s16 region, key (-1 = any), flag (-1, else the rule applies while the flag is
   clear), zone}`. The first match wins.
3. The zone indexes the 0x1C encounter table (`gs_units_items.md`).

The step formula comes from alchemy:
- rate += 5 × clamp(average level − target level, 0, 5);
- step = rate-scaled, with a random bias that is re-rolled after each battle;
- `encounter_steps` accumulates against 0x100000.
- Encounters are suppressed by flags 0x160/0x161, by `no_encounters`, and by level > 130 with flag 5.
- Flag 0x15F forces an encounter.

**GS1** rules at `0x0809D7A8`, 32 rows (region: zone for keys 4/7/1 (3), then zone for key 2):
- region 1: 7 / 8
- region 2: 13 / 14
- region 21: 29 for key 5, 30 for key 6
- region 31: 37 for key 1, 38 for key 2
- region 3: 45 / 46
- region 4: 54 / 55
- region 5: 64 / 65
- region 6: 80 / 81
- Key 3 is never produced by GS1's table, so its rows are dead (INFERRED).
- Region 0 (land outside any region) has no encounters.

**GS2**: region = kind % 20 (`FUN_0800206C`; modulo INFERRED). The field-state mode byte `0x02000452`
(`0x02000240 + 0x212`) picks the rule table:
- **8**: no encounters.
- **7**: ship table `0x080EEF34`. Region 7 → zone 52, region 8 → 77, region 9 → 52, all with key 8 (sea).
- Otherwise: foot table `0x080EEDBC`, 46 rows covering regions 1–5, 11, 12, 15, 16 and 18. Region 18 is gated by
  flag 0x8EF.

`worldmap.json` → `regions[]` lists each kind's cell count, variant, rules and the warp targets inside it.

## Entry points and events

- **Step cells**: cell byte 2 indexes the room-2 warp table, or a type-2 handler.
  - GS1: 21 of 21 ids resolve (Mogall Forest, Lamakan, Alpine Crossing, Tolbi-bound Ship, Crossbone Isle, …).
  - GS2: 32 of 38 ids resolve; the other 6 are open.
  - The Tiled `events` objects carry `to_room`, `to_door` and `to_name`.
- **Towns and landmarks** are placed actors (icons). Entry is by **actor contact**: VERIFIED in alchemy
  `MapActor_UpdateContact`, which uses a 160/300/200 px activity window and the sum of axis distances against the
  scaled radii. The touched trigger then runs the actor's event.
  - GS1: 41 of 48 actors have a static position.
  - GS2: only 1 of 18; scripts place the rest.
  - **Open**: the actor-trigger → warp mapping. It's in the scripts, and needs a script decompiler or a trace.
- **Entrances** (24-byte rows from room 2) are arrival points when leaving a place: GS1 has 81, GS2 has 87. They
  sit a median of about 135 px (GS1) or 170 px (GS2) from the nearest step cell, because towns use actors, not
  cells.

## Movement (from `gs_movement.md`, VERIFIED constants)

| | GS1 | GS2 |
|---|---|---|
| Walk / run on the world map (px/frame in world units = half that in image px) | `0x0800F2F8` 0.5 (acceleration 0.25) / 1.0 (1.25) | `0x080279B0` 0.5/0.25, run 1.0/0.5; `0x0802A124` 0.5/0.25 |
| Ship | none: the Tolbi-bound ship is a warp (event 74) | INFERRED `0x08028534`, 1.25/0.5 (it calls the collision getter and tests class 1–3) |
| Probes | 7 px, 1 probe | 3 probes fanned ±30° (`0x1555`), each through `0x0802DB64` (walk) or the ship tests |

Boarding and landing: on foot the player cannot enter classes 1–4. The ship can enter 1–4 and 6, so class 6 (shore)
is the shared border where control changes hands. The swap code and the ship actor are not traced (open).

## What a late-game Lost Age save would unblock (live tracing, next pass)

1. Values of `0x02000452` while walking, sailing, Hovering and flying (which values are 7 and 8), and which
   controller runs per mode (confirm `0x08028534` as the ship and get its real speeds).
2. The ship-state byte `*(0x0300006C)+0xD3A` before and after the Black Crystal, Hover (flag `0x8DF`, +0x276) and
   the Wings of Anemos. That maps the class sets above to the upgrades.
3. Boarding and landing: break on `0x0802DB88` and `0x0802DBD0` and their callers (`0x08028552`, ...) and on the
   actor-mode swap at the shore.
4. Region → graphics swap (`FUN_0802BE4C`) at the borders, and the music call `FUN_0802D088(kind)`.
5. The encounter counter (`encounter_steps`) per step on sea compared with land, to check the formula.
6. Actor-contact triggers → warps, and which chunk swaps (`Map_SetWindowCellTile`) apply at which story flags.

## Coverage

- GS1: 640/640 chunks, 4,386 metatiles, 2 variants, 32 encounter rules, 21/21 cell events resolved, 81 entrances,
  48 actors.
- GS2: 1,079 non-empty chunks, 10,980 metatiles, 4 variants, 46 foot rules + 3 ship rules, 32/38 cell events,
  87 entrances, 18 actors.
- Both composites were checked by eye. GS1 shows Angara and Gondowan plus the replacement chunk rows. GS2 shows all
  of Weyard with its world-edge ring.

## Open

- GS1 variant file 5 (16 KB → `gMapLayerData`) and GS2 `0x199`: purpose unknown.
- The animation channels (`0xD6`, GS2 variant field 1) and the animated banks are not applied.
- The six unmatched GS2 event ids and the actor → warp mapping.
- Story chunk swaps.
- Region names are only hinted at by the warps inside each region.
- The pause-screen world picture (`Field_WorldMapPicture`, 600 8bpp tiles) and its markers (`WorldMap_PlaceMarkers`
  `0x080A0138`) are not exported.
