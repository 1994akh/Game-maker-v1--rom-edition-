# Adult mode: the Adult-o-Vision glasses

**Requested by you, 16 Oct.** This page proposes the mechanics. Which story points, lines, scenes and hidden
pictures exist, the engine side drafts as mission pages for your yes on the decision page (decision 9); the
engine builds only what's recorded here and in docs/story/story.md. Everything below is **proposed** unless
marked **your rule**.

**Order of work (your rule, 17 Oct):** adult mode is built **after the Act I demo** (missions 1–10) is complete with
its art, engine and story. Until then this page, the asset curation and the decompile tooling wait; nothing here is
built, and the demo carries no adult content.

## 1. Rules

**Your rules (16–17 Oct):**
- An optional item, the **Adult-o-Vision glasses**, switches adult mode on and off at any time.
- Adult mode opens what is otherwise hidden: alternate sprites, story points, dialogue, easter eggs, and a side
  mission that collects pop-up art from hidden books, magazines and other places, viewed in a hidden menu.
- **Adult mode has its own missions (17 Oct):** adult-themed side missions, missions that exist only in the mode, and
  mode-exclusive variants of missions.
- Adult scenes are between **consenting adults only**.

**Proposed rules that follow from those:**
- **People only.** No Pokémon or other creature appears in any adult content. Pokémon stay what they are everywhere
  else in the game.
- **Canon adults only.** Every character who appears in adult content is an adult in the cast list, with the age
  written down (in story.md §4, story decision 10). A character written as younger is excluded from all of it, lines
  included. The hero counts too: the LPC "teen" body is an art body type, not an age; if the hero appears in adult
  content, the hero is an adult in canon, and the adult body type is the safer art choice (art decision 4).
- **Consent is on the page.** A scene shows both people choosing it; nothing is written as coercion, payment for
  rescue, or a captor's leverage. The engine side holds this line when it drafts the beats.
- **Off by default, and nothing required is behind it.** No main mission, recruit, area, reward or completion item
  needs adult mode. Its own missions are side content; a mode-exclusive variant of a mission changes the scenes and
  lines, never the unlocks, so the normal version stays complete. Turning it off hides everything again at once.
- **No effect on play.** Adult mode never changes battles, stats, prices, encounters or the clock. The one
  exception you asked for is a unique ultimate weapon (decision 11; its power is decision 23).

## 2. The item

| Rule | Proposed |
|---|---|
| Id and pocket | 9410 in the key-items range (items-and-economy.md §4), named "Adult-o-Vision", flag 8, shown in the Key Items pocket. It can't be sold, dropped or lost |
| Where it comes from | Decided 17 Oct (decision 1): an optional find in Act I that the player can pass by, so the choice is theirs from early on. [Sold at the Tradewind Bazaar (m8); a bounty reward; a gift from a side character] |
| Toggling | Key Items → the glasses → Use. A short toast: "Adult-o-Vision: on" / "off". No settings row and no button: the glasses are the switch. **Your rules (17 Oct):** the first use shows an 18+ content warning and an age check the player must confirm before the mode can turn on (decision 12), and **the game saves after every toggle** (decision 13) |
| What it sets | The permanent flag `adult_mode`, saved with the game. A new game starts with it clear |
| When it takes effect | At once for the next dialogue page, the next room load and the next menu open. A scene already running finishes as it started |

## 3. What it gates

All of it uses what the engine already has.

- **Dialogue, actors and scenes.** Actor rows, dialogue branches and scene steps carry the existing conditions:
  `{show: "while_set", flag: "adult_mode"}` for adult-only content and `while_clear` for the version shown
  otherwise. An adult-only NPC, book or poster simply isn't there when the mode is off.
