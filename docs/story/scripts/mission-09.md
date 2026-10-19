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

### 8. The archive

- Room: `fallhaven_archive`. Trigger: entering, unless `m9_archive_intro`: Crew 2's first turn, from the lower
  town's relay stone (today's `archive_arrival`, rewritten).

*[fade in 40] The Fallhaven archive at night: a great hall cut back into the cliff, shelves climbing the rock to the
roof, charts rolled in racks like bottles in a cellar, a long reading table under lamps that swing on their chains
at every shake. South, the great doors stand open on the plaza's lamps and the roar beyond. East, the east wing runs
back into the dark. A thin old man in ink-stained sleeves hurries between the racks with an armful of charts:
Gannet, the archivist. Sael stands at the great doors, the archive's key on a cord round her neck, a hand on each
door. [crew out]*

**Sael:** Your keeper's down there with a
medic, a forest girl and a fog
pilot. They came through a storm.

**Corvin:** Two nights of it. Ketch says
{HERO} didn't argue once.

**Sael:** Hm. The medic looked at my hands
before she looked at my face. I
like her.

**Tamsin:** Everyone likes the medics. It's
how they get you.

*[face Sael → Corvin]*

**Sael:** The order's vault is in the east
wing. They barred it from below
when they left. Before my time.

**Sael:** Nobody's needed what's in it. I
never asked what that was. I'm
asking now.

**Wynn:** The archivist knows. He's been
thinking about it all night. Very,
very loudly.

**Gannet:** I am not thinking about anything.
I am carrying charts.

**Sael:** And Old Jory, on the harbour
steps. The lift's wind-wheel jammed
in the first shake. Up on the ledge.

**Sael:** Get your book. Get that lift down.
I'm watching the plaza.

*[face Sael → the doors] [wait 20]*

**Sael:** ...Corvin. Did you eat?

**Corvin:** There were biscuits. At some
point.

**Sael:** That's not eating. That's
surviving.

*[crew in] [rest point] [flag m9_archive_intro] Control returns. The relay stone stands by the reading table.*

### 9. The archivist's thought

- Room: `fallhaven_archive`, the racks. Trigger: Mind Read on Gannet (slot 10, `m9_where`, as built; puzzle 5).

*[light: a faint violet shimmer round Gannet] Wynn puts two fingers to her temple.*

**Gannet, thinking:** Don't think it. The Ledger of the
Crown. East vault, top shelf, blue
and silver. Don't think it.

**Gannet, thinking:** My master said never open it. The
bar's below, in the cellar, under
the plaza's well. Let it rot.

*[emote Gannet: sweat] [crew out]*

**Wynn:** The Ledger of the Crown. He's been
carrying that name round like a
stone in his shoe.

**Corvin:** The Crown. In our own archive, all
the years Sael's kept it.

**Gannet:** My master made me promise. I was
nineteen. He said some books are
better left shut.

**Corvin:** He was wrong.

**Gannet:** ...I've thought so for forty
years. Quietly.

*[crew in] [flag m9_where] Control returns.*

### 10. The east wing

- Room: `fallhaven_archive`, the east wing. Trigger: Blaze on the great lamp (`m9_lamp`, puzzle 6).

