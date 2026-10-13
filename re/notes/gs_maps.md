# Golden Sun field maps (GS1 + GS2) — formats and exporter

Exporter: `gbax\codecs\gs_maps.py`. Run from `C:\Users\aaron\Documents\UnboundHack` with
`.venv\Scripts\python.exe -m gbax.codecs.gs_maps ROM [--map N ...] [--all] [--no-render]`.
N is a room number. Without `--map`, it exports every room. A full run takes about 70 s for GS1. The first GS2 run
took about 32 min, but the verification pass exported 3 GS2 rooms in 3.3 s, so that figure probably came from
contention with other jobs; re-time it.

**Verification pass (13 Oct), open issues:**
- **Actor ids don't match the exported actor lists.** Only 111 of 734 GS1 "talk to actor" events (GS2 303 of 876)
  point inside the room's exported actor list; with an offset of 8 it rises to 333 / 624. So actor slots 0–7 are
  probably reserved for the party, and many actors are created by room scripts rather than the actor table. This
  blocks placing Psynergy puzzle objects (see `gs_field_psynergy.md`) and is the top open item.
- **Placeholder tiles:** GS1 Mercury Lighthouse (area 56) shows ~3,300 px of solid red blocks on layer 2, drawn with
  palette row 6, which looks like a placeholder. Probably tiles the game animates or reloads at run time (tile
  animation part `+0x30` isn't applied yet).
- **Filler outside the playable area:** e.g. GS2 Champa (area 176): about a quarter of the image is a repeated
  "A" filler tile, and `walkable_bounds_px` doesn't trim it yet.
- **Tiled vs collision size:** the Tiled map is one tile larger in each direction than `collision.json`
  (e.g. Vale 31×95 vs 30×94) by design (`write_tiled`); code reading both must align them.

Output goes to `games\<slug>\maps\`:

| Path | Contents |
|---|---|
| `index.json` | Table addresses, coverage, and one entry per room: name, debug label, place group, area, per-door names, event counts, Tiled path |
| `index.html` | Gallery of area composites with room names |
| `areas\area_NNN\` | `layer0..2.png` (RGBA, colour 0 transparent), `composite.png` (backdrop + layers by priority), `tileset.png` (unique 16×16 tiles for Tiled), `palette.png`, `area.json` (header, layers, parts, palette, height shapes), `collision.json` |
| `rooms\room_NNN\` | `room_NNN.tmj` (Tiled JSON: tile layers plus object layers for tile events, entrances and actors), `events.json` (map-code tables), `map_code.bin` (the room's decompressed Thumb code, base `0x02008000`) |
| `export.log` | One line per room |

Rooms vs areas: a **room** is the game's map id. Warps, place names and map code (events) belong to rooms. An
**area** is a graphics and collision set. Several rooms can share one area (GS1: 201 rooms on 186 areas).

## Tables (both games)

| | GS1 (AGSE) | GS2 (AGFE) | How found |
|---|---|---|---|
| Room table, 8 B/room | `0x0809F1A8`, 201 rooms | `0x080F17A8`, 325 rooms | gsmagic's pointer chase from file 6 (VERIFIED: byte 2 is read by `FUN_0808A8D0`) |
| Area table, 12 B/area | `0x08013784`, 186 areas, file base `0x128` | `0x0802F380`, 332 areas, base `0x26C` | literal of `FUN_0800FB38` (VERIFIED); same chase in GS2 |
| Place-name table, 8 B/row | `0x0809DDD8`, 126 rows | `0x080EF4A4`, 110 rows | literal of the lookup loop at `0x0808B158` (VERIFIED by disassembly); GS2 found by the same Thumb loop bytes plus a data check |
| Current-room variable (s16) | `0x02000400` (INFERRED from `FUN_0808A5F4`) | `0x02000420` (VERIFIED: map-code getters compare it with room numbers) | |

**Room record**: u16 map-code file, u8 place group, u8 kind (1 or 2; 0 for a few system rooms), u16 area, u16 0.
The table runs a few rows past the last real room. The room count is taken from the debug room labels in the
location-name text group (`TITLE`, `UTIL`, `WORLD`, `PLOGV00`, ...): GS1 2567–2767, GS2 from 3768.

**Place names** (`FUN_0808B158`, VERIFIED by disassembly): rows `{s16 key, u16 door, u32 name}`, ending at key −1.
- Bit 15 of `door` set: the key is a room number. Clear: the key is the room's place group (room byte 2).
- `door & 0x7FFF == 0x7FFF` matches any door. Otherwise it's a signed 15-bit door number.
- The first match wins. Name text id = location base (GS1 2459, GS2 3672) + name.
- `index.json` gives each room's default name (first any-door row) and all per-door rows.
- Example: Vale's houses share the group name "Vale", but room 9 door 1 → "Vale Sanctum".

**Area record**: six u16 file numbers, each plus the base:
1. map container
2. palette: format 0, 448 bytes = 14 BG palettes of 16 colours
3. four tileset files: format 2, 16 KB 4bpp each, in VRAM char blocks 0–3

Every area a room uses follows this pattern: GS1 186 areas, GS2 312. VERIFIED by decoding all of them.

## Map container

Header: 0x3C bytes in GS1 and 0x40 in GS2 (the first part offset says which).

| Offset | Meaning |
|---|---|
| 0–3 | camera bounds ×8 px: x0, y0, x1, y1. Bytes 2 and 3 are the map size in 8 px units; sometimes looser than the content, e.g. 128,128 |
| 4–6 | BG priority of layers 0, 1, 2 |
| 7–9 | char-block value of layers 0, 1, 2: tile data = tile number + (value − 1) × 512. The value can be 0: layer 0 of Vale uses tile numbers 512–1023, which then start at block 0. VERIFIED visually (Vale renders correctly; gsmagic uses the same formula) |
| 0xA–0xB | 0 in all GS1 areas |
| 0xC + 8·l | layer record: x and y offset of the layer's region in the cell grid (8 px units); scroll ratio x and y (16 = 1.0, e.g. 20 for desert overlays); two signed bytes (auto-scroll, INFERRED); two bytes, usually FF FF |
| 0x24… | u32 offsets of the parts: 6 in GS1, 7 in GS2 |

Parts:

| Part | GS1 | GS2 | Status |
|---|---|---|---|
| +0x24 | metatiles: 16×16 = 4 GBA tilemap entries (tile 10 bits, h/v flip, palette 4 bits) | same | VERIFIED. Coding by `FUN_0800F9F4`: byte 0 = type; 0 = plain u16; 1 = high bytes then low bytes; 1 and 2 are cumulative XOR. The game skips even-length data |
| +0x28 | height-shape table, 4 B/shape: byte 0 low nibble = shape function (16, table `0x080134FC`), bytes 1–3 = signed heights ×8 px | same | VERIFIED (movement pass) |
| +0x2C | 64 KB cell grid, 128×128 | same | VERIFIED: ARM routine `0x0800A37C`, copied to RAM by `FUN_0800FAC8` |
| +0x30 | ~700 B, read by `FUN_080118D8` → `0x0202D000`. 8-byte records with an incrementing tile field; probably tile animation (INFERRED, not exported) | 16 KB plane (128×128 u8); gsmagic calls it a height map. Kept in `area.json` sizes only | open |
| +0x34 | `FUN_08011A84` → `0x0202DE00` (often absent) | ~900 B; looks like GS1's +0x30 (INFERRED) | open |
| +0x38 | uncompressed, pointer kept at `map+0x10` | 2 bytes (gsmagic: blend control) | open; blending code is in place but no GS2 area has the 4-byte form |
| +0x3C | – | 13–107 bytes | open |

**Cell grid** (the ARM routine's layout):
- The decompressed part has three planes:
  - bytes 0x0000–0x3FFF: byte 2 of each cell (event id; `0xFF` = solid);
  - bytes 0x4000–0x7FFF: byte 3 of each cell (height-shape index);
  - bytes 0x8000–0xFFFF: u16 per cell, the metatile id. When the low 12 bits are `0xFFF`, use the next number of a
    running counter (k-th placeholder → k).
- The planes are interleaved into 4-byte cells at `0x02010000`, which is exactly what the collision code reads.

**Layers**:
- The three BG layers (and the three collision layers) are rectangles of the same 128×128 grid, at the per-layer
  offsets.
- Layer l is BG(3−l). This comes from gsmagic's blend bits; the draw order on equal priority (higher l on top)
  follows from it. Both are INFERRED.
- Map size = header size, clipped so a layer's window doesn't run into the next layer's region. Without the clip,
  area 36 showed the next layer's tiles as a strip.

## Map code: events, NPCs, warps

- Each room's map-code file (format 0/1) is Thumb code run at `0x02008000`.
- It starts with 6–7 stubs `ldr r4,[pc]; bx r4; .word f`. Stub 0 is the room's init script.
- Stubs 1–4 return data tables. In GS1 they are plain `ldr r0,=table; bx lr`. In GS2 they often pick a table by the
  current room, because rooms share code.
- The exporter runs each getter in the Unicorn emulator with the room number set. Unicorn's translation cache must
  be flushed between rooms (`ctl_remove_cache`); without that, stale code from the previous room returns wrong
  tables.

| Stub | Table | Record | Status |
|---|---|---|---|
| 1 | entrances | 24 B: u16 id, u16 flag (FFFF), u16 x, u16 y, u16 z (px), u16 angle (0x4000 = 90°), 12 B rest; ends at id FFFF | INFERRED from shape; positions fall inside the maps |
| 2 | warps | u32: dest room (bits 0–11), dest door (12–19), event id (20–27), flags (28–31); GS1 ends at 0x1FF, GS2 at FFFFFFFF | consistency: GS1 4575 of 4952 warps point at an entrance id that exists in the target room (92%) |
| 3 | actors (NPCs, objects) | 24 B: u16 sprite, u16 flag, u8 kind, 3 B, s32 x, y, z (16.16 px), u16 angle, u8, u8; ends at FFFF | INFERRED. Index = actor number, used by type-0 events. Many rows are at 0,0 (placed later by script) |
| 4 | event handlers | 12 B: u8 type, u8 b1, u16 0, u16 id, u16 flag (FFFF = always, else a story flag), u32 script pointer (Thumb, in map code) or a text id; ends at type FF | partly VERIFIED, see below |

Event types (low nibble of the type byte):
- **0** = talk to actor `id`. The value is a script, or a text id shown directly (1,884 GS1 events resolve to
  dialogue text).
- **2** = step-on tile event: the id is the collision cell byte 2, and the same ids appear in the warp table.
- **3** = A-button on the tile ahead. VERIFIED: `FUN_0808CE74` looks tile ids up as type-3 events.
- **1, 5 and others** (0x13, 0x15 ×950, 0x21, 0x31, 0x85 …): high nibble set. Probably Psynergy-reactive
  (0x15 ≈ one per NPC, like Mind Read). INFERRED; exported raw.

Tile ids `0xF2`–`0xF9` are engine-level: ladders, hops and climb checks (see `gs_movement.md`).

Tiled objects:
- `tile events`: rectangles of equal cell event ids, per collision layer. Each carries `event_id`, `layer`, the
  `to_room` and `to_door` of its warp, and the handler script.
- `entrances`: points.
- `actors`: points at (x, z) with `sprite`, `y` (height), `angle`, and the talk script or text.

## Coverage

**GS1**:
- 186 areas: **176 render** and 10 are stubs with 1 metatile (title/utility, world map, test maps 0, 1 and
  178–185).
- Checked visually on a contact sheet of all 186: Vale, Sol Sanctum, Bilibin, Kolima, Mercury Lighthouse,
  Lamakan, ships, Tolbi, Babi Lighthouse and others look right.
- Some areas show leftover tiles outside the playable part: the camera bounds are loose, e.g. area 36. The
  `walkable_bounds_px` field in `area.json` gives the reachable box.
- 201 of 201 rooms export event tables. Totals: 1,708 entrances, 4,958 warps, 1,101 actors, 3,857 event handlers.
- Test rooms 181–186 share code whose warp table has no terminator in range: 106 junk warps each.

**GS2**:
- 312 areas used by the 325 rooms: **301 render**, 10 are stubs, and area 100 has a zero size in its header.
- Contact sheet checked: Daila, Madra, Lemuria, the Lemurian ship, Kibombo, Mars Lighthouse and others look right.
  The ship (area 194) was checked at full size.
- A few areas are only sea/sky fills or strips: 183, 184, 285–288 and 315. They're probably scrolling backgrounds
  or cut-scene maps.
- 325 of 325 rooms export event tables: 641 entrances, 8,766 warps, 2,543 actors, 5,369 event handlers.
- The warp check is weak in GS2: only 1,677 of 8,746 doors are found in the target room's entrance table. GS2
  entrance tables are short (often 1–3 ids, e.g. 0/10/20) and type-1 events are common (1,165). Arrival points are
  probably set by scripts or type-1 handlers. **Open**: the GS2 door → arrival mapping.
- Some test rooms show junk warp lists (106 rows), like GS1's.

## Not done / open

- **World map**: area 1 in GS1 (room 2). It's stored differently: 256 px chunks, files 0xD4/0xD5, 2 palettes, 8
  tilesets (gsmagic `dispWMGS1`/`dispWMGS2`). Not exported.
- **Tile animation**: GS1 part +0x30, GS2 +0x34. Not exported.
- **Parallax**: scroll ratios are recorded but not applied; the composite draws every layer 1:1.
- **Alpha blending**: needs the BLDCNT source for GS1 (+0x38 raw) and the 2-byte GS2 form.
- **Map-code fields**: the meanings of the actor bytes, the entrance "rest" bytes, the event `b1` byte, and the
  high-nibble event types. Scripts are Thumb code calling the engine through RAM stubs; they need a script
  decompiler.
- **GS2 part +0x30**: the 16 KB plane (third collision plane or height map).
- **Actor sprites**: the actor sprite numbers aren't linked to overworld sprite files yet (sprite job).

Sources: adituv/gsmagic `Form1.cs` (`loadEntireMap`, `dispMap`, `decompTileData`, `decompMap2`;
https://github.com/adituv/gsmagic, clone in `external\gsmagic`, commit ecde9b5). Every table and format above was
checked against the ROM code or data.
