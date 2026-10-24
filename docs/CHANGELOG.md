# Changelog of decisions

Every design decision since the phase-1 answers, newest first, with the reason. `DESIGN.md` carries a summary
header; the detailed rules are in `docs/design/`.

## 24 Oct 2026

- **Decided (you, 24 Oct):** the room music, open 53 to 64, all as recommended. Stonehollow and the hero's house
  move to gs1 2 (Vale's theme); Canalport gs1 10 (Tolbi), the Tradewind Bazaar gs1 6 (Kalay), Fallhaven gs2 15
  (Garoh), the Forgeheart's halls gs1 5 (the temples) and sanctum gs2 27 (Magma Rock), the Greenwild gs1 21 and the
  Eldergrove gs1 4 (the Tret Tree), Lantern Reef gs1 28 (Crossbone Isle), Bastion Rock gs1 23 (Lunpa Fortress), the
  Vault's upper halls gs1 20 (Sol Sanctum) and the Wayfarer gs2 41 (the Lemurian Ship). A room's cue can change with
  a story flag, starting with Fallhaven's sad theme after its fall.
- **Decided (you, 24 Oct):** the easter eggs, story questions 13 to 39 (story.md §9a now carries them). Original
  names and bent lines, with looks allowed from the source's art; two or three eggs per Act I mission; a Curios tab
  in the Log plus one Bounty Board rumour per region; small rewards and a full-set credits card. New cameos: the
  Spigot brothers (Mario), Turvey the turnip seller (Avatar), Captain Jory Swallow (Pirates of the Caribbean), the
  Bliss cousins (Nurse Joy), Linden (Zelda), Sabra Arn (Metroid), Captain Obed Hake (Moby Dick), Vedge (Dragon Ball)
  and Uncle Ashby (Avatar); nods from Ghibli, Dragon Quest, Zelda, Star Wars, Unbound and the GBA; the Idol Run;
  the makers' cabin, your cameo, holidays and the title-screen code. Left out: the sun knight, the inner-screen
  secret and the bridge keeper.
- **Decided (you, 24 Oct):** open question 52, the One Piece GBA sheets as a parts bin; credits row added.
- **New for your answer (story 40 to 45):** follow-ups to the egg answers: four more Avatar gags (your note on 36),
  your cameo's look and name, and how the birthday is kept.
- **Found (24 Oct):** how Golden Sun picks each room's music. Both games keep a table of rows (a room or place, an
  optional door and story flag, a song), and the first row that matches wins, so a town's music changes with the
  story. gs1 1 turned out to be Lunpa's theme, not Vale's: open 53 offers Vale's own, gs1 2, for Stonehollow.
- **New for your answer (open 53 to 64):** Stonehollow's track, corrected; Canalport; The Tradewind Bazaar;
  Fallhaven; The Forgeheart's halls; The Forgeheart's sanctum; The Greenwild and the Eldergrove; Lantern Reef; Bastion
  Rock; The Vault's upper halls; The Wayfarer; Music that changes with the story.
