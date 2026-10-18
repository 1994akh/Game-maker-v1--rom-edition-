# Progression: levels, power scaling and evolution

From the progression audit (15–16 Oct). Agents read the engine, then simulated story fights and level curves with
the Python battle oracle (`gs_battle.py`) on engine main with bonded partners. Each finding was checked by an
adversarial verifier and a critic. Anything not marked **Built** or **Decided** is **proposed**.

## 1. The short answers

- **Does levelling work end to end?** The code does: Adepts reach 99, partners keep pace on the Adepts' table,
  and saves can't overflow. What breaks is the story's EXP and content:
  - Story-only play leaves everyone at about L5–6 through Act I, but the story fights were tuned at L7.
  - A lost story fight restarts with no way out.
  - Golden Sun 1's enemies stop at L43, with regular foes topping out at L28.
- **Does power scaling hold, or does anything go obsolete?**
  - **Adepts.** They get fragile at L20–32, because the class never rises and gear never improves. A regular foe
    needs only about 2.2 hits to down Rowan at L30.
  - **Bonded Pokémon.** They always add 9–17% HP and the one-hit shield.
  - **The Pokémon command.** It keeps up for Adepts with weapons (Squire, Guard). For the weaponless Seers it
    goes flat from about L20–40, because physical moves add only power ÷ 4 when Attack is below the enemy's
    Defense.
  - **Unleash** stops mattering from about L10–20.
  - **Summons** scale with enemy HP, so they are the one Pokémon role that doesn't go flat. Not yet measured.
  - **Late game.** Past L43–50 the content runs out before anything else does.
- **Do evolutions work?**
  - Level evolutions work, including for benched Set Pokémon and the waiting crew.
  - Item, trade and friendship evolutions don't exist yet, so Tamsin's Riolu and Maren's Eevee can never evolve.
  - On the current curve, no story partner evolves in Act I. The starters evolve at about Adept L17.

## 2. Fixed on 16 Oct

| Engine PR | What |
|---|---|
| #50 | The waiting crew earns half of each won battle ([party-and-battle.md](party-and-battle.md) §5) |
| #51 | The exporter keeps evolution conditions (131 entries). Ralts, the Togepi line and 6 other species get real types; the colour forms and Mothim export, so no evolution target is missing. `evolve()` only fires on conditions the game can meet |
| #52 | A bonded Adept keeps its partner's HP share through a level-up (it lost 12–32 HP before). Gifts take the species table's name ("Mime Jr."), and gift ids never repeat |

Still to come, needing no decision:
- tests at the level caps and on pace for every growth rate;
- `tools/progression_check`, which replays only the story's EXP and prints each crew's level at every story fight.

## 3. Measurements

**Story fights, chance to win per attempt** (300 seeds, bonded partners). Columns are three ways of playing: plain
Attack only, Psynergy used sensibly, and Psynergy plus the Pokémon command.

| Fight | Party | Attack only | Psynergy | + Pokémon |
|---|---|---|---|---|
| Corvin (M1) | hero L5 + Treecko | 51% | 99% | 100% |
| Sluice Beast (M3) | hero + Maren at L5, as the story gives | 0% | 74% | 82% |
| Sluice Beast | L7, as tuned | 23% | 100% | 100% |
| Ho-Oh (M4), straight after Tamsin, no inn | Corvin + Tamsin at L5, as the story gives | 0% | 14% | 62% |
| Ho-Oh | L6 | about 1% | 86% | 98% |
| Ho-Oh, fresh, 5 Herbs | L7, as tuned | 7% | 100% | 100% |

The mission checks raise the party to L14–16 before these fights, so no check tests a level the game actually
produces.

**Adept growth** (Rowan: Isaac's curve, Squire, starting kit). The "Spire" column is the best Psynergy that ignores
Attack.

| Lv | HP | Attack | Spire Psynergy | Plain Attack vs ±2-level foes | Hits to down Rowan |
|---|---|---|---|---|---|
| 10 | 107 | 55 | 49 | 16 | 2.7 |
| 20 | 191 | 96 | 94 | 18 | 2.0 (bonded 2.3 + shield) |
| 30 | 275 | 138 | 92 | 8 (bonded 15) | 2.0 (bonded 2.2 + shield) |
| 50 | 442 | 220 | 173 (last learned at L42) | 48 | 3.6 |
| 99 | 851 | 424 | 173 | 150 | 10 |

Past the content (about 688 EXP a battle at best), L30 to L43 takes about 670 battles, L43 to L60 about 2,700,
and L60 to L99 about 8,100.

**What the Pokémon command is worth:** its best move against the best Psynergy, per target, per hit, ignoring PP.
Past L43 these are measured against an extrapolated enemy that doesn't exist yet.

| Adept Lv | Hero + Torchic line | Maren + Eevee | Story evolutions by then |
|---|---|---|---|
| 10 | 0.71 | about 0.6 | none |
| 20 | 0.41 | 0.43 | the starters at about A17, Rowlet A18 |
| 40 | 0.62 | 0.28 | Ralts A22/A32, Gastly A26, Larvitar A32, second starter stage A37 |
| 50 | 0.35 (0.48 vs real foes; Blaziken has dropped Slash) | about 0.22 | |
| 99 | 0.54 | 0.22 | Riolu and Eevee: never |

The Pokémon command costs no PP, so in a long dungeon it is a Seer's only free damage (their plain Attack does
about 2).

