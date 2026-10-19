# Mission 8: The Tradewind Bazaar

> **Status:** draft for your yes or notes (19 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 8, §4 (Wynn), §9 (the Bazaar: Pokémon as currency), §9a (the Tumbleweed Trio,
> the Bounty Board) and §9b (the Freeport Guild). Today's build: [mission-8-build.md](../../design/mission-8-build.md).

| | |
|---|---|
| Mission | 8, The Tradewind Bazaar (Act I; the second Crew 2 interlude) |
| Plays after | Crew 1's second recruitment and mission 7: Crew 1's next rest at an inn or a sanctum once `m5_done`, `m6_done` and `m7_done` are all set (demo decision 7; story.md §14 Q1) |
| Crew | Corvin (at his L9 floor, progression 1) and Larvitar, Tamsin and Riolu, Nerissa and Froakie, with crew 2's own bag (the Linking Cord in it); Wynn (L9) and Ralts join in scene 3 |
| Rooms | Wherever Crew 1 rests (the handover and the hand-back); `tradewind_bazaar` (re-clipped larger: the Guild hull, the market hull, Hull Nine, the licence hull, the grain hull, the rope hull, the fish hull, the bell hull, Hull Two's old hold and the lanes of water between them). The Bazaar's other hulls stay narration and painted backdrop (decision 5) |
| Clock | The rest sets dawn for Crew 1; the handover sets dawn at the Bazaar, and the clock runs as the crew walks; dusk as the skiff leaves; Crew 1 wakes at dawn |
| Flags in | `m5_done`, `m6_done`, `m7_done` |
| Flags out | `m8_started`, `m8_intro`, `m8_wynn`, `m8_code`, `m8_bridge`, `m8_heights`, `m8_crates`, `m8_heist`, `m8_trio`, `m8_back`, `m8_cleared`, `m8_guild`, `m8_chart`, `m8_done`, `m8_posters`; the contracts: `m8_c_bilge`, `m8_box`, `m8_c_overboard`, `m8_c_ice`, `m8_hold_lamp`, `m8_hold_crate`, `m8_c_hold`, `m8_tibbs_read`, `m8_bell_rope`, `m8_c_bell`; and, optional, `m8_plumb_read`, `m8_clerk_read` |
| Unlocks | Wynn (Sky, with Ralts) joins, and with her Whirlwind and Mind Read; the Dawn Stone in crew 2's bag (story decision 5); crew 2's Freeport Guild rank, Bronze, and five hand-written contracts on the Bazaar's board (decision 11, step 1); the wanted posters on Tidewarden notice boards (decision 11; §9a's Bounty Board). Both crews are full |
| Reply beats | 2, Corvin's (README §3): Wynn's offer (scene 3); Wynn's chart (scene 13) |
| Fights | The Tumbleweed Trio (`tumbleweed_trio`, new) on Hull Nine; optional, the Bilge King (`bounty_bilge_king`, new: contract G1). A loss plays "Try again" |
| Leads into | Crew 1 resumes where it rested, with Runner Pell and the posters (scene 16). Mission 9 begins from its own page |

**The flow.** The next time Crew 1 rests after both its recruitments, the story crosses to Corvin's crew again,
come east through the Galeway to the Tradewind Bazaar for a chart with the Crown on it. The only one is Wynn's,
an "impossible" chart that Factor Plumb holds in his strongbox as surety for a debt of two hundred coins, to which
he has added a nought. If Wynn can't pay by the turn of the tide, the Bazaar's oldest law lets him take her Ralts in
kind. She joins on the promise of a heist. Mind Read gets the strongbox's numbers out of Plumb's purser; Whirlwind
swings a sail across the gap to his hull; Move clears his collateral; the dial opens the box on the real note, the
chart and Wynn's Dawn Stone. A crate labelled ORANGES turns out to hold the Tumbleweed Trio, who want the "treasure
map". Beaten, they are blown away on Wynn's wind. At the Guild, Guildmistress Tally weighs the two notes, clears
Wynn's name, fines Plumb his nought and the crew one coin, and opens the board to them. Wynn's chart shows six
threads of light running under the world to a ring beneath the Pinnacle, "the Crown", and a tower above the clouds
where sky-ships moored; Corvin lays the ledger page on it. The crew sails for Fallhaven at dusk, and Crew 1 wakes to
a runner with four wanted posters.

## Scenes

### 1. The handover

- Room: wherever Crew 1 rests. Trigger: the rest hook (decision 7), once `m5_done`, `m6_done` and `m7_done`, unless
  `m8_started`. A bunk or the home bed doesn't count.

*The rest's fade holds on black. The innkeeper's after-rest line is held back until Crew 1 returns.*

**Narration:** {HERO} slept. Far to the east,
beyond the Galeway, a Rimborn skiff
came in out of the storm lanes.

Ahead of it, a hundred ships were
lashed together into one town, and
every deck was a market.

*[phase dawn] [crew 2] [flag m8_started] [warp tradewind_bazaar, entrance 0] Crew 1 is recorded where it rested,
and resumes there in scene 16.*

### 2. The Tradewind Bazaar

- Room: `tradewind_bazaar`, the Guild hull's landing. Trigger: entering, unless `m8_intro` (today's
  `bazaar_arrival`, rewritten).

