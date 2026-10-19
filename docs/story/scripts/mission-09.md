# Mission 9: The Fall of Fallhaven

> **Status:** draft for your yes or notes (19 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 9, §3 (layer 2), §4 (Sael, Maren, Ilse) and §9 (Fallhaven a ruin after it).
> Today's build: [mission-9-build.md](../../design/mission-9-build.md).

| | |
|---|---|
| Mission | 9, The Fall of Fallhaven (Act I's ending, part one) |
| Plays after | Mission 8's posters ([mission-08.md](mission-08.md), scene 16): Crew 1's next rest at an inn or a sanctum once `m8_posters` is set. "Soon after", played at night (decision 8), on mission 7's rest hook (decision 7) |
| Crew | Both. Crew 1 ({HERO}, Maren, Sorrel, Vesper) is played from the knock; Crew 2 (Corvin, Tamsin, Nerissa, Wynn) is placed in the archive. Relay stones switch between them (mission-9-build.md). Each crew keeps its own bag until mission 10 |
| Rooms | Wherever Crew 1 rests (the knock); `fallhaven_cliff` (mission 2's cliff road: the way down at the start, falling at the end); `fallhaven_lower` (re-clipped: mission 2's lower town, at night, with the households' lanes); `fallhaven_archive` (re-clipped: the great hall, the east wing and vault, the wind-wheel ledge, the high door); `stonehollow` (the cove, for the landing) |
| Clock | The knock sets night. Night all through Fallhaven: the clock holds while the crews are there (mission 6's reef rule). Dawn at Stonehollow |
| Flags in | `m8_posters` |
| Flags out | `m9_started`, `m9_road`, `m9_lower_intro`, `m9_alley`, `m9_ev_a`, `m9_vine`, `m9_ev_b`, `m9_hatch_seen`, `m9_hatch`, `m9_lift`, `m9_ev_c`, `m9_evacuated`, `m9_archive_intro`, `m9_where`, `m9_lamp`, `m9_case`, `m9_ledger`, `m9_meet`, `m9_sael`, `m9_climb`, `m9_boulder`, `m9_slab`, `m9_top`, `m9_confession`, `m9_done`; and, optional, `m9_marta`, `m9_charts` |
| Unlocks | The Ledger of the Crown (a story object, items §5) and with it story.md's layer 2; Maren's notebook (a new story object); the name of Lord Warden Vey. Fallhaven is lost for good (story.md §9) |
| Reply beats | 2: Ketch's message (scene 1); Maren's confession (scene 18) |
| Fights | None. Fallhaven has no random battles tonight: the cliff is the danger |
| Leads into | Mission 10 ([mission-10.md](mission-10.md)), straight on from the landing at Stonehollow |

**The flow.** Soon after the posters, in the middle of the night, Ketch knocks on the door where Crew 1 sleeps. He
has crossed the Galeway alone: Fallhaven is going, all of it, and Corvin has sent him with four words for {HERO}: "Tell
{HERO} I'm asking." Maren reminds the deputy of the Commodore's orders, decides a falling town needs a medic, and
sends one more Wingull west. Ketch leads the Kestrel through the storm lanes, and on the third night Crew 1 comes
down the cliff road into Fallhaven's lower town, where Corvin and Sael wait on a cracking plaza. Sael gives the
keeper three households she can't reach and goes up to lock the archive. Crew 1 frees Tanner and Ossian, brings Pip
down from a terrace and finds the order's cellar under the plaza; Crew 2, in the archive, hears the archivist think
about the Ledger of the Crown, lights the dark east wing and spins the lift down for Old Jory. Relay stones pass the
turn between them. With everyone out, Crew 1 climbs to the archive. The plaza goes into the falls, and Sael bars the
great doors and holds them while both crews read the Ledger: the seals drain the Wells into the Crown, and the rim
is the price, town by town, written down in the order's own hand. Sael sends them out by the high door, and tells
Corvin to take a coat. The doors hold long enough. Up the falling cliff road, Fallhaven slides into the mist, and
Maren tells the crews who has been reading her reports. Every boat that floats follows Ketch into the Galeway. At
its edge the order's fleet waits with orders to turn them back, and Commodore Ilse escorts them home instead, to
Marrow Isle.

## Scenes

### 1. The knock

- Room: wherever Crew 1 rests. Trigger: the rest hook (decision 7), once `m8_posters`, unless `m9_started`. A bunk
  or the home bed doesn't count.

*The rest's fade holds on black. That rest's after-rest line is dropped: Crew 1 doesn't come back to this inn.*

**Narration:** {HERO} slept. Then, a long while
after midnight, somebody knocked
at the door.

*[phase night] [fade in 30] The inn at night, in whatever room Crew 1 rested. Rain blows in at the open door. A
wiry man in a coat made of patches stands on the step, soaked through, an apple in one hand: Ketch. [show Ketch]
[walk Ketch → before {HERO}] [crew out]*

**Ketch:** There you are. Do you know how
many inns there are in the Calm?
I've eaten at all of them.

**Ketch:** Ketch. Corvin's pilot. You'll be
{HERO}. He said look for the one
who stands like a gatepost.

**Maren:** A Rimborn pilot. In the Calm, in
this weather.

**Ketch:** Through the Galeway, in worse.
Two days of it. I don't recommend
it.

*[wait 20] He stops chewing.*

**Ketch:** Fallhaven's going. All of it,
this time. The cliff's split at
the foot of the lower town.

**Ketch:** Sael's holding the town together
with rope and shouting. Corvin's
there with her. His whole crew.

**Ketch:** He sent me. He said, tell {HERO}
Fallhaven's falling, and I can't
hold it on my own.

**Ketch:** Tell {HERO} I'm asking.

**{HERO} replies:**

1. "I'm coming." · quiet: (Nod)

   **Ketch:** He said you'd say that. He also
   said you'd argue first. ...You
   didn't argue.

2. "He's a seal-breaker." · quiet: (Shake head)

   **Ketch:** Tonight he's carrying people up
   a cliff. Arrest him in the morning.
   He'll wait. He's good at that.

3. "Why me?" · quiet: ...

   **Ketch:** Because you always came after
   him. His words. Then he went quiet
   and ate all my biscuits.

*Every reply rejoins here.*

**Maren:** Deputy. The Commodore's last
orders were to leave him to the
fleet. Hold to our own work.

**Vesper:** The fleet stops at the Galeway.
People are falling off the world,
medic. That's work.

**Sorrel:** I'm going. Whatever the order
says.

*[wait 30] Maren looks down at her satchel: the bandages, the splints, the little bottles in their loops.*

**Maren:** A whole town on a cliff, falling.
There'll be crush injuries. Burns.
Broken bones by the dozen.

**Maren:** ...I'm a medic. Of course I'm
coming.

*She takes out her notebook, writes a page, tears it out and rolls it into a tube. She whistles. A Wingull drops
out of the rain onto the step, and she ties the tube to its leg. It flies off west into the dark, toward the middle
of the world. [show Wingull] [walk Wingull → off west] [hide Wingull] [emote Vesper: squint]*

**Sorrel:** Toward the middle again. At this
hour.

**Maren:** Medical returns. They don't wait
for the weather.

**Ketch:** Lovely. Wake your mate. The lanes
don't wait for it either.

*[crew in] [fade out 40]*

**Narration:** Ketch's skiff ran ahead with one
lantern on its stern. The Kestrel
followed it into the Galeway.

**Narration:** For two nights Vesper steered by
that one small light, and nobody
said very much.

**Narration:** On the third night, Fallhaven
rose out of the spray. Every lamp
was lit, and the cliff was moving.

*[flag m9_started] [place crew 2 → fallhaven_archive, entrance 0] [warp fallhaven_cliff, the high town gate (a new
entrance)]*

### 2. The high town gate

- Room: `fallhaven_cliff`, the top. Trigger: entering, unless `m9_road`.

*[fade in 40] The top of the cliff road, at night, by the high town gate, where Hask once leaned. Lanterns stream up
the switchbacks below: the lower town climbing, with bundles and children and chickens in baskets. Beyond the edge,
the white roar of the Rimfalls. Every few breaths the ground shivers. [an ambient shake of 1 every few seconds, as
in mission 2] Ketch comes out through the gate from the high town with Crew 1 behind him. [crew out]*

**Ketch:** The Kestrel's tied up in the west
cove, with every boat on the rim.
That's the high town behind you.

**Ketch:** The lower town's down the road.
Sael's on the plaza, and Corvin's
with her. Mind the edge.

*A woman pushes up the last bend against the crowd, looking at every child she passes: Hanne. [walk Hanne →
before Ketch]*

**Hanne:** Ketch! Have you seen Pip? Pip was
right behind me. I turned round, and
Pip was gone!

**Ketch:** Back down, if I know Pip. Up
something tall.

**Hanne:** Not again. Not again.

*[walk Ketch → through the gate] [hide Ketch]*

**Maren:** We'll find Pip. Go on up to the
boats.

*[face Hanne → Maren] [emote Hanne: squint] She takes in the white coat with the blue cuffs.*

**Hanne:** Tidewardens. On the rim. Helping.
...I'll believe it when I see it.

**Hanne:** Find Pip, and I'll believe it.

*[walk Hanne → through the gate] [hide Hanne] [crew in] [rest point] [flag m9_road] Control returns. The road leads
down to the lower town.*

### 3. The plaza

- Room: `fallhaven_lower`. Trigger: entering from the cliff road, unless `m9_lower_intro` (today's `lower_arrival`,
  rewritten).

*[fade in 30] Fallhaven's lower town at night: mission 2's plaza, a street smaller. A crack a hand wide runs right
across it, and the lamps along its far side lean toward the edge. The Leaning Gull leans more than it did. North, a
stair climbs to the archive's great doors, cut into the cliff and standing open, lamplit. South, the harbour stair
ends in mist halfway down: the harbour went at dusk. The last few townsfolk hurry for the west alley with bundles.
On the plaza Sael stands with a coil of rope over one shoulder, giving orders to anyone in reach. Corvin is beside
her.*

*[walk {HERO} → the plaza's edge] Corvin turns. For a moment neither of them moves. [face Corvin → {HERO}] [crew
out]*

**Corvin:** ...You came.

**{HERO}:** You asked.

*Quiet: [pose {HERO}: nod] and no line.*

**Corvin:** I did. Ketch owes me a biscuit.
He said you'd stop to arrest me
first.

**Maren:** Corvin of Fallhaven. There's a
poster with your face on it.

**Corvin:** I've seen it. It isn't my face.

**Maren:** ...No. It isn't.

*[wait 20]*

**Corvin:** Arrest me in the morning. I'll
wait. Tonight there's a town.

**Maren:** Tonight there's a town.

*Sael looks the crew over, one by one, the way she'd look over a new hand's knots. [walk Sael → beside Corvin]
[face Sael → {HERO}]*

**Sael:** So. The keeper. He talks about
you in his sleep. Did he tell you
that?

**Corvin:** Sael.

**Sael:** He was somewhere worth being
found, then. Good.

**Sael:** Now listen. The cliff split at
dusk, under the plaza. It'll go
before morning. All of it.

**Sael:** Most of the lower town's up the
road. Three households I can't get
to.

**Sael:** Tanner and Ossian, in the west
lane. A chimney came down across
their door.

**Sael:** Hanne's Pip, up on the old
terrace. The steps fell. Pip went
up anyway. Of course.

**Sael:** And Old Jory, on what's left of
the harbour steps. He won't climb,
and he won't be carried.

**Corvin:** My crew's in the archive. The
order left a vault in there, barred
from underneath.

**Corvin:** If anything in this town says
what the Crown is, it's in that
vault. We're getting it out.

*Sael nods at a squat stone by the Leaning Gull's door, carved with a lamp, humming faintly.*

**Sael:** That's a relay stone. Knock on it,
and its twin in the archive hums.
Every Rimborn house keeps a pair.

**Sael:** I'll be at the archive. Somebody
has to lock up. I'll be the last.
The captain always is.

**Sael:** Corvin. Up.

*[walk Sael and Corvin → up the north stair to the archive's doors] [hide Sael] [hide Corvin] [wait 20]*

**Sorrel:** I like her.

**Vesper:** You don't like anyone.

**Sorrel:** I like her.

*[crew in] [rest point] [flag m9_lower_intro] Control returns. The relay stone stands by the Leaning Gull.*

### 4. Tanner and Ossian

- Room: `fallhaven_lower`, the west lane. Trigger: the fallen chimney reaching the niche (Move, `m9_alley`, as
  built; puzzle 1). Before that, the voices behind it (People and signs).

*The chimney grinds aside into the niche, and the door behind it bangs open. Out comes Tanner with a loaf under one
arm, and Ossian behind him, coughing soot. [show Tanner] [show Ossian] [walk Tanner → before {HERO}]*

**Tanner:** I've still got the bread. It's
different bread. Same idea.

**Tanner:** Forty years on the east street,
and now I lodge with a Saltcombe
man. He snores in his sleep.

**Ossian:** Again. We're doing this again.

**Ossian:** I lost one town. I wasn't going to
lose a second with me still in it.

**Tanner:** Up the road, Ossian. Come on. You
can say the names on the way.

*[walk Tanner and Ossian → the west alley] [hide Tanner] [hide Ossian] [flag m9_ev_a] Then, if all three
households are out, scene 12.*

### 5. Pip

- Room: `fallhaven_lower`, the old terrace. Trigger: talking to Pip (slot 12), once `m9_vine` (Growth on the sprout,
  puzzle 2), unless `m9_ev_b` (today's `child_b`, rewritten). Before the vine, Pip's line from the terrace (People
  and signs).

*{HERO} climbs the vine to the old terrace. Pip stands right at its edge in a sailor's jacket three sizes too big,
looking out at the lamps of the boats in the west cove. [face Pip → {HERO}]*

**Pip:** You can see all the boats from up
here! All of them! Are you Corvin's
keeper?

**Pip:** He said you'd be taller.

*[emote {HERO}: sweat] [crew out] [walk Sorrel → the foot of the vine]*

**Sorrel:** Hold the vine. It won't drop you.
It likes you.

*[walk Pip → down the vine] [walk {HERO} → after Pip] Pip slides down the last of it and lands in a heap at the
bottom.*

**Pip:** ...Can we do that again?

**Sorrel:** No.

**Pip:** Hanne's going to be so cross.

**Maren:** Hanne's at the top of the road.
Go straight up. Don't climb
anything on the way.

*[walk Pip fast → the west alley] [hide Pip] [crew in] [flag m9_ev_b] Then, if all three households are out, scene
12.*

### 6. The cellar

- Room: `fallhaven_lower`, the plaza's well. Trigger: talking to the hatch (slot 16), once `m9_hatch_seen` (Reveal,
  puzzle 3), unless `m9_hatch` (today's `hatch`, rewritten).

*The hatch: an iron plate flush with the plaza's flags beside the old well, painted to look like stone until Reveal
showed what it was. The order's sigil is cast in its lid, a wave beneath a closed ring. [crew out]*

**Maren:** That's the order's seal. Ours.

**Vesper:** On the rim. Under a coat of paint
that wanted very much to be a
flagstone.

*{HERO} hauls the hatch open. Steps go down into a low cellar under the plaza. [fade out 20] [fade in 20] At the
cellar's far end a short stair climbs to the underside of a door, an iron bar across it in two brackets, rusted
in. A plate is fixed to the wall beside it.*

**Sign:** PROPERTY OF THE ORDER. RIMWARD
STATION, EAST VAULT. THIS BAR TO
REMAIN DOWN.

*[pose {HERO}: lift] {HERO} sets both hands under the bar and pushes. It doesn't move. Then the Earth answers.
[light: amber glow on {HERO}'s hands] The rust cracks, and the bar swings up out of its brackets. Far above, through
the rock, a door booms free. [shake 20, 1]*

**Sorrel:** Somebody up there just got a door.

**Maren:** Rimward station. The order kept a
station on the rim, once. I never
read that in any book.

**Vesper:** Funny, what's not in books.

*[fade out 20] [fade in 20] Back on the plaza. [crew in] [flag m9_hatch] Control returns. The vault in the archive
is unbarred (Crew 2's side).*

### 7. Old Jory

- Room: `fallhaven_lower`, the harbour steps. Trigger: talking to Old Jory (slot 13), once `m9_lift` (Crew 2's
  Whirlwind, puzzle 8), unless `m9_ev_c` (today's `family_c`, rewritten). Before the lift, his line (People and
  signs).

*The lift's basket hangs at the foot of the cliff beside the harbour steps, swaying on its rope, which climbs the
cliff face into the dark. Old Jory sits on the top step that's left, his nets in his lap. [face Jory → {HERO}]*

**Old Jory:** The lift! Sael never once let me
ride it. Thirty years I asked. "It's
for cargo, Jory."

**Old Jory:** Well. I'm cargo now. Help me in.

*[crew out] [walk Maren → beside Jory] She takes one arm and {HERO} the other, and they lift him into the basket
with his nets.*

**Maren:** Sit down in it. Hold the sides.
Don't stand up until it stops.

**Old Jory:** Yes, medic. Don't tell Sael I
rode it. She'll have words.

*Jory pulls the bell-rope. Far above, the wind-wheel turns, and the basket starts to rise. He sings as he goes up
into the dark, an old man's voice under the roar. [walk the basket → up the cliff] [hide the basket] [hide Jory]*

**Old Jory:** Under the marrow, under the stone,
sleeps a ship to carry us home...

**Maren:** What's that song?

**Vesper:** A Rimborn skiff-song. They never
mean anything. That's what they're
for.

**Sorrel:** Marrow. Like your island, keeper.

*[emote {HERO}: question] [crew in] [flag m9_ev_c] Then, if all three households are out, scene 12.*

