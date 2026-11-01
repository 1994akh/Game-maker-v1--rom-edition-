# Mission 2: The Drowned Boy

> **Status:** draft for your yes or notes (18 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 2. Today's build: [mission-2-build.md](../../design/mission-2-build.md).

| | |
|---|---|
| Mission | 2, The Drowned Boy (prologue) |
| Plays after | Mission 1's dawn scene, which switches to crew 2 ([mission-01.md](mission-01.md), scene 7) |
| Crew | Corvin alone (crew 2) with Larvitar, his own bag and an empty purse (as built) |
| Rooms | `sea_caves`, `fallhaven_harbour` (the harbour below the lower town, where Ketch's skiff lands: built by engine PR #98), `fallhaven_lower` (the lower town: mission 2's `fallhaven`, merged into it by engine PR #98), `fallhaven_cliff` (the falling cliff road, decision 5: built as ground by engine PR #98, its scenes still to build) |
| Clock | Dawn in the caves; dusk in Fallhaven; night on the cliff road; dawn when crew 1 resumes |
| Flags in | `m1_done`, `m2_started` |
| Flags out | `m2_caves_intro`, `m2_silt_dug`, `m2_marines`, `m2_stone_moved`, `m2_stash`, `m2_fallhaven`, `m2_sael`, `m2_path_cleared`, `m2_cliff_in`, `m2_boulder`, `m2_wenna`, `m2_pip`, `m2_done` |
| Unlocks | Nothing new: the mission shows the rim's stakes first-hand |
| Reply beats | 2, Corvin's (README §3): Sael's question; Hask's offer |
| Fights | None. The caves' encounter table comes with slice 10 |
| Leads into | Crew 1 in Stonehollow; mission 3 starts when {HERO} talks to Ilse (slot 16) |

**The flow.** The underground river spits Corvin out in the Marrow sea caves at dawn. He digs and pushes his way to
the river mouth while Ilse's marines search the wrong caves, and Ketch's skiff carries him through the Galeway to
Fallhaven. Sael, his foster mother, scolds him home; then a street falls into the Rimfalls in front of them, and the
lower town has to climb to the high town tonight. Corvin clears the west alley and the cliff road, digs Wenna out of
her cellar and catches Pip at the edge. At the top, Hask offers to tear out every seal at once. Corvin refuses: one
seal, done right, the Flame Well first. Sael sends him to Embral at first light.

## Scenes

### 1. Washing in

- Room: `sea_caves`. Trigger: entering, unless `m2_caves_intro`.

*[phase dawn] [fade in 40] The Marrow sea caves: a long cavern of wet black rock, its floor a maze of tide pools and
ledges, grey dawn light falling through cracks in the roof. At the south end the underground river spills out of a
low tunnel into a pool.*

*Corvin drags himself out onto the stones, coughing. [pose Corvin: on hands and knees] Larvitar crawls out after
him and shakes itself like a wet dog. [emote Larvitar: sweat]*

**Corvin:** Still with me, Larvitar?

*[emote Larvitar: smile]*

**Corvin:** Good. That makes one of us in
one piece.

*[pose Corvin: stand] [face Corvin → the tunnel]*

**Corvin:** I came for a door, and ended up
fighting {HERO} in front of it.

Five years, and that's how I say
hello.

*[emote Corvin: silence] [face Corvin → north]*

**Corvin:** The sea's that way. I can smell
it. Ketch had better still be
waiting.

*[rest point] [flag m2_caves_intro] Control returns.*

### 2. The marines

- Room: `sea_caves`. Trigger: stepping past the silted arch (a step-on spot), unless `m2_marines`.

*Voices echo through the rock from somewhere far behind, broken up by the water. Lantern light flickers on a wall,
then is gone.*

**Distant voice:** ...the north caves first! Lanterns
up! Commodore's orders!

*[emote Corvin: exclaim] [emote Larvitar: exclaim]*

**Corvin:** North caves. Good. These are the
east ones.

Quietly, Larvitar. Like we were
never here.

*[flag m2_marines] Control returns.*

### 3. Ketch

- Room: `sea_caves`, the river mouth. Trigger: talking to Ketch (a new actor; this replaces today's bare warp to
  Fallhaven).

*The cave opens onto a grey dawn sea. In the river mouth bobs a Rimborn skiff, mast down, its sail bundled under a
net. Ketch, a wiry pilot in a coat made of patches, sits on the gunwale eating an apple.*

**Ketch:** There you are. I'd started on
your funeral song. It rhymed and
everything.

You're soaked, you're bruised, and
you look like a keeper sat on you.
So it went well.

**Corvin:** It went. Can we go?

**Ketch:** Marines on the north shore with
lanterns. Get down in the boat and
look like a sack of nets.

You're good at that. You've had
practice.

*Corvin climbs in and lies down under the net. Larvitar curls up on his chest. [fade out 40]*

**Narration:** Ketch ran the skiff out through
the reef gap and into the Galeway,
by lanes only Rimborn pilots know.

Two days of storm and silence later,
Fallhaven rose out of the spray.

*[phase dusk] [warp fallhaven_harbour, entrance 0]*

### 4. Fallhaven at dusk

- Room: `fallhaven_lower`. Trigger: entering, unless `m2_fallhaven`.

*[fade in 40] Dusk at the end of the world. Fallhaven clings to a cliff above the Rimfalls: houses on stilts and
chains, stairs cut into the rock, washing strung between the roofs. Beyond the east edge the sea pours away into
white mist, and its roar never stops. Neither does the ground's soft trembling. [an ambient shake of 1 every few
seconds while in Fallhaven]*

*[walk Corvin → up the harbour stair to the plaza's edge, cell (14,27)] [face Corvin → east]*

**Corvin:** Home. Still here. Mostly.

The lamp-house is gone. Five days,
and the edge took the lamp-house.

*[flag m2_fallhaven] Control returns.*

### 5. Sael

- Room: `fallhaven_lower`, the plaza. Trigger: talking to Sael (slot 20, cell (16,21)), unless `m2_sael`.

*Sael stands on the plaza with a coil of rope over one shoulder, directing two sailors who are lashing a house to a
post: a tall woman in a captain's coat gone white at the seams with salt, her grey hair cropped short. She hears
footsteps behind her and goes still.*

**Sael:** I know that walk. You drag your
left heel when you've done
something stupid.

*[face Sael → Corvin] [emote Sael: anger] [wait 30] [emote Sael: silence]*

**Sael:** Five days, Corvin. Your note said
"a quick look at Marrow Isle". Five
days.

**Corvin:** I'm back, aren't I?

*[walk Sael → beside Corvin] She takes him by both shoulders, hard.*

**Sael:** You're back. Good. Now I can be
angry with you properly.

Well? Did you find your "only way"?

**Corvin replies:**

1. "I found {HERO}."

   **Sael:** Your keeper friend. The one you
   talk about in your sleep. And?

   **Corvin:** {HERO}'s oath said no. Then we
   fought. Then the floor fell in.

   **Sael:** That's a short story with a lot
   of falling in it.

2. "The door held."

   **Sael:** Doors do. It's what they're for.

   **Corvin:** It takes two Earth Adepts. I
   only brought one.

3. "I woke something."

   *[emote Sael: squint]*

   **Sael:** Something.

   **Corvin:** Under the Vault. It breathed,
   Sael. The whole hall breathed with
   it.

   **Sael:** We'll talk about that when the
   ground stops moving.

*Every reply rejoins here.*

**Sael:** Five years since I fished you
out of that wreck, half drowned and
furious at the sea.

I've watched you look west, toward
the Calm, ever since. I hoped you'd
stop.

You only got better at hiding it.

*[shake 70, 3] The roar of the falls doubles. [camera → the east street] On the east street a whole row of houses
leans out over the mist, slowly, like old men bowing, and goes. [gate: the east street's cells become the edge]
[hide the east street's props and the edge post] [camera back]*

*[emote Corvin: exclaim] [emote Larvitar: exclaim]*

*Tanner stumbles onto the plaza from the east with a loaf under his arm. [walk Tanner → beside Sael]*

**Tanner:** My house. Sael, my house. Forty
years on that street.

**Sael:** Tanner. Are you hurt?

**Tanner:** I was out buying bread. I was
out buying bread, Sael.

*Sael puts a hand on his shoulder. Then she turns to Corvin. [face Sael → Corvin]*

**Sael:** That's the third street this
season, and the cliff under the
lower town is next.

Everyone climbs to the high town
tonight, and a cart's blocking the
west alley. Earth Adept. Clear it.

Then find me at the top. We're not
finished, you and I.

**Corvin:** On it.

*[show the new edge board] [flag m2_sael] Control returns.*

### 6. The alley clears

- Room: `fallhaven_lower`. Trigger: the cart reaching cell (3,15) by Move (`m2_path_cleared`, as built).

*The cart grinds aside and the alley is open. [emote Hanne: exclaim]*

**Hanne:** It's clear! Everyone, up the
cliff road! Bring what you can
carry!

*Townsfolk stream past Corvin into the alley with bundles and children: Hanne, Ossian, Old Jory with his nets,
Marta with a crate. [walk each → the alley] [hide each] Tanner stays on the plaza with Sael.*

**Hanne:** Pip? Pip! ...Pip's run on ahead.
Of course Pip has.

*Control returns. The alley leads up to the cliff road (`fallhaven_cliff`).*

### 7. The cliff road

- Room: `fallhaven_cliff`. Trigger: entering, unless `m2_cliff_in`.

*[phase night] [fade in 30] The cliff road: a narrow road cut into the cliff face, climbing in switchbacks from the
lower town to the high town gate. East of it there's nothing but mist and the roar of the falls. Lanterns bob up
the road ahead as the townsfolk climb.*

*[shake 40, 3] A boulder bounces down the cliff and lands square on the first switchback with a crunch. The
townsfolk behind Corvin stop dead.*

**Ossian:** The road! We can't get past that!

**Corvin:** Stand back. Larvitar, eyes on the
edge.

*[flag m2_cliff_in] Control returns.*

### 8. The boulder goes over

- Room: `fallhaven_cliff`. Trigger: the boulder pushed east off the road (puzzle 5).

*The boulder tips over the edge and drops into the mist. [hide the boulder] [wait 60] Corvin listens for it to
land. It never does.*

**Corvin:** ...Right. Nobody look over the
edge.

*[flag m2_boulder] The townsfolk start up the road again.*

### 9. Wenna

- Room: `fallhaven_cliff`, the cellar ledge on the second bend. Trigger: Scoop on the scree (puzzle 6). Before
  the dig, talking at the door gives the muffled voice (People, below).

*The scree slides away and the cellar door bangs open. Wenna climbs out: a small, round old woman in three shawls,
a jar held to her chest.*

**Wenna:** Corvin! Sael's lad. Oh, you look
very fine, digging like that.

I went down for my pickled eggs, and
the hill came down after me.
Priorities, dear.

Here. It's not a pickled egg, it's a
Nut. I'm not made of pickled eggs.

*[give Nut ×1]*

**System:** {LEADER} received Nut!

*[walk Wenna → up the road] [hide Wenna] [flag m2_wenna]*

### 10. Pip

- Room: `fallhaven_cliff`, the last bend. Trigger: stepping onto the last bend (a step-on spot), once
  `m2_boulder`, unless `m2_pip`.

*The last bend runs along the very edge, with only a low wall between the road and the mist. Pip is up on the
wall, arms out, balancing: a small child in a sailor's jacket three sizes too big. Hanne is further up the road.*

**Pip:** Corvin! Look! I can see right
over the end of the world!

**Hanne:** Pip! Get down from there!

*[shake 50, 3] The wall crumbles. Pip drops over the edge onto a sloping lip of rock and starts to slide toward
the mist. [emote Pip: exclaim]*

**Pip:** Corvin!

*[walk Corvin fast → the edge] [pose Corvin: flat on his front, one arm over the edge] Larvitar grabs Corvin's
boot in its jaws and digs in. [wait 40] [pose Corvin: haul up] Pip comes up over the edge by the collar and lands on
the road.*

**Corvin:** Got you. Got you.

Larvitar, you can let go of my boot
now.

*[emote Larvitar: smile]*

**Pip:** ...Can we do that again?

**Corvin:** No.

*[walk Hanne → Pip] Hanne snatches Pip up in both arms.*

**Hanne:** Never again. You're never leaving
my sight again. Ever.

Thank you, Corvin. Thank you.

*[walk Hanne and Pip → up the road to the top] [flag m2_pip] Control returns.*

### 11. Hask

- Room: `fallhaven_cliff`, the top, by the high town gate. Trigger: talking to Hask, once `m2_boulder`,
  `m2_wenna` and `m2_pip` are all set. Before that, his "still counting heads" line (People, below).

*Hask leans on the gatepost with his arms folded: a lean, weathered man in a sea-coat stitched together from old
sails, a scar through one eyebrow. Two Breakers stand behind him. A Gible sits at his boot and bares its teeth at
Larvitar. [emote Larvitar: anger]*

**Hask:** Sael's stray. Back from the
heartland, and empty-handed.

I watched you shove carts and rocks
about for an hour. You're good at
it.

It changes nothing. Fallhaven will
be gone by the turn of the year.

Then the next town. Then the next.
Until the rim is the Spine, and the
Spine is the falls.

**Corvin:** What do you want, Hask?

**Hask:** You. The seals are a noose with
six knots. I mean to cut all six.

One night. Every Well at once.

I have the people. I have the
powder. What I don't have is an
Earth Adept for the Vault.

**Corvin:** The Vault door takes two. And
the other one just beat me.

*[emote Hask: squint]*

**Hask:** Then bring the other one too.
Come with me, Corvin, and the
waiting ends.

**Corvin replies:**

1. "No."

   **Hask:** Just "no". Sael's favourite
   word. She taught you well.

2. "That could drown us all."

   **Hask:** The rim is drowning now. The
   centre's had six hundred years of
   summer. Let it learn some weather.

3. "And if you're wrong?"

   **Hask:** Then the rim falls a little
   faster. It's falling anyway.
   Look behind you.

*Every reply rejoins here.*

**Corvin:** One seal, opened right, and
watched. Then the next. The Flame
Well first.

**Hask:** Sael's way. Slow, careful, and
too late.

Open your one Well, then. When it
isn't enough, come and find me.

The Breakers keep a lamp lit.

*[walk Hask → through the high town gate] [walk the Breakers and the Gible → after him] [hide Hask, the Breakers
and the Gible] [emote Larvitar: silence]*

### 12. Sael at the top

- Room: `fallhaven_cliff`. Trigger: straight on from scene 11.

*Sael comes up the last bend with the last of the lower town behind her: Tanner with his loaf, and Fen with the
inn's keys. [walk Sael → beside Corvin] [face Sael → Corvin]*

**Sael:** That was Hask's coat going in at
the gate. What did he want?

**Corvin:** Me. For his big night.

**Sael:** And?

**Corvin:** I told him the Flame Well first.
Your way.

*[emote Sael: smile]*

**Sael:** My way. Then it's Embral, and
the Forgeheart.

The monks there won't hand their
seal to a Rimborn for the asking.

**Corvin:** Then I won't ask. I'll earn it.

**Sael:** Ketch sails at first light. Take
the skiff, take bread, take a coat.
You never take a coat.

Your keeper friend, {HERO}. Will
{HERO_SUBJ} come after you?

**Corvin:** Yes. {HERO} always came after
me. It was the best thing about
{HERO_OBJ}.

**Sael:** Then be somewhere worth being
found.

*[fade out 60] [flag m2_done]*

**Narration:** Corvin sailed for Embral at first
light, with bread, and for once,
a coat.

Far to the west, on Marrow Isle,
{HERO} still kept a compass that
pointed nowhere.

*[phase dawn] [crew 1] [warp stonehollow, entrance 3] Crew 1 stands in Stonehollow with its own bag and coins, as
built. Mission 3 begins when {HERO} talks to Ilse.*

## People and signs, by room

### `sea_caves`

No people but Corvin, Larvitar, the distant voice (scene 2) and Ketch (scene 3). The things to examine:

- **The pool**, where the river comes out (the rest point):

  **Sign:** The underground river spills out
  of the tunnel, cold and loud, on
  its way to the sea.

- **The silted arch** (puzzle 1), until `m2_silt_dug`:

  **Sign:** The river has silted up a low
  arch. Sea air comes through the
  mud. Scoop would clear it.

- **The fallen stone**, slot 9, cell (19,8) (puzzle 2), as built:

  **Sign:** A fallen stone chokes the
  passage north. Earth would shift
  it.

- **The chalk mark** (new), by the stash:

  **Sign:** A chalk mark on the rock: a wave
  over a line. Rimborn for "something
  kept here".

- **The crate** (puzzle 3), until `m2_stash`:

  **Sign:** A Rimborn supply crate, wedged
  in front of a niche. It would
  slide, with a push.

- **The chest**, slot 10, moved into the niche: Herb ×2, with the engine's chest line.

- **The view from the river mouth**, beside the skiff:

  **Sign:** Grey sea, grey sky, and somewhere
  past them both, Fallhaven.

### `fallhaven_harbour`

*The states:* the lower town's (arrival, then the fall). Engine PR #98 built the harbour below the lower town:
Ketch's skiff lands at its jetty, entrance 0 (scene 3), and the harbour stair climbs from here to the lower town. As
built, the placeholder arrival (`skiff_in`) plays on the jetty; where scene 4 plays is for your answer (open 145).

- **Ketch** (new), at the foot of the harbour stair, by the skiff. Arrival:

  **Ketch:** Go and see Sael before somebody
  else tells her you're back. Trust
  me.

  I'll be here. Somebody has to bail
  the boat.

  *After the fall:*

  **Ketch:** If the harbour goes, I'm rowing
  out past the stair to wait. Go on,
  they need you.

### `fallhaven_lower`

*The states:* arrival (until `m2_sael`); the street has fallen (`m2_sael`, until `m2_path_cleared`); the alley is
clear (`m2_path_cleared`): Hanne, Ossian, Old Jory and Marta have gone up the alley, and Sael, Tanner and Fen stay,
with Ketch down in the harbour. Cells and slots are the merged lower town's (engine PR #98): the whole of Bilibin,
where the old 25×20 clip's cells moved by (+2, +12), and mission 2's slots 8 to 13 became 20 to 25. Entrance 2 is
the head of the harbour stair, where Corvin comes up from the harbour.

- **Sael**, slot 20, cell (16,21), on the plaza. Scene 5. Then, until the alley is clear:

  **Sael:** The alley, Corvin. They're
  waiting on you.

  *Once the alley is clear:*

  **Sael:** Go on up. I'll be the last. The
  captain always is.

- **Tanner**, slot 23, cell (25,16) on the east street; after the fall, on the plaza beside Sael. He stays in the
  town (today's build hides him). Arrival:

  **Tanner:** My house is on the east street.
  It leans a little more every year.
  So do I.

  Forty years I've lived there. You
  stop hearing the roar after the
  first ten.

  *After the fall:*

  **Tanner:** I've still got the bread. Funny,
  the things you keep.

- **Old Jory, the net-mender** (new), on the harbour steps. Arrival:

  **Old Jory:** Corvin! Back already? Sit down,
  sit down. I'll sing you the one you
  like.

  Under the marrow, under the stone,
  sleeps a ship to carry us home.

  Just a skiff-song. My gran sang it,
  and hers. Nobody knows what it
  means.

  *After the fall:*

  **Old Jory:** Up the cliff road? At my age? Oh,
  very well. As soon as the nets are
  mended.

- **Marta, the shopkeeper** (new), at Marta's. She opens the Fallhaven shop (Herb, Antidote, Elixir, Travel Vest,
  Leather Cap, Wooden Shield; items-and-economy.md §8) after her line, until the alley is clear:

  **Marta:** Buy today. I can't promise the
  shop's here tomorrow. That isn't a
  sales trick. Look out the window.

  *Not enough coins, in the shop:*

  **Marta:** No coins? Then you're Rimborn
  like the rest of us. Come back when
  the sea's been kind.

  *Leaving the shop:*

  **Marta:** Mind the edge.

  *Once the alley is clear, the counter:*

  **Sign:** MARTA'S. A note on the counter:
  GONE UP THE CLIFF ROAD. BACK WHEN
  THE CLIFF IS.

- **Fen, the innkeeper**, slot 25, cell (15,14), at The Leaning Gull (the inn role, free during mission 2). Before
  the rest menu:

  **Fen:** The Leaning Gull. Every bed's
  level, if you sleep on your left
  side.

  Sael's folk rest free tonight.
  Don't tell the others.

  *After resting:*

  **Fen:** You slept through two shakes.
  That's a Rimborn talent, that is.

- **Hanne**, slot 24, cell (4,14), by the alley mouth. Arrival:

  **Hanne:** Corvin! Have you seen Pip? Small,
  loud, always climbing something
  tall.

  *After the fall:*

  **Hanne:** The cart's blocking the alley,
  and the alley's the only way up.
  We have to get the children out.

  *Then scene 6.*

- **Ossian, from Saltcombe** (new), on the plaza. Arrival:

  **Ossian:** I'm from Saltcombe. There isn't a
  Saltcombe any more. I say the name
  so somebody does.

  We sailed for the Calm. The
  Tidewardens turned us back at the
  Galeway. So: Fallhaven.

  *After the fall:*

  **Ossian:** Again. We're doing this again.

- **Pip** (new), on a barrel at the edge of the plaza, on arrival only (from the fall on, Pip has run ahead):

  **Pip:** Corvin! Watch! I can see the
  falls from up here!

  Hanne says I can't climb the cliff
  road wall. I can, though.

**Signs and things to examine**

- **The town sign**, at the top of the harbour stair:

  **Sign:** FALLHAVEN. Built on solid
  ground. The ground has since
  changed its mind.

- **The edge post**, on the east street, on arrival (it falls with the street):

  **Sign:** THE EDGE WAS HERE. Under it, in
  other hands: here. Here. Here.

  *After the fall, a new board at the new edge:*

  **Sign:** A fresh board, the paint still
  wet: THE EDGE IS HERE. FOR NOW.

- **The Tidewarden notice**, on the plaza:

  **Sign:** BY ORDER OF THE PINNACLE: no
  unlicensed vessel shall enter the
  Calm.

  Refugees will be turned back for
  their own safety.

  Chalked underneath: SAFE WHERE?
  THE SEA IS BEHIND US.

- **The archive door**, on the plaza's north side (a seed for mission 9):

  **Sign:** FALLHAVEN ARCHIVE. Charts,
  ledgers and songs of the rim.

  Locked. Captain Sael has the key,
  and nobody gets the key off
  Captain Sael.

- **The inn sign:**

  **Sign:** THE LEANING GULL. Beds, broth,
  and a fine view of the end of the
  world.

- **The shop sign:**

  **Sign:** MARTA'S. Herbs, gear, and no
  promises.

- **The cart**, slot 22, cell (3,18) (puzzle 4):

  **Sign:** A cart lies on its side across
  the alley, one wheel still turning.
  Earth would shift it.

### `fallhaven_cliff` (built as ground by engine PR #98)

*The states:* climbing (from `m2_cliff_in`); at the top, which changes as `m2_wenna` and `m2_pip` are set.

- **Ossian**, on the first switchback (scene 7). After the boulder, climbing:

  **Ossian:** Keep moving. Don't look at the
  edge. Don't look at the edge.

- **Old Jory**, climbing, after the boulder:

  **Old Jory:** Uphill both ways, the sign says.
  It's not wrong.

- **Marta**, climbing with her crate, after the boulder:

  **Marta:** Don't mind me. Just carrying the
  shop up a cliff.

- **The muffled voice**, at the cellar door on the second bend, until `m2_wenna`:

  **Muffled voice:** Hello? Is someone there? I'm not
  dead. I'm just under things.

- **Wenna**, at the top after scene 9:

  **Wenna:** Pickled egg? No? More for me.

- **Hanne**, at the top with Pip after scene 10 (the last bend's step-on spot lies on the only way up, so Pip is
  always safe by the time Corvin reaches the top). Until `m2_wenna`:

  **Hanne:** Wenna's not here. Her cellar is
  on the second bend. She'll have
  gone down for something.

  *Once `m2_wenna`:*

  **Hanne:** Pip is sitting right here until
  we're both old. Thank you, Corvin.

- **Pip**, at the top after scene 10:

  **Pip:** I wasn't scared. Larvitar was a
  bit scared.

- **Hask**, by the high town gate, until scene 11. Before `m2_boulder`, `m2_wenna` and `m2_pip` are all set:

  **Hask:** Your town is still counting
  heads, Sael's stray. Go and finish.

- **Two Breakers**, behind Hask, until scene 11:

  **Breaker:** Hask speaks for us.

  **Breaker:** One night. Every seal. Then the
  rim breathes.

- **Sael**: scene 12 only.

**Signs and things to examine**

- **The road sign**, at the bottom:

  **Sign:** CLIFF ROAD TO THE HIGH TOWN.
  Uphill both ways.

- **The edge sign**, halfway up:

  **Sign:** MIND THE EDGE. It minds you.

- **The boulder** (puzzle 5):

  **Sign:** A boulder the size of a cart,
  square on the road. East of it,
  nothing but mist.

- **The scree** over the cellar door (puzzle 6):

  **Sign:** Loose scree over a cellar door.
  Somebody's knocking underneath.
  Scoop would dig it clear.

- **The high town gate:**

  **Sign:** HIGH TOWN. Fallhaven's spare
  streets. Please wipe your feet.

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| The Rimborn stash | `sea_caves`, the niche behind the crate (today's slot 10 chest, moved) | Herb ×2 | The engine's chest line, naming `{LEADER}` |
| Wenna's thanks | `fallhaven_cliff`, scene 9 | Nut ×1 | Scene 9's system line |

## Puzzles

Corvin's verbs are Move and Scoop, both innate to Earth Adepts; Larvitar has no kept HM yet. Three puzzles in the
caves (one optional) and three on the way out of Fallhaven. As in mission 1, an unsolved puzzle resets when the room
is left and entered again (decision 71), so leaving is always a way back from a wrong push; no room lets a block be
pushed where it can't be got behind again all the same.

**The sea caves**

**Puzzle 1. The silted arch (Scoop, new).**
1. North of the landing pool, the only way on is a low arch, silted up with river mud. A glint marks it as a dig
   spot.
2. Cast Scoop on it: the mud slumps away and the arch opens (`m2_silt_dug`, a gate on that cell).
3. Stepping through plays scene 2.

It teaches Corvin's second verb at once; he needs it at Bastion Rock (mission 7).

**Puzzle 2. The rockfall (Move twice, as built).**
1. A fallen stone (slot 9) chokes the passage north, one cell wide.
2. Stand south of it and cast Move twice: it slides north two cells into a side bay at cell (19,6)
   (`m2_stone_moved`), and the passage is clear.

**Puzzle 3. The Rimborn stash (Move, optional, new).**
1. On a side ledge, a chalk mark (a wave over a line) marks a crate wedged in front of a niche.
2. Stand in front of the crate and cast Move: it slides aside one cell (`m2_stash`).
3. In the niche is the chest: Herb ×2.

It teaches the Rimborn mark, which later rooms can reuse for hidden stashes.

**Fallhaven and the cliff road**

**Puzzle 4. The west alley cart (Move, as built).**
1. The cart (slot 22) lies across the alley mouth.
2. Cast Move from the south: it slides north to cell (3,15), out of the way (`m2_path_cleared`). Scene 6 plays.

**Puzzle 5. The boulder (Move, new).**
1. The boulder sits on the first switchback with the cliff wall west of it and the edge east of it.
2. Stand west of it, on the uphill side, and cast Move: it rolls east one cell, off the edge, and falls (scene 8,
   `m2_boulder`).
3. Pushing it north or south along the road only moves it along the switchback; it can always be got behind again,
   and only the push east clears the road.

**Puzzle 6. Wenna's cellar (Scoop, new).**
1. On a ledge off the second bend, scree has buried a cellar door. Knocking comes from inside.
2. Cast Scoop on the scree: it slides away (scene 9, `m2_wenna`).
3. Hanne's line at the top points here if the player walks past it. Hask won't talk until Wenna is out.

## Eggs

story.md §9a places no egg in mission 2. One of its unplaced Golden Sun nods fits here and is placed as an
invention: **"a kid who falls from a great height in a cutscene and is caught in time"** is Pip at the last bend
(scene 10), caught by Corvin with Larvitar holding his boot.

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **Corvin's trip:** his own idea against Sael's wishes, left as a note ("a quick look at Marrow Isle"), five days
  there and back, with Ketch's help; his landing in the "east" caves while Ilse's marines search the north ones;
  Sael's "You never take a coat" and the coat he takes to Embral.
- **Ketch:** a Rimborn skiff pilot, chatty, with a funeral song half written; the reef gap; two days through the
  Galeway lanes.
- **The Rimborn chalk mark** for "something kept here", and the stash.
- **Sael:** her look; "You drag your left heel"; fishing Corvin out of the Tern's wreck five years ago (mission 1's
  memorial); "I'll be the last. The captain always is" (a quiet seed for mission 9, where she holds the archive).
- **Fallhaven:** the lower town and the high town above it, the cliff road between them, the lamp-house and the east
  street falling, the edge post, the Tidewarden notice and its chalked answer, the archive door (a seed for mission
  9), The Leaning Gull and Marta's.
- **Fallhaven's people:** Tanner surviving with his bread (today's build has him vanish), Ketch, Old Jory and his
  skiff-song "Under the marrow, under the stone, sleeps a ship to carry us home" (a seed for the Wayfarer under
  Marrow Isle, mission 10, and the reason Corvin believes in the door), Marta, Fen, Hanne and Pip, Ossian and the
  lost town of Saltcombe, Wenna and her pickled eggs.
- **Hask:** his look; his Gible (a seed for his Mega Garchomp in mission 18); "Sael's stray"; the seals as "a noose
  with six knots"; his powder (a seed for the Galeway relay in mission 11); "The Breakers keep a lamp lit". He never
  names the Crown, which stays the mission 7 to 9 reveal.
- **Corvin's lines:** "The Vault door takes two. And the other one just beat me", and what he says of {HERO} to
  Sael.
- **The free rest** at The Leaning Gull during mission 2, since Corvin's purse is empty.
- **Pip's fall** as the placed §9a nod (Eggs, above).

## Changes to the build

**Rooms**
- **`fallhaven_cliff`** (decision 5's falling cliff road): switchbacks from the top of the west alley to the high
  town gate, with the edge along the east, the cellar ledge on the second bend, the low wall on the last bend and the
  gate at the top. Built as ground only by engine PR #98, cut from Golden Sun 1's Alpine Crossing, the builder's pick
  (its look is for your answer, open 146). Its terraces are only in the art so far, so how the switchbacks are walked
  is for your answer (open 153). The west alley's top leads into it (built).
- **`sea_caves`:** the silted arch on the main path (a dig spot and a gate), the chalk mark, the crate in front of
  a niche with today's chest (slot 10) moved into it, a step-on spot for scene 2, and Ketch's skiff as an actor
  whose scene replaces today's bare warp to Fallhaven. Extend the clip if the three puzzles don't fit.
- **`fallhaven_harbour`** (built by engine PR #98): scene 3's warp lands the skiff at its jetty (entrance 0), as
  built, and Ketch's row (new) stands by it. As built, the placeholder arrival (`skiff_in`) plays on the jetty; where
  scene 4 plays is for your answer (open 145).
- **`fallhaven_lower`** (mission 2's `fallhaven`, merged into it by engine PR #98): Sael's scene rewritten (scene 5);
  the east street falls (a gate turning its cells into the edge, with the camera pan), and the edge post swaps for the
  new board; Tanner stays and moves to the plaza (today he's hidden); Hask moves to `fallhaven_cliff`; new rows for
  Old Jory, Marta (with the shop, slice 4), Ossian and Pip, and the signs; the townsfolk walk off up the alley in
  scene 6.

**Actors and engine**
- **A pushed block that reaches a void cell falls** (hidden after a short drop): the boulder.
- **`{LEADER}` in the give and chest system lines.** Today they say "{HERO} found..." and would name the hero
  during Corvin's mission.
- **Fen's inn rests free until `m2_done`** (`restoration_price` 0 for mission 2).
- **Hask has two states** (the "still counting heads" line, then scene 11), and his talk waits on three flags.
- **Sael gets a row in `fallhaven_cliff`** for scene 12, and her plaza row hides when the scene starts.
- **The ending** keeps today's `crew 1` and warp to Stonehollow's entrance 3, with `phase dawn` before it.

**New scene steps** (README §2): `choice` (Corvin's replies, with no quiet set), `phase`, `camera`, `pose` (on hands
and knees, stand, flat on his front reaching over the edge, haul up), step-on triggers (scene 2 and scene 10), a
crowd walk (several actors walking off in one step), and Larvitar and Hask's Gible as actors scenes can move
(overworld sprites from the expansion, decision 28).

**Checks.** `tools/mission2_check` follows the new flow: the caves' three puzzles and the marines, Ketch, the
arrival, Sael's reply menu, the falling street, the cart, the cliff road's boulder, Wenna, Pip, Hask's two states
and his reply menu, Sael's farewell and the return to crew 1.