- **Sprites.** `data_src/cast.json` looks get an optional `adult` variant. The cast resolver (engine PR #55) returns
  that look while the flag is set, for the field and for battle. Variants are drawn to the 64×64 standard like
  every other look (art scale 2).
- **Story points and easter eggs.** Scene steps gated with `when`; a scene may branch on the flag. The list of
  adult-only beats is a decision on the decision page (the story chat is archived), so the engine knows what to
  build per mission.
- **From the moment the glasses are found (your rule, 17 Oct):** adult references, lines and variants begin at once, including an easter egg in the player's home, so the toggle shows something immediately (decision 14).
- **Adult-only gear and attacks (your rule, 17 Oct):** adult variants of weapons and attacks exist in the mode. **Proposed reading:** reskins (names, looks, attack lines and effects) of items and moves with the same numbers, so "no effect on play" holds and the normal run stays complete (decision 11).
- **Adult-only missions and variants (your rule, 17 Oct).** Three shapes, all on the existing mission tooling
  (`maps_src/<room>/events.json`, flags, `FieldScript` steps, `tools/missionN_check.gd`):
  - **Side missions** that only exist while the mode is on: their quest-givers, rooms' extra actors and rewards carry
    `while_set adult_mode`. They are optional, hang off the home island and the recruited Adepts' heart quests, and
    reward gallery entries, adult looks, charms or coins. The gallery hunt (§3 above) is the first of them.
  - **Mode-exclusive missions**: the same, but with their own rooms or room variants and a mission page in
    `docs/design/` like the main ones. Flags `am_<n>_done` keep them apart from the main `m<n>_done` chain.
  - **Mode-exclusive variants of main missions**: the same mission with adult scenes, lines and looks swapped in
    through `when` branches and `adult` looks. The variant sets the same flags and gives the same unlocks as the
    normal run, so a player who toggles the mode mid-game is never stuck or short.
  - Each mission's two versions are checked by the same `missionN_check`, run with the flag clear and set.
- **Pop-up art.** A new actor role `gallery`: a hidden book, magazine, painting or the like. With the mode on,
  interacting shows the picture full screen (a `Popup` screen: fit to the view, A or B closes) and sets the flag
  `gallery:<id>`. With the mode off, the object shows a plain line ("A dusty book.") or is absent, per its row.
  Pop-up art is shown at its own resolution scaled to fit, never pixel-doubled: it's the one place, with portraits,
  where higher resolution pays.
- **The gallery menu.** A **Gallery** entry in the Start menu that exists only while the mode is on
  (menus-and-navigation.md §3). It lists collected pictures as "n of N", opens one on A, and shows an uncollected
  one as a locked slot with the area's name as a hint.
- **The side mission.** Collect all N pictures for a reward: coins and a charm, and a scene
  (decision 3). Progress shows in the Gallery and,
  while the mode is on, as a line on the Farer's Log Bearings page. It counts toward no visible completion % when
  the mode is off.
- **Save.** Flags only (`adult_mode`, `gallery:<id>`), so the save format doesn't change.


### Your answers to decisions 11–22 (17 Oct)

- **Gear (11):** adult variants of weapons and attacks are reskins with the same numbers, **plus one unique ultimate
  weapon of our own design, the Giant Dildo Sword**, unlocked at the end of one adult side quest and usable from then
  on. Its power is question 23.
- **Age gate (12):** the first use shows the 18+ warning and the age confirmation, then the player sets a four-digit
  code; every later turn-on asks for the code. A wrong code leaves the mode off. Forgetting the code is question 24.
- **Saving (13):** the toggle writes the game's save silently with a short "Saved" after the on/off toast; the glasses
  can't be used where saving is blocked (mid-battle, mid-scene).
- **Home (14):** all three: a magazine under the hero's bed (the gallery's first picture, which teaches the Gallery
  menu), a bedroom poster that changes with the mode, and a line from Keeper Brann, who shares the house.
  **Proposed:** Brann's line is a dry, embarrassed joke about the find; Brann is the hero's guardian, so it is never
  flirtation or anything sexual between them.
- **Explicitness (15):** explicit text and pictures within the §1 rules, and **videos too** (your note); mini-games
  are for a later version. **Proposed:** videos from the local folder are converted offline to Ogg Theora (the format
  Godot plays) and shown in the same pop-up and Gallery, with the same curation and credits as pictures.
- **Townsfolk (16):** generic townsfolk may carry adult variants and lines, on adult bodies only, never a child body.
  Your note: at the least, with the mode on **Mind Read on a townsperson reads a dirty thought**, and some thoughts
  add a picture or video to the Gallery or an alternate line.
- **Looks (17):** the Adepts' adult looks are revealing-outfit variants composed from the same LPC layers.
- **Toggling off mid-mission (18):** the mission pauses, its actors and markers vanish and its flags keep.
- **Credits (19):** the Gallery shows a picture's maker under it when the source credits one.
- **Sound (20):** stingers and loops in adult scenes, and **voice clips from the pack too**, all gated by the flag.
- **The glasses (21):** no sprite change; the looks and the toast show the switch.
- **Rewards (22):** the same coin and charm scale as normal side missions.

### Your answers to decisions 25–51 (19 Oct)

All as recommended except five alternatives:
- **One APK (25):** everything goes in the one APK, adult content included; its size is question 55.
- **The quarters night (40):** mission 10's quarters talks get an optional adult version, after the demo is built;
  how many per night is question 56.
- **The Giant Dildo Sword (44):** any Adept can wield it, the one exception to the weapon table.
- **The fan game's rows (45):** you review the rows with no age either way on a private sheet and keep only those
  that clearly show adults with consent (question 52; the sheets are in `OneDrive\Apps-Roms\_adult-review`).
- **The fan game's other parts (46):** copied into the game's third-party folder now (question 57 asks about
  converting them).
- **Review sheets 1-3 (52-54, 19 Oct late):** you viewed them and approved every number as showing adults over 18:
  the fan game's 12 rows with no stated age, the five loose uploads and the pixel animation set's 22 clips. Their
  proposed uses are listed beside them in the private review folder (`approved.csv`); sheets 4-8 and the fan
  game's adult sounds follow as questions 58-63.
- **Review sheets 4-8 and the sounds (58-63, 19 Oct night):** all approved, every number, and you confirmed in chat
  that every picture in the review folder is approved: the smooth animation set, both sets' faces, the small
  sprite pack, the character and scene cards (reference only), the fan game's portrait busts (style references)
  and its 16 adult sounds. 160 approved items are listed in the folder's `approved.csv`; the draft Gallery plan is
  question 64.

## 4. Assets

- **Where they live.** `assets/adult/` in the engine repo, gitignored like the ROM content, with a committed manifest
  (`data_src/gallery.json`: id, title, area, file; `data_src/adult_looks.json`: cast id → sheet). The pictures never
  reach GitHub; the design repo is public and holds only this page.
- **Sizes.** Sprites and animations to the 64×64 standard (converted where they aren't); pop-up art kept at its
  size.
- **Sound.** The game has no audio code yet. The sound pack you added becomes part of the audio pass
  ([needed-assets-2026-10-16.md](../engine/resources/needed-assets-2026-10-16.md) §4), with adult-only sounds gated by
  the same flag.
- **What you added on 16 Oct** is inventoried in the local-folder audit of that date (names, counts and sizes
  only).
- **Curation is yours.** The engine never picks which picture goes where; the manifest does, and only assets that
  meet the rules in §1 go into it.

## 5. Decisions for you

Answered on the decision page: accepted items are marked **Decided** with the date, the rest **To talk over**.

1. **Decided (17 Oct):** **Where the glasses are found.** Recommended: an optional Act I find the player can skip. [Bazaar stock; a bounty
   reward; a gift.]
2. **Decided (17 Oct):** **The hero's canon age and body.** Recommended: an adult, drawn with the adult body (this settles art decision 4
   for the boy hero). [Keep the teen body and keep the hero out of adult scenes.]