- **New for your answer (story 13 to 39):** 27 easter egg and spoof questions in five groups: the rules (how close,
  how many, how obvious, rewards, a full set), new spoof cameos (each with a place in Act I or II), small nods,
  themed puzzles, and personal and seasonal eggs (a makers' cabin, a cameo of you, holidays). Ask for any others
  in question 27's note box.
- **New for your answer (open 52):** The One Piece GBA sprite sheets.
- **Decided (you, 24 Oct):** open question 51, the DS-style Pokémon sprite pack kept as a backup for missing or broken
  expansion sprites (most of the 171 without one are alternate forms the pack lacks; it fills a few, such as Genesect).
- **New for your answer (open 51):** The DS-style 64x64 Pokémon sprite pack.
- **Built (engine PR #77, merged):** the first music, from your table (open 39-49): title, Stonehollow, the sea caves,
  sailing, every battle and its victory. Other rooms stay silent until 53 to 64 are answered.

## 20 Oct 2026

- **Merged (engine), demo slices 1-3 done:** the 480x320 picture with its review fixes (#72; checks pass at the
  cover's and the inner screen's sizes), the review fixes for slice 3 and missions 2-4 with Tamsin's Mace and
  Cloak on dark cells (#76), the progression rules with Eevee by day, night or stone (#73), and no coin loss on
  "No" after a lost story fight (#75). New build: `_GameMaker-builds/GameMaker-debug-2026-10-20-picture-rules.apk`.
- **Built (engine):** the fan game's non-adult parts copied in as they are (PR #74: 20,080 files, people and title
  art left out); Tamsin joins with the Mace (open 27) and Cloak works on dark cells (open 28), with the Greenwild
  glade's shade marked, in the review-fixes PR; Corvin's crew rests free at Fallhaven's inn until mission 2 is done,
  as the approved script has it. Mission 3's and 4's win rates re-measured on the current rules.

## 19 Oct 2026

- **story.md carries the approved canon** of the opening and missions 1-10 (Scripts 4, 8, 11, 14, 17 and 18) in
  §§2-9b, and the cast's ages in §4 (open question 2); the story questions page is renamed
  [story-questions.md](story/story-questions.md) (open question 26).
- **New for your answer (open 39 to 50):** Title screen and opening; Stonehollow, the home village; Caves: the sea
  caves, the river caves and the Vault's lower halls; Sailing the Calm; Monster battles; Story bosses; Wild Pokémon
  battles; Pokémon trainer battles; Victory fanfares; Catching and evolution; Sad scenes; The other places.
- **New for your answer (adult 64 to 64):** The draft Gallery plan.
- **Decided (you, 19 Oct night):** every adult review sheet and sound approved (adult 52-54 in chat, 58-63 on the
  page, and "all images in the file approved"): 160 items in the private review folder's `approved.csv`, each
  with its proposed use.
- **New for your answer (adult 58 to 63):** Review sheet 4: the smooth animation set; Review sheet 5: the expression
  frames; Review sheet 6: the small sprite pack; Review sheet 7: the character and scene cards; Review sheet 8: the
  fan game's portrait busts; The fan game's adult sounds.
- **Decided (you, 19 Oct late):** adult 52-57 and open 32-38. Adult: you keep only the review-sheet numbers you
  write in the note boxes (52 and 53, none written yet); the pixel animation set approved as the scenes' base if
  every figure is clearly an adult (54); videos at 720p and the APK under 1 GB (55); one adult quarters talk per
  night (56); the fan game's parts copied now as they are, converted when used (57). Open: adult mode's Act I
  build comes first after the demo, then mission 11 (32); **missions 11 onward are written once the demo ships**
  (33, an alternative); a Send report row in debug builds (34); playtest saves carry from build to build (35);
  Android's backup allowed (36); the music rendered to `OneDrive\Apps-Roms\_music-preview` for a table you change
  by number (37); Unbound's trainer themes and Golden Sun's boss themes (38).
- **Decided (you, 19 Oct night):** adult 25-51, as recommended except five alternatives: one APK with everything
  (25), an optional adult version of mission 10's quarters talks (40), any Adept may wield the Giant Dildo Sword
  (44), a private review of the fan game's rows with no stated age (45), and the fan game's other parts copied in
  now (46). The review sheets are in `OneDrive\Apps-Roms\_adult-review`.
- **New for your answer (open 32 to 38):** What comes first after the demo; Writing mission 11 onward; Reports from
  the phone; Playtest saves from one build to the next; Android's own backup of saves; How you pick the music; Trainer
  and boss battle music.
- **New for your answer (adult 52 to 57):** Review sheet 1: the fan game's rows with no stated age; Review sheet 2:
  the sprite strip and four loose uploads; Review sheet 3: the pixel animation set; The one APK's size; The quarters
  night in adult mode; Copying the fan game's other parts.
- **Decided (you, 19 Oct evening), all as recommended:** open questions 29-31 (Espeon and Umbreon by a day or night
  level-up and by the Sun and Moon Stones; no coin loss for turning back from a lost story fight; the five
  friendship levels kept) and Scripts 15-18 (missions 9 and 10 approved as written, their new canon accepted, and
  the Kestrel's burning send-off kept).
- **New adult-mode questions for your answer:** adult 25 to 51 on the decision page (adult mode is still built after
  the demo): How adult content reaches the phone; Hiding the game from the recent-apps view; One code for the phone,
  or one per save file; Wrong codes; The 18+ warning's words; Leaving the game quickly; The cover screen; Adult sounds
  and voice clips; Browsing the Gallery on the touch screen; How much the first adult build covers; Where the glasses
  are found; Who the hero's adult beats are with; The hero's gender in adult scenes; What opens an adult beat; Mission
  variants and story decision 11; Adult beats after Fallhaven; How the Adepts' adult scenes are shown; Mind Read on
  the townsfolk; Where the Giant Dildo Sword comes from; Who can wield the Giant Dildo Sword; The fan game's
  characters and scenes; The fan game's other parts; The curation lessons as rules; Packs without terms; Showing you
  adult assets for a yes; Revealing looks where LPC has no piece; Adult makers in the end credits.
- **Decided (you, 19 Oct), all as recommended:** the 28 open questions (among them: the Forest and Shadow Summon
  names Dryad, Silvanus, Cernunnos and Nyx, Erebus, Hecate; the cast's ages written into story.md; Gible in
  Dustplain; the seven backup items' names kept; the Log's entries written with each mission's script; the other
  starters after the demo; ordinary forms beside Weyard forms; legendaries' catch rate rising to 45 once calmed;
  finds joining at the area's level; Teleport at mission 19; the six group class lines through the demo; the
  partner numbers kept and retuned in slice 10; the proposed battle, gear and catch rules confirmed; catch-up at
  the join-level floor; no Z-Moves or Dynamax; 600 steps a clock phase; no random battles in the Vault's upper
  halls; four Forest and Shadow pieces of gear; 1x inside and 2x on the cover with a Large text row; a go-ahead
  for the LPC tileset download when the redraw starts; Weyard Mimikyu's Djinn costume; the Adepts and adult
  townsfolk in adult content, never Brann; the video converter when adult mode starts; the sprite strip held;
  for-the-story-chat.md renamed; **Tamsin joins with a mace**; **Cloak works by Golden Sun's rule**, unseen on
  dark cells). **Scripts approved:** the opening and missions 1 to 8 with their new canon and build changes.
  **Art approved:** the LPC cast and townsfolk, the poses plan, the foot shadow, the UI art, night backdrops only
  where it is night, our own Tab and Enter prompts.
- **New for your yes:** the drafts of missions 9 and 10 (design PR #78), their new canon and the Kestrel's fate
  (Scripts 15-18), and open questions 29-31 (Espeon and Umbreon, the cost of turning back after a lost story
  fight, friendship levels for five species).
- **The Fold's real screens, measured on your phone (demo decision 22):** the cover screen is 2520×1080 and the inner
  screen 2184×1968 (1080×2520 and 1968×2184 held upright), both at about 120 frames a second. They match the sizes the
  plan assumed, so the 480×320 picture draws at 3× on the cover (a 746×320 view, thin bars) and 4× inside (480×432).
  The readout came from the first diagnostics app (Gate 0); the new probe adds the look of the LPC people on the glass,
  which is optional now. The 480×320 switch (demo slice 2) is being built, landscape on both screens (art 2).

## 18 Oct 2026

- **Merged in the engine:** the LPC cast (PR #61: 8 Adepts and 20 townsfolk on adult and child bodies, the critic's
  fixes, the five poses, a foot shadow, credits for 33 LPC authors, a check that the game's sheets are current) and
  the art files (PR #63: the CC0 pipeline and picks, item icons by id only, Pokémon menu icons and the emote sprite).
  Nothing on screen changes until art part B wires them in with the 480×320 switch. Art approvals card 6 asks about
  the Tab and Enter prompts.
- **Art for your yes** (demo decision 21): a new **Art approvals** tab on the decision page with five cards: the LPC
  cast and 20 townsfolk looks with the art critic's fixes, the scripted poses, a foot shadow, the UI art, and night
  battle backgrounds. The pictures were sent in chat. Also merged in the engine: the Fold probe (PR #65) and the music
  tools (PR #66, agbplay and soundfile, with their review fixes).
- **The first scripts, for your yes** (demo decision 1): the opening and missions 1 and 2 written in full in
  [docs/story/scripts/](story/scripts/) (334 message-box pages, every line within the 3-line, 36-character budget, two
  reply beats a mission with quiet versions, the mission 1 eggs), checked by a second editor against story.md and
  your rules. A new **Scripts** tab carries one card per script plus their new canon and build changes.
- **Every question and decision on the decision page (your rule, 18 Oct: the cloud chat is archived and will
  no longer be used).** Two new tabs: **Open questions** ([open-questions.md](design/open-questions.md)), 26
  questions swept from every doc that were still left to the chat or open (Summon and class names, the cast's
  ages, the other starters, how legendaries join, the partner numbers, the rules still marked proposed, UI scale
  per screen, the LPC tile download, who appears in adult content, and more), each with a recommendation; and the
  **Decision log** ([decision-log.md](design/decision-log.md)), 100 decisions you made before or beside the page
  (12–18 Oct: DESIGN.md, the phase 1 answers, party and battle, the story Q&A and its 20 mechanics answers, and
  your rules in chat), each marked decided with its date. 33 lines across the docs that still said the story
  chat would decide or write something now point to the decision page.
- **Decided (you, 18 Oct): all 40 demo questions** ([demo-plan.md](design/demo-plan.md) §5), every one as recommended
  except the title screen (25), where you chose **the logo over a live scene, Stonehollow at dusk**. So: the engine
  side writes every mission's full script and posts it for your yes; the hero speaks short lines with two or three
  replies at about two beats a mission; a narrated, illustrated opening; the big beats staged in their rooms with
  stills for Celebi's vision and Sael's death; the rooms a beat happens in get built; 2–4 puzzles per dungeon with
  Blaze and Cloak; the mission 7/8 interludes start when Crew 1 next uses an inn or a sanctum; Fallhaven falls
  "soon after", at night; the Hive opens once Vesper is in the crew; all of Act I's eggs; four to six hand-written
  bounties; Mimikyu as a Djinn-style find; the Shiny Stone at mission 13; the starter trio and Marill kept; ordinary
  forms in the demo; Golden Sun's Summons for four groups, our own names on recolours for Forest and Shadow; our own
  Forest and Shadow class names; the islands of the week as rumours; free play after mission 10 and an end card at
  the Wayfarer's helm. Art: contact sheets for your yes before wiring; a Fold probe APK for you to run; illustrated
  art from an image generator, cleaned to our palette; 64-px portraits with three expressions; Golden Sun's ships
  and the surf mount; a sailable Calm and a parchment Chart; field sprites for Ho-Oh, Celebi and Mimikyu; the
  lead's partner follows; Essentials backdrops for the gaps; helms, shields, gloves and mail show on the sprite.
  Features: the Farer's Log found on the Wayfarer; the Kin Garden browser; the hero's house in Stonehollow; story
  fights tuned to 85% with Psynergy, 25% attack-only. Audio: Golden Sun's music for places and battles, Unbound's
  for Pokémon moments. A release-signed demo APK, two playtest rounds, one reviewer per PR.
- **Decided (you, 17–18 Oct), the last talk items, as recommended:** progression 3 (about L6–7 at mission 3, L8 at
  5, L10 at 10, through encounter tables and story-fight EXP), progression 4 (Stonehollow's west gate, and Canalport's
  lower-town exit, behind a story flag until our world map exists), equipment 8 (Golden Sun 1's item table for Act
  I; Golden Sun 2's later with a save migration). Nothing is left to talk over.
- **Go-ahead (you, 18 Oct) for the audio tools** (demo 36): an open-source GBA music renderer and an OGG encoder,
  from their official sources, checksum-checked, to render Golden Sun's and Unbound's own tracks offline (assets 1).
- **The demo plan** ([demo-plan.md](design/demo-plan.md)): what the Act I demo holds and how it ends, what is built
  and in flight, twelve build slices in order, which talk items still block it (progression 3, 4, equipment 8), and
  40 questions on the decision page's new Demo tab (the dialogue pass, the hero's voice, the opening, staging, rooms,
  puzzles, the mission 7/8 handovers, art approval, the Fold probe, portraits, the title, ships, the Calm, audio, the
  demo build and playtests). Found while planning: the mission 7 and 8 handovers start at the end of the recruitment
  scene, not at the next restoration point as story.md §14 Q1 says (decision 7).
- **Decided (you, 18 Oct): Ho-Oh stays special** (progression 20, from your note). At mission 4 Ho-Oh judges Crew 2
  in its fixed-length fight and flies off; the crew gains nothing legendary there. The top Flame Summon unlocks with
  the caldera catch after the Breaking. This replaces the Summon part of story decision 9; mission 4 changes in the
  next feature build.

## 17 Oct 2026, night (15 talk items answered)

- **Decided (you, 17 Oct), as recommended:** art 12 (hard-edged CC0 move effects now, Golden Sun's Psynergy
  effects later); equipment 14 (a Best button on Y with a yes/no check); items 1 (Golden Sun's coin scale: Poké
  Ball 30, Great 100, Ultra 300, specialty 250, Escape Rope 50, Repel 40, stones 1,200; Brann gives 5 balls with
  the first partner), items 7 (Poké, Great and Ultra in shops plus a rare Farer Ball that always catches), items 18
  (no bike, rod or Dowsing Machine), items 25 (Ho-Oh's classic catch after its fight, after the Breaking);
  progression 8 (Vesper on Mia's curve), 9 (no new Psynergy after L50), 12 (one growth factor for every partner),
  17 (Weyard species ids at the Weyard data pass, with a save migration), 18 (Ho-Oh filtered to damaging moves,
  then the fight re-measured).
- **Decided (you, 17 Oct), alternatives:** art 16, keep the Lost Age files in the APK for later content;
  art 17, research the uncredited LPC layers, and your note: use them even uncredited, the game being for personal
  use; equipment 13, armour layers show on the sprite too, not only weapons; progression 16, Gen 8/9 and regional
  evolutions allowed with mapped methods.
- **Your note on Ho-Oh** ("unlocked REALLY early") is now progression decision 20: Ho-Oh is only caught after
  the Breaking already; the question is whether the top Flame Summon should wait for that catch too.
- Still to talk over: progression 3 (target levels per mission), 4 (Stonehollow's west gate), equipment 8 (the
  item table).

## 17 Oct 2026, evening (more answers)

- **Decided (you, 17 Oct), all as recommended:**
  - **Progression 1, recruits' levels:** a join-level floor per mission in data (Corvin L7 at missions 2 and 4, L8 at
    7, L9 at 8), then every story fight re-measured.
  - **Progression 5, class tiers:** Golden Sun's 5-tier lines rising at Adept L1/10/20/30/40; each Set Pokémon of the
    Adept's group adds +1 elemental level (+5 Power and Resist); the late Psynergy unlocks with the tiers.
  - **Items 10, evolution items:** the 28 items used from the bag, the Linking Cord for every trade, the story routes
    in [items-and-economy.md](design/items-and-economy.md) §9; friendship and Eevee as progression.md §4 says.
  - **The clock 1–4** ([day-night-clock.md](design/day-night-clock.md)): night changes Kin habitats, the Lantern Reef
    decks and the battle backgrounds, never prices, stats or the encounter rate; no HUD, the pause screen names the
    phase; inns rest to dawn and bunks offer "Sleep until dusk/dawn"; scenes may set the phase, saved under a new save
    format version with a migration.
  - **Adult 23–24:** the Giant Dildo Sword matches the best weapon available at that point in the story; a forgotten
    code is cleared from the title's options after the 18+ gate again, which also turns the mode off.
  - **Art 18, tile redraws:** right after the demo, area by area, Stonehollow first, on the LPC base tilesets (the
    download waits for your go-ahead when that work starts), Essentials and our own drawing for gaps.

## 17 Oct 2026 (your answers on the story, adult mode and assets)

- **Decided (you, 17 Oct):** all 25 questions on the Story, Adult mode and Assets tabs, every one as recommended
  except the Kin clock, where you chose **a day/night clock now** (story 8; the clock's model is a new question,
  story 12). Among them: the Lodestar dormant until the Wayfarer and awake from mission 12; Brann gives it; Ho-Oh's
  mission-4 judgement becomes a fixed-length fight it ends itself; the Act I island shops; Canalport's flood; every
  character in adult content a canon adult; adult beats in side stories and heart quests only; the animation sets as
  the adult sprite base; the Essentials tiles into the tile spike (done, see the art probes); Pokémon menu icons and
  ball art from the expansion.
- **Your notes, now rules in [adult-mode.md](design/adult-mode.md):** an 18+ warning and age check on the glasses'
  first use; the game saves after every toggle; adult references and an easter egg at home from the moment the
  glasses are found; the gallery hunt's reward is coins and a charm *and* a scene; adult-only weapon and attack
  variants (read as reskins with the same numbers, decision 11); ideas and art may draw on the local folder. Adult
  mode itself still waits for the Act I demo.
- **New questions on the page (you asked for every open adult-mode question, 17 Oct):** adult-mode 11–22 (reskins or
  new gear, the age gate's form, what the toggle-save writes, the home easter egg, how explicit, generic townsfolk,
  how adult looks are drawn, toggling off mid-mission, picture credits, adult sounds, the glasses on the hero,
  rewards and the economy) and story 12 (the clock's model).
- **Assets:** anything in the local folder may be used where it is better for the story or in quality (your note on
  the music route).
- Decision marks on the pages now carry the date of the answer.
- **The clock (story 8):** a new page, [day-night-clock.md](design/day-night-clock.md), proposes the model (four
  phases by walking and rest, never the phone's time), what reads it (Lantern Reef's night decks, Kin habitats,
  time evolutions, night battle backgrounds) and the engine seams, with four questions on the decision page's new
  Clock tab. It is built after the bug-fix slices.
- **Decided (you, 17 Oct): adult mode 11–22 and the clock's model (story 12).** Reskinned adult gear plus one unique
  ultimate weapon of our own, the Giant Dildo Sword, from an adult side quest; a four-digit code after the 18+
  gate; a silent save after each toggle; all three home easter eggs; explicit text, pictures and videos (mini-games
  later); adult townsfolk on adult bodies, with Mind Read reading dirty thoughts; LPC revealing-outfit looks;
  missions pause when the mode goes off; makers credited in the Gallery; voice clips allowed; no glasses sprite;
  normal reward scale. The clock: four phases by walking and rest. New questions: adult 23 (the sword's power) and
  24 (a forgotten code). Details in [adult-mode.md](design/adult-mode.md) §5. Adult mode still waits for the demo.
- **Decided (you, 17 Oct, talked over in chat): the demo's art direction.** Art 3: every person is LPC, the 8
  Adepts first, then all 18 townsfolk looks together. Art 4: the adult body for the hero (your adult-mode answer 2)
  and for Corvin, so the rivals match. Art 8: Golden Sun's tiles stay at 2× for the demo, Essentials as a parts
  bin. Battle is all 2×. The art pass starts with the probe's fix list ([art-integration.md](design/art-integration.md) §3a).

## 17 Oct 2026 (demo first)

- **Decided (you, 17 Oct): the order of work.** A **playable Act I demo** (missions 1–10) **with great art** comes
  first: its art, engine and story finished. **Adult mode moves after it** ([adult-mode.md](design/adult-mode.md),
  decision 10); mission 11 too. The decompile and asset reviews keep running in the background until done.
- **Found for the demo:** the uploaded Pokémon Essentials fan game carries Essentials' Gen 4/5-style library already
  at our scale: 27 tilesets at 32 px with 48 autotiles, 219 human overworld sheets at 64×64 a frame, 200 battle
  backgrounds, windowskins, 48-px item icons, Pokémon menu icons and 1,524 sounds and tracks. It is a candidate for
  the open tile and character questions (art 3, 4 and 8) beside LPC, and goes into the Phase 2 probes. Only its
  non-adult files are considered; nothing from it enters git.
- **Art Phase 2 probes done (17 Oct):** the eight Adepts composed in LPC on two bodies, the Essentials library rendered
  from its map data, the same scene and a battle mocked three ways at 480×320, and a critic's comparison
  ([art-integration.md](design/art-integration.md) §3a). Recommendation: crisp LPC people in a Golden Sun world, battle
  all at 2×; Essentials as a parts bin. Decisions 3, 4 and 8 stay yours, with the probe notes on their cards.
- Built on Opus 5.5 and Fable 5.1.

## 16–17 Oct 2026 (your answers, adult mode, the Fable review)

- **Decided (you, 16 Oct, on the decision page):** 80 of the 104 open questions from the five reviews, every one as
  recommended; 24 are marked to talk over. The pages mark each item **Decided (16 Oct)** or **To talk over**.
- **Progression** ([progression.md](design/progression.md)): accepted 2 (A lost story fight), 6 (Level span), 7 (Gear), 10 (Physical moves), 11 (Learning moves), 13 (Evolutions beyond level), 14 (Branches), 15 (Several stages at once), 19 (Wild Pokémon EXP).
  - Still to talk over: 1 (Story recruits' levels), 3 (Target levels per mission), 4 (Stonehollow's west gate), 5 (Class tiers), 8 (Vesper's curve), 9 (Psynergy after L50), 12 (Partner pace), 16 (Gen 8/9 and regional evolutions), 17 (Weyard forms), 18 (Ho-Oh's wasted moves).
- **Art** ([art-integration.md](design/art-integration.md)): accepted 1 (The picture), 2 (Filling the Fold), 5 (The hero creator), 6 (Font), 7 (UI scale after the switch), 9 (Library art in git), 10 (Battle sprite scales), 11 (Battle backgrounds), 13 (Unleash and Pokémon on their feet), 14 (Icons, emotes, prompts, frames), 15 (Tamsin's look).
  - Still to talk over: 3 (LPC for Adepts and townsfolk), 4 (The boy hero's body), 8 (32-px tiles), 12 (Move effects), 16 (Shipping less), 17 (LPC eye credits).
- **Items and economy** ([items-and-economy.md](design/items-and-economy.md)): accepted 2 (Shops in Act I), 3 (Selling and artifacts), 4 (Act I income), 5 (Extra reward and wild drops), 6 (Catch EXP and where the catch goes), 8 (Held items), 9 (Permanent stat items), 11 (Mega trigger), 12 (TMs), 13 (Escape Rope and Repel), 14 (Key items pocket), 15 (Backup Psynergy items), 16 (PP for item Psynergy), 17 (Stack cap and pockets), 19 (Rest prices), 20 (Trainer rewards), 21 (Breakable gear, curses, the forge), 22 (Crew 2's balls before m10), 23 (Naming), 24 (Mini-game currency).
  - Still to talk over: 1 (Coin scale and ball prices), 7 (Ball roster), 10 (Evolution items), 18 (Bike, rod, Dowsing Machine), 25 (Ho-Oh's catch style).
- **Equipment** ([equipment.md](design/equipment.md)): accepted 1 (How gear is stored and changed), 2 (Who can wear what), 3 (The order stats are built in), 4 (Weapon Arts), 5 (The starting Machete's lock), 6 (Usable gear), 7 (Slots), 9 (Forest and Shadow gear), 10 (Gear across crews and guests), 11 (Recruit kits), 12 (Paying for eight Adepts), 15 (Enemy trainers' gear).
  - Still to talk over: 8 (Item table), 13 (Does gear show on the sprite?), 14 (A "Best" button).
- **Menus and navigation** ([menus-and-navigation.md](design/menus-and-navigation.md)): accepted 1 (Start menu), 2 (Pause), 3 (Freeze the world under the Start menu), 4 (Saves), 5 (Autosave timing), 6 (First Settings screen), 7 (Orientation), 8 (Back up saves off the phone), 9 (Battle menu shape), 10 (Running from battles), 11 (After losing a story fight), 12 (Partner tactics), 13 (Touch selects rows), 14 (Start inside a submenu), 15 (The Lodestar before mission 12), 16 (Pointing it at a marker), 17 (Default target with several open goals), 18 (Mini map), 19 (Danger stars and rumours), 20 (The area map's contents), 21 (Objective tracking), 22 (Log pages), 23 (DexNav's form), 24 (Landmarks on a small screen), 25 (Where Lantern Reef sits), 26 (L/R shortcuts), 27 (Fast travel), 28 (Pronouns at the mirror).
- **Requested (you, 16 Oct): adult mode.** An optional Key Item, the Adult-o-Vision glasses, switches an adult mode on
  and off at any time; it opens alternate sprites, story points, dialogue, easter eggs and a collection side mission
  with a hidden gallery; adult scenes between consenting adults only. Mechanics proposed in
  [adult-mode.md](design/adult-mode.md); the content rules (people only, canon adults only, consent on the page, off by
  default, nothing required behind it) are written there.
- **Decided (you, 16 Oct): the story chat is archived.** Story questions now go to the decision page too; the engine
  side updates story.md from the answers. [story-questions.md](story/story-questions.md) carries them.
- **Decided (you, 16 Oct): the local folder's materials may be used,** with or without licence terms, with your
  approval per item where needed, and every maker tracked for an end-credits scroll:
  [credits.md](engine/resources/credits.md).
- **Published:** [needed-assets-2026-10-16.md](engine/resources/needed-assets-2026-10-16.md) (what art and sound the
  game still needs, where each comes from) and the audit of the 16 Oct uploads
  ([local-folder-audit-2026-10-16.md](engine/resources/local-folder-audit-2026-10-16.md)).
- **The Fable review of the Opus work began.** The design-doc pass found 13 wording and status problems, all fixed
  here: the catching rules in party-and-battle.md §5 and §8 now agree and carry the 16 Oct decision; the pre-16-Oct
  battle model is gone from §10, §12 and the paste table; DESIGN.md's header table has rows for the 15–16 Oct
  decisions; field-abilities.md and docs/engine/README.md say what is built; the Farer's Log has four decided sections.
  The engine pass over the bonded-partner PRs found six defects (one medium: a field hazard at full HP strips the
  partner's HP share); they go to the bug-fix build. The rest of the engine review is running.
- Earlier, 16 Oct: design PR #45 corrected the codec's item type and flag labels and the oracle's unleash clamp;
  design PR #46 added the story-chat questions page.
- **Decided (you, 17 Oct): adult mode has its own missions.** Adult-themed side missions, missions that exist only
  in the mode, and mode-exclusive variants of main missions; a variant changes scenes and lines, never unlocks.
  [adult-mode.md](design/adult-mode.md) §1 and §3, with four new decisions.
- **17 Oct:** engine PR #56 (the APK pipeline: `builds/` and `tests/` leave the APK, 62.7 → 52.9 MB) merged after its
  reviewer ran all three new tools clean. The uploaded Pokémon Essentials fan game was decompiled read-only
  (scripts to text, maps to JSON, every graphic and sound catalogued) for the adult-mode asset curation; two
  Pokémon-involving scene sets are excluded under the rules.
- Built on Fable 5.1 from here.

## 16 Oct 2026 (progression audit and the art-integration plan)

- **Proposed, built: the waiting crew earns half** of each won battle, as in GS2. Its level-ups and evolutions are
  told in one line each after the battle ("Meanwhile, with Corvin:"). Engine PR #50.
- **Fixed:**
  - The Pokémon exporter keeps evolution conditions; before, Riolu → Lucario read "level 0".
  - Wynn's Ralts line (and 7 other species) gets its real Fairy type.
  - Colour forms and Mothim export.
  - A bonded Adept no longer loses its partner's HP share when it levels up.
  - Gifts take the species table's name.

  Engine PRs #51 and #52.
- **Proposed: evolution conditions the game has no system for are ignored** (gender, time, weather, "not in region",
  personality and Attack/Defense splits; the first branch wins for now). Friendship, known moves, held items, places
  and regions hold an evolution back until their rules exist.
- **Published: [progression.md](design/progression.md).** It answers whether levelling, power scaling and evolution
  hold up end to end.
  - The code holds, but the story's EXP leaves Act I at about L5–6 against fights tuned at L7.
  - A lost story fight restarts forever.
  - Classes and gear never improve.
  - The content ends at L43.

  It lists 19 decisions for you.
- **Published: [art-integration.md](design/art-integration.md).** It plans how the new libraries and 64-px art come
  in without re-authoring rooms, saves or checks. Phase 1, seams and bug fixes with no decision needed, is being
  built. It lists 17 decisions for you.
- **Published: [items-and-economy.md](design/items-and-economy.md).** It answers what every item does, key and
  action items, buffs, drops, shops, selling, coins, catching, and evolution and Mega items.
  - One coin scale (Golden Sun's), so balls get re-priced: Poké Ball 30.
  - Golden Sun items for Adepts.
  - Our own items only where Pokémon or the story need them.
  - No bike, rod or held items.

  It lists 15 bugs (item Psynergy can never fire, battle items hit your own side, rests charge full-health
  Adepts...) and 25 decisions for you. Its evolution routes follow progression.md (Maren's Shiny Stone, Riolu at
  20, Wynn's Dawn Stone, Vesper's Linking Cord).
- **Published: [equipment.md](design/equipment.md).** It covers how weapons, armour and other gear work and their
  screens.
  - Today nothing can change gear, and only Attack, Defense and the weapon element apply.
  - Proposed: Golden Sun's rules (stat order, equipped effects, Weapon Arts, curses, usable gear) and an Equip
    screen with a before-and-after preview.
  - Proposed: per-Adept equip profiles, recruit kits with weapons, and no held items for Pokémon.

  It lists 15 decisions; questions the items page already asks aren't repeated.
- **Published: [menus-and-navigation.md](design/menus-and-navigation.md).** It covers menus, pause, settings, saves,
  maps and the compass.
  - Proposed: a Golden Sun Start menu that freezes the world, a pause box elsewhere, and Android Back that never
    quits.
  - Proposed: a Settings screen saved on the phone, and 3 save files with safe writes and autosave.
  - Proposed: no always-on minimap in rooms, an area map on a button, a Chart for the sea, and an objective line.
  - The Lodestar is kept as decided: world map and sea only, full use from mission 12.

  It lists 18 bugs, including the battle menu hiding half its commands, unsafe save writes, and the world running
  under menus. It also lists 28 decisions.
- **Doc fixes:**
  - party-and-battle.md §1 now says bags are per crew until mission 10, as decided.
  - items-and-economy.md §11 now records "worn gear can't be sold" as our change; Golden Sun refuses only locked
    gear.
- Built on Opus 5.5; marked for the Fable review.

## 16 Oct 2026 (bonded partners)

- **Decided (you, 16 Oct): partners are bonded to their Adepts.** The active Pokémon stops being a separate fighter
  and stands behind its Adept. It gives the Adept a share of its stats (a boost that levels with it), its moves
  join the Adept's menu, and it **shields its Adept from one hit** per battle. The **revive window and Rouse stay**.
  Battles have up to 4 fighters a side, one stat system. `party-and-battle.md` §2, §3 and §5 record it.
- **Decided: all three Set Pokémon of a standing Adept earn EXP**, benched ones included, so they grow toward
  evolution and swapping partners over time pays.
- **Proposed numbers (to tune in play):** a 30% stat share; a fifth of a move's PP as uses per battle; partners on
  the Adepts' EXP table scaled by growth rate, so they keep pace with their Adept instead of reaching 100 by Adept
  level 49.
- **Built:** level evolutions (others wait for their rules); Rouse's group bonus now applies; enemy trainers mirror
  the bond. Engine PR #49.
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

## 15 Oct 2026 (mission 10, Act I complete)

- **Mission 10 is playable end to end** (engine PR #48): the refugees settle in Stonehollow, the two Earth leads
  open the Vault's inner door, the Wayfarer is found, the crews' bags merge and **crew swapping unlocks**.
  `docs/design/mission-10-build.md` has the flow, the swapping rules as built, the words and the placeholders.
- **Crew logistics built** (`party-and-battle.md` §1): the other crew waits on Marrow Isle; swap at its lead,
  where the player stands; trade Adepts with their Set Pokémon at the lead or the muster roll (leads never move, four
  per crew); innkeepers away from home offer the trip home (relay stones don't).
- **Fixed placeholders:** Corvin walked as the default hero's sprite; he is Felix now (masked in mission 1). Ilse
  and the Kestrel's mates wore a small dog's sprite.
- **Act I is complete.** Mission 11 (the Breaking) is next.
- The Fable review of the Opus work was started, then paused until 16 Oct. Built on Opus 5.5; marked for review.

## 15 Oct 2026 (art scale and the asset audit)

- **Decided (you, 15 Oct): Adept sprites at 64×64 pixels if possible, 32×32 if not**, and other art at that scale
  where it can be. This replaces Golden Sun's small field sprites in the graphics pass; nothing changes yet.
- **Proposed with it:** 32-pixel tiles and an internal picture of about 480×320, so the field shows a similar area.
- **Answered: 128-pixel Adepts?** Draw at 64 and show bigger where wanted. LPC is drawn at 64, our Pokémon pictures
  are 64×64, and the libraries stop at about 64, so 128 would double pixels or mix pixel sizes, at four times the
  art cost. 128 and up pays for portraits, Summons, bosses and title art.
- **Asset audit** (`docs/engine/resources/asset-audit-2026-10-15.md`): `2d-assets` (1,101 CC0 packs), the CC0
  sprite library (76 packs) and the LPC generator (88,114 layer sheets), inventoried by the engine's new
  `tools/inventory_assets.py`. Picks: LPC for Adepts, Kenney Pixel for the dialogue font, Dungeon Crawl icons,
  Pixel-boy battle backgrounds, CC0 effect sheets for Pokémon moves, Kenney emotes and UI. Gaps: 32-pixel tiles,
  portraits, audio.
- Mission work paused after mission 9 for this audit, as asked. Done on Opus 5.5; marked for review on Fable.

## 15 Oct 2026 (mission 9)

- **Mission 9 is playable end to end** (engine PR #46) with both crews: the hero's crew evacuates Fallhaven's lower
  town (Move, Growth, Reveal) while Corvin's crew holds the archive (Mind Read, Whirlwind); the Ledger of the Crown
  is read, Sael holds the doors, Maren confesses, Ilse escorts the boats, and both crews land at Stonehollow.
  `docs/design/mission-9-build.md` has the flow, the words and the placeholders.
- **Relay stones (proposed):** a restoration point inside a two-crew dungeon. It offers rest and Set Pokémon like an
  innkeeper, and switching to the other crew where it stands.
- **Open point for the cloud chat:** the story has Fallhaven fall "the night after" the Forest seal was deepened
  (mission 5), but mission 9 needs both crews full, so it plays after mission 8.
- **Fixed:** Sael wore a small animal's sprite in mission 2.
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

## 15 Oct 2026 (mission 8)

- **Mission 8 is playable end to end** (engine PR #45): after crew 1's second recruitment, the story hands over to
  Corvin's crew at the Tradewind Bazaar; Wynn joins with Ralts, Mind Read takes the strongbox code from the purser,
  Whirlwind swings a sail into a bridge, the strongbox gives up Wynn's note and chart, and the chart shows the
  Crown under the Pinnacle. Both crews are full. `docs/design/mission-8-build.md` has the flow, the words and the
  placeholders.
- **Whirlwind and Mind Read** work in the field as Sky Psynergy, refused until a Sky Adept is in the active crew.
- **Fixed:** a gate's repaint tiles that the map never drew came out invisible; the engine now creates them first.
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

## 15 Oct 2026 (mission 7)

- **Mission 7 is playable end to end** (engine PR #44): after crew 1's first recruitment, the story hands over to
  Corvin's crew at Bastion Rock; Scoop digs a tunnel under the walls, a guard's line of sight sends the crew back to
  the tunnel, the key ring opens Nerissa's cell, she joins with Froakie, and the crew Surfs out to the open Calm.
  `docs/design/mission-7-build.md` has the flow, the words and the placeholders.
- **Scoop** is in the field-ability table as Earth Psynergy (party-and-battle.md §7 already listed it for both
  crews), so both Earth leads can dig.
- **Guards** see in a straight line along their heading, blocked by walls; seen, the room's "caught" scene plays.
  Vision cones and Cloak can come later.
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

## 15 Oct 2026 (mission 6)

- **Mission 6 is playable end to end** (engine PR #43): Vesper pilots for fifty coins and joins with Gastly,
  Lantern Reef's broken wreck has Reveal planks, a Halt boom, fog that Defog clears, and Corvin's note ("Ask your
  Commodore where the tithe goes"), which unlocks Defog. Easter eggs: Mimikyu, Maestro Bonewhistle, a Litwick
  lantern. `docs/design/mission-6-build.md` has the flow, the words and the placeholders.
- **Crew 1 is complete** once missions 5 and 6 are done: the hero, Maren, Sorrel and Vesper (Earth, Sea, Forest,
  Shadow), which is what the story's later puzzles assume.
- **Not built yet:** night-only decks (there is no day and night).
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

## 15 Oct 2026 (mission 5, Act I begins)

- **Mission 5 is playable end to end** (engine PR #42): the Kestrel's chart sails to the Greenwild, Sorrel joins
  with Rowlet, Growth binds the rotten bridge, the poison swamp stings, Celebi's vision plays at the great tree's
  heart, the Forest seal is driven deeper on Ilse's order, and Cut unlocks. `docs/design/mission-5-build.md` has
  the flow, the words and the placeholders.
- **The Kestrel's chart** (proposed placeholder): until the sea map of the Calm exists, a deckhand at each port
  lists the places the story has opened and sails there.
- **Hazards** (poison swamps) cost HP per step, never below 1. **Cut** and the other kept HMs need their story
  unlock as well as a Set Pokémon that can learn them.
- **Open point for the cloud chat:** the story's Hive (mission 5's easter egg) is solved with Cloak and Reveal,
  which only arrive with Vesper in mission 6, while missions 5 and 6 can be played in either order. It isn't built
  yet; it could be an optional Greenwild area to return to.
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

## 15 Oct 2026 (mission 4)

- **Mission 4 is playable end to end** (engine PR #41): the handover to Corvin's crew after the sluice beast, the
  Forgeheart's Earth trial, Tamsin's fight and her joining with Riolu, the Flame seal, Ho-Oh's judgment, the fire
  and the escape, and the return to the hero's crew in Canalport. `docs/design/mission-4-build.md` has the flow,
  the words, the measured balance and the placeholders.
- **Top Summons wait for their legendary** (following story §5: "calming one unlocks its group's top Summon at
  once"). Each group's highest tier is locked until then; lower tiers are always available. Calming Ho-Oh unlocks
  Mars's top Summon.
- **Legendary judges** are story fights against a single Pokémon with the story's numbers (Ho-Oh: 420 HP, two
  actions a round, proposed).
- Built on Opus 5.5 while Fable 5.1 was rate-limited; marked for review on Fable.

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
