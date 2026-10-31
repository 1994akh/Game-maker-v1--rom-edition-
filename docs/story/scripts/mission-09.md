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

   **Ketch:** He said you'd say that. Straight
   off, no arguing. ...I owe him a
   biscuit.

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

*A woman pushes back out through the gate against the crowd, looking at every child who passes: Hanne. [walk Hanne
→ before Ketch]*

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
He bet you'd want a warrant
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
man. He snores like a foghorn.

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

**Corvin:** Two nights of it, in a cutter,
through the lanes. Nobody does
that.

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

**Ledger:** The cost, as the founders reckoned
it: the rim. Measured every year at
the edge posts. A street a year.

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

**Maren:** ...I can.

**Corvin:** Then she stays.

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

- Room: `marrow_cove`. Trigger: entering from the voyage, once `m9_top`, unless `m9_done` (it replaces
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

## People and signs, by room

### Where Crew 1 rests

No lines of its own: the knock (scene 1) plays there. That rest's after-rest line is dropped, since Crew 1 sails
from that door and never comes back to it in this mission.

### `fallhaven_cliff`

*The states:* the way down (`m9_road`, until `m9_sael`), the road intact but shaking, with the lower town climbing
past; falling (`m9_sael` on). Mission 2's rows hide from `m2_done`. Nobody stands here after mission 9: Fallhaven is
a ruin beyond the Galeway (story.md §9) and on no chart in the demo.

- **Wenna** (mission 2), on the first switchback with a jar, the way down:

  **Wenna:** Pickled egg? For the road. I went
  back for them. Twice. Priorities,
  dear.

  **Wenna:** You're Corvin's keeper. He said
  you'd come. I said nobody comes
  to the rim on purpose.

- **Marta** (mission 2), on the second bend with the shop's till in her arms, the way down:

  **Marta:** Carrying the shop up a cliff.
  Again. I've got it down to just
  the till.

  **Marta:** The rest's on the counter. Take
  what you need. The sea will take
  what you don't.

- **Fen** (mission 2), with the Leaning Gull's keys on a ring, the way down:

  **Fen:** I locked up the Leaning Gull.
  Habit. She's going in the sea,
  and I've locked her.

- **Cidrick** (new, mission 10's egg, seeded here), on the last bend: a stocky man with goggles pushed up into his
  hair and a toolbag over each shoulder, the way down:

  **Cidrick:** Cidrick. Shipwright. My family
  built every boat in that harbour.
  And most of the others.

  **Cidrick:** The harbour's gone. So I'm carrying
  its tools. That's what's left of a
  shipwright: the tools.

- **A Rimborn sailor**, at the top by the gate, the way down:

  **Sailor:** Hask's boats went out at dusk, west
  along the rim. Low in the water.
  They weren't carrying people.

  **Sailor:** Powder, if you ask me. Nobody
  asks me.

**Signs and things to examine**

- **The road sign**, at the bottom. The way down:

  **Sign:** CLIFF ROAD TO THE HIGH TOWN.
  Uphill both ways. Under it, in
  tonight's chalk: UP. EVERYONE UP.

- **The edge sign**, halfway. The way down:

  **Sign:** MIND THE EDGE. It minds you.

  *Falling:*

  **Sign:** The edge sign is gone, and the
  edge it stood beside.

- **Wenna's cellar door**, on the second bend (mission 2's). The way down:

  **Sign:** Wenna's cellar door, propped open.
  On every shelf, a gap where a jar
  used to be.

- **The archive's high door**, on the second bend. The way down:

  **Sign:** A heavy door set in the cliff: the
  archive's high door. Barred from
  inside.

  *Falling:*

  **Sign:** Rubble where the high door was.

- **The high town gate**, at the top:

  **Sign:** HIGH TOWN. Fallhaven's spare
  streets. Under it, in chalk: BOATS.
  WEST COVE. HURRY.

- **The boulder** (puzzle 9), falling, until `m9_boulder`:

  **Sign:** A boulder, fresh down off the
  cliff, square across the road. East
  of it, nothing but mist.

- **The rocking slab** (puzzle 10), falling, at the last bend where the low wall was:

  **Sign:** A slab of the road has broken
  loose. It rocks on the edge: out
  over the drop, and back.

- **The bends behind** (falling): as the crew passes each, a step-on spot shakes it loose ([shake 20, 3]) and a gate
  turns its cells to the edge. No lines.

### `fallhaven_lower`

*The states:* the night (`m9_lower_intro`, until `m9_evacuated`); everyone out (`m9_evacuated`, until `m9_meet`).
Crew 1 never comes back after scene 14: the lower town falls in scene 17. Positions are places in the re-clipped
room.

- **The relay stone**, slot 8, by the Leaning Gull's door (the relay role, as built), until `m9_meet`:

  **Sign:** A relay stone, carved with a lamp.
  Knock on it, and its twin in the
  archive hums.

  *Then the relay menu: To Corvin, Rest, Pokémon, Leave (as built).*

- **The fallen chimney**, slot 9, in the west lane (puzzle 1), until `m9_alley`:

  **Sign:** A chimney has come down across a
  door in the west lane. Somebody is
  thumping on the door behind it.

  *Then, from behind the door:*

  **Tanner:** Is that a person? We're in here.
  Me and Ossian. And the bread.

  **Ossian:** Tell Sael we're not dead. We're
  just behind things.

- **Pip**, slot 12, on the old terrace, until `m9_vine`:

  **Pip:** Hello! I can see ALL the boats!
  The steps fell down. I'm fine! I'm
  very high!

  *From `m9_vine`:* scene 5.

- **The sprout**, slot 11, in a crack at the terrace's foot (puzzle 2). Until `m9_vine`:

  **Sign:** A sprout in a crack at the foot of
  the old terrace. Above it, somebody
  small is waving.

  *From `m9_vine`:*

  **Sign:** A vine climbs the cliff to the old
  terrace.

- **Old Jory**, slot 13, on the harbour steps, until `m9_lift`:

  **Old Jory:** Up the cliff road? At my age? I
  said that once before. I meant it
  then, too.

  **Old Jory:** If Sael's lift came down, I'd ride
  it. She's never once let me ride
  it.

  *From `m9_lift`:* scene 7.

- **The lift basket**, slot 14, from `m9_lift` until `m9_ev_c`:

  **Sign:** The archive's lift basket, swaying
  at the foot of the cliff. Its rope
  climbs away into the dark.

- **The old well** (new), on the plaza (puzzle 3). Until `m9_hatch_seen`:

  **Sign:** The plaza's old well, dry for
  years. The flagstones beside it
  shimmer, as if something's there.

  *From `m9_hatch_seen`:*

  **Sign:** The plaza's old well. Beside it,
  the order's hatch.

- **The hatch**, slot 16 (slot 15's hidden row, as built, is what Reveal finds). From `m9_hatch_seen`: scene 6.
  From `m9_hatch` (today's `text_after`):

  **Sign:** The order's hatch, standing open on
  the cellar stair.

- **Dace, a fisher** (today's "Townsman", slot 17), on the plaza with a last armful of nets, until `m9_evacuated`:

  **Dace:** Sael says the archive's cellar runs
  under the plaza. Under the old
  well, my gran said.

  **Dace:** Nobody's seen the door in sixty
  years. Gran said it was painted
  shut. Gran said a lot of things.

**Signs and things to examine**

- **The town sign** (mission 2's):

  **Sign:** FALLHAVEN. Built on solid ground.
  The ground has since changed its
  mind. Chalked under it: AGAIN.

- **The edge board** (mission 2's new board):

  **Sign:** THE EDGE IS HERE. FOR NOW. Under
  it, in fresh chalk: NOW.

- **The crack**, across the plaza:

  **Sign:** A crack across the plaza, a hand
  wide and getting wider. Mist
  breathes up out of it.

- **The Tidewarden notice** (mission 2's):

  **Sign:** BY ORDER OF THE PINNACLE: no
  unlicensed vessel shall enter the
  Calm.

  Chalked underneath: SAFE WHERE?
  THE SEA IS BEHIND US. And under
  that, tonight: IT'S UNDER US NOW.

- **The harbour stair:**

  **Sign:** The harbour stair ends halfway
  down, in mist. The harbour went
  at dusk.

- **The Leaning Gull:**

  **Sign:** THE LEANING GULL. It leans further
  than it did. Every bed is level now,
  if you sleep standing up.

- **Marta's counter** (optional A), until `m9_marta`:

  **Sign:** MARTA'S. A note on the counter:
  GONE UP THE CLIFF ROAD. TAKE WHAT
  YOU NEED. THE SEA GETS THE REST.

  *Then the counter's chest (Items, below) and `m9_marta`. From `m9_marta`:*

  **Sign:** Marta's counter, bare. The note
  is still there.

- **The north stair** (the warp to the archive's great doors, as built). Until `m9_evacuated`:

  **Maren:** Not yet. Three households, the
  captain said. Not one fewer.

  *From `m9_evacuated`, without `m9_ledger`:*

  **Maren:** Corvin's crew hasn't got their
  book yet. The relay stone reaches
  them.

  *With both, the warp's scene sets `m9_meet` and plays scene 14 (as built).*

### `fallhaven_archive`

*The states:* the night (`m9_archive_intro`, until `m9_meet`); both crews (`m9_meet`, until `m9_sael`). The archive
falls in scene 17.

- **The relay stone**, slot 8, by the reading table, until `m9_meet`: the lower town stone's sign and menu ("To
  {HERO}").

- **Sael**, slot 9, at the great doors. Scene 8; then, until `m9_ledger`:

  **Sael:** The book. And Jory's lift. I'm
  watching the plaza. Go on.

  *From `m9_ledger`, until `m9_meet`:*

  **Sael:** You've got it? Good. Wait for your
  keeper. Read it here, where I can
  hear it.

  *From `m9_meet`:* scene 14. The row hides from `m9_sael`.

- **Gannet, the archivist**, slot 10 (today's "Archivist"). Until `m9_where`:

  **Gannet:** The east vault? Dust. Nothing in
  it but dust. Nobody has opened it in
  my lifetime.

  **Gannet:** Please. I have four hundred charts
  to carry, and two arms.

  *Mind Read, until `m9_where`:* scene 9. *From `m9_where`, until `m9_ledger`:*

  **Gannet:** Forty years I kept that shut. You'd
  think it would feel lighter, open.
  It doesn't. Not yet.

  *From `m9_ledger`:* gone up the high stair with the charts (scene 13).

- **The wind-wheel**, slot 11, on its ledge (puzzle 8). Until `m9_lift`:

  **Sign:** The lift's wind-wheel, its little
  sails hanging still. A strong wind
  would turn it.

  *From `m9_lift`:*

  **Sign:** The wind-wheel turns slowly in the
  draught that comes up off the drop.

- **The vault door**, slot 12, until `m9_hatch`:

  **Sign:** The east vault's door, iron-bound.
  It won't give. It's barred on the
  other side, from below.

- **The Ledger's shelf**, slot 13, in the vault. Until `m9_where`:

  **Sign:** Shelves of the order's blue ledgers,
  a season to a book. Hundreds.
  Somebody knows which one matters.

  *From `m9_where`:* scene 13. *From `m9_ledger` (today's `text_after`):*

  **Sign:** The top shelf, and a clean gap in
  the dust where the Ledger was.

- **The great lamp** (puzzle 6), over the east wing's aisle. Until `m9_lamp`:

  **Sign:** A great lamp on a chain, cold. Past
  it, the dark in the east wing is
  very thick.

  *From `m9_lamp`:*

  **Sign:** The great lamp burns. The east
  wing's stacks stand in its light.

- **The fallen case** (puzzle 6), from `m9_lamp` until `m9_case`:

  **Sign:** A tall case of ledgers, down across
  the aisle. It would slide, with a
  push.

- **The smouldering racks** (optional B), in the west alcove, until `m9_charts`:

  **Sign:** A lamp has fallen into the west
  racks. The charts are smouldering.
  Water would save them.

  *Douse on them (Crew 2's Nerissa): [light: grey rain in the alcove] [flag m9_charts] [crew out]*

  **Nerissa:** Not the charts. Never the charts.

  **Wynn:** Every coast on the rim. You saved
  them. I'm going to cry on them now.
  Don't let me cry on them.

  *[crew in] The gear chest behind the racks can be opened (Items, below).*

  *From `m9_charts`:*

  **Sign:** The west racks, wet and black at the
  edges. The charts inside are dry.

- **Corvin, Tamsin, Nerissa and Wynn**, slots 14 to 17, from `m9_meet` (as built): scene 14 only.

**Signs and things to examine**

- **The reading table:**

  **Sign:** A long reading table, scarred by
  sixty years of elbows. The lamps
  over it swing at every shake.

- **The chart racks:**

  **Sign:** Charts rolled in racks to the roof:
  every coast on the rim, and a few
  that aren't there any more.

- **The great doors**, until `m9_meet`:

  **Sign:** The great doors, open on the plaza.
  Sael stands between them. She has
  the key.

- **The inner stair:**

  **Sign:** A stair cut up through the rock to
  the wind-wheel ledge and the high
  door.

- **The high door**, at the inner stair's top, until `m9_sael`:

  **Sign:** The archive's high door, barred
  from inside. The cliff road is on
  the other side.

- **The south way out** (today's warp back to the lower town), for Crew 2, until `m9_meet`:

  **Corvin:** We hold the archive. The lower
  town is {HERO}'s. The relay
  stone's quicker than I am.

### `stonehollow`

Scene 20 only. Mission 10's page takes Stonehollow over from `m9_done`.

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| Marta's counter | `fallhaven_lower`, Marta's (optional A; sets `m9_marta`) | Herb ×3, Antidote ×2, into Crew 1's bag | The engine's chest line, naming `{LEADER}` |
| The west racks | `fallhaven_archive`, the west alcove behind the smouldering racks (Douse, optional B; the dungeon's gear chest, items §13) | Bronze Shield (the Bazaar's tier, items §11; Crew 2's bag) | The engine's chest line, naming `{LEADER}` |
| The Ledger of the Crown | Scene 13 | A story object (items §5's row, shown from `m9_ledger`) | — |
| Maren's notebook | Scene 18 | A story object (new: shown from `m9_confession`, never gone) | Scene 18's system line |
| Sael's coat | Scene 14 | Nothing: a prop Corvin wears from scene 18 | — |

**The Ledger's Key Items text:**

**Item:** The order's ledger from its old rim
station, bound in blue and silver.
The rim's account, paid in towns.

**Maren's notebook's Key Items text:**

**Item:** Maren's notebook: a copy of every
report she sent the Pinnacle, in a
neat medic's hand.

## Puzzles

Both crews, each with the verbs it holds (story.md §7: mandatory puzzles use what the named crew brings). Crew 1:
{HERO}'s Move and Scoop, Maren's Frost and Ply, Sorrel's Growth, Vesper's Reveal, Halt and Cloak. Crew 2: Corvin's
Move and Scoop, Tamsin's Blaze, Nerissa's Frost, Douse and Ply, Wynn's Whirlwind and Mind Read. Two puzzles cross
the relay, one each way. An unsolved puzzle resets when the room is left (decision 71), and every block can always
be got behind again.

**Crew 1, the lower town**

**Puzzle 1. The chimney (Move, as built).**
1. In the west lane, a fallen chimney lies across Tanner and Ossian's door. A niche opens in the lane's wall beside
   it.
2. Stand on the far side and cast Move: the chimney slides into the niche (`m9_alley`, its target cell as built),
   and scene 4 plays.

**Puzzle 2. Pip's terrace (Growth, as built).**
1. The old terrace's steps have fallen. Pip is on top.
2. In a crack at its foot, a sprout. Cast Growth: a vine climbs to the terrace (`m9_vine`, the gate as built).
3. Climb, and talk to Pip (scene 5).

**Puzzle 3. The order's cellar (Reveal, as built, extended).**
1. Dace's line and the well's sign say the archive's cellar runs under the plaza's old well, and the flags beside
   it shimmer.
2. Cast Reveal there: the hatch shows, painted to look like stone (`m9_hatch_seen`).
3. Open it: the cellar's bar is lifted with the Earth (scene 6, `m9_hatch`), which unbars the vault on Crew 2's
   side.

**Puzzle 4. Old Jory's lift (the relay: Crew 2's Whirlwind).**
1. Jory won't climb and won't be carried. His line names Sael's lift.
2. On Crew 2's side, Whirlwind turns the wind-wheel (puzzle 8, `m9_lift`), and the basket comes down by the
   harbour steps.
3. Back with Crew 1, talk to Jory (scene 7, `m9_ev_c`).

**Crew 2, the archive**

**Puzzle 5. The archivist (Mind Read, as built).** Gannet says the vault holds dust. Mind Read hears the Ledger's
name, its shelf, and that the bar is below, under the plaza's well (scene 9, `m9_where`).

**Puzzle 6. The east wing (Blaze, then Move, new).**
1. The east wing's lamps are out, and its aisle is drawn dark (mission 8's hold).
2. Cast Blaze on the great lamp over the aisle: the dark lifts (scene 10, `m9_lamp`), and the fallen case shows
   across the aisle.
3. Stand at its end and cast Move: it slides into the gap between two stacks (`m9_case`), and the vault door is
   reachable. The aisle is open round the case's cells, so it can always be got behind.

**Puzzle 7. The vault (the relay: Crew 1's bar).** The vault's door opens only once Crew 1 has lifted the bar
(`m9_hatch`, a gate on Crew 2's side, as built). The Ledger needs `m9_where` as well (scene 13).

**Puzzle 8. The wind-wheel (Whirlwind, as built).** On the ledge, Whirlwind on the wheel drops the lift (scene 11,
`m9_lift`), for puzzle 4.

**The falling road, Crew 1**

**Puzzle 9. The boulder (Move, new; mission 2's, turned round).**
1. Between the second bend and the last, a boulder comes down square across the road, with the cliff wall west of it
   and the edge east.
2. Stand west of it and cast Move: it rolls east off the edge (scene 16, `m9_boulder`). Pushed north or south it
   only moves along the road, and can always be got behind again.

**Puzzle 10. The rocking slab (Halt, new; mission 6's spar).**
1. At the last bend, where Pip's low wall stood, a slab of the road has broken loose. It rocks out over the drop and
   back across a one-cell gap in the road (a patrol actor), and nobody can cross while it moves.
2. Cast Halt while the slab lies across the gap: for ten seconds the gap can be walked (`m9_slab` once crossed).
   Halted out over the drop, it bridges nothing; wait and try again.

**Optional A. Marta's counter (no verb).** Marta's note says take what you need: the counter's chest.

**Optional B. The smouldering racks (Douse, Crew 2).** Douse puts out the west racks (`m9_charts`), and the gear
chest behind them can be opened.

## Eggs

story.md §9a places no egg in mission 9, and none is added: the mission is the loss. Cidrick, mission 10's egg,
walks up the cliff road with his tools (People and signs), so he isn't a stranger when he opens his yard on Marrow
Isle.

## Either order

Mission 9 always follows both of Crew 1's recruitments and both interludes, so Sorrel and Vesper are always in Crew
1 and nothing differs with the order missions 5 and 6 were played in.

## Not in this mission

Fallhaven's ruin as a memorial you can visit (story.md §9), and Corvin and {HERO}'s heart quest to rebuild its
memorial (§11), both beyond the Galeway after the demo; the one lamp that goes another way in the storm, which is
Hask's Breakers on their way to the Galeway relay (mission 11); the Ledger and Maren's notebook as evidence at her
trial (mission 13) and Ilse's (mission 21, where she answers for Fallhaven); Lord Warden Vey in person; the
Kestrel's end, which is mission 10's funeral; Gannet's charts as the start of the Marrow Isle library (Act II).

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **How Crew 1 gets to the rim:** Corvin sends Ketch through the Galeway to fetch {HERO} ("Tell {HERO} I'm
  asking"), and Ketch's skiff leads the Kestrel through the storm lanes; the order's ships still never cross. The
  knock plays on mission 7's rest hook, wherever Crew 1 sleeps, and sets night (decision 8's "soon after").
- **Maren's choice to come**, and her last report, sent west by Wingull that night: the reason the order's fleet is
  waiting at the Galeway.
- **Fallhaven's geography for its fall:** the boats gathered in the west cove under the high town; the harbour
  gone at dusk; the lower town reached down the cliff road; the archive cut into the cliff above the plaza, with
  great doors on the plaza, a high door onto the cliff road, a wind-wheel lift down to the harbour steps, and the
  order's east vault, barred from a cellar under the plaza's well.
- **The archive was the order's:** its Rimward station on the rim, left "before Sael's time", its vault barred from
  below and its hatch painted to look like stone; the edge posts ("THE EDGE WAS HERE") as the order's measuring
  sticks.
- **The Ledger of the Crown's words:** the seals draw each Well "up under the Spine, into the Crown"; the great ones
  "do not wake. They thin"; the Crown keeps the centre in summer; the rim is the cost, "a street a year"; towns paid
  (Hale's Point, Gullstone, Kettle Bay) and to pay (Saltcombe, Fallhaven); and the last warden's note, "We were told:
  hold a while. Only a while. It has been a long while. I am going home. Forgive us", which echoes the founders in
  Celebi's vision (mission 5) and hints at layer 3 without naming the Farers.
- **Each crew brings a piece to the reading:** Tamsin's grey firebird, Sorrel's "hold a while", Maren's "the
  order's hand", Wynn's six lines and her mother's lights, Vesper's "Paid for by the edge", Corvin's "It's being
  bled".
- **Sael's last night:** "He was somewhere worth being found" (mission 2's "be somewhere worth being found"); "I'll
  be the last. The captain always is" (mission 2's seed, said on the plaza); "Somebody has to lock up"; the lift she
  never let Jory ride; "Then stop paying"; "Doors hold. It's what they're for" (mission 2's "Doors do. It's what
  they're for"); and "Take a coat" (mission 2's "You never take a coat"), with her captain's coat, which Corvin wears
  from then on.
- **Sael's still** and its white-out.
- **Corvin's grief:** "She made me take a coat. I always forget the coat."
- **The three households as mission 2's people:** Tanner (new bread, lodging with Ossian) and Ossian of Saltcombe
  behind the chimney ("Again. We're doing this again"), Pip on the old terrace ("Can we do that again?" "No."), and
  Old Jory, who rides Sael's lift singing the skiff-song, so Crew 1 hears "Under the marrow" and Sorrel hears "Marrow"
  in it. Wenna, Marta and Fen on the road; Hanne's "Tidewardens. On the rim. Helping."
- **New people:** Gannet the archivist, who promised his master never to open the vault and carries the rim's charts
  out (a seed for the Marrow Isle library); Dace the fisher; a sailor who saw Hask's boats go "low in the water"; and
  Cidrick (mission 10's egg).
- **Relay stones as Rimborn lamp-stones,** "Every Rimborn house keeps a pair."
- **Maren's confession:** to both crews, at the cliff top; Lord Warden Aurelian Vey named in Act I for the first
  time; he asked for her by name, "a medic to watch the deputy. The deputy would lead him to the seal-breaker"; "I
  noticed you noticing. I wrote that down too"; her notebook of copies handed to {HERO}, a seed for her trial
  (mission 13) and Ilse's (mission 21); and Corvin's "Can she set a bone?" "...I can." "Then she stays."
- **The way home:** every boat in the west cove follows Ketch through the Galeway; the Kestrel's keel cracks on the
  second night (mission 10's funeral); one lamp goes another way into the storm (Hask, for mission 11); Crew 2 hides
  under Ketch's nets ("sacks of nets. You've had practice", mission 2's "look like a sack of nets"); the Holdfast's
  hail and Ilse's "Belay that order. ...To Marrow Isle."
- **Ilse at the landing:** "I had never once watched it fall"; "Written and witnessed" (her own words from mission
  1), with Brann as witness; "The order knew where you'd gone, Deputy, before I did. I'd like to know how" (Maren
  silent); "And you've broken my cutter" and Tully's answer; sailing for the Pinnacle that noon to answer for it (a
  seed for mission 21), so she never sees the Wayfarer.
- **Brann's welcome:** "There's pie. There's always pie"; mission 1's "Whole. Good. That's the first thing a keeper
  checks", and "The second's the report. ...Later. Eat first."
- **The rewards:** Herb ×3 and Antidote ×2 from Marta's counter, and a Bronze Shield behind the charts.

## Changes to the build

**Rooms**
- **`fallhaven_lower`** re-clipped from the same part of Golden Sun 1's Bilibin as mission 2's `fallhaven`, so the
  plaza, the Leaning Gull, Marta's, the harbour stair and the new edge are where a player left them, with more of
  Bilibin's lanes south and west for the households: the west lane with the chimney's door and niche, the old
  terrace with the sprout's crack and the vine gate (`m9_vine`), the broken harbour steps with the lift's foot, the
  plaza with its crack (a gate opening it wider in scene 12), the old well and the hatch, the relay stone by the
  Leaning Gull, Marta's counter, the north stair (the warp to the archive's entrance 1, as built) and the west alley
  (a warp to `fallhaven_cliff`'s bottom). Entrance 0 moves from the harbour to the foot of the west alley. Outdoor,
  at night, with `clock_hold: night`.
- **`fallhaven_archive`** re-clipped: the great hall (entrance 1 at the great doors) with a strip of the plaza
  outside the doors that a gate turns to the edge in scene 14; the reading table, the racks and the relay stone
  (entrance 0 beside it for Crew 2); the east wing, drawn dark until `m9_lamp` (mission 8's hold), with the great
  lamp and the fallen case (a pushable actor, `m9_case` on its target cell); the vault door (the gate on `m9_hatch`,
  as built) and the vault with the shelf; the west alcove with the smouldering racks and the gear chest; and the inner
  stair to the wind-wheel ledge and the high door (a warp to `fallhaven_cliff`'s new high-door entrance, taken only
  by scene 14). `clock_hold: night`.
- **`fallhaven_cliff`** (mission 2's room), mission 9's states: two new entrances (the high town gate at the top,
  and the high door on the second bend); the people climbing on the way down; in the falling state, gates turning
  the road below the second bend and the high door to the edge and rubble, a step-on spot at each bend that drops it
  behind the crew, the boulder (pushable; falls off the edge, mission 2's rule), the rocking slab (a patrol actor
  over the last bend's gap that Halt stops, its cell walkable while it's halted there: mission 6's spar), and the
  lower town's roofs at the road's foot, which a gate turns to the edge in scene 17. `clock_hold: night`.
- **`stonehollow`:** a new entrance at the cove for the landing; scene 20 (Ilse, the Holdfast's boat, the towed
  Kestrel, Ketch's skiff and its nets as actors) replaces the first half of today's `refugees_settle`.

**Actors and engine**
- **The rest hook** (mission 7's shared file) plays scene 1 once `m8_posters`, unless `m9_started`, and drops that
  rest's after-rest line. Ketch is an actor the scene places at the room's restoration point. The `when` step on the
  Bazaar's gangway that starts mission 9 today comes out (mission 8's page moves it here).
- **The clock:** `phase night` in scene 1, `clock_hold: night` in the three Fallhaven rooms, `phase dawn` before the
  landing.
- **`place_crew`** (as built): Crew 2 into the archive in scene 1, and into Stonehollow's cove (Ketch's skiff) in
  scene 19.
- **Relay stones** as built, hidden from `m9_meet`, when both crews stand together.
- **Today's rows renamed:** `fallhaven_lower` slot 10's "Mother" family becomes Tanner and Ossian, behind the chimney
  until `m9_alley` and staged in scene 4; slot 12 "Child" is Pip; slot 13 "Old man" is Old Jory; slot 17
  "Townsman" is Dace. `fallhaven_archive` slot 10 "Archivist" is Gannet. Every row's text by state (mission 1's
  recommendation).
- **Story objects by flag** (items §5): a `key_items.json` row for Maren's notebook (`m9_confession`), the Ledger's
  row (`m9_ledger`) with its text, and a System line said by the scene.
- **The still** `sael_doors` (the `still` step), with a white-out end.
- **Poses** (art part A's list grows): brace against the doors, hold Corvin, a hand on a shoulder, put on the coat,
  lift.
- **Crowd walks** (mission 2's): the crews to the stair, Tanner and Ossian, Crew 2 up the road.
- **Lines over black** for the Galeway (mission 4's), with a `Distant voice` and Ilse unseen.
- **Blaze lifting a room's dark** (mission 8's hold) and **Douse on smouldering racks** (mission 7's burning cells).
- **Today's lines replaced:** `lower_arrival`, `family_a`, `child_b`, `family_c`, `hatch`, `archive_arrival`,
  `ledger`, `finale`, and every row's text in the two rooms.
- **The Kestrel** is damaged from `m9_done`: Stonehollow's voyage row (Tully, slot 17) gives no chart until the
  Wayfarer (mission 10).

**New scene steps** (README §2): `phase`, `light` (the shimmer, the gust, the amber hands, the cold white through the
doors), `camera`, `pose`, `choice` (both beats, with the quiet set), `crew out` and `crew in`, `still`, `place crew`
(as built), step-on triggers (scene 17 and the bends behind), Psynergy-flag triggers (scenes 4, 10, 11 and 16), a
flag trigger (scene 12) and the rest-hook trigger (scene 1).

**Checks.** `tools/mission9_check` follows the new flow from a rest after `m8_posters`: the knock and Ketch's reply
menu in both voices, the voyage, the road down, the plaza, the three households in any order through the relay
(Jory refusing before the lift), the hatch and the bar, the archivist's thought, the lamp and the case, the wheel,
the vault shut before the bar and open after it, the Ledger, the north stair refusing until both halves are done,
the doors and the still, the falling road (the boulder, the slab), the fall, Maren's reply menu in both voices, the
Galeway, the landing and `m9_done`.
