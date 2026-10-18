# The Act I demo

The demo is missions 1 to 10 of Halcyra, played end to end on the Fold 7: great art, the decided engine features, and
the finished story with no placeholder line left. This is your order of work (17 Oct): the demo comes first, with its
art, engine and story finished; adult mode and mission 11 come after it. It is built in twelve slices, about two
agents at a time. Everything on this page is **proposed** until you answer it on the decision page. The decided rules
it builds are named by their page and number, up to your answers of 18 Oct.

## 1. What the demo is

**In:**
- Missions 1–10 as story.md §7 lists them: the prologue (1–4), Crew 1's two recruitments in either order (5, 6),
  Crew 2's interludes (7, 8), the fall of Fallhaven (9) and the Two-Earth Door (10), with crew swapping from the
  Wayfarer on.
- The decided look: every person in LPC (the 8 Adepts, with Rowan and Corvin on the adult body, then the 18 townsfolk
  looks), Golden Sun's tiles at 2×, battle all at 2×, on the 480×320 picture, with weapons and armour on the sprites
  and hard-edged move effects (art 1, 3, 4, 8, 10, 12; equipment 13).
- The decided features, built: the Start menu, pause, Settings, three save files with autosave, the Equip screen with
  its Best button, shops at Golden Sun's coin scale, the area map, the Chart, the objective line, the dormant
  Lodestar, the mirror, the day/night clock, class tiers, recruit level floors, evolution items, learning moves,
  branches, "Try again" after a lost story fight, and Flee.
- Final words for every line, written to story.md's beats and approved by you (decision 1).
- Music and sound on the decided route (assets 1).

**Out:** the list in §6.

**How it ends (decision 20):** mission 10 ends on the Wayfarer, with crew swapping unlocked and the Lodestar pointing
nowhere. Free play goes on: both crews, swapping and trading, catching, the side areas and the eggs. At the Wayfarer's
helm, the maiden voyage plays an end card ("The Breaking: to be continued"), then the credits with every maker from
credits.md, then a save prompt, and returns you to the deck. That save carries into mission 11: saves are versioned,
and every format change brings a migration (clock 4, progression 17).

## 2. What is built, what is in flight

