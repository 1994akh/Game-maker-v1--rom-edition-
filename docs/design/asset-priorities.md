# Assets: what we make, what we reuse (31 Oct 2026)

Your rule, 31 Oct: anything we keep or use as an asset, Claude may make, or reuse and modify from the local folder, as
each slice comes up, so long as every maker is credited. This page is the plan behind that: for each kind of asset the
demo still needs, whether we reuse local material or make our own, which decision set it, and how urgent it is. It
follows the decided rules: Golden Sun's art for the rooms (art 8), LPC for every person (art 3-5), generate only where
Golden Sun has nothing (open 91) and generate in code except painted pieces (open 102). Credits go in
[credits.md](../engine/resources/credits.md) in the same PR that uses a source. Nothing from a ROM enters a public repo;
what we make goes in the engine's `assets/own`.

**Priority:** P1 blocks a mission or the playtest build; P2 is the demo's look and sound; P3 is after the demo.

## 1. The biggest things to make (in order)

1. **Interiors no Golden Sun room gives us** (P1, the interiors job): the hatchery, the sluice house, the Bazaar's hulls,
   Fallhaven's high town. Drawn in code to Golden Sun's palette and 16-pixel grid (open 102), checked beside a Golden
   Sun tile on the phone. Everything else indoors is a Golden Sun interior clipped like the rooms (open 100).
2. **The Calm's pieces Golden Sun lacks** (P1-P2, world map step 6): the Galeway's storm ring and its eye, the north fog
   and Westgloam's fog banks, the Stillwaters, the bite in the rim, Marrow Isle's reef lagoon. The compose tool joins
   them to The Lost Age's coasts and islands (world-map.md §5.5); the exporter reads The Lost Age since 31 Oct.
3. **The opening's stills, the title card and the end card** (P2): painted pieces, made with an image tool, each on a
   contact sheet for you before it goes in (open 102; the opening is scripts 1 and demo 3).
4. **The ships and the Surf mount** (P2): the Kestrel, Ketch's skiff and the Wayfarer on the world map and in the cove
   (open 97 sets their looks), plus the hero on Marill. Adapt Kenney's pirate pack where a hull fits, draw the rest at
   Golden Sun's scale; coloured boxes stand in today.
5. **Place icons Golden Sun lacks** (P2): the new islets, the Bazaar, Lantern Reef's wrecks. Golden Sun's own town icons
   everywhere else.
6. **Ambient loops** (P3, open 105): shore, cliff, rain, fog, cave drip, market, generated, short, low under the music.
7. **Dialogue portraits** (P3): illustrated art after the demo, by an image tool, the one place high-resolution art is
   wanted (art 2 and the UI slice's note).

## 2. The biggest things to reuse or modify (in order)

1. **People: the LPC generator** (P1, slice 6): the eight Adepts and the 20 townsfolk looks in every room, the hero
   creator's kit, the follower partner (open 101). Composed by tools/compose_lpc.py from the generator on disk; each
   layer credited from its CREDITS.csv, eyes as art 17 decided.
2. **Golden Sun's interiors** (P1, open 100): inns, shops, houses and halls clipped from both ROMs, one style per place.
3. **The Lost Age's world map** (P1-P2, step 6): coasts, islands, mountains and the falls' edge ring, cut along open sea.
4. **Golden Sun's sound effects and the expansion's cries** (P2, decision 105): the menu, field and Psynergy sounds
   exported from the ROM with agbplay or the music ripper (research running 31 Oct: notes/gs_sound_effects.md), cries
   from the Pokémon expansion. The engine has no sound-effect system yet: that is the audio slice's first build.
5. **The Adepts in battle: LPC's battle rows** (P2, slice 7): spellcast, thrust, slash, backslash, halfslash, shoot and
   hurt already exist in the generator, so battle Adepts are a compose recipe, not a new asset.
6. **Battle backdrops** (P2): Pixel-boy's twelve day and night scenes (art 11, art 30) and The Lost Age's ship-deck
   backdrop at sea, with a night tint and a fog version (open 103).
7. **Move and Psynergy effects** (P2): hard-edged CC0 sheets now, Golden Sun's own effects from the ROM later (art 12);
   the decompilation now shows where each effect's frames and sounds live.
8. **Pokémon everywhere** (done or P2): battle sprites from the expansion with the DS64 fallback (open 51), menu icons
   and followers from the expansion (P2), item icons from DCSS and the expansion (art 14).
9. **Smaller reuse** (P2-P3): Golden Sun's emotes (sprite 21), weapon overlays in battle (equip 13), Summon and boss
   sprites from the ROM where the battle rules keep them, the expansion's evolution-scene art, and the One Piece rips
   as a recoloured parts bin for Act II's bandits and the eggs (open 52).

## 3. Already in and not to touch again

Fonts, frames, prompts and the touch faces (Kenney, art 6 and 14, PR #84); Golden Sun's room tiles at 2× (art 8);
the room music from both ROMs (PR #80); Pokémon battle sprites (open 51); the UI's navy and its presets (PR #85).

## 4. Order against the build queue

| When | Make | Reuse or modify |
|---|---|---|
| Interiors job (next after the three branches land) | the four generated interiors | Golden Sun interiors, LPC people in them |
| World map step 4 and the Calm (step 6) | storm ring, fogs, Stillwaters, the bite, the lagoon; missing icons | The Lost Age's pieces, Golden Sun's icons, Kenney's pirate hulls for the ships |
| Missions 2-10 rebuild | nothing new (the scenes use what the rooms have) | LPC cast per mission, Golden Sun enemies |
| Art slices 6-7 | the stills, the title card | LPC battle rows, backdrops, effects |
| Audio slice | ambient loops | Golden Sun SFX, expansion cries, scene tracks (open 104) |
| After the demo | portraits, the painted Chart, the tile redraws (art 18) | Act II parts bins |

No new decision is needed for this plan: every row rests on a decided question. Where a slice finds a piece that fits
neither column, it goes on the decision page as usual.
