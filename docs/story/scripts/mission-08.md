# Mission 8: The Tradewind Bazaar

> **Status:** draft for your yes or notes (19 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 8, §4 (Wynn), §9 (the Bazaar: Pokémon as currency), §9a (the Tumbleweed Trio,
> the Bounty Board) and §9b (the Freeport Guild). Today's build: [mission-8-build.md](../../design/mission-8-build.md).

| | |
|---|---|
| Mission | 8, The Tradewind Bazaar (Act I; the second Crew 2 interlude) |
| Plays after | Crew 1's second recruitment and mission 7: Crew 1's next rest at an inn or a sanctum once `m5_done`, `m6_done` and `m7_done` are all set (demo decision 7; story.md §14 Q1) |
| Crew | Corvin (at his L9 floor, progression 1) and Larvitar, Tamsin and Riolu, Nerissa and Froakie, with crew 2's own bag (the Linking Cord in it); Wynn (L9) and Ralts join in scene 3 |
| Rooms | Wherever Crew 1 rests (the handover and the hand-back); `tradewind_bazaar` (re-clipped larger: three hulls, the ones a beat happens in: the Guild hull with its old hold, the market hull and Hull Nine, and the lanes of water between them). The Bazaar's other hulls stay narration and painted backdrop (decision 5) |
| Clock | The rest sets dawn for Crew 1; the handover sets dawn at the Bazaar, and the clock runs as the crew walks (nothing at the Bazaar depends on the phase); dusk as the skiff leaves; Crew 1 wakes at dawn |
| Flags in | `m5_done`, `m6_done`, `m7_done` |
| Flags out | `m8_started`, `m8_intro`, `m8_wynn`, `m8_code`, `m8_bridge`, `m8_heights`, `m8_crates`, `m8_heist`, `m8_trio`, `m8_back`, `m8_cleared`, `m8_guild`, `m8_chart`, `m8_done`, `m8_posters`; the contracts: `m8_c_bilge`, `m8_box`, `m8_c_overboard`, `m8_c_ice`, `m8_hold_lamp`, `m8_hold_crate`, `m8_c_hold`, `m8_tibbs_read`, `m8_bell_rope`, `m8_c_bell`; and the optional Mind Read flags, `m8_plumb_read`, `m8_clerk_read`, `m8_scratch_read`, `m8_rook_read`, `m8_aipom_read` |
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
chart and Wynn's Dawn Stone; the note shows the nought added in a different ink. A crate labelled ORANGES turns out to hold the Tumbleweed Trio, who want the "treasure
map". Beaten, they are blown away on Wynn's wind. At the Guild, Guildmistress Tally weighs the two notes, clears
Wynn's name, fines Plumb his nought and the crew one coin, and opens the board to them. Wynn's chart shows six
threads of light running under the world to a ring beneath the Pinnacle, "the Crown", and a tower above the clouds
where sky-ships moored; Corvin lays the ledger page on it. The crew sails south for Fallhaven at dusk, and Crew 1
wakes to a runner with three wanted posters.

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

**Tally:** New faces, off a Rimborn skiff.
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
Fine. Fair. Then he filed his copy
of the note with the Guild...

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

**Wynn:** My Ralts. For a nought.

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

**Wynn:** Dabney, Plumb's purser, on the
market hull. He knows the numbers.
Thinks about them all day. Loudly.

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
moving. At the table's far end Plumb is haggling with a fisher, his back turned. [crew out] Wynn puts two fingers
to her temple. [light: a faint violet shimmer round Dabney]*

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

*At the relic stall beside the table, two slipping moustaches turn toward the bow, then toward each other. [emote
the relic sellers: idea] [crew in] [flag m8_code] The relic stall's rows hide (People and signs). Control returns.
Hull Nine's bow can be read from the market hull's rail.*

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
about.*

**Wynn:** I'm fine. I'm fine. I'm just not
looking down. Why is there so much
down?

**Tamsin:** It's a plank over a puddle. You've
been higher.

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

### 8. The strongbox

- Room: `tradewind_bazaar`, inside Hull Nine's deckhouse. Trigger: talking to the strongbox (slot 11, today's
  `strongbox`, rewritten), unless `m8_heist`. The crates (puzzle 3) stand between the deck and the deckhouse door.

*Inside the deckhouse: a cabin hung with framed bills of sale, a desk, and in the corner an iron strongbox as big as
a sea chest, with a brass dial of three rings set in its lid. [crew out]*

*Without `m8_code`:*

**Wynn:** Three rings, and we don't know a
single number. Dabney does. He's
thinking about them right now.

*With `m8_code`:*

**Wynn:** Three rings. Seven, three, and the
bow.

*Then: [dial] The dial shows three rings of the numbers 0 to 9. The player turns each ring and presses A. A wrong
code:*

**System:** Click. The lid holds fast.

*The right code, 7, 3, 9:*

**System:** Click. Click. Clunk.

*The lid springs open. Wynn dives in with both hands.*

**Wynn:** My chart! Oh, my chart. Hello.
You're all crumpled. I'm sorry.

*She lifts out a long roll tied with blue ribbon, then a folded paper, then a small stone that glows faintly, pale
gold, like the edge of morning.*

**Wynn:** And the note. Look. Two hundred, in
brown ink. And a nought after it, in
black.

And my stone! He took my stone too.
It was in my fist when the fisher
fished me out of the sea.

**Nerissa:** That's a Dawn Stone.

**Wynn:** Is it? I always just called it
mine.

*[give Dawn Stone]*

**System:** {LEADER} received the Dawn Stone!

*[flag m8_heist] [shake 20, 1] Out on the deck, a crate bangs open.*

*[emote Corvin, Tamsin, Nerissa, Wynn, Larvitar, Riolu, Froakie and Ralts: exclaim] [crew in] Straight on to scene 9.*

### 9. The Tumbleweed Trio

- Room: `tradewind_bazaar`, Hull Nine's deck. Trigger: straight on from scene 8.

*[walk the crew → out onto the deck] [crew out] The crate labelled ORANGES lies open. Out of it climb a lanky woman
in a dusty green duster with a thistle in her hatband, a round man in a brown coat stuck all over with burrs, and a
Meowth in a tiny tricorn hat. [show Bramble] [show Burr] [show Scratch] The woman plucks the chart roll out of
Wynn's hands. [walk Bramble fast → Wynn] [emote Wynn: exclaim]*

**Bramble:** Thank you SO much, dears. We'd have
been in that crate all day.

**Burr:** We had ourselves delivered. As
oranges. I can't feel my legs. Or
the oranges.

**Scratch:** Quiet! The motto. Do the motto!

*[pose Bramble: flourish] [pose Burr: flourish] [light: a spotlight on the three of them, from nowhere]*

**Bramble:** Hark! Is that trouble,
blown in on the breeze?

**Burr:** It's us, dearest Bramble,
the scourge of the seas!

**Bramble:** We roll where we like,
and we take what we please!

**Bramble:** Bramble!

**Burr:** Burr!

**Scratch:** And Scratch, that's the cat!
The Tumbleweed Trio, rolling
free!

*[light: back to day]*

**Tamsin:** ...Was that a song?

**Corvin:** I think it was a threat.

**Scratch:** It's a motto! It's a whole brand!
The Factor bragged he had a treasure
map in that box. We heard him.

Hand it over, and nobody gets hurt.
Mostly you.