3. **Decided (17 Oct):** **The side mission's reward.** To be named with the story beats; a mechanics default is
   coins plus a charm. [An adult scene as the reward.] Your note: both, and adult-only weapon variations and attacks
   (decision 11).
4. **Decided (17 Oct):** **Toggle persistence.** Recommended: saved with the game. [Off again every time the game starts.]
5. **Decided (17 Oct):** **Easter eggs and completion.** Recommended: adult-only finds count in a hidden % shown only while the mode is on.
   [Count nowhere; count in the Log's normal %.]
6. **Decided (17 Oct):** **Adult looks in battle too, or field only.** Recommended: both, through the same cast variant. [Field only.]
7. **Decided (17 Oct):** **How many adult-only missions in Act I.** Recommended: the gallery hunt plus one side mission per recruited
   Adept (a heart quest with an adult beat), so seven, written after the main missions' variants. [The gallery hunt
   only; a fixed three.]
8. **Decided (17 Oct):** **Which main missions get a variant.** Recommended: only missions whose scenes involve an approved adult character
   and no Pokémon beat, starting with missions 3, 5 and 6 (Maren, Sorrel and Vesper join there). [Every mission;
   none, side missions only.]
9. **Decided (17 Oct):** **Who writes them.** The story chat is archived. Recommended: the engine side drafts each mission's outline and
   lines as a mission page for your approval on the decision page, then builds it. [You write the outlines in
   story.md first.]
10. **Decided (17 Oct):** **Where adult missions and variants sit in the order of work.** Recommended: after the Act I demo (missions
    1–10) is complete with its art, engine and story (your words, 17 Oct). [Before mission 11, as soon as the first
    adult assets land; after Act II.]

**Open questions (17 Oct)**

11. **Decided (17 Oct):** **Adult-only weapon and attack variants: reskins or new gear?** Your note on decision 3 asks for them.
    Recommended: reskins, so an adult name, look, attack line and effect animation on items and moves that keep their
    numbers, and the §1 "no effect on play" rule holds. [New items and moves with their own stats, balanced with the
    equipment work; reskins plus a few mode-only accessories with no combat effect.]
12. **Decided (17 Oct), alternative:** **The age gate's form.** Your rule: an 18+ content warning and an age check before the mode can turn on.
    Recommended: once per save file, on the glasses' first use: the warning page, then "I confirm I am 18 or older"
    with No as the default; a new game asks again. [Ask every time the mode is turned on; a four-digit code the
    player sets on first use, needed for every turn-on.]
13. **Decided (17 Oct):** **What "save after every toggle" writes.** Recommended: the toggle writes the game's save silently, the way the
    game saves today, with a short "Saved" after the on/off toast; the glasses can't be used where saving is blocked
    (mid-battle, mid-scene). [A separate autosave file so the player's own save is untouched; a save prompt instead
    of a silent write.]
14. **Decided (17 Oct), alternative:** **The easter egg at home.** Your rule: one in the player's home from the moment the glasses are found.
    Recommended: a magazine hidden under the hero's bed that is the gallery's first picture and teaches the Gallery
    menu, with a plain "Old magazines." line while the mode is off. [A poster on the bedroom wall that changes with
    the mode; a line from whoever shares the house; all of these.]
15. **Decided (17 Oct):** **How explicit.** Your note on decision 9: "raunchy lust is the idea". Recommended: explicit text and pictures
    within the §1 rules (people only, canon adults, consent on the page); a scene cuts to black only where no art
    exists for it. [Suggestive text and art only; explicit text with suggestive art.]
16. **Decided (17 Oct), alternative:** **Who else can appear: the generic townsfolk.** Recommended: only the Adepts and named NPCs with written ages
    (story decision 10); the 18 generic townsfolk looks never carry adult variants or lines. [Generic adult townsfolk
    too, on a stated-adult body, for background flavour.]
17. **Decided (17 Oct):** **How the adult looks are drawn.** Recommended: for the Adepts, a revealing-outfit variant composed from the same
    LPC layers (same body, same palette) so the mode matches the demo's art; the 16 Oct animation sets and the fan
    game's sheets serve scenes and pop-up art rather than the walking cast. [Fan-game or animation-set sheets as the
    walking variants regardless of style match; no walking variants, scenes and pictures only.]
18. **Decided (17 Oct):** **Toggling off in the middle of an adult mission.** Recommended: the mission pauses, its actors and markers
    vanish and its flags keep, so it resumes where it was when the mode comes back; a scene already running finishes
    as it started (§2). [Toggling off abandons and resets the adult mission; the toggle is refused while an adult
    mission is active.]
19. **Decided (17 Oct):** **Picture credits in the gallery.** Every maker goes in the end-credits scroll (your rule, 16 Oct).
    Recommended: the Gallery also shows the maker's name under a picture when the source's credits give one.
    [Credits scroll only.]
20. **Decided (17 Oct), alternative:** **Adult sounds.** The SFX pack you added (assets decision 1). Recommended: short stingers and ambient loops in
    adult scenes only, gated by the flag; no voice clips. [Voice clips from the pack too; no adult-only sound.]
