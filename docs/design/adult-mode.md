# Adult mode: the Adult-o-Vision glasses

**Requested by you, 16 Oct.** This page proposes the mechanics. Which story points, lines, scenes and hidden
pictures exist is the story chat's to write (docs/story/story.md); the engine builds only what's recorded here and
there. Everything below is **proposed** unless marked **your rule**.

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
  written down (the story chat sets ages). A character written as younger is excluded from all of it, lines
  included. The hero counts too: the LPC "teen" body is an art body type, not an age; if the hero appears in adult
  content, the hero is an adult in canon, and the adult body type is the safer art choice (art decision 4).
- **Consent is on the page.** A scene shows both people choosing it; nothing is written as coercion, payment for
  rescue, or a captor's leverage. The story chat holds this line when it writes the beats.
- **Off by default, and nothing required is behind it.** No main mission, recruit, area, reward or completion item
  needs adult mode. Its own missions are side content; a mode-exclusive variant of a mission changes the scenes and
  lines, never the unlocks, so the normal version stays complete. Turning it off hides everything again at once.
- **No effect on play.** Adult mode never changes battles, stats, prices, encounters or the clock.

## 2. The item

| Rule | Proposed |
|---|---|
| Id and pocket | 9410 in the key-items range (items-and-economy.md §4), named "Adult-o-Vision", flag 8, shown in the Key Items pocket. It can't be sold, dropped or lost |
| Where it comes from | The story chat's call. Default: an optional find in Act I that the player can pass by, so the choice is theirs from early on. [Sold at the Tradewind Bazaar (m8); a bounty reward; a gift from a side character] |
| Toggling | Key Items → the glasses → Use. A short toast: "Adult-o-Vision: on" / "off". No settings row and no button: the glasses are the switch |
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
- **The side mission.** Collect all N pictures for a reward the story chat names. Progress shows in the Gallery and,
  while the mode is on, as a line on the Farer's Log Bearings page. It counts toward no visible completion % when
  the mode is off.
- **Save.** Flags only (`adult_mode`, `gallery:<id>`), so the save format doesn't change.

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

1. **Where the glasses are found.** Recommended: an optional Act I find the player can skip. [Bazaar stock; a bounty
   reward; a gift.]
2. **The hero's canon age and body.** Recommended: an adult, drawn with the adult body (this settles art decision 4
   for the boy hero). [Keep the teen body and keep the hero out of adult scenes.]
3. **The side mission's reward.** The story chat's call; a mechanics default is coins plus a charm.
4. **Toggle persistence.** Recommended: saved with the game. [Off again every time the game starts.]
5. **Easter eggs and completion.** Recommended: adult-only finds count in a hidden % shown only while the mode is on.
   [Count nowhere; count in the Log's normal %.]
6. **Adult looks in battle too, or field only.** Recommended: both, through the same cast variant. [Field only.]
7. **How many adult-only missions in Act I.** Recommended: the gallery hunt plus one side mission per recruited
   Adept (a heart quest with an adult beat), so seven, written after the main missions' variants. [The gallery hunt
   only; a fixed three.]
8. **Which main missions get a variant.** Recommended: only missions whose scenes involve an approved adult character
   and no Pokémon beat, starting with missions 3, 5 and 6 (Maren, Sorrel and Vesper join there). [Every mission;
   none, side missions only.]
9. **Who writes them.** The story chat is archived. Recommended: the engine side drafts each mission's outline and
   lines as a mission page for your approval on the decision page, then builds it. [You write the outlines in
   story.md first.]
10. **Where adult missions and variants sit in the order of work.** Recommended: after the Act I demo (missions
    1–10) is complete with its art, engine and story (your words, 17 Oct). [Before mission 11, as soon as the first
    adult assets land; after Act II.]
