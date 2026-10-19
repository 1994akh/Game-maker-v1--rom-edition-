# Mission 10: The Two-Earth Door

> **Status:** draft for your yes or notes (19 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 10, §8 (home, the ship and the Log) and §9a (Cidrick, "A Funeral at Sea").
> Today's build: [mission-10-build.md](../../design/mission-10-build.md); the crews' rules: party-and-battle.md §1.

| | |
|---|---|
| Mission | 10, The Two-Earth Door (Act I's ending, part two; the demo's last mission) |
| Plays after | Mission 9's landing at Stonehollow ([mission-09.md](mission-09.md), scene 20), straight on |
| Crew | Crew 1 is played. Corvin's crew stands beside it as actors until the muster roll (scene 9); from there, crew swapping and trading (party-and-battle.md §1, as built) |
| Rooms | `stonehollow` (the cove, the memorial stone, the refugees), `vault_halls` (the inner door chamber, with the landing behind the door), `wayfarer_berth` (new: the sea cave under Stonehollow), `wayfarer` (re-clipped: the deck, the engine's well and the chart room; berthed in the sea cave until dawn, then at anchor in Stonehollow's cove), `wayfarer_galley` (new), `wayfarer_quarters` (new: eight bunks and the ship's bunk, decision 34), `hero_house` (free play) |
| Clock | Day from the landing; dusk at supper; night in the quarters; dawn when free play begins. The Kestrel's send-off (optional) sets dusk |
| Flags in | `m9_done` |
| Flags out | `m10_intro`, `m10_stone`, `m10_vault_in`, `m10_asked`, `m10_door`, `m10_berth_in`, `m10_shingle`, `m10_gangway`, `m10_ship`, `m10_cradle`, `m10_log`, `m10_muster`, `crew_swap`, `m10_supper`, `m10_night`, `m10_talk_corvin`, `m10_talk_maren`, `m10_talk_sorrel`, `m10_talk_vesper`, `m10_talk_tamsin`, `m10_talk_nerissa`, `m10_talk_wynn`, `m10_done`; and, optional, `m10_glint`, `m10_cidrick`, `m10_funeral`, `m10_cache` |
| Unlocks | The Wayfarer: her helm sails the Calm on sea trials, and offers the maiden voyage, which ends the demo (decision 20); crew swapping and trading (`crew_swap`); one bag and one purse; the Farer's Log, its tabs filled from records kept since mission 1 (decision 32); the Lodestar stirred in its cradle (story decision 1); the ship's bunk in the quarters (decision 34); Marta's shop reopened on Marrow Isle (items §11) |
| Reply beats | 2: Corvin at the inner door (scene 4); Brann at supper (scene 10) |
| Fights | None |
| Leads into | Free play in Act I. At the Wayfarer's helm the maiden voyage plays the end card, the credits and the save prompt, and returns to the deck (decision 20). Mission 11, the Breaking, comes after the demo |

**The flow.** Later that morning, with the Holdfast gone, Corvin's crew climbs out of Ketch's nets in Stonehollow's
cove, and Brann meets the boy who hatched his eggs in his boots. He cuts Sael's name on the memorial stone, and
Fallhaven's and Saltcombe's under it, and then, for the first time in forty years of keeping it, lets the inner door
be opened: "Two keepers stand where one cannot." In the chamber where they fought on Keeping Night, Corvin asks
{HERO} again, and the two Earth Adepts open the door together. Behind it a warded stair breathes once, red, toward
the Sleeper, and a second stair goes down to the sea. In a cave under Stonehollow lies the Wayfarer, a Farer ship
with sails folded along her sides like wings, just as Wynn saw from her mother's window. Her engine wakes on the
open Flame Well, the Lodestar stirs in her cradle, and the Farer's Log writes itself full of everything the crews
have seen. Wynn puts both crews on the muster roll, the bags go into one hold, and crew swapping opens. Brann comes
down six hundred steps for supper, the table drinks to Sael, and Brann asks {HERO} what they are now. That night
each Adept has a word with {HERO} from their bunk. In the morning the Wayfarer lies at anchor in the cove, and Act
I is open: both crews, the Calm on sea trials and, at the helm, the maiden voyage, which plays the end card. If
the crews want it, the cracked Kestrel gets a burning send-off at dusk, with Ketch's funeral song finished at last.

## Scenes

### 1. Nets

- Room: `stonehollow`, the cove. Trigger: straight on from mission 9's landing (or entering the cove once
  `m9_done`, unless `m10_intro`). It replaces the second half of today's `refugees_settle`.

*[phase day] [fade in 40] Later that morning, in Stonehollow's cove. The Holdfast's sails go out round the point,
white against the sea, and are gone. The cove is all noise: Rimborn carrying bundles up the path, villagers carrying
them back down to help, Nell handing out Herbs, Maudie handing out pie. The Kestrel lies hauled up on the shingle,
her keel cracked. On Ketch's skiff the heap of nets hasn't moved. Ketch sits on top of it, eating. [crew out]*

**Ketch:** She's gone. You can stop being
nets now.

*The nets heave. Corvin climbs out in Sael's coat, then Tamsin, then Nerissa, and last of all Wynn, with a net still
round one ankle. [show Corvin, Tamsin, Nerissa and Wynn]*

**Wynn:** Two days a net. I've forgotten how
to be a person. Which way up do
people go?

**Tamsin:** As nets go, three out of ten.
Too lumpy.

*Corvin stands on the jetty and looks up the cove path: the village, the Keeping Stone, the hatchery roof, the
Vault road climbing the hill behind. He doesn't move. Brann is coming down the path with a basket of blankets. He
sees Corvin, and stops. [walk Brann → the foot of the path] [emote Brann: exclaim] [wait 40]*

**Brann:** ...You're late.

**Corvin:** Five years late.

**Brann:** Hm. You've grown. Not much.

*[walk Corvin → before Brann]*

**Corvin:** I'm sorry about your halls. And
your seal-bar. And your floor. And
the Sleeper.

**Brann:** You broke my bar, split my floor
and stirred the Sleeper. On Keeping
Night.

*[wait 30]*

**Brann:** Come here.

*Brann puts the basket down and takes Corvin in both arms, coat and all. [pose Brann: embrace] [emote Corvin:
silence] [wait 60]*

**Brann:** Eggs in your boots. Every spring.
I never once caught you.

**Corvin:** You did. You let me.

**Brann:** ...Hm.

*[pose Brann: stand] He looks at the coat.*

**Brann:** That's a captain's coat.

**Corvin:** Sael's. She held the archive's
doors so we could read a book. She
didn't come out.

*[wait 30]*

**Brann:** Then she goes on my stone. Today.

*[flag m10_intro] Straight on to scene 2.*

### 2. The stone

- Room: `stonehollow`, the memorial stone. Trigger: straight on from scene 1.

*[fade out 20] [fade in 20] The memorial stone by Old Moss's bench. Brann kneels at it with a chisel and a mallet,
his knees complaining. Corvin stands over him. Both crews wait a little way off, and some of the Rimborn with them.
Old Moss has given up his bench to Old Jory. [pose Brann: kneel] [crew out]*

*Brann cuts, slowly. [shake 5, 1] [wait 20] [shake 5, 1] [wait 20] [shake 5, 1]*

**Sign:** FOR THOSE THE SEA KEPT. And,
new-cut, the chips still white:
CAPTAIN SAEL, OF FALLHAVEN.

*[walk Ossian → beside Brann]*

**Ossian:** Keeper. Would you cut Saltcombe
on it too? Nobody ever has.

**Brann:** ...There's room. There's always
room on this stone. That's the
trouble with it.

*He cuts two more names under Sael's, smaller. [wait 40] [pose Brann: stand]*

**Sign:** And under the captain, smaller:
FALLHAVEN. SALTCOMBE.

**Ossian:** There. The stone says it now. I
don't have to say it on my own.

**Corvin:** Thank you.

**Brann:** Don't. You'll come home for
supper. Both of you. That's how you
thank a keeper.

*[face Corvin → {HERO}]*

**Corvin:** {HERO}. You heard Old Jory's
song at Fallhaven. "Under the
marrow, under the stone."

**Corvin:** Under the marrow: Marrow Isle.
Under the stone: the Vault.

**Old Jory:** Sleeps a ship to carry us home.
My gran sang it, and hers. Nobody
knows what it means.

**Corvin:** I think I do. I've thought so for
five years. It's why I came back on
Keeping Night.

*[face Brann → Corvin] [emote Brann: squint]*

**Brann:** Keepers are never told what's
behind the inner door. Only to keep
it shut.

**Brann:** Forty years I kept it. I never
once asked what it was for.

*[wait 30]*

**Brann:** Maybe it's time somebody asked.

**Brann:** Go on, then. Both of you. Two
keepers stand where one cannot.

*[walk Corvin, Tamsin, Nerissa and Wynn → the north gate] [hide them] [crew in] [flag m10_stone] Control returns.
The Vault road is open, and Corvin's crew has gone up ahead.*

### 3. The upper halls

- Room: `vault_halls`. Trigger: entering, once `m10_stone`, unless `m10_vault_in`.

*[fade in 30] The Vault's upper halls as Keeping Night left them: the seal-bar snapped on the threshold, the pillar
drum wedged in the split floor, the two small stone keepers on their sockets with their eyes still glowing amber. Far
below, the underground river. Corvin's crew waits in the Sentinel gallery. [show Corvin, Tamsin, Nerissa and Wynn]
[crew out]*

**Corvin:** I broke all this. In one night.
You should see what I can do with a
week.

**Tamsin:** I've seen. There was a monastery.

**Vesper:** And a fortress, the posters say.

**Corvin:** ...Fair.

*[walk Corvin, Tamsin, Nerissa and Wynn → the inner door chamber] [hide them] [crew in] [flag m10_vault_in] Control
returns.*

### 4. The question

- Room: `vault_halls`, the inner door chamber. Trigger: talking to Corvin (slot 12), once `m10_vault_in`, unless
  `m10_asked`.

*The inner door chamber. The door is a slab of dark stone, two handprints cut side by side into its seal. Along the
east wall, the gap where the floor fell on Keeping Night, and the river loud below it. Corvin stands where he stood
that night, his palm a hand's width from the east print, not touching it. Tamsin, Nerissa and Wynn wait by the
chamber's mouth. [face Corvin → {HERO}] [crew out]*

**Corvin:** Last time we stood here, I asked
you to open it with me. You said
no. Then you hit me.

**Corvin:** I deserved it. I'd broken your
seal-bar.

**Corvin:** So. I'm asking again, properly.
Will you open it with me?

**{HERO} replies:**

1. "Together." · quiet: (Nod)

   **Corvin:** Together. I've waited five years
   to hear that word in this room.

2. "If this is a trick..." · quiet: (Shake head)

   **Corvin:** Then you can push me in the
   river. I'll go quietly. I know the
   way.

3. "What's behind it?" · quiet: ...

   **Corvin:** A song, and a hunch. And if I'm
   wrong, a very old cupboard.

*Every reply rejoins here.*

*[walk Corvin → the east print] He lays his palm flat on it. [light: the east print glows a faint amber] [crew in]
[flag m10_asked] Control returns. The west print waits for {HERO}'s Move (puzzle 1).*

### 5. The Two-Earth Door

- Room: `vault_halls`, the inner door chamber. Trigger: Move on the inner door's west print (slot 11's Psynergy
  event), once `m10_asked`, unless `m10_door` (today's `inner_door`, rewritten). Before `m10_asked`, its refusal
  line (People and signs).

*[crew out] [pose {HERO}: a hand on the door] {HERO} lays a palm on the west print and pushes, with the mind, not
the back. [light: amber on both prints] Beside {HERO}, Corvin pushes too. [shake 40, 2] The amber runs out of the
two prints and along the seal's carved lines until the whole door glows with it.*

**Corvin:** It knows us.

*[shake 60, 3] The door splits down the middle and grinds open, each half sliding back into the walls. [gate: the
door's cells open] Cold air comes out of the dark behind it, and the smell of the sea.*

*Behind the door is a landing of dressed stone. On the left a stair goes down into the dark, and the sound of the
sea comes up it. On the right a second stair spirals down out of sight, closed by a curtain of dull red light that
fills its arch from side to side. [camera → the warded stair] [camera back]*

*[wait 30] The red curtain brightens, slowly, and dims. Once. Like breathing. [light: a single slow red pulse from
the warded stair] [shake 30, 1] Everyone holds very still.*

**Wynn:** Did that just... breathe?

**Nerissa:** Slowly. Like something asleep, very
deep down.

**Corvin:** The Sleeper. On Keeping Night it
turned over. Now it's settled.

**{HERO}:** Let it sleep.

*Quiet: [emote {HERO}: silence] and no line.*

**Corvin:** Not that stair. The other one.

*[walk Corvin, Tamsin, Nerissa and Wynn → down the sea stair] [hide them] [crew in] [flag m10_door] Control returns.
The sea stair goes down to the berth. The warded stair won't open (People and signs).*

### 6. The berth

- Room: `wayfarer_berth` (new). Trigger: entering, unless `m10_berth_in`.

*[fade in 30] A sea cave under Stonehollow: a long hall of wet black rock, its roof lost in the dark, the sea
breathing in and out through a mouth far off where a grey light shows. Below the stair, a quay of dressed stone runs
along the cave wall, older than the Vault's halls and carved with the six marks. Corvin's crew stands on the last
dry step above it. [show Corvin, Tamsin, Nerissa and Wynn] And at the quay, riding the black water, there is a
ship.*

*She is long and low, her hull a pale grey wood that shines in the lantern light, her masts bare, her sails furled
along their yards. Down each side, folded flat against the hull like a bird's at rest, lie two long fins of
sailcloth on ribs. [camera → the ship] [camera back] [crew out] For a while nobody says anything.*

**Wynn:** Oh.

**Wynn:** Oh, she's one of them. Sails like
wings. From the window. My mother
showed me ships like her.

**Wynn:** I said. I always said, and nobody
ever believed me.

**Corvin:** Under the marrow, under the
stone.

**Tamsin:** Ten out of ten. Nobody gets a ten
after this. I've decided.

**Sorrel:** That wood isn't dead. It's
asleep. I can feel it from here.

**Vesper:** And not a ghost on her. ...That's
disappointing.

*[crew in] [flag m10_berth_in] Control returns. The stair's last flight is buried in shingle (puzzle 2), and the
ship's gangway swings over the water on its chain (puzzle 3).*

### 7. The Wayfarer

- Room: `wayfarer`, the deck. Trigger: boarding by the gangway, unless `m10_ship` (today's `wayfarer_found`,
  rewritten and split into scenes 7 to 9).

*[fade in 30] The Wayfarer's deck: pale grey planks, smooth as river stone; brass fittings gone green. Aft, a wheel
taller than a man. Amidships, a hatch with a brass grating over it, and under the grating, nothing but dark. At the
stern, a cabin door with a window of blue glass. Both crews come aboard. [show Corvin, Tamsin, Nerissa and Wynn]
[crew out]*

*Under the grating, something takes a breath. [light: red, brightening through the grating] A low hum comes up
through the planks into everyone's boots. [shake 10, 1] [emote everyone: exclaim]*

**Tamsin:** That's fire. Down there. ...I know
that fire.

*[walk Tamsin → the grating] [pose Tamsin: kneel] [camera → the grating] Below it, in the engine's well, six chambers
of thick glass stand in a ring round a heart of brass. Five are dark. In one, a flame burns, red and gold.*

**Tamsin:** That's the Well's fire. Ours. The
Forgeheart's, in a glass jar,
running a ship.

**Corvin:** The Flame Well. I opened it, and
it burned down a monastery.

**Tamsin:** And now it's in a ship. That's a
nine, Landslide. I'm being
generous.

**Wynn:** Six chambers. Six Wells. She runs
on what's open, and one is.

*[camera back] Ketch has come down the stair after them. He stands on the quay with his mouth open and an apple in
his hand. [show Ketch] [walk Ketch → the gangway's foot]*

**Ketch:** One's plenty. Out in the Wide
there are the Stillwaters. Dead
calm. No wind. No current.

**Ketch:** Boats sit in them till they're
bones. Not her. Not with a fire in
her belly.

**Corvin:** Does she have a name?

*[walk Wynn → the bow] [pose Wynn: lean over the rail] [emote Wynn: sweat]*

**Wynn:** There's letters on the bow. I can't
read the top ones. Nobody reads
Farer.

**Wynn:** But somebody's cut plain letters
under them. Old ones. They say
WAYFARER.

**Corvin:** The Wayfarer.

*[crew in] [flag m10_ship] Control returns. The chart room is at the stern; the muster roll stands by the
mainmast.*

### 8. The cradle and the Log

- Room: `wayfarer`, the chart room. Trigger: talking to the chart table (slot 11), once `m10_ship`, unless
  `m10_log`.

*The chart room: a stern cabin under a window of blue glass, with a chart table of the same grey wood, and on the
table a brass cradle cut to the exact shape of a compass. Beside the cradle lies a book bound in blue-grey leather,
the six marks pressed into its cover. [crew out]*

**Wynn:** That's a cradle. For a compass.
That size. That exact size.

*Everyone looks at {HERO}. {HERO} takes out the Lodestar and sets it in the cradle. It fits as if it had never left.
[pose {HERO}: set the Lodestar down]*

*[wait 40] [light: a faint blue glow round the cradle's rim] The needle of blue glass shivers. It swings once, a full
turn, slowly, like something stretching in its sleep. Then it settles, trembling, pointing at nothing. [shake 10,
1]*

**Maren:** It moved.

**Corvin:** Brann's had that since before his
grandmother. It never once moved.

**Sorrel:** It isn't awake. It's stirring.
Like the wood.

*[flag m10_cradle]*

**System:** The Lodestar stirred in its
cradle. It still points nowhere.

*In the blue light, the book beside the cradle falls open on its own. [walk Wynn → the table]*

**Wynn:** The first half's Farer. I can't read
a word of it. Look at the charts,
though. Look at them.

**Wynn:** Then blank pages. Hundreds of them.
Wait. They aren't blank. They're...

*[light: ink spreading across the pages] On the blank pages, ink comes up through the paper like a stain through
cloth: drawings, names, lines in a small neat hand.*

**Wynn:** It's writing! It's writing itself!
That's Canalport! That's the reef!
That's a Marill!

**Nerissa:** That's the Bazaar. How does it
know about the Bazaar?

**Corvin:** It's a Farer book. I've stopped
asking how.

**Maren:** It's been keeping notes. All this
time. On all of us.

*[wait 30]*

**Maren:** ...I know how that sounds.

**Vesper:** From you? Yes.

*[emote Maren: sweat] Wynn turns back to the last of the Farer pages. Under the Farer script, in the same old plain
letters as the bow, there is one line.*

**Wynn:** There's one line I can read. Plain
letters, like the bow.

**Log:** To whoever finds her: keep the
Log. We will come back when it is
complete.

**Corvin:** Come back. From where?

*Nobody answers. Wynn looks up through the blue window, as if she could see the sky through the rock.*

*{HERO} lifts the Lodestar back out of its cradle. Its needle drifts, and goes still. [give Farer's Log] [flag
m10_log]*

**System:** {HERO} received the Farer's Log!

**System:** It keeps both crews' records: Kin,
Bestiary, Charts, Relics and
Cultures.

**System:** And the Guild Ledger and your
Bearings. Open it from the Start
menu.

*[crew in] Control returns.*

### 9. The muster roll

- Room: `wayfarer`, by the mainmast. Trigger: talking to the muster roll (slot 12), once `m10_log`, unless
  `m10_muster`.

*A board of the grey wood by the mainmast, ruled in two columns. At the top of each, faded Farer letters; under them,
empty lines. A stick of chalk hangs from it on a cord, as if somebody meant to come back and fill it in. [crew
out]*

**Corvin:** A muster roll. Two columns. Two
crews. One ship.

**Tamsin:** Put me at the top. I hit the
hardest.

**Wynn:** Let me. My hand's the neatest.
Nobody argue. Nobody's hand is
neater than mine.

*[walk Wynn → the roll] [pose Wynn: write] She writes fast and small, in two columns: Corvin's crew on one side,
{HERO}'s on the other, and the two leads at the top, side by side.*

**Wynn:** There. Two keepers, standing where
one can't. The keeper said it, so
it goes on the roll.

**Nerissa:** And the bags. Two crews, two bags,
two purses, on one ship. That's
silly.

**Maren:** Everything into the hold, then.
I'll do the inventory. I like an
inventory. It isn't a report.

*[fade out 20] [merge bags] [fade in 20] Both crews' packs lie open on the deck, and Maren is writing a list.*

**System:** The two crews' bags and purses are
one now.

**Maren:** Your crew carries one linking
cord, one Dawn Stone and a great
many biscuit crumbs.

**Tamsin:** Your crew carries a great many
Herbs.

**Maren:** Herbs first. Always Herbs first.

*[flag crew_swap]*

**System:** Crew swapping is open. The crew
you aren't playing waits on Marrow
Isle, its lead in Stonehollow.

**System:** Talk to the waiting lead to take
over, or to trade Adepts. The muster
roll trades them too.

**Corvin:** Your crew, my crew. Swap whoever
you like. Only the two of us stay
put.

**Corvin:** Somebody has to stand at the top
of each column.

*[crew in] [flag m10_muster] From the galley hatch, a shout:*

**Ketch:** Supper! Fish stew! Come down
before I eat it all!

*Control returns. The galley is below, down the hatch by the mainmast.*

### 10. Supper

- Room: `wayfarer_galley` (new). Trigger: entering, once `m10_muster`, unless `m10_supper`.

*[phase dusk] [fade in 30] The galley: a long table of the grey wood with benches down both sides, and a stove of
Farer brass that Ketch has somehow lit and is very pleased about. Both crews crowd onto the benches with a bowl each.
[show Corvin, Tamsin, Nerissa and Wynn] [crew out]*

**Ketch:** Fish stew. Rimborn recipe. The
recipe is: fish.

**Tamsin:** Six out of ten. Seven with bread.

**Ketch:** There's no bread.

**Tamsin:** Six, then.

*Boots on the ladder, slow and heavy, and a good deal of muttering. Brann comes down into the galley one rung at a
time, a pie in a cloth under one arm. [show Brann] [walk Brann → the head of the table]*

**Brann:** Six hundred steps to a ship. My
knees will be writing to you both.
Separately.

**Brann:** I said supper. I didn't say
where.

*He sets the pie down in the middle of the table. [emote Wynn: heart]*

**Maren:** Maudie's.

**Brann:** It's always on.

*[wait 20] Nerissa leans across the table and puts the braided cord into Vesper's hand.*

**Nerissa:** The linking cord. I said one day
somebody's Pokémon would want it
more than mine does.

**Nerissa:** A Haunter, they say. Yours is a
Gastly. It'll grow.

*[emote Gastly: heart]*

**Vesper:** Gastly doesn't want anything.

*[wait 20]*

**Vesper:** ...Gastly wants that.

**Brann:** Ketch tells me my compass moved.

**Wynn:** It turned right round! In a cradle!
And a book wrote itself! I can show
you the book!

**Brann:** Six keepers carried that compass
before me. It never moved for one
of us.

**Brann:** It was waiting for the ship, not
for you, apprentice. Don't let it
go to your head.

*[wait 30] Corvin stands, with his cup. The table goes quiet.*

**Corvin:** To Sael.

**All:** To Sael.

**Brann:** To the captain.

**Ketch:** I finished the song, you know.
The funeral one. ...Not tonight.

*[wait 30] Brann turns to {HERO}.*

**Brann:** Well, apprentice. You went out a
deputy. You've come home with a
ship and a seal-breaker.

**Brann:** So. What are you now?

**{HERO} replies:**

1. "Still your apprentice." · quiet: (Nod)

   **Brann:** Hm. You'll always be that. It's
   not an answer. I'll take it.

2. "Not just a keeper." · quiet: (Shake head)

   **Brann:** No. Not just. A keeper, a deputy
   and a friend of seal-breakers. A
   busy year.

3. "I don't know yet." · quiet: ...

   **Brann:** Good. Nor do I. That's where the
   good keepers start.

*Every reply rejoins here.*

**Brann:** Eat your pie. That's an order.
Mine outranks the Commodore's, at
this table.

**Corvin:** Since when?

**Brann:** Since the table.

*[crew in] [flag m10_supper] [fade out 30]*

**Narration:** Later, Brann went back up the six
hundred steps, complaining all the
way. The crews went below to sleep.

*[phase night] [warp wayfarer_quarters, entrance 0]*

### 11. The first night

- Room: `wayfarer_quarters` (new). Trigger: entering, once `m10_supper`, unless `m10_night`.

*[fade in 30] The quarters: eight bunks of the grey wood down both walls, each with a curtain and a little lamp.
Tamsin has already claimed the biggest. Vesper has slung a hammock between two hooks instead. [crew out] Each Adept
goes to a bunk and stays there for the night (the first night's rows, below). {HERO}'s bunk is at the end, beside
Corvin's.*

**Corvin:** Eight bunks. Exactly eight. Do
you ever feel like somebody
planned this?

**{HERO}:** Every day, lately.

*Quiet: [emote {HERO}: sweat] and no line.*

**Corvin:** Talk to whoever you like. I'll be
on the end bunk, being quiet. It's
a new thing I'm trying.

*[flag m10_night] Control returns. Each Adept's bunk plays that Adept's talk, once (the talks, below). {HERO}'s own
bunk ends the night (scene 12).*

### The talks (the first night)

Room: `wayfarer_quarters`, each Adept at their bunk. Trigger: talking to the Adept, once `m10_night`, unless that
talk's flag. All seven are optional and can come in any order; each sets its flag and plays once (decision 5's "one
talk per Adept"). From `m10_done`, the bunks give the free-play lines instead (People and signs).

**T1. Corvin** (`m10_talk_corvin`)

*Corvin sits on his bunk with Sael's coat across his knees, picking at a burn on its sleeve.*

**Corvin:** She burned this sleeve on a lamp,
the winter I came. Never mended it.
"It's a reminder."

**Corvin:** Of what, I asked. Of not leaning
on lamps, she said.

*[wait 30]*

**Corvin:** I keep thinking she'll come down
that ladder and tell me my bunk's a
disgrace.

**Corvin:** It is a disgrace. Look at it.

*[wait 30] [face Corvin → {HERO}]*

**Corvin:** You came. I asked, and you came.
I'd never asked anybody for
anything.

**Corvin:** When this is over, I'm going back
to the rim. There's a post there
that says THE EDGE WAS HERE.

**Corvin:** I want to put up one that says
something else. I don't know what
yet.

**Corvin:** You'll help me think of it. You
always had the good words. I just
had the loud ones.

*[flag m10_talk_corvin]*

**T2. Maren** (`m10_talk_maren`)

*Maren sits on her bunk with a new notebook open on her knee, a pencil in her hand. The page is empty.*

**Maren:** I bought a new notebook from Nell.
Herbs first, she said. Then she sold
me the notebook.

**Maren:** I've sat here an hour. I don't know
what to write when nobody's going
to read it.

**Maren:** Every page I ever wrote, I wrote
for someone. The order. The Lord
Warden.

*[wait 30]*

**Maren:** You have the old one. My reports.
Whatever you decide to do with
them, I'll stand by it.

**Maren:** If I ever write for the order
again, it'll be something it has to
read. Rules. Better ones.

**Maren:** ...I'll start with a list. I always
start with a list. It's how I know
I'm still me.

*[flag m10_talk_maren]*

**T3. Sorrel** (`m10_talk_sorrel`)

*Sorrel kneels on her bunk with her palm flat on the wall beside it and her eyes shut. Rowlet sits on her head.*

**Sorrel:** Shh. Listen.

*[wait 40]*

**Sorrel:** It's alive. The whole hull, under
the polish. Asleep, like the tree
was before the spring.

**Sorrel:** I could wake it. Not with Growth.
With something I haven't got yet.

*[wait 30] She takes her hand off the wall.*

**Sorrel:** We buried the Forest seal on the
order's word. Your Earth. My roots.
You were there.

**Sorrel:** That Ledger says every seal drinks
its Well. We made that one drink
harder.

**Sorrel:** One day I'm going back to undo it.
And to plant something in the ash
where the groves burned.

**Sorrel:** Don't tell anyone I said that.
Especially the Elder.

*[flag m10_talk_sorrel]*

**T4. Vesper** (`m10_talk_vesper`)

*Vesper lies in her hammock, slung between two hooks over a perfectly good bunk, one boot over the edge, Gastly curled
on her chest with the linking cord round it like a scarf.*

**Vesper:** I don't do bunks. Bunks are for
people who expect to wake up in the
same place.

**Vesper:** Not a ghost on this ship. Six
hundred years. ...I checked twice.

*[wait 30]*

**Vesper:** That Ledger. A street a year, paid
by the edge. And the islands that
wouldn't pay?

**Vesper:** I knew one. I told you that.
...Not tonight. Old weather.

*[wait 20]*

**Vesper:** There's fog out past the Galeway
that never lifts. One day I'll take
you into it.

**Vesper:** Not as a client. I'll still send
you the bill.

*[flag m10_talk_vesper]*

**T5. Tamsin** (`m10_talk_tamsin`)

*Tamsin is doing press-ups beside her bunk, counting under her breath. She stops at a round number.*

**Tamsin:** Ninety. The abbot made us do a
hundred before bed. I'm leaving ten
for the Forgeheart.

**Tamsin:** That fire in the engine is ours.
The Well's, I mean. I'd know it
with my eyes shut.

**Tamsin:** Our sacred flame went up with the
bird. The brazier's cold. And here's
its Well, warming a ship.

*[wait 30]*

**Tamsin:** One day I'll go home and light
that brazier again. Properly. Then
the abbot can throw me out.

*[wait 20]*

**Tamsin:** Corvin's captain. Sael. She made me
carry rope for four days, and never
said thank you once.

**Tamsin:** Ten out of ten. I'd have followed
her anywhere.

*[flag m10_talk_tamsin]*

**T6. Nerissa** (`m10_talk_nerissa`)

*Nerissa sits cross-legged on her bunk with her eyes shut, as she sat in her cell. Froakie is asleep in a bucket of
seawater at her feet.*

**Nerissa:** You walk differently since the
cliff. Heavier on the left. That's
all right. It passes.

**Nerissa:** This ship. Wynn says she flew,
once. Sorrel says she's alive.

**Nerissa:** I'd like to know if she can go
down. Under. Where Pearlhollow is.

*[wait 30]*

**Nerissa:** Corvin promised me home, one day.
I said I'd remember it for him. I
have. Every day.

**Nerissa:** No hurry. Divers are patient.
...Mostly.

*[flag m10_talk_nerissa]*

**T7. Wynn** (`m10_talk_wynn`)

*Wynn lies on her front on her bunk with her chart spread out under the lamp, drawing the Wayfarer in its corner.*

**Wynn:** ...and if she's one of the ships
from the window, then the window
was real, which I said. Hello!

**Wynn:** I'm drawing her. For the chart.
Every chart should have a ship on
it, and this one's true.

**Wynn:** Do you know what it's like? Being
right, and nobody believing you,
for years and years?

*[wait 20]*

**Wynn:** ...Of course you do. You went after
Corvin, when everybody said he'd
drowned.

**Wynn:** If she ever flies again, I'm
staying below. In a bunk. Holding
on to something.

**Wynn:** But I'll draw the view. Somebody
should. My mother would want it
drawn.

*[flag m10_talk_wynn]*

### 12. Morning

- Room: `wayfarer_quarters`, {HERO}'s bunk. Trigger: talking to it, once `m10_night`, unless `m10_done` (the ship's
  bunk's first use, decision 34).

**Bunk:** Your bunk, beside Corvin's. Sleep
until morning?

*[yes/no] No: nothing happens. Yes: [fade out 60]*

**Narration:** For the first time since Keeping
Night, {HERO} and Corvin slept
under the same roof.

**Narration:** Deep under the Vault, the Sleeper
slept on. In {HERO}'s pack, the
Lodestar lay still. Mostly.

*[phase dawn] [fade in 40] Morning in the quarters. The bunks are empty and made, all but Vesper's hammock. Through
the hatch comes the sound of Ketch singing in the galley, badly. [crew in] Corvin comes down the ladder. [show
Corvin] [walk Corvin → before {HERO}]*

**Corvin:** Morning. Ketch took her out of the
cave on the tide. She's at anchor in
the cove now.

**Corvin:** Tully's been polishing her since
dawn. He says she's not the
Kestrel. He says she'll do.

**Corvin:** Cidrick looked her over at first
light. Fit for the Calm, he says.
Sea trials first.

**Corvin:** The Galeway's another matter.
When we go, we go with everything
ready. Both crews.

**Corvin:** I'll be in the village when you
want us. So. Where to, {HERO}?

*[walk Corvin → up the ladder] [hide Corvin] [flag m10_done]*

**System:** The Wayfarer is the crews' ship.
Her helm sails the Calm, and her
maiden voyage waits there too.

*Control returns. Free play goes on in Act I (decision 20): both crews, swapping and trading, the Calm on the
Wayfarer, and the maiden voyage at her helm (scene 15).*

### 13. Cidrick (optional, the egg)

- Room: `stonehollow`, the cove's far end. Trigger: talking to Cidrick, once `m9_done`, unless `m10_cidrick` (the
  egg's short staged scene, decision 10).

*At the cove's far end, two trestles and a heap of timber have become a shipyard overnight, with a painted board
leaning on the trestles. A stocky man with goggles pushed up into his hair, a toolbag over each shoulder and a
mallet in his belt is measuring the Kestrel's keel with a knotted string, and tutting. [face Cidrick → {HERO}] [crew
out]*

**Cidrick:** Cidrick. Shipwright. Of Fallhaven,
formerly. Of here, now, it seems.
My family built every ship ever.

**Cidrick:** Every boat on the rim. Every
cutter in the Calm. And most of the
ones that aren't.

**Cidrick:** This one, for instance. My great
uncle built her. ...He'd have built
her better, if they'd asked him.

*[face Cidrick → the Kestrel] [emote Cidrick: sweat]*

**Cidrick:** Her keel's cracked, stem to stern.
The lanes did that. She got you
home first, though.

**Cidrick:** She won't sail again. I'm sorry.
I'd tell you different if I could.
I'm a shipwright, not a liar.

*With `m10_done`:*

**Cidrick:** And that one at anchor. The Farer
one. My family built her too.
Obviously.

**Cidrick:** ...Six hundred years ago. Someone
in my family. Probably. I'll look
into it.

*[crew in] [flag m10_cidrick] Control returns.*

### 14. A Funeral at Sea (optional, the egg)

- Room: `stonehollow`, the cove. Trigger: yes to the beached Kestrel's question (People and signs), once
  `m10_done`, unless `m10_funeral` (§9a's "A Funeral at Sea", decision 10).

*[fade out 30] [phase dusk] [fade in 30] Dusk in the cove, the tide going out. The Kestrel has been floated off the
shingle and rides at the end of a long line, her sails set, her deck heaped with driftwood and old nets. Both crews
stand on the jetty, with half of Stonehollow behind them and what's left of Fallhaven. Beyond, the Wayfarer lies at
anchor, very still. Tully holds the line. [show the crew that isn't played] [crew out]*

**Tully:** She was the fastest hull in the
Calm. I polished every inch of her.

**Tully:** She took us to Canalport, and the
Greenwild, and the reef. To the rim,
and home again.

**Tully:** She wasn't built for the lanes.
She went anyway, because we asked
her to.

*[wait 30]*

**Tully:** Thank you, Kestrel.

*He lets go of the line. The tide takes her. [walk the Kestrel → out on the ebb] Tamsin steps up beside {HERO} and
looks at {HERO}. [face Tamsin → {HERO}]*

**Tamsin:** Ready?

*{HERO} nods. [pose {HERO}: nod] Tamsin points two fingers. [light: a spark across the water] Fire catches in the
driftwood on the Kestrel's deck and climbs her rigging, and her sails go up gold against the dusk. [light: orange on
the water] She sails on out of the cove on the tide, burning, with her own light under her on the water.*

*Ketch walks to the end of the jetty and clears his throat.*

**Ketch:** I wrote this for Corvin. For a
joke. It was going to rhyme with
"drowned".

**Ketch:** It fits her better. Her, and the
captain.

*Ketch sings, and for once he isn't eating. [music: Ketch's song, slow (the music table, decision 37)]*

**Ketch:** Go out on the ebb, old girl,
with your sails all gold and bright.
Go easy, where we can't.

**Ketch:** The captain was the last ashore,
so she's first aboard tonight.
Keep her a place by the rail.

*[wait 40]*

**Corvin:** ...It rhymed and everything.

**Ketch:** Course it did.

*[wait 60] Far out past the point, the Kestrel's light grows smaller, and smaller, and goes out. [light: dusk]
Nobody moves for a long while.*

**Tully:** ...Right. The Wayfarer wants
polishing. Somebody has to.

*[crew in] [flag m10_funeral] Control returns. The Kestrel's place on the shingle is empty from here.*

### 15. The maiden voyage

- Room: `wayfarer`, the helm. Trigger: "The Galeway", the last row of the helm's menu (slot 8, its voyage role,
  rewritten; People and signs), from `m10_done` (decision 20).

*Ketch climbs up out of the galley hatch, wiping his hands, and comes to the helm. [show Ketch] [walk Ketch → beside
the helm]*

**Ketch:** The Galeway. Her maiden voyage.
Both crews aboard, and me calling
the lanes.

**Ketch:** Once we're in, there's no turning
round. Not in that storm. Ready?

*[yes/no] No:*

**Ketch:** Sensible. I'll finish my apple.

*[hide Ketch] Control returns. Yes:*

*[fade out 30] [phase dawn] [fade in 30] The Wayfarer's sails fill. She slides out of Stonehollow's cove on the
morning tide, past the beacon on the eastern headland, with both crews on her deck and Ketch at the bow calling the
lanes. On the jetty, Brann lifts a hand and keeps it up. [camera → the cove's mouth] [camera back]*

**Narration:** On the morning tide the Wayfarer
put out from Marrow Isle, with both
crews aboard.

**Narration:** Ahead, the Galeway stood up out of
the sea like a wall. And somewhere
in it, a single lamp was waiting.

*[fade out 60] [end card] The card, over black, in the title's lettering:*

**Card:** THE BREAKING
To be continued.

*[credits] The credits roll: every maker in [credits.md](../../engine/resources/credits.md), under the title
"HALCYRA. Act I: Open Water". [save prompt]*

**System:** Save your game? It carries on
into the Breaking.

*[yes/no] Yes saves to the file in play (decision 20; the save screen if the player wants another file). Then:
[fade in 40] The Wayfarer's deck, at anchor in Stonehollow's cove, the morning before she sailed: the voyage is still
ahead. The clock is where it was. Ketch leans on the helm, eating an apple.*

**Ketch:** ...Not today, eh? The Galeway's
not going anywhere.

*[wait 30]*

**Ketch:** ...Probably.

**System:** Act I's seas are still open. The
maiden voyage waits at the helm.

*[hide Ketch] Control returns.*

