# Equipment: weapons, armour and other equipables

From the equipment review (15–16 Oct): five areas, each checked by an adversarial verifier, then a synthesis and a
critic, with the critic's corrections applied. Statuses:
- **Built:** engine main (e229fdd) does it.
- **Decided:** a doc records your answer.
- **Proposed:** a recommendation.
- **Open:** undecided or unknown.
- **Golden Sun:** a fact about Golden Sun from its code (the alchemy decomp) or data.

Related: [party-and-battle.md](party-and-battle.md), [items-and-economy.md](items-and-economy.md),
[progression.md](progression.md), [art-integration.md](art-integration.md).

## 1. The short answer

Today the game can't change equipment at all. Each Adept starts with a fixed kit; the engine applies only its
Attack, Defense and the weapon's element; no screen shows or changes gear. Five recruits have no weapon.

**Proposed:**
- Gear works as it does in Golden Sun, with Golden Sun's data and formulas.
- There is a new **Equip** screen with a before-and-after stat preview, a Gear pocket in Items, a paged Status
  screen, and a shop compare.
- Pokémon don't hold items. A few of their effects become rings and charms for Adepts.

## 2. Storage

| Rule | Status |
|---|---|
| Each Adept record holds `equip: {slot: item id}` over 7 slots | Built |
| One bag per crew until mission 10, then one shared bag and purse | Decided (story.md §14 question 4); built |
| Equipping takes one copy out of the bag; the piece it replaces goes back | Proposed |
| Only bag items can be sold or discarded (Golden Sun lets you sell worn gear unless it's flagged 0x02) | Proposed, a deliberate change; recorded in items-and-economy.md §11 |
| Gear travels with its Adept when they change crew | Built (to be written into party-and-battle.md §1) |
| Guests may re-equip from the bag (unlike their Set Pokémon) | Proposed |
| Changing gear: anywhere outside battle | Proposed. Whether Golden Sun lets you equip during battle, and at what cost, is open (not traced) |
| HP and PP when gear changes: a full Adept stays full; otherwise the missing HP and PP stay missing, clamped to the new maximum | Proposed (today, +HP gear on a full Adept would be a free heal) |

## 3. Slots

| Slot | Golden Sun type | GS1 named rows | Typical pieces |
|---|---|---|---|
| Weapon | 1 | 51 | swords, light blades, axes, maces, staffs |
| Body | 2 | 32 | armour, clothing, robes |
| Arm | 3 | 22 | shields, gloves, armlets |
| Head | 4 | 23 | helms, hats, circlets, crowns |
| Boots | 5 | 4 | Hyper, Quick, Fur, Turtle Boots |
| Ring | 8 | 7 | Adept, War, Sleep, Healing, Unicorn, Fairy, Cleric's |
| Shirt | 9 | 3 | Mythril, Silk, Running Shirt |

All seven slots are built. Psynergy items (type 6) aren't gear; they're key items (items-and-economy.md §6). GS2's
class items (type 10) get no slot, because our class comes from Set Pokémon.

## 4. Who can wear what

**Golden Sun.** Each item's equip mask has one bit per character. In GS1 every mask breaks down into a weapon family
and an armour class:

| Family or class | GS1 rows | Golden Sun wearers |
|---|---|---|
| Long sword (the Machete counts here) | 12 | Isaac, Garet |
| Light blade | 12 | Isaac, Garet, Ivan, Jenna |
| Axe | 8 | Isaac, Garet |
| Mace | 8 | Isaac, Garet, Mia |
| Staff | 11 | Ivan, Mia, Jenna |
| Heavy (mail, shields, helms) | 26 | Isaac, Garet |
| Any (clothes, gloves, caps, boots, rings, 2 shirts) | 40 | all |
| Light (robes, armlets, circlets) | 19 | Ivan, Mia, Jenna |
| Dress | 6 | Mia, Jenna |

**Today.** The mask helper is built but nothing calls it, so no limit applies. Each Adept's mask would follow the
Golden Sun curve it borrows, so Corvin and Tamsin share all 106 pieces, and Sorrel and Vesper share every weapon.

**Proposed: equip profiles.**
- `data_src/adepts.json` gets `"equip_profile": {"weapons": [...], "armour": [...]}`, and today's starting kit moves
  to a `"kit"` key.
- The profile doesn't depend on the borrowed curve, so moving Vesper to Mia's curve (progression.md decision 8)
  doesn't change it.
- The exporter writes `family` and `armour_class` on every gear row. Family comes from the icon range, falling back
  to the mask (55 light blade, 44 staff, 27 mace), with the Machete set by hand. Four weapons sit outside the icon
  ranges: the Machete, the Shaman's Rod, the Bandit's Sword and the Zodiac Wand.
- The default profile equals the borrowed Golden Sun character's, so nothing changes until you tune it.
- A `gear_check` tool validates every kit in adepts.json and trainers.json against its profile. Only then may a
  load-time rule move an illegal piece to the bag.
- Adopting a tuned profile changes that Adept's kit in the same step, so nobody loads unarmed.

Suggested tuning (decision 2):

| Adept | Weapons | Armour | Kit change in the same step |
|---|---|---|---|
| Hero | long sword, light blade, axe, mace | heavy, any | none |
| Corvin | long sword, axe | heavy, any | Short Sword → Long Sword |
| Tamsin (monk) | mace, staff | any, light | Short Sword → a mace |
| Maren | mace, staff | any, light, dress | gains a mace |
| Nerissa | light blade, mace | any, light, dress | gains a knife |
| Sorrel | light blade, staff | any, light | gains a staff |
| Vesper | light blade | any, light, dress | gains a knife |
| Wynn | light blade, staff | any, light, dress | gains a staff |

The kits disagree today: Corvin and Tamsin fight their story battles with a Machete (trainers.json) but join with
a Short Sword (adepts.json). Decision 11 settles which is meant.

## 5. What gear does

### 5.1 The order stats are built in

**Golden Sun:**
1. Curve, plus item Attack and Defense, plus flat effects.
2. Times the class multiplier.
3. Rate effects (value ÷ 10).
4. Clamps: Attack, Defense and Agility at 999, Luck at 99, Power and Resist at 200.

**Today:** curve × class, then the gear's Attack and Defense, then the bond share.

**Proposed (decision 3):** Golden Sun's order, with the bond share (proposed 30%, to tune) added last. It goes into
the oracle (`gs_battle.py`) with test vectors first, then into GDScript. A Squire's weapon then gains about 10%, and
a Wind Seer's loses about 20%: a Kusanagi gives 108, as in Golden Sun, instead of 135.

### 5.2 Equipped effects (Golden Sun, item +0x18: four {kind, value} entries)

| Kind | Meaning | GS1 rows | Example |
|---|---|---|---|
| 1, 3 | Max HP +, max PP + | 1, 3 | Mythril Shirt, Psynergy Armor |
| 2, 4 | HP and PP regained each round | 5, 4 | Asura's Armor +8, Thunder Crown +4 |
| 5, 6 | Agility +, Luck + | 6, 2 | Ninja Garb +30, Jeweled Crown +5 |
| 7–14 | × value/10 on HP, HP regen, PP, PP regen, Attack, Defense, Agility, Luck (after the class) | several | Adept's Helm PP ×1.2; Turtle Boots Agility ×0.5 |
| 15–18 | Power: Earth, Sea, Flame, Sky | 7 | Gaia Blade Earth +20 |
| 19–22 | Resist, same order | 14 | Demon Mail Sky −10 |
| 23 | Crit and Weapon Art bonus | 4 | Hyper Boots 12 |
| 25 | Curse ward (stops the lost turns, not the lock) | 1 | Cleric's Ring |
| 27 | More encounters | 1 | Lure Cap |
| 28–31 (ours) | Forest and Shadow Power and Resist | own items | a Forest charm (decision 9) |

43 of GS1's 142 equipables depend on these, and none of them work today.

### 5.3 Weapon Art (Golden Sun's weapon unleash)

**Golden Sun:**
- 29 of GS1's 51 weapons have one.
- The chance is the gear's kind-23 bonus (never below 0) plus 35%.
- On success the Attack becomes the weapon's own ability (for example Titan Blade, +70 Earth), at no PP cost.
- Monsters never use one.

**Proposed:**
- The Adept rolls for the Weapon Art first, then the critical hit.
- The battle line is Golden Sun's: "Rowan's Gaia Blade lets out a howl! Titan Blade!". It never says "unleash",
  which stays the Set Pokémon command.
- The name in menus is decided with items-and-economy.md decision 23.

### 5.4 Curses and locked gear

**Golden Sun:**
- 6 cursed GS1 items: Muramasa, Demon Axe, Wicked Mace, Demonic Staff, Demon Mail, Thunder Crown.
- A cursed piece locks on, and the wearer loses about 1 turn in 4 ("Rowan is bound and cannot move!").
- A Sanctum removes the curse and keeps the item.
- Flag 0x02 blocks removing a piece.

**Proposed:**
- 0x02 counts only together with the curse flag. Otherwise the starting Machete, which carries 0x02, could never be
  swapped.
- Rests offer "Remove curse". The price comes from the decided rule that Adepts pay at restoration points, priced
  like Golden Sun's Inns and Sanctums (party-and-battle.md §1): level × 10 (items-and-economy.md decision 19).
- No cursed item is placed until this is built. Whether curses exist at all is items-and-economy.md decision 21.

### 5.5 Usable gear

**Golden Sun:**
- 16 GS1 pieces can be used: rings, armlets, a few shields, hats, the Blessed Mace and the China Dress.
- Each use from the field has a 1-in-8 chance of breaking the piece.
- Repair costs a quarter of the price.

**Proposed:**
- Usable from the bag or while worn, in the field and in battle. Worn pieces are tagged "E" in the battle Item list.
- Breakage comes later, if kept (items-and-economy.md decision 21). It needs more than a save-version bump:
  - bag entries would be keyed by item *and* broken state, because today's bag keys by item id alone and a
    battle's id-to-count bag would lose the broken state;
  - worn usable gear would go into battle as its own list;
  - the battle round trip, selling and repairing broken copies would each need tests.

### 5.6 Item flags (Golden Sun)

| Bit | Meaning | Our rule |
|---|---|---|
| 0x01 | curses when worn | §5.4 |
| 0x02 | can't be removed | only with 0x01 |
| 0x04 | rare | never shop stock; sold ones go to Artifacts |
| 0x08 | important | can't be sold or discarded |
| 0x10 | stacks | consumables |

The extractor's labels for these and for types 7–11 were fixed in design PR #45 (`re/gbax/codecs/gs_units.py`).

## 6. Pokémon and gear

- **No held items** (items-and-economy.md decision 8; that decision is the one to answer).
- A few Pokémon effects become gear for Adepts:
  - a Leftovers Ring (HP each round);
  - six group charms (Power in Earth, Sea, Flame, Sky, Forest, Shadow);
  - a Scope Lens charm (crit);
  - a Quick Claw charm (Agility).
- Lucky Egg and Amulet Coin are party-wide boosts, not gear. If kept, they'd be Farer's Log reward charms in the Key
  Items pocket.
- **Megas** are decided for the whole Gen 1–7 roster plus 14 Weyard forms (DESIGN.md). Their trigger is
  items-and-economy.md decision 11.
- No evolution needs a held slot: all 20 held-item evolutions have a bag route.
- Bonded partner moves already use the Adept's geared Attack (built). Which stats an unleashed benched Pokémon uses
  belongs to progression.md decision 10.

## 7. Where gear comes from

| Source | What | Status |
|---|---|---|
| Starting and recruit kits | Each recruit arrives with a kit for their join level, weapon included (decision 11). `new_game` reads the hero's kit from adepts.json instead of writing it a second time | Proposed |
| Chests, quests, Farer's Log rewards, Galgamash's sword | After the find message: "Rowan can equip it. Equip now?" | Proposed |
| Battle drops | GS1's 11 gear drops (Bandit's Sword always at L7; the rest 1/64–1/256) | Proposed; owned by items-and-economy.md §10 |
| Shops and Artifacts | Golden Sun's tiers: up to 300 coins in Act I, up to 600 at Marrow Isle | Proposed; items-and-economy.md §11 |
| Forge | GS2's forge at Forgeheart in Act II (20 rows, not yet extracted) | Proposed; items decision 21 |
| Our own items | Forest and Shadow gear, story weapons, in `data_src/own_items.json` | Proposed |