**Wynn:** It isn't a treasure map! It's a
chart! It's much better than a
treasure map!

**Bramble:** Then it's worth even MORE.

*Bramble's Seviper slides out of the crate after her. Burr's Ferroseed rolls out, and sticks to his coat. [emote
Burr: sweat] [crew in] [battle tumbleweed_trio]*

*If the fight is lost, "Try again" plays and the fight restarts as it began. Tamsin's line as it restarts:*

**Tamsin:** Again. They're terrible. That's what
makes it embarrassing.

### 10. Tumbling off

- Room: `tradewind_bazaar`, Hull Nine's deck. Trigger: winning the fight (the Trio's `scene_after`).

*The Seviper and the Ferroseed fall in a heap on top of Burr. Bramble still has the chart. [emote Bramble: sweat]
[crew out]*

**Bramble:** We'll take our map and go! With
dignity!

**Scratch:** Run with dignity! RUN!

*[face Wynn → Bramble] [emote Wynn: anger] Wynn lifts both hands. [light: a swirl of wind]*

**Wynn:** That. Is. My. CHART.

*A gust bursts across the deck, picks up all three of them, and the Seviper, and the Ferroseed, and lifts them
spinning over the mainmast. The chart flutters out of Bramble's hands and drops into Wynn's. [walk Bramble, Burr,
Scratch, Seviper and Ferroseed fast → up, off the top of the screen] [hide the Trio]*

**Burr:** I still can't feel my legs!

**Scratch:** Nobody can feel anything up here!

**Bramble:** We're tumbling off agaaain!

*[light: a twinkle, high in the sky] [wait 30]*

**Corvin:** ...Again?

**Nerissa:** They did say again.

**Wynn:** Wind. Sky Psynergy. I can't do
heights. But I can do that.

*[crew in] [flag m8_trio] Control returns. The way back is over the sail-bridge.*

### 11. The way back

- Room: `tradewind_bazaar`, the far end of the sail-bridge. Trigger: stepping onto it (a step-on spot), once
  `m8_trio`, unless `m8_back`.

*[crew out]*

**Wynn:** In. Out. In. Out. I hate this
bridge. I hate it slightly less.

*[walk the crew → across the spar] [crew in] [flag m8_back] Control returns. Tally waits on the Guild hull.*

### 12. The Guild weighs it

- Room: `tradewind_bazaar`, the Guild hull. Trigger: talking to Tally, once `m8_trio`, unless `m8_cleared`.

*Guildmistress Tally sits at her desk under the awning: a big woman in a coat of many pockets, a pencil behind
each ear, a set of brass scales at her elbow. She looks at the crew's faces, and at the chart under Wynn's arm.*

**Tally:** You've got something to show me.
It's all over your faces.

*Factor Plumb is already hurrying over from the market hull, Dabney at his heels. [walk Plumb fast → beside the
desk] [walk Dabney → behind him]*

**Plumb:** Guildmistress! They have been on my
hull! My dear Wynn, how nice. Have
you brought two thousand coins?

**Wynn:** I've brought the note. The real one.
Out of your strongbox.

*[emote Plumb: exclaim] [emote Dabney: sweat] Wynn lays the folded note on the desk. Tally unfolds it beside the
Factor's copy and holds them both up to the light.*

**Tally:** Two notes. One debt. One hand.

Two hundred, in brown ink. And on
this one, a nought after it. In
black.

Brown ink and black ink, Factor.
Weigh that for me.

**Plumb:** A clerk's slip! Dabney! You
slipped!

**Dabney:** I did not slip! I never slip! I
said it wasn't legal, I said it out
loud, I said...

*[emote Dabney: exclaim] He claps both hands over his mouth.*

**Tally:** Thank you, Dabney.

*[wait 20] Tally lays one note in each pan of her scales. They balance. She looks at them for a while.*

**Tally:** The Guild doesn't care who you are.
The Guild cares what you owe.

Wynn owes two hundred. Factor, you
owe the Guild for every nought you
added.

That's eighteen hundred coins. The
Guild keeps twelve hundred for its
trouble.

Two hundred pays her debt, in full.
The rest goes to the wronged party.

*[face Tally → Corvin]*

**Tally:** And you. You broke into a Factor's
strongbox, on the Guild's water.
That's a fine as well.

One coin.

*[take_coins 1]*

**System:** {LEADER} paid 1 coin.

**Tamsin:** Ha! Ten out of ten.

*[give coins 400]*

**System:** {LEADER} received 400 coins!

*Tally tears the notice with Wynn's name off the board and drops it over the rail into the lane. [hide the notice]*

**Tally:** Wynn, cartographer. In good
standing. Debt paid in full.

*[emote Wynn: heart] [emote Ralts: smile]*

**Plumb:** Business is business, my dear. No
hard feelings.

*[walk Plumb → the market hull] He doesn't look back.*

**Plumb:** ...Many hard feelings.

*[hide Plumb] [walk Dabney fast → after him] [hide Dabney] (Both return to the counting table: People and signs.)*

**Tally:** Now. A crew that can open a
strongbox and then tell me so to my
face is a crew I can use.

The Guild board's open to you.
Bronze. Don't make me sorry.

*[flag m8_guild]*

**System:** Corvin's crew joined the Freeport
Guild! Rank: Bronze.

*[flag m8_cleared] Straight on to scene 13.*

### 13. The chart

- Room: `tradewind_bazaar`, the bench under the Guild hull's awning. Trigger: straight on from scene 12.

*Wynn spreads her chart along the bench and pins its corners with whatever is to hand: a pie tin, an inkpot,
Tamsin's fist and Larvitar. [crew out] It is beautifully drawn: the Calm and its islands, the Galeway as a ring of
tiny storms, Meridia in the middle with the Spine down its back.*

**Wynn:** There. Every chart on the Bazaar
stops at the ground. Mine doesn't.

*Under the land and under the sea, in fine silver lines, six threads run in from six places across the chart and
meet beneath the Pinnacle in a ring of points, like a crown.*

**Corvin:** Six lines, from six places. Embral.
The Greenwild. Marrow Isle.

They're the Well sites. All six of
them.

**Wynn:** I didn't know they were Well sites.
I just drew what I saw.

I was six. My mother held me up to a
window, very high, up in the
clouds.

She pointed down at the world and
said, see the lights? They all run
in, under the mountain.

And that's the Crown. Don't you ever
fall on it.

*[wait 20]*

**Wynn:** Then I fell. Not on it. In the sea,
off Eastwater. A fisher found me.
I've been drawing it ever since.

**Nerissa:** The Crown. "Shipped on, all. To the
Crown."

*Corvin takes the ledger page out of his coat, unfolds it, and lays it on the chart over the ring beneath the
Pinnacle. [emote Tamsin: exclaim] [emote Wynn: question]*

**Corvin:** It's a place. The tithe goes to a
place under the Pinnacle. And the
order calls it the Crown too.

**Tamsin:** Your mother and the order use the
same word for it. Eight out of ten,
for creepy.

*Wynn taps the chart's top edge, far north, above the clouds, where one tall tower is drawn in blue ink.*

**Wynn:** And this. A tower higher than the
clouds, with ships tied up to it
like boats at a jetty.

Ships with sails like wings. That's
where the sky-ships moored. I saw
them.

You believe it? Nobody believes it.

**Corvin replies:**

1. "I believe it."

   **Wynn:** Oh. Oh, good. Nobody's ever said
   that. I don't know what to do with
   my hands.

