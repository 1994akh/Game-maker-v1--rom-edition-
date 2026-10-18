# Items and economy

From the items review (15–16 Oct): six areas, each checked by an adversarial verifier, then a synthesis and a
critic. Statuses: **Decided** means a doc records your answer; **Built** means engine main (e229fdd) does it;
**Proposed** is a recommendation; **Open** means nobody has decided it. It folds together the item rules spread
across DESIGN.md, party-and-battle.md, field-abilities.md, story.md, [progression.md](progression.md) and
[art-integration.md](art-integration.md). Where they disagree, it says so.

## 1. Principles (proposed)

1. **One coin scale: Golden Sun's.** A Herb costs 10, a Long Sword 200 and a Great Sword 7,000. Our own items are
   priced to fit. Income already uses this scale: Golden Sun monster coins, and level × 2 for wild Pokémon.
2. **Golden Sun items for Adepts.** Bonded partners are never hurt (party-and-battle.md §3, decided). So every heal,
   cure, buff and piece of gear targets an Adept, where Golden Sun's items already balance.
3. **Our own items only where Pokémon or the story need them:** balls, Escape Rope, Repel, evolution items, Mega
   items, new backup Psynergy items, and key and quest items.
4. **No Pokémon item system that needs a mechanic we don't have.** Held items, EVs, natures, abilities,
   friendship, gender, day and night, and fishing stay out unless a decision brings one back.
5. **Function first.** No item goes in a shop or a drop table until its effect works.

## 2. Item families

| Family | Source and price | What it does | Status |
|---|---|---|---|
| Healing | Golden Sun: Herb 10 (50 HP), Corn 12 (100), Nut 200 (200), Vial 500 (500), Potion (full; rare, loot only) | Heal one Adept | Built |
| PP | Golden Sun: Psy Crystal (rare, loot or prize only) | Restore all PP | Built |
| Revival | Golden Sun: Water of Life (rare, loot only). Optional own Revive (60%, about 800) | An Adept uses it on a downed ally, or a bonded partner uses it on its own Adept in the revive window | Built (Water of Life) |
| Cures | Golden Sun: Antidote 20 (poison, venom), Elixir 30 (stun, sleep, delusion, seal) | Cure | Built in battle; field use proposed (§7) |
| Battle items | Golden Sun: Smoke Bomb 30, Sleep Bomb 60, Oil Drop 30, Weasel's Claw 40, Bramble Seed 50, Crystal Powder 60 | Status or elemental damage on foes | Broken today (§14) |
| Stat foods | Golden Sun: Power Bread, Cookie, Apple, Hard Nut, Mint, Lucky Pepper (rare, loot or prize only) | Permanently raise one Adept stat | Inert today |
| Field consumables | Own: Escape Rope, Repel. Golden Sun: Sacred Feather (loot) | Retreat or Avoid | Decided to exist; form open (decision 13) |
| Psynergy items | Golden Sun 1 200–207, Golden Sun 2 198–217, our own backups | Grant a field Psynergy to any Adept | Concept decided; the gate is broken (§14) |
| Balls | Own (9001+) | Catch | Built: Poké and Great only |
| Evolution items | Own: 10 stones, Linking Cord, 17 former held items | Used from the bag on a Pokémon | Proposed (§9) |
| Mega items | Own: Mega Ring and Mega Stones; the Red Orb (story) | Mega Evolution | Megas decided; trigger open |
| Gear | Golden Sun weapons, armour, arm, helm, boots, rings, shirts | Equipped on Adepts | Built: Attack, Defense, element only. The equipment review owns the rest |
| Treasures | Golden Sun Lucky Medal and Game Ticket; optional own Nugget, Pearl, Star Piece | Sell, or spend at the Glimmer Saucer | Proposed |
| Key and quest items | The Lodestar (built, 9003); flag-backed story objects; Well relics; quest objects | Story | §5 |

"Rare" rows (Golden Sun flag 0x04) are never normal shop stock (§11). They come from loot, drops, artifacts or the
prize counter.

