# Art integration: the new asset libraries and 64-px art

From the asset-integration review (15–16 Oct). Six agents read the engine and the libraries in OneDrive
(LPC generator, CC0-Public-Domain-Sprites, 2d-assets, Kenney packs, Pixel-boy, DCSS and others). Each claim was
checked by an adversarial verifier, then by a critic. It builds on the art-scale decision of 15 Oct: Adept sprites
at 64×64 where possible (32×32 otherwise), other art at that scale where possible
([CHANGELOG](../CHANGELOG.md)). Anything not marked **Built** or **Decided** is **proposed**.

## 1. The core idea

The game world stays in Golden Sun pixels with 16-px collision cells, permanently. Movement speeds, room data, saves
and the ten missions' checks never change. Bigger art is absorbed by four things:

- **An art scale per sprite sheet**, written in its data. A 64-px LPC sheet says 2, so it draws at half size in world
  units.
- **A map scale from the tile size.** A 32-px tile still covers one 16-px cell, so gates and room tools keep working.
- **One UI scale** for every menu and the battle screen.
- **Later, a 480×320 picture** with the field camera at zoom 2. A 64-px sheet then lands 1:1 on screen, and Golden
  Sun rooms show at 2× (Option A).

A character's look gets named once, in `data_src/cast.json`, instead of by sprite number in every room file. Art
from the libraries comes in through committed manifests and tools that only read the library folders. They never
run anything in them and never copy a library wholesale.

## 2. Phase 1: seams and fixes (being built 16 Oct)

No decision needed. The critic trimmed it to what has a use now, in two parts.

- **Zero visible change:**
  - a UiStyle file and UI-scale seam;
  - re-layout when the Fold opens or closes (title, creator, battle);
  - a text-fit test over every authored page;
  - loaders that read our own 64-px sheets (art scale, radius, a shared cache);
  - a cast resolver that reads an optional `cast` key, with no room data rewritten yet;
  - the creator's data seam, plus clamping old saves' appearance;
  - an `emote` scene step;
  - a room-data lint test;
  - diagnostics that print the real stretch factor;
  - APK tools: drop `builds/` and `tests/` from the APK, a size report, a needed-sprites check, and a dry-run
    content rebuild list;
  - an offline LPC composer that writes previews to `builds/lpc_preview/`.
- **Visible bug fixes:**
  - ▶ and ▼ come from a tiny fallback font, since the Kenney fonts lack them and Android would substitute its own;
  - the battle command menu no longer runs off the bottom of the screen;
  - battle narration is split into pages of 3 lines;
  - the creator preview walks instead of standing;
  - enemy cast animations end instead of looping.
- **Held back by the critic until you decide:**
  - rewriting every room's actor rows to cast ids;
  - battle backgrounds and effect hooks;
  - the map-scale and gate-layer seams (wait for Phase 9 tiles);
  - a content rebuild that writes files.

## 3. The phases after that

| Phase | What | Waits on |
|---|---|---|
| 2 | Probes on a throwaway branch: a Fold readout on both screens, a 480×320 1:1 test with one LPC sheet, touch under a scaled UI, fonts, LPC contact sheets, a battle mockup, a 32-px tile spike, a palette-shader test | Phase 1 |
| 3 | Font and text | Your font decision |
| 4 | Switch to the 480×320 picture, UI scale 2, filling the Fold's screens | Probes; your picture and fit decisions |
| 5 | Asset pipeline and credits (`asset_picks.json`, `import_assets.py`, a Credits screen) | Your commit-policy decision |
| 6 | LPC Adepts in the field, then all 18 townsfolk looks together; the hero kit in the creator | Decided 17 Oct (art 3, 4, 5) |
| 7 | Battle art: LPC Adepts, backgrounds, move effects | Your battle-art decisions |
| 8 | UI art: item icons, button prompts, emotes, window frames | Your UI-art decisions |
| 9 | Tiles, area by area, without touching events | Decided 17 Oct (art 8): Golden Sun's tiles stay for the demo; only gaps (ships, Surf) get new art |

## 3a. What the Phase 2 probes showed (17 Oct)

Two probes drew the open art questions as pictures (the LPC composer over all eight Adepts on two bodies; the
Essentials library from the 16 Oct uploads rendered from its own map data; the same scene and a battle mocked at
480×320 three ways), and a critic compared them. The pictures live outside the repo (third-party art); you have them.

**Measured:**
- LPC people are 47 sheet px tall with the head, 23.5 world px at art scale 2: about 13–21% shorter than Golden Sun's
  leads (Isaac 30, Felix 31), and drawn twice as finely as the tiles. Teen, male and female bodies are the same height;
  teen differs from male only in build (shoulders 24 px against 30).
