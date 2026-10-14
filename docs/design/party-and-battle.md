# Party and battle rules

Agreed 13 Oct 2026, for the native Android app. Labels:
- **Decided:** you chose it, or agreed to my proposal for it.
- **Proposed:** added after an adversarial review (two independent reviewers) to close gaps in the decided rules.
  Not confirmed yet.
- **Corrected:** a decided item whose wording or numbers the review showed were wrong. The intent is unchanged.

This spec replaces several parts of DESIGN.md, listed in §10. Those parts were written for the GBA's 4-fighter
limit and a single party, and a native app with two crews needs neither.

Golden Sun facts come from the ROM extraction. The notes and reference code (`re/notes/gs_*.md`,
`re/gbax/codecs/gs_battle.py` and others) are added to this repo in PR #4.

## 1. Two crews of four

- **Decided:** the 8 Adepts form two crews of 4. You play one crew at a time.
- **Decided composition** (Claude's call, as you asked). Each crew has an Earth lead and a Sea healer. Crew 1 holds
  Forest and Shadow, so the hero's crew has DESIGN.md's whole proving set of field Psynergy (Move, Frost, Growth,
  Reveal) without backup items. This replaced an earlier line-up that put Flame and Sky in Crew 1.

  | | Crew 1 (the hero's) | Crew 2 (the rival's) |
  |---|---|---|
  | Lead | Earth: hero | Earth: rival / co-lead |
  | Healer | Sea: healer 1 | Sea: healer 2 |
  | Others | Forest, Shadow | Flame, Sky |
- **Decided:** Adepts move between crews **only on the home island / village**.
- **Decided:** Set Pokémon change **only at restoration points**. That covers which 3 Pokémon are Set on each Adept
  and swapping them with Pokémon in storage.
- **Decided, healing at restoration points:**
  - **Pokémon** heal **free**.
  - **Adepts** pay coins for healing (HP, PP, revival and cures), priced like Golden Sun's Inns and Sanctums.
  - A paid Adept heal also heals the Pokémon.
  - Healing outside restoration points (Psynergy, items, partner moves) is unaffected: it heals only its target.
- **Decided:** which of an Adept's 3 Set Pokémon is the active partner can be changed any time outside battle from
  the menu. The class is recalculated afterwards.
- **Decided, how the crews form (story):**
  - **Opening:** the party is **only the hero**, facing the rival.
  - **Then you play as the rival** for a story mission.
  - **Recruitment:** every other Adept has their own story mission(s). Each one either adds them to a crew or moves
    the story forward.
  - **Swapping between the crews** (switching which crew you play, and moving Adepts between crews on the home
    island) **unlocks only once the story missions that build the crews are done.** Before then, the story decides
    which crew you play.
  - So a crew can have fewer than 4 Adepts early on, and battles use however many it has (down to 1 Adept + 1
    partner). 4 + 4 is the maximum.
  - Some dungeons need both crews.
- **Proposed, crew logistics:**
  - **Handovers:** each story handover between crews starts at a restoration point.
  - **The other crew** waits on the home island once swapping is unlocked.
  - **Shared:** the bag, coins and Pokémon storage are shared by both crews.
  - **Per crew:** each crew keeps its own "last restoration point".
  - **Getting home:** once swapping is unlocked, every restoration point offers travel to the home island, so a
    crew without Teleport or Retreat can't strand itself.

## 2. Who is in a battle

- **Decided, your side:** the active crew's 4 Adepts, each with one partner Pokémon, so up to 8 fighters.
- **Decided, the battle line:** each Adept stands next to their partner. When a partner withdraws or faints with no
  replacement, the line closes the gap. This matters because Golden Sun's spread attacks hit neighbours.
- **Decided, the enemy side:** it isn't only Pokémon, and its size is capped at what Golden Sun allowed.
  - **Corrected:** the exact cap is **not yet confirmed from code**. Extracted groups never exceed 6 enemies (GS1)
    or 5 (GS2), and the notes say "6 slots, large enemies take 2", but that line has no code evidence.
  - **To do:** trace the group-setup routine (GS2 `FUN_08127cd4`, GS1 `0x080C1A40`). Until then the working figure
    is 6 slots.
- **Decided, enemy types:**

  | Enemy | Catchable | How it fights |
  |---|---|---|
  | Golden Sun monsters, bosses and bandits | No | Extracted stats, Psynergy, AI and drops. **Corrected:** about 260 distinct enemies across both games (GS2's version where both have one), not 541. The record counts include Djinni battles, placeholders and boss phases |
  | Wild Pokémon | Yes | Mixed with monsters in wild battles, within the cap |
  | Human trainers | No | Adept + Pokémon pairs, 2 slots each, with element-limited rosters like Pokémon's trainer classes |

- **Proposed, how enemy trainers mirror your crew:**
  - **Set Pokémon:** each enemy Adept has up to 3, with the same partner, replacement and revive-window rules.
  - **Unleash and Summons:** they draw on the enemy Adept's benched Set Pokémon. This also answers the earlier open
    question of where enemy trainers' Standby pool comes from.
  - **AI:** in the revive window the AI uses Rouse. Summons follow a Z-move-style "should use" check.
  - **Targeting:** the AI targets the player's Adepts as well as their Pokémon, so it can't be beaten by simply
    focusing its Adepts.
  - **Size:** a Pokémon takes 1 slot unless its species is flagged large (for example Wailord or Groudon), in which
    case it takes 2.
- **Proposed, how a battle is won:** wild and monster sides lose when every enemy is down or caught. Trainer sides
  lose when all their Adepts are down, checked by the rule in §3.

## 3. Adepts and their partners

**Decided:**
- **A Pokémon fights only while its Adept can.**
- **When an Adept is downed,** their partner gets **one action** to try to revive them. If it fails, or the partner
  does something else, the partner can't act until the Adept is revived.
- **If an Adept is already downed when a battle starts,** neither they nor their Pokémon take part.
- **An Adept can fight without a Pokémon** when all of theirs have fainted.
- **No swapping during battle,** except that a fainted partner is replaced.
- **The revive action:** a reviving item from the bag, or **Rouse**, a chance-based revive at low HP that every
  partner has.
  - **Corrected:** "a reviving move" is dropped, since no Gen 1–7 move revives an ally. Custom moves (for example
    Weyard-form signatures) could add it later.
- **After that one action,** the partner **withdraws** and can't be targeted.
- **If another Adept revives them later,** the partner comes back at the end of that turn. This also applies to an
  Adept who started the battle downed and is revived during it.
- **A fainted partner's replacement** comes in at the end of the turn, at no cost. It must be one of that Adept's Set
  Pokémon that isn't on Standby, recovering or fainted. If one returns from Recovery while its Adept has no partner,
  it joins at the end of that turn.
- **Defeat (decided, kept 13 Oct):** the battle is lost when all 4 Adepts are down. You wake at the last restoration
  point with **every Adept and Pokémon restored**, and lose **half your coins**.
  - This is Pokémon's rule, kept on purpose. Golden Sun's differs: the extracted text has no coin loss on defeat,
    and its Sanctums charge to revive.

**Proposed, the revive window:**
- **Opening:** when an Adept is downed, the partner's queued command is cancelled. At the partner's next action
  (this turn if it hasn't acted, otherwise next turn), it gets a short menu: **Rouse / item / pass**.
- **Ally revives first:** if an ally revives the Adept before then, the window closes, the partner gets its normal
  menu, and no item is used up.
- **Both down at once:** if the Adept and partner go down in the same action, there's no window. The partner has
  fainted, and its replacement waits until the Adept is revived.
- **Partner can't act:** a status that makes the partner skip its turn (sleep, stun) uses up the window.
- **Automation:** Auto tactics and "repeat last turn" always take the window with Rouse.
- **Rouse limits:** **once per Adept per battle**, and only on the partner's own Adept. This prevents down → Rouse
  loops, for the enemy as well.
- **Decided, Rouse numbers** (Claude's call, as you asked; tune in play-testing):
  - **Success chance:** 50%, or 60% if the partner's type is in its Adept's element group (the same matching idea
    as the class bonus).
  - **On success:** the Adept comes back with 25% of max HP.
- **Items:** partners can use bag items **only in the revive window**, so a turn still has at most 4 item users,
  as in Golden Sun.
- **Victory and defeat:** checked only after every open revive window has resolved, so the last Adept's partner
  always gets its try. The same rule applies to enemy trainers.

**Proposed, end-of-turn order:**
1. Status damage
2. Standby recovery ticks
3. Revived Adepts' partners return, and replacements come in
4. Victory and defeat check

## 4. Set, Standby and Summons

**Decided:** this is Golden Sun's Djinn model, applied to Set Pokémon.
- **Unleash:** an Adept spends their turn to unleash one of their **two benched** Set Pokémon. It uses its
  signature move and goes to Standby. The active partner can't be unleashed.
- **Summons** cost 1–3 Standby Pokémon of matching types, drawn from the **active crew**. **Corrected:** that's up
  to **8 per crew** (4 Adepts × 2 benched), not 12.
- **Class** stays locked during battle. Unlike Golden Sun, unleashing doesn't change it.
- **Corrected, recovery (re-checked against the code, 14 Oct):**
  - Recovery is **per Adept**. Each Adept's spent Pokémon get countdowns of 2, 3, 4…, assigned at the end of the
    Adept's turn. The countdowns drop **at the end of each round**, only while that Adept is in the battle with HP
    above 0. So the Pokémon return at the ends of rounds R+1, R+2, …, one per Adept per round.
  - So a Summon paid by three Adepts can return three Pokémon in one round.
  - An earlier version of this page said the countdowns drop on the Adept's own turn. Golden Sun 1's code ticks
    them at round end (`re/notes/gs_battle_mechanics.md` §13); the page now follows the code.
  - **Also from the code:** after a Summon, the summoner gains Power in the Summon's element for the rest of the
    battle, 5 × b × (b + 1) for b Pokémon spent (+10 / +30 / +60 / +100). We keep that.

**Proposed:**
- **Downed Adept:** their Standby Pokémon can't be spent and don't recover until the Adept is revived. Fainted
  Pokémon can't be unleashed or spent.
- **After battle:** all Standby and recovering Pokémon return to Set when the battle ends. Golden Sun carried
  Standby over and ticked it while walking, which would make the class shift between battles.
- **Field menu:** there's no Standby from the field menu.
- **Locked with the class:** Set Pokémon bonuses and element Power/Resist are locked during battle along with it.

## 5. Stats, damage and levelling

- **Decided: damage uses Golden Sun's formulas**, from the reference implementation `gs_battle.py`.
  - **Corrected (14 Oct):** its formulas match the game's own routines in 2,794 emulated checks (GS1 1,293, GS2
    1,499), covering attack, Psynergy, healing, PP drain and recovery, guarding, the Summon HP bonus and the
    status-chance roll. Criticals and multi-hit are read from the code, not emulated.
  - Four earlier claims were wrong and are fixed in the notes and the code: Golden Sun 1 has two Guard levels (half,
    then one tenth), it does have a Summon bonus (+3/6/9/12% of the target's max HP by tier, uncapped), Drain-type
    abilities deal HP damage when they land, and PP recovery has no random part.
- **Decided: Pokémon partners use Golden Sun's stat scale,** and Adepts clearly out-HP their partners.
- **Corrected, HP conversion:** the earlier "base HP / 100 × 0.6" let high-HP Pokémon pass their Adept (Blissey 1.5×,
  Snorlax 0.96×). Proposed instead:

  | Golden Sun stat | Comes from |
  |---|---|
  | HP | Adept HP curve (before the class multiplier) × clamp(0.25 + 0.0025 × base HP, 0.25, 0.80). A balancing check keeps every species at every level below 0.8 of its Adept |
  | Attack | Attack and Special Attack |
  | Defense | Defense and Special Defense |
  | Agility | Speed |
  | Luck | A tier from the base-stat total, **1–8 for Pokémon**. Golden Sun's Luck 40+ blocks several status effects (poison, venom, haunt, instant death and others), so 40+ stays boss-only |

- **Decided, elements:** every Adept and Pokémon has Power and Resist in each of the six element groups. A Pokémon's
  types set its values, and a double weakness gets a small extra penalty.
- **Decided:** Psynergy works as in Golden Sun, with long lists, in and out of battle, and no 4-slot cap. Pokémon
  keep 4 moves.
- **Decided:** Pokémon keep the Pokémon-style level-up and evolution popup, showing Golden Sun-scale stats.
  - **Proposed:** it shows HP, Attack, Defense, Agility and Luck (Pokémon have no PP stat), with a skip / fast
    option.
- **Decided: Adepts' level-ups are shown as in Golden Sun.** After battle, the message window announces the new
  level, then each stat's gain (HP, PP, Attack, Defense, Agility, Luck), then any newly learned Psynergy.
- **Proposed, EXP:**

  | Who | EXP |
  |---|---|
  | Adepts standing at the end | Full total (Golden Sun) |
  | Adepts downed at the end, or who sat out | None |
  | Partners and replacements that acted | Full total |
  | Withdrawn partners | Their one action counts |
  | Unleashed Pokémon | None |
  | The inactive crew | Half, as in GS2, so a handover doesn't bring in an under-levelled crew |

  - Pokémon level on their own Pokémon curves, with Golden Sun enemy EXP scaled to them. Golden Sun's curve reaches
    8M at Lv 99; Pokémon's tops out around 1–1.6M. The scale factor is left to balancing.
  - **To do:** check that GS's reward routine (`FUN_081284c0`) skips downed members.
- **Proposed, flee and encounter rate:** only Adept levels count in the party-level averages these formulas use.
- **Proposed, after a battle:** EXP, then level-up popups, then move learning, then evolutions, then class
  recalculation (evolution can change types), then Standby reset.

## 6. Battle pacing

**Decided:** partners get an optional tactics setting (Auto, or a default action per partner), plus "repeat last
turn" and fast animations. Partners can still be commanded by hand.

**Proposed:** enemy HP, action counts or group sizes get rescaled for 8 player fighters. Golden Sun's numbers assume
4.

## 7. Field Psynergy and water moves per crew (proposed)

Field Psynergy works for the active crew only (decided). With full crews, each crew lacks two element groups.
Early on, while a crew is still being recruited (§1), it lacks more: the hero alone has only Earth.

| Group Psynergy | Crew 1 (Earth, Sea, Forest, Shadow) | Crew 2 (Earth, Sea, Flame, Sky) | Golden Sun item backup |
|---|---|---|---|
| Move, Pound, Tremor, Scoop (Earth) | ✓ | ✓ | Pound Cube, Tremor Bit, Scoop Gem |
| Frost, Douse, Ply (Sea) | ✓ | ✓ | Frost Jewel, Douse Drop |
| Growth, Lash, Catch (Forest) | ✓ | — | Lash Pebble, Catch Beads; **none for Growth** |
| Reveal, Cloak, Halt, Avoid (Shadow) | ✓ | — | Cloak Ball, Halt Gem, Repel (Avoid); **none for Reveal** |
| Blaze, Burst, Force, Parch (Flame) | — | ✓ | Burst Brooch, Orb of Force; **none for Blaze, Parch** |
| Whirlwind, Cyclone, Mind Read, Teleport, Retreat (Sky) | — | ✓ | Cyclone Chip, Teleport Lapis, Escape Rope (Retreat); **none for Whirlwind, Mind Read** |

**Proposed:**
- **New backup items** for Growth, Reveal, Blaze, Parch, Whirlwind and Mind Read. That completes DESIGN.md's rule
  that no puzzle requires one specific Adept.
- **Psynergy items** are key items in the shared bag, usable by any active Adept. In Golden Sun only the holder can
  use them, which would lock an item away in the other crew.
- **Area design:** each crew's chapters use only Psynergy that crew has at that point in the story, or that its
  backup items provide. Each recruitment mission is a natural place to hand out a backup item or to show off the new
  Adept's Psynergy.
- **Water moves:** "the party" means the active crew. Surf, Dive and Waterfall work if any of the crew's Set Pokémon
  can learn them. A restoration point **won't unset the last Set Pokémon that can learn an unlocked water move**,
  and each handover guarantees the incoming crew has them, so no one gets stranded on an island or underwater.

## 8. Catching (proposed)

- **Throwing:** a ball can target any one catchable Pokémon, however many enemies are left. Adepts throw, as an item
  action; partners can't (see the item rule in §3).
- **After a catch:** the caught Pokémon leaves the field and the battle goes on. Catching gives EXP, as in Pokémon
  from Gen 6.
- **Storage:** caught Pokémon, and Pokémon that join through Djinn-style encounters, go to the shared storage with a
  "sent to storage" message. They can be Set at the next restoration point.

## 9. What changes in the earlier plans

- **Battle sizing:** `docs/phase1/BATTLE_FORMAT.md` sized a GBA engine with 1 + 1 per side.
  - Dropped: in-battle Adept switching with the partner reload (its riskiest stage) and the 8-Adept battle roster.
  - New work: an 8-against-6 battle line, the downed-Adept, revive-window and partner rules, partnerless Adepts,
    the enemy-trainer mirror, two crews in save data and menus, and backup items.
  - The engine is still to be chosen (native app first).
- **World proposal:** its acts need re-cutting around the decided story structure. The game opens with the hero
  alone against the rival, then a mission played as the rival, then recruitment missions for each other Adept;
  crew swapping comes after that. Its "Crew 2's opening is the rival's chapter" idea becomes that early rival
  mission.

## 10. DESIGN.md parts this replaces

| DESIGN.md | Now |
|---|---|
| Platform: GBA ROM hack | Native Android app first (decided 13 Oct) |
| Battle format: 1 Adept + 1 Pokémon per side | 4 Adepts + 4 partners; enemy side capped as in Golden Sun |
| Party: 8 Adepts, one on the field, others swap in | Two crews of 4, built up through story missions; crews change only on the home island, once unlocked |
| Sea's reason: "a second healer for when Adepts swap in and out" | One Sea healer per crew |
| Summon cost: drawn from the whole party | Drawn from the active crew (up to 8) |
| Field Psynergy: the whole party's works | The active crew's works, with backup items for every group Psynergy |
| Water field moves: any Set Pokémon in the party | Any Set Pokémon in the active crew, with the stranding rule in §7 |
| Risk note: 4-fighter battle limit | No longer applies |
| Risk note: party-wide Standby pool across all 8 Adepts | Active crew's pool |
| Build order step 1: 1 Adept + 1 Pokémon battle format | 4 + 4 battle format |

## 11. Still open

1. **Story missions:** written by Claude (your call, 13 Oct) in the story document. Anything there that needs a
   mechanic or changes how the game plays comes back to you as a question.

Settled since the first version: crew composition, Rouse numbers, how Adepts' level-ups are shown, when crew
swapping unlocks, the defeat rule, restoration-point healing, and the three code checks below.

## 12. Confirmed from the game code (14 Oct)

No decisions needed; these were the open checks from the first version, now read from Golden Sun 1's code
(`re/notes/gs_battle_mechanics.md` §13) and taken as the rules.

- **Enemy cap:** at most 6 enemy slots. A formation names up to 5 enemy types with minimum and maximum counts; the
  minimums are always placed, extras are rolled while they fit. **Large enemies take 2 slots** (a flag on the
  battle-sprite entry, not the enemy record): in GS1, 43 enemies are 1-slot (vermin, bats, slimes, rats…) and 121 are
  2-slot. Trainer pairs (Adept + Pokémon) take 2 as planned.
- **EXP:** the award goes in full to the members standing at the end with HP above 0. Downed members get nothing.
  Golden Sun 1 also has an "extra reward" mode (bonus EXP and coins, better drop chance) that a battle event can
  switch on; we can use it for story battles.
- **Recovery timing:** countdowns are assigned at the end of the summoner's turn and tick at the end of each round
  (§4).
- **Turn order:** a member's priority is Agility plus a random bonus of up to 6.25%; a second action in the same
  round gets half. Only a few effects jump to the front of the round. We keep the random bonus, so equal-Agility
  fighters don't always act in the same order.
- **Criticals** use the target's level in both games (bonus = level / 5 + 6).

## For DESIGN.md (to paste into the claude.ai project)

| Area | Decision | Source |
|---|---|---|
| Platform | Native Android app (Galaxy Z Fold 7) first | — |
| Party | **Two crews of 4 Adepts** (8 in all): Crew 1 = hero (Earth), Sea, Forest, Shadow; Crew 2 = rival (Earth), Sea, Flame, Sky. The game opens with the hero alone against the rival, then a mission played as the rival; every other Adept has recruitment or story missions. Crew swapping (switching crews, and moving Adepts between them on the home island) unlocks once those missions are done | Golden Sun: The Lost Age, adapted |
| Level-up display | Adepts: Golden Sun-style results text. Pokémon: Pokémon-style popup with Golden Sun-scale stats | Hybrid |
| Battle format | **4 Adepts + 4 partner Pokémon** on your side; the enemy side is capped as in Golden Sun (about 6 slots; trainer pairs take 2) | Hybrid |
| Partners | A Pokémon fights only while its Adept can. A downed Adept's partner gets one action (Rouse or an item) to try to revive them, then withdraws. An Adept downed before battle sits out with their Pokémon. Adepts can fight without Pokémon | New |
| Swapping | No swapping in battle, except replacing a fainted partner; Set Pokémon change only at restoration points | New |
| Restoration points | Pokémon heal free; Adepts pay to heal or revive (priced like Golden Sun's Inns and Sanctums), and a paid Adept heal heals the Pokémon too | Hybrid |
| Defeat | Wake at the last restoration point with everyone restored; lose half your coins | Pokémon |
| Summons | Cost 1–3 Standby Pokémon from the **active crew**; Unleash puts a benched Set Pokémon on Standby | Golden Sun, adapted |
| Field Psynergy | The active crew's Psynergy works; backup items exist for every group Psynergy and live in a shared bag | Golden Sun, adapted |
| Water field moves | Usable if any Set Pokémon in the active crew can learn them | Pokémon / Unbound |
| Enemies | Golden Sun monsters, bosses and bandits are uncatchable; wild Pokémon are catchable; human trainers fight as Adept + Pokémon pairs | Hybrid |
| Damage and stats | Golden Sun's formulas and stat scale for everyone; Adepts have clearly more HP than partners | Golden Sun |
| Psynergy | Golden Sun-style long lists, in and out of battle; no 4-slot cap | Golden Sun |