*[fade in 40] Morning on the Tradewind Bazaar: a hundred hulls lashed together in the middle of Eastwater, plank
bridges between their rails, sails strung overhead for shade, every deck a market. Sellers cry from every
direction; gulls, music, the smell of tar and frying fish. Ketch brings the skiff in to the landing of the Guild
hull, a broad old barge at the heart of the Bazaar, with an awning over a desk, a set of brass scales and a notice
board as tall as a door. [crew out]*

**Ketch:** The Tradewind Bazaar. If it's for
sale anywhere, it's for sale here.
Mind your purse.

Mind your Pokémon, too. Some debts
here get paid in kind.

**Tamsin:** In kind?

**Nerissa:** In Pokémon. The oldest law on the
water. Pearlhollow sells its pearls
here. We never bring our partners.

**Corvin:** We want a chart. One with the Crown
on it.

*Under the awning, a big woman behind the desk is listening to a plump man in a plum-coloured coat, who talks a
great deal with his hands. On a bollard by the notice board a young woman sits with a long map case across her
knees, writing very fast. [camera → the desk] [camera back]*

**Plumb:** ...two thousand, Guildmistress, by
the turn of the tide. Paid in coin,
or paid in kind.

**Tally:** I know the law, Factor. I keep it.
Till the tide turns, she's a debtor,
not a payment. Off my deck.

**Plumb:** Of course, of course. Business is
business.

*[walk Plumb → the market hull] He tips his hat to the crew as he passes. [hide Plumb] Tally looks the crew up and
down.*

**Tally:** New faces. Rimborn, by the coats.
Buying or selling?

**Corvin:** Buying. A chart, with something on
it called the Crown.

**Tally:** The Crown? Ha. There's one chart on
the Bazaar daft enough for that.

*[face Tally → the bollard] She nods at the young woman with the map case.*

**Tally:** Hers. And it's locked up in Factor
Plumb's strongbox. Good luck.

*[crew in] [rest point] [flag m8_intro] Control returns. Plumb's row now stands at his counting table on the market
hull.*

### 3. Wynn

- Room: `tradewind_bazaar`, the Guild hull. Trigger: talking to Wynn (slot 9), unless `m8_wynn` (today's
  `wynn_joins`, rewritten).

*Wynn sits on the bollard under the notice board, scribbling on the back of an old chart with a stub of pencil: a
small, quick young woman in a sky-blue coat with too many pockets, her hair escaping from a scarf, a map case's strap
across her chest. A Ralts peeps out from behind her boots. Above her head, nailed to the board, is a notice with her
name on it. She doesn't look up.*

**Wynn:** ...and if the current turns there,
then the whole east chart is wrong,
which it is, which I said. Hello!

*[face Wynn → Corvin] [emote Wynn: exclaim] [crew out]*

**Wynn:** You want the Crown chart. I heard.
The whole hull heard. The
Guildmistress has a carrying voice.

Wynn. Cartographer. A very good one.
Nobody believes that either. That's
me, up on the notice.

**Notice:** WYNN, CARTOGRAPHER. DEFAULTED ON
A DEBT OF 2,000 COINS.

DO NOT TRADE WITH HER. Posted at
the request of Factor Plumb.

**Corvin:** Two thousand?

**Wynn:** Two hundred. I borrowed two hundred
from Plumb, to have the chart
engraved. Two. One, two.

Nobody bought it. A man at the
chart-hall laughed so hard he had to
sit down. So I couldn't pay.

So Plumb took the chart as surety.
Fine. Fair. Then the note came back
from his strongbox to the Guild...

...and it says two thousand. He
added a nought. Noughts are very
easy to add. They're round.

**Tamsin:** Ha. Seven out of ten, for the
nought.

**Wynn:** Thank you! Nobody's rated it before.

If I can't pay by the turn of the
tide, he takes it in kind.

*[face Wynn → Ralts] Ralts hides its face in her coat. [emote Ralts: sweat]*

**Nerissa:** In kind. Your Ralts.

**Wynn:** A Pokémon can settle a debt, on the
Bazaar. It's the oldest law on the
water. I hate it.

**Corvin:** And the real note? The one that
says two hundred?

**Wynn:** In his strongbox, on his own hull,
moored off the market. With my
chart.

So! Here's a thought. A small one. A
completely legal sort of illegal
one.

We open his strongbox. We take the
real note to the Guild. And my chart
is yours to read. So am I.

**Corvin replies:**