21. **Decided (17 Oct):** **The glasses on the hero.** Recommended: no sprite change for the glasses themselves; the adult looks are the
    visible change and the toast confirms the switch. [A glasses overlay on the hero's field sprite while the mode is
    on.]
22. **Decided (17 Oct):** **Adult-mission rewards and the economy.** Recommended: the same coin and charm scale as normal side missions, so
    a player with the mode on is never richer or stronger (§1); gallery entries and adult looks are the mode's own
    rewards. [Richer rewards as an incentive for the mode.]
23. **Decided (17 Oct):** **The Giant Dildo Sword's power.** Recommended: an ultimate weapon in look and moves (its own unleash, attack
    line and effect), with numbers equal to the best weapon available at that point in the story, so a player
    without the mode is never weaker. [Genuinely stronger, the one exception to "no effect on play"; the strongest
    weapon in the game, unlocked late.]
24. **Decided (17 Oct):** **A forgotten code.** Recommended: the title screen's options can clear the code after the 18+ warning and the
    age confirmation again, which also turns the mode off. [No recovery: a new game; the code can be changed only
    while the mode is on.]

**The build and the phone (19 Oct)**

25. **Decided (19 Oct), alternative:** **How adult content reaches the phone.** The pictures, sounds and videos live in the gitignored assets/adult/
    folder, and the debug APK is already about 53 MB, past the 30 MB a file can be sent to you in chat (from
    adult-mode.md §4 and the probe builds). Recommended: one game APK without them, plus a separate adult pack file
    you copy to the phone once; the game loads it at start and the glasses work only when it is there, so no build
    that gets sent around carries adult content. [Everything in the one APK; two APKs, a normal one and an adult one.]
26. **Decided (19 Oct):** **Hiding the game from the recent-apps view.** Android keeps a picture of the last screen in its recent-apps list,
    and screenshots and screen recordings catch whatever is shown. Android can mark a window secure, which in Godot
    needs a small Android plugin (from adult-mode.md §2). Recommended: while the mode is on, the game's window is
    marked secure, so the recent-apps card is blank and screenshots come out black; with the mode off everything works
    as now, so you can still send me screenshots. [Never: screenshots always work; a Settings row that you switch
    yourself.]
27. **Decided (19 Oct):** **One code for the phone, or one per save file.** The game has three save files, and adult 12 and 24 don't say
    whether the four-digit code and the 18+ confirmation belong to a save file or to the phone (from adult-mode.md §3
    and menus-and-navigation.md §1). Recommended: one code and one confirmation for the phone, kept with the Settings
    and outside any save, so all three save files share them and the title screen can clear them (adult 24); each save
    file keeps its own on or off. [A code per save file, set on each file's first use; one code for the phone that
    turns the mode on or off for every save file at once.]
28. **Decided (19 Oct):** **Wrong codes.** Adult 12 says a wrong code leaves the mode off, but not what happens after many wrong tries (from
    adult-mode.md §3). Recommended: no lockout: each wrong code shows "Wrong code." and leaves the mode off, and the
    pad shows the digits as dots. [After three wrong tries in a row the glasses rest for five minutes; after five
    wrong tries the code must be cleared from the title screen.]

**Screens and safety (19 Oct)**

29. **Decided (19 Oct):** **The 18+ warning's words.** Adult 12 decided the warning, the age check and the code, but not the text (from
    adult-mode.md §3). Recommended: one short page: "Adult-o-Vision shows sexual content between adults: nudity,
    explicit scenes and sounds. It is for players 18 or older." Then "I confirm I am 18 or older" with No as the
    default, and nothing adult shown before both. [A longer page that lists every kind of content; your own words,
    written in the note box.]
30. **Decided (19 Oct):** **Leaving the game quickly.** A phone game gets interrupted: a call, the home button, someone walking in. The
    planned pause box offers Resume, Settings and Return to title (from adult-mode.md §2 and menus-and-navigation.md
    §1). Recommended: while the mode is on, the pause box covers the whole screen whenever it opens or the game goes
    to the background, so nothing adult shows behind it; no separate panic button. [A quick-hide gesture, such as a
    three-finger tap, that also turns the mode off; nothing extra.]
31. **Decided (19 Oct):** **The cover screen.** The Fold's cover screen is the one used folded, often in public (from art-integration.md
    §3b). Recommended: the mode shows the same on both screens: it is your switch. [Pictures and videos open only on
    the inner screen, and folded the Gallery asks you to unfold; the mode turns itself off when you fold the phone.]
32. **Decided (19 Oct):** **Adult sounds and voice clips.** Adult 20 adds stingers, loops and voice clips; Settings plans music, effects and
    voice volumes (from adult-mode.md §3 and menus-and-navigation.md §6). Recommended: an "Adult sounds" volume row
    that appears only while the mode is on, starting at the effects volume, so they can be turned down without muting
    the rest. [They follow the effects and voice volumes; voice clips play only through headphones and stay silent on
    the speaker.]
33. **Decided (19 Oct):** **Browsing the Gallery on the touch screen.** The Gallery lists pictures as "n of N" and opens one on A; videos
    show in the same pop-up (from adult-mode.md §3). Recommended: swipe left and right for the next and previous,
    pinch to zoom a picture, tap a video to pause it, and B closes; the pad and buttons work too. [The pad and buttons
    only; the swipes plus a seek bar on videos.]

**The story and the cast (19 Oct)**

