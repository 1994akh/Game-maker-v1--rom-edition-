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

## People and signs, by room

These are Act I's free-play lines too: from `m10_done` the demo plays on (decision 20), and every row below keeps its
last state for good. While Corvin's crew is played, every line stands as written unless it's marked *Corvin
leading*; none of the others names the lead.

### `stonehollow`

This page takes Stonehollow over from mission 3's "Act I" state and mission 8's posters. *The states:* settling
(`m9_done`, until `m10_done`): the cove full of Rimborn boats and the beached Kestrel, the refugees moving in;
free play (`m10_done`): the Wayfarer at anchor in the cove. Cells are mission 1's; new people give a place instead.

- **Keeper Brann**, slot 8, at the hatchery gate. Settling:

  **Brann:** Rimborn in the inn. Rimborn in the
  hatchery. Rimborn in my porridge
  pot.

  **Brann:** Good. The island was getting far
  too quiet.

  *Free play:*

  **Brann:** A Farer ship in my cove, and a
  seal-breaker at my table. My
  grandmother would have fainted.

  **Brann:** I'm enjoying it. Don't tell anyone.

  *Free play, Corvin leading:*

  **Brann:** Supper's at six. Both of you. I'll
  be counting heads.

- **Brann's Sudowoodo.** Settling:

  **Sign:** The Sudowoodo has a Rimborn child
  hanging off each arm. It is being a
  very good tree.

  *Free play:*

  **Sign:** The Sudowoodo has moved to the head
  of the cove path. It stares at the
  ship. It's never seen a bigger tree.

- **Nell**, at the stall (Marrow Isle's general store from mission 10, items §11; her shop lines are mission 1's).
  Settling:

  **Nell:** Herbs for everyone off the boats!
  Free! Brann said so. ...Brann said
  so once. I'm saying it lots.

  *Free play:*

  **Nell:** Brann says I'm the island's general
  store now. I said I always was. He
  said: patience.

- **Ada**, slot 15. Settling:

  **Ada:** I've hung lanterns all down the
  cove path, so the boats could find
  the jetty. Two hundred and twelve.

  *Free play:*

  **Ada:** There's a Farer ship in the cove,
  and I'm lighting lamps round it.
  Ships like lamps. Everyone knows.

- **Dunstan**, slot 10. Settling:

  **Dunstan:** Forty Rimborn after quarry work,
  and I've got forty picks. Funny how
  these things work out.

  *Free play:*

  **Dunstan:** Corvin fell in my gravel pit twice
  one summer. Now he's found a ship
  under the Vault. Still falling in.

- **Old Moss**, slot 11, standing by his bench. Settling:

  **Old Moss:** I gave my bench to Old Jory. He
  sings. I'll allow it.

  *Free play:*

  **Old Moss:** Three new names on the stone in
  one morning. It's a sad old stone.
  Busy, though.

- **Maudie**, slot 9, at The Quiet Stone (the inn role). Before the rest menu, settling:

  **Maudie:** The Quiet Stone's full to the
  rafters. There's Rimborn asleep in
  the bath. Driest they've been.

  *Free play:*

  **Maudie:** Fen from Fallhaven helps me now.
  She keeps locking all the doors.
  Habit, she says.

  *After resting:* mission 1's line.