- **Essentials art is pixel-doubled throughout** (2×2 blocks everywhere; halving it is lossless): it is 16-px tiles and
  32×32 frames drawn at 2×, the same density as Golden Sun at 2× and the Pokémon pictures. It could drop onto today's
  16-px grid with no map-scale seam at all.
- The composer in the stash ran unchanged: 8 of 8 Adepts in about 1.5 s per variant, every layer credited (144 files by
  22 authors), eye credits already satisfied (art 17).
- Essentials overworld sheets only walk (4 frames, 4 directions): no idle, run, cast or emote, and their looks are
  fixed trainer classes, so they can't be the Adepts.

**The critic's recommendation: crisp people in a Golden Sun world.** Every person LPC (the 8 Adepts on the teen body
for Rowan and Corvin, then all 18 townsfolk looks together so heights agree), the world Golden Sun's tiles at 2×
unchanged, and battle all at 2× (Pokémon pictures and LPC Adepts the same pixel size, on a pixel-art backdrop: the
Essentials forest backdrop read well, its flat field one did not). Essentials stays a parts bin (its Boat, Caves,
Harbour and beach sets are worth a look for the ship gap). The LPC tile download waits until after the demo.

**Decided (you, 17 Oct, talked over in chat): the critic's look.** Every person is LPC (the 8 Adepts, then all 18
townsfolk looks together), on the adult body for the hero and Corvin; the world keeps Golden Sun's tiles at 2× for
the demo, with Essentials as a parts bin; battle is all 2×. This is the demo's art direction.

**To fix before the demo is shown (now the art pass's first list):** Tamsin's back view (red hair plus tied headband merge into a
mask shape), Corvin and Tamsin both dark red over dark red in the same crew, Nerissa's wavy hair reading as a helmet
from behind, Vesper's near-black hair on a dark outfit on dark floors; the five scripted poses room scripts call (nod,
shake_head, push, hammer, sprawled) map to LPC's emote, sit and hurt rows; Rowan's scarf and Maren's cuffs vanish in
LPC's combat poses, so battle uses the cast and idle rows or other items.

**If LPC is a no:** an all-Golden-Sun-density game: Golden Sun tiles and cast as today, Essentials townsfolk where
Golden Sun has no fitting look, no density mismatch, but the cast keep borrowed faces and the decided hero creator
(art 5) loses its kit.

## 4. Decisions for you

Recommended first. The alternatives are in brackets.

Answered on the decision page: accepted items are marked **Decided** with the date, the rest **To talk over**.
1. **Decided (16 Oct):** **The picture.** Recommended: switch to 480×320 with the world still in Golden Sun pixels (Option A), but only
   after the first 64-px art is ready and the 1:1 probe passes. [B: re-author everything in 32-px units; C: stay at
   240×160 with 32-px field Adepts; D: stretch with the 240 base, tested in the same probe.]
2. **Decided (16 Oct):** **Filling the Fold.** Recommended:
   - The picture is sized per screen, so both screens are used fully and you see a bit more world.
   - The cover screen stays landscape unless the probe shows portrait is pleasant.

   [Fixed size with black borders; allow portrait.]
3. **Decided (17 Oct):** **LPC for Adepts and townsfolk.** Recommended:
   - Adopt it through the offline composer.
   - Diagonal steps use the side-facing rows, and casting snaps to 4 directions like Golden Sun.
   - Order: the Adepts, hero and rival first, then all 18 person looks together.

   [Adepts only; draw diagonal rows.] LPC adults are about 22% shorter than Isaac at exactly half size.
   - **Probe (17 Oct):** composed and seen; the critic recommends yes, Adepts first then all 18 townsfolk together (§3a).

4. **Decided (17 Oct), alternative:** **The boy hero's body.** Recommended: LPC "teen", closer to Golden Sun's leads; the adult body for adult NPCs.
   - **Probe (17 Oct):** teen and male are the same height; teen reads as a slim youth like Golden Sun's leads, male stockier. The critic recommends teen for Rowan and Corvin; the male body's extra wardrobe (jackets, most swords) matters only for the creator and battle weapons later.
   - **Settled by your adult-mode answer (17 Oct, adult-mode.md decision 2):** the hero is an adult in canon, drawn on the
     adult body. **Proposed:** Corvin on the adult body too, so the two Earth rivals match; with every Adept an adult
     (story decision 10) the teen body is used by no one in the cast.

5. **Decided (16 Oct):** **The hero creator.** Recommended:
   - Pre-composed sheets with colour keys: 2 genders × 6 styles × 3 outfits × 3 accessories, about 13 MB.
   - A palette shader does the recolouring, so colours change instantly.
   - Eye colour uses the head's own eye ramp.

   [Layers composed at runtime and baked to the save folder, about 3 MB with more code.] Either way this rewrites
   the creator page's "paper-doll layers" line.