34. **Decided (19 Oct):** **How much the first adult build covers.** Adult mode is built after the demo (adult 10). Act I's adult missions
    are the gallery hunt and a heart quest with an adult beat for each recruited Adept (adult 7), but the Gallery's
    size isn't set (from adult-mode.md §3 and §5). Recommended: the first adult build covers Act I's places and every
    Adept's quest, with about 30 Gallery finds, three for each mission's places; each later act adds its own finds and
    beats as it is built. [About 12 finds, with the quests; all of the game's adult content at once, after Act III.]
35. **Decided (19 Oct):** **Where the glasses are found.** Adult 1 makes them an optional Act I find the player can pass by, without naming
    the place (from adult-mode.md §2). Recommended: a hidden spot in Stonehollow, the home village, there from mission
    1 on and still there in free play, so a save from the demo can find them, close to the home eggs of adult 14. [The
    Tradewind Bazaar's back rooms in mission 8; aboard the Wayfarer in free play after the demo.]
36. **Decided (19 Oct):** **Who the hero's adult beats are with.** Adult 7 gives each recruited Adept a heart quest with an adult beat,
    while story.md's heart quests are friendships that decide each ending (from adult-mode.md §5 and story.md §11).
    Recommended: the player may follow any of the heart quests, as many as they like; no partner is exclusive, nobody
    is jealous, and each beat is between the hero and that Adept. [One partner per playthrough, chosen at a set point
    in Act I; the hero's beats, plus some between two Adepts where their scripts support it.]
37. **Decided (19 Oct):** **The hero's gender in adult scenes.** The hero is a boy or a girl, chosen at the start, with pronouns chosen
    apart; drawing for both bodies doubles the scene art (from character-creator.md). Recommended: every Adept's adult
    beat works with either hero: the lines use the pronoun tokens and the art is drawn for both bodies. [Each Adept
    has a stated preference, and only the beats with a hero they'd choose play; the beats are written for one hero
    body only, which you name.]
38. **Decided (19 Oct):** **What opens an adult beat.** The asset curation's lessons suggest a bond with a threshold and a yes on the page,
    with no effect on battles or prices (from the curation lessons). Recommended: no meter: each beat opens at a set
    step of that Adept's heart quest, and every scene first asks both people; "Not now" ends it with an ordinary line
    and no penalty, and it can be asked again later. [A bond meter for each Adept, raised by talks and gifts and shown
    in the Log; the same bond meter, kept hidden.]
39. **Decided (19 Oct):** **Mission variants and story decision 11.** Story decision 11 puts adult scenes in side stories and heart quests,
    never a main mission, while your rule of 17 Oct (decision log 75) and adult 8 give missions 3, 5 and 6 variants in
    the mode (from story decision 11 and adult-mode.md §3 and §5). Recommended: a variant may add optional adult lines
    and scenes beside a main mission's path, such as a night at the inn, but never changes a required scene, so
    nothing required touches the mode. [Variants may replace a main mission's own scenes; no variants: story decision
    11 wins.]
40. **Decided (19 Oct), alternative:** **Adult beats after Fallhaven.** Mission 9 ends with Sael's death, and mission 10's night in the quarters is a
    toast to her and seven quiet talks that seed the heart quests (from the mission 9 and 10 drafts). Recommended: no
    adult beat in missions 9 and 10; the first heart-quest beats open at the first rest aboard the Wayfarer in free
    play after the demo. [An optional adult version of the quarters talks in mission 10; nothing until after mission
    11.]
41. **Decided (19 Oct):** **How the Adepts' adult scenes are shown.** The 16 Oct animation sets show generic figures, not our cast, and the
    LPC people are small sprites; adult 15 cuts to black only where no art exists (from adult-mode.md §3 and §4 and
    needed-assets decision 2). Recommended: sprite scenes in the engine, built from the pixel animation set on adult
    bodies only and recoloured to each Adept's hair, skin and palette at the 64×64 standard, with the text carrying
    the rest; the packs' own pictures and videos stay Gallery finds that don't stand for our cast. [A painted still
    for each scene, from an artist you commission; text over the scene's room, cutting to black.]
42. **Decided (19 Oct):** **Mind Read on the townsfolk.** With the mode on, Mind Read on a townsperson reads a dirty thought, and some
    thoughts add a Gallery find (decision log 78), but not who writes how many (from adult-mode.md §3). Recommended: a
    pool of thoughts for each townsfolk look, picked at random, plus written thoughts for named people once you
    approve them (open question 23); one thought in each place adds a Gallery find, and Brann's thoughts never change.
    [A written thought for every townsperson; thoughts for a few chosen townsfolk, the rest read as normal.]
43. **Decided (19 Oct):** **Where the Giant Dildo Sword comes from.** Adult 11 unlocks it at the end of one adult side quest without naming
    which (from adult-mode.md §3 and decision log 76). Recommended: the gallery hunt's final reward, beside its coins,
    charm and scene (adult 3), so it marks finishing the mode's biggest quest. [A quest of its own from a smith at the
    Tradewind Bazaar; the end of the hero and Corvin's heart quest.]
44. **Decided (19 Oct), alternative:** **Who can wield the Giant Dildo Sword.** Long swords go only to the hero and Corvin; the other Adepts' class lines
    use light blades, maces and staffs (from equipment.md). Recommended: it is a long sword, so the hero and Corvin.
    [Any Adept, as the one exception to the weapon table; the hero only.]

**Assets and curation (19 Oct)**

45. **Decided (19 Oct), alternative:** **The fan game's characters and scenes.** The 17 Oct asset curation found no character there with a stated age and
    no scene set that passes the §1 rules; rows written as younger or failing a rule are out and are never shown (from
    the private curation sheet, kept out of the repo). Recommended: approve none of them; the 16 Oct animation sets
    and the sound pack stay the adult base. [A private contact sheet of the few rows with no age either way, and you
    tick only those that clearly show adults with consent, adding an age to each first.]
46. **Decided (19 Oct), alternative:** **The fan game's other parts.** Its tiles, audio, windows, battle backgrounds, icons and follower sprites hold no
    adult content. Since the curation, the Kenney UI, the CC0 art and music rendered from the ROMs were chosen (from
    the curation sheet and art approvals 4). Recommended: keep them outside git as a parts bin and take a piece only
    when a screen has a gap the chosen art doesn't fill, each one credited. [Copy them all into the game's third-party
    folder now; leave them out.]
47. **Decided (19 Oct):** **The curation lessons as rules.** The curation drew twelve lessons for this page. Among them: a check that the
    adult_mode and gallery flags are read only by dialogue, looks and menus, so the mode can't change play; an age
    field on every cast row, with the build refusing an adult entry whose people lack an age of 18 or more or that
    includes a Pokémon; and adult text kept in separate files (from the curation lessons). Recommended: add all twelve
    to §1 and §3 as proposed rules, with the age field and both checks built in the first adult slice. [Add only the
    two checks; keep the lessons on the private sheet.]
48. **Decided (19 Oct):** **Packs without terms.** The two animation sets and the small sprite pack came with no licence file, so their
    makers are unknown (from credits.md). Recommended: one web search for each pack's name before the adult build, to
    find its maker and terms; if nothing turns up, use it in this personal build and credit it as "maker unknown".
    [Hold them until a maker is found; use them now, with no search.]
49. **Decided (19 Oct):** **Showing you adult assets for a yes.** Every art step gets your yes (demo 21), but adult pictures can't go on the
    public repo or this decision page (from art-approvals.md §1 and adult-mode.md §4). Recommended: numbered contact
    sheets made by a saved script into a review folder beside your uploads (`OneDrive\Apps-Roms\_adult-review`), for
    you to open on the computer or the phone; you answer here by number only. [You look in the source folders yourself
    and write the file names in the note box; the same contact sheets kept on the computer only, outside OneDrive.]
50. **Decided (19 Oct):** **Revealing looks where LPC has no piece.** Adult 17 composes the Adepts' adult looks from the same LPC layers,
    but the library may lack a piece a look needs (from adult-mode.md §3). Recommended: draw the missing layer
    ourselves in LPC's style and palette, credited to this project. [Use the nearest LPC piece; leave that Adept's
    adult look unchanged until a piece exists.]
51. **Decided (19 Oct):** **Adult makers in the end credits.** Every maker goes in the end-credits scroll (your rule, 16 Oct), and the
    Gallery shows a picture's maker under it (adult 19) (from credits.md and adult-mode.md §3). Recommended: an
    "Adult-o-Vision" section at the end of the scroll, shown only while the mode is on; credits.md lists them always.
    [Always in the main scroll; only in credits.md and the Gallery.]

**Review sheets: pictures for your yes (19 Oct)**

52. **Decided (19 Oct), alternative:** **Review sheet 1: the fan game's rows with no stated age.** Your choice on adult 45. The sheet is
    review-sheet-1.png in `OneDrive\Apps-Roms\_adult-review` (adult 49), with a README: 12 numbers, a ranch character,
    a milkmaid dance, milk pumps, four trainer classes' field and battle sprites, and an unplaced animation sheet.
    Left out by the rules and not shown: the fan game's protagonist (written as younger), its rival (the protagonist's
    peer, so out too, a change from the curation sheet), every scene with a Pokémon and every scene where consent
    fails. Recommended: keep none. [Keep the numbers I write in the note box, each clearly an adult, with an age I
    give each person.]
53. **Decided (19 Oct):** **Review sheet 2: the sprite strip and four loose uploads.** review-sheet-2.png in the same folder: number 1 is
    the 3000×628 sprite strip held by open question 25, and numbers 2 to 5 are four pictures that arrived the same
    evening, 16 Oct, and were never inventoried. Recommended: keep the numbers you write in the note box, each with
    what it is for (a Gallery find, a look or a scene) and only if every person in it is clearly an adult; the rest
    stay out. [Keep none of them.]
54. **Decided (19 Oct):** **Review sheet 3: the pixel animation set.** review-sheet-3.png in the same folder shows one middle frame of each
    of the set's 22 clips. Adult 41 builds the Adepts' adult scenes from this set, recoloured to each Adept on adult
    bodies only, so this is the check that its figures are adults. Recommended: approve the set as the base for the
    Adepts' scenes, if every figure is clearly an adult. [Approve all but the numbers in the note box; find another
    set.]

