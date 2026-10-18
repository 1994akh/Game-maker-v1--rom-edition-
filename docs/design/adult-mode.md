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