**Built on engine main (a3d0f51):**
- Missions 1–10, playable end to end in 17 rooms (engine PRs #33–#48), each with an end-to-end check.
- Two crews with a bag each until mission 10, relay stones, swapping and trading (#36, #46, #48); bonded partners
  (#49); the waiting crew's half EXP (#50); the evolution-condition and HP-share fixes (#51, #52).
- The UI-scale seam and re-layout on fold (#53), the visible UI fixes (#54), and the field seams: the sheet loader,
  the cast resolver, the creator's data, the emote step and the room lint (#55).
- The APK pipeline, 52.9 MB (#56), and the gitignored adult-mode groundwork (#57).
- Bug-fix slice A (#58): item Psynergy, hidden unbuilt items, the Ball command, catch EXP to the Kin Garden, trainer
  pay per Adept, rests at the real maximum, story drops, the caster pays.
- The LPC composer and the eight Adepts' recipes (#59).
- Field abilities: Move, Frost, Growth, Reveal, Halt, Scoop, Whirlwind, Mind Read, Cut, Defog and Surf.
- The title (Continue, New Game), the creator (choices recorded, not yet drawn), one save slot, the Start menu
  (Psynergy, Items, Status, Save) and the touch controls.

**Decided, not built yet:** the clock, class tiers, recruit floors, the evolution rules and items, the learn-move
prompt, branches, "Try again" and Flee, the screen stack, pause, Settings, three saves and autosave, Android Back, the
Equip screen with its Best button and shops at Golden Sun's coin scale, the pockets, the area map, the Chart, the
objective line, the mirror, the Lodestar's new giver (Brann, with 5 Poké Balls), Vesper on Mia's curve, one growth
factor for every partner, armour and weapons on the sprite, and Ho-Oh's fixed-length judgement on damaging moves only,
after which it flies off with no Summon (story 9; progression 18 and 20).

**In flight:**
- Bug-fix slice B, engine PR #60 (open): battle and bonded-partner fixes, gear by slot, one hero kit. 285 GUT tests and
  28 end-to-end checks pass on its branch.
- Slices C (crew, menu, save and input fixes) and D (progression tests and `tools/progression_check`), stacked behind
  it.
- Art part A: the probe's fix list (Tamsin's back view, Corvin's and Tamsin's colours, Nerissa's hair, Vesper on dark
  floors), the five scripted poses, the 18 townsfolk looks, and the CC0 asset pipeline with its credits.
- The review of missions 2–4, with a sceptic pass over what it didn't cover.

**Placeholders today** (from the ten mission pages):
- Every Act I line is placeholder text written to the story's beats, meant for the archived story chat.
- The cast wears Golden Sun sprites. Ho-Oh, Celebi and Mimikyu have no field sprite, the sluice beast wears a
  statue's, and there are no portraits.
- The Kestrel, the Wayfarer and Surf are coloured boxes. The title is a text label. There is no audio code.
- The Calm is a deckhand's list of places (the Kestrel's chart). Golden Sun's Angara map stands in for the world map
  behind Stonehollow's west gate and Canalport's lower town.
- The starters (Treecko, Torchic, Mudkip), Marill as the canal Kin, Mars's top Summon (Meteor, which now stays locked
  through the demo, progression 20), and the Forest and Shadow Summons ("Forest Spirit" and "Shadow Spirit", copies of
  Venus's) are placeholders.
- The big beats are narration over a fade: Groudon's stir, Ho-Oh's fire, Celebi's vision, Sael's death, Maren's
  confession, Ilse's choice.
- Each beat has one puzzle, and Tamsin's Blaze and Vesper's Cloak have no field use. Canalport is one beach room,
  Bastion Rock a docks cottage and a jail, the Bazaar one ship, the reef one wreck, the Wayfarer one deck.
- Smaller points: the Bazaar's strongbox code is never typed in; a pushed Sentinel's place isn't saved; the Vault and
  the river caves have no random battles; eleven Golden Sun sprites (missions 9 and 10) need exporting on a new
  machine.

**Found while planning: the mission 7 and 8 handovers.** story.md §14 Q1 (decided) starts each Crew 2 interlude at
the next restoration point after a Crew 1 recruitment, and Crew 1 resumes where it left off. The engine starts it at
the end of the recruitment instead. `eldergrove_heart`'s `celebi_vision` scene and the note's `scene_after` in
`lantern_reef` each end with `when` steps that switch to crew 2 and warp to Bastion Rock's shore (`m7_started`) or the
Bazaar (`m8_started`, once missions 5–7 are done). The `crew` step records where Crew 1 stood, and neither
`RestorationPoint` nor the inn menu in `game.gd` has a hook. So Crew 1 comes back deep in the tree's heart or by the
reef's rudder house, not at an inn. Decision 7.

## 3. Build order

1. **Land what is in flight.** Review and merge slices B (#60), C and D in order, art part A, and the fixes from the
   missions 2–4 review.
   - Builds: the 16 Oct bug lists (items §14, equipment §10, menus §11), `progression_check` (progression §2), the
     probe's fix list (art §3a).
   - Waits on: nothing from you. Decision 40 sets how it is reviewed.
   - Size: M.
2. **The Fold probe and the 480×320 switch.** A readout APK, then the picture switch, the field camera at zoom 2 and
   the layout tests at the measured sizes.
   - Builds: art 1, 2 and 7.
   - Waits on: decision 22.
   - Size: M.
3. **Engine rules.** The clock with save format 2 and its migration, and Lantern Reef's night decks; class tiers;
   recruit floors; Vesper on Mia's curve and one growth factor (1.0) for every partner; the evolution resolver, items,
   branches, several stages at once, Gen 8/9 and regional evolutions by mapped methods, and the learn-move prompt;
   physical moves and wild EXP; stat foods; drops and extra rewards; the rope, the Repel and the backup Psynergy items;
   gear rules, breakage and curses; recruit kits; "Try again" and Flee; Ho-Oh's fixed-length judgement on damaging
   moves only, ending with Ho-Oh flying off and the top Flame Summon still locked (`forge_sanctum` stops setting
   `calmed_flame`, and the mission checks that expect it change to match); the handovers; the Lodestar from Brann;
   the field verbs the puzzle pass needs (Blaze, Cloak and the others the crews learn by Act I's levels).
   - Builds: day-night-clock.md 1–4 and story 12; progression 1, 2, 5, 8, 10–16, 18–20; items 5, 9, 10, 13, 15, 21;
     equipment 2–6, 9, 11, 15; menus B-2, B-3; story 1, 2, 5, 9; story.md §14 Q1.
   - Waits on: decision 7. Decision 18 names the Forest and Shadow tiers, decision 34 places the bunks, and decisions
     6 and 9 set the field verbs.
   - Size: L.
4. **Screens.** The screen stack, the Start menu, the pause box and the world freeze, Android Back, Settings, three
   save files with autosave and Android backup, with pushed objects saved in place (mission 1's Sentinel); the Equip
   screen with the Best button on Y, the Gear pocket, the paged Status screen, the shop screen and its stock at Golden
   Sun's prices (Poké Balls 30 and Great Balls 100 in Act I), the Key Items pocket; the area map, the objective line,
   place banners, the Chart with DexNav's habitat marks and the dormant Lodestar; the mirror; the Credits screen; the
   Farer's Log and the Kin Garden browser; a hidden debug menu for the playtest (menus §10).
   - Builds: menus N-0 to N-13, S-1 to S-7, B-1, B-4, T-1, T-2, C-1; equipment 1, 7, 10, 12, 14 and its §8 screens;
     items 1, 2, 3, 7, 14, 17, 19, 20.
   - Waits on: slice 1 (slice C's menu and save fixes); equipment 8 (§4), for the item ids the saves hold; decisions
     32–34.
   - Size: L.
5. **Art part B1: UI art.** Kenney Pixel 16 and Mini 8, the navy RPG frame, the pixel button prompts, DCSS icons and
   the drawn gaps, the emote sprite, the expansion's Pokémon menu icons and ball art.
   - Builds: art 6 and 14; assets 4.
   - Waits on: slice 2 for the final sizes. The fonts can land before it.
   - Size: M.
6. **Art part B2: people.** The LPC cast in every room through cast ids, the named people's own looks (Ilse, Brann,
   Sael, Hask, the harbourmaster, the purser and Act I's cameos), the 18 townsfolk, the scripted poses, the hero
   creator's kit with its palette shader, worn armour as LPC layers, portraits, Pokémon on the field and followers.
   Uncredited LPC layers may be used, credited as "LPC contributors (uncredited)".
   - Builds: art 3, 4, 5, 15, 17 and §3a; equipment 13.
   - Waits on: slices 1 and 2; decisions 21, 23, 24, 28, 29 and 31.
   - Size: L.
7. **Art part B3: battle.** LPC Adepts in battle (the cast and idle rows), whole-number scales, the backdrops and the
   clock's night backdrops, the unleashed Pokémon beside its Adept, Pokémon on their feet, hard-edged CC0 move effects
   (Golden Sun's Psynergy effects plugged in later), the weapon and armour on the sprite, the Summons.
   - Builds: art 10, 11, 12, 13; equipment 13; clock 1.
   - Waits on: slice 2; decisions 17, 21, 30 and 31.
   - Size: L.
8. **Art part B4: the world.** The ships and Surf, the sailable Calm and its painted Chart, the title card, the
   opening's stills, the new rooms, the hero's house, and Essentials as a parts bin for gaps such as the swamp.
   - Builds: art 8; menus N-4, N-5.
   - Waits on: slice 2; progression 4 (§4); decisions 3, 5, 21, 23, 25, 26, 27 and 34.
   - Size: L.
9. **The story pass.** Each mission's script with its replies, staging, puzzles and eggs; the opening; Brann's 5 Poké
   Balls with the first partner (items 1); mission 4 rewritten so Ho-Oh judges and flies off (progression 20), with
   story.md's mission table and §5 to match; the backup-item placement table for your yes (story 4); every line
   through the text-fit test at the new font.
   - Builds: story 1–5; items 1; progression 20; decisions 1–20 as answered.
   - Waits on: decisions 1–20; slice 5's fonts for the fit test; slice 8's new rooms for their scenes.
   - Size: L.
10. **Balance and levels.** Encounter tables in the mission rooms (the Vault and the river caves have none today),
    wild EXP scaled to the area, every story fight re-measured with `progression_check` and `balance_fight` (Ho-Oh's
    filtered moves included), gear and coin chests at items §13's density, rest prices on Golden Sun's inn ladder,
    and Act I income near 2,800 a crew at Golden Sun's coin scale.
    - Builds: progression 1, 18 and 19; items 1, 4 and 19; equipment 12.
    - Waits on: slices 3 and 4; progression 3 and 4 (§4); decision 35.
    - Size: M.
11. **Audio.** An audio autoload (music with crossfade, effects, the Settings volume rows), the rendered tracks, the
    music and sound table, the cries.
    - Builds: assets 1; menus S-5's volume rows.
    - Waits on: decisions 36 and 37.
    - Size: M.
12. **The ending and the playtest build.** The end card, the credits scroll, the save prompt, the demo APK built from
    a clean checkout (with every sprite export the mission pages list), the playtest rounds, then a fix round.
    - Builds: decisions 20, 38 and 39.
    - Waits on: everything above.
    - Size: S, then M for the fixes.

**Side by side.** Slice 1 goes first. Then, two at a time: slices 2 and 3; slices 4 and 9 (the scripts are written
while the screens are built); slices 5 and 6, with 11 whenever an agent is free; slices 7 and 8; then 10 and 12.
Slices 3, 9 and 11 touch different files from the art slices, so any of them can fill a free agent.

## 4. Talk items that block the demo

Three are still to talk over (CHANGELOG, 17 Oct night):

- **Progression 3, target levels per mission:** blocks slice 10 (encounter tables and story-fight EXP) and the tuning
  in decision 35. The choice: about L6–7 at mission 3, L8 at 5 and L10 at 10 through more encounters and bigger
  story-fight EXP, or a flat L5–7 Act I.
- **Progression 4, Stonehollow's west gate:** blocks slice 8's world edges. The choice: close the gate onto Golden
  Sun's L14–21 Angara zones (and Canalport's lower-town exit, which reaches the same map) behind a story flag for the
  demo, or leave them open with Flee and danger markers.
- **Equipment 8, item table:** blocks slice 4 only in the item ids the demo's saves hold. The choice: keep Golden Sun
  1's table for Act I and switch later with a save migration, or switch to Golden Sun 2's superset before the demo
  (art 16 keeps the Lost Age files in the APK either way).

The other fifteen were answered on 17 Oct (night), and your note on Ho-Oh became progression 20 (decided 18 Oct).
None of them blocks the demo now:

- **Progression 8, Vesper's curve:** Mia's curve until Shadow has its own Psynergy. Slice 3.
- **Progression 9, Psynergy after L50:** no new entries. Not in the demo.
- **Progression 12, partner pace:** one growth factor (1.0) for every partner. Slice 3.
- **Progression 16, Gen 8/9 and regional evolutions:** allowed, with mapped methods. Slice 3; few demo species
  evolve that way by L10.
- **Progression 17, Weyard forms:** Weyard species ids at the Weyard data pass, with a save migration. After the demo
  (decision 16).
- **Progression 18, Ho-Oh's wasted moves:** filtered to damaging moves, then the fight re-measured. Slices 3 and 10.
- **Progression 20, Ho-Oh in Act I:** Ho-Oh judges and flies off at mission 4; the top Flame Summon unlocks with the
  caldera catch after the Breaking. Slices 3 and 9.
- **Art 12, move effects:** hard-edged CC0 sheets now, Golden Sun's Psynergy effects later. Slice 7.
- **Art 16, shipping less:** keep the Lost Age files for later content. Nothing to build; the APK stays near 52.9 MB.
- **Art 17, LPC eye credits:** uncredited layers may be used, credited as "LPC contributors (uncredited)". Slice 6.
- **Items 1, coin scale and ball prices:** Golden Sun's scale (Poké Ball 30, Great 100), and Brann gives 5 balls
  with the first partner. Slices 4, 9 and 10.
- **Items 7, ball roster:** Poké, Great and Ultra in shops plus a rare Farer Ball. Act I sells Poké and Great Balls
  (slice 4); Ultra and the Farer Ball come later.
- **Items 18, bike, rod, Dowsing Machine:** none. Not in the demo.
- **Items 25, Ho-Oh's catch style:** the classic catch after its fight, after the Breaking. Not in the demo.
- **Equipment 13, gear on the sprite:** armour layers show too, not only weapons. Slices 6 and 7, with decision 31.
- **Equipment 14, a "Best" button:** on Y, with a yes/no check. Slice 4.

## 5. Decisions for you

Recommended first. The alternatives are in brackets.

**Story and dialogue**

1. **The dialogue pass.** Every Act I line is placeholder text written for the story chat, which is archived; this
   blocks slice 9. Recommended: the engine side writes each mission's full script (scenes, named people, townsfolk,
   signs and item text) in story.md's tone and posts it as a mission page for your yes or notes before building it.
   [You write the scripts in story.md first; only the main scenes are rewritten and townsfolk keep today's lines.]
2. **The hero's voice.** story.md §4 says the player decides how the hero feels, and the creator already offers a
   talkative or a quiet hero; this blocks the scripts. Recommended: the hero speaks short lines, and at about two
   beats a mission the player picks one of two or three replies that change only the next few lines, never a flag; a
   quiet hero's replies are a nod, a shake of the head or "…". [A silent hero with no replies; replies that set flags
   later scenes read.]
3. **The opening.** New Game goes straight to the creator and then the Keeping Night; this blocks the opening's script
   and its stills. Recommended: a narrated intro of about six pages over painted stills before the creator: the six
   Wells, the sealing, the falling rim, Marrow Isle on the festival night. [Straight to the creator, as built; an
   intro staged with sprites in the engine.]
4. **Staging the big beats.** Groudon's stir, Ho-Oh's fire and escape, Celebi's vision, Ilse's runner, Sael's death,
   Maren's confession and Ilse's choice are narration over a fade; this blocks slice 9. Recommended: stage each in its
   room with actors, walks, emotes, shakes, light and the camera, and add an illustrated still for Celebi's vision and
   Sael's death only. [Sprites only, no stills; keep the narration.]
5. **Places the story names.** Saltmarsh Reach, Canalport's canals and upper town, Bastion Rock's sea-gate, cells and
   sea caves (a docks cottage and a jail stand in), the skiff journey, the Galeway chase, the Bazaar's other hulls,
   Fallhaven's collapsing cliff, the reef's other hulks and the Wayfarer's quarters and galley aren't rooms; this
   blocks the room list for slices 8 and 9. Recommended: build the ones a beat happens in (Canalport's canals for
   Surf, Bastion Rock's sea-gate, cells and sea-cave escape, Fallhaven's falling cliff road, the Wayfarer's quarters
   with one talk per Adept, and its galley), clipped from Golden Sun rooms, and keep Saltmarsh Reach, the skiff, the
   hulls, the hulks and the chase as narration. [Build every place the story names; keep today's 17 rooms.]
6. **Puzzle depth.** Most mission dungeons have one puzzle per beat, where Golden Sun's chain several; Tamsin's Blaze
   and Vesper's Cloak have no field use yet, and the Bazaar's strongbox code is never typed in; this blocks the
   scripts. Recommended: 2 to 4 puzzles per dungeon from the verbs the crew holds at that point, Golden Sun style,
   with Blaze and Cloak built and the code entered on a dial, listed on each mission's script page. [One puzzle per
   beat, as built; only the puzzles story.md names.]
7. **The mission 7 and 8 handovers.** The decided rule (story.md §14 Q1) starts each Crew 2 interlude at the next
   restoration point after a recruitment, but the engine starts it at the end of the recruitment scene (§2), and the
   rule doesn't say whether arriving or resting counts; this blocks slice 3. Recommended: after a recruitment, the
   interlude starts the next time Crew 1 uses an inn or a sanctum, as its menu closes, and Crew 1 later resumes at
   that restoration point. [Start it on entering any room with a restoration point; keep it as built and amend the
   rule.]
8. **Fallhaven's timing.** story.md has Fallhaven fall "the night after" Crew 1 deepened the Forest seal (mission 5),
   but mission 9 needs both crews full, so it plays after missions 5 to 8; this blocks mission 9's script.
   Recommended: "soon after", with the fall played at night (the scene sets the clock). [The night after Crew 2's
   heist at the Bazaar; keep the line as written.]
9. **The Hive.** Mission 5's egg is solved with Cloak and Reveal, which arrive with Vesper in mission 6, and missions
   5 and 6 can come in either order; this blocks mission 5's script and a Cloak build. Recommended: an optional
   Greenwild area that opens once Vesper is in the crew, with Cloak built for it and a reward chest at the queen.
   [Leave the Hive out of the demo; make mission 6 come before mission 5.]
10. **Act I's easter eggs.** Mission 6's three are built, while Gary Rivalson and the Mercury-blue puddle (1), Captain
    Maize and the push-the-truck rumour (3), the Tumbleweed Trio's first heist (8) and Cidrick with "A Funeral at
    Sea" (10) are not; this blocks the scripts. Recommended: all of them in the demo, each a short scene with its own
    look. [Only the eggs that need no new room; none beyond mission 6's.]
11. **Bounties at mission 8.** Items 4 (decided) counts bounties from mission 8 in Act I's income, and story.md §14
    Q17 builds them in three steps; this blocks mission 8's script and the income target. Recommended: step 1 only in
    the demo: 4 to 6 hand-written contracts on the Bazaar's Freeport Guild board from mission 8, plus wanted posters
    with terrible portraits on Tidewarden notice boards. [Generated contracts as well; a single named bounty.]
12. **Mimikyu.** It shows only with Reveal at the reef's bow, wears a placeholder sprite and can't be caught; this
    blocks mission 6's script. Recommended: a Djinn-style find: once revealed it hides twice around the wreck, then
    battles and joins with no ball, going to the Kin Garden. [A sighting only until Act II; a wild catch with a ball.]
13. **Maren's Shiny Stone.** Story 5 (decided) makes it a gift in her arc, which runs through missions 3, 9 and 13,
    while Wynn's Dawn Stone (8) and Vesper's Linking Cord (7) fall inside the demo; this blocks the item placement.
    Recommended: mission 13, her regroup chapter, so Eevee stays Eevee in the demo. [After her confession in mission
    9; when she joins in mission 3.]
14. **The starter trio.** The mission 1 page calls Treecko, Torchic and Mudkip placeholders, though story.md §4 names
    them; this blocks Brann's hatchery scene. Recommended: keep them: they cover Grass, Fire and Water, Mudkip can
    Surf, two can Cut, and their fights are measured. [Another trio you name; any Gen 1–7 starter, the player's pick.]
15. **The canal Kin.** Marill, the harbourmaster's Surf gift in mission 3, is a placeholder; this blocks mission 3's
    script. Recommended: keep Marill, a canal Water type that learns Surf. [Lotad, for Brightcoast's farms; Psyduck.]
16. **Weyard forms.** story.md §4 gives every story partner a Weyard form, DESIGN.md plans 25 Weyard families, data
    first and art last, and progression 17 (decided 17 Oct) switches the story partners to Weyard species ids at the
    Weyard data pass, with a save migration; when that pass comes blocks the partners' data and art. Recommended:
    ordinary forms throughout the demo, with the Weyard pass after it. [The eight story partners' Weyard forms in the
    demo, as palette swaps.]
17. **Summons.** Golden Sun's Summon sprites are in the ROM but not exported, and the Forest and Shadow Summons are
    placeholders ("Forest Spirit" and "Shadow Spirit", copies of Venus's); since progression 20 (decided 18 Oct) the
    top Flame Summon waits for Ho-Oh's catch, so no top Summon unlocks in the demo and only the lower tiers show; this
    blocks slice 7 and the scripts. Recommended: Golden Sun's own Summons and names for Earth, Sea, Flame and Sky,
    exported from the ROM, and our own names on recoloured Golden Sun Summons for Forest's and Shadow's lower tiers;
    the top tiers' names and art wait for Act II. [Our own names for all six groups; a Pokémon-themed Summon per
    group.]
18. **Class names for Forest and Shadow.** With class tiers decided (progression 5) and Vesper on Mia's curve
    (progression 8, decided 17 Oct), Sorrel would show Golden Sun's Wind Seer line and Vesper the Water Seer line;
    this blocks the Status screen and the tier build. Recommended: our own five names over the borrowed numbers:
    Forest "Sprout, Briar, Grovekeeper, Wildwarden, Elder Sage" and Shadow "Shade, Fogrunner, Gloamcaller,
    Nightwarden, Umbral Sage". [Keep Golden Sun's names; names written in the dialogue pass for your yes.]
19. **The islands of the week.** Dustplain, Frostmarch, Hushwater and Twin Bells are Act I places with decided shops
    (story 6), but no mission from 1 to 10 goes there; this blocks the Chart's contents. Recommended: not in the demo;
    they show on the Chart as rumours ("?") and are built after it. [Hushwater, the smallest, as a sample; all four.]
20. **How the demo ends.** Mission 10 ends on the Wayfarer, and mission 11, the maiden voyage, is not in the demo; this
    blocks slice 12. Recommended: free play goes on in Act I, and the Wayfarer's helm offers the maiden voyage, which
    plays an end card ("The Breaking: to be continued"), the credits with every maker and a save prompt, then returns
    you to the deck. [An end card straight after the Wayfarer scene; the helm refuses to sail, with no end card.]

**Art**

21. **Approving the art.** Every art slice changes how the whole game looks; this blocks slices 5 to 8. Recommended:
    each slice posts a contact sheet (cast, townsfolk, creator kit, portraits, ships, title, battle) to the decision
    page as a yes-or-redo card before it is wired in. [Build it and judge on the phone; judge only at the playtest.]
22. **The Fold probe.** Art 1 switches to 480×320 only after the 1:1 probe passes, and the Fold's real screen sizes are
    still inferred; this blocks slice 2. Recommended: you install one probe APK from `_GameMaker-builds` and send its
    readout folded and unfolded, two screenshots. [Switch on the documented sizes and fix at the playtest.]
23. **Illustrated art.** The portraits, the title card and the opening's stills need art no library has in our style;
    this blocks slices 6 and 8. Recommended: made with an image generator from written prompts and each character's
    LPC look, then reduced to the game's palette and pixel size and cleaned by hand, each on a contact sheet first.
    [Drawn by hand as pixel art, which is slower; only art already in the local folder.]
24. **Portraits.** There are none, and the creator previews one for the hero; this blocks the message box's layout.
    Recommended: a 64×64 portrait with three expressions for each of the 8 Adepts and Act I's named people (Ilse,
    Brann, Sael, Hask), beside the message box, the hero's drawn per body and hair style with colour keys so the
    creator's palette shader recolours them; everyone else gets a name tag. [Name tags only; 128-px busts in key
    scenes only.]
25. **The title screen.** It is a text label; this blocks slice 8. Recommended: a painted title card at 480×320, the
    Wayfarer under the Pinnacle with "Halcyra" in a drawn logo, slow sea and cloud parallax and the menu below. [The
    logo over a live scene, Stonehollow at dusk; the logo on the navy frame only.]
26. **Ships and Surf.** The Kestrel, the Wayfarer and Surf are coloured boxes, and Golden Sun's own boat and ship
    sprites are in the export but not yet identified; this blocks the sea and the art of missions 3–10. Recommended:
    Golden Sun's own sailing sprites for both ships, the expansion's surf-blob mount under the rider, and drawn ships
    only where Golden Sun has none. [Draw both ships at 64 and 128 px; adapt Kenney's pirate pack.]
27. **The Calm.** The Kestrel's chart is a deckhand's list of places; this blocks slice 8 and the Chart. Recommended: a
    sailable Calm built from Golden Sun 2's world-map tiles to story.md §2's layout, with the Act I places as
    landings, and the decided Chart painted once as a parchment map of the Calm; Meridia's walkable map comes with
    Dustplain and Frostmarch after the demo (decision 19), and the Angara gate is progression 4 (§4). [Keep the
    deckhand list for the demo; draw the Calm at 32 px from scratch.]
28. **Pokémon and monsters on the field.** Ho-Oh, Celebi, Mimikyu and the Litwick have no field sprites of their own,
    and the sluice beast wears a statue's; this blocks the art of missions 3–6. Recommended: the expansion's overworld
    sprites at 2×, with short appear and flight animations for Ho-Oh and Celebi, and the beast as Kraken's battle
    picture rising from the canal. [Their battle pictures as stills over the scene; our own drawings at 64 px.]
29. **Partner followers.** There is no code or decision yet, and the expansion has an overworld sprite for every
    species; this sets slice 6's scope. Recommended: the lead's active partner follows the lead on the field, hidden
    while surfing and in scenes unless a scene stages it. [No followers in the demo; the whole crew follows the lead.]
30. **Battle backdrops for the gaps.** Art 11 picked Pixel-boy's 12 day and night scenes, which have no cave, ship
    deck, jail or forge; this blocks slice 7. Recommended: Essentials backdrops for those places at the same pixel
    size (the probe found its forest one read well), each approved under your materials rule. [Pixel-boy's nearest
    scene; draw our own.]
31. **Armour on the sprite.** Equipment 13 (decided 17 Oct) shows armour layers as well as the weapon, but every
    Adept always wears body armour, and the cast's and the creator's outfits are what make them recognisable; this
    blocks slices 6 and 7. Recommended: helms, shields, gloves, and mail or plate add their LPC layer over the Adept's
    own look, in the field and in battle, mapped once per item in data; shirts, robes and other light body armour keep
    the Adept's own outfit. [Battle only, with the field keeping the cast's looks; every piece replaces its slot's
    layer, outfits included.]

**Features**

32. **The Farer's Log.** Its screen and sections are decided and its records start now, but not when the player gets
    the book; this blocks the Start menu's Log row. Recommended: found aboard the Wayfarer at mission 10, where the
    Farers left it, with every tab filled from records kept since mission 1 (Kin and Bestiary from battles, Charts
    from places visited, Relics from the story notes, the Guild Ledger from the demo's contracts) and DexNav's
    "Search here" working from it (menus N-9). [A keeper's notebook from mission 1 that becomes the Log; not in the
    demo.]
33. **The Kin Garden.** Storage works through innkeepers, but its browser and the walkable garden aren't built; this
    blocks the Pokémon screens. Recommended: the browser (paging, sorting, summary, use an item) at every restoration
    point in the demo, and the walkable garden with Marrow Isle's growth in Act II. [The walkable garden too; today's
    list only.]
34. **The hero's house and the ship's bunk.** The hero's house with its mirror and bed, shared with Brann, is decided
    (character-creator.md, adult 14) but isn't a room, and the decided "Sleep until dusk/dawn" bunk (clock 3) needs a
    place on the ship; this blocks the clock and mirror builds. Recommended: the house as a small Stonehollow room,
    its bed the home bunk, and the ship's bunk as a row on the Kestrel's deckhand (in the Wayfarer's quarters from
    mission 10), with no cabin room on the Kestrel. [A cabin room on the Kestrel too; the home bed only, with no bunk
    at sea.]
35. **Story-fight difficulty.** The recruit floors and the re-measure are decided (progression 1), but not the win
    rate to tune to; this blocks slice 10. Recommended: at the levels progression 3 settles, a player using Psynergy
    sensibly wins each story fight on the first try at least 85% of the time and an attack-only player at least 25%,
    with "Try again" for the rest. [Golden Sun's ease, about 95% with Psynergy; harder, about 60%.]

**Audio**

36. **Downloads for audio.** The decided route (assets 1) renders Golden Sun's and Unbound's tracks offline to OGG,
    and neither a renderer nor an encoder is installed; this blocks slice 11. Recommended: a go-ahead to install an
    open-source GBA music renderer and an OGG encoder from their official sources, checksum-checked by
    `tools/setup_dev.py`, when slice 11 starts. [Only tools already on disk; WAV files, with a larger APK.]
37. **Music and sound by place.** Nothing assigns tracks or sounds to places yet; this blocks slice 11. Recommended:
    Golden Sun's tracks for places, sailing, monster battles and story scenes, and Unbound's for Pokémon moments (wild
    battles, catching, evolution, the hatchery); Golden Sun's menu, field and Psynergy sounds; the expansion's cries
    when a Pokémon enters; the fan game's ambient loops where Golden Sun has none; all in one table for your yes.
    [Golden Sun's music and sounds only; Unbound's only.]

**Shipping the demo**

38. **The demo build.** Today's builds are debug APKs; this blocks slice 12. Recommended: a release-signed APK with its
    own keystore, backed up beside the debug one in OneDrive, with the debug build kept for testing. [The debug APK,
    as today.]
39. **Playtest rounds.** You test on the phone; this sets when builds reach `_GameMaker-builds`. Recommended: two
    rounds, a mid build once missions 1–4 have their final art and words and then the full demo, each with a
    playtest page where you mark every mission yes or add a note. [One round at the end; a build after every slice.]
40. **Reviews before merge.** The 16 Oct reviews used six reviewers each, and the demo has twelve slices; this sets the
    pace. Recommended: one reviewer and the end-to-end checks per PR, and one critic pass over the whole demo before
    the full playtest. [Six reviewers per slice, as on 16 Oct; checks only.]

## 6. Not in the demo

- Adult mode and everything on adult-mode.md, including the glasses' Act I find (after the demo, adult 10).
- Mission 11 (the Breaking), Acts II and III, the guest system and the post-Breaking map variants (Canalport's
  flood).
- The tile redraws (art 18: right after the demo, Stonehollow first) and the LPC base tileset download.
- A walkable Meridia world map and the four Act I islands of the week: Dustplain, Frostmarch, Hushwater and Twin
  Bells (decision 19).
- Heart quests, regroup chapters and the Adepts' ending scenes.
- Generated contracts and rival hunter crews (decision 11).
- DexNav's separate screen with chains (menus N-9: later).
- The walkable Kin Garden and Marrow Isle's growth beyond the decided Act I shops (decision 33).
- Weyard forms (decision 16; progression 17 sets the switch), Mega Evolution, the Mega Ring and the Mega Stones.
- The three mini-games (Act II).
- Rock Climb, Whirlpool, Dive, Waterfall and Teleport; the item-only verbs Lift, Carry, Hover, Grind and Sand.
- Legendary catches and every top Summon: Ho-Oh's classic catch after the Breaking unlocks the top Flame Summon
  (items 25, progression 20).
- Ultra Balls (Act II shops), the Farer Ball and the specialty balls (items 7); no bike, rod or Dowsing Machine
  (items 18).
- Golden Sun 2's item table, unless equipment 8 switches it before the demo.
- The Lodestar's needle (it wakes at mission 12) and crossing the Stillwaters.
- Golden Sun-style vision cones for guards; voice clips.