**Follow-ups to your answers (19 Oct)**

55. **Decided (19 Oct):** **The one APK's size.** Your choice on adult 25 puts everything in the one APK. With the Gallery's videos inside,
    it could pass several hundred MB; it installs from OneDrive as now and can't be sent in chat (from adult 25 and
    adult 15). Recommended: videos converted to 720p at a moderate bitrate and pictures kept at their own size, aiming
    for an APK under 1 GB. [Full source quality, whatever the size; 480p videos, aiming under 300 MB.]
56. **Decided (19 Oct):** **The quarters night in adult mode.** Your choice on adult 40: an optional adult version of mission 10's quarters
    talks. The night follows supper and the toast to Sael, and each talk seeds that Adept's heart quest (from the
    mission 10 script). Recommended: each of the seven talks can turn adult when the Adept and the hero both choose
    it, written as comfort after the loss, and choosing one ends the night with that Adept, so one per night; the
    supper and the toast stay as written. [Any number of talks may turn adult that night.]
57. **Decided (19 Oct):** **Copying the fan game's other parts.** Your choice on adult 46 copies its tiles, audio, windows, battle
    backgrounds, icons and follower sprites into the game's third-party folder now. The curation's extraction plan
    also converts them (tiles re-cut, autotiles baked, sprites padded to 64, MIDI rendered, audio re-encoded) (from
    the curation sheet §5). Recommended: copy them now as they are, with the exclusion list and a manifest, and
    convert each part only when a screen uses it. [Copy and convert everything now.]