**Cut:**
- all Pokémon medicine (Golden Sun's items cover it, and the names Potion and Elixir would clash);
- vitamins, feathers, Mints and Ability Capsules;
- berries, gems, plates, incenses, Choice items, weather items;
- Z-Crystals and Dynamax items (Z and Dynamax are decided out, DESIGN.md);
- Rare Candy, Apricorns, Mail, contest items, bikes and the PC items.

**Optional later:**
- Exp. Candy for one Pokémon (a fixed EXP grant to that record alone; `award_exp` would split it);
- charms as Farer's Log rewards;
- fossils with a reviver at the Marrow Isle library.

## 3. Bag rules

| Rule | Value | Status |
|---|---|---|
| Ownership | One bag and purse per crew until mission 10, then one shared bag. Pokémon storage is always shared | Decided (story.md); built |
| Slots | Unlimited | Built |
| Stack cap | 99 per item (Golden Sun used 30) | Proposed; built has none |
| Pockets | Items, Battle, Balls, Gear, Psynergy items, Key Items | Proposed |
| Key protection | Golden Sun flag 0x08, `key: true` or type 6 can't be sold, discarded or given | Proposed; the Lodestar needs flag 8 |
| Who uses items in battle | Adepts on their turn; a bonded partner only in its revive window, and only a reviving item | Decided; built |
| Descriptions | Golden Sun 1 text id 117 + item id; Golden Sun 2 146 + item id; our own rows carry text | Proposed |

## 4. Item ids (proposed)

| Range | Use |
|---|---|
| 0–515 | Golden Sun. GS2's table becomes the base once exported; 180 of GS1's 191 items share ids and values |
| 9001–9099 | Balls and field consumables (9001 Poké Ball and 9002 Great Ball keep their ids) |
| 9100–9199 | Evolution items. Each row carries `evo_item`, the slug the species data uses (`fire_stone`, `linking_cord`) |
| 9200–9299 | Mega Ring and Mega Stones (each names its species) |
| 9300–9399 | New backup Psynergy items (key `grants`: a field ability id) |
| 9400–9499 | Key and quest items (9003 Lodestar keeps its id) |
| 9500–9599 | Treasures and prize items |

Our own rows move from `PartyBuilder.OWN_ITEMS` into `data_src/own_items.json`.

## 5. Key items (proposed)

- **Real bag items only for things you use:** the Lodestar (the compass from mission 12, decided), Psynergy items,
  balls, the Mega Ring, Mega Stones and evolution items.
- **Story objects stay flags.** `data_src/key_items.json` (`{id, name, text, shown_when, gone_when}`) shows them in a
  Key Items pocket while you hold them. You can't sell or lose them, and no gate or save changes.

| Object | Shown when | Gone when |
|---|---|---|
| Corvin's note | m6_note | never (filed in the Farer's Log) |
| Jail key ring | m7_key | m7_cell_open |
| Wynn's debt note and chart | m8_heist | never |
| Ledger of the Crown | m9_ledger | never |
| Well relics, one per opened Well | well_* | used at the Beacon |
| Quest objects (violin, flute, real sword, Wooloo food, feast food) | quest flag | quest done |

