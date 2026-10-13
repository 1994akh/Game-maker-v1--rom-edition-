# Golden Sun 1 & 2: field Psynergy, spec for a native rebuild

Exporter: `gbax\codecs\gs_field.py`. Run from `C:\Users\aaron\Documents\UnboundHack`:

    .venv\Scripts\python.exe -m gbax.codecs.gs_field all      (or gs1 / gs2; about 5 s)

It writes `games\<slug>\data\field_psynergy.json`. The file holds each Psynergy's abilities, PP, the items that
grant it, its targeting parameters (from ROM), its effect routines (from the ROM's dispatch tables), event counts,
and every Psynergy event in every room, decoded. It also has two reference functions for the rebuild:
`pick_actor_target()` (target selection) and `match_event()` (event lookup).

**Verification pass (13 Oct):**
- Confirmed: the dispatch tables are case-label tables indexed by field id − 1; Move, Frost, Growth and Reveal
  handlers are real function entries; every Psynergy event decoded here has its row in the maps export.
- **Open — puzzle targets:** the "actor index" that actor-targeted events name is usually outside the room's exported
  actor table (GS1 Move 34 of 138 inside, Frost 7 of 37, Growth 3 of 10). Same cause as the maps' actor-id problem
  (slots 0–7 probably reserved for the party; many puzzle objects created by room scripts). Needed before the puzzles
  can be rebuilt.
- **Doubtful — persistence:** flag `0x305` (used by the room-49 Growth puzzle) is also used in GS1 rooms 23 and 69 and
  in GS2 rooms 81 and 233. Flags in the `0x300` range are probably reset per room, not saved, so "one saved flag per
  solved puzzle" needs confirming before the save format is designed around it.

Inputs (read-only): the ROM, `data\abilities.json` and `items.json`, `maps\rooms\*\events.json` (from the map
job's `gs_maps`), and `text\strings.json`.

Evidence tags: **VERIFIED** means seen in ROM bytes or a Ghidra/capstone read of the code. **INFERRED** means
deduced from data or names, or from how the game is known to play. Addresses are GS1 (AGSE) / GS2 (AGFE) ROM
addresses.

## 1. Big picture

Field Psynergy works the same way in both games. **The engine plays the animation; the map's own script does the
puzzle.**

1. A request value (ability, caster, flags) comes from the Psynergy menu, an L/R shortcut, or an item.
2. The cast function checks whether Psynergy is allowed here and whether the caster has the PP, then deducts PP.
3. It works out the **target**: an actor, the tile in front, or nothing.
4. It searches the room's **event table** (map-code stub 4, see `gs_maps.md`) for **Psynergy events**. A Psynergy
   event has type low nibble 5. The search matches on the event's ability's *field id*, the target, a phase, the
   event's flag condition and, optionally, the facing direction.
5. It plays the cast animation. Then, per field id, it runs either the "targeted" effect routine (an event matched)
   or the "empty" one (nothing to affect).
6. It runs the matched event's script (a Thumb function in the room's map code) or shows its text (Mind Read).
7. **State changes are made by those scripts.** A script moves the pillar, sets the story flag, swaps the actor's
   sprite, or edits the collision. The engine routines only animate. Exceptions: Move and Lift/Carry physically
   move the target actor inside the engine routine, Frost/Growth switch the target actor's animation, and Reveal
   starts a timed view mode.

**Persistence** uses story flags (§5). Each event names a flag. The event works until the flag is set, and the
script sets the flag once the puzzle is solved. When the room loads again, its init script reads the flags and
rebuilds the solved state. The engine saves nothing per Psynergy.

## 2. Requests: menu, L/R shortcuts, items

**Request value** (VERIFIED, GS1 `0x0808E680`, GS2 `0x080CE61C`):

| Bits | Meaning |
|---|---|
| 0–9 | ability id |
| 10–13 | caster (party slot). 15 means none. Slots 8 and up skip the PP check |
| 13 (`0x2000`) | **end-of-effect cast**: goes to GS1 `0x0808E5D8` / GS2 `0x080CE574`. It runs phase-3 and phase-2 events with no PP cost |
| 14–15 (shortcut value only) | 0 = Psynergy (goes to field state +0x17E), 1 = item (goes to +0x180) |

**Field loop.** GS1 `0x0808C4F8` reads request word **+0x17E** and calls the cast at `0x0808E680`. It reads
**+0x180** and calls item use at `0x0808E23C` (VERIFIED). The field state is `*(0x03001EBC)`.

**Shortcuts** (VERIFIED code; the button identity is INFERRED):
- GS1 `0x0800EAF8` tests new key presses against the key-map halfwords at `0x02000240`: `+0x214` → A request
  (+0x172), `+0x210` → +0x174, `+0x216` → +0x176.
- Two more buttons are checked: `+0x218` and `+0x21A`. Their **stored shortcut values** are `+0x220` and
  `+0x222`, and they're passed to `0x0800EA60`, which routes the value to +0x17E (Psynergy) or +0x180 (item).
- The same function checks GBA key bits `0x100` (R) and `0x200` (L) in a special mode, which is why the two slots
  are believed to be the **L and R shortcuts**.
- GS2 `0x08026E60` → `0x08026DD0` has two call sites, so it also has 2 slots.
- Two blocks:
  - If flag `0x107` is set, the shortcut is refused: request +0x182 = `0xFA`.
  - In mode 3, L/R post `0xFC87` / `0xFC88` instead of the shortcut. Mode 3 is field state +0x19E == 3 (GS1);
    GS2 +0x18A == 3 is set when the room is the world map, VERIFIED in `0x080CB91C`.
- On the world map, GS1 refuses Reveal (`0x90`). GS2 refuses Reveal (`0x90`) and ability `0x9B`
  (VERIFIED, `0x0808E680` / `0x080CE61C`).

**Psynergy items.** "Utility" items (Orb of Force, Lifting Gem, Frost Jewel, …; item type 6) don't have their own
field path. The item adds its use-ability to the holder's Psynergy list, so the Psynergy is cast through the normal
cast with the **normal PP cost** (INFERRED from the item flags and the request format; `gs_units_items.md` lists
the item → ability pairs). The JSON lists each Psynergy's granting items.

Using an item from the Item menu goes through GS1 `0x0808E23C` (VERIFIED):
- The item id is in bits 0–9 and the holder in bits 10–13. Holder 15 means "the party member holding the most
  copies".
- It first looks for an item event (`0x0808E14C`).
- With no event, it takes the item's use-ability (+0x28):
  - prints "X used Y";
  - runs `0x08096FB0` (cast visual) and `0x08096810` (that Psynergy's *empty* effect);
  - consumes the item if item flag bit 0 says so.
- Retreat (`0x95`) has the same special-case prompt here as in the Psynergy cast.

## 3. The cast (GS1 `0x0808E680`, GS2 `0x080CE61C`): VERIFIED by decompile

1. Mask the ability (`& 0x3FF`), get the caster, and clear flag `0x145` (GS1 `0x080770D0`, GS2 `0x08016D18`).
2. Refusals:
   - Flag **`0x17E`** set: "can't use Psynergy here", text `0x91F`.
   - World-map mode: see §2.
   - Retreat (`0x95`) when flag `0x144` is clear: a yes/no prompt (text `0x920`). The answer goes to warp
     variables +0x1C0/+0x1C2 and a 999 timer.
   - GS2 extras:
     - On the world map, Hover (`0x99`) is refused unless +0x276 is set and flag `0x8DF` is set; then it
       sets flag `0x147` and posts request `0xFD`.
     - `0x8B` Sand: refused when +0x276 is non-zero.
     - `0x9C` Teleport needs a valid destination (+0x1E0).
     - Sand also asks `0x080DBCD8` whether the ground is sand. If not, no event matches.
3. **PP**: if caster < 8 and the caster's current PP (`+0x3A`) is below ability byte 9, show "not enough PP"
   (text `0x91E`) and stop. Otherwise subtract the PP **before** any target check, so casting at nothing still costs
   PP.
4. If request bit `0x2000` is set, do the end-of-effect cast instead.
5. **Event lookups**, each `search(phase_type, field_id)`: phase 1 (`0x10000005`), phase 0 (`5`), phase 5
   (`0x50000005`). GS2 first tries phase 8 (`0x80000005`) and, if it matches, runs only that event and then the
   end-of-effect cast.
6. Effect flags:
   - `0x140` = "play the engine effect".
   - `0x141` = "there is a target". It's cleared if none of the three lookups matched.
   - If the main event's id has bit `0x400`, both flags are cleared: the script animates everything itself.
7. Cast visual `0x08096FB0(ability)` (GS2 `0x080DC410`): the caster pose and the Psynergy-name banner (+0x23)
   with sound `0xD4` (+0x22). GS2 phase-5 events with id bit `0x200` turn both off (silent cast).
8. `0x080970F8(player, target)` stores the aim:
   - the cast direction is **the facing snapped to 4 directions**, `(facing + 0x2000) & 0xC000`;
   - with no actor target, the aim point is **16 px ahead** of the caster;
   - with an actor target, it's the actor's position.
9. Run the phase-1 event, then the effect routine for this field id:
   - `0x141` clear: **empty** routine. GS1 jump table `0x08096838`; GS2 compare chain `0x080DB4B8`.
   - `0x141` set: **targeted** routine. GS1 `0x0809698C`; GS2 `0x080DB670`.
10. Run the phase-0 (main) event. Then GS1 `0x08096AB0` (Mind Read cleanup) or GS2 `0x080DB848`, then end
    (`0x08097194`): free the effect objects and restore the camera.

Running an event (`0x08096B28` / GS2 `0x080CEAFC`), VERIFIED:
- script word < `0x10000`: it's a **text id**, shown in a box at the target. This is how Mind Read works (650 GS1
  events / 672 GS2).
- otherwise it's called as a map-code function `script(caster, target)`.

## 4. Targeting: VERIFIED

**Actor targets.** GS1 `0x0808DF1C`; GS2 `0x080CE31C` + `0x080CDAC0`.
- **Aim is 4-way.** The cone test uses the facing snapped to N/E/S/W even though walking is 8-way.
- Candidates are actor slots 0–0x42, skipping actors with flag `0x800` (not targetable).
- Vertical gate: |dy| ≤ vertical. GS1 default 8 px; Catch 48, Douse 64, Mind Read 16.
- Distance: dist = √(dx² + dz²) in px, which must be below the range.
  - Range: GS1 table `0x0809E686` (pairs: id → px, default 16). GS2 table `0x080EFF28`: 8-byte records {id, range,
    vertical, cone}, with the −1 record as the default.
  - Actors with flag `0x1000` (large) get ×1.5 effective range.
- Cone: skipped within 11 px. Otherwise the bearing must be within ±0x1800 (33.75°) of the 4-way facing at
  ≤ 19 px, and ±0x1000 (22.5°) beyond that. Mind Read uses ±0x2000 (45°), as do GS2 Pound, Tremor and Grind.
- The nearest qualifying actor wins.
- **GS2 difference:**
  - Only actors that **have an event** for this field id are considered.
  - A **tile event on the cell 16 px ahead** wins over actors. Teleport (id 30) tests the cell underfoot
    (`0x080CB144`) instead.
  - "Anywhere" events (type bit `0x80`) return target `0x200`.
  - GS1 instead targets whatever actor is nearest, event or not.

| Range (px) | GS1 field ids | GS2 (from `0x080EFF28`, range stored −1) |
|---|---|---|
| 16 | Ply, Frost, Lift, Carry, Growth, default | default 16; Frost, Lift, Carry, Growth, Lash, Scoop, Burst, Blaze… |
| 32 | Move, Mind Read, Whirlwind, Douse, Halt | Move, Mind Read, Douse, Halt, Pound, Tremor, Parch, Grind; Whirlwind 35 |
| 48 | Force, Catch | Force, Catch |

The full per-id values are in the JSON (`field_psynergy[].targeting`).

**Tile target**: the cell 16 px ahead along facing. Its byte 2 (event id) is matched against the event's id
(GS1 `0x0808BD24`, GS2 `0x080CB09C`).

## 5. Psynergy events in map data: VERIFIED

These are rows of the room's event table (12 bytes, see `gs_maps.md`) with `type & 0x0F == 5`. They are matched by
GS1 `0x0808E4B4` and GS2 `0x080CE458`.

| Field | Meaning |
|---|---|
| type bit `0x10` | target is an **actor**: `id & 0xFF` is the actor index in the room's actor table |
| type bit `0x80` | **anywhere**: no target needed (Reveal, Retreat, Sand, Hover) |
| neither | target is a **tile**: `id & 0xFF` is the collision-cell event id (byte 2) of the tile ahead |
| b1 | ability id. Matching uses that ability's **field id**, so Ply/Ply Well/Pure Ply, Whirlwind/Gale and the item copies all trigger the same events |
| u16 +2, bits 12–14 (GS2 12–15) | **phase**, see below |
| id bit `0x400` | no engine effect animation; the script does it all |
| id bit `0x800` | **facing restriction**: the caster's facing must be within ±0x17FF of `id & 0xF000`, e.g. a pillar that can only be pushed from one side |
| id bit `0x200` (GS2) | silent cast |
| flag | `0xFFFF` = always active. Bit `0x1000` set = active while the flag is set. Otherwise active **until** the flag is set (GS1 `0x0808D428`) |
| script | map-code pointer (`0x0200xxxx`), or a text id when < `0x10000` |

Phases (the type word masked with GS1 `0x7000000F`, GS2 `0xF000000F`):
- 0: main.
- 1: pre (before the effect animation).
- 2, 3: end-of-effect; run by the `0x2000` cast, e.g. when Reveal wears off: GS1 `0x0808E118` casts `0x2090`.
- 4: Reveal view. Looked up by GS1 `0x080984C0` with field id 8.
- 5: effect-hit. Looked up from inside the effect routine when the visual lands: Frost `0x080992A4`, Force
  `0x08098FBE`, Reveal `0x0809840A`.
- 6: GS2 only, Blaze; not traced.
- 8: GS2 override, checked first.

Coverage: **GS1 1,005 Psynergy events in 123 of 201 rooms; GS2 1,808 in 238 of 325 rooms.** Every event's ability
resolves to a field id (100%).

**Persistence example** (GS1 room 49, Bilibin Cave Entrance; VERIFIED bytes, meaning INFERRED):
- The Growth event on actor 8 has flag `0x305`.
- Its script `0x02008425` ends by calling a map stub with `0x305`, which sets the flag that disables the event.
- Room-init scripts check the same flag numbers to put the vine back on re-entry.
- The flags are saved with the normal story flags, so for the rebuild: **one boolean per solved puzzle**, keyed by
  the event's flag.

## 6. Per-Psynergy spec

**Columns**
- Field id: the ability record's field byte.
- Ability: the ability id.
- PP: from the ability table (VERIFIED).
- Target: the event kinds actually used in the map data (VERIFIED counts).
- Routines: GS1 *empty* / *targeted* effect routine; GS2 in the JSON.
- Events: number of Psynergy events, GS1 / GS2.

**State change and visuals**: VERIFIED where a routine was decompiled (Move, Frost, Growth, Reveal); otherwise
INFERRED from the game, and the per-room script is the real authority.

| Id | Psynergy (ability) | PP | Target | Range px | GS1 routines | Events GS1/GS2 | State change / visual |
|---|---|---|---|---|---|---|---|
| 1 | **Move** (140) | 2 | actor | 32 | `0x0809802C` / `0x08097C3C` | 138 / 355 | See §7. Interactive push: the player steers with the d-pad (4 directions), the actor slides 16 px per push. VERIFIED |
| 2 | Mind Read (141) | 1 | actor | 32 (cone 45°, dy 16) | `0x080984C0` both | 650 / 672 | Shows the event's text id at the NPC. No state change. VERIFIED |
| 3 | Ply series (93–95; GS2 also 731) | 4/8/12 | actor | 16 | `0x080994D0` / `0x080994C0` | 2 / 0 | Heals in the menu; 2 GS1 map events (scripted). INFERRED |
| 4 | Force (142) | 2 | actor | 48 | `0x08098CD8` / `0x08098CCC` | 22 / 7 | A force bolt travels along the aim; the phase-5 event at impact knocks a pillar or tree or rings a bell. INFERRED (phase-5 lookup VERIFIED at `0x08098FBE`) |
| 5 | Douse (33) | 5 | actor | 32 (dy 64) | `0x080999F0` / `0x080999E4` | 28 / 21 | Rain cloud over the target; the script raises water or wets dirt. INFERRED |
| 6 | **Frost** (24) | 5 | actor (puddle) | 16 | `0x08099160` / `0x08099128` | 37 / 47 | See §7: the puddle actor becomes an ice pillar (anim 2). VERIFIED |
| 7 | Lift (143) | 2 | actor | 16 | `0x08098954` / `0x08098848` | 6 / 19 | A hand lifts the boulder actor, then the script moves or removes it. INFERRED |
| 8 | **Reveal** (144) | 1 | anywhere | – | `0x080983A0` both | 46 / 46 | See §7: a 600-frame view mode; phase 4/5 events show hidden things. VERIFIED |
| 9 | Halt (145) | 2 | actor | 32 | `0x0809ADE8` (both, inline in the case) | 9 / 4 | Freezes moving actors for a while; scripts stop moving platforms or NPCs. INFERRED |
| 10 | Cloak (146) | 1 | none | – | `0x08099838` | 0 / 0 | Engine-only: the party turns invisible to field monsters/guards until moving far. INFERRED (no events in either game) |
| 11 | Carry (147) | 2 | actor | 16 | `0x0809A294` / `0x08099DA4` | 18 / 7 | Lifts the actor and carries it over a gap to a cell the player picks (like Move). INFERRED |
| 12 | **Growth** (12) | 4 | actor (sprout) | 16 | `0x080985FC` / `0x080985A8` | 10 / 6 | See §7: the sprout actor becomes a vine (anim 2) and its no-interact bits are cleared. VERIFIED |
| 13 | Catch (148) | 1 | actor | 48 (dy 48) | `0x0809AE64` / `0x0809AE58` | 13 / 2 | A hand grabs a far item actor and the script gives the item. INFERRED |
| 14 | Whirlwind / Gale (78, 185) | 5/3 | actor | 32 | `0x0809A8C4` / `0x0809A8B8` | 17 / 116 | Wind on the target: blows away leaves or bushes, reveals stairs. INFERRED |
| 15 | Retreat (149) | 6 | anywhere | – | `0x0809B208` | 9 / 0 | A yes/no prompt, then a warp to the dungeon entrance stored in +0x1C0/+0x1C2. GS1 rooms carry phase-1 "anywhere" events (9 rooms, INFERRED: where Retreat goes or why it's blocked). Flag `0x144` controls the prompt. VERIFIED code path |
| 16 | Avoid (150) | 5 | none | – | `0x0809B698` | 0 / 0 | Engine-only: no random battles for a while. INFERRED |
| 17 | Lash (133) | 1 | actor | 16 | GS2 `0x080E09C0` / `0x080E0978` | – / 29 | A rope actor is tied across a gap. INFERRED |
| 18 | Pound (134) | 2 | actor (pillar) | 32 (cone 45°, compares floor heights) | `0x080E5D5C` / `0x080E5D54` | – / 85 | Pounds a pillar into the ground; 82 of 85 events are phase 5. INFERRED |
| 19 | Tremor (135) | 1 | actor | 32 | `0x080E9090` / `0x080E8DB0` | – / 11 | Shakes the area; loose objects fall or crack. INFERRED |
| 20 | Scoop (136) | 1 | tile | 16 | `0x080E68D0` / `0x080E68C8` | – / 38 | Digs the dirt tile ahead and finds an item or stairs. INFERRED |
| 21 | Burst (151) | 2 | tile | 16 | `0x080E572C` / `0x080E5724` | – / 55 | Explodes the cracked-rock tile ahead. INFERRED |
| 22 | Parch (138) | 2 | tile | 32 | `0x080E7844` / `0x080E783C` | – / 15 | Dries water tiles. INFERRED |
| 23 | Sand (139) | 2 | anywhere | – | `0x080E4A34` / `0x080E4A2C`; end-of-effect `0x080E4730` | – / 55 | The player becomes sand (only on sand ground, `0x080DBCD8`) and slips under obstacles; phase 4 handles leaving sand. INFERRED |
| 24 | Hover (153) | 2 | anywhere | – | `0x080E9AF4` / `0x080E9AEC`; end-of-effect `0x080E9DB4` | – / 6 | Floats over quicksand or spikes for a while. INFERRED |
| 25 | Cyclone (137) | 2 | tile | (no actor targeting) | `0x080E3074` / `0x080E306C` | – / 131 | Whirlwind around the player that clears bush or grass tiles (all 131 events phase 5). INFERRED |
| 26 | Blaze (154) | 1 | actor | 16 (dy 64) | `0x080E3D04` / `0x080E3CFC` | – / 46 | Lights torches; uses phases 0, 1, 2 and 6. INFERRED |
| 27 | Grind (152) | 2 | actor + tile | 32 | `0x080E97C8` / `0x080E92B4` | – / 19 | Grinds rocks. INFERRED |
| 28 | (unnamed, 155 "Ma????") | 1 | – | – | `0x080E82CC`; end-of-effect `0x080E87C4` | – / 0 | Unused. INFERRED |
| 29 | (unnamed, 157 "A??") | 2 | actor | – | `0x080E1F2C` | – / 2 | Only in debug room 322. INFERRED |
| 30 | Teleport (156) | 3 | tile (underfoot) | – | `0x080E781C` / `0x080E7818` | – / 14 | Warps between teleport pads; the target tile is the cell underfoot. INFERRED |

GS2 routines for ids 1–16 are in the JSON (e.g. Move `0x080DD4E8` / `0x080DD054`, Frost `0x080DE688` /
`0x080DE654`, Growth `0x080DDB3C` / `0x080DDA30`, Reveal `0x080DD820`). GS2's compare-chain parse misses Mind Read
and Halt, whose case blocks are inline.

## 7. The priority four in detail (GS1 decompiled; GS2 has the same structure)

**Move** (field 1). Targeted routine `0x08097C3C`, VERIFIED constants:
1. A hand object is spawned 16 px above and 16 px in front of the target actor, then sticks to it (`+0x68`).
2. The target's max speed is set to `0x6666` (0.4 px/frame) and its collision layer to 2.
3. Loop, once per frame, until A, B, L or R is pressed (mask `0x303`):
   - Read the d-pad through table `0x0809F0F8`. **Only pure directions count**: R `0x0000`, D `0x4000`,
     L `0x8000`, U `0xC000`. Diagonals and no input give `0xFFFF`.
   - On a direction, test the cell 16 px and 32 px ahead of the actor: wall/height (`0x080120DC`), then actors
     (`0x080092A0`).
   - If the way is free, play sound `0xAF`, set speed `0x3333` (0.2 px/frame), and slide the actor **one 16 px
     cell**. Wait 15 frames.
4. Then the main (phase-0) event script runs. Scripts typically test the actor's new cell (e.g. GS1 room 12 Sol
   Sanctum: actor 9 must reach cell (31, 9)) and then set the puzzle flag.
5. Rebuild: Move = a hand on the target; the player picks one of 4 directions per step; the actor moves a cell if
   the next cell is free; the puzzle checks positions after each push; the solved flag fixes the final layout.

**Frost** (field 6). `0x08099128` → `0x08099160`, VERIFIED:
1. Sound `0x73`. Snowflake particles (object `0xE8`) spawn every 3 frames around the aim point at random radius
   2–6 px. Wait 10 frames, sound `0x73` again, wait 50.
2. If there is a target: sound `0xD4`, and the target flashes 16 times (palette 7 for 1 frame, 0 for 4 frames;
   about 80 frames).
3. Then sound `0xDC`, the target's **animation set to 2** (the frozen pillar sprite), and a new behaviour callback.
4. Phase-5 events for field 6 run (the script makes the pillar solid and climbable and sets the flag). Wait 20
   frames.
5. The target is marked (+0x23 |= 2) before the effect.

**Growth** (field 12). Targeted `0x080985A8`, VERIFIED:
- Common growth visual `0x08098698`; the target's **animation set to 2** (grown vine); its `+0x59` interaction bits
  cleared, so the vine becomes usable (climbable); +0x23 |= 2.
- Wait 10 frames, sound `0x7E`, wait 40.
- Empty cast `0x080985FC`: sound `0x86` and leaf particles (object `0xD9`) at 4–10 px around the aim point, then
  wait 30.
- The main event then sets the flag (room 49 example, §5).

**Reveal** (field 8; "anywhere" events). `0x080983A0`, VERIFIED:
1. Switch the screen to the Reveal view (`0x0808FE38(8)` and window/blend setup) and run the phase-5 events (hidden
   things appear). Sound `0x83`.
2. Record the cast centre (x, z) and a **timer of 600 frames** (10 s) in field-state slots, and set the active flag.
3. Phase-4 events are the objects drawn while the view lasts.
4. When it ends, `0x0808E118` casts `0x2090`: end-of-effect phases 3 and 2 hide things again.
5. Reveal is refused on the world map (§2).

## 8. Notes for the native (8-way) rebuild

- Keep **4-way aiming** for Psynergy, `snap4(facing)`, even with 8-way walking. Every range, cone and tile-ahead
  rule in the ROM assumes it.
- Data model per room: a list of Psynergy triggers `{field_id, target: actor|tile|anywhere, target_id, phase,
  facing_required?, flag_condition, action}`.
  - `field_psynergy.json` → `rooms[]` is already in this shape.
  - The `action` scripts are map-code Thumb functions. They have to be re-authored per puzzle; there's no script
    decompiler yet.
- Order: PP check and deduct → target → pre (phase 1) → visual (empty or targeted) → main (phase 0) → end. Timed
  effects (Reveal, Cloak, Avoid, Sand, Hover) need an end-of-effect hook (phases 2/3).
- Persistence: one saved boolean per event flag. Room init rebuilds the solved state from the flags.
- Shortcuts: two assignable slots (L and R on GBA); on a phone, map them to two on-screen buttons. A slot holds
  ability + caster (or an item).

## 9. Corrections to earlier notes

- `gs_movement.md` §6 guessed that `0x0808EF70` is the facing-tile cast. **It isn't Psynergy.** It spawns the
  object-16 "item pops out" sprite 16 px ahead. Its callers are the A-button chest/tile handler `0x0808D9A4` (types
  `0x200000` and other item-giving tile events) and `0x0808E078`. VERIFIED.
- `0x08012B2C` switches on a byte of a map header (`*(map+0x28)+4`), not on a Psynergy, so it isn't Psynergy
  targeting. Its callers are in the map module (`0x080126E2`, `0x08012758`). VERIFIED, purpose open.

## 10. Open questions

- The text of messages `0x91E`–`0x921` and `0x927` (refusal, not-enough-PP and Retreat prompts). The numbers are
  VERIFIED; the texts weren't looked up.
- The meaning of mode 3's `0xFC87`/`0xFC88` requests (world-map L/R).
- GS2's phase 6 (Blaze), and the GS2 Mind Read and Halt case blocks (inline, not parsed).
- Per-Psynergy routines other than Move, Frost, Growth and Reveal are named but not decompiled. Their "state
  change" column is INFERRED.
- The map-code scripts (the actual puzzle logic) need a script decompiler or hand translation, one puzzle at a
  time.
- The flag-number space: whether flags with bit `0x1000` are a separate bank.
- Live verification (mGBA) wasn't done in this pass; this job wasn't allowed to launch mGBA.