Gear isn't placed until the Equip screen and Gear pocket exist. Today a chest's sword would sit invisible in the bag.

## 8. Screens

All screens are specified in UI units at today's 240×160 base with today's font, and that is the only layout to
build now.
- **Re-layout on fold.** Every screen re-lays out when the phone folds or unfolds, keeping the cursor, scroll
  position, tab and preview (the engine's screen rule).
- **Testing.** Each screen is tested on both Fold views with a 10-character hero name, through the text-fit and
  layout tests the art Phase 1 adds.
- **If you take the art decisions** (480×320, a new font, icons; art-integration.md decisions 1, 6, 7 and 14), the
  rects scale with the UI scale. These screens don't decide any of that.

**Shared frame:**
- **Header** across the top: the screen name, Adept or pocket tabs and coins. It is inset so it clears the touch L
  and R bars.
- **Body:** two columns on the inner screen, three on the wide cover view.
- **Description strip:** the item's Golden Sun text. It stops 64 px short of the right edge, so it never sits under
  the touch A and B buttons.
- **Hint bar:** device glyphs, as text until icon art exists. Its chips can be tapped.
- **Menu mode for the touch overlay:**
  - the stick hides, and A, B, L and R stay;
  - START hides, and an "×" chip in the header closes the menu;
  - positions come from the overlay's own placement function, not constants.
- One `MenuList` draws every list: scrolling, greyed rows, tap, key repeat, and a "highlight changed" signal that
  drives previews.

### 8.1 Equip screen (Start → Equip; also from Status → Gear and Items → Gear)

```
Equip  [ROWAN] MAREN SORREL VESPER          1240c
>WEAPON MACHETE       | ROWAN  LV 5  SQUIRE
 BODY   COTTON SHIRT  | HP      48       48
 ARM    PADDED GLOVES | ATTACK  27  >  35  +8
 HEAD   -             | DEFENSE 14       14
 BOOTS  -             | AGILITY 12       12
 RING   -             | ELEMENT NEUTRAL > EARTH
 SHIRT  -             | WEAPON ART  TITAN BLADE 35%
LIGHT BLADE: USED FOR CHORES
A Equip  B Back  X Info  Y Best  L/R Adept
```

- **Choosing a piece.** A on a slot lists "(Remove)", then the bag pieces that fit the slot and the profile, best
  first. A grey last row says how many others can't be worn.
- **The preview panel** follows the cursor: HP, PP, Attack, Defense, Agility and Luck before and after, the element,
  the Weapon Art and its chance, and "CURSED" in red.
  - When the panel overflows the cover view's height, the effect lines move to Info (X) or a second panel page on
    Left/Right.
- **Cursed pieces.** A cursed piece asks "That's a cursed item. Equip it?" first. A slot holding a cursed piece
  won't open.
- **Info (X)** shows effects, Weapon Art, price and sell value, and who can wear it.
- **Best (Y)** fills each slot with the best non-cursed piece, shows the total change, and asks yes or no.
- **One stat path.** The numbers come from `PartyBuilder.preview(party, adept_id, changes)`, which builds the Adept
  and its bond exactly as a battle does.
- **The active partner** shows as a row with the same preview, since it changes the bond share and the class. You
  can change it here, outside battle, as decided. Today the engine allows that only at restoration points (a bug).
- **Both crews.** On Marrow Isle, at the waiting lead or the muster roll, the tabs show both crews (decision 10).

### 8.2 Items → Gear pocket

- The pockets are from items-and-economy.md §3; L and R switch between them.
- A on a gear row opens: Equip on… / Use / Info / Discard. "Equip on…" replaces Golden Sun's Give, listing the
  crew's Adepts with their deltas, with those who can't wear it greyed out.

### 8.3 Status

```
ROWAN  LV 12  SQUIRE        [STATS] GEAR PSY PKMN
HP 130/130 (BOND +39)  PP 40/40  EXP 1234/345
ATTACK  62 (45+8+9)  | ELEM  LV POW RES
DEFENSE 40 (21+10+9) | EARTH  7 112 122
AGILITY 33           | SEA    1  82  92
LUCK     5           | FLAME / SKY / FOREST / SHADOW
PARTNER TREECKO L11  SHIELD READY
```

- The breakdowns read base + gear + bond.
- There are four pages: Stats, Gear, Psynergy, Pokémon. Left and Right turn pages; L and R change Adept.
- Only Adepts are listed. Today the list includes Pokémon and runs to about 50 lines.

### 8.4 Shop

```
"WHAT'LL IT BE?"                          1240c
>LONG SWORD       200 | [ROWAN]+8 MAREN --
 SHORT SWORD      120 |  SORREL+2 VESPER+2
 WOODEN SHIELD     40 | ROWAN ATK 27 > 35
 HERB              10 | YOU HAVE 1
A Buy  B Back  X Info  L/R Compare
```

- **Choices:** Buy / Sell / Leave. Artifacts and Repair appear when those systems exist.
- **Buying:** rows you can't afford are greyed but still selectable. Stackable items get a quantity box.
- **After buying gear:** "Equip it now?" and a wearer picker. If something was replaced: "Sell your old X for N?".
- **Prices and sell rates** are the items review's.

### 8.5 Rest

- "Remove curse", and "Repair" if breakage is kept.

### 8.6 Battle

| Moment | Line |
|---|---|
| Weapon Art | "Rowan's Gaia Blade / lets out a howl! / Titan Blade!" |
| A turn lost to a curse | "Rowan is bound and / cannot move!" |
| Regen at round end | "Rowan recovers 8 HP." |
| Item command | a scrolling list: bag items, then the actor's usable worn gear tagged "E" |
| A use breaks an item | "The Healing Ring broke!" |

### 8.7 Controls

| Function | Pad (Xbox, Backbone) | Touch |
|---|---|---|
| Move | D-pad and left stick, with key repeat | tap a row: the first tap previews |
| Confirm | A | tap the same row again, or A |
| Back | B | B, or "<" in the header |
| Adept or pocket | LB/RB | tap the tab, or the L and R bars |
| Info | X | "Info" chip |
| Best / Sort / Max | Y | chip |
| Page | Left/Right | tap a column; drag scrolls |
| Close all | Menu (Start) | the "×" chip |
| Yes / No | A / B | tap |

- **Menus consume their input.** On the field, X and Y are the quick wheel and auto-run, so a menu must mark its
  input handled or auto-run would toggle.
- **First tap.** A tap counts as the first (preview) tap after any switch of device, or on a row it didn't itself
  select.
- **Scrolling.** A drag of 4 UI px or more scrolls instead of tapping.
- **Questions.** Menu questions need their own box above the menus: today the dialogue box draws under them, and B
  doesn't answer No.

### 8.8 Look (art pass, last)

- **Now:** the weapon shows by family on the current Golden Sun battle sprite, using Golden Sun's own weapon
  overlays.
- **Later:** an LPC weapon layer, if art decision 3 adopts LPC.
- ~~Armour never shows, so the creator's outfit stays.~~ **Changed by your answer to decision 13 (17 Oct): armour
  layers show too.** Which pieces replace the outfit is [demo-plan.md](demo-plan.md) decision 31.
- Icons follow art decision 14. Until then the screens use text only: names, and coloured +/− for stat changes.

## 9. In code (proposed)

- `Inventory.equip(rec, bag, items, item_id, profile) -> {ok, reason, replaced}`, `unequip`, `candidates_for`,
  `is_key`, `is_locked`.
- `Equipment.mods(rec, items)` returns the flat stats, rates, Power and Resist (7 groups), crit bonus, regen, curse,
  encounter rate, weapon element and Weapon Art. It is used inside `UnitFactory.adept_from_pc` before the class
  multiplier.
- `PartyBuilder.preview(party, adept_id, changes) -> {before, after}`.
- `GsFormulas.unleash_chance`, `crit16` and `recalc_stats`, each with oracle vectors. The oracle's unleash chance clamps a
  negative bonus to 0 since design PR #45.
- `Battle`: a Weapon Art roll in `_attack`, the bound check at turn start, regen at round end, and worn gear as an
  item source. `BattleUnit` serialises `weapon_element` and the new fields.
- `tools/gear_check.gd` validates every kit (slot and profile) in adepts.json and trainers.json.

## 10. Bugs found

**Fixes need no decision:**
- **Gear in the bag is invisible.** A chest or scene that gives gear puts it in the bag, where the Items list never
  shows it and nothing can equip it.
- **`equipment_bonus` accepts anything.** It adds any item in any slot, counts a duplicate weapon twice, and lets a
  weapon in a non-weapon slot set the element.
- **The hero's kit is written twice:** in `new_game` and in adepts.json.
- **The battle command box overflows the screen.** The touch START button also sits inside it. The art Phase 1
  build fixes this.
- **Status and the Items target lists include bonded and benched Pokémon.** A full crew gives about 50 lines.
- **`BattleUnit` drops `weapon_element` when saved to a dictionary.**
- **Two comments are wrong:** the record-shape comment leaves out `equip` and `group`, and `new_crew_state` calls
  the roster kit "Golden Sun's starting kit".
- **Battle, choice and Pokémon menus don't re-lay out on a fold.** The art Phase 1 build fixes this.

**Need a decision:**
- **The starting Machete carries "can't be removed".** Decision 5.
- **Kits disagree.** Corvin and Tamsin wear a Machete in trainers.json but a Short Sword in adepts.json. Decision 11.
- **The active partner can only change at restoration points**, though the decided rule says any time outside
  battle (party-and-battle.md §1). This one is a bug to fix rather than a choice: it gets a field-menu entry with the
  Equip screen's preview.

## 11. Decisions for you

Recommended first. The alternatives are in brackets. Questions the items review already asks are answered there
(held items: items 8; curses, breakage and the forge: items 21; the Weapon Art name: items 23), and are not repeated
here.

Answered on the decision page: accepted items are marked **Decided** with the date, the rest **To talk over**.
1. **Decided (16 Oct):** **How gear is stored and changed.** Recommended: the shared bag plus each Adept's 7 worn slots, as built. An
   Equip entry in the Start menu, also reached from Items and Status, with one stat preview, usable anywhere outside
   battle. [Golden Sun's per-Adept item lists with Give; only at restoration points.]
2. **Decided (16 Oct):** **Who can wear what.** Recommended: equip profiles per Adept, starting equal to today, then the tuning in §4 with
   the kit changes in the same step. [Keep the borrowed Golden Sun masks; no restrictions.]
3. **Decided (16 Oct):** **The order stats are built in.** Recommended: Golden Sun's, with gear before the class multiplier and the bond
   share last. [Today's order: Seers gain up to 25% extra from weapons, and Squires and Guards lose about 9%.]
4. **Decided (16 Oct):** **Weapon Arts.** Recommended: keep them at Golden Sun's 35% plus the gear bonus. [Drop them: 29 weapons lose their
   signature move.]
5. **Decided (16 Oct):** **The starting Machete's lock.** Recommended: honour "can't be removed" only on cursed gear. [Start the hero with
   the Short Sword; honour it everywhere, leaving the hero stuck with the Machete.]
6. **Decided (16 Oct):** **Usable gear.** Recommended: usable from the bag or while worn, now; breakage later if items decision 21 keeps it.
   [Usable and unbreakable for good; not usable.]
7. **Decided (16 Oct):** **Slots.** Recommended: all seven, as built. [Golden Sun's four classic slots first; an eighth class-item slot.]
8. **To talk over:** **Item table.** Recommended: GS1's table for Act I. Switch to GS2's superset later, as its own step. The switch
   touches more than item ids:
   - item rows point into their own game's ability table (Weapon Arts, uses);
   - the description text base changes;
   - the engine hard-codes the GS1 item, ability and class tables;
   - saves already hold GS1 ids.

   [Switch now, before saves spread; hand-pick GS2 pieces into our own items.]
9. **Decided (16 Oct):** **Forest and Shadow gear.** Recommended: our own effect kinds for Forest and Shadow Power and Resist, and a few
   elemental weapons and charms of our own. [Golden Sun's four elements only, so Sorrel and Vesper never get element
   gear.]
10. **Decided (16 Oct):** **Gear across crews and guests.** Recommended:
    - Gear travels with its Adept, as built.
    - Guests may re-equip.
    - On Marrow Isle the Equip screen shows both crews and offers "Hand over gear" to move the waiting crew's gear
      into the bag.

    [Strip gear on every trade; only the active crew can be equipped.]
11. **Decided (16 Oct):** **Recruit kits.** Recommended: each recruit arrives with a kit for their join level, weapon included (Maren a
    mace, Sorrel a staff, Vesper and Nerissa light blades, Wynn a staff). Corvin and Tamsin's story-fight Machete
    becomes their join kit too. [Keep the Cotton Shirt kits and rely on shops and chests.]
12. **Decided (16 Oct):** **Paying for eight Adepts.** Recommended: Golden Sun prices, with recruit kits, chests in each crew's missions,
    and coins from crew 2's story fights. Agree one income figure with items decision 4. [The waiting crew earns
    half coins; halve gear prices; a shared armoury.]
13. **Decided (17 Oct), alternative:** **Does gear show on the sprite?** Recommended: the weapon in battle (Golden Sun's overlays now, LPC later); armour
    never. [Armour layers too; nothing.]
14. **Decided (17 Oct):** **A "Best" button.** Recommended: yes, on Y, with a yes/no check. [None, as in Golden Sun.]
15. **Decided (16 Oct):** **Enemy trainers' gear.** Enemy Adepts mirror ours (decided) and wear kits through the same build. Recommended:
    they get gear stats, effects and regen, but no Weapon Arts or curses at first; Golden Sun's monsters never use
    Weapon Arts. [Everything ours has; stats only.]
