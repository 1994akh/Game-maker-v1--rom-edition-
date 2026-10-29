# Mission 1: The Keeping Night

> **Status:** draft for your yes or notes (18 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 1. Today's build: [mission-1-build.md](../../design/mission-1-build.md).

| | |
|---|---|
| Mission | 1, The Keeping Night (prologue) |
| Plays after | The opening ([opening.md](opening.md)) and the creator |
| Crew | {HERO} alone, then {HERO} with the first partner |
| Rooms | `hero_house` (new), `stonehollow`, `vault_halls` (re-clipped larger) |
| Clock | Dusk in the house; night from the festival on; dawn for the last scene (day-night-clock.md §1) |
| Flags in | None: a new game |
| Flags out | `m1_woke`, `m1_intro`, `starter_chosen`, `m1_quake`, `m1_vault_in`, `m1_sentinel_aside`, `m1_dug`, `m1_drum_set`, `m1_lock_a`, `m1_lock_b`, `m1_corvin_fled`, `m1_done`, `m2_started` |
| Unlocks | The first partner (Treecko, Torchic or Mudkip, decision 14); 5 Poké Balls and the Lodestar, a dormant Key Item, from Brann (story decision 2, items 1); Move and Scoop, the hero's innate Earth verbs, first used here |
| Reply beats | 2: Corvin at the inner door; Ilse at dawn |
| Fights | Corvin (`corvin_vault`, as balanced: Corvin L4, a L3 Larvitar, the Machete). A loss plays "Try again" |
| Leads into | Mission 2: Corvin's crew in `sea_caves` |

**The flow.** {HERO} wakes late on Keeping Night and goes out to the festival. At the hatchery, Brann gives the first
partner, five Poké Balls and the Lodestar, and then the Vault shakes: someone has forced its doors. Brann sends
{HERO} up the Vault road. Three Move puzzles and an optional dig lead to the inner door, where a masked man waits:
Corvin, alive. He asks for help, is refused, and fights, hoping two Earth Adepts' Psynergy will force the seal. It
stirs the Sleeper instead. The hall splits and Corvin escapes down the underground river. At dawn, Ilse names him a
seal-breaker and makes {HERO} her deputy.

## Scenes

### 1. Waking

- Room: `hero_house`. Trigger: entering, unless `m1_woke` (a new game starts here, after the creator).

*[phase dusk] [fade in 40] The hero's room under the eaves of Brann's cottage: a bed, a mirror, a window over the
Vault road; a stove, a table and Brann's bed in the room beyond. Late sun comes red through the window. Far off,
drums.*

*{HERO} lies on the bed in work clothes, boots still on, quarry dust on everything. [wait 40] [emote {HERO}:
exclaim] [pose {HERO}: sit up]*

**{HERO}:** The drums. I slept through the
lanterns.

*Quiet: [emote {HERO}: sweat] and no line.*

*[flag m1_woke] Control returns. The door leads out to Stonehollow.*

### 2. Keeping Night

- Room: `stonehollow`. Trigger: entering, unless `m1_intro`.

*[phase night] [fade in 30] Stonehollow on Keeping Night. Paper lanterns hang in strings between the roofs.
Drummers play at the foot of the Keeping Stone in the square, and villagers in festival colours dance round it.
North, past the gate, the Vault road climbs dark into the hills.*

*Ada the lamplighter, up a ladder by the north gate, spots {HERO} and climbs down. [walk Ada → beside {HERO}]
[face Ada → {HERO}]*

**Ada:** There you are! The lanterns are
lit and you're still yawning.

Brann's been at the hatchery gate
all evening, looking up the road
for you.

West side, by the old wall. Go on,
before he sends the whole village.

*[walk Ada → her ladder] [flag m1_intro] Control returns.*

### 3. The hatchery

- Room: `stonehollow`. Trigger: talking to Brann (slot 8, today's hatchery role), unless `starter_chosen`.

*Brann stands at the hatchery gate with a lantern: a broad old man in a keeper's brown coat, with a beard like a
hedge. His old Sudowoodo stands by the gate, pretending to be a tree. Behind him are three pens: a Treecko on a
branch, a Torchic on warm sand, a Mudkip in a tub of water. Nell minds the stall beside the gate.*

**Brann:** There's my apprentice. Late, and
with quarry dust on your collar.

Never mind. This Keeping Night is
yours, {HERO}. Nobody else's.

Every keeper of the Vault walks with
a partner. I hatched three this
spring, and I kept them for tonight.

*[face Brann → the pens] [camera → the pens] [camera back]*

**Brann:** Treecko keeps a cool head and
climbs anything. Torchic runs hot
and loves a crowd.

Mudkip digs in, and it will follow
you into any water.

Take your time. Then take your pick.

*[choice "Partner": Treecko, Torchic, Mudkip] The menu must be answered (as built). The picked one hops out of
its pen and comes to {HERO}'s side as the follower (decision 29). [emote partner: heart]*

- Treecko:

  **Brann:** Treecko. It's been watching you
  since you walked in. It'll keep its
  head when you lose yours.

  **System:** Treecko became {HERO}'s partner!

- Torchic:

  **Brann:** Torchic! It'll keep you warm in
  the Vault. And loud.

  **System:** Torchic became {HERO}'s partner!

- Mudkip:

  **Brann:** Mudkip. Steady as stone, that
  one. Like someone I could name.

  **System:** Mudkip became {HERO}'s partner!

*[flag starter_chosen]*

**Brann:** Two more things. Five Poké Balls,
for the Pokémon you'll meet out
there. Ask first. Then throw.

*[give Poké Ball ×5]*

**System:** {HERO} received Poké Ball x5!

*Brann takes a brass compass from his coat and turns it over in his big hands.*

**Brann:** And this. The Lodestar. Keepers
have handed it down since before
my grandmother's time.

A Farer piece, they say, whatever
a Farer was. It has never pointed
anywhere. "Hold it till it wakes."

*[give Lodestar]*

**System:** {HERO} received the Lodestar!

**Brann:** There. Now you look like a
keeper. Come on, the rite's at
moonrise, and the pie is nearly...

*[shake 70, 3] The drums stop dead. Lanterns swing on their strings. A deep boom rolls down the Vault road, then
another, and somewhere up the hill stone grinds on stone.*

*[emote {HERO}: exclaim] [emote Brann: exclaim] [emote partner: sweat]*

**Brann:** That came from the Vault.

*Commodore Ilse comes at a run from the square, one hand on her sword hilt: a tall woman in a Tidewarden's blue
coat, grey at the temples. [walk Ilse → beside Brann] [face Ilse → Brann]*

**Ilse:** Keeper! There's light at the top of
the Vault road. The doors are open.

**Brann:** Open? Nobody opens the Vault
but a keeper.

**Ilse:** Then somebody has.

*[emote Brann: silence] [face Brann → {HERO}]*

**Brann:** {HERO}. The upper halls answer
to Earth, and tonight you're the
keeper. Go up.

I'll keep the village from running
into the sea. My knees haven't
climbed that road fast in years.

**Ilse:** My marines would be lost in
there. The Vault is a keeper's road.
I'll hold the gate till you're back.

**Brann:** The shake will have knocked the
halls about. Statues off their
plinths. You know Move.

Hand out flat. Push with your mind,
not your back. Go on, apprentice.

*[walk Ilse → the north gate] [flag m1_quake] Control returns. The Vault road is open.*

### 4. The upper halls

- Room: `vault_halls`. Trigger: entering, unless `m1_vault_in`.

*[fade in 30] The Vault's upper halls: a long hall of dressed stone, Earth sigils carved on the pillars, torches
guttering in their brackets. Dust hangs in the air from the shake. On the threshold lies the Vault's seal-bar, a
bronze beam as thick as an arm, snapped in two.*

*[emote partner: sweat] [walk {HERO} → one cell north] [emote {HERO}: question]*

**{HERO}:** Someone forced it. Tonight, of
all nights.

*Quiet: [emote {HERO}: scowl] and no line.*

*[flag m1_vault_in] Control returns. The puzzles below lead north to the inner door.*

### 5. The inner door

- Room: `vault_halls`, the inner door chamber. Trigger: stepping onto the chamber's threshold (a new step-on
  trigger; today, talking to Corvin), unless `m1_corvin_fled`.

*The inner door chamber: a round room with the inner door at its north end, a slab of dark stone with two
handprints cut side by side into its seal. Along the east wall a deep crack hums with running water somewhere below.
A figure in a grey hooded coat and a white mask of carved wood stands with one palm flat on the seal, back to the
room. [sprite Corvin: 34, masked] Until the unmasking the speaker shows a name tag only, "Masked figure", with no
portrait, so the portrait doesn't give him away.*

*[walk {HERO} → three cells south of the figure] The figure doesn't turn.*

**Masked figure:** I knocked. The Vault knocked
back. You'll have felt it.

Every soul on the island down at
the lanterns, and they send the
apprentice up alone.

*[face Masked figure → {HERO}]*

**Masked figure:** Hello, {HERO}.

*[emote {HERO}: exclaim] [emote partner: question] The figure lifts the mask away. [sprite Corvin → 35] He lets
it fall by the door.*

**{HERO}:** Corvin?

*Quiet: no line; the ! is enough.*

**Corvin:** You look like you've seen a
ghost. Fair. I'd look the same.

Five years. The sea nearly kept me.
The Rimborn pulled me out, and I've
sailed with them since.

I'd have written. I didn't know what
to say. I still don't, so I'll be
quick.

*[face Corvin → the door] [light: the two handprints glow a faint amber]*

**Corvin:** It takes two Earth Adepts, side
by side. That door hides the only
way to save my home.

*[face Corvin → {HERO}]*

**Corvin:** Not this home. The other one. A
town on the rim, falling off the
world a street at a time.

Will you help me open it?

**{HERO} replies:**

1. "Show me what's there." · quiet: (Nod)

   **Corvin:** You'd say yes? With Brann's oath
   still in your mouth?

   No. You'd stop halfway, hands on
   the seal, hating yourself. I know
   you.

2. "No. I swore an oath." · quiet: (Shake head)

   **Corvin:** I know. I watched you practise
   the words when we were small. I
   hoped you'd forget them.

3. "Corvin... why?" · quiet: ...

   **Corvin:** Because I've knocked on every
   other door there is. This is the
   last one.

   The rest I'll tell you somewhere
   your oath can't hear.

*Every reply rejoins here.*

**Corvin:** So. If you won't open it with
me, you'll open it against me.

Two Earth Adepts in one hall, and
Psynergy flying. Let's see if the
seal can tell the difference.

*Larvitar trundles out from behind Corvin and plants its feet. [emote Larvitar: anger] [emote partner: anger]
[battle corvin_vault]*

*If the fight is lost, "Try again" plays and the fight restarts as it began (as built). Corvin's line as it
restarts:*

**Corvin:** Again? Fine. I've had five
years of practice.

### 6. The hall splits

- Room: `vault_halls`. Trigger: winning the fight (Corvin's `scene_after`).

*Corvin staggers back against the inner door, breathing hard. Larvitar flops down at his feet. [pose Corvin: lean
on the door]*

**Corvin:** You got strong. Brann's drills?
Every morning, in the rain?

*[wait 30] The floor shudders. Behind Corvin, the two handprints in the seal flare a deep red, three slow pulses,
like breathing. [light: red pulse ×3 from the door] [shake 40, 1]*

*[face Corvin → the door] [face {HERO} → the door]*

**Corvin:** That isn't me.

**{HERO}:** Not me either.

*Quiet: [pose {HERO}: shake head] and no line.*

*A long, low sound comes up through the floor, more felt than heard. Dust pours from the ceiling. [shake 90, 3]
The red light sinks out of the door and runs across the floor in a jagged line to the crack along the east wall.*

**Corvin:** Something down there just
turned over in its sleep.

*[shake 30, 4] With a crack like a mast breaking, the floor along the east wall falls away. Below, the underground
river roars past in the dark. [gate: the east wall's cells become the river's edge] [light: back to torchlight]*

*Corvin looks down at the water, then at {HERO}.*

**Corvin:** Well. That's my way out.

I never meant to hurt anyone.
Tell Brann I'm sorry about his
halls.

And when you want to know what that
door is for, come and find me. I'll
tell you everything.

*[walk Corvin → the river's edge] [face Corvin → {HERO}]*

**Corvin:** Don't follow. The river's cold,
and you've got a village to keep.

*Corvin drops into the river. Larvitar jumps in after him. [hide Corvin] [hide Larvitar] [wait 40] [emote {HERO}:
silence]*

*The white mask lies by the inner door where Corvin let it fall. [walk {HERO} → the mask] [hide the mask] {HERO}
takes it (a prop, not an item).*

*[flag m1_corvin_fled] Control returns. The way back down is open.*

### 7. Dawn

- Room: `stonehollow`. Trigger: entering from the Vault road, while `m1_corvin_fled` and unless `m1_done`. It
  replaces Ilse's quest role.

*[phase dawn] [fade in 40] Dawn. The lanterns have burned out on their strings. Half the village waits at the
north gate in festival clothes gone grey with dust: Brann at the front, Ilse beside him, her marine behind. Gary is
nowhere near the front.*

*[walk Brann → beside {HERO}] [emote Brann: smile]*

**Brann:** Whole. Good. That's the first
thing a keeper checks.

**Ilse:** And the second is the report.
What was up there?

*[face {HERO} → Brann]*

**{HERO}:** It was Corvin. He's alive.

*Quiet: [emote {HERO}: silence] and no line.*

*{HERO} holds out the white mask. Brann takes it and turns it over in his hands for a long moment. (He knows it
on sight, so the quiet hero's silence still tells the scene who it was.)*

**Brann:** I carved this mask. A Keeping
Night, years back, for a boy who
hatched my eggs in his boots.

...Corvin. So the sea gave him
back.

**Ilse:** Whatever he was to you both, he
forced the Vault on the one night
we honour it.

The order has a word for that.
Seal-breaker.

My marines are searching the north
shore caves, where the charts say
the river comes out.

But I need someone who knows his
face.

*[face Ilse → {HERO}]*

**Ilse:** Will you hunt him, {HERO}?

**{HERO} replies:**

1. "I'll find him." · quiet: (Nod)

   **Ilse:** Good. Find him before someone
   less kind does.

2. "He was my friend." · quiet: (Shake head)

   **Ilse:** I know. That's why it has to
   be you. A stranger would only see
   a seal-breaker.

3. "What happens to him?" · quiet: ...

   **Ilse:** That depends on what he does
   next. And on who reaches him first.

*Every reply rejoins here.*

**Ilse:** So. Let it be said properly.

{HERO} of Marrow Isle, keeper's
apprentice. From this dawn, deputy
of the Tidewardens.

Written and witnessed.

**Brann:** And still my apprentice. Deputy
or no, you come home for supper.

**Ilse:** The Kestrel stays in the cove a
few days. When I have work for you,
you'll hear it from me first.

*[flag m1_done] [fade out 40]*

**Narration:** All that long night, the
underground river ran on beneath
Marrow Isle.

At dawn, it gave up what it took.

*[crew 2] [flag m2_started] [warp sea_caves, entrance 0] Mission 2 begins ([mission-02.md](mission-02.md)).*

## People and signs, by room

### `hero_house` (new)

*The states:* before the Vault (until `m1_corvin_fled`); after the Vault (`m1_corvin_fled`).

- **Brann's note**, on the table. Before the Vault:

  **Note:** {HERO}. Come by the hatchery
  before moonrise. Don't be late.

  You'll be late. Come anyway.
  Brann.

  P.S. Wash your face.

  *After the Vault:*

  **Note:** Brann's note from Keeping Night.
  You were late. He was right.

- **The mirror**, by the bed (the decided mirror: the creator in cosmetics mode). Before the Vault:

  **Mirror:** Quarry dust in your hair. On
  Keeping Night, of all nights.

  *After the Vault:*

  **Mirror:** You look older than you did
  last night.

  *Then, in both:*

  **Mirror:** Change your look?

  *[yes/no] Yes opens the mirror.*

- **The bed**, the home bunk (clock decision 3). Before `m1_done`:

  **Bed:** No sleeping. It's Keeping Night.

  *From `m1_done`:*

  **Bed:** Your own bed. Sleep until...?

  *[menu: Dusk, Dawn, Not now]*

- **Brann's bed**, in the far room:

  **Sign:** Brann's bed, made with corners
  sharp enough to slice bread.

- **The bookshelf:**

  **Sign:** Brann's books. Eggs and the
  Patient Hand. A Keeper's Almanac.

  Six Hundred Keeping Nights, volume
  nine. Volumes one to eight are
  missing. Brann says he lent them.

- **The stove:**

  **Sign:** A pot of Brann's porridge. It
  has been simmering since spring.
  It is not ready.

- **The egg basket**, by the stove. Before the Vault:

  **Sign:** A speckled egg in a warm basket.
  Brann talks to it when he thinks
  nobody's listening.

  *After the Vault:*

  **Sign:** The egg wobbles. It might be
  listening back.

- **The window.** Before the Vault:

  **Sign:** Through the glass, the Vault
  road climbs the hill north of the
  village, dark between the lanterns.

  *After the Vault:*

  **Sign:** Morning on the Vault road. The
  gate is barred again.

### `stonehollow`

*The states:* the festival (until `m1_quake`); after the quake (`m1_quake`, until `m1_corvin_fled`); after the
Vault (`m1_corvin_fled`, until mission 3's script takes over). Positions are cells on today's 31×24 clip; new people
give a place instead.

- **Keeper Brann**, slot 8, cell (3,9), at the hatchery gate. The festival: scene 3. After the quake:

  **Brann:** Hand flat. Mind, not back. And
  come home, apprentice.

  *After the Vault:*

  **Brann:** I scratched his name off the
  memorial stone. First good news
  that stone's had in five years.

- **Brann's Sudowoodo** (new), by the hatchery gate. The festival:

  **Sign:** A small tree by the hatchery
  gate. It blinks at you.

  *After the quake:*

  **Sign:** Brann's Sudowoodo is holding very
  still. Even for a tree.

  *After the Vault:*

  **Sign:** The Sudowoodo has a lantern
  hung on one arm. It seems proud.

- **The hatchery pens** (new), behind Brann. Before the pick, each pen:

  **Sign:** Treecko eyes you coolly from
  its branch.

  **Sign:** Torchic hops about on the warm
  sand, cheeping at the drums.

  **Sign:** Mudkip blows bubbles in its
  tub and watches you over the rim.

  *After the pick, the two left behind (the builder shows the right two):*

  **Sign:** It watches you go. Brann will
  find it a good keeper.

- **Nell**, at the hatchery stall (new), beside Brann. She opens the Stonehollow stall (Herb, Antidote, Poké
  Ball; items-and-economy.md §8) after her line. The festival:

  **Nell:** Herbs, Antidotes, Poké Balls.
  Brann says no credit, and he says
  it twice.

  I'll be a keeper one day. Brann
  says I'm too impatient. I say he's
  too slow.

  *After the quake, and after the Vault:*

  **Nell:** Buying for the road? Herbs
  first. Always Herbs first.

  *Not enough coins, in the shop:*

  **Nell:** That's more coins than you've
  got. Brann would say: patience.

  *Leaving the shop:*

  **Nell:** Mind how you go.

- **Commodore Ilse.** The festival, at the Keeping Stone (a new row):

  **Ilse:** {HERO}. Brann tells me tonight's
  your night. I sailed from the
  Pinnacle to watch.

  Six hundred years of quiet, and the
  seals to thank for it. Nights like
  this are why I took the oath.

  *After the quake, at the north gate (a new row):*

  **Ilse:** Go on, {HERO}. I'll hold the
  gate till you come down.

  *After the Vault:* no idle line. Scene 7 plays her part and crew 2 takes over at once, so slot 14 is never
  seen again; it hides from `m1_done`, which the dawn scene sets. From `m2_done`, when crew 1 is back, her slot
  16 belongs to mission 3's script.

- **A Tidewarden marine** (new), beside Ilse; goes where she goes. The festival:

  **Marine:** Commodore's orders: enjoy the
  festival. I'm enjoying it. At
  attention.

  *After the quake:*

  **Marine:** Nobody up the Vault road but the
  keeper. Commodore's orders, and
  keeper law besides.

  *After the Vault:*

  **Marine:** Deputy {HERO}. Congratulations.
  I think.

- **Ada, the lamplighter**, slot 15, cell (15,4), by the north gate with her ladder. She opens the festival
  (scene 2). Afterwards, the festival:

  **Ada:** Two hundred lanterns, and I lit
  every one. My arms will tell me
  about it tomorrow.

  *After the quake:*

  **Ada:** Half my lanterns went out in that
  shake. The rest are swinging like
  they've had cider.

  *After the Vault:*

  **Ada:** Keeping Night has never ended in
  a quake before. Old Moss says so,
  and he's seen seventy of them.

- **Dunstan, the quarry foreman**, slot 10, cell (24,7). The festival:

  **Dunstan:** No carts tonight, no picks, no
  dust. Just pie. A foreman could get
  used to it.

  Tomorrow we're back to the west
  road. That rockslide won't shift
  itself.

  Unless you fancy trying Move on it.
  Ha! It's the size of the inn.

  *After the quake:*

  **Dunstan:** That wasn't a quarry blast. I
  know every blast on this island,
  and that wasn't one.

  *After the Vault:*

  **Dunstan:** Corvin. Fell in my gravel pit
  twice in one summer, that boy. The
  sea couldn't keep him either.

- **Old Moss**, slot 11, cell (5,17), on the bench by the memorial stone. The festival:

  **Old Moss:** Seventy Keeping Nights I've seen.
  The lanterns get brighter and the
  pie gets worse.

  The rite's the same as ever, mind.
  Six hundred years, the same words.
  That's a comfort.

  *After the quake:*

  **Old Moss:** Seventy Keeping Nights, and the
  ground never once joined in.

  *After the Vault:*

  **Old Moss:** The Keeping Stone cracked last
  night, right down the old words.
  I don't like that. Not one bit.

- **Maudie, the innkeeper**, slot 9, cell (22,12), at The Quiet Stone (the inn role). Before the rest menu, in
  every state:

  **Maudie:** The Quiet Stone. A warm bed and
  a cold supper, or the other way
  round if you ask nicely.

  *After resting:*

  **Maudie:** Up already? The pie's still on
  if you want it. It's always on.

- **Gary Rivalson** (new), outside the Rivalsons' house, next door to Brann's cottage. The festival:

  **Gary:** Well, well. {HERO}. Late to your
  own Keeping Night. Typical.

  I'd show you my partner, but it's
  resting. It's very talented. You
  wouldn't understand.

  Smell you next tide!

  *After the quake:*

  **Gary:** A quake? I'd go up and sort it
  myself. But someone has to guard
  the pie table.

  *After the Vault:*

  **Gary:** So it was Corvin, back from the
  dead. He always did steal the big
  scenes.

  Every story needs a hero, and I'm
  not saying it's me. I'm letting
  you work it out, {HERO}.

  Smell you next tide!

- **Corla, a fisher** (new), at the head of the south road, mending a lobster pot. The festival:

  **Corla:** Saw a skiff at dusk, no lights,
  slipping round the east point.
  Rimborn rig, by the sail.

  Nobody runs dark on Keeping Night
  unless they've a reason.

  *After the quake:*

  **Corla:** Was that the Vault? The water in
  the cove jumped like a startled
  Magikarp.

  *After the Vault:*

  **Corla:** That dark skiff. I should have
  rowed out and asked its business.

- **Tobin, a child** (new), by the Keeping Stone, holding a red paper lantern shaped like a great beast. The
  festival:

  **Tobin:** Look! I made a Sleeper lantern.
  It's the big red one that sleeps
  under the Vault.

  Gran says if you're good all year,
  it never wakes up.

  *After the quake:*

  **Tobin:** Was that the Sleeper? Was it
  because I wasn't good? I was mostly
  good.

  *After the Vault:*

  **Tobin:** Gran says the Sleeper only rolled
  over. I'm being extra good. Just in
  case.

- **Tully, the Kestrel's mate**, slot 17, cell (13,1) (today's voyage role, before `has_ship`). The festival:

  **Tully:** The Commodore's cutter, the
  Kestrel. Fastest hull in the Calm.
  I polished every inch of her.

  *After the quake, and after the Vault:*

  **Tully:** The Kestrel's yours once the
  Commodore says so. Not yet.

**Signs and things to examine**

- **The village sign**, at the head of the south road:

  **Sign:** STONEHOLLOW, MARROW ISLE.
  Home of the Vault.
  Mind the quarry carts.

- **The Keeping Stone**, in the middle of the square. The festival:

  **Sign:** The Keeping Stone. Six marks are
  cut in it, worn smooth by six
  hundred years of hands.

  Carved beneath them: WHAT WAS
  SEALED, WE KEEP. WHAT WE KEEP,
  KEEPS US.

  *From the quake on:*

  **Sign:** A fresh crack runs down the
  Keeping Stone, right through the
  old words.

- **The notice board**, by the inn:

  **Sign:** KEEPING NIGHT. Lanterns at dusk.
  The rite at moonrise. Pie when the
  pie is ready.

  TIDEWARDEN NOTICE. The element
  tithe falls due at the turn of the
  season. By order of the Pinnacle.

- **The memorial stone**, by Old Moss's bench. Until `m1_corvin_fled`:

  **Sign:** FOR THOSE THE SEA KEPT.

  The Tern, lost off the Galeway
  five years ago. Skipper Ebb. Orrin.
  Corvin.

  *After the Vault:*

  **Sign:** FOR THOSE THE SEA KEPT.

  The Tern, lost off the Galeway
  five years ago. Skipper Ebb. Orrin.

  A neat line has been scratched
  through a third name. The hand
  looks like Brann's.

- **The hatchery sign:**

  **Sign:** BRANN'S HATCHERY. Eggs hatch
  when they're ready, not when you
  are.

- **The inn sign:**

  **Sign:** THE QUIET STONE. Beds, baths,
  and Maudie's pie.

- **The Rivalsons' door** (new), next to Brann's cottage:

  **Sign:** THE RIVALSONS. Below it, a
  smaller sign: GARY'S HOUSE, REALLY.

- **The Mercury-blue puddle** (new, the egg), beside the village well:

  **Sign:** A puddle of startling blue. It
  hasn't rained in a week.

  *With Frost on it (from mission 3, once Maren travels with {HERO}):*

  **Sign:** The puddle refuses to freeze. It
  looks rather pleased with itself.

- **The Vault road gate** (the north warp's closed line, until `m1_quake`):

  **Sign:** The Vault road is barred for
  Keeping Night. Only the Keeper
  lifts the bar, at moonrise.

- **The west gate** (the west warp's closed line, progression decision 4, until our world map opens it):

  **Sign:** The west road to the quarries.
  A rockslide closed it in spring.
  It's far too big for Move.

- **The buried chest**, slot 12, stays hidden until Reveal (mission 6 on) and gives Herb ×2 with the engine's chest
  line, as built.

### `vault_halls`

No people but Corvin (scenes 5 and 6). The things to examine, from the entrance north:

- **The snapped seal-bar**, on the threshold:

  **Sign:** The Vault's seal-bar, a bronze
  beam as thick as your arm. Snapped
  clean through, from the outside.

- **The entrance plaque:**

  **Sign:** THE MARROW VAULT. Here the Earth
  Well sleeps. Walk softly.
  Keep what is kept.

- **The mural**, along the gallery wall:

  **Sign:** A carving runs along the wall: six
  robed figures, each closing a great
  door. Their faces are worn away.

- **The Sentinels**, slots 9 and 10 (puzzle 1):

  **Sign:** A stone Sentinel, carved as a
  keeper with a staff. The shake has
  knocked it off its plinth.

- **The loose earth** (the optional dig):

  **Sign:** Loose earth, shaken down from a
  cracked wall. Something glints in
  it. Scoop would dig it out.

- **The crack** (puzzle 2). Before the drum:

  **Sign:** The shake has split the floor.
  Too wide to step over, too dark to
  see the bottom.

  *After the drum:*

  **Sign:** The pillar drum sits snug in the
  crack, its top level with the
  floor.

- **The pillar drum:**

  **Sign:** A drum of fallen pillar, round
  and heavy. It would roll, with a
  push.

- **The lock gate** (puzzle 3):

  **Sign:** A gate of stone bars. Two
  sockets in the floor before it are
  cut with the Earth sigil.

  The words above the gate: TWO
  KEEPERS STAND WHERE ONE CANNOT.

- **The small keeper statues**, two:

  **Sign:** A small stone keeper on a round
  base. It would slide, with Move.

- **The sockets**, two:

  **Sign:** A socket cut with the Earth
  sigil, the size of a statue's base.

- **The inner door**, slot 11, from `m1_corvin_fled` (the first branch of today's `inner_door` scene):

  **Sign:** The inner door. Its seal is warm
  under your palm, like something
  asleep.

  Two handprints, side by side. It
  opens only to two Earth Adepts,
  together.

- **The river's edge**, the new east edge, from `m1_corvin_fled`:

  **Sign:** The underground river runs loud
  and black toward the sea. There's
  no sign of Corvin.

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| Brann's gift | Scene 3 | Poké Ball ×5, the Lodestar | Scene 3's system lines |
| The glint | `vault_halls`, the gallery (Scoop) | Nut ×1 | **System:** {HERO} found Nut! (the engine's line) |
| The lock chest | `vault_halls`, a nook in the lock antechamber | Herb ×2 | The engine's chest line |
| The buried chest | `stonehollow`, slot 12 (Reveal, later) | Herb ×2 | As built |
| Corvin's mask | Scene 6, then handed to Brann | Nothing: a prop | — |

**The Lodestar's Key Item text** (the Items screen, story decision 1: dormant in Act I):

**Item:** A brass Farer compass with a
needle of blue glass. It hangs
still, pointing nowhere.

## Puzzles

The hero's verbs here are Move and Scoop, both innate to Earth Adepts. The partner's HMs (Cut, Surf) still wait on
their story flags. Three Move puzzles stand between the entrance and the inner door, and one optional Scoop. They
all fit one re-clipped `vault_halls` (changes, below).

**Pushed things stay where they're pushed** once slice 4 saves them in place, so no puzzle may rely on leaving the
room to reset it: every room is laid out so a block can never be pushed into a cell it can't be brought back from
(no reachable corner, and no wall on the side the next push needs).

**Puzzle 1. The Sentinels (Move, as built).**
1. The corridor north out of the entrance hall is two cells wide, blocked by two Sentinels side by side (slots 9
   and 10).
2. An alcove opens in the east wall beside them.
3. Stand west of the east Sentinel and cast Move: it slides east into the alcove (two cells; `m1_sentinel_aside`
   when it reaches cell (9,9)).
4. Pushing either Sentinel north up the corridor clears the way too, as built; the space beyond is wide enough that
   it never blocks puzzle 2.

It teaches that Move pushes a thing the way you aim it (Golden Sun's free aim: open question 120).

**Puzzle 2. The split floor (Move, new).**
1. Past the Sentinels, the shake has split the floor right across the hall: a crack one cell wide, wall to wall.
2. In a bay on the near side lies a pillar drum, knocked from a broken column.
3. Push the drum north into the crack. It drops in and wedges, its top level with the floor (`m1_drum_set`; a gate
   repaints that cell as floor). Any cell of the crack works.
4. The bay opens south onto the hall, so the drum can always be got behind and pushed north again.

It teaches that Move can fill a gap.

**Puzzle 3. The keepers' lock (Move twice, new).**
1. The antechamber before the inner door is closed by a gate of stone bars. In front of it, two sockets cut with
   the Earth sigil sit in the floor, two cells apart.
2. Two small keeper statues stand in the room. The first is in the open, two cells west of the west socket, in the
   same row. The second stands one row north of the sockets and three cells east of the east socket.
3. The first: push it east twice onto the west socket (`m1_lock_a`). It settles with a click, and its eyes glow
   amber.
4. The second needs pushes in two directions: west three times and south once, in either order, each one aimed
   (`m1_lock_b` on the east socket).
5. With both statues on their sockets, the bars sink into the floor (a gate on both flags). The words above the
   gate echo the inner door: two keepers, where one cannot.

It teaches that a pushed thing needs room to slide into, and sets up the two-Earth door.

**Optional. The glint (Scoop, new).**
1. In the Sentinel gallery, earth has poured from a cracked wall into a heap with a glint in it (a dig spot).
2. Cast Scoop on it: {HERO} digs out a Nut (`m1_dug`).

It teaches the Earth Adepts' second verb, which Corvin needs at Bastion Rock (mission 7).

## Eggs

- **Gary Rivalson** (story.md §9a, the hero's smug rival from next door). Outside his house in Stonehollow, in all
  three states. His running gags start here: he signs off "Smell you next tide!" (bent, never the original), he's
  never in danger (he guards the pie table through the quake), he's sure the story is his, and he has a "very
  talented" partner nobody has ever seen. His own look, never a copied one: the art slice's call.
- **The Mercury-blue puddle** (§9a, Golden Sun). Beside Stonehollow's well. A plain oddity now; from mission 3,
  Maren's Frost bounces off it.

## Not in this mission

These rows sit in the same rooms but belong to later scripts, which keep their slots: in `stonehollow`, Ilse's
mission 3 scene (slot 16, `to_canalport`), the Rimborn refugee and child (slots 18–19, mission 9), Corvin's rows
(slots 20–21) and the hero's crew row (slot 22) for mission 10, and the `refugees_settle` scene; in `vault_halls`,
Corvin (slot 12), the warded stair (slot 13) and the inner door's mission 10 branches.

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **The hero's house:** its rooms and contents, Brann's note, the porridge, the books, the speckled egg (a seed for
  a later hatching), the window on the Vault road.
- **The hero's days:** an apprentice who works the island's quarries by day, hence the dust and the late nap.
- **The west road's rockslide,** the in-world reason for progression decision 4's closed west gate.
- **Keeping Night's customs:** lanterns at dusk, the rite at moonrise, the Keeping Stone with its six marks and the
  words "What was sealed, we keep. What we keep, keeps us." An apprentice gets their partner on their Keeping Night.
- **Stonehollow's people:** Ada the lamplighter, Dunstan the quarry foreman, Old Moss, Maudie and The Quiet Stone,
  Nell at the stall (she wants to be a keeper), Corla the fisher, Tobin and his Sleeper lantern, Tully the Kestrel's
  mate, Ilse's marine, Brann's old Sudowoodo.
- **"The Sleeper":** Stonehollow's name for whatever sleeps under the Vault (Groudon), never named in mission 1.
- **The Tern:** the fishing boat Corvin was lost with five years ago, its skipper Ebb and its hand Orrin, and the
  memorial stone; Brann scratching Corvin's name off it. Corvin crewing the Tern as a young deckhand; his family
  stays offstage.
- **Brann:** his look, his knees, "Hold it till it wakes", the Lodestar as a keepers' heirloom handed down since
  before his grandmother's time, and "Farer" as a word nobody can explain any more (a seed for mission 19 that says
  nothing of who the Farers were or of the Crown); Corvin hatching Brann's eggs in his boots; "Deputy or no, you
  come home for supper".
- **Ilse:** her look; in port for the festival as the order's guest; her marines searching the north shore caves
  (mission 2 hears them); seeing the Vault's light from the north gate.
- **Corvin's actions:** he forced the Vault's doors himself on the festival night ("I knocked. The Vault knocked
  back"), which is the quake; he fights hoping two Earth Adepts' Psynergy at the seal will force the door, which is
  what stirs the Sleeper; his mask, a Keeping Night mask Brann carved for him as a boy, left behind and handed back
  to Brann (so Brann names him even when a quiet hero says nothing); his line "come and find me. I'll tell you
  everything".
- **The Vault:** the bronze seal-bar, the entrance plaque, the mural of six faceless robed figures, the inner door's
  two handprints, the crack along the east wall that becomes his escape.
- **The puzzles:** the split floor, the keepers' lock and the dig, with their rewards (Nut ×1, Herb ×2).
- **Placing Corvin's "Ask your Commodore where the tithe goes"** in mission 6 only, as story.md has it: mission 1's
  placeholder used the line early, and this script drops it here.

## Changes to the build

**Rooms**
- **`hero_house`** (new, decision 34): the hero's room and Brann's beyond it, with the mirror, the bed as the home
  bunk, the note, the shelf, the stove, the egg basket and the window. A door warp to and from `stonehollow`, next
  to the Rivalsons' door.
- **A new game starts in `hero_house`** after the opening and the creator, at dusk, instead of in `stonehollow`.
- **`vault_halls`** re-clipped from a larger part of Sol Sanctum (Golden Sun room 12) to hold, south to north: the
  entrance with the seal-bar, the Sentinel gallery with the mural and the dig spot, the split floor, the lock
  antechamber with its gate, statues, sockets and chest nook, and the inner door chamber with the crack along its
  east wall. Mission 10's door rows keep their slots.

**Actors and rows**
- `stonehollow`: new rows for Nell (with the stall's shop, slice 4), Gary, Corla, Tobin, the marine, Brann's
  Sudowoodo, the three pens, Ilse at the festival and at the gate, and the signs (village sign, Keeping Stone,
  notice board, memorial stone, hatchery and inn signs, the Rivalsons' door, the puzzle). Names on today's rows:
  slot 9 Maudie, 10 Dunstan, 11 Old Moss, 15 Ada, 17 Tully.
- **Text by state:** most people have three states. Either one row per state with `condition`s, or a row field that
  picks its text by flag (a list of `{flag, text}`, the last match winning). The second keeps slots stable and is
  recommended.
- **Ilse's slot 14** loses its quest role and the Lodestar (item 9003): scene 7 does her part, and the row hides
  from `m1_done` (crew 2 takes over at once, so an idle line there would never be seen). The handover
  narration and `crew 2` move from her `scene_after` into scene 7.
- **The masked figure's name tag:** scene 5's first pages show the tag "Masked figure" and no portrait (decision
  24's portraits would give Corvin away); his portrait appears with the unmasking.
- **The hatchery** becomes a scene: Brann's lines, the choice, the per-pick lines and system lines from the room's
  events (today the pick line is in code: "X is yours now"), the gifts, the quake, Ilse's run and `m1_quake`.
- **The opener** (`keeping_night`) loses its quake and its villager line: scene 2 replaces it.
- **The north warp's** `if_flag` becomes `m1_quake` (today `starter_chosen`), with the closed line above.
- **The west warp** gets its closed line and a story flag (progression decision 4).
- **The new game's bag** starts with no Poké Balls (today five, "until the story hands them out"): Brann gives
  them.
- **Corvin** (slot 8, `vault_halls`) plays scene 5 from a step-on trigger, swaps from sprite 34 to 35 mid-scene,
  and says a retry line when "Try again" restarts the fight; scene 6 replaces his `scene_after` and `text_after`.
- **The east crack** opens to the river (a gate repainting cells) in scene 6, and stays open.
- **The puddle** reacts to Frost with its line and no change (a Frost event with text only).
- **The inn role** shows its `text` before the rest menu, and a line after resting.

**New scene steps** (README §2): `phase`, `light` (a tint and a pulse), `camera` (pan and back), `pose` (sit up,
lean on the door, and the quiet hero's nod and head shake), `choice` (reply beats with the quiet labels, from the
creator's Voice setting), `sprite` (swap mid-scene), a step-on trigger, and the partner follower and Larvitar as
actors scenes can move.

**Checks.** `tools/mission1_check` follows the new flow (the house, the opener, the hatchery's gifts and quake, the
three puzzles, the fight and its retry line, the split, dawn, the handover) and the reply menus in both voices.