6. **Decided (16 Oct):** **Font.** Recommended: Kenney Pixel 16 in the message box and battle narration, and Kenney Mini 8 in menus. Both
   have real lower case. Boxes then hold 3 lines, as Golden Sun's do. [Mini 8 everywhere; keep Mini Square, which
   has capitals only.]
7. **Decided (16 Oct):** **UI scale after the switch.** Recommended: 2× everywhere at first, which looks identical to today. Decide 1×
   inner / 2× cover later. [Native 1×; per screen from the start.]
8. **Decided (17 Oct):** **32-px tiles.** Recommended: keep Golden Sun's tiles at 2× until the graphics pass. Then download the LPC base
   tilesets from OpenGameArt as the main source; that download needs your go-ahead. [CC0 only (flat top-down DCSS);
   draw our own.]
   - **Probe (17 Oct):** Golden Sun's tiles were the best-looking of the three windows; the Essentials sets are clean but modern-Pokémon and would mean redrawing all 17 rooms. The critic recommends keeping Golden Sun's tiles for the demo and using Essentials as a parts bin.

9. **Decided (16 Oct):** **Library art in git.** Recommended: commit the CC0 picks (about 1–3 MB) and gitignore the LPC output, which
   the composer rebuilds from committed recipes. [Gitignore both; commit both.]
10. **Decided (16 Oct):** **Battle sprite scales.** Recommended: whole numbers at 480. Adepts and partners at 2×; enemies at 2× for up to
    4 and 1× for 5 or more. [Keep today's fractional steps (your 1.3 and 0.7 end points).]
11. **Decided (16 Oct):** **Battle backgrounds.** Recommended: Pixel-boy's 12 day/night scenes at 1× with the horizon clamped, and night
    set per room. [A clock or story flag.]
12. **Decided (18 Oct):** **Move effects.** Recommended: hard-edged CC0 sheets now, Golden Sun's own Psynergy effects plugged in later.
    Drop the soft-rendered packs. [Decode GS effects first.]
13. **Decided (16 Oct):** **Unleash and Pokémon on their feet.** Recommended:
    - The unleashed Pokémon appears beside its Adept.
    - Pokémon pictures stand on their feet line; today they float a few pixels up.
14. **Decided (16 Oct):** **Icons, emotes, prompts, frames.** Recommended:
    - DCSS 32-px icons, plus drawn ones for Herb, Nut, Mint and the balls;
    - Golden Sun's emote sprite;
    - Kenney pixel button prompts;
    - an RPG-Frames window border recoloured to our navy.
15. **Decided (16 Oct):** **Tamsin's look.** She is Mia's sprite in one room and Garet's in another. Recommended: one female look now
    (sprite 3), and an LPC look later.
16. **Decided (18 Oct), alternative:** **Shipping less.** Recommended: after a phone smoke test, also drop the test framework (1.4 MB) and the unused
    Golden Sun 2 sprites (6 MB). Together with Phase 1 the APK goes from about 63 MB to 45 MB. [Keep them for
    Lost Age content.]
17. **Decided (18 Oct), alternative:** **LPC eye credits.** 3,263 LPC files have no credit, including the adult eyes. Recommended: use the head's own
    eyes and refuse uncredited layers. [Research their credits.]
    Your note (17 Oct): uncredited layers may be used, the game being for personal use; the composer credits
    them as "LPC contributors (uncredited)" and the research continues for the credits scroll.
18. **Decided (17 Oct):** **Tile redraws after the demo** (you asked, 17 Oct). Each room's tiles are a placeholder layer apart from its
    collision and events, so a redraw never touches missions. Recommended: right after the demo, area by area,
    starting with Stonehollow as a pilot, on the LPC base tilesets (they match the LPC people's pixel density; a tile
    art scale like the people's art_scale 2 is the only engine change; the OpenGameArt download needs your go-ahead),
    with Essentials pieces and our own drawing filling the gaps. [Essentials sets only, at Golden Sun's density, no
    engine change; keep Golden Sun's tiles for good; redraw before the demo.]

## 5. Risks worth knowing

- The Fold's real screen sizes, the stretch factors and the touch hit areas under a scaled UI are inferred; only
  the phone probe settles them. That probe needs you to install a debug APK.
- Mixed density while art arrives: Golden Sun rooms and NPCs at 2× beside 1:1 LPC Adepts.
- LPC gaps: muscular and child bodies, run and climb in many layers, staves without a spellcast.
- Key-coloured hero sheets break if the texture is compressed on import.
- Redrawn maps must keep the three layer names the engine looks for, or gates and the over-player layer break
  silently.
- OneDrive libraries can change on re-sync, so manifests pin files by checksum.

## 6. Not planned yet

The ship and Surf art (both coloured boxes today), the world map at 480, Summon and boss art, the title art,
portraits, Pokémon pictures in the menus, and field followers (none exist).
