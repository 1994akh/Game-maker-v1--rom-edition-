# For the story chat: questions from the engine side (16 Oct)

The design reviews of 16 Oct turned up a few things that belong to the story, not to mechanics. Story decisions
live in the claude.ai design chat and land in [story.md](story.md), so the engine side lists them here instead of
editing story.md. Each comes with a suggested answer; take it, change it, or ignore it. Mechanics questions from the
same reviews are on the decision page and in `docs/design/` (progression, art-integration, items-and-economy,
equipment, menus-and-navigation).

## Conflicts inside story.md

1. **When the Lodestar first works.** story.md §6 says "the Lodestar offers story bearings" in Act I. §7 and §10
   say mission 12 is its first full use. The Wayfarer's cradle text says it "points nowhere yet" (mission 10).
   - **Suggested:** in Act I it is a Key Item with no needle, and the Kestrel's chart marks the story destination.
     It stirs in its cradle on the Wayfarer at mission 10 and is fully awake from mission 12.
   - Reword §6 to match (menus-and-navigation.md §8.5).
2. **Who gives the Lodestar.** story.md mission 1 calls it Brann's heirloom. The build has Commodore Ilse hand it
   over at the end of mission 1.
   - **Suggested:** Brann gives it at the hatchery with the first partner, and Ilse's deputising stays as it is. Or
     keep Ilse and drop "Brann's heirloom".
3. **Where Lantern Reef sits.** The world sketch puts it west of Meridia; mission 6 says the north Calm.
   - **Suggested:** north-west of Meridia, which fits both. The Chart needs one position.
4. **Torro's "The Wrong Way" side story** relies on the Lodestar inside a room. The decided navigation UI (Q10) shows
   it only on the world map and at sea.
   - **Suggested:** give the beat a scripted bearing shown in that room, or rewrite it around the Chart.

## Places to fill in

5. **Backup Psynergy items.** DESIGN.md has left their placement open since 12 Oct. Please add an "Items" column to
   §7's mission list placing these, so the engine can put them in the right rooms:
   - Carry, Hover, Grind and Sand (item-only verbs);
   - the backups for each crew's missing verbs (Growth, Reveal at mission 20, Lash, Catch, Cloak, Halt; Blaze,
     Parch, Force, Burst, Whirlwind, Mind Read, Cyclone, Teleport);
   - the Waterfall, Rock Climb and Whirlpool unlocks.

   items-and-economy.md §6 lists them with suggested sources.
6. **Story partners' evolution items.** These need a mission, bounty or gift each:
   - Maren's Shiny Stone (Eevee → Sylveon), suggested as a gift in her arc;
   - Wynn's Dawn Stone (Kirlia → Gallade, the player's choice);
   - Vesper's Linking Cord (Haunter → Gengar).

   Tamsin's Riolu evolves at level 20, so it needs nothing (progression.md §4, items-and-economy.md §9).
7. **Shops on the Act I islands.** Dustplain, Frostmarch, Hushwater and Twin Bells each need a stock line or "no
   shop" that fits their culture.
   - Hushwater fears Pokémon and treats Psynergy healing as taboo, which suggests herbs but no balls.
   - Proposed shops elsewhere: items-and-economy.md §11.
8. **Canalport after the Breaking.** Its lower town floods at mission 11.
   - **Suggested:** its shops move to the upper town, and the drowned lower town becomes Dive loot.
9. **Kin habitats.** The Farer's Log Kin entries mention "time of day", but the game has no clock.
   - **Suggested:** drop time of day from habitats until a day/night cycle is decided (a mechanics question).

## Kept as the story decided

These are noted so the story chat knows the engine side didn't change them:
- Ho-Oh is fought and then caught classically. A Farer Ball or a calmed catch-rate floor makes that possible.
- Groudon rests in the Vault and is caught in the postgame.
- Legendaries join at the level of the area where they're caught (Q9), and a mid-game legendary can't be the
  active partner until Act III.