## 4. Evolution, the rest (proposed)

1. **Data.**
   - `data_src/evolution_rules.json` maps each condition the game has no system for:
     - **Friendship** becomes a fixed level per species: Riolu at 20, Golbat at 35, the babies at 15, Chansey at 40.
     - **Trade** uses the existing item twin (the Linking Cord etc.); Karrablast and Shelmet get one.
     - **Knows a move** becomes the level the move is learned.
     - **Time, gender and weather** are ignored where one target remains, and become the player's choice where two
       remain. **Since 17 Oct** the day/night clock is decided: time conditions read it
       ([day-night-clock.md](day-night-clock.md) §2).
     - **Gen 8/9 and regional** targets: **allowed with mapped methods** (decision 16, your answer 17 Oct); the
       exporter maps each one's method to a rule above or leaves it held back until its rule exists.
     - **Eevee** evolves by stone: Sun → Espeon, Moon → Umbreon, Shiny → Sylveon. Maren's Shiny Stone could be a
       gift in her arc.
     - **Kirlia → Gallade** by Dawn Stone.
2. **Resolver** (`src/battle/evolution.gd`):
   - It lists the targets that qualify, given the level or the item used.
   - An unmapped condition never qualifies, and "level 0" never means "any level".
3. **Applying it.**
   - The species changes, and the name changes unless the player gave a nickname.
   - The pages are: "What? X is evolving!", "X evolved into Y!", a stat-gains line, then the moves learned.
   - The new species' evolution move counts as learned. Today Lucario's Aura Sphere and Gardevoir's Dazzling
     Gleam are pushed out of the last four moves.
4. **Triggers.**
   - A level-up after battle, as now.
   - An evolution item used from the field menu, used up only when the evolution happens. The items get ids
     9100–9199 ([items-and-economy.md](items-and-economy.md) §4 and §9).
   - Kin Garden Pokémon evolve by item only.
5. **Choices.**
   - When two targets qualify (Wurmple, Tyrogue, Rockruff), the player picks "Which way?" or "Not now".
   - "Not now" postpones to the next level-up.
   - An evolution that would remove the crew's last unlocked water HM warns and defaults to "Not now".

## 5. Decisions for you

Recommended first. The alternatives are in brackets.

Answered on the decision page: accepted items are marked **Decided** with the date, the rest **To talk over**.
**Act I levels and story fights**
1. **Decided (17 Oct):** **Story recruits' levels.** Corvin copies the hero's level once, which is L5 unless you trained. Recommended: a
   join-level floor per mission in data (Corvin L7 at M2 and M4, L8 at M7, L9 at M8), then re-measure every story
   fight. [Add random fights to crew 2's rooms; retune Tamsin and Ho-Oh for L5; leave it.]
2. **Decided (16 Oct):** **A lost story fight.** Today it restarts forever, and an Attack-only player can be stuck. Recommended: after a
   loss, offer "Try again" or "Return to the last restoration point", with the fight not done. Add Flee to ordinary
   fights with Golden Sun's formula. [Keep the restart, with a test that every story fight is winnable at story
   levels.]
3. **To talk over:** **Target levels per mission.** Recommended: about L6–7 at M3, L8 at M5, L10 at M10, reached through more encounter
   tables in mission rooms and bigger story-fight EXP, checked by `progression_check`. [Accept a flat L5–7 Act I;
   rely on grinding.]
4. **To talk over:** **Stonehollow's west gate** opens onto Golden Sun world zones of L14–21, where an L5 party wins 0–8%.
   Recommended: put it behind a story flag until our world map and danger stars exist. [Leave it open, with Flee
   and danger markers.]

**Adept growth**

5. **Decided (17 Oct):** **Class tiers.** Recommended:
   - Golden Sun's 5-tier lines, rising at Adept L1/10/20/30/40.
   - Each Set Pokémon of the Adept's group adds +1 elemental level (+5 Power and Resist).
   - At L30 that takes hits-to-down from 2.0 to about 3, and unlocks the late Psynergy (the Gaia line, Revive, Wish).

   [Tiers by Set Pokémon type count, like Djinn; one tier per act; keep tier 1 and weaken enemies.]