2. "It's hard to believe."

   **Wynn:** It's a chart. You don't believe a
   chart. You sail it, and you see.

3. "Where's the tower?"

   **Wynn:** North. Then up. A long way up.
   Don't make me go up.

*Every reply rejoins here.*

*[wait 30] Corvin looks at the tower for a long time.*

**Corvin:** Ships that sail the sky. Nobody in
Halcyra builds those. Nobody ever
has.

There's a song in Fallhaven. "Under
the marrow, under the stone, sleeps
a ship to carry us home."

To carry us home. Whoever built the
Crown didn't come from here.

*[emote Wynn: question] [emote Nerissa: silence]*

**Corvin:** Sael has to see this. The page, the
chart, all of it. She keeps every
chart of the rim in her archive.

We sail for Fallhaven. When you're
ready.

*[crew in] [flag m8_chart] Control returns. The Guild board is open (The Freeport Guild's contracts, below), and
talking to Ketch at the landing sails.*

### 14. Ketch

- Room: `tradewind_bazaar`, the Guild hull's landing. Trigger: talking to Ketch, once `m8_chart`. Before then, his
  line (People and signs).

**Ketch:** Fallhaven? South, down the rim.
A day and a night, if the wind's
kind. It never is.

*With any contract not done (any of `m8_c_bilge`, `m8_c_overboard`, `m8_c_ice`, `m8_c_hold`, `m8_c_bell` unset):*

**Ketch:** There's still work on that board,
and coin. We won't be back this way
for a long while. Sail anyway?

*Otherwise:*

**Ketch:** Ready when you are.

*[yes/no] No:*

**Ketch:** I'll be here. Eating.

*Yes: scene 15.*

### 15. Down the rim

- Room: `tradewind_bazaar`, the landing. Trigger: yes to Ketch.

*[phase dusk] The Bazaar's lanterns come on, hull by hull, as the skiff pulls away from the landing. [hide the crew]
[fade out 40]*

**Narration:** Ketch ran the skiff south from
the Bazaar at dusk, down the rim
toward Fallhaven.

*Over black:*

**Wynn:** This boat is very low. Low is good.
I love low.

**Nerissa:** The deep's lower still. You'd love
it.

**Wynn:** ...Ask me again in a few years.

*[wait 20]*

**Wynn:** Corvin? You keep thinking about
somebody. {HERO}.

Like a compass needle. It swings
away, and it always swings back.

**Corvin:** Don't do that.

**Wynn:** Sorry. You think very loudly.

**Tamsin:** He does. You can hear it from
the bow.

**Narration:** Both crews were full now: four
Adepts each, on either side of the
Galeway.

And neither knew how soon they would
need each other.

*[flag m8_done] [phase dawn] [resume crew 1] Crew 1 plays again where it rested.*

### 16. The posters

- Room: wherever Crew 1 rested. Trigger: Crew 1 resuming there, once `m8_done`, unless `m8_posters` (mission 7's
  resume scene).

*[fade in 40] Dawn, where Crew 1 rested. The innkeeper's after-rest line plays (it was held back). Then running
feet, and Runner Pell comes in at a scramble, muddy to the knees as always, a fat oilskin satchel on her back. [show
Pell] [walk Pell fast → before {HERO}] She salutes, sways, and gets her breath. [crew out]*

**Pell:** Deputy {HERO}! Runner Pell, off
the Dunlin. Begging your pardon, at
this hour.

The Dunlin's been after the Kestrel
since the turn of the tide. Thank
you for being so easy to find.

Orders from the Commodore. One set
for every Tidewarden board in the
Calm. And one set for you.

*She pulls a roll of posters out of the satchel and unrolls the first. [show the poster]*

**Poster:** WANTED. CORVIN OF FALLHAVEN,
called THE SEAL-BREAKER.
5,000 COINS.

For the Flame seal, the Forgeheart
fire and the breaking of Bastion
Rock.

*Under the words is a portrait: a scowling face with a jaw like an anvil and eyebrows like two Wurmple. [emote
{HERO}: question]*

**{HERO}:** That's a terrible likeness.

*Quiet: [emote {HERO}: sweat] and no line.*

**Sorrel:** That's a potato with a grudge.

**Vesper:** Five thousand. For that, I'd
think about it.

*[wait 20]*

**Vesper:** Briefly.

**Pell:** There are three, Deputy. The
seal-breaker's crew, as far as the
order knows it.

*She unrolls the rest, one after another.*

**Poster:** WANTED. TAMSIN OF THE FORGEHEART.
For arson, assault and insolence.
1,200 COINS.

**Poster:** WANTED. THE DIVER, NAME UNKNOWN.
Escaped prisoner of the order.
800 COINS.

**Maren:** A monk and a diver. The portraits
get worse as they go. The diver is
a fish.

**Sorrel:** The monk's quite good, actually.

**Maren:** Three Adepts. One short of us.
For now.

*[emote Maren: silence]*

**Pell:** The Commodore says, if you see them,
send word. Don't take them on alone.
Thank you for listening.

*[walk Pell fast → off] [hide Pell]*

**Vesper:** Five thousand. That's not a
fire's price. That's a storm's.

**Maren:** Then we'd better be ready for
weather.

*[crew in] [flag m8_posters] Control returns. From here every Tidewarden notice board in the Calm carries the three
posters (People and signs). The cartographer's poster is the Bazaar's own, drawn that afternoon; it hasn't crossed
the Galeway yet.*

## The Freeport Guild's contracts (decision 11)

Step 1 of story.md §14 Q17 only: five hand-written contracts on the Guild hull's board, open from `m8_guild`. Each
notice is read at the board; the job is done on the Bazaar's hulls; the client pays, and the board stamps it DONE.
No contract touches a story flag. The Bazaar lies beyond the Galeway, so in the demo it can't be reached again once
the skiff leaves (scene 15): Ketch warns before sailing, and the contracts stay on the board for Act II.

### The board

- **The board**, on the Guild hull. Before `m8_guild`:

  **Sign:** THE FREEPORT GUILD. Contracts for
  Guild crews only. Apply at the desk.

  *Until `m8_cleared`, Wynn's notice follows (scene 3's two Notice pages).*

  *From `m8_guild`, a menu of the five notices, each read as below. Once a contract's flag is set, its notice
  ends with this page:*

  **Sign:** Stamped across it in red: DONE.
  And a small, neat T.

### G1. The Bilge King (Hunt)

**Notice:** HUNT. THE BILGE KING. Something
big is eating the Guild's grain. It
wears a bucket. Reward: 150 coins.

Ask Mother Bunce, at the grain hold.

- **Mother Bunce** (new), on the market hull, by its open grain hold. Before `m8_guild`:

  **Bunce:** Grain! Good dry grain! Mind the
  hold, mind. Something lives in the
  hold.

  *From `m8_guild`, until `m8_c_bilge`:*

  **Bunce:** You've come about the Bilge King?
  Bless you. In the hold, on the
  grain. You'll know it by the bucket.

  It's eaten half a ton. It's eaten my
  best scoop. It looked at me while it
  did it.

  *From `m8_c_bilge`:*

  **Bunce:** Not a whisker in the hold. I sleep
  at night again. I'd forgotten how.