**More review sheets (19 Oct)**

58. **Decided (19 Oct):** **Review sheet 4: the smooth animation set.** In `OneDrive\Apps-Roms\_adult-review\sheets`, with the README: one
    middle frame of each of the 21 clips of the full-size animation set, the same clips as sheet 3's pixel set.
    Proposed use: stills and pop-up art for the Gallery (adult 15). Recommended: keep every number that clearly shows
    adults, writing any you leave out in the note box. [Keep none of them; keep only the numbers I write in the note
    box.]
59. **Decided (19 Oct):** **Review sheet 5: the expression frames.** 18 faces: numbers 1-9 from the smooth set and 10-18 from the pixel set,
    whose faces sheet 3 didn't show. Proposed use: faces for the scene portraits. Recommended: keep every number that
    clearly shows adults, writing any you leave out in the note box. [Keep none of them; keep only the numbers I write
    in the note box.]
60. **Decided (19 Oct):** **Review sheet 6: the small sprite pack.** 21 strips of 48-pixel frames from the small pack, a character and an
    NPC, shown enlarged; its Aseprite source lets them be redrawn at 64. Proposed use: extra scene poses and
    townsfolk. Recommended: keep every number that clearly shows adults, writing any you leave out in the note box.
    [Keep none of them; keep only the numbers I write in the note box.]
61. **Decided (19 Oct):** **Review sheet 7: the character and scene cards.** 26 cards' own pictures: two character cards and 24 studio scene
    cards, approved on 16 Oct as reference only. The files also carry their game's data, which this game won't use.
    Recommended: keep them as references for drawing our own art, every number that clearly shows adults. [Keep none
    of them; use the numbers I write in the note box as Gallery finds too.]
62. **Decided (19 Oct):** **Review sheet 8: the fan game's portrait busts.** 19 busts: the professor's four (an adult by role; her one scene
    stays out because it has a Pokémon) and 15 of six characters with no stated age, never in its scenes. Proposed
    use: style references for our own portraits, not in the game as they are. Recommended: keep them as style
    references, every number that clearly shows an adult. [Keep none of them; use the numbers I write in the note box
    in the game as they are.]
63. **Decided (19 Oct):** **The fan game's adult sounds.** 16 sounds copied to the review folder's audio subfolder for listening: breaths,
    wet sounds, a kiss, a spank and one ambient loop; one ambient loop with a creature stays out. Adult 20 already
    keeps voice clips and loops from the Kentaro pack. Recommended: keep the ones you like beside the Kentaro pack,
    writing any you leave out in the note box. [Keep none: the Kentaro pack is enough.]

**The Gallery plan (19 Oct)**

64. **Decided (19 Oct):** **The draft Gallery plan.** gallery_plan.csv in the private review folder lists the 33 approved pictures meant as
    Gallery finds: the four loose uploads first, then the fan game's pictures, then the smooth set's stills. 30 are
    placed three to each of the demo's ten places (adult 34), the first being the magazine under the hero's bed (adult
    14), and three wait for later acts. Each find's hiding spot is chosen when its room's adult content is built.
    Recommended: approve the draft, with any moves you want written in the note box (find number and place). [Place
    them yourself in the file; leave the places until each room's adult content is built.]

**From the visual survey (1 Nov)**

65. **Decided (1 Nov):** **Bella's two music themes in the parts bin.** The fan game's copy holds two music tracks named for Bella (her
    theme and her battle theme). They are music, not pictures of her, but your rule excludes Bella. Recommended: drop
    both, so nothing of Bella's is in the game. [Keep them as ordinary music the game may use under other names; keep
    them in the parts bin but never use them.]
66. **Decided (1 Nov):** **Fan-game people as adult townsfolk and trainer art.** Review sheet 1's approved rows propose four of the fan
    game's people sprites as adult townsfolk walking looks and four as adult-mode trainer art. Their frames are 64 px
    like LPC's, but they are drawn in Pokémon Essentials' style, and art 3 makes every person in the game LPC. Beside
    the LPC townsfolk they would look out of place. Recommended: use them only as Gallery finds and drawing
    references, with the adult townsfolk looks made as LPC variants of today's townsfolk (adult 17's method). [Redraw
    them on LPC bodies as new adult-only townsfolk; use them as they are and accept the style mismatch.]
67. **Decided (1 Nov):** **How the Adepts' scenes use the pixel animation set.** Adult 41 builds the Adepts' scenes from the pixel set
    (sheet 3), recoloured to each Adept at the 64x64 standard. Its figures are about 220 px tall, roughly four times
    an LPC person in a 64 frame, so shrinking them loses the drawing. Their outline and palette also differ from
    LPC's. Recommended: show each scene as a close-up panel over the dimmed room at the set's own size, recoloured to
    the Adept's hair, skin and outfit colours, with the field sprites staying LPC. [Redraw every pose at 64 in LPC
    style (the largest art job); shrink the frames to 64 and accept the lost detail.]