6. **Decided (16 Oct):** **Level span.** Recommended: the main story ends around L45–55, as Golden Sun's does. Golden Sun 2's enemies are
   extracted for Acts II–III, and L56–99 is post-game. [Scale GS1 monsters by area; raise EXP; lower the cap.]
7. **Decided (16 Oct):** **Gear** is the equipment review's question: an equip menu plus shops and chests by area.
8. **Decided (17 Oct):** **Vesper's curve.** She casts Water Seer Psynergy on Jenna's Mars curve (Mercury Power 77, so heals are 26%
   weaker). Recommended: Mia's curve (pc 3) until Shadow has its own Psynergy. [A Mars placeholder class.]
9. **Decided (17 Oct):** **Psynergy after L50.** Recommended: no new entries if the story ends near L50, which is true to Golden Sun.
   Ragnarok and Heat Wave still grow with Attack. [Add Golden Sun 2 Psynergy up to the cap.]

**Pokémon**

10. **Decided (16 Oct):** **Physical moves.** Recommended: they add power ÷ 2 like special moves, so the move's power sets the damage for
    every Adept, Seers included. [A level-based Attack floor for weaponless Adepts; accept it.]
11. **Decided (16 Oct):** **Learning moves.** Recommended: each Pokémon stores four moves, with a "Learn X — forget which?" prompt at
    level-up and evolution. [Keep the automatic last four, but always keep the strongest damaging move.] Today
    Riolu at L52+ offers only Final Gambit, and Blaziken drops Slash at L49.
12. **Decided (17 Oct):** **Partner pace.** Recommended: one growth factor (1.0) for every partner. A partner only lends 30%, so slow and
    fluctuating partners trailing 12–22 levels late isn't worth the flavour. [Keep today's factors; clamp to within
    ±3 of the Adept.]
13. **Decided (16 Oct):** **Evolutions beyond level.** Recommended: the rules in §4. [A "bond" counter on each record; a day/night clock;
    story-beat evolutions only.]
14. **Decided (16 Oct):** **Branches** (Wurmple, Tyrogue, Rockruff, Eevee). Recommended: "Which way?" or "Not now". [Fixed by the
    record's id; first entry plus an item for the other.] Until then the first branch wins.
15. **Decided (16 Oct):** **Several stages at once.** Recommended: keep chaining, since a synced partner rarely gains more than a level or
    two a battle. [One stage per level-up, as in the main games.]
16. **Decided (17 Oct), alternative:** **Gen 8/9 and regional evolutions.** Recommended: left out. [Allowed with mapped methods; "Weyard" as a region.]
17. **Decided (17 Oct):** **Weyard forms.** Recommended: story partners switch to Weyard species ids at the Weyard data pass, with a save
    migration. [Rename species in place; a "form" field.]
18. **Decided (17 Oct):** **Ho-Oh's wasted moves.** Ho-Oh picks Whirlwind and Life Dew, which do nothing. Filtering them makes a 14% fight
    harder, so decide with item 1.
19. **Decided (16 Oct):** **Wild Pokémon EXP.** It is linear (yield × level ÷ 50), so from about L15 a wild Pokémon is worth 0.2–0.7 of a
    same-level monster. Recommended: scale it to the area's monster EXP. Decide with item 3.
20. **Ho-Oh in Act I** (your note on decision 18: "Ho-Oh is unlocked REALLY early ... devalues legendaries").
    Ho-Oh is never caught in Act I: story.md has it judge Crew 2 at mission 4 and be caught only after the Breaking,
    in Embral's caldera (items 25, your answer). What comes early is the top Flame Summon, unlocked when the
    judgement ends (story decision 9). Recommended: at mission 4 Ho-Oh judges and flies off, and the crew gains
    nothing legendary; the top Flame Summon unlocks with the caldera catch after the Breaking, so legendaries stay
    special. [Keep the Summon at mission 4 as story decision 9 says; unlock it at mission 4 but weaker until the
    catch.]

## 6. Not covered yet

- **Summons** as late-game Pokémon power. They deal a percent of the enemy's max HP, plus the summoner's Power
  boost.
- **Mega Evolution.** It is promised for 14 Weyard Megas, including Blaziken, Lucario, Gardevoir, Gengar and
  Tyranitar, but how it works with the bond is open.
- **Z-Moves and Dynamax** folded into Summons (DESIGN.md's open question).
- **Guests and the Breaking** (after mission 11). Adepts outside both crews earn nothing, so they need a catch-up
  rule.
- **Held items or gear for partners.** These go to the equipment review.
- **Stat-raising items** (Golden Sun's Power Bread and Mint, Pokémon vitamins). These go to the items review.
- **Special Pokémon encounters** (DESIGN.md's Djinn-style finds): the level they join at.
