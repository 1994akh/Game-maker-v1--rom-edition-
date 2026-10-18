# Decisions made outside the page

## 1. What this is

The decision page holds the questions asked on it and your answers. Many decisions came before it or beside it:
DESIGN.md's component decisions (12 Oct), the phase 1 answers and the party and battle rules (13 Oct), the story Q&A
and its 20 mechanics questions in the cloud chat (14 Oct, story.md §13 and §14), and the rules you gave in chat that
docs/CHANGELOG.md records as "your decision" or "Decided (you, ...)". The cloud chat is archived, so this tab logs
each of them as an already-decided item and the decision page shows every decision. Each item carries the date of the
CHANGELOG entry, what was asked, what you decided and, in brackets, what it replaced or the other options. A later
decision says which earlier one it replaces, and an item a later answer on another tab changed names that answer.
Decisions already asked on the other tabs are not repeated here.

## 2. Decisions for you

Every item here is decided: the decision is under "Recommended", and the brackets hold what it replaced or the other
options.

Answered on the decision page: accepted items are marked **Decided** with the date, the rest **To talk over**.
**Platform and engine**

1. **Decided (12 Oct):** **A GBA ROM hack.** What kind of game this is, in DESIGN.md's first component decisions.
   Replaced on 13 Oct. Recommended: a GBA ROM hack taking from Golden Sun, The Lost Age and Pokémon Unbound, played on
   the Fold 7, on a Pokémon code base still to be chosen and with FireRed's assets as placeholders. [A native Android
   app, chosen on 13 Oct.]
2. **Decided (12 Oct):** **Free 8-way movement.** How the hero walks, the largest single job on a tile-grid engine.
   Recommended: Golden Sun's free 8-way movement, sized in phase 1 against 8-direction walking on the grid as the
   fallback. [Pokémon's 4-way grid walking.]
3. **Decided (13 Oct):** **Native Android app first.** Phase 1 asked which edition comes first. This replaces the GBA
   ROM hack. Recommended: a native Android app for the Galaxy Z Fold 7 first, so the GBA's limits (a 32 MB ROM, about
   116 bytes free in the save block) no longer drive the design. [The ROM edition first, on pokeemerald-expansion's
   FireRed target, as phase 1 recommended.]
4. **Decided (13 Oct):** **The code base.** Phase 1 recommended forking pokeemerald-expansion now. Recommended: on
   hold until the Golden Sun extraction is done, with the expansion kept as a candidate beside engines built for
   native Android. [Fork pokeemerald-expansion now; CFRU, as Unbound was built; pret's pokefirered.]
5. **Decided (13 Oct):** **Free movement straight away.** Phase 1 recommended grid-diagonal walking first, with free
   movement as a later mode. Recommended: go straight to free 8-way movement, the natural default on a native engine,
   with Golden Sun's walk and run speeds measured as the targets. [Grid-diagonal walking first, as phase 1
   recommended.]
6. **Decided (13 Oct):** **Where the engine code lives.** Phase 1 asked whether the code shares this repo.
   Recommended: a new private repo under your GitHub (later named GameMaker-Engine), with this repo keeping the design
   docs. [One repo for the design and the code.]
7. **Decided (14 Oct):** **The engine.** Three routes were argued and judged, then libGDX and Unity were tried as
   challengers. This replaces the code base on hold. Recommended: Godot 4.7.2 with typed GDScript, "for now": the best
   score of the three routes (46), with 6–8 weeks to a playable slice. [Native C on pokeemerald-expansion with an SDL3
   Android layer (35); extending goldensun_html5 in a WebView (32); libGDX; Unity 6.6.]

**Party and battle**