1. "Count us in."

   **Wynn:** Oh, good. I had a speech ready. It
   had diagrams.

2. "That's stealing."

   **Wynn:** From a thief. It's more like
   un-stealing. Un-stealing is barely a
   crime.

3. "What's in it for us?"

   **Wynn:** The only chart in the world with
   your Crown on it. And me. I'm very
   good. Ask anyone.

   Don't ask anyone.

*Every reply rejoins here.*

**Wynn:** I'm Sky, by the way. I can make a
wind. And I can hear what people
are thinking, a little.

When they think loudly. Most people
think very loudly.

*[recruit wynn] Wynn and Ralts join the crew.*

**System:** Wynn joined the crew!

**Wynn:** Plumb's purser, Dabney, keeps his
counting table on the market hull.
He knows the strongbox numbers.

He thinks about them all day. He
can't help it. He's that sort.

And Plumb's hull has its gangplank
up. But there's a spar on the market
hull with a sail on it, and...

*[emote Wynn: sweat]*

**Wynn:** ...and I'll tell you about that
part when we get to it. I don't like
that part.

*[crew in] [flag m8_wynn] Control returns.*

### 4. The purser

- Room: `tradewind_bazaar`, the market hull. Trigger: Mind Read on Dabney (slot 8, `m8_code`, today's `mind_read`
  event, rewritten). Before Wynn, nobody in crew 2 has Mind Read, and Dabney says his line (People and signs).

*Behind Factor Plumb's counting table, a thin young man in a clerk's coat counts coins into stacks, very fast, lips
moving. Plumb is away down the deck, haggling. [crew out] Wynn puts two fingers to her temple. [light: a faint
violet shimmer round Dabney]*

**Dabney, thinking:** Seven. Three. Don't think it,
Dabney. Don't you think it.

And the last one's on the bow. The
hull's own number. Don't look at the
bow!

*[emote Dabney: sweat] He looks at the bow of the hull across the gap.*

**Wynn:** Seven, three, and the number on
the bow. Every hull on the Bazaar
has its number on its bow.

He's been thinking it all week, poor
man. It's very loud.

*[crew in] [flag m8_code] Control returns. Hull Nine's bow can be read from the market hull's rail (People and
signs).*

### 5. The sail-bridge

- Room: `tradewind_bazaar`, the market hull's rail. Trigger: Whirlwind on the furled sail (slot 10, `m8_bridge`, as
  built; puzzle 2).

*[crew out] Wynn faces the furled sail and lifts both hands. A gust comes out of nowhere and fills it with a crack.
[light: a swirl of wind] The spar swings out over the gap on its pivot and drops its far end onto Hull Nine's rail
with a thump. The sail hangs flat and taut beneath it. [gate: the bridge's cells open, as built]*

**Wynn:** There. A bridge. A lovely bridge.

*[emote Wynn: sweat]*

**Wynn:** That's the part I don't like.

*[crew in] [flag m8_bridge] Control returns.*

### 6. The gap

- Room: `tradewind_bazaar`, the near end of the sail-bridge. Trigger: stepping onto it (a step-on spot), once
  `m8_bridge`, unless `m8_heights`.

*[crew out] Wynn stops at the foot of the spar. Below it, between the two hulls, the green water of the lane slops
about, a long way down.*

**Wynn:** I'm fine. I'm fine. I'm just not
looking down. Why is there so much
down?

**Tamsin:** It's three masts high. You've been
higher.

**Wynn:** I fell out of the sky once. Once
was plenty. Once was a whole life's
worth.

**Nerissa:** Look at my back. Breathe when I
breathe. In. Out.

*[walk Nerissa → across the spar] [walk Wynn → after her] [walk Corvin, Tamsin, Larvitar, Riolu, Froakie and Ralts →
after them] [wait 30]*

**Wynn:** ...In. Out. In. Oh, it's over.
It's over! I did it! Don't make me
do it again.

**Corvin:** We'll be coming back this way.

**Wynn:** Don't tell me things.

*[flag m8_heights] Straight on to scene 7.*

### 7. Hull Nine

- Room: `tradewind_bazaar`, Hull Nine's deck. Trigger: straight on from scene 6.

*Hull Nine: a broad old merchantman, her gilt rails gone green, her deck crowded with crates, chests and bundles
under tarpaulins, every one with a tag: COLLATERAL. At her stern stands a painted deckhouse, and crates are stacked
in front of its door. In a pen by the mainmast, a Lillipup lies with its chin on its paws.*

**Corvin:** Everything here is somebody's
debt.

**Wynn:** Every bit. That pen was going to be
Ralts's.

*[emote Ralts: sweat] [face Corvin → the pen] The Lillipup lifts its head, then puts it down again.*

**Corvin:** ...One thing at a time. The
deckhouse.

**Tamsin:** Behind about forty crates.

*[crew in] Control returns. The crates are puzzle 3.*