*Tamsin points two fingers at the great lamp that hangs over the east wing's aisle. Fire catches in its wick and
climbs, and the dark draws back along the stacks. [light: the east wing's dark lifts] Halfway down the aisle a tall
case of ledgers has come down across it, end to end. Past it, the vault's door. [crew out]*

**Tamsin:** Finally. Something I can do in a
library.

**Wynn:** Please don't do it to any of the
books.

*[crew in] [flag m9_lamp] Control returns. The fallen case is the rest of puzzle 6.*

### 11. The wind-wheel

- Room: `fallhaven_archive`, the wind-wheel ledge. Trigger: Whirlwind on the wind-wheel (slot 11, `m9_lift`, as
  built; puzzle 8).

*The wind-wheel ledge: a niche cut through the cliff face, open to the night and the drop, with a great wheel of
little sails on an axle, and a rope running over a pulley and down into the dark. [crew out] Wynn stands as far back
from the edge as the ledge allows.*

**Wynn:** It's high. Why is it always high?
Every time. Every single time.

*She lifts both hands without looking. A gust fills the wheel's sails with a crack, and the wheel turns, faster and
faster. [light: a swirl of wind] Far below, the basket drops down the cliff on its rope to the lower town.*

**Nerissa:** Breathe when I breathe. You've done
it.

**Wynn:** I didn't look. I never look. It's
my very best skill.

*[crew in] [flag m9_lift] Control returns. Old Jory can ride up (scene 7, Crew 1's side).*

### 12. Everyone out

- Room: `fallhaven_lower`. Trigger: the third household out (`m9_ev_a`, `m9_ev_b` and `m9_ev_c` all set), unless
  `m9_evacuated` (as built: a `when` at the end of each household's scene).

*[shake 50, 3] The crack across the plaza opens wider with a sound like a mast breaking. The lamps on its far side
tilt, and one goes over the edge into the mist. [camera → the crack] [camera back] [crew out]*

**Maren:** That's everyone. The whole lower
town is up the road or up the lift.

**Vesper:** And the lower town's about to be
down the falls.

**Maren:** The archive, then. The north
stair. Corvin's crew is still up
there.

*[crew in] [flag m9_evacuated] Control returns. The north stair climbs to the archive's great doors once Crew 2 has
the Ledger (its warp, People and signs).*

### 13. The Ledger

- Room: `fallhaven_archive`, the east vault. Trigger: talking to the Ledger's shelf (slot 13), once `m9_where` and
  the vault unbarred (`m9_hatch`), unless `m9_ledger` (today's `ledger`, rewritten). Before `m9_where`, the shelf's
  line (People and signs).

*The east vault: a small square room behind the unbarred door, shelved to the roof with ledgers bound in blue, a
season to a book, grey with dust. On the top shelf one book is bound in blue and silver, the six marks on its spine.
[crew out] Corvin takes it down and opens it on the lectern. He reads the first page, and stops. [emote Corvin:
silence]*

**Corvin:** This is it. The Ledger of the
Crown.

**Tamsin:** And? Read it, Landslide.

**Corvin:** Not without {HERO}. Not this.
We read it together, or I'm not
reading it.

**Nerissa:** Then carry it. The cliff won't
wait for anybody's reading.

*Corvin shuts the Ledger and holds it against his chest. [walk Gannet → the vault door] Gannet stands in the
doorway with his arms full of charts.*

**Gannet:** I'm taking the rim's charts up the
high stair. All I can carry.
Somebody should keep them.

*[walk Gannet → the inner stair] [hide Gannet] [crew in] [flag m9_ledger] Control returns. Once the lower town is
out (`m9_evacuated`), Crew 1's north stair leads here.*

### 14. The doors

- Room: `fallhaven_archive`, the great hall. Trigger: entering from the north stair, once `m9_meet` (set by that
  warp's scene once `m9_evacuated` and `m9_ledger`, as built), unless `m9_sael` (today's `finale`, rewritten and
  split into scenes 14 to 18).

*[fade in 30] Crew 1 comes up the north stair and in through the great doors. Corvin's crew waits at the reading
table with the Ledger. Sael stands just inside the doors, a hand on each. [show Corvin, Tamsin, Nerissa and Wynn]
[walk {HERO} → the reading table] [crew out]*

**Sael:** Everyone out?

**{HERO}:** Everyone.

*Quiet: [pose {HERO}: nod] and no line.*

**Maren:** Tanner, Ossian, Pip and Old Jory.
Not a broken bone among them.

**Sael:** Good. Then I'll shut the door
behind you.

*[shake 90, 4] The roar outside doubles. Through the open doors the plaza tilts, slowly, like a table with a leg
gone, and slides away into the mist: the well, the Leaning Gull, Marta's, the lamps one after another, going out as
they go. [camera → the doors] [gate: the plaza strip beyond the doors becomes the edge] [camera back] [emote
everyone: exclaim]*

*Sael swings the great doors shut and drops the bar across them. [pose Sael: brace against the doors] The doors
boom. Spray hisses in through the cracks round their frame, and the loose papers on the reading table lift and
flutter toward them.*

**Sael:** Read it. Quick. That's what we're
here for.

*Corvin opens the Ledger on the reading table, and both crews crowd round it. [walk both crews → round the reading
table]*

**Ledger:** THE LEDGER OF THE CROWN. Kept at
the Rimward station, by the order's
own hand.

**Ledger:** Six Wells, sealed. What each seal
holds, it draws: up under the
Spine, into the Crown.

**Ledger:** And what sleeps in each Well is
drawn with it. The great ones do
not wake. They thin.

*[emote Tamsin: exclaim]*

**Tamsin:** The firebird. It was grey. It was
being drunk.

**Ledger:** The Crown holds the centre in
summer. The fields green, the
Pinnacle bright. Every year.

**Ledger:** The cost, as the founders set it:
the rim. Measured each year at the
edge posts. A street a year.

**Corvin:** The edge posts. THE EDGE WAS HERE.
They were never ours. They were the
order's measuring sticks.

**Ledger:** Paid by the rim: Hale's Point.
Gullstone. Kettle Bay. And under
them, a hundred more names.

**Ledger:** To pay, by our reckoning:
Saltcombe. Fallhaven. Then the
next. Then the next.

**Corvin:** Saltcombe. Ossian's town. They
wrote it down before he was even
born.

*[wait 30] The doors boom again. Sael leans into them. Corvin turns to the last page. It is in another hand,
shaky, the ink gone brown.*

**Ledger:** We were told: hold a while. Only
a while. It has been a long while.
I am going home. Forgive us.

*[emote Sorrel: exclaim]*

**Sorrel:** "Hold a while. Only a while." The
founders said that. In the tree's
vision. We heard them.

**Maren:** And that's the order's hand. It's
how we're taught to keep a ledger.
I'd know it anywhere.

**Wynn:** The six lines on my chart. The
lights my mother showed me. That's
what they were. The Wells, running.

**Vesper:** Running to the middle. Paid for
by the edge.

**Corvin:** The rim isn't dying of bad luck.
It's being bled.

*[emote {HERO}: silence] Sael doesn't let go of the bar.*

**Sael:** Well? What does your book say?

**Corvin:** That the rim's the price. Every
town. Us. It always was.

*[wait 30]*

**Sael:** ...Then stop paying.

*[shake 60, 4] One of the bar's brackets cracks out of the stone. The doors bow inward, and the roar comes through
the gap with a sheet of spray. [light: cold white through the cracks round the doors] Sael throws her weight against
them and holds. [pose Sael: brace against the doors]*

**Corvin:** Sael! The doors!

**Sael:** Doors hold. It's what they're for.

**Sael:** Up. The high door. All of you.
Now.

*Nobody moves. [wait 20]*

**Sael:** I said now!

*[walk Wynn, Nerissa, Maren, Sorrel and Vesper → the inner stair] Tamsin takes Corvin by one arm. {HERO} takes the
other. [pose Tamsin: hold Corvin] [pose {HERO}: hold Corvin]*

**Corvin:** Not without you.

**Sael:** Corvin.

*[face Sael → Corvin] She looks back at him over her shoulder, and for a moment she isn't scolding at all. She nods
at the reading chair, where her captain's coat hangs, gone white at the seams with salt.*

**Sael:** Take a coat.

*[still sael_doors] (The still, for the illustrator, is described below.)*

*Corvin takes the coat. [walk Tamsin, Corvin and {HERO} → the inner stair] [fade out 60]*

**Narration:** The doors held long enough.

**Narration:** Captain Sael did not come out.

*[flag m9_sael] [warp fallhaven_cliff, the high door (a new entrance on the second bend)]*

### 15. The falling road

- Room: `fallhaven_cliff`, the archive's high door on the second bend. Trigger: entering, unless `m9_climb`.

*[fade in 20] The cliff road by the archive's high door, at night. It is falling. Below the second bend the road has
already gone into the dark, and stones come bouncing down the switchbacks above and over the edge. The whole cliff
groans. [shake 30, 2] Corvin's crew is ahead, going up: Tamsin with an arm round Corvin, who carries the Ledger and
the coat and doesn't look back. [walk Corvin, Tamsin, Nerissa and Wynn → up the road] [hide them] [crew out]*

*[shake 20, 3] Behind Crew 1 the high door's frame cracks, and the door falls in. [gate: the high door's cells
become rubble]*

**Maren:** Up. Don't stop. Don't look down,
and don't stop.

**Vesper:** Nobody's looking down, medic.

*[crew in] [flag m9_climb] Control returns. The road climbs to the high town gate (puzzles 9 and 10). Each bend
falls away behind the crew as they pass it (step-on spots, People and signs).*

### 16. The boulder goes over

- Room: `fallhaven_cliff`, between the second bend and the last. Trigger: the boulder pushed east off the road
  (`m9_boulder`, puzzle 9).

*The boulder tips over the edge and drops into the mist. [hide the boulder] Nobody stops to listen for it to land.
[flag m9_boulder] Control returns.*

### 17. Fallhaven falls

- Room: `fallhaven_cliff`, the top. Trigger: stepping off the last bend onto the top (a step-on spot), once
  `m9_climb`, unless `m9_top`.

*The top of the road, by the high town gate. Corvin's crew waits there. Corvin stands at the edge with the Ledger
under one arm and the coat over the other, looking down. [walk {HERO} → beside Corvin] [crew out]*

*[shake 120, 4] Below them, the whole of the lower town goes at once: the plaza's last edge, the stairs, the stilts
and the chains, the archive's face with its great doors, all of it sliding away into the white mist, slowly, as if
it were tired. The lamps go out one by one. Then the roar of the falls drops to a deeper note, and holds it.
[camera → the lower town's roofs, at the foot of the road] [gate: the lower town's cells become the edge] [wait 90]
[camera back]*

*[wait 60] Nobody says anything. The roar goes on.*

**Corvin:** She made me take a coat.

*[wait 40]*

**Corvin:** I always forget the coat.

*[pose {HERO}: a hand on Corvin's shoulder] [emote {HERO}: silence] [wait 60]*

### 18. Maren

- Room: `fallhaven_cliff`, the top. Trigger: straight on from scene 17.

*Maren steps forward. She has her notebook in both hands. [face Maren → {HERO}]*

**Maren:** Before we go down to the boats. I
have to say something.

**Maren:** I have to say it now. Or I'll
write it down instead, and that's
how this started.

**Maren:** My reports. Every week, by
Wingull. I told you they were
medical returns.

**Maren:** They went to the Pinnacle. To the
Lord Warden himself. Aurelian Vey.

**Maren:** Where we went. Who we met. The
Forest seal. Corvin's note on the
reef. All of it.

**Maren:** He asked for me by name. A medic
to watch the deputy. The deputy
would lead him to the seal-breaker.

**Maren:** My last report went the night
Ketch came. It said where we were
going.

*[emote Corvin: silence] [emote Vesper: squint]*

**Maren:** I told myself the order keeps
people safe. I wrote it down so
often, I believed it.

**Maren:** Then I read that Ledger, in our
own hand. And I watched Sael shut
those doors.

**Maren:** I'm not asking you to say
anything.

**{HERO} replies:**

1. "I'm glad you told us." · quiet: (Nod)

   **Maren:** Don't be glad yet. If tonight
   hadn't happened, I'd have kept on
   writing. ...I think.

2. "You lied to us." · quiet: (Shake head)

   **Maren:** Yes. Every week, in a neat hand.
   I'm very good at it. That's the
   worst part.

3. "Why tell us now?" · quiet: ...

   **Maren:** Because the next report would
   have been about Sael. And I can't
   write that one.

*Every reply rejoins here.*

**Vesper:** I asked you once who reads your
reports. You said the order.

**Vesper:** You weren't lying. You just didn't
say which bit.

**Sorrel:** Toward the middle. Every week. I
noticed.

**Maren:** I know. You both noticed. I
noticed you noticing. I wrote that
down too.

*She holds the notebook out to {HERO}.*

**Maren:** Every report I sent. I kept a
copy of each one. I always keep a
copy.

**Maren:** You decide what happens to them.
No more reports. Not one.

*{HERO} takes the notebook. [flag m9_confession] (Maren's notebook shows in Key Items from this flag, items §5.)*

**System:** {HERO} took Maren's notebook.

**Maren:** I'm still your medic. If you'll
have me.

*[wait 30]*

**Corvin:** Sael would have asked one thing.
Can she set a bone?

**Corvin:** She can. So she stays.

*[wait 20] Running feet. Ketch comes out through the high town gate and stops dead when he sees their faces. [show
Ketch] [walk Ketch → the gate]*

**Ketch:** The boats are loaded. Every one
that floats, and two that mostly
don't. ...Corvin.

**Corvin:** I know.

*Corvin puts on Sael's coat. It's too big in the shoulders. He turns his back on the falls and walks to the gate.
[pose Corvin: put on the coat] [walk Corvin → the gate] [crew in] [flag m9_top] [fade out 60]*

### 19. The Galeway

- Room: none: lines over black, as mission 4's chase. Trigger: straight on from scene 18.

**Narration:** Every boat that would float put
out from the west cove that night,
and Ketch led them into the storm.

**Narration:** Two nights in the Galeway lanes.
On the second, the Kestrel's keel
cracked. She sailed on anyway.

**Narration:** Far off through the rain, one lamp
went another way: into the storm's
heart, and out of sight.

**Narration:** On the third morning the storm let
them go. And the order's fleet was
waiting.

**Distant voice:** Rimborn boats! By order of the
Lord Warden, turn back! The Calm
is closed to you!

**Ketch:** That's the Holdfast. Corvin, all
of you: sacks of nets. You've had
practice.

**Corvin:** ...I've had practice.

*[wait 40]*

**Ilse:** Holdfast. Belay that order.

**Distant voice:** Commodore? It's the Lord Warden's
own hand...

**Ilse:** I can read, Lieutenant. Signal the
fleet. We escort them in.

**Ilse:** To Marrow Isle.

*[place crew 2 → stonehollow, the cove (in Ketch's skiff, under its nets)] [phase dawn] [warp stonehollow, the cove
(a new entrance)]*

### 20. The landing

- Room: `stonehollow`, the cove. Trigger: entering from the voyage, once `m9_top`, unless `m9_done` (it replaces
  the first half of today's `refugees_settle`).

*[fade in 40] Dawn in Stonehollow's cove, crowded as it has never been: Rimborn boats tied two deep along the jetty,
the Holdfast at anchor off the point under her white-and-blue sails, and the Kestrel coming in last on a towline,
low in the water. Villagers come down the cove path with blankets, lanterns and baskets: Brann at the front, Nell
and Maudie behind with pies. Rimborn climb up onto the jetty with their bundles. On Ketch's skiff, under a heap of
nets, something lumpy keeps very still. [crew out]*

*Ilse comes ashore in the Holdfast's boat, her coat dark with spray. [show Ilse] [walk Ilse → before {HERO}] [face
Ilse → {HERO}]*

**Ilse:** Deputy.

**Ilse:** My orders were to turn every
Rimborn boat back at the Galeway.
In the Lord Warden's own hand.

**Ilse:** I read them twice. Then I looked
at the boats.

*[face Ilse → the jetty] Old Jory is being helped up the steps with his nets. Pip rides on Hanne's hip. Wenna is
handing out pickled eggs to anyone who'll take one.*

**Ilse:** I've read "the rim falls" in a
hundred reports. I had never once
watched it fall.

*[face Ilse → {HERO}]*

**Ilse:** So. Let it be said properly. I
disobeyed an order of the
Pinnacle.

**Ilse:** Written and witnessed.

*[walk Brann → beside Ilse]*

**Brann:** Witnessed.

**Ilse:** Thank you, Keeper.

*[wait 20]*

**Ilse:** The order knew where you'd gone,
Deputy, before I did. It knew in
time to send me orders.

**Ilse:** I'd like to know how.

*[emote Maren: silence] [wait 40]*

**Ilse:** ...Another time.

*[face Ilse → the Kestrel] Tully stands on the Kestrel's deck with one hand on her rail.*

**Ilse:** And you've broken my cutter.

**Tully:** She got us home, Commodore. Every
one of us. Through the lanes and
all.

**Ilse:** Then she did her work.

**Ilse:** I sail for the Pinnacle on the
noon tide, to answer for this. Hold
the island, Deputy.

**Ilse:** Feed these people. That's an
order. Possibly my last one.

**Brann:** Feeding people is keeper's work.
We'll manage.

**Ilse:** I know you will.

*[walk Ilse → the Holdfast's boat] [hide Ilse] Brann turns to the jetty and lifts his voice over the noise.*

**Brann:** Rimborn, sailors, fishers! Marrow
Isle has room for every one of you.
There's pie. There's always pie.

*[face Brann → {HERO}] He looks {HERO} over, slowly, the way he checks an egg.*

**Brann:** Whole. Good. That's the first
thing a keeper checks.

**Brann:** The second's the report. ...Later.
Eat first.

*[crew in] [fade out 40]*

**Narration:** That morning, Marrow Isle took in
what was left of Fallhaven.

*[flag m9_done] Mission 10 begins straight on ([mission-10.md](mission-10.md), scene 1).*

## The still (for the illustrator)

*Still `sael_doors`, 480×320, made like the opening's stills and Celebi's ([opening.md](opening.md),
[mission-05.md](mission-05.md)): painted from a written prompt, reduced to the game's palette and pixel size and
cleaned by hand, on a contact sheet first (decision 23). The message box covers the bottom third, so the focal point
stays in the top two-thirds, with quiet ground at the bottom. No text.*

*The still: the archive's great hall from inside, at night, looking south toward the great doors. The doors fill
the upper middle of the picture: tall, dark, iron-banded, a heavy bar across them, bowing inward. Cold blue-white
light (the falls' mist, lit by the moon) blazes through the cracks round their frame and between their planks, and a
fine spray hangs in it. One iron bracket hangs loose from the stone. Sael stands with her back to the doors, arms out
along the bar, boots braced on the flags, in her shirtsleeves, her cropped grey hair wet with spray. She is looking
back over her shoulder toward the viewer: not afraid, not sad, the face of a captain telling her crew to go, with
the smallest softening at the mouth. Loose papers and a chart lift off the reading table on the left and drift
toward the cracks. A lamp swings on its chain, throwing warm amber across the shelves. On the right, at the edge of
the frame, the empty reading chair. In the bottom third, the floor of the hall and the long shadows of people going
away up a stair out of the picture: quiet ground under the box. Palette: the doors' cold white against the lamp's
warm amber, with Sael between them, half in each. It should feel like the opening's stills: painted, still, a
memory.*

*Motion: a slow push in toward Sael while the page is up; the papers drift; the light through the cracks pulses
with the falls' roar. Then the light through the cracks swells until it whites out the picture, and fades to black
(Celebi's still tears; this one goes white, then dark).*

