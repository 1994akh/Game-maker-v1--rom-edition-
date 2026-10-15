# Changelog of decisions

Every design decision since the phase-1 answers, newest first, with the reason. `DESIGN.md` carries a summary
header; the detailed rules are in `docs/design/`.

## 15 Oct 2026 (mission 3, Surf)

- **Crew 1's Surf is a gift in Canalport** (your decision). Of crew 1's story partners only Mudkip can learn
  Surf, so in mission 3 the harbourmaster gives the hero a canal Pokémon that can (Marill, a placeholder species)
  and Surf unlocks. Water travel stays Pokémon-powered, as decided.
- **Field Psynergy is limited to the active crew** (the decided rule, now enforced in the engine): Frost needs a
  Mercury Adept, Reveal a Shadow one, Growth a Forest one.
- **Mission 3 is playable end to end** (engine PR #40): Ilse sends the hero and Maren (with Eevee) to Canalport,
  Frost plugs the beach breaches and the flood drains, the harbourmaster's gift unlocks Surf, the sluice beast,
  and the Calm opens. `docs/design/mission-3-build.md` lists the flow, the words and the placeholders.
- **Engine pieces** (PRs #38–#40): Surf in our rooms; story bosses from scaled Golden Sun enemies (the sluice beast
  is Kraken at level 8, proposed); recruits bring their story partner; rooms that change by flag (open cells and
  repaint tiles).
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

## 15 Oct 2026 (two crews, mission 2)

- **Two crews in the engine** (engine PR #36): switching crews stores the active crew's party, bag, coins,
  location and last restoration point and loads the other's. Bags and coins stay per crew until mission 10, as
  decided (§14 question 4); the Kin Garden is shared. **Proposed:** a crew's first state is its roster lead at
  the hero's level with the partner from its first trainer row, three Herbs and no coins.
- **Mission 2 is playable end to end** (engine PR #37): mission 1 ends in the handover to Corvin's crew, the
  Marrow sea caves (a Move stone), Fallhaven (Sael, the falling street, the cart, Hask's refused offer), then
  back to the hero. `docs/design/mission-2-build.md` lists the flow, where the words live and what is placeholder.
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

## 15 Oct 2026 (the battle screen)

- **Heroes on the left, enemies on the right** (your decision; engine PR #35). The party stands along the lower
  left seen from behind facing up-right, the enemies across the upper right facing down-left. Golden Sun draws
  the sides the other way round, so its sheets are mirrored; Pokémon pictures already face this way. The first
  placement had everyone facing away from their foe.
- **Sprites scale with the line** (your decision): a lone foe draws at 1.3, a full line of eight at 0.7, with the
  spacing to match (proposed steps in between: 2 → 1.15, 3 → 1.0, 4 → 0.9, 5–6 → 0.8).
- **The boxes over the sprites while choosing** (your decision): the status box (top left) and the command menu
  (bottom centre) draw over the fighters during action selection and hide while the round's words play at the
  top, as Golden Sun does; both keep clear of the touch joystick and buttons. Enemy names sit above their heads.
- **Cutscene review fixes** (engine PR #34 as merged): the Start menu is refused during a scene (a save there
  would have recorded the scene as unplayed), scenes start on the next frame so a story fight's flag can never be
  missed, fades sit under the message box, a hidden actor can't be talked to or targeted.

## 15 Oct 2026 (cutscenes)

- **Cutscenes in the rooms** (engine PR #34): a room's `events.json` can list scenes, each a list of small steps
  (words, waits, walks, turns, a camera shake, fades, flags, items, a story fight, a warp), played on entering,
  when talking to an actor, or after a story fight is won. Mission 1 now opens with the Keeping Night and the
  quake, and the hall splits after Corvin loses before he drops into the river. The lines are placeholders; the
  format is documented in the engine's `maps_src/README.md` so the story pass can write scenes directly.

## 14 Oct 2026 (story fights, mission 1)

- **Losing a story fight restarts it** (your decision). If the party is knocked out in a fight the story stages,
  such as Corvin at the Vault's inner door, the standard defeat plays and then the fight restarts from its start
  (the party, bag and coins as they were when it began). No walk back to a restoration point, no coins lost.
  Built in engine PR #33 (`Game.start_trainer_battle(..., story)`), checked end to end by `tools/mission1_check`.
- **Mission 1 is playable end to end** (engine PR #33): the Vault road gated until the starter, the Vault's upper
  halls (placeholder Sol Sanctum tiles), a Move puzzle with two Sentinel statues, Corvin's fight, Commodore Ilse
  deputising the hero and handing over the Lodestar. The lines are placeholders for the cloud chat's story pass;
  `docs/design/mission-1-build.md` lists what is built and where the words live.
- **Corvin's first fight tuned (proposed):** level 4 with a level-3 Larvitar and the hero's own Machete. The rival
  check's level-6 pair beat a new game's hero every time, which the retry rule would have made a lock; the
  engine's balance tool and a test now keep the fight beatable (Quake and an Herb win 25 of 30). Noted for the
  partner numbers: a level-5 starter falls to one Quake.
- **Fixed:** a role's dialogue pages (Brann, chests, Maren, Corvin, Ilse, post-battle pages) could not be turned
  by the player; the checks had turned them directly. They now press confirm like a player.

## 14 Oct 2026 (engine: the battle look)

- **Battle sprites come from the extraction** (engine PR #32). Enemies draw their Golden Sun sheets (161 from GS1
  and 370 from GS2, exported locally), Adepts the party sheets (Isaac, Garet, Ivan, Mia, Jenna; the hero and the
  Forest and Shadow Adepts borrow one until the graphics pass), Pokémon their pokeemerald-expansion pictures
  (front for foes, back for partners). Rounds play one entry at a time, the actor's animation before the words.
  **Proposed placeholders:** the Thief sheet stands in for rival Adepts; the animation scripts' roles are
  inferred (0 idle, 1 attack, 3 cast) and recorded in `re/notes/gs_battle_sprites.md` with the decoded format.

## 14 Oct 2026 (story)

- **The story is written** (`docs/story/story.md`), from a Q&A in the cloud chat. Tone: warm adventure with real
  stakes and no party deaths. World: rings around one walkable continent (Meridia), with an archipelago beyond.
  Areas are blocked only by puzzles, story or visibly strong monsters. Conflict in three layers: the Tidewardens
  against free islands → the Crown draining the Wells → the Farers, outsiders who built it. Villain: Lord Warden
  Vey, sympathetic. Short guided prologue, then open play. The midpoint "Breaking" changes the world map. Late-game
  airship; islands of the week with Star Trek-style dilemmas and an exploration log. All six legendaries are
  catchable, each a different way. One ending with per-Adept variations. Easter eggs and copyright-friendly spoof
  cameos from the influences run through the side stories (§9a). The world stays open after the ending for side
  quests, catching and the Log. The Farer's Log has a Pokédex-style Kin section. Extra Pokémon live in the Kin
  Garden on Marrow Isle. Bounties (§9b): the crew's own wanted bounty, a Freeport Guild board of hand-written
  and generated contracts, and rival hunter crews. Mechanics questions 19 (the post-ending world: yes) and 20
  (keep swaps at any restoration point) are decided.
- **All 20 story mechanics questions answered** (`docs/story/story.md` §14). Mostly as recommended. The changes:
  - Golden Sun-style world-map walking plus sailing.
  - A small guest system for the scattered crews after the midpoint.
  - Larger sky and undersea regions, each about a quarter of the outer sea.
  - A bigger postgame: the Farside, a full region beyond the world's edge.
  - All three mini-games built: the language puzzle, the Dodo Derby and the Glimmer Saucer.

## 14 Oct 2026

- **The story is written** (`docs/story/story.md`, PR #11, from the cloud chat): Halcyra, rings around one continent,
  two crews, a three-layer conflict, 24 missions, islands of the week, a bounty system and a postgame. Its 20
  mechanics questions were all answered by you there (§14). The ones that change play, now part of the design:
  world-map walking Golden Sun-style on the continent and large islands; a **guest system** after the midpoint (a
  found Adept fills an empty slot in the other crew until home); map variants switched by flag (the midpoint, the
  ending, the time-loop town); the airship lands only on marked pads; the sky and undersea layers each about a
  quarter of the outer sea; **the Farer's Log** (Pokédex, bestiary, charts, relics) as a menu screen; the **Kin
  Garden** on the home island as Pokémon storage, swaps at any restoration point; a **bounty system** built in three
  steps (hand-written contracts, generated contracts from templates, rival hunter crews); three mini-games from Act
  II; a bigger postgame region beyond the world's edge. The hero's default name is **Rowan**; our text uses
  `{HERO}` / `{HERO_SUBJ}` / `{HERO_OBJ}` / `{HERO_POSS}`. Engine order from the story (§12): Marrow Isle and the
  Vault first (Move, first partner, the rival battle).
- **The debug APK runs on the Fold 7.** You confirmed it on the phone. Folding, touch and controller details are still
  to be checked in play, but the build pipeline (Godot 4.7.2 → API 36 APK) is proven end to end.
- **Battle rules re-checked against Golden Sun 1's code** (`docs/design/party-and-battle.md` §4, §5, §12). The
  three open code checks are closed: enemy cap 6 slots with large enemies taking 2; EXP only to members standing at
  the end; Set/Standby countdowns tick at the end of each round (the page had said "on the Adept's own turn"). New
  from the code: a Summon gives the summoner a Power boost for the rest of the battle; turn order has a random bonus
  of up to 6.25%. Four wrong claims in the notes (Guard levels, the GS1 Summon bonus, Drain damage, PP recovery)
  are fixed in `re/`, and the formula self-test now runs 2,794 checks. *Why:* the engine's battle code is next, and
  it is tested against `gs_battle.py`, so the oracle has to be right first.
- **Local folder audited again, GitHub additions ranked** (`docs/engine/resources/local-folder-audit-2026-10-14.md`).
  Already on disk and worth lifting now: the official Godot demos (turn queue, 21:9 layout, controller remap wizard,
  JSON dialogue, RPG theme), the MetroidvaniaDeveloperSystem environment shaders and music crossfade, `lit`'s post
  shaders, the joypads remap wizard. Top adds: KoBeWi's palette-swap shader, controller_icons, gloot, Maaack's menus,
  pokerecomp (read-only), goldensunvst. Three folders must stay disabled (ziva_installer, GodotBridge, godot-mcp).
- **Golden Sun extraction pass 3** landed in `re/`: all field sprites with per-direction animations, actor slots and
  puzzle objects, exits with arrival points (GS2 warps 19% → 99.5% resolved), both world maps, Lost Age field
  Psynergy handlers, and the battle confirmations above. Notes: `re/notes/gs_field_sprites.md`, `gs_worldmap.md`,
  `gs_maps.md`, `gs_field_psynergy.md` §12, `gs_battle_mechanics.md` §13.
- **HMs merged into the field Psynergy system** (`docs/design/field-abilities.md`, PR #8). One table for both. Kept:
  Cut, Rock Climb, Defog, Whirlpool, Surf, Dive, Waterfall. Dropped: Strength (= Move), Flash (Reveal/Blaze), Fly
  (Teleport is fast travel). Rock Smash folded into Burst. HMs are free; Psynergy costs PP. *Why:* both are "an
  ability used on the tile or object ahead, gated by who's in the crew"; the engine already treats them identically,
  and the kept HMs add four new puzzle verbs.
- **Character creator settled** (`docs/design/character-creator.md`, PR #7): options approved; pronouns a separate
  choice defaulting to the chosen gender; no starter Pokémon at creation; name and gender permanent, cosmetics
  changeable at a mirror at home.
- **Engine: Godot 4.7.2** (`docs/engine/README.md`, PR #6), chosen after a three-route comparison and a challenger
  round against libGDX and Unity. The engine lives in the private repo `GameMaker-Engine`. *Why:* Godot supplies
  rendering, input, audio, saves, UI and the Android build; it was the only route scoring well on every criterion,
  with a 6–8 week path to a playable slice.
- **Golden Sun is decompiled now:** `PascalPixel/alchemy` (GS1 ~90%). `DESIGN.md`'s "no Golden Sun decomp found" is
  out of date. The extraction notes and exporters are in `re/`.
- **Story moves to the cloud chat.** Non-mechanical story decisions are made there; this repo records them.
  Graphics are remade after the engine works; music and sound near the end.

## 13 Oct 2026

- **Party and battle rules** (`docs/design/party-and-battle.md`, PR #5), replacing DESIGN.md's battle format:
  - Two crews of 4 Adepts (Crew 1: hero/Earth, Sea, Forest, Shadow; Crew 2: rival/Earth, Sea, Flame, Sky). You play
    one at a time; Adepts change crews only on the home island; Set Pokémon change only at restoration points.
  - Battles are 4 Adepts + 4 partner Pokémon vs an enemy side capped as in Golden Sun (~6 slots).
  - A Pokémon fights only while its Adept can. A downed Adept's partner gets one action (Rouse: once per Adept per
    battle, 50% / 60% if the partner matches the Adept's group, revives at 25% HP) to revive them, then withdraws.
    Adepts can fight without Pokémon. No swapping in battle except replacing a fainted partner.
  - Golden Sun's damage formulas and stat scale for everyone (the reference implementation is `re/gbax/codecs/
    gs_battle.py`); Adepts clearly out-HP partners. Golden Sun-style long Psynergy lists, no 4-slot cap. Pokémon keep
    the Pokémon-style level-up popup; Adepts' level-ups shown Golden Sun-style.
  - Set/Standby/Summons follow Golden Sun's Djinn model; Summons draw on the active crew.
  - Restoration points: Pokémon heal free, Adepts pay (a paid Adept heal heals the Pokémon too). Defeat: wake at the
    last restoration point with everyone restored, half your coins lost.
  - Story structure: the hero alone vs the rival → a mission played as the rival → recruitment missions → crew
    swapping unlocks.
  - *Why:* the 1+1 format existed only to fit the GBA's 4-fighter limit; a native app doesn't have it, and crews
    remove the riskiest battle code (switching Adepts mid-battle) while opening story possibilities.
- **Phase-1 answers** (`docs/phase1/README.md`, PR #3): native app first; code base on hold until the Golden Sun
  extraction was done; free 8-way movement; all 8 Adepts usable (later refined into two crews); the partner swaps
  with its Adept (later superseded: no swapping in battle); the engine in a new private repo.
- **Golden Sun extraction** (`re/`, PR #4): all text, every mechanics table, battle formulas, movement constants,
  maps as Tiled JSON, battle and field sprites, field-Psynergy spec, music. Verified against the ROMs and
  goldensunwiki.net.

## 12 Oct 2026

- Phase-1 research (`docs/phase1/`, PR #2): code-base comparison, movement sizing, battle-format sizing, Dive and
  water moves, the Fold 7 controls spec, a world/story proposal, a red-team review, a schedule. Written when the
  target was still a GBA ROM; its engine recommendations were superseded on 13–14 Oct, but its sizing and the controls
  spec still apply.