- **Fen** (mission 2's innkeeper), at The Quiet Stone's counter. Settling:

  **Fen:** The Quiet Stone. Every bed's level.
  I've checked them all. Twice.

  *Free play:*

  **Fen:** I lock the doors. Maudie unlocks
  them. We're getting on very well.

- **Gary Rivalson**, outside the Rivalsons' house. Settling:

  **Gary:** Refugees? On my island? ...Fine.
  They can have my room. Not my
  partner, though. It's resting.

  **Gary:** Smell you next tide!

  *Free play:*

  **Gary:** A Farer ship! I'd have found it
  myself, but I didn't want to show
  off. Smell you next tide!

  *Free play, Corvin leading:*

  **Gary:** Corvin. Back from the dead AGAIN.
  Some of us only bother being born
  once. Smell you next tide!

- **Corla.** Settling:

  **Corla:** I've never seen the cove this full.
  Or a Commodore's flagship towing a
  wreck in.

  *Free play:*

  **Corla:** There's a ship in the cove the
  size of the inn. Dunstan says that
  about everything. This time, yes.

- **Tobin.** Settling:

  **Tobin:** Pip says Pip's been to the end of
  the world. I've been to the end of
  the jetty. It's not the same.

  *Free play:*

  **Tobin:** Did the Sleeper breathe again? I
  felt it in my bed. I'm being extra
  good. Extra extra good.

- **Tully** (slot 17's voyage row hides from `m9_done`: the Kestrel is beached, and from `m10_done` the Wayfarer's
  helm has the chart). Settling, on the shingle by the Kestrel:

  **Tully:** She got us home. Every one of us.
  I'm going to sit with her a while.

  *Free play:* aboard the Wayfarer (below), and in scene 14.

- **Old Jory** (mission 2), on Old Moss's bench. Settling:

  **Old Jory:** Old Moss gave me his bench. I gave
  him a song. He says it was a fair
  trade. He's lying, bless him.

  *Free play:* aboard the Wayfarer (below).

- **Hanne and Pip** (mission 2), by the hatchery. Settling:

  **Hanne:** Pip is sitting right here until
  we're both very old. Again.

  **Pip:** Is that the Vault up there? Can I
  climb it?

  **Hanne:** No.

  *Free play:*

  **Pip:** Tobin says a Sleeper lives under
  the Vault. I'm going to be good too.
  Mostly.

- **Tanner** (mission 2), at The Quiet Stone's back door. Settling:

  **Tanner:** Maudie's lent me her oven. I've
  still got the bread. Now I've got
  somewhere to put it.

  *Free play:*

  **Tanner:** Bread every morning, at this door.
  Forty years on the east street, and
  now I'm a baker.

- **Ossian** (slot 18, today's "Rimborn refugee"), by the memorial stone. Settling:

  **Ossian:** Saltcombe. Fallhaven. Now this
  place. ...I'm going to try very
  hard to stay in this one.

  *Free play:*

  **Ossian:** The stone says Saltcombe now. I
  still say it. But it's good to have
  help.

- **The Rimborn child** (slot 19), in every state:

  **Child:** Everyone says the captain held the
  doors, right to the end. I'm going
  to be a captain.

- **Wenna** (mission 2). Settling:

  **Wenna:** I brought the pickled eggs. All of
  them. Priorities, dear.

  *Free play:*

  **Wenna:** There's a cellar under my new
  house. Good and dry. I'm not going
  down it. I've learned.

- **Marta** (mission 2). Settling, with a basket:

  **Marta:** Shop's shut. The shop's in this
  basket. Come back when I've found
  a counter.

  *Free play, at her new counter by the inn: she opens Marrow Isle's second shop, with Fallhaven's stock (items
  §11):*

  **Marta:** MARTA'S, again. Herbs, gear and no
  promises. Same as ever.

  *Not enough coins, in the shop:* mission 2's line. *Leaving the shop:*

  **Marta:** Mind the edge. ...Habit. There
  isn't one here.

- **Gannet** (mission 9), by the hatchery with a crate of charts. Settling:

  **Gannet:** Four hundred charts, and I carried
  three hundred and twelve. I count
  the twelve as a win.

  *Free play:*

  **Gannet:** The keeper says I can have the
  cellar under the hatchery, for the
  charts. A library, he called it.

- **Cidrick** (the egg), at his yard at the cove's far end: scene 13. Then, settling:

  **Cidrick:** Her keel's done. I'm sorry. Saying
  it twice doesn't make it any
  easier.

  *Free play:*

  **Cidrick:** That Farer ship. Somebody in my
  family built her. I'm nearly sure.
  I'll have the papers by spring.

- **Ketch**, at his skiff in the cove, eating. Settling:

  **Ketch:** Two crossings in a week. I'm owed
  a nap and a cake. I'll take the
  cake first.

  *Free play:* in the Wayfarer's galley (below).

- **Corvin** (slot 20): scenes 1 and 2 only; the row hides from `m10_stone` (today it shows until `m10_door`), and
  Corvin waits in the Vault (`vault_halls`, slot 12).

- **Corvin, the waiting lead** (slot 21, the crew role, as built), by the Keeping Stone, while {HERO}'s crew is
  played, from `crew_swap`. Before the menu:

  **Corvin:** My lot's ready when you are.
  Tamsin's rating Maudie's pie. It's
  getting a nine.

- **{HERO}, the waiting lead** (slot 22, as built), while Corvin's crew is played. Before the menu:

  **{HERO}:** Go on. I'll keep the island.

  *Quiet: [emote {HERO}: smile] and no line.*

**Signs and things to examine**

- **The memorial stone**, from `m10_stone`:

  **Sign:** FOR THOSE THE SEA KEPT.
  The Tern, lost off the Galeway
  five years ago. Skipper Ebb. Orrin.

  **Sign:** A neat line through a third name.
  Under it, new-cut: CAPTAIN SAEL, OF
  FALLHAVEN.

  **Sign:** And under her, smaller: FALLHAVEN.
  SALTCOMBE.

- **The notice board**, from `m9_done`: its mission 1 text and mission 8's posters page, then:

  **Sign:** A new notice, in Brann's square
  hand: RIMBORN WELCOME. PIE AT THE
  QUIET STONE. HERBS FROM NELL.

  **Sign:** And under Corvin's poster, in the
  same hand: WANTED HOME FOR SUPPER.

  *Corvin leading, after it:*

  **Corvin:** Still not my face.

- **The cove.** Settling:

  **Sign:** Rimborn boats, tied two deep along
  the jetty. Every one has a name on
  its bow, and under it: FALLHAVEN.

  *Free play (beside the boarding warp to the Wayfarer):*

  **Sign:** The Wayfarer at anchor. Her folded
  sails lie along her sides like
  wings at rest.

- **The beached Kestrel** (new), on the shingle, until `m10_funeral`:

  **Sign:** The Kestrel, hauled up on the
  shingle, her keel cracked stem to
  stern. Her rail's been polished.

  *From `m10_done`, the same page, then:*

  **Sign:** Tully would want her seen off
  properly. Give her a send-off?

  *[yes/no] Yes: scene 14. No: nothing. From `m10_funeral`:*

  **Sign:** A long scar in the shingle, where
  the Kestrel lay.

- **Cidrick's yard:**

  **Sign:** CIDRICK AND SONS. SHIPWRIGHTS.
  Under it, smaller: SONS TO FOLLOW.

- **Marta's**, from `m10_done`:

  **Sign:** MARTA'S, AGAIN. Herbs, gear and
  no promises.

- **The Mercury-blue puddle**, with Frost from Corvin's crew (Nerissa): mission 1's line, then:

  **Nerissa:** It doesn't want to. I respect that.

### `hero_house`

Mission 1's rows, with these states from `m9_done` (and the note from `m10_done`):

- **Brann's note**, on the table, from `m10_done`:

  **Note:** {HERO}. Corvin. Supper at six.
  HERE, not on that ship. My knees
  have opinions. Brann.

- **The mirror**, from `m9_done`:

  **Mirror:** You look like you've been to the
  end of the world. You have.

  *Then mission 1's "Change your look?" and its yes/no.*

- **Brann's bed**, from `m10_done`:

  **Sign:** Brann's bed, corners sharp enough
  to slice bread. A second blanket is
  folded at its foot. For Corvin.

- **The egg basket**, from `m9_done`:

  **Sign:** The speckled egg has a hairline
  crack in it. Brann says: not yet.

- **The window**, from `m10_done`:

  **Sign:** Through the glass, the Vault road.
  And past the cove, a ship with her
  sails folded like wings.

- **The bed**, the home bunk: mission 1's lines.

### `vault_halls`

Mission 1's signs stand. From `m10_vault_in`:

- **Corvin**, slot 12, by the inner door. Scene 4; then, from `m10_asked` until `m10_door`:

  **Corvin:** Go on. Hand flat. Push with your
  mind, not your back. Brann's
  drills.

- **The inner door**, slot 11. Until `m10_door` (mission 1's text, then):

  **Sign:** Two handprints, side by side.
  Corvin stands by the east one.

  *Move on the west print before `m10_asked` (the Psynergy event's `else_text`):*

  **System:** The print stays cold. It opens to
  two Earth Adepts, together.

  *From `m10_door`:*

  **Sign:** The inner door stands open, its two
  halves drawn back into the walls.
  The prints are cold now.

- **The warded stair**, slot 13 (as built), on the landing, from `m10_door`:

  **Sign:** A stair spirals down toward the
  Earth Well, behind a curtain of red
  light. It won't open. Not yet.

  *Move on it (nothing moves):*

  **System:** The ward doesn't move. Whatever is
  down there is asleep. Let it be.

- **The sea stair**, on the landing, from `m10_door`:

  **Sign:** A stair down into the dark. The
  sound of the sea comes up it, and
  the smell of salt.

- **The sea-chest**, on the landing (the dungeon's gear chest, Items, below):

  **Sign:** An old sea-chest on the landing,
  its lock long rusted away.

- **The river's edge**, from `m9_done`:

  **Sign:** The underground river runs loud
  and black toward the sea. It took
  Corvin once. It gave him back.

### `wayfarer_berth` (new)

*The states:* berthed (until `m10_done`); empty (`m10_done`): the Wayfarer has gone round to the cove.

- **Corvin, Tamsin, Nerissa and Wynn**, on the last dry step, from `m10_berth_in` until `m10_ship`. Corvin, before
  the shingle is dug:

  **Corvin:** You first. I dug the last hole. It
  was a very good hole.

  *Wynn:*

  **Wynn:** She's just sitting there being a
  ship. I could look at her all day.
  I might.

- **The shingle** (puzzle 2), until `m10_shingle`:

  **Sign:** Six hundred years of shingle, washed
  in from the cave mouth over the
  stair. Scoop would dig it clear.

  *From `m10_shingle`:*

  **Sign:** The stair's last flight, dug clear
  down to the quay.

- **The gangway** (puzzle 3), until `m10_gangway`:

  **Sign:** The ship's gangway hangs from a
  brass arm on her rail. It swings out
  over the water, and back.

  *From `m10_gangway`:*

  **Sign:** The gangway, its chain made fast,
  bridging the quay to her rail.

- **The quay:**

  **Sign:** A quay of dressed stone, carved
  with the six marks. Older than the
  Vault's halls.

- **The cave mouth:**

  **Sign:** Far off, a grey light where the sea
  comes in, under the north cliffs.

- **The glint** (optional A), at the waterline, until `m10_glint`:

  **Sign:** Something glints in the shingle at
  the waterline. Scoop would dig it
  out.

- **The empty berth**, from `m10_done`:

  **Sign:** The berth, empty. The water where
  she lay is still and black. She's
  at anchor in the cove now.

### `wayfarer` (re-clipped)

*The states:* berthed (`m10_ship`, until `m10_done`); at anchor in the cove (`m10_done`).

- **The helm**, slot 8 (the voyage role, rewritten). Berthed:

  **Sign:** The Wayfarer's wheel, taller than a
  man. It's very still. She's going
  nowhere yet.

  *At anchor, with Tully beside it, until `m10_funeral`:*

  **Tully:** The Wayfarer, Deputy. She's not
  the Kestrel. She's very nice,
  though. Where to?

  **Tully:** And the Kestrel's on the shingle.
  When you've a moment. She ought to
  be seen off.

  *From `m10_funeral`:*

  **Tully:** Where to, Deputy? The Calm's on
  the chart. Sea trials, Cidrick
  says. She likes them.

  *Corvin leading, in place of Tully's first page:*

  **Tully:** Where to? I still don't know what
  to call you. The poster says
  seal-breaker. ...Corvin, then.

  *Then: [menu: the chart's places, The Galeway, Not now]. The chart's places sail as the Kestrel's chart did (as
  built). The Galeway: scene 15.*

- **Corvin**, slot 9 (as built), berthed, from `m10_ship` until `m10_supper`:

  **Corvin:** She's ours. Both crews'. Go and
  look at everything. I already
  have. Twice.

- **Tamsin, Nerissa and Wynn**, on deck, berthed, until `m10_supper`. Tamsin, by the grating:

  **Tamsin:** I'm watching the fire, in case it
  needs anything. It doesn't. I'm
  watching anyway.

  *Nerissa, at the rail:*

  **Nerissa:** She sits in the water as if she's
  thinking. Good ships do.

  *Wynn, at the bow:*

  **Wynn:** WAYFARER. In plain letters.
  Somebody wanted us to know her
  name.

- **The engine**, slot 10, the grating over the engine's well:

  **Sign:** Six glass chambers round a heart
  of brass. One burns red and gold.
  Five are dark.

  **Sign:** With the Flame Well open, she can
  cross the Stillwaters, Ketch says.

- **The chart table**, slot 11. Scene 8; then, from `m10_log`:

  **Sign:** The chart table, and the Lodestar's
  brass cradle. Set the Lodestar in
  it?

  *[yes/no] Yes: [light: a faint blue glow round the cradle's rim]*

  **System:** The needle shivers, turns once and
  settles, pointing nowhere. Then
  {LEADER} takes it back.

- **The muster roll**, slot 12 (the muster role, as built). Scene 9; then, from `m10_muster`, before the trade
  menu:

  **Sign:** The muster roll: two columns in
  Wynn's small neat hand, the two
  leads side by side at the top.

- **The Farer lamp** (optional B), on the chart room wall, until `m10_cache`:

  **Sign:** A Farer lamp on the chart room
  wall, cold. A flame is etched into
  its glass.

  *Blaze on it, from `m10_done` (a crew with Tamsin): [light: the lamp lights, warm]*

  **System:** The lamp's light falls across the
  chart table, and shows a seam in
  it: a drawer nobody had seen.

  *Then the drawer's chest (Items, below) and `m10_cache`. From `m10_cache`:*

  **Sign:** The Farer lamp burns, small and
  steady. It doesn't seem to need
  oil.

- **The bow:**

  **Sign:** Farer letters on the bow. Under
  them, cut in old plain letters:
  WAYFARER.

- **The folded wings:**

  **Sign:** Long fins of sailcloth on ribs,
  folded flat along her sides like a
  bird's wings at rest. Very still.

- **The blue window**, in the chart room. Berthed:

  **Sign:** A window of blue glass. Through it,
  rock, and the dark of the cave.

  *At anchor:*

  **Sign:** A window of blue glass. Through it
  the sky is bluer than the sky.

- **The hatches:**

  **Sign:** A hatch down to the galley. It
  smells of fish stew.

  **Sign:** A hatch down to the quarters:
  eight bunks, and a hammock.

- **Old Jory**, on deck, from `m10_done`:

  **Old Jory:** Under the marrow, under the stone.
  I always said it meant something.
  ...I never said it. I thought it.

  **Old Jory:** Corla rowed me out. Don't tell
  anyone. I've a reputation for not
  going places.

### `wayfarer_galley` (new)

- **Ketch**, at the stove, from `m10_done` (a free restoration point, as his skiff was at Bastion Rock):

  **Ketch:** Galley's open. Fish stew. It's
  always fish stew. I've written a
  galley verse.

  **Ketch:** It rhymes "stew" with "stew". That's
  allowed, in galley verses.

  **Ketch:** A nap at the table? I'll keep
  watch. And eat. Quietly.

  *[menu: Rest, Pokémon, Not now] (the inn's menu, at no charge). After resting:*

  **Ketch:** You slept through two verses. That's
  a compliment, from you.

- **The stove:**

  **Sign:** A stove of Farer brass. Ketch lit it
  with an apple core and a lot of
  words. He won't say which.

- **The table:**

  **Sign:** The galley table. Somebody has
  carved into it, very neatly: TAMSIN
  10/10.

- **The pie dish**, from `m10_supper`:

  **Sign:** Maudie's pie dish, scraped clean.
  Somebody has to take it back to
  Maudie.

### `wayfarer_quarters` (new)

*The states:* the first night (`m10_night`, until `m10_done`): all seven Adepts at their bunks, the talks; free
play (`m10_done`): each Adept at their bunk while they're in the waiting crew and aren't its lead.

- **The ship's bunk** ({HERO}'s, beside Corvin's; decision 34). The first night: scene 12. Free play:

  **Bunk:** Your bunk, beside Corvin's. Sleep
  until...?

  *Corvin leading:*

  **Bunk:** Corvin's bunk, beside {HERO}'s.
  Sleep until...?

  *[menu: Dusk, Dawn, Not now] (the home bed's)*

- **The waiting Adepts**, free play, one each:

  **Maren:** I wrote a list today. Bandages,
  splints, Herbs. Nobody will read it
  but me. It's very restful.

  **Sorrel:** The hull's warmer today. Don't ask
  me how I know. I know.

  **Vesper:** Still a hammock. Still not a ghost
  on her. I'm keeping an eye out.

  **Tamsin:** Ninety press-ups for me, ten for
  the Forgeheart. Every morning. It's
  a system.

  **Nerissa:** Froakie likes the bucket. I like
  the quiet. We're both very happy.
  You can't tell, but we are.

  **Wynn:** ...and if those are wings, then she
  flew, which I said. Don't take me
  up. I'm only saying.

- **Corvin's bunk**, while he isn't there:

  **Sign:** Corvin's bunk, beside yours. A
  disgrace, he says. He's right.

- **Vesper's hammock**, while she isn't there:

  **Sign:** A hammock, slung between two hooks
  over a perfectly good bunk.

- **The other bunks**, while their Adepts aren't there:

  **Sign:** A bunk of the grey wood, with a
  curtain and a little lamp, and
  somebody's things on it.

### The other rooms (free play)

- **Tully, the Wayfarer's mate**, in every room where the ship moors (Canalport slot 15, Eldergrove slot 13, Lantern
  Reef's mate), from `m10_done`, in place of the Kestrel's lines:

  **Tully:** The Wayfarer, Deputy. Not the
  Kestrel. Very nice, though. Where
  to? Or a bunk below?

  *Corvin leading, in place of it:*

  **Tully:** The Wayfarer. Where to? ...I still
  don't know what to call you.
  Corvin, then.

  *[menu: the chart's places, Bunk, Not now] Bunk:*

  **Bunk:** A Farer bunk below decks. It
  smells of cedar and six hundred
  years. Sleep until...?

  *[menu: Dusk, Dawn, Not now] (at the reef, Night in place of Dusk, as mission 6 has it)*

- **Canalport, while Corvin's crew is played** (bounties add a joke line in Tidewarden towns, story.md §9b):

  *The marine at the sandbags:*

  **Marine:** You look like the seal-breaker on
  the poster. ...No. He's uglier.
  Move along.

  *Harbourmaster Quayle, before his own lines:*

  **Quayle:** The seal-breaker! On my quay! Have
  you a licence? No? Well. Mind the
  tide. It doesn't care who you are.

- **The poster boards** (Canalport's Tidewarden notice and Eldergrove's tithe notice, as Stonehollow's above),
  Corvin leading, after the posters' page:

  **Corvin:** Still not my face.

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| The landing's sea-chest | `vault_halls`, the landing behind the inner door (the dungeon's gear chest; items §13's suggestion for the Vault) | Long Sword | The engine's chest line, naming `{LEADER}` |
| The berth's glint | `wayfarer_berth`, the shingle at the waterline (Scoop, optional A; sets `m10_glint`) | Elixir ×1 | **System:** {LEADER} found Elixir! |
| The Farer drawer | `wayfarer`, the chart table's hidden drawer (Blaze on the chart room's lamp, from `m10_done`, optional B; sets `m10_cache`; items §13's "Farer cache on the Wayfarer") | 300 coins and a Psy Crystal | **System:** {LEADER} found 300 coins! Then the engine's chest line for the crystal |
| The Farer's Log | Scene 8 | The Log (decision 32): a key item that opens the Start menu's Log row | Scene 8's system lines |
| The linking cord | Scene 10 | Nothing new: mission 7's Linking Cord is in the one bag from scene 9; the scene stages it changing hands | — |
| Marta's shop | `stonehollow`, from `m10_done` | Fallhaven's stock (items §11) | Her shop lines |

**The Farer's Log's Key Items text:**

**Item:** The Farers' half-written book. Its
first pages nobody can read. The
rest fill as you go.

**The Lodestar's Key Item text**, from `m10_cradle` (mission 1's, rewritten):

**Item:** A brass Farer compass with a
needle of blue glass. It stirred in
its cradle, and points nowhere yet.

## Puzzles

The crew's verbs: Crew 1's Psynergy (Move, Scoop, Frost, Ply, Growth, Reveal, Halt, Cloak) until the muster roll,
with Corvin beside it; from `m10_done`, whatever either crew holds, and any Adept traded across. The main path needs
only Crew 1's verbs and Corvin's scripted hand. Pushed things stay where they're pushed, so every block can always
be got behind again.

**Puzzle 1. The Two-Earth Door (Move, with Corvin; new).**
1. Corvin waits by the inner door's east print. Talking to him plays his question (scene 4); he lays his palm on
   the east print (`m10_asked`).
2. Cast Move on the west print. Before `m10_asked` it stays cold, with its line; after, scene 5 plays: both prints
   glow, the door opens (`m10_door`).
3. Both hands are needed, and one is the player's: the door is the player's to open, as the Forest seal was in
   mission 5.

It pays off mission 1's lock gate ("Two keepers stand where one cannot") and the fight in this room.

**Puzzle 2. The shingle (Scoop; new).**
1. At the sea stair's foot, six hundred years of shingle have buried the last flight above the quay.
2. Cast Scoop on it: it slides away (`m10_shingle`, a gate opening the stair), and the quay is open.

**Puzzle 3. The gangway (Halt; new: mission 6's spar).**
1. The Wayfarer's gangway hangs from a brass arm on her rail and swings out over the one-cell gap between quay and
   rail, and back (a patrol actor).
2. Cast Halt while it lies across the gap: for ten seconds that cell can be walked.
3. Once the crew is across, Corvin catches its chain and makes it fast (`m10_gangway`, a gate keeping the cell
   bridged), so the way back never needs Halt again.

**Optional A. The glint (Scoop).** At the berth's waterline: an Elixir (`m10_glint`).

**Optional B. The Farer lamp (Blaze, from `m10_done`).** On the chart room wall, a cold Farer lamp. With Tamsin in
the crew (Corvin's crew played, or Tamsin traded in at the muster roll), Blaze lights it, and its light shows a
hidden drawer in the chart table (`m10_cache`). It gives the player a reason to try a trade at once.

## Eggs

- **Cidrick** (story.md §9a, Final Fantasy's recurring engineer; decision 10): a Fallhaven shipwright who walked up
  the cliff road with his tools in mission 9 and opens a yard on Marrow Isle's cove the morning after. His gag starts
  here: his family built every ship ever ("And most of the ones that aren't"), the Kestrel included ("He'd have built
  her better, if they'd asked him"), and the Wayfarer too, "probably". His yard's board says CIDRICK AND SONS, with
  SONS TO FOLLOW underneath. His own look, never a copied one: goggles pushed up into his hair, a toolbag over each
  shoulder, a mallet in his belt. His quest (the airship's figurehead) and the Wayfarer's upgrades come later.
- **"A Funeral at Sea"** (§9a, One Piece's send-off of a ship that can't sail on; decision 10): when the Wayfarer
  replaces the Kestrel, an optional scene at dusk floats the cracked cutter out on the ebb, Tamsin's Blaze sets her
  sails alight, and Tully says goodbye. Ketch sings the funeral song he has been writing for Corvin as a joke since
  mission 2, finished for Sael, and Corvin answers with his own line from then, "It rhymed and everything." Nothing
  in it is quoted; the Kestrel never speaks.
- **Gary Rivalson's** gag carries on (mission 1's egg): he gives the refugees his room but not his "very talented"
  partner, would have found the ship himself, and has a word for Corvin back from the dead "AGAIN".
- **The Mercury-blue puddle** (mission 1's egg) gets a line for Corvin's crew: Nerissa's Frost bounces off it too.

## Either order

Nothing differs: mission 10 always follows mission 9, with both crews full.

## Not in this mission

The warded stair and the Earth Well under it (mission 22, Primal Groudon); the Wayfarer's other upgrades (the
living hull at mission 14, the bubble hull at 18, wings at 19, fog sight at 20), which Sorrel's, Nerissa's and Wynn's
talks seed; Cidrick's quest and his upgrades; the Lodestar waking (mission 12); the Breaking itself (mission 11) and
the lamp waiting in the Galeway; the heart quests the talks seed (Corvin and {HERO}'s Fallhaven memorial, Maren's
charter, Sorrel's groves, Vesper's survivor, Tamsin's flame, Nerissa's domes, Wynn's chart); Ilse's answer at the
Pinnacle (mission 21); Maren's Shiny Stone (mission 13, demo decision 13); the walkable Kin Garden, Gannet's library
and the rest of Marrow Isle's growth (decision 33); Vesper's Haunter and Ralts's Kirlia, which their levels keep
after the demo; the Farers' return "when it is complete" (the postgame) and the Steward (mission 19).

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **The morning after:** mission 10 opens the same morning, once the Holdfast has sailed; Corvin's crew climbs out
  of Ketch's nets ("Which way up do people go?").
- **Brann and Corvin:** "You're late." "Five years late."; the halls, the seal-bar, the floor and the Sleeper;
  Brann's embrace; "Eggs in your boots... I never once caught you." "You did. You let me."
- **The memorial stone:** Brann cuts Sael's name, then Fallhaven and Saltcombe at Ossian's asking ("There's always
  room on this stone. That's the trouble with it"; "The stone says it now. I don't have to say it on my own").
- **Brann's blessing:** keepers are never told what's behind the inner door; "Forty years I kept it. I never once
  asked what it was for. Maybe it's time somebody asked"; mission 1's lock words, "Two keepers stand where one
  cannot", as his leave.
- **Old Jory's skiff-song as the key** (mission 2's seed, heard by Crew 1 in mission 9): "Under the marrow" is
  Marrow Isle, "under the stone" the Vault, and Corvin's reason for Keeping Night.
- **The door:** Corvin asking again, properly, in the room where they fought; both prints amber, "It knows us"; the
  landing behind it with two stairs; the warded stair's one slow red breath, the Sleeper settled since Keeping Night.
- **The Wayfarer:** a sea cave under Stonehollow that opens under the north cliffs; a quay older than the Vault,
  carved with the six marks; her pale grey wood that Sorrel feels is alive and asleep; her sails folded along her
  sides like wings (§8's wings, dormant until the Sky Well); WAYFARER cut in old plain letters under her Farer name;
  her engine of six glass chambers round a brass heart, one per Well, with only the Flame chamber alight; Ketch's
  Stillwaters, where boats "sit till they're bones".
- **Wynn's proof:** the Wayfarer is one of the sky-ships her mother showed her from the window (mission 8), "I said.
  I always said."
- **The cradle and the Log:** a brass cradle on the chart table cut to the Lodestar's shape, where it turns once
  and settles; "It isn't awake. It's stirring"; the Farer's Log lying beside it, half Farer script and charts
  nobody can read, half blank pages that fill themselves with both crews' records as the crews watch, which is how
  decision 32's records "kept since mission 1" reach the book; its one plain line, "To whoever finds her: keep the
  Log. We will come back when it is complete" (story.md §3's promise, hinted in Act I); "Come back. From where?";
  Maren's "It's been keeping notes. ...I know how that sounds."
- **The muster roll** in Wynn's hand, "Two keepers, standing where one can't"; the bags into one hold, Maren's
  inventory ("It isn't a report"), and mission 1's "Herbs first" from Maren.
- **Supper:** Ketch's fish stew ("The recipe is: fish"), Brann's six hundred steps and "I said supper. I didn't say
  where", the linking cord passing from Nerissa to Vesper's Gastly (mission 7's "A Haunter, they say"), Brann's "It
  was waiting for the ship, not for you", the toast to Sael, Ketch's song held back, and Brann's "What are you now?"
  with "Since the table."
- **The quarters:** eight bunks and Vesper's hammock; the seven talks and what they seed: Corvin's burned sleeve
  and his new post for the rim; Maren's empty notebook and her "Rules. Better ones"; Sorrel feeling the hull alive and
  meaning to undo the Forest seal and replant the groves; Vesper's fog past the Galeway ("Not as a client. I'll still
  send you the bill"); Tamsin's ninety press-ups and the cold brazier; Nerissa wanting to know if the ship can go
  under; Wynn drawing the ship onto her chart.
- **The morning:** Ketch takes the Wayfarer round to the cove on the tide; Tully becomes her mate; Cidrick's "Sea
  trials first", so she sails the Calm and her maiden voyage is the Galeway crossing.
- **The Kestrel's end:** her keel cracked in the lanes (mission 9), Cidrick's verdict, and her send-off with Tully's
  goodbye, Tamsin's Blaze and Ketch's song in two verses ("The captain was the last ashore, so she's first aboard
  tonight").
- **The ending's frame:** the Wayfarer leaving the cove with Brann's hand raised, "somewhere in it, a single lamp was
  waiting" (Hask, mission 9), the end card's wording, the credits' title "HALCYRA. Act I: Open Water", the save
  prompt, and the deck "the morning before she sailed" with Ketch's "...Probably."
- **Marrow Isle starts to grow:** Marta's shop reopened with Fallhaven's stock, Tanner baking at the inn's back door,
  Fen at The Quiet Stone, Gannet's library-to-be in the cellar under the hatchery, Wenna's cellar, Old Jory on Moss's
  bench, Cidrick's yard, and Brann's notice with WANTED HOME FOR SUPPER under Corvin's poster.
- **Free play:** every line above for Stonehollow, the house, the Vault and the ship; Corvin's and {HERO}'s waiting
  lines; the waiting Adepts aboard; Ketch as the ship's free restoration point; Tully at the moorings; the joke lines
  for Corvin's crew in Canalport, and "Still not my face".
- **The rewards:** a Long Sword, an Elixir, 300 coins and a Psy Crystal.

## Changes to the build

**Rooms**
- **`vault_halls`:** the inner door chamber gains the landing behind the door (a gate on `m10_door` opening the
  door's cells), with the sea stair (a warp to `wayfarer_berth`, in place of today's straight warp to `wayfarer`),
  the warded stair (slot 13, as built, moved onto the landing) and the sea-chest. The west print is a Psynergy event
  (Move) gated on `m10_asked`, with its `else_text`; Corvin's slot 12 shows from `m10_vault_in` (today `m10_intro`).
- **`wayfarer_berth`** (new, decision 5's Wayfarer rooms): a sea cave clipped from a Golden Sun water cave, the
  builder's pick, with `--water`: the sea stair's foot (entrance 0) and its shingle (a dig spot with a gate on
  `m10_shingle`), the quay, the gangway (a patrol actor across the one-cell gap to the ship's rail that Halt makes
  walkable; a gate on `m10_gangway` keeps it bridged), the glint, the painted cave mouth, and the ship's rail (a
  warp to `wayfarer`'s entrance 0). From `m10_done` the ship, the gangway and the warp are gone.
- **`wayfarer`** re-clipped (today one deck): the deck with the helm, the grating over the engine's well, the muster
  roll by the mainmast and the bow; the chart room at the stern with the chart table and cradle, the blue window, the
  Farer lamp and its hidden drawer (a chest that shows on `m10_cache`); the hatches down to the galley and the
  quarters. Two moorings: in the berth (entrance 0, the gangway from `wayfarer_berth`) until `m10_done`, and at
  anchor in Stonehollow's cove (entrance 1, the gangway to the jetty) from it.
- **`wayfarer_galley`** (new): the table, the stove and Ketch, a free restoration point from `m10_done`.
- **`wayfarer_quarters`** (new): eight bunks and the hammock; the ship's bunk with the home bed's menu (decision 34);
  the first night's rows (`m10_night` until `m10_done`) and the free-play rows.
- **`stonehollow`:** the cove's two states (the boats and the beached Kestrel; then the Wayfarer at anchor, with a
  boarding warp from `m10_done`); new rows for Old Jory, Hanne and Pip, Tanner, Wenna, Marta (her shop from
  `m10_done`), Fen, Gannet, Cidrick and his yard, Ketch, Tully and the beached Kestrel (hidden from `m10_funeral`);
  slot 18 renamed Ossian; slot 19's line; slot 20 hidden from `m10_stone`; slot 17's voyage row hidden from `m9_done`;
  the memorial stone's and the notice board's new pages; every row's text by state. Today's `refugees_settle`
  becomes mission 9's scene 20 and scenes 1 and 2 here.
- **`hero_house`:** the note, mirror, bed, egg and window states.

**Actors and engine**
- **Today's scenes replaced:** `refugees_settle` (mission 9's scene 20, scenes 1 and 2), `inner_door` (scenes 4 and
  5: a talk, then a Psynergy event), `wayfarer_found` (scenes 7 to 9: `merge_bags` and `crew_swap` move to the
  muster roll, and `m10_done` to the morning, scene 12).
- **The Wayfarer moves at `m10_done`:** her deck's gangway warp switches from the berth to the cove, the berth
  empties, and Stonehollow's cove shows her at anchor.
- **The helm:** the voyage role's menu (as built, the Kestrel's chart) gains a last row, "The Galeway", which plays
  scene 15.
- **New steps for the ending (decision 20):** `end card` (a full-screen card over black, in the title's lettering),
  `credits` (the roll from credits.md), and `save prompt` (a yes/no into the save flow), after which the scene puts
  the player back on the deck as it was before the voyage: the same phase and the same mooring.
- **The Log** (decision 32): scene 8 gives the Farer's Log, which opens the Start menu's Log row with its tabs filled
  from the records kept since mission 1 (menus §8.9), and DexNav's "Search here".
- **The Lodestar:** the chart table's cradle as a yes/no with a light, which changes nothing; the item's text from
  `m10_cradle`.
- **Crew conditions:** a row that shows only while a named Adept is in the waiting crew and isn't its lead (the
  quarters' free-play rows); scenes that show any Adept, wherever they are (supper, the first night, the funeral's
  Tamsin, whichever crew she is in).
- **The first night** as a state: from `m10_night` every Adept stands at their bunk as an actor, the played crew
  stepped out (`crew out`), until the morning's `crew in`.
- **Tully's mate rows** in every mooring room (Canalport slot 15, Eldergrove slot 13, Lantern Reef's) switch to the
  Wayfarer's lines and bunk text from `m10_done`.
- **Corvin's crew in Canalport:** the marine's and Quayle's lines while Crew 2 is played (`while_crew 2`), and
  Corvin's line after the posters on the three boards.
- **Marta's shop** in Stonehollow from `m10_done`, with Fallhaven's stock (items §11); Nell's stall stays as built.
- **Music:** Ketch's song for the funeral in the music table (decision 37, slice 11).
- **`{LEADER}`** in the give, chest and cradle lines.
- **Actors scenes can move:** Brann (aboard), Ketch, Tully, Old Jory, Ossian, Cidrick, the Kestrel (floated out,
  burning, with a fire tint), Gastly, Rowlet, and Froakie in its bucket.

**New scene steps** (README §2): `phase`, `light` (the amber prints, the ward's breath, the engine's glow, the
cradle's blue, the spreading ink, the Kestrel's fire), `camera`, `pose` (embrace, kneel, stand, a hand on the door,
set the Lodestar down, write, lean over the rail, nod), `choice` (both beats, with the quiet set), `crew out` and
`crew in`, `merge bags` (as built), `end card`, `credits`, `save prompt`, a Psynergy-event trigger (scene 5), and
yes/no menus (the bunk, the Kestrel, the chart table, Ketch).

**Checks.** `tools/mission10_check` follows the new flow from mission 9's landing: the nets and the stone; the door
refusing Move before Corvin's question; his reply menu in both voices; the door, and the warded stair refusing; the
shingle and the gangway; the ship; the cradle; the Log's row in the Start menu; the muster roll, the one bag and
purse, and `crew_swap`; supper's reply menu in both voices; the seven talks in any order, and none; the bunk to dawn
and `m10_done`; the Wayfarer in the cove; a swap at Stonehollow and a trade at the muster roll; Tully's rows; the
funeral, yes and no; the Farer drawer with Tamsin traded in; and the helm's maiden voyage, with the end card, the
credits, the save prompt (yes and no) and the return to the deck with the clock and the mooring as they were.