- **The Bilge King** (new), on the grain heap in the market hull's open hold, until `m8_c_bilge`:

  **Sign:** A rat the size of a pig, sitting on
  the Guild's grain with a bucket on
  its head like a crown. It's eating.

  *From `m8_guild`, talking to it: it stops chewing and looks at the crew. [emote the Bilge King: anger] [battle
  bounty_bilge_king]*

  *If the fight is lost, "Try again" plays and the fight restarts as it began. Nerissa's line as it restarts:*

  **Nerissa:** Again. It's mostly teeth. Stay out
  of the teeth.

  *Won (the fight's `scene_after`): the Bilge King drops its bucket, squeals and goes over the rail into the lane
  with a splash. [hide the Bilge King] [flag m8_c_bilge] [walk Bunce → the hold's edge]*

  **Bunce:** My bucket! And my grain! Here. Every
  coin of it. Well earned.

  *[give coins 150]*

  **System:** {LEADER} received 150 coins!

### G2. Overboard (Salvage, Surf)

**Notice:** SALVAGE. OVERBOARD. My cashbox
went over the rail into the lane.
It floats. I don't. Reward: 80.

Pim, chandler. The market hull.

- **Pim** (new), at his chandlery stall on the market hull. Before `m8_guild`:

  **Pim:** Rope, tar, nails, lamp oil.
  Everything a hull needs to go on
  being a hull.

  *From `m8_guild`, until `m8_box`:*

  **Pim:** You saw my notice? There. In the
  barrel, out in the lane. A week's
  takings, bobbing about.

  I'd fetch it, but I sink. Always
  have. It runs in the family.

  *From `m8_box`, until `m8_c_overboard`:*

  **Pim:** My cashbox! Not a coin wet. Here's
  your eighty. Count it. No, don't. I
  trust you. Count it.

  *[give coins 80] [flag m8_c_overboard]*

  **System:** {LEADER} received 80 coins!

  *From `m8_c_overboard`:*

  **Pim:** Rope, tar, nails. And a new lock on
  my cashbox, on a longer chain.

- **The barrel** (new), bobbing in the lane off the Guild hull's landing, reached on Froakie, until `m8_box`:

  **Sign:** A barrel bobbing in the lane, a
  cashbox wedged in its mouth.

  *From `m8_guild`: [flag m8_box]*

  **System:** {LEADER} fished out Pim's
  cashbox.

### G3. Melting Point (Help, Frost)

**Notice:** HELP. MELTING POINT. The ice
house is melting. Fish wait for
nobody. Reward: 60, and a fish.

Gudrun, the fish stall. Hurry.

- **Gudrun** (new), at her fish stall on the market hull. Before `m8_guild`:

  **Gudrun:** Fish! Fresh fish! Fresh-ish fish!
  The ice is going, and so are the
  fish.

  *From `m8_guild`, until `m8_c_ice`:*

  **Gudrun:** The ice house is a tub of water,
  and my fish are getting ideas.

  The ice boat's late. It's always
  late. If only somebody could freeze
  the thing.

  *From `m8_c_ice`:*

  **Gudrun:** Fish! Frozen fish! Corvin's still in
  there. He's doing very well.

- **The ice tub** (new), beside Gudrun's stall. Until `m8_c_ice`:

  **Sign:** The ice house: a great tub of
  meltwater, full of fish. They look
  worried. Frost would set it.

  *Frost on it, from `m8_guild` (before, the tub freezes for a moment and melts again, and nothing is set): [light:
  a pale blue flash] The tub freezes solid with a crack, fish and all. [flag m8_c_ice] [walk Gudrun → the tub]*

  **Gudrun:** Ice! Proper ice! Ha! The ice boat
  can stay lost. Here's your sixty.

  *[give coins 60]*

  **System:** {LEADER} received 60 coins!

  **Gudrun:** And your fish. That one, in the
  ice. I've named him Corvin. He's got
  your jaw.

  **Tamsin:** He has. Nine out of ten.

  **Corvin:** ...Thank you?

  *From `m8_c_ice`:*

  **Sign:** A tub of solid ice. A fish in it
  looks out at you with your jaw.

### G4. The Guild's old hold (Cache: Blaze, Move, Scoop)

**Notice:** CACHE. THE GUILD HULL'S OLD HOLD.
Shut since Guildmaster Penhallow's
day. Nobody's been down since.

Whoever can get in keeps what's
inside. By the Guild's leave. T.

- **The hatch**, on the Guild hull's deck behind Tally's desk. Before `m8_guild`:

  **Sign:** A hatch, nailed shut. Painted on
  it: GUILD PROPERTY. NOT YOURS.

  *From `m8_guild` the nails are out and the hatch is open (a gate): a ladder goes down into the dark.*

- **The hold** is drawn dark until the lamp is lit; its rows show from `m8_hold_lamp`.

- **The lamp**, on a hook at the ladder's foot. Until `m8_hold_lamp`:

  **Sign:** An old ship's lamp on a hook, cold.
  The dark down here is very thick.
  Blaze would light it.

  *Blaze on it: [light: the hold's dark lifts] [flag m8_hold_lamp] [crew out]*

  **Tamsin:** There. Now we can see what we're
  falling over.

  *[crew in]*

- **The ballast crate**, half sunk in the sand, until `m8_hold_crate`:

  **Sign:** A crate of ballast stone, half sunk
  in the sand. Behind it, something
  glints. It would slide, with a push.

- **The glint**, in the ballast behind the crate, from `m8_hold_crate`, until `m8_c_hold`:

  **Sign:** Something glints in the ballast
  sand. Scoop would dig it out.

  *Scoop on it: a small iron chest comes up out of the sand (the chest's row shows). [flag m8_c_hold] [crew out]*

  **Wynn:** Penhallow's chest! They say he never
  once got his feet wet. Not in sixty
  years on the water.

  *[crew in] The chest: Turtle Boots, with the engine's chest line.*

### G5. Who took the bell-rope? (Mind Read)

**Notice:** WHO TOOK THE BELL-ROPE? The
Guild's bell can't ring. Nobody
knows when lunch is. Reward: 100.

Absalom, at the bell. Ask anyone.
Nobody will admit anything.

- **Absalom** (new), the bell-ringer, on the Guild hull under the Guild's bell, which has no rope. Before
  `m8_guild`:

  **Absalom:** I ring the Guild's bell. Every
  hour, on the hour. Well. I used to.

  *From `m8_guild`, until `m8_bell_rope`:*

  **Absalom:** Somebody's had my bell-rope. Off
  the bell, in the night. A good rope.
  A very good rope.

  It was Rook, or Tibbs, or my own
  Aipom. Nobody will say. Nobody ever
  says.

  *From `m8_bell_rope`, until `m8_c_bell`:*

  **Absalom:** My rope! Tibbs? For the Aipom's
  swing? ...I see. Well. Hold this.

  *He knots the rope back onto the bell and hauls. [shake 10, 1] The Guild's bell rings out across the Bazaar,
  once, twice, and every hull answers it with a cheer. Somewhere, somebody shouts "Lunch!"*

  **Absalom:** There. Now everybody knows when
  lunch is. Here's your hundred.

  *[give coins 100] [flag m8_c_bell]*

  **System:** {LEADER} received 100 coins!

  **Absalom:** And Tibbs can have my old rope, for
  the swing. Don't tell him it was my
  idea.

  *From `m8_c_bell`:*

  **Absalom:** On the hour, every hour. And a
  swing for the Aipom. Everybody's
  happy.

- **Rook** (new), a sailmaker, stitching by the Guild's bell:

  **Rook:** I sew sails. I don't steal rope.
  I've got all the rope I need.
  Mostly.

  *Mind Read (`m8_rook_read`):*

  **Rook, thinking:** Rope. I could use some rope. I
  didn't take it. But I could use it.

- **Tibbs** (new), a deck-boy, by the market hull's mainmast:

  **Tibbs:** I never! I never anything!

  *Mind Read (`m8_tibbs_read`):*

  **Tibbs, thinking:** Don't look at the swing. Don't
  look at the swing. Don't look at...

  *[emote Tibbs: sweat] He looks at the swing.*

  *From `m8_c_bell`:*

  **Tibbs:** Absalom gave me his old rope! For
  the swing! I didn't even have to
  steal it!

- **The Aipom**, on the Guild hull's rail under the bell:

  **Sign:** An Aipom, hanging from the rail by
  its tail, swinging hopefully.

  *Mind Read (`m8_aipom_read`):*

  **Aipom, thinking:** Swing! Swing! Swing! Swing!
  Swing! Swing!

- **The swing**, from the market hull's yard. Until `m8_tibbs_read`:

  **Sign:** A rope swing, hung from a yard. A
  very good rope.

  *From `m8_tibbs_read`, until `m8_bell_rope`:*

  **Sign:** A rope swing. On the end of the
  rope, a brass bell-pull. Take it?

  *[yes/no] Yes: [flag m8_bell_rope]*

  **Tibbs:** Aww. It was for the Aipom. It loves
  a swing.

  *From `m8_c_bell`:*

  **Sign:** A rope swing, an old rope this
  time. The Aipom is on it.

## People and signs, by room

### Where Crew 1 rests

No lines of its own: the handover (scene 1) and the posters (scene 16) play there, and that rest's after-rest line
is held back until scene 16.

### `tradewind_bazaar`

*The states:* before Wynn (until `m8_wynn`); the heist (`m8_wynn`, until `m8_cleared`); after the Guild's ruling
(`m8_cleared`). Most people change only once, at the ruling. The Bazaar is beyond the Galeway, so in the demo
nobody here is seen after scene 15. Positions are places in the re-clipped room.

- **Guildmistress Tally** (new), at her desk on the Guild hull. After scene 2, until `m8_trio`:

  **Tally:** The tide turns when it turns. Till
  then she's a debtor, and he's a
  Factor. That's the law.

  *From `m8_trio`:* scene 12. *From `m8_cleared`:*

  **Tally:** The board's yours, Bronze. Work's
  work, and the Guild pays what it
  owes. Every coin.

- **Factor Plumb** (new), at his counting table on the market hull, from scene 2 until scene 12:

  **Plumb:** Factor Plumb, my friend. Anything
  bought, anything sold, anything
  lent. At very fair rates.

  Paid in coin, or paid in kind. The
  oldest law on the water. I'm so fond
  of the old laws.

  *Mind Read (optional, `m8_plumb_read`):*

  **Plumb, thinking:** Two hundred, and one little
  nought. Two thousand. Lovely Ralts.
  Lovely, lovely Ralts.

  *From `m8_cleared`:*

  **Plumb:** No hard feelings, my friend. None
  at all. I'm writing them all down.

- **Purser Dabney** (new), slot 8, at the counting table. Until `m8_code`:

  **Dabney:** The Factor's business is the
  Factor's business. Move along. I'm
  not thinking about anything.

  *From `m8_code`, until `m8_cleared`:*

  **Dabney:** I wasn't thinking anything! Nobody
  heard me not thinking anything!

  *From `m8_cleared`:*

  **Dabney:** I said it out loud. In front of the
  Guildmistress. I feel wonderful.

- **Wynn**, slot 9, on the bollard: scene 3. From `m8_wynn` she is in the crew, and the row hides (as built).

- **Ketch**, at the Guild hull's landing. Until `m8_chart`:

  **Ketch:** I'll mind the skiff. Buy me
  something. Anything. Food.

  The song's got a market verse now.
  Everything rhymes with "haggle".

  *From `m8_chart`:* scene 14.

- **Calloway** (new), the chart-seller, at his stall on the market hull. Until `m8_chart`:

  **Calloway:** Charts! Every sea that's ever been
  sailed, and two that haven't!

  The Crown? Ha! Ask Wynn. She'll sell
  you a chart of the moon, signed by
  the moon.

  *From `m8_chart`:*

  **Calloway:** You believe that girl's chart?
  ...Well. It's very well drawn. I'll
  give her that. Don't tell her.

- **Ottoline** (new), at her stall on the market hull. She opens the Bazaar's shop (items-and-economy.md §11:
  tier 2 weapons and armour, Vial, Great Ball; no Pokémon for sale) after her line. In every state:

  **Ottoline:** If it floats, I sell it. If it
  sinks, I sell it cheaper.

  Blades, shields, Vials, Great Balls.
  No Pokémon. Not on my deck. I don't
  hold with it.

  *Not enough coins, in the shop:*

  **Ottoline:** Short? Everybody's short. Come back
  long.

  *Leaving the shop:*

  **Ottoline:** Fair winds, and fair prices.

- **Ossery** (new), the treasure buyer, beside Ottoline's stall. He buys what the crew finds and sells the
  Artifacts list back (items §11's treasure buyer) after his line. In every state:

  **Ossery:** I buy what you find, and I don't
  ask where you found it. Rare things.
  Odd things. Old things.

  *Leaving:*

  **Ossery:** Bring me something strange.

- **Hettie** (new), the innkeeper, at The Hammock: hammocks strung between the Guild hull's masts (the inn role, at
  Eastwater's price on Golden Sun's inn ladder). Before the rest menu:

  **Hettie:** The Hammock. Beds strung between
  the masts. Very airy. Nobody falls
  out. Hardly anybody.

  *From `m8_wynn`, then:*

  **Wynn:** Between the masts. High up. In a
  net. ...Lovely.

  *After resting:*

  **Hettie:** Slept? Good. The masts creak. It's
  how they say good morning.

- **The relic sellers** (the Trio in disguise), at a stall on the market hull beside Plumb's table, until `m8_code`
  (they hear Wynn read the purser, and go to be delivered to Hull Nine as oranges):

  **Relic seller:** Genuine Farer relics! Used by the
  Farers themselves! Whoever they
  were!

  **Other relic seller:** A Farer teapot. A Farer spoon.
  Another Farer spoon. Very rare.

  **Sign:** Both of them have moustaches. Both
  moustaches are slipping.

- **The "Persian"**, on the relic stall's counter, until `m8_code`:

  **Sign:** A Meowth in a tiny tricorn hat sits
  on the counter. A card round its
  neck says PERSIAN.

  *Mind Read (optional, `m8_scratch_read`):*

  **Meowth, thinking:** Don't talk. Persians don't talk.
  Persians are classy. Be classy.

  *From `m8_code`, the stall:*

  **Sign:** The relic stall, empty. A card on
  the counter: BACK SOON. NOT ROBBING
  ANYBODY.

- **Mother Bunce, Pim, Gudrun, Absalom, Rook, Tibbs and the Aipom:** the contracts, above.

- **The licence clerk** (new), a Tidewarden at a licence desk at the market hull's west end, the order's one post on
  the Bazaar. Until `m8_cleared`:

  **Clerk:** Licences for the Calm. Name. Hull.
  Cargo. Next.

  *He never looks up.*

  *Mind Read (optional, `m8_clerk_read`):*

  **Clerk, thinking:** Four more hours. I should look at
  those posters properly one day.
  ...Nah.

  *From `m8_cleared`:*

  **Clerk:** New poster up. A cartographer.
  Drawn from a description. Next.

**Signs and things to examine**

- **The Bazaar sign**, at the Guild hull's landing:

  **Sign:** THE TRADEWIND BAZAAR. A hundred
  hulls, one law: the Guild's. No
  Tidewarden writ runs on this water.

- **Tally's scales:**

  **Sign:** Brass scales, polished bright. The
  Guild weighs everything.

- **Hull Nine's bow**, read from the market hull's rail:

  **Sign:** On the bow of the hull across the
  gap, in gold paint: PLUMB AND CO.
  NINE.

- **The furled sail**, slot 10, on the market hull's rail. Until `m8_wynn` (as built):

  **Sign:** A furled sail on a swinging spar. A
  strong wind would carry it across.

  *From `m8_wynn`, until `m8_bridge`, the same page, then:*

  **Wynn:** That's the part I don't like.

  *From `m8_bridge`:*

  **Sign:** The spar lies across the gap, the
  sail flat and taut beneath it. A
  bridge, more or less.

- **Hull Nine's gangplank:**

  **Sign:** Hull Nine's gangplank, hauled up and
  chained.

- **The collateral crates**, on Hull Nine (puzzle 3):

  **Sign:** A crate tagged COLLATERAL.
  Somebody's whole life, probably. It
  would slide, with a push.

- **The orange crate**, beside the deckhouse door, until `m8_heist`:

  **Sign:** A crate labelled ORANGES. It's
  breathing.

  *Move on it (it doesn't move):*

  **Crate:** Ow!

  *From `m8_trio`:*

  **Sign:** An empty crate. It smells of
  oranges and regret.

- **The debt pen**, by Hull Nine's mainmast:

  **Sign:** A pen by the mainmast. A tag on the
  Lillipup's collar: TAKEN IN KIND.
  60 COINS.

  *From `m8_wynn`, then:*

  **Wynn:** Somebody's Lillipup, for sixty
  coins. And it's all perfectly legal.

- **The bills of sale**, in the deckhouse:

  **Sign:** Framed bills of sale, one for each
  debt. Every one says PAID IN KIND.

- **The strongbox**, slot 11, from `m8_heist` (today's `text_after`):

  **Sign:** Plumb's strongbox, open and empty.

- **The wanted posters**, on the board behind the licence desk. Corvin's:

  **Poster:** WANTED. CORVIN OF FALLHAVEN,
  called THE SEAL-BREAKER.
  5,000 COINS.

  *Under it, the portrait: a jaw like an anvil and eyebrows like two Wurmple.*

  **Corvin:** That isn't my face.

  **Tamsin:** It's a bit your face. Round the
  ears. Three out of ten.

  *Tamsin's:*

  **Poster:** WANTED. TAMSIN OF THE FORGEHEART.
  For arson, assault and insolence.
  1,200 COINS.

  **Tamsin:** Nine out of ten. They got my good
  side.

  *The diver's:*

  **Poster:** WANTED. THE DIVER, NAME UNKNOWN.
  Escaped prisoner of the order.
  800 COINS.

  **Nerissa:** It's a fish. It's a good fish.

  *From `m8_cleared`, a fourth:*

  **Poster:** WANTED. A CARTOGRAPHER, NAME
  UNKNOWN. An accomplice.
  300 COINS.

  **Wynn:** A map case with legs. ...Fair,
  honestly.

- **The lanes**, the water between the hulls:

  **Sign:** Green water slops between the
  hulls. Calm enough to Surf.

- **The Hammock's sign:**

  **Sign:** THE HAMMOCK. Beds between the
  masts. Mind the drop.

- **Ottoline's sign:**

  **Sign:** OTTOLINE'S. If it floats. And a few
  things that don't.

### Crew 1's notice boards (from `m8_posters`)

The Tidewarden boards Crew 1 can reach in the demo each gain the posters as a last page after their own text:
`stonehollow`'s notice board (mission 1), `canalport`'s Tidewarden notice (mission 3) and `eldergrove`'s tithe notice
(mission 5).

**Sign:** Three wanted posters, nailed up
fresh: a seal-breaker, a monk and a
fish.

Corvin's is the worst likeness, by a
long way.

*Then, the first time each is read:*

**Maren:** Every board in the Calm, the
Commodore said. She meant it.

- **Gary Rivalson**, in Stonehollow, from `m8_posters` (before mission 9's page takes Stonehollow over):

  **Gary:** Five thousand coins, for Corvin! I
  could catch him. I'm just busy. Very
  busy.

  Nobody's put a price on me. They
  wouldn't dare. Smell you next tide!

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| Wynn's stone | Hull Nine's strongbox (scene 8; story decision 5) | Dawn Stone ×1, into crew 2's bag | Scene 8's system line |
| The Guild's award | Scene 12 | 400 coins (items §12's "heist purse"), less the 1-coin fine | Scene 12's system lines |
| The Trio's purse | The fight | Their coins (small: they're terrible thieves) | The fight's own line |
| The Bilge King | G1, Mother Bunce | 150 coins | G1's system line |
| Pim's cashbox | G2, Pim | 80 coins | G2's system line |
| The ice house | G3, Gudrun | 60 coins (and a frozen fish named Corvin, a joke, not an item) | G3's system line |
| Penhallow's chest | G4, the Guild hull's old hold, in the ballast (Scoop; the dungeon's gear chest, items §13) | Turtle Boots (the artifact items §13 lists) | The engine's chest line, naming `{LEADER}` |
| The bell-rope | G5, Absalom | 100 coins | G5's system line |
| The Bilge King's purse | G1's fight | The fight's coins | The fight's own line |
| Wynn's chart and the real note | Scene 8 | Nothing: props (the note goes to Tally) | — |

**The Dawn Stone's item text** (the Items screen):

**Item:** A pale stone that glows like the
edge of morning. Wynn has carried
it since she fell.

## Puzzles

The crew's verbs here: Corvin's Move and Scoop, Tamsin's Blaze, Nerissa's Frost, Douse and Ply, Surf on Froakie,
and from scene 3 Wynn's Whirlwind and Mind Read. The main path needs Mind Read (or a lucky guess at the dial),
Whirlwind, Move and the dial. The contracts use the rest: a fight, Surf, Frost, Blaze with Move and Scoop, and Mind
Read three times. An unsolved puzzle resets when the room is left (decision 71), and every crate can always be
got behind again.

**Puzzle 1. The purser and the bow (Mind Read, as built; and a sign, new).**
1. Dabney sits at Plumb's counting table on the market hull. Talking to him gets nothing.
2. Mind Read him (scene 4): "Seven. Three... And the last one's on the bow. The hull's own number" (`m8_code`).
3. From the market hull's rail, Hull Nine's bow reads PLUMB AND CO. NINE. The code is 7, 3, 9.

Golden Sun's habit: half the answer in a thought, the other half in plain sight.

**Puzzle 2. The sail-bridge (Whirlwind, as built).**
1. Hull Nine is moored across a gap of open water from the market hull, its gangplank up and chained.
2. On the market hull's rail, a spar on a pivot carries a furled sail. Cast Whirlwind on it: the spar swings over
   and drops its far end on Hull Nine's rail, and the sail becomes a bridge (scene 5, `m8_bridge`, the gate as
   built).
3. The first crossing plays scene 6, Wynn's fear; the first one back, scene 11.
4. The lane between the hulls is surf water, but Hull Nine's sides are sheer and have no landing steps, so Froakie
   can't board her: the sail-bridge is the only way across.

**Puzzle 3. The collateral (Move, new).**
1. On Hull Nine, crates tagged COLLATERAL stand stacked in front of the deckhouse door, with open deck round the
   stack on the west, the east and the north.
2. Two pushes open a lane: the front crate west into the gap by the rail, then the next north into the bay by the
   mainmast (`m8_crates` when it gets there). The deck is open round every crate the lane needs, so each can always
   be got behind again.
3. The orange crate stands beside the door and won't move: Move on it gets "Ow!" (the Trio are inside). It is never
   in the lane.

**Puzzle 4. The dial (new, decision 6).**
1. In the deckhouse, the strongbox has a brass dial of three rings, 0 to 9.
2. Turn the rings to 7, 3, 9 and press A: it opens (scene 8, `m8_heist`). Any other code clicks and holds, with no
   penalty and no limit.
3. Wynn's line says the numbers if Dabney has been read, and sends the player back to him if not.

**The contracts.** All five are on the Guild and market hulls (decision 5). G1 is a fight. G2 is Surf in the lanes
(the barrel can only be reached on Froakie, from landing steps at the Guild hull's landing, as mission 3's). G3 is
Frost on the ice tub. G4 chains three verbs: Blaze lights the hold, Move shifts the ballast crate off the glint, Scoop
digs out the chest. G5 is a Mind Read riddle: three suspects, one
thought that gives the thief away, and a swing that only shows what it's made of once Tibbs has been read.

## Eggs

- **The Tumbleweed Trio's first heist** (story.md §9a; decision 10). Bramble, Burr and their talking Meowth, Scratch,
  with their own names and looks: a dusty green duster with a thistle in its hatband, a brown coat stuck all over
  with burrs, a tiny tricorn hat. Their Seviper and Ferroseed fight; Scratch doesn't. Their motto keeps the
  original's shape (call and answer, two names, the cat's tag line) and not a word of it, and they leave on a gust,
  "We're tumbling off agaaain!", with a twinkle in the sky: the bent catchphrase their last quest, "Blasting Off
  Again... Again", pays off. Even their first heist says "again". Before it, they sell fake Farer relics in slipping
  moustaches beside Plumb's table, with a Meowth wearing a card that says PERSIAN, overhear the code, and have
  themselves delivered to Hull Nine as oranges.
- **The Bounty Board starts** (§9a; decision 11). The Freeport Guild's board with its five hand-written contracts,
  and the order's wanted posters with terrible portraits: Corvin always gets the worst one (§9a's "one Adept always
  gets the worst portrait"), first at the Bazaar's licence desk, then, from scene 16, on every Tidewarden board in the
  Calm.

## Either order

Mission 8 always follows both of Crew 1's recruitments and mission 7, so Sorrel and Vesper are both in Crew 1 for
scene 16 and nothing differs with the order missions 5 and 6 were played in. Their lines there need no `when` steps.

## Not in this mission

"Paid in Full" (story.md §9's Bazaar story, freeing a Pokémon sold as a debt), which Plumb's pen and its Lillipup
seed; Captain Maize at the Bazaar (§9a), after the demo; generated contracts, guild ranks above Bronze and rival
hunters (decision 11); Wynn's mother at the Aerie and the Stormspire (missions 17 and 19), which her story seeds; a
Gallade by the Dawn Stone, which waits for Ralts to become Kirlia; the Bazaar after the interlude, which is beyond
the Galeway until mission 11's Breaking; mission 9's start ("soon after", at night: decision 8), which is its own
page's, seeded by "We sail for Fallhaven" and Sael's archive.

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **The handover's words** ("{HERO} slept. Far to the east, beyond the Galeway...") and the posters' hand-back,
  written for any restoration point.
- **The way to Fallhaven:** east from the Bazaar to the rim, a day and a night, with no Galeway between (both lie
  outside it, mission 2); Ketch's warning that they won't be back this way for a long while.
- **Why Corvin comes:** a chart with the Crown on it, because "if it's on a chart anywhere, it's for sale at the
  Tradewind Bazaar" (Ketch, mission 7).
- **The Bazaar:** three walkable hulls among a hundred painted ones: the Guild hull (Tally's desk, scales and board,
  the Guild's bell, The Hammock's hammocks between its masts, its old hold), the market hull (the stalls, the open
  grain hold, the yard, the order's licence desk) and Hull Nine; the lanes of water between them; "A hundred hulls,
  one law: the Guild's"; the oldest law on the water, a debt "paid in coin or paid in kind" (story.md §9's "Pokémon
  as currency, which is a problem"); Ottoline's "No Pokémon. Not on my deck"; Pearlhollow selling its pearls there.
- **The Bazaar's people:** Guildmistress Tally ("The Guild doesn't care who you are. The Guild cares what you owe";
  her scales; the one-coin fine); Factor Plumb and his nought ("No hard feelings... I'm writing them all down");
  Purser Dabney, who thinks very loudly; Calloway the chart-seller; Ottoline; Ossery the treasure buyer; Hettie and
  The Hammock; Mother Bunce; Pim, who sinks; Gudrun; Absalom and his Aipom; Rook; Tibbs; the licence clerk who never
  looks up; old Guildmaster Penhallow, named only.
- **Wynn:** her look (a sky-blue coat with too many pockets, a scarf, the map case's strap from art part A's note);
  beginning in the middle of a thought; the debt of two hundred for engraving the chart, with a nought added; the
  chart-hall laughing; her mother at a window in the clouds, pointing at the lights that "all run in, under the
  mountain" and "the Crown. Don't you ever fall on it" (the Wells' threads are Corvin's reading, not hers); falling into the sea off Eastwater, found by a fisher; the
  Dawn Stone in her fist (story decision 5's stone, given a past); "I can't do heights. But I can do that"; reading
  Corvin's thoughts of {HERO}, "like a compass needle".
- **Wynn's chart:** six silver threads from the six Well sites meeting under the Pinnacle in a ring "like a crown"
  (Celebi's vision in mission 5 showed the same threads, to the other crew), and a tower above the clouds in the
  north (story.md's "where the sky-ships moored"); Corvin laying the ledger page on it; "the order calls it the
  Crown too".
- **Corvin's reasoning:** Old Jory's skiff-song (mission 2) set against the sky-ships, "Whoever built the Crown
  didn't come from here" (today's line, kept), and "Sael has to see this... She keeps every chart of the rim in her
  archive", a seed for crew 2 at the archive in mission 9.
- **The heist's shape:** Hull Nine's collateral, the debt pen with the Lillipup, the breathing orange crate, the
  bills of sale, and the code 7, 3, 9 (today's, kept), split between Dabney's thought and the bow.
- **The Guild's ruling:** Plumb's copy filed with the Guild at two thousand, and the original in his strongbox,
  two hundred in brown ink with a nought added in black; the two notes weighed on Tally's scales; Dabney's "I said
  it wasn't legal" (story.md's "Mind Read gets the truth out of a purser", finished out loud); the nought's eighteen hundred
  coins (twelve hundred to the Guild, two hundred for the debt, four hundred to the crew), the crew's one-coin fine,
  and Bronze rank for "Corvin's crew".
- **The five contracts:** the Bilge King and its bucket; Pim's cashbox; the ice house and the frozen fish named
  Corvin; the Guild's old hold and Penhallow's dry boots; the bell-rope and Tibbs's swing.
- **The wanted posters:** the figures (Corvin 5,000, Tamsin 1,200, the diver 800, the cartographer 300) and the
  charges; the portraits (Corvin's jaw like an anvil and Wurmple eyebrows, the worst; Tamsin's a good likeness; the
  diver a fish; the cartographer a map case with legs); the order's licence desk on the Bazaar and its clerk (like
  mission 2's Tidewarden notice in Fallhaven, the order's word reaching past the Galeway though its ships don't);
  the three posters made after Bastion Rock reaching Crew 1 by Runner Pell, then every Tidewarden board in the Calm,
  while the cartographer's, drawn the same afternoon, stays on the Bazaar for now; Gary's line.
- **Crew 1's lines** in scene 16: "That's a terrible likeness", "a potato with a grudge", Vesper's "For that, I'd
  think about it. ...Briefly" and "That's not a fire's price. That's a storm's", Maren's "Three Adepts. One short of
  us. For now", "ready for weather".
- **The narration's last line,** "And neither knew how soon they would need each other", a seed for mission 9.
- **The Trio's details** (Eggs, above), including their fake Farer relics and the delivery as oranges.
- **The rewards:** the Dawn Stone, 400 coins (the heist purse), the contracts' 390 coins, the Turtle Boots (items
  §13's artifact list) and the fights' purses.

## Changes to the build

**Rooms**
- **`tradewind_bazaar`** re-clipped larger from Golden Sun 2's Lemurian ship (room 42) and other Lost Age decks, the
  builder's pick, with painted sea and painted far hulls round three walkable ones, the hulls a beat happens in
  (decision 5):
  - **The Guild hull:** the landing (entrance 0) with Ketch and the landing steps; Tally's desk with the scales; the
    board; Wynn's bollard (slot 9); the bench; the Guild's bell with Absalom, Rook and the Aipom; The Hammock's
    hammocks between its masts, with Hettie; and the hatch down to its old hold (G4), drawn dark until lit.
  - **The market hull,** joined to the Guild hull by a plank bridge: the counting table with Plumb and Dabney (slot
    8); Calloway's, Ottoline's, Ossery's and the relic stalls; Pim's and Gudrun's stalls with the ice tub; Bunce's
    open grain hold with the Bilge King; the yard with Tibbs and the swing; the licence desk with the clerk and the
    posters at its west end; and the spar and its sail (slot 10) on the rail facing Hull Nine.
  - **Hull Nine,** across a gap of water: its bow sign, the chained gangplank, the collateral crates, the orange crate,
    the pen, and the deckhouse with the strongbox (slot 11). Her sides are sheer, with no steps, so Surf never boards
    her.
  - The lanes round the hulls are on the surf layer (Pim's barrel). Every other hull stays painted backdrop. Slot 12's
    merchant gives way to the named people; today's gangway warp goes (Ketch's scene sails instead).

**Actors and engine**
- **The rest hook and the resume scene** (mission 7's), for scenes 1 and 16, on `m5_done`, `m6_done` and `m7_done`.
- **The ending:** today's gangway scene comes out. Scene 15 ends with `resume_crew 1`, and today's `when` step that
  starts mission 9 from the gangway moves to mission 9's page.
- **The dial** (decision 6): a new step, `[dial]`, three rings of 0 to 9 and A to try; the right code (7, 3, 9,
  held in the scene) plays the rest of the scene, a wrong one its line. Any number of tries.
- **Mind Read** on our actors, as built, with each thought written `**Name, thinking:**` (README §2) and shown with
  the name tag; the swing's text and its yes/no follow `m8_tibbs_read`.
- **Whirlwind** on the sail, as built; the staged gust of scene 10 is the `light` step and walks.
- **Wynn's recruit:** `recruit wynn` at L9 with Ralts and her kit (a staff, equipment decision 11), on Golden Sun's
  Sky class line and Summons (Ivan's), as decisions 17 and 18 keep Golden Sun's names; Corvin's L9 floor (progression
  1). She keeps her borrowed field sprite until art part B2.
- **`tumbleweed_trio`** (new): Bramble's Seviper and Burr's Ferroseed, about L9 each (proposed; slice 10 measures
  it), as a Pokémon-only trainer fight if the battle system allows one, or two units with no Adept; Scratch doesn't
  fight. "Try again" with Tamsin's line, and scene 10 as its `scene_after`.
- **`bounty_bilge_king`** (new): an alpha of one of Golden Sun's rat monsters (the builder's pick from the
  bestiary), about L10, with Nerissa's retry line and G1's win.
- **Coins:** `take_coins 1` and coins in `give` (mission 3's) for the ruling and the contracts.
- **The board:** one row whose menu lists the five notices, each with its DONE page once its flag is set (text by
  state, mission 1's recommendation).
- **The orange crate:** a Move event that only shows its line and never moves.
- **The Guild's old hold:** drawn dark until `m8_hold_lamp` (a tint over the hold's cells, the `light` step's), the crate
  and the glint showing from it, and the chest's row from `m8_c_hold`.
- **Frost with a flag gate:** the ice tub sets `m8_c_ice` only from `m8_guild` (mission 4's `if_flag` with
  `else_text`).
- **Hettie's inn** at Eastwater's rest price, on items §12's ladder.
- **The shops:** Ottoline's stock and Ossery's buying and Artifacts list in `data_src/shops.json` (items §11's
  Bazaar row).
- **The posters:** rows on the licence desk's board (three, then a fourth from `m8_cleared`); a last page on `stonehollow`'s
  notice board, `canalport`'s Tidewarden notice and `eldergrove`'s tithe notice from `m8_posters`, with Maren's line
  the first time each is read; Gary's line in Stonehollow from `m8_posters`.
- **Ketch's yes/no** with a condition on the five contract flags.
- **`{LEADER}`** in every system line here.
- **Wynn, Ralts, Plumb, Dabney, Tally, the Trio and their Seviper and Ferroseed, the Bilge King, the Aipom, Tibbs,
  Pell and the posters** as actors scenes can move.

**New scene steps** (README §2): `phase`, `light` (Mind Read's shimmer, the gust, the spotlight, the twinkle, the
hold's dark), `camera`, `pose` (flourish), `choice` (Corvin's two beats, with no quiet set), `crew out` and `crew in`,
`dial`, step-on triggers (scenes 6 and 11), Psynergy-flag triggers (scenes 4 and 5), the rest-hook and resume
triggers (scenes 1 and 16), and yes/no menus (Ketch, the swing).

**Checks.** `tools/mission8_check` follows the new flow from a rest after the second recruitment: the handover, the
arrival, Wynn's reply menu, Dabney's thought, the bow, the sail-bridge and Wynn's crossing, the crates (the orange
crate won't move), the dial (a wrong code holds, the right one opens), the Dawn Stone in crew 2's bag, the Trio and
their retry line, the gust, the way back, the ruling (a coin out, 400 in, the notice gone, Bronze), the chart's reply
menu, each contract done and paid, Ketch's warning while a contract is open, the departure and `m8_done`; then Crew 1
back where it rested, with Pell, the posters and `m8_posters`, and the posters on the three boards.
