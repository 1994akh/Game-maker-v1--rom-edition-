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