8. **Decided (12 Oct):** **Adept elements.** What an Adept's element is and what it does. Recommended: each Adept
   belongs to one of the six site groups (Earth, Flame, Sea, Sky, Forest, Shadow), with two Earth Adepts (the hero and
   a rival, a nod to Isaac and Felix) and two Sea; the element decides the Adept's Psynergy, and Set Pokémon that
   match it give a bonus. [Golden Sun's four elements.]
9. **Decided (12 Oct):** **Pokémon in the Djinn role.** How the Pokémon fit Golden Sun's party. Recommended: three
   Pokémon Set on each Adept, 24 in all: their types decide the Adept's class, one of them fights beside the Adept,
   and Pokémon on Standby power Summons. [Golden Sun's own Djinn.]
10. **Decided (12 Oct):** **Class lines for all 18 types.** How classes read Pokémon types. Recommended: every type
    gets its own class lines, picked by a weighted score across the three Set Pokémon (primary type 1 point, secondary
    0.5, so stacked secondaries can tip it), with certain type pairs unlocking special classes. [The types collapsed
    into Golden Sun's four elements.]
11. **Decided (12 Oct):** **Class ties.** Which line wins when two types score the same. Recommended: the type in the
    Adept's own element group; failing that, the fighting partner's primary type. [The fighting partner's primary type
    alone.]
12. **Decided (12 Oct):** **The class in battle.** Whether anything mid-battle changes the class. Recommended: locked
    for the whole battle: Mega Evolution, form or type changes and partner swaps don't change it, and it's
    recalculated after the battle. [Golden Sun's way, where spending Djinn changes the class at once.]
13. **Decided (12 Oct):** **One Summon system.** How Golden Sun's Summons and Unbound's Z-Moves and Dynamax fit
    together. Recommended: one Summon system with Z-Moves and Dynamax merged in, their visuals free to be reused as
    Summon variants (which ones stayed an open question), each Summon costing 1–3 Standby Pokémon of matching types by
    tier, drawn from the whole party. [Z-Moves and Dynamax kept beside the Summons.]
14. **Decided (12 Oct):** **Catching.** How Pokémon are caught. Recommended: both ways: Poké Balls for most Pokémon,
    and Djinn-style encounters for special and regional ones, which join on contact, run and must be cornered, fight
    first, or hide where only Psynergy reaches. [Poké Balls only; Djinn-style finds only.]
15. **Decided (12 Oct):** **The roster.** Which Pokémon are in the game. Progression 16 on the page later allowed Gen
    8/9 and regional evolutions with mapped methods. Recommended: all Gen 1–7 Pokémon catchable throughout, plus
    Megas, with Z-Moves and Dynamax folded into Summons. [Every generation, Gen 8 and 9 included.]
16. **Decided (12 Oct):** **Weyard-form families.** Which Pokémon get regional forms. Recommended: 25 families get
    Weyard-style forms in the spirit of the Hisuian ones, whole evolution lines changing (about 57 species): the Gen
    1–3 starters, the most popular non-legendaries and the six site legendaries, data first and art last. [Final
    stages only.]
17. **Decided (12 Oct):** **Weyard branches and Megas.** How Weyard lines branch and Mega Evolve. Recommended: Weyard
    Eevee can evolve into any Eeveelution and Weyard Kirlia can still become Gallade, with only Umbreon, Sylveon and
    Gardevoir getting Weyard forms; Weyard forms keep Mega Evolution, as 14 Weyard Mega and Primal forms. [Weyard
    lines limited to their Weyard branches; no Weyard Megas.]
18. **Decided (13 Oct):** **All eight Adepts in battle.** Phase 1 questions 4 and 5: how many Adepts can swap in, and
    what their partner does. Replaced the same day by the two crews. Recommended: all 8 can swap in, and the partner
    swaps too: the new Adept brings its own Set Pokémon in at once. [A pool of 6 Adepts; the old partner stays when
    the Adept changes.]
19. **Decided (13 Oct):** **Two crews of four.** The party for a native app. This replaces the 8-Adept pool above and
    DESIGN.md's single party with one Adept on the field. Recommended: two crews of 4, played one at a time, each with
    an Earth lead and a Sea healer: Crew 1 the hero, Sea, Forest and Shadow; Crew 2 the rival, Sea, Flame and Sky
    (Claude's line-up, as you asked, so the hero's crew has Move, Frost, Growth and Reveal). [One party of 8 swapping
    in; an earlier line-up with Flame and Sky in Crew 1.]
20. **Decided (13 Oct):** **When crews and Set Pokémon change.** Where the party can be rearranged. Recommended:
    Adepts move between crews only on the home island, Set Pokémon change only at restoration points, and the active
    partner can change any time outside battle, with the class recalculated. [Any change anywhere outside battle.]
21. **Decided (13 Oct):** **Four Adepts and four partners.** The battle format. This replaces DESIGN.md's 1 Adept + 1
    Pokémon per side, sized for the GBA's limit of 4 fighters, and was replaced in turn by bonded partners on 16 Oct.
    Recommended: the active crew's 4 Adepts and 4 partner Pokémon against an enemy side capped as in Golden Sun, about
    6 slots. [1 Adept + 1 Pokémon per side.]
22. **Decided (13 Oct):** **A downed Adept's partner.** What a partner does when its Adept falls. This replaces the
    phase 1 answer that the partner swaps with its Adept. Recommended: a Pokémon fights only while its Adept can; when
    the Adept falls, the partner gets one action, Rouse (once per Adept per battle: 50%, or 60% if its type is in the
    Adept's group, reviving at 25% HP) or a reviving item, then withdraws; Adepts can fight without Pokémon, and
    nothing swaps in battle but a fainted partner. [The partner swaps out with its Adept.]
23. **Decided (13 Oct):** **Healing at restoration points.** Who pays to heal. Recommended: Pokémon heal free; Adepts
    pay for HP, PP, revival and cures, priced like Golden Sun's Inns and Sanctums, and a paid Adept heal heals the
    Pokémon too. [Free healing for everyone, as at a Pokémon Center; paid healing for everyone.]
24. **Decided (13 Oct):** **Defeat.** What a lost battle costs. Recommended: the battle is lost when all 4 Adepts are
    down: you wake at the last restoration point with every Adept and Pokémon restored and lose half your coins,
    Pokémon's rule kept on purpose. [Golden Sun's rule: no coin loss, and Sanctums charge to revive.]
25. **Decided (13 Oct):** **Damage and stats.** Whose battle maths everyone uses. Recommended: Golden Sun's formulas
    and stat scale for everyone, partners included, with Adepts' HP clearly above their partners', and Power and
    Resist in each of the six groups, set for a Pokémon by its types. [Pokémon's damage maths.]
26. **Decided (13 Oct):** **Psynergy lists and Pokémon moves.** How many skills each side carries. Recommended: Golden
    Sun-style long Psynergy lists, in and out of battle, with no 4-slot cap; Pokémon keep 4 moves. [Psynergy capped at
    4 in battle.]
27. **Decided (13 Oct):** **Summons from the active crew.** Where the Standby Pokémon come from. This replaces
    DESIGN.md's whole-party pool. Recommended: Golden Sun's Djinn model applied to Set Pokémon, with Summons drawn
    from the active crew's Standby Pokémon, up to 8. [The whole party's Standby pool.]
28. **Decided (13 Oct):** **The enemy side.** Who you fight. Recommended: Golden Sun monsters, bosses and bandits,
    never catchable; wild Pokémon, catchable, mixed in within the cap; and human trainers who fight as Adepts with
    their Pokémon, with element-limited rosters like Pokémon's trainer classes. [Pokémon only, as in Unbound.]
29. **Decided (13 Oct):** **Tactics per partner.** How much of a battle runs itself. Since replaced by menus 12 on the
    page, which moved the tactics to the Adepts. Recommended: an optional tactics setting per partner (Auto, or a
    default action), plus "repeat last turn" and fast animations, with hand commands always possible. [Every command
    by hand.]
30. **Decided (14 Oct):** **The hero starts without a Pokémon.** Whether the creator hands out a starter. Recommended:
    no starter at creation: partners are gained through the story, the first at Keeper Brann's hatchery in mission 1.
    [A starter picked in the creator.]
31. **Decided (14 Oct):** **Scattered crews after the Breaking.** Mechanics question 3, for missions 12–20.
    Recommended: a small guest system: an Adept the other crew finds joins it as a guest, fills an empty slot with
    their own Set Pokémon and field Psynergy, and goes home at Marrow Isle or when their own crew's regroup chapter
    starts. [No guests: a missing Adept is absent until their regroup chapter (the recommendation).]
32. **Decided (14 Oct):** **Bags before the crews unite.** Mechanics question 4. Recommended: each crew has its own
    bag and coins until mission 10, then they merge; Pokémon storage is always shared. [One bag and purse from the
    start.]
33. **Decided (14 Oct):** **Legendaries caught mid-game.** Mechanics question 9: Ho-Oh after the Breaking, and Celebi,
    Lugia and Rayquaza in Act II. Recommended: they join at the level of the area where they're caught and can only be
    Set, never the active partner, until Act III. [Full use from the catch.]
34. **Decided (14 Oct):** **Allies at the Pinnacle.** Mechanics question 11: whether the islands you helped change
    mission 21. Recommended: each helped island adds a one-time battle assist in the Pinnacle fights: an item drop, a
    free Summon charge or a distraction that removes one enemy slot. [The closing montage only.]
35. **Decided (14 Oct):** **Talking a fight down.** Mechanics question 13: Hushwater, the Sentinel and Lugia.
    Recommended: a dialogue choice before or during a scripted battle that ends it, with no new battle rules. [Fight
    every one to the end.]
36. **Decided (14 Oct):** **The final battle relay.** Mechanics question 14. Recommended: Vey fights in two phases,
    one per crew, in the order the player picks, with his HP carrying over. [One final fight with one crew.]
37. **Decided (14 Oct):** **Kin Garden swaps.** Mechanics question 20: where Pokémon swap in from storage.
    Recommended: keep the rule: at any restoration point, which reaches the Kin Garden's storage. [Only on the home
    island, stricter and more Golden Sun-like.]
38. **Decided (14 Oct):** **Losing a story fight restarts it.** What happens when the party falls in a fight the story
    stages, such as Corvin's at the Vault door. Since replaced by progression 2 on the page ("Try again" or return).
    Recommended: the standard defeat plays, then the fight restarts from its start with the party, bag and coins as
    they were: no walk back and no coins lost. [The normal defeat: the last restoration point and half the coins.]
39. **Decided (16 Oct):** **Bonded partners.** Whether partners fight on their own. This replaces the 13 Oct line of 4
    Adepts and 4 partner fighters. Recommended: the active Pokémon stands behind its Adept: it lends a share of its
    stats that grows as it levels, adds its moves to the Adept's menu and shields its Adept from one hit a battle; the
    revive window and Rouse stay, so battles have up to 4 fighters a side and one stat system. [Partners as separate
    fighters, up to 8 a side.]
40. **Decided (16 Oct):** **EXP for all three Set Pokémon.** Who earns EXP after a battle. Recommended: all three Set
    Pokémon of a standing Adept, benched and Standby ones included, earn the full EXP, so they grow toward evolution
    and swapping partners over time pays. [Only the active partner.]

**Field and puzzles**

41. **Decided (12 Oct):** **Field Psynergy by group.** Which field Psynergy each element group has. Recommended: Earth
    Move, Pound, Tremor, Scoop; Flame Blaze, Burst, Force, Parch; Sea Frost, Douse, Ply; Sky Whirlwind, Cyclone, Mind
    Read, Teleport (late), Retreat; Forest Growth, Lash, Catch; Shadow Reveal, Cloak, Halt, Avoid. The whole party's
    works on the field, and puzzles use it in place of most HMs. [Pokémon's HMs.]
42. **Decided (12 Oct):** **Item Psynergy.** What Psynergy items are for. Recommended: items grant a Psynergy anyone
    can use (Lift, Carry, Hover, Grind, Sand, and backups of group Psynergy), as progression keys and as backups so no
    puzzle requires one specific Adept; Retreat and Avoid keep their item twins, Escape Rope and Repel, each pair
    sharing one effect. [Progression keys only, as in Golden Sun.]
43. **Decided (12 Oct):** **Water travel.** Whether water travel becomes Psynergy. Recommended: Surf, Dive and
    Waterfall stay Pokémon-powered, as HM-style field moves with no move slot: usable if any Set Pokémon can learn
    them, with Dive opening underwater maps. [Water Psynergy in their place.]
44. **Decided (12 Oct):** **Limited Surf.** Where Surf works. Recommended: only on rivers, lakes and coastal shallows,
    for short distances; deep sea needs the ship. [Surf anywhere, as in Pokémon.]
45. **Decided (12 Oct):** **World map and sailing.** How the world is crossed. Recommended: The Lost Age's world map
    and sailing, with the ship handling open sea. [Pokémon's routes between towns.]
46. **Decided (12 Oct):** **Unbound's quality of life.** Which conveniences come from Unbound. Menus 23 on the page
    later set DexNav's form. Recommended: DexNav, auto-run, and no HM moves taking up move slots. [Gen 3's own
    behaviour.]
47. **Decided (13 Oct):** **Field Psynergy per crew.** Whose Psynergy works on the field once there are two crews.
    This replaces DESIGN.md's whole party. Recommended: only the active crew's, with backup items for every group
    Psynergy, enforced in the engine from mission 3. [The whole party's.]
48. **Decided (14 Oct):** **Psynergy and HMs as one system.** Whether HMs stay beside field Psynergy. Recommended: one
    field-ability table: Cut, Rock Climb, Defog, Whirlpool, Surf, Dive and Waterfall stay as free puzzle verbs;
    Strength (it is Move), Flash (Reveal and Blaze) and Fly (Teleport) are dropped, and Rock Smash folds into Burst.
    [Psynergy replacing most HMs, as DESIGN.md had it.]
49. **Decided (14 Oct):** **Walking on the world map.** Mechanics question 2. Recommended: Golden Sun style, as
    needed: walk the continent and the large islands on the world map, sail between them, and enter small islands
    straight from the ship. [Ship-only travel.]
50. **Decided (14 Oct):** **Map changes at the midpoint.** Mechanics question 5. Recommended: map variants switched by
    flag: Canalport flooded, three isles sunk and three risen, the Galeway in fragments and the rim moved inward, with
    no timer. [A change on a timer.]
51. **Decided (14 Oct):** **The airship.** Mechanics question 6. Recommended: it flies over the world map on its own
    collision layer and lands only on marked pads, never inside towns or dungeons. [Landing anywhere.]
52. **Decided (14 Oct):** **The sky and undersea layers.** Mechanics question 7. Recommended: larger: the Cloudreach
    and the Deep Shelf each about a quarter of the Wide, with their own towns, routes and islands of the week. [One
    small sailable chunk each, with Dive spots to on-foot maps (the recommendation).]
53. **Decided (14 Oct):** **The Hollow.** Mechanics question 8: Giratina's mirror world. Recommended: recoloured
    copies of 5–6 earlier maps with new puzzles. [All-new maps.]
54. **Decided (14 Oct):** **The time loop.** Mechanics question 12: the Clockwork Key's repeating day. Recommended:
    one map with a loop-count flag; changes persist across loops only where the script says so. [A time-loop system of
    its own.]
55. **Decided (15 Oct):** **Crew 1's Surf.** Of Crew 1's story partners only Mudkip can learn Surf; Treecko, Torchic
    and Eevee can't. Demo 15 on the page keeps Marill as the gift. Recommended: a gift in Canalport: in mission 3 the
    harbourmaster gives the hero a canal Pokémon that can Surf, and Surf unlocks; water travel stays Pokémon-powered.
    [Surf only for a player who picked Mudkip.]

**Story structure**

56. **Decided (12 Oct):** **The region.** Where the game is set. Recommended: a brand-new region reminiscent of
    Weyard, later named Halcyra. [Golden Sun's Weyard itself.]
57. **Decided (12 Oct):** **Six elemental sites.** What drives the story. Recommended: six ancient sites like Golden
    Sun's lighthouses, each covering three types and bound to a legendary: Earth (Groudon), Flame (Ho-Oh), Sea
    (Lugia), Sky (Rayquaza), Forest (Celebi) and Shadow (Giratina); the six groups are also the Adept elements.
    [Golden Sun's four lighthouses.]
58. **Decided (13 Oct):** **The story's shape.** How the crews form in the story. Recommended: the hero alone against
    the rival, then a mission played as the rival, then recruitment missions for every other Adept, with crew swapping
    unlocked once the crews are built; a crew can be under 4 early, and some dungeons need both. [The phase 1 world
    proposal's four acts.]
59. **Decided (14 Oct):** **Tone and stakes.** From the story Q&A in the cloud chat (story.md §13). Recommended: warm
    adventure with real stakes: One Piece's warmth day to day, Golden Sun and Final Fantasy weight at the big moments,
    and losses (a town, a mentor) but no party deaths. [One Piece's warmth alone; Golden Sun's earnest moral grey.]
60. **Decided (14 Oct):** **The world and how it opens.** The story Q&A. Recommended: an archipelago around one
    walkable continent; a short guided intro, then open play, with areas blocked only by puzzles, story or monsters
    too strong (shown before you go). [A guided story throughout.]
61. **Decided (14 Oct):** **The conflict, the villain and the rival.** The story Q&A. Recommended: all three
    conflicts, layered: an order against free islands, then the elements failing, then an outsider's legacy; a
    sympathetic villain with a point (Lord Warden Vey); a rival who is a childhood friend whose path split from the
    hero's (Corvin). [One conflict alone; a villain without a point.]
62. **Decided (14 Oct):** **Star Trek and Final Fantasy.** Which parts of each the story takes (the story Q&A).
    Recommended: Star Trek's islands of the week with dilemmas, the ship as home and the crew as family, first contact
    and an exploration log; Final Fantasy's world-changing midpoint, personal arcs, optional superbosses and a
    late-game airship. [Some of these only.]
63. **Decided (14 Oct):** **The midpoint.** The story Q&A. Recommended: left to Claude, who wrote the Breaking
    (mission 11): the Galeway relay blown, the world map changed and the crews scattered. [A midpoint you set.]
64. **Decided (14 Oct):** **The legendaries.** The story Q&A. Recommended: all three roles: every legendary judges,
    several talk and take sides, and all six are catchable, each a different way (classically, after a story point, by
    puzzle, at the end of its arc). [Judges only; catchable only.]
65. **Decided (14 Oct):** **Length and ending.** The story Q&A. Recommended: 40–60 hours, with one ending and
    variations: each Adept's ending scene follows their heart quest, and the islands you helped join the montage.
    [Several endings.]
66. **Decided (14 Oct):** **Pokémon in society.** The story Q&A. Recommended: it varies by region: forest kin in the
    Greenwild, feared spirits on Hushwater, currency at the Bazaar, licensed only where the Tidewardens rule. [The
    same everywhere, as in Pokémon.]
67. **Decided (14 Oct):** **Home.** The story Q&A. Recommended: both: Marrow Isle, a home island that grows, and the
    ship as a mobile hub; Pokémon beyond the party limit live in the Kin Garden there until switched in. [A home
    island only; the ship only.]
68. **Decided (14 Oct):** **Easter eggs and spoof cameos.** The story Q&A. Recommended: small and large nods to all
    the influences throughout, a few One Piece and Star Trek themed puzzles, and copyright-friendly but obvious spoof
    characters in side stories. [No cameos.]
69. **Decided (14 Oct):** **Bounties.** The story Q&A and mechanics question 17. Demo 11 on the page keeps step 1 for
    the demo. Recommended: a real bounty system outside the story and after it: your crew's own bounty (wanted
    posters, rival hunters) and a Freeport Guild board, built in three steps: hand-written contracts, then generated
    ones, then rival hunter crews. [Cosmetic bounties only, the earlier recommendation.]
70. **Decided (14 Oct):** **After the ending.** The story Q&A and mechanics question 19. Recommended: the world stays
    open: a post-ending flag switches the maps to their final variants and returns you to Marrow Isle, with side
    quests, exploration, catching and the Log still there. [The game ends at the credits.]
71. **Decided (14 Oct):** **Crew 2 interludes.** Mechanics question 1: how the rival's crew gets its turns in an open
    Act I. Demo 7 on the page later fixed the exact trigger. Recommended: a Crew 2 interlude starts at the next
    restoration point after each Crew 1 recruitment (missions 7 and 8), and Crew 1 resumes where it left off.
    [Interludes at fixed points in the mission order.]
72. **Decided (14 Oct):** **The postgame.** Mechanics question 15. Recommended: bigger: the Farside, a full region
    beyond the Rimfalls and the Farers' own world, with its own story, Pokémon, named bounties and the final
    superboss. [A small set of new islands and superbosses with the remaining catches (the recommendation).]
73. **Decided (14 Oct):** **Mini-games.** Mechanics question 18. Recommended: build all three, from Act II: the
    Speakers' language puzzle, the Dodo Derby and the Glimmer Saucer. [The language puzzle only, with the Derby and
    the casino as postgame extras (the recommendation).]
74. **Decided (16 Oct):** **Adult mode.** Your request. Recommended: an optional Key Item, the Adult-o-Vision glasses,
    switches an adult mode on and off at any time, opening alternate sprites, story points, dialogue, easter eggs and
    a side mission that collects hidden pictures into a hidden gallery; adult scenes are between consenting adults
    only. [No adult content.]
75. **Decided (17 Oct):** **Adult mode's own missions.** What else the mode holds. Adult 7 and 8 on the page set how
    many and which. Recommended: adult-themed side missions, missions that exist only in the mode, and mode-exclusive
    variants of main missions; a variant changes scenes and lines, never unlocks. [The gallery hunt as the only adult
    mission.]
76. **Decided (17 Oct):** **The unique adult weapon.** Your answer to adult 11, beside reskins that keep their
    numbers; adult 23 on the page sets its power. Recommended: one unique ultimate weapon of our own design, the Giant
    Dildo Sword, unlocked at the end of one adult side quest and usable from then on. [Reskins only.]
77. **Decided (17 Oct):** **Adult videos.** Your note on adult 15 (how explicit). Recommended: videos too, beside
    explicit text and pictures; adult mini-games wait for a later version. [Text and pictures only.]
78. **Decided (17 Oct):** **Mind Read with the mode on.** Your note on adult 16 (generic townsfolk, on adult bodies
    only). Recommended: Mind Read on a townsperson reads a dirty thought, and some thoughts add a picture or video to
    the Gallery or an alternate line. [Mind Read unchanged by the mode.]

**Art and UI**

79. **Decided (12 Oct):** **The look.** How the game looks, in DESIGN.md. Art 3 on the page later made every person
    LPC, and art 12 sets the move effects. Recommended: Golden Sun's world (its tilesets and chibi field sprites) with
    Pokémon-style battle scenes and Golden Sun's spell and Summon effects. [Pokémon's look throughout; Golden Sun's
    look throughout.]
80. **Decided (12 Oct):** **Menus and dialogue boxes.** Whose menus the game uses. The battle half was replaced on 15
    Oct. Recommended: Golden Sun's menus and portrait dialogue boxes on the field and Pokémon's menus in battle, with
    the menus' functions built early and the Golden Sun look last. [Pokémon's menus everywhere.]
81. **Decided (13 Oct):** **Level-ups.** How level-ups are shown. Recommended: Adepts' as in Golden Sun, in the
    message window (the new level, each stat's gain, then new Psynergy); Pokémon keep the Pokémon-style level-up and
    evolution popup, with Golden Sun-scale stats. [One style for both.]
82. **Decided (14 Oct):** **The character creator.** What the player sets for the hero. Menus 28 on the page later let
    pronouns change at the mirror too. Recommended: the proposed options approved: name, gender, pronouns as their own
    choice (defaulting to the gender, with "they" always there), skin, hair, eyes, outfit, colours and an accessory,
    all cosmetic; name and gender fixed once made, cosmetics changeable at a mirror at home. [Pronouns tied to gender;
    a fixed hero.]
83. **Decided (14 Oct):** **Navigation aids.** The story Q&A and mechanics question 10. Story 3 on the page later gave
    Torro's room a scripted bearing. Recommended: all four: danger stars on the map, one tall landmark per region, the
    Lodestar compass and rumour markers, all as world-map UI, with rumours as flags set by dialogue and danger a
    hand-set number per area. [Fewer aids; a new gameplay system for them.]
84. **Decided (14 Oct):** **The Farer's Log as a screen.** The story Q&A and mechanics question 16. Menus 22 and demo
    32 on the page set its pages and where it's found. Recommended: a Pokédex-style book as a menu screen in four
    sections (Kin, Bestiary, Charts, Relics and Cultures): Kin entries from the species data plus a hand-written text,
    habitat marks from the encounter tables, "seen" on first sight, and a completion % with rewards per section. [A
    plain Pokédex.]
85. **Decided (15 Oct):** **64-px Adepts.** The scale of the new art. Asked about 128 px, the answer was to draw at 64
    and show bigger where wanted. Recommended: Adept sprites at 64×64 if possible, 32×32 if not, and other art at that
    scale where it can be, replacing Golden Sun's small field sprites in the graphics pass. [Golden Sun's small field
    sprites; 128-px Adepts.]
86. **Decided (15 Oct):** **Heroes on the left.** Which side each team stands on in battle. Recommended: the party
    along the lower left, seen from behind and facing up-right, the enemies across the upper right facing down-left,
    with Golden Sun's sheets mirrored. [Golden Sun's sides, the other way round.]
87. **Decided (15 Oct):** **Sprites scale with the line.** How big battle sprites draw. Replaced on 16 Oct by art 10
    on the page (whole-number scales). Recommended: a lone foe at 1.3 and a full line of eight at 0.7, with the
    spacing to match. [One fixed scale.]
88. **Decided (15 Oct):** **Boxes over the sprites.** Where the battle menus sit. This replaces Pokémon's menus in
    battle. Recommended: while choosing, the status box (top left) and the command menu (bottom centre) draw over the
    fighters and hide while the round's words play at the top, as Golden Sun does, clear of the touch controls, with
    enemy names above their heads. [Pokémon's battle menus.]
89. **Decided (17 Oct):** **Battle all at 2×.** Talked over in chat with the demo's art direction. This replaces art
    10's 1× for five or more enemies. Recommended: everything in battle at 2×, Pokémon pictures and LPC Adepts the
    same pixel size, on a pixel-art backdrop. [Art 10: enemies at 1× for five or more.]

**Process**

90. **Decided (12 Oct):** **Function first, cosmetics last.** DESIGN.md's guiding principle, restated on 14 Oct.
    Recommended: make it work first and pretty at the end: custom art, sprites and most cosmetics come last unless
    story or function needs them sooner, with existing assets as placeholders; graphics are remade after the engine
    works, music and sound near the end. [Art alongside each feature.]
91. **Decided (12 Oct):** **Where decisions are made.** Which document rules. Replaced on 18 Oct by the decision page.
    Recommended: the claude.ai project's component-decisions doc is where design decisions get made, and DESIGN.md is
    the copy Claude Code builds from. [This repo alone.]
92. **Decided (12 Oct):** **Left out for now.** What isn't a must-have. Recommended: Unbound's difficulty modes, its
    Missions and Mission Log, and its Battle Frontier, Tower and Circus; they could come back later. [Keep Unbound's
    extras.]
93. **Decided (13 Oct):** **Who writes the story.** Who writes the story missions. Recommended: Claude writes them in
    the story document, and anything there that needs a mechanic or changes how the game plays comes back to you as a
    question. [You write the story.]
94. **Decided (14 Oct):** **The story in the cloud chat.** Where story decisions are made. This narrows the 12 Oct
    rule for the story. Recommended: non-mechanical story decisions are made in the cloud chat and this repo records
    them; the story was written there from a Q&A. [The story worked out in this repo.]
95. **Decided (15 Oct):** **An asset audit before mission 10.** What to do before the last Act I mission. Recommended:
    pause mission work after mission 9 for an audit of the art libraries (the CC0 packs, the CC0 sprite library and
    the LPC generator), with picks and gaps. [Keep building missions, audit later.]
96. **Decided (16 Oct):** **The story chat archived.** Where story questions go now. This replaces the 14 Oct cloud
    chat. Recommended: archive the story chat: story questions go to the decision page beside the mechanics ones, and
    the engine side updates story.md from the answers. [Story questions in the cloud chat.]
97. **Decided (16 Oct):** **The local folder's materials.** Whether what you put in the local folder can be used.
    Recommended: yes, with or without licence terms, with your approval per item where needed, and every maker tracked
    for an end-credits scroll. [Openly licensed assets only.]
98. **Decided (17 Oct):** **The local folder where it's better.** Your note on the music route. This widens the 16 Oct
    rule. Recommended: anything in the local folder may be used wherever it is better for the story or in quality.
    [The library picks first, the local folder as a fallback.]
99. **Decided (17 Oct):** **The order of work: the demo first.** What comes after Act I was built. This changes the 12
    Oct "cosmetics last" for Act I; adult 10 on the page places adult mode. Recommended: a playable Act I demo
    (missions 1–10) with great art first, its art, engine and story finished; adult mode and mission 11 after it; the
    decompile and asset reviews keep running in the background until done. [Mission 11 next, with the art at the end.]
100. **Decided (18 Oct):** **Every question on the decision page.** Your rule, 17–18 Oct. This replaces the 12 Oct
    rule and widens the 16 Oct one, which moved only story questions here. Recommended: the cloud chat is archived and
    no longer used: every question and every decision lives on the decision page, those made elsewhere included, as
    logged here. [Story questions in the cloud chat; decisions kept only in the CHANGELOG.]
