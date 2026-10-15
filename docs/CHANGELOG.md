# Changelog of decisions

Every design decision since the phase-1 answers, newest first, with the reason. `DESIGN.md` carries a summary
header; the detailed rules are in `docs/design/`.

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