Ship states (Kestrel, Wayfarer, Well upgrades) go on a ship page, not in the bag. The Lodestar's giver mismatch
(story.md says Brann's heirloom; the build has Ilse give it) is for the story pass.

## 6. Item Psynergy and backups

**Decided:**
- Items grant a Psynergy anyone can use, as progression keys and as backups.
- Lift, Carry, Hover, Grind and Sand are item-only.
- Psynergy costs the casting Adept's PP.

DESIGN.md says backups exist for every group Psynergy, while party-and-battle.md §7 still calls that proposed.

**Proposed:**
- Psynergy items are key items in the bag (one per crew until mission 10, then shared); any Adept in the active crew can use one and pays the normal PP.
  Today field PP always comes from the lead (a bug, §14).
- A crew's field verbs are its group Psynergy, plus HMs (flag plus a Set Pokémon that learns it), plus the verbs
  its bag's items grant.
- Crew 2's verbs (Blaze, Whirlwind, Mind Read) and the Sky and Flame backups reach Crew 1 only from mission 10.
  This keeps story.md's rule that Crew 2's verbs guard optional rewards in Act I.

| Verb | Missing from | Backup item | Source | Placed |
|---|---|---|---|---|
| Lift (item-only) | everyone | Lifting Gem | GS1 203 | m15 Ironfist Arena (decided) |
| Carry (item-only) | everyone | Carry Stone | GS1 206 | open (suggest m15) |
| Hover (item-only) | everyone | Hover Jade | GS2 215 | open |
| Grind (item-only) | everyone | Grindstone (any Adept) | GS2 214 | open |
| Sand (item-only) | everyone | new: Dune Glass | own | open |
| Reveal | Crew 2 | new: Truth Lens | own | m20 Gloam Shore (decided) |
| Growth | Crew 2 | new: Sprout Seed | own | open |
| Lash, Catch | Crew 2 | Lash Pebble, Catch Beads | GS2 198, GS1 207 | open |
| Cloak, Halt | Crew 2 | Cloak Ball, Halt Gem | GS1 205, 204 | open |
| Avoid | Crew 2 | Repel | own | shops |
| Blaze, Parch | Crew 1 | new: Ember Flint, Dry Wind Charm | own | open, from m10 |
| Force, Burst | Crew 1 | Orb of Force, Burst Brooch | GS1 200, GS2 213 | open |
| Whirlwind, Mind Read | Crew 1 | new: Gust Fan, Thought Glass | own | open, from m10 |
| Cyclone, Teleport | Crew 1 | Cyclone Chip, Teleport Lapis | GS2 210, 217 | open |
| Retreat | Crew 1 | Escape Rope | own | shops |
| Pound, Tremor, Scoop, Frost, Douse | none | Pound Cube, Tremor Bit, Scoop Gem, Frost Jewel, Douse Drop | GS | optional loot |

The new names are placeholders. Where they are placed (missions, recruitments, bounty rewards) goes to the cloud
chat for story.md §7. New rows go in `data_src/field_abilities_hm.json`, the exporter's overlay, never in the
generated `data/field_abilities.json`.

## 7. Consumables, buffs and permanent boosts (proposed)

- **One item resolver.** An item uses its ability row the way Psynergy does:
  - the target side comes from the ability's target (none, foes, allies, self);
  - damage types resolve with `from_item`, and every effect goes through the battle's effect path;
  - menus respect "usable in battle" and "usable from menu";
  - an item whose effect isn't built is hidden, never used up.
- **Battle items:** Smoke Bomb (delusion), Sleep Bomb (sleep), and the four elemental attack items. With catching,
  Sleep Bomb becomes a catch tool.
- **No Pokémon X items.** Buffs come from Psynergy and gear casts (War Ring: Impact; Sleep Ring: Sleep), with the
  equipment review.
- **Stat foods** add to `rec.boosts` on an Adept record, applied after curve stats. The exact gain is read from
  Golden Sun's code before porting. Adepts only.
- **Statuses out of battle:** poison and venom carry over after battle until an Antidote or a rest clears them;
  other statuses end with the battle. Open: whether field poison hurts per step (Golden Sun's code decides), and how
  the field menu shows it. The status also has to go into save records.
- **Run command** for wild and monster battles, using Golden Sun's flee formula on Adept levels. It is blocked in
  story and trainer fights. See progression.md decision 2.

## 8. Catching and befriending

**Decided:**
- Poké Balls catch most Pokémon; Djinn-style Kin need no ball.
- All six legendaries are catchable, each in its own style:
  - one classically;
  - one after a story point;
  - one by puzzle;
  - one at the end of its arc.
- A legendary caught mid-game is Set-only until Act III.
- Legendaries join at the level of the area where they're caught (story.md §14 Q9).
- A guest's Set Pokémon can't be changed (§14 Q3).

| Ball | Price | Rule | When |
|---|---|---|---|
| Poké Ball (9001) | 30 | ×1.0 | Brann gives 5 with the first partner; 2–3 in Act I chests; Stonehollow stall and Canalport |
| Great Ball (9002) | 100 | ×1.5 | Canalport after m6; the Bazaar |
| Ultra Ball | 300 | ×2.0 | Act II shops |
| Farer Ball | not sold | always catches | 1–3 story or postgame rewards |
| Later, optional: Net, Nest, Dive, Quick, Timer, Level, Fast, Heavy, Dream, Moon | 250 | the expansion's rules; each reads data we have | Act II specialty shops |

**Proposed rules:**
- The Catch command is renamed **Ball** and opens a ball list with counts. Today it always throws the first ball.
- Status bonus on the catch: sleep ×2.5; stun, poison, venom and delusion ×1.5 (Unbound's formula).
- The caught record keeps its ball.
- Legendaries:
  - Lugia joins on its return, with no fight.
  - Celebi is a gift after its puzzle.
  - Groudon rests in the Vault and is caught in the postgame (story.md).
  - Rayquaza and Giratina are wild, caught with the Farer Ball or a calmed catch-rate floor. At catch rate 3 they
    are 2% per Ultra Ball at 1 HP.
  - Ho-Oh is open (decision 25).
- **Befriending:** no food or berry system. Kin are won with field verbs and their backup items: Halt freezes a
  runner, Cloak lets you approach, Reveal shows a hidden one.

## 9. Evolution and Mega items

The evolution rules are in [progression.md](progression.md) §4. Today the resolver is `PartyBuilder.evolve()` in
`src/battle/party_builder.gd`; `src/battle/evolution.gd` is progression.md §4's proposed home. This section covers the
items.

- **Used from the bag** on a Pokémon (Pokémon menu and Kin Garden): the 28 Gen 1–7 items. These are the Fire,
  Water, Thunder, Leaf, Ice, Sun, Moon, Shiny, Dusk and Dawn Stones, the Linking Cord, and the former held items
  (King's Rock, Metal Coat, Dragon Scale, Upgrade, Dubious Disc, Protector, Electirizer, Magmarizer, Reaper Cloth,
  Deep Sea Tooth and Scale, Prism Scale, Oval Stone, Razor Fang and Claw, Sachet, Whipped Dream). An item is used
  up only when the evolution happens.
- **The Linking Cord replaces every trade**, Karrablast and Shelmet included.
- **Story partners with a non-level step:**

| Partner | Step | Route (proposed) |
|---|---|---|
| Maren's Eevee | → Sylveon | Shiny Stone, a gift in her arc (progression.md: Sun → Espeon, Moon → Umbreon, Shiny → Sylveon; Water, Thunder and Fire as in Unbound) |
| Tamsin's Riolu | → Lucario | Friendship as a fixed level: 20 |
| Vesper's Haunter | → Gengar | Linking Cord |
| Wynn's Ralts line | Kirlia → Gardevoir (level 30) or Gallade | Gallade by Dawn Stone, the player's choice (story.md) |

- **Prices:** stones 1,200, the Linking Cord 1,500, other trade items 1,200, sold from Act II. Story or bounty gifts
  come earlier: Maren's Shiny Stone, Wynn's Dawn Stone and Vesper's Linking Cord.
- **Mega (trigger open, decision 11).** The recommendation is the Mega Ring as a story key item, and each Mega Stone
  as a key item assigned to one Pokémon.
  - Once per battle per side, the Adept Mega-evolves its bonded partner. The bond share is recomputed from the
    Mega form, and the class stays locked.
  - Enemies mirror it (Hask's Mega Garchomp, m18).
  - The engine needs two things:
    - a new battle command kind, since Golden Sun battles have no free action;
    - a way to show the partner, since today a bonded partner is hidden and a Mega would be only a stat change.

    It ties to art-integration decision 13 (show the unleashed Pokémon) and needs the form-change tables
    exported. The 14 Weyard Megas and the Red Orb come first.

## 10. Drops

| Source | Rule | Status |
|---|---|---|
| Golden Sun monsters | Their own drop item, dropped if rand16 < 0x20000 >> rate code. Up to 4 spoils a battle | Decided (party-and-battle.md); not built |
| Story monsters and bosses | Drop item and rate set by hand in trainers.json. Without that, the Sluice Beast would always drop Kraken's 3,000-coin Water of Life | Proposed |
| Extra reward | Rate code − 2 (4× odds) plus Golden Sun's coin bonus | Proposed; trigger open (decision 5) |
| Wild Pokémon | Coins level × 2 (built). Held items only if they exist in our table, or as sellable treasures | Open (decision 5) |
| Trainers | Coins and EXP per Adept beaten, as trainers.json says. The build also pays for every enemy partner unit | Open (decision 20) |
| Ally assists at the Pinnacle | "An item drop" (story.md §14 Q11) | Decided; not built |

With drops built, Act I gives about 0.08 items a battle (Greenwild: Antidote, Elixir, Smoke Bomb; Lantern Reef:
Herb). A lost story fight rolls back the party, bag and coins (CHANGELOG, 15 Oct), so drops and items spent in it
are rolled back too.

## 11. Shops, selling and artifacts

**Decided:** Marrow Isle grows shops. Bounties never raise prices.

Counters (Golden Sun): Buy, Sell, Artifacts, and Repair (which comes with breakable gear).

**Golden Sun's rules** (proposed; verified in its shop code):
- Buy at list price. Sell at 3/4, or 1/2 for a broken item. Repair costs 1/4.
- These can't be sold: key items (flag 8), story, quest and backup items, price-0 items, casino tokens, bounty
  cargo and Pokémon.
- **Worn gear can't be sold (proposed, our change).** Golden Sun refuses only gear that is both worn and flagged
  0x02, but here only bag items can be sold ([equipment.md](equipment.md) §2).
- Rare items (flag 4) are never normal stock. Selling one adds it to a global Artifacts list. Any shop of the
  matching type sells it back at list price (weapons / armour, boots and shirts / items and rings), and Marrow
  Isle's smith shows the whole list.
- A free Game Ticket after 300, 500, 1,000, 2,000, 4,000 and 8,000 coins spent, for the Glimmer Saucer.

**Shops by place (proposed).** Bags and purses are per crew until mission 10, so the "Crew" column says who can shop
there in Act I.

| Place | Opens | Crew before m10 | Stock | Notes |
|---|---|---|---|---|
| Stonehollow stall (Brann's hatchery) | m1 | 1 | Herb, Antidote, Poké Ball | Becomes Marrow Isle's general store at m10 |
| Fallhaven | m2 | 2 | Herb, Antidote, Elixir, Travel Vest, Leather Cap, Wooden Shield | Lost at m9; the keeper reopens on Marrow Isle |
| Canalport | m3 | 1 | Tier 1 weapons and armour (Wooden Stick 40 to Battle Axe 280; Cotton Shirt to Open Helm 180); Herb, Nut, Antidote, Elixir, Poké Ball, Escape Rope, Repel; Great Ball after m6 | Floods at the Breaking (m11): shops move to the upper town, and the drowned lower town becomes Dive loot |
| Eldergrove apothecary | m5 | 1 | Herb, Corn, Nut, Antidote, Elixir | Forest culture: no balls, no weapons |
| Tradewind Bazaar | m8 | 2 (all crews in Act II) | Tier 2 (Hunter's Sword 520, Bronze Shield 500, Bronze Helm 600…), Vial, Great Ball, Artifacts, a treasure buyer | No Pokémon for sale |
| Marrow Isle | m10 on | both | A stall per rescued keeper: general store, smith (gear plus all artifacts), apothecary, daycare, ship cosmetics, Kin Garden decor | Rows gated by flags |
| Ironfist Arena | m15 | — | Tier 3 battle gear; the Glimmer Saucer prize counter (tickets and Lucky Medals for artifacts, Psy Crystals, stones, Exp. Candy) | The casino is decided |
| Coralreach / Pearlhollow | m16 | — | Dive, Net and Nest Balls, Water Stone; buys pearls | |
| Forgeheart smith | Act II | — | Forge (GS2's table), Repair, appraisal of Rusty weapons | After Tamsin's heart quest |
| Dustplain, Frostmarch, Hushwater, Twin Bells | Act I | — | Open: a stock or "no shop" line each, matching its culture. Hushwater fears Pokémon and treats Psynergy healing as taboo | For the story pass |
| Later towns | Acts II–III | — | Golden Sun's tier ladder | |

Stock ladder: Act I uses Golden Sun 1's Vale-to-Bilibin rows (up to about 600), Act II Xian to Tolbi (1,200–7,000)
plus GS2 basics, and Act III the top GS2 rows. Shops live in `data_src/shops.json`.

Shop screens need more than today's choice list: a quantity picker, the coin total, and Golden Sun's "who can
equip" and stat-change comparison (from the equipment review).

## 12. Coin economy

| Direction | Flow | Value | Status |
|---|---|---|---|
| In | Golden Sun monsters | Their coin field (Act I: 3–40) | Built |
| In | Wild Pokémon | level × 2 (proposal: × 4) | Built |
| In | Story trainers | per Adept (Corvin 30, Tamsin 40) | Built, plus partner units (a bug) |
| In | Bounties | k × the area's mean coins per battle (Bronze 4, Silver 6, Gold 8, Legend 12); named bounties 10–15× plus an artifact. Bounties start at m8 | Bounties decided; formula proposed |
| In | Quest pay, coin chests, selling | | Proposed |
| Out | Rest | Only Adepts below full. A per-room price on Golden Sun's inn ladder (2 up to 25 per Adept, rising outward); revival extra level × 20; curse removal level × 10 | Decided "like Golden Sun's Inns and Sanctums"; built: a flat 6 |
| Out | Shops, forge, repair, rumour broker, daycare, cosmetics, tickets | | Proposed |
| Out | Defeat | half your coins | Decided; built |
| Out | Fees (Vesper 50) | | Built |

**Act I income.** Today Act I pays about 490 coins merged, while a basic gear refresh for eight Adepts costs about
5,740. The proposal to close the gap:
- encounters in the story dungeon rooms (rate 25–35);
- one gear chest per dungeon;
- quest coin rewards;
- bounties from m8.

The target is about 2,800 per crew by mission 10.

Crew 2's Act I is four short interludes and earns about 48 coins today. So either it gets its own, lower target
(interlude fights, the heist purse, the Bastion locker), or it buys almost nothing before the merge. This is the
same change as progression.md decisions 3 and 4 (more encounter tables, gating the world-map warp), tuned once for
EXP and coins together.

## 13. Placement density (proposed)

| Room | Chests | Gating |
|---|---|---|
| Town | 1–2 plus a "glint" search spot | one behind Psynergy |
| Dungeon room | 2–3 | one behind the crew's newest verb, one behind a later verb |
| Dungeon | 1 gear or artifact chest | the next tier-1 piece or an artifact (Magic Rod, Turtle Boots, Bandit's Sword) |
| Region | 1 Reveal cache, 1 Scoop dig spot | |

Act I suggestions:
- Long Sword in vault_halls, Travel Vest in sea_caves.
- Elixir ×2 and Great Ball ×2 in Canalport.
- Leather Gloves and Turtle Boots in the Greenwild, a Circlet in eldergrove_heart.
- Travel Robe and Magic Rod in Lantern Reef.
- A confiscated-gear locker in the Bastion, the heist purse at the Bazaar, and a Farer cache on the Wayfarer.
- 2–3 Poké Balls across Act I.

## 14. Bugs found (fixes need no decision unless marked)

- **Item Psynergy can never work.** The crew's item list holds bag item ids, but the field check looks for ability
  ids, so a Lifting Gem would grant nothing. The Scoop and Burst rows also lack their ability ids.
- **Battle items target your own side** and do nothing, but are used up (Smoke Bomb, Sleep Bomb, the attack items).
  Until the item resolver exists, they should be hidden.
- **Items whose effect isn't built are listed and used up** (stat foods, Sacred Feather, Elixir and Antidote in the
  field).
- **Water of Life can be spent on a standing ally** in battle.
- **The field Items menu offers bonded and benched Pokémon as targets**, though partners are always at full HP.
- **Catch always throws the first ball**, so a Great Ball is never chosen while Poké Balls remain.
- **Rests charge Adepts already at full health.**
- **Trainer fights pay for every enemy partner unit** (Corvin pays 36, not 30). Decision 20.
- **Latent:** the Sluice Beast would inherit Kraken's always-drop Water of Life once drops exist.
- **Chests don't check their item id** and default to item 0, so a typo puts a phantom item in the bag.
- **The Lodestar isn't flagged as a key item**, so a sell rule would allow selling it.
- **Field Psynergy PP is always charged to the lead**, while the decided rule says the caster pays.
- **A caught Pokémon always goes to the lead's Set.** Decision 6.
- ~~The extractor mislabels Golden Sun item types and flags~~ **Fixed in design PR #45** (`re/gbax/codecs/gs_units.py`): 7
  special, 8 ring, 9 shirt, 10 class item, 11 carried key item; flags 0x01 cursed, 0x02 locked when equipped,
  0x04 rare, 0x08 important, 0x10 stackable.
- **The Golden Sun world-map placeholder is reachable from mission 1**, with fights of L12–22 paying up to 243
  coins. progression.md decision 4.

## 15. Icons

[art-integration.md](art-integration.md) decision 14 recommends DCSS 32-px icons mapped per item, plus drawn ones for
Herb, Nut, Mint and the balls. The alternatives are Golden Sun's own icon sheet (every row has an `icon` index;
nothing is exported yet) and the expansion's ball graphics for our own items. Each item row gets an `icon` key that
the bag, shop and drop page read.

## 16. Decisions for you

Recommended first. The alternatives are in brackets.

Answered on the decision page: accepted items are marked **Decided** with the date, the rest **To talk over**.
1. **Decided (17 Oct):** **Coin scale and ball prices.** Recommended:
   - Golden Sun's scale for everything: Poké Ball 30, Great 100, Ultra 300, specialty balls 250, Escape Rope 50,
     Repel 40, stones 1,200.
   - Brann gives 5 balls with the first partner.

   [Keep Pokémon's 200/600 and multiply Golden Sun coins about 10×; or keep 200/600 and make balls mostly gifts.] At
   200, one catch costs 6–12 Greenwild battles.
2. **Decided (16 Oct):** **Shops in Act I.** Recommended: a Stonehollow stall (m1), Fallhaven (m2), Canalport (m3), an Eldergrove
   apothecary (m5) and the Bazaar (m8), then Marrow Isle from m10. [No shops until m10; Marrow Isle only.]
3. **Decided (16 Oct):** **Selling and artifacts.** Recommended: Golden Sun's rules (sell at 3/4, repair at 1/4, sold rare items go to a
   global Artifacts list you can buy back). [Pokémon's 1/2 with no buy-back; per-shop artifact lists.]
4. **Decided (16 Oct):** **Act I income.** Recommended: dungeon encounters, one gear chest per dungeon, quest coins, and bounties from m8,
   aiming at about 2,800 per crew. Crew 2 gets its own lower target. Tuned together with progression.md decisions
   3 and 4. [Encounters only; chests only; cheaper gear.]
5. **Decided (16 Oct):** **Extra reward and wild drops.** Recommended:
   - 4× drop odds and bonus coins for story fights, alphas and bounty targets, and when a Summon or the partner's
     Pokémon move lands the finishing blow.
   - Wild Pokémon: coins level × 4, plus held items mapped to our table (50% / 5% on a catch, 1/16 / 1/128 on a
     defeat).

   [Story fights only; never. Wild: keep × 2 with no drops.]
6. **Decided (16 Oct):** **Catch EXP and where the catch goes.** Recommended: the same EXP as a defeat, no coins. The catch goes to the
   Kin Garden and can join a Set at the next restoration point, which keeps the decided "Set Pokémon change only at
   restoration points". [The thrower's Set if it has an empty slot, which amends that rule (filling an empty slot
   isn't a swap); or as built, the lead's Set.] Never a guest's Set.
7. **Decided (17 Oct):** **Ball roster.** Recommended: Poké, Great and Ultra in shops, plus a rare Farer Ball (always catches); the
   specialty balls later. [The full expansion set; Poké, Great, Ultra and Master only.]
8. **Decided (16 Oct):** **Held items.** Recommended: none. Held evolution items become bag items, and about six effects (type boost,
   Leftovers, Lucky Egg, Amulet Coin, Quick Claw, Scope Lens) can become Adept rings or charms (equipment review).
   [One held slot per Set Pokémon that affects its Adept.]
9. **Decided (16 Oct):** **Permanent stat items.** Recommended: Golden Sun's six stat foods, on Adepts only, with an optional Exp. Candy
   for Pokémon. [Foods on Pokémon too; Pokémon vitamins.]
10. **Decided (17 Oct):** **Evolution items.** Recommended: the 28 items used from the bag, the Linking Cord for every trade, and the
    story routes in §9. Friendship and Eevee follow progression.md §4. [Every evolution by level; evolution
    through an NPC.]
11. **Decided (16 Oct):** **Mega trigger.** Recommended: the Mega Ring plus a Mega Stone per Pokémon (key items), once per battle per side,
    and the bond share recomputed from the Mega form. It needs a new battle command and a visible partner (art
    decision 13). [A Summon-like Mega spending Standby Pokémon; enemy bosses only.]
12. **Decided (16 Oct):** **TMs.** Recommended: not now. If progression decision 11 stores four moves per Pokémon, a move tutor at the
    Marrow Isle library becomes possible. [Unbound's 120 TMs with a forget-move screen.]
13. **Decided (16 Oct):** **Escape Rope and Repel.** DESIGN.md says they stay as backups "following the same rule as item Psynergy". That
    reads two ways:
    - **Recommended:** a one-use rope (50) sharing Retreat's effect, and a Repel (40, 200 steps) sharing Avoid's.
      The Sacred Feather stays as loot.
    - **Alternative:** a reusable key-item rope and repel, like the other backup items.

    Crew 1 has no Sky Adept, so the rope is its only retreat.
14. **Decided (16 Oct):** **Key items pocket.** Recommended: yes, flag-backed entries with readable text. [Real bag items with "take item"
    script steps; hidden flags only, as today.]
15. **Decided (16 Oct):** **Backup Psynergy items.** Recommended: Golden Sun's own items where they exist, and our own gems or charms for
    Growth, Reveal, Blaze, Parch, Whirlwind, Mind Read and Sand. Crew 2-only backups reach Crew 1 from m10, and the
    cloud chat places them in story.md §7. [All as bounty rewards; drop backups for verbs no crew needs.]
16. **Decided (16 Oct):** **PP for item Psynergy.** Recommended: the normal PP of the Adept who uses it, which confirms the decided rule.
    [Free like HMs; a flat 1 PP.]
17. **Decided (16 Oct):** **Stack cap and pockets.** Recommended: 99 per stack, with the six pockets. [Golden Sun's 30; no cap.]
18. **Decided (17 Oct):** **Bike, rod, Dowsing Machine.** Recommended: none. Water Pokémon come from Surf, Dive and sailing; one "Rod" key
    item can come later. [Unbound's three rods; a bike on the world map.]
19. **Decided (16 Oct):** **Rest prices.** Recommended: a per-room price on Golden Sun's inn ladder (2–25 per Adept), charged only for
    Adepts below full; revival level × 20, curse removal level × 10. [A flat price by danger stars; keep the flat 6.]
20. **Decided (16 Oct):** **Trainer rewards.** Recommended: pay per Adept beaten, as trainers.json says. [Count the bonded partner; keep
    the built per-unit pay.]
21. **Decided (16 Oct):** **Breakable gear, curses, the forge.** Recommended: keep all three with the equipment review. Gear breaks 1 use
    in 8 and repairs at 1/4; cursed gear locks until removed at a rest; the GS2 forge comes at Forgeheart in Act II.
    [Curses without breakage; neither; no forge.]
22. **Decided (16 Oct):** **Crew 2's balls before m10.** Recommended: 3 Poké Balls in Corvin's first kit. [Catching is Crew 1's until the
    Wayfarer.]
23. **Decided (16 Oct):** **Naming.** Recommended: the battle command becomes "Ball" and Golden Sun's weapon effect "Weapon Art", keeping
    "Catch" for the Forest verb and "Unleash" for the Set Pokémon action. [Keep both names.]
24. **Decided (16 Oct):** **Mini-game currency.** Recommended: Golden Sun's Game Tickets and Lucky Medals at the Glimmer Saucer. [Plain
    coins; a casino coin.]
25. **Decided (17 Oct):** **Ho-Oh's catch style.** story.md gives each legendary its own style. Recommended: keep Ho-Oh's classic catch
    after the fight, made possible by the Farer Ball or a calmed catch-rate floor. [Make the forge fight end with
    Ho-Oh joining by script.]