68. **Decided (1 Nov):** **Scaling the pixel-art pop-ups.** Adult-mode.md §3 says pop-up art is scaled to fit, never pixel-doubled. Several
    approved finds are pixel art with 96- and 144-px frames (sheet 2). Smooth scaling to the inner screen (2184x1968)
    or the cover (2520x1080) will blur them. Recommended: pixel-art finds scale by the largest whole number that fits
    and stay sharp, and the smooth set's stills scale to fit with smoothing. [Everything scales to fit with smoothing,
    as written; everything scales by whole numbers only.]
69. **Decided (1 Nov):** **Videos: none exist in the local folder.** Adult 15 and 55 plan videos converted to 720p Ogg Theora, but the
    local folder holds no video file. The two animation sets are frame sequences. Recommended: play the animation
    sets' frame sequences as looping animated pop-ups, and convert real videos only if you add some later. [You will
    add video files to the local folder for the adult build; drop videos and keep still pictures only.]
70. **Decided (1 Nov):** **Gallery finds on Nightmarket Isle.** The draft Gallery plan places 30 finds, three in each demo place, and holds
    3 for later acts. Nightmarket Isle, the adult-only town decided on 24 Oct after that plan, has none. Recommended:
    move the three later-act finds to Nightmarket Isle: one on the quay, one in the inn, one in the shop. [Move three
    from the demo places instead; give Nightmarket Isle its own new finds when its rooms are built.]
71. **Decided (1 Nov):** **Nightmarket Isle's marker on the map and the Chart.** With the mode on, the island shows today as a hot-pink
    debug square. It stands out on the cover screen in public, and adult 31 keeps the mode the same on both screens.
    Recommended: a discreet marker: the same town icon as any other place, in the UI's own colours, with only its
    name. [A distinct icon or colour that marks it as the adult town; no marker at all, with Vesper sailing there from
    a helm line only.]
72. **Decided (1 Nov):** **Art for Nightmarket Isle's rooms.** The rooms nightmarket (quay and market), nightmarket_inn and
    nightmarket_shop are planned as 'later'. Golden Sun has no night-market tileset. The art rules use Golden Sun's
    room tiles at 2x, with generated art only where Golden Sun has nothing (open 91 and 102). Recommended: Golden Sun
    town and harbour tiles at 2x with a night tint, plus lanterns and lashed boats drawn in code to Golden Sun's
    palette. [Generated art throughout for a look of its own; tiles from the fan game's parts bin.]
73. **Decided (1 Nov), alternative:** **Brann's line about the home find.** Adult 14 (your choice, 17 Oct) gives the home three finds: the magazine
    under the bed, a poster that changes with the mode, and an embarrassed, non-sexual line from Keeper Brann. Your
    rule is 'never Brann'. Recommended: Brann has no adult-mode line at all, and the magazine and the poster stay.
    [Keep his one embarrassed, non-sexual line, as decided in adult 14.]
74. **Decided (1 Nov):** **Which named people may carry adult looks or thoughts.** Adult 16 allows generic adult townsfolk on adult bodies,
    and adult 42 adds Mind Read thoughts. The townsfolk looks include two children, Brann (tf_keeper) and Maestro
    Bonewhistle (a skeleton with no age). Named adults with written ages are Commodore Ilse (47), Hask (39), Captain
    Sael (52, Corvin's foster mother, who dies in mission 9) and Vey (58, the villain). Gary Rivalson has no written
    age. Recommended: adult looks and thoughts for the 13 generic adult townsfolk kinds, Mind Read thoughts only (no
    looks or scenes) for Ilse and Hask, and nothing for Sael, Vey, Gary, Bonewhistle, Brann or the children, with a
    build check that refuses them. [Every named adult with a written age except Brann; generic townsfolk only, with no
    named person.]
75. **Decided (1 Nov):** **The glasses' Key Items icon.** Adult 21 keeps the hero's sprite unchanged, but item 9410 still needs an icon in
    the Key Items pocket. The pocket can be seen on the cover screen. Recommended: plain round glasses drawn in code
    to the item-art style, with nothing adult about the look. [Reuse the fan game's Reveal Glass key-item icon from
    the parts bin; a distinct design, such as tinted lenses.]
76. **Decided (1 Nov):** **A safe way to survey adult screens.** Adult 26 blanks screenshots while the mode is on, adult pictures stay off
    every repo, and Claude doesn't look at explicit images. That leaves no way to check adult screens for layout, size
    or seam faults the way today's survey checked the rest of the game. Recommended: a debug-only survey switch that
    swaps every adult picture, video and look for numbered grey cards and lifts the secure window, so the screens can
    be checked, while you review the real art yourself on the private contact sheets. [You check adult screens
    yourself on the phone and note faults by number; screenshots of the real screens, saved only to the private folder
    for you.]
77. **Decided (1 Nov):** **Pokémon and creatures during adult scenes.** Your rule is nothing sexual with Pokémon or creatures. Rooms hold
    Pokémon and creature actors (for example Mimikyu, the Sluice Beast and the lantern Litwick), and partners are
    bonded to the Adepts. Recommended: the scene runner hides every Pokémon and creature actor in the room, partners
    included, while an adult scene or pop-up plays, Mind Read on a Pokémon never gives an adult thought, and the adult
    build check enforces both. [Only keep them out of the scene's frame; handle it scene by scene when each one is
    written.]
78. **Decided (1 Nov):** **Sheet 2's long sprite strip: a find or a look.** Review sheet 2's number 1 (the 3000x628 sprite strip) was
    approved as 'your call: a look or an animated Gallery find'. The draft Gallery plan counts it as a find, which is
    why adult 64 says four loose uploads but the plan has five. Recommended: an animated Gallery find, since it isn't
    LPC and can't sit as a walking look. [A look, redrawn on LPC bodies; reference only.]
