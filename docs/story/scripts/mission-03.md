# Mission 3: Highwater

> **Status:** draft for your yes or notes (18 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 3. Today's build: [mission-3-build.md](../../design/mission-3-build.md).

| | |
|---|---|
| Mission | 3, Highwater (prologue) |
| Plays after | Mission 2's last scene, which resumes crew 1 in Stonehollow at dawn ([mission-02.md](mission-02.md), scene 12) |
| Crew | {HERO} and the first partner; Maren and Eevee join in scene 1; Marill joins in scene 4 |
| Rooms | `stonehollow`, `canalport` (the harbour front: today's beach room), `canalport_canals` (new: the lower town's canals and the sea sluice, decision 5) |
| Clock | Dawn in Stonehollow; day on arrival in Canalport; dusk in the canals; night from the sluice on |
| Flags in | `m2_done` |
| Flags out | `m3_started`, `m3_intro`, `m3_breach_west`, `m3_breach_east`, `m3_beach`, `m3_glint`, `m3_surf`, `hm_surf`, `m3_canals_in`, `m3_barnaby`, `m3_bridge`, `m3_dug`, `m3_weir_1`, `m3_weir_2`, `m3_weir_3`, `m3_beast`, `m3_done`, `has_ship`, `m3_truck`, `m4_started` |
| Unlocks | Maren (Sea, with Eevee) joins, and with her Frost; Marill, Harbourmaster Quayle's gift (decisions 14 and 15), and so Surf (`hm_surf`); the Kestrel (`has_ship`): the Calm opens on the Kestrel's chart |
| Reply beats | 2: Maren's posting (scene 1); Maren's question on the jetty (scene 10) |
| Fights | The sluice beast (`sluice_beast`, as built: Kraken's sheet at L8). A loss plays "Try again" |
| Leads into | Mission 4: Corvin's crew at the Forgeheart ([mission-04.md](mission-04.md)) |

**The flow.** A few days after Keeping Night, Ilse has a Wingull letter: Canalport is flooding and its sea sluice
has jammed with something living in it. She posts Maren, a Tidewarden medic and Sea Adept, to {HERO}, lends them
the Kestrel ("If Canalport stands, keep her") and sails south with the tithe fleet. In Canalport, Maren's Frost
plugs the two breaches in the beach dike, and Harbourmaster Quayle gives {HERO} a Marill from his ferry pod, so
{HERO} can Surf. The crew swims the drowned lower town: a swing bridge to open, a bargeman to patch up, a weir to
cross on ice. At the sluice the beast isn't guarding anything: the spring tide pushed it up the channel and it
wedged itself in the gates, which is what jammed them. Beaten, it slips free, the gates swing open and the town
drains out to sea. The Kestrel is theirs. On the jetty that night, Maren asks about Corvin, then sends her report
by Wingull, west toward the Pinnacle, while Ilse sails south.

## Scenes

### 1. Ilse's posting

- Room: `stonehollow`. Trigger: talking to Ilse (slot 16, at the north gate), once `m2_done`, unless
  `m3_started` (today's `to_canalport` scene, rewritten).

*Dawn. Ilse stands by the north gate with a rolled letter in one hand, her marine behind her. Beside her waits a
young woman in a Tidewarden medic's coat, white with blue cuffs, a satchel on one shoulder and a notebook in her
breast pocket. An Eevee sits at her heel, washing a paw.*

*[face Ilse → {HERO}]*

**Ilse:** {HERO}. Good. A Wingull came in
at first light, from Brightcoast.

Canalport is flooding. The spring
tide broke the beach dike in two
places, and it's still rising.

And the sea sluice that drains the
lower town has jammed shut. The
harbourmaster says it's not empty.

Something is living in it.

The Kestrel sails for Canalport
within the hour. Tully has her
ready.

You won't go alone. This is Maren,
of the order's medical corps. She's
a Sea Adept.

*[walk Maren → beside {HERO}] [face Maren → {HERO}] [emote Eevee: smile]*

**Maren:** Deputy {HERO}. The Commodore has
posted me to you.

I'm to keep you in one piece. Try
not to make it hard.

**{HERO} replies:**

1. "Glad of the help." · quiet: (Nod)

   **Maren:** Good. Most deputies argue. It
   wastes time I could spend on
   bandages.

2. "I can manage alone." · quiet: (Shake head)

   **Maren:** You have a split knuckle, a
   bruised jaw and quarry grit in a
   graze. That was managing alone.

3. "Why you?" · quiet: ...

   **Maren:** I asked for this posting. The
   Commodore said yes before I'd
   finished asking.

   **Ilse:** She did. First to volunteer, and
   the best Frost in the cutter fleet.

*Every reply rejoins here.*

*[recruit maren] Maren and Eevee join the crew.*

**System:** Maren joined the crew!

**Ilse:** Maren's Frost should hold the
breaches. Your Earth is for the
rest of it.

I can't come. The tithe fleet sails
south today, and I sail with it, on
the Holdfast.

The turn of the season. The order
collects, island by island. Embral
first.

*[face Ilse → the cove]*

**Ilse:** One more thing. The Kestrel is
mine, and I'm lending her.

If Canalport stands at the end of
it, keep her. A deputy needs a
ship.

*[emote {HERO}: exclaim]*

**Ilse:** Don't thank me. Earn her.

*Brann comes up the lane from the hatchery at his slow pace, with a cloth bundle in both hands. [walk Brann →
beside {HERO}]*

**Brann:** Off to sea, apprentice? Here.
Maudie's pie. Don't argue.

*He looks Maren up and down.*

**Brann:** A medic. Good. Mind you don't
bleed in front of her. She looks
the sort to take notes.

**Maren:** I do take notes, Keeper. It's
a habit.

**Brann:** Hm. Keep my apprentice fed, and
you can write what you like.

*[walk Ilse and the marine → the cove] [hide Ilse] [hide the marine] [fade out 40]*

**Narration:** The Kestrel carried them south
across the Calm, two days and two
nights, to the coast of Meridia.

Then up the brown channels of
Saltmarsh Reach, where the reeds
stood higher than the mast.

*[flag m3_started] [phase day] [warp canalport, entrance 0]*

### 2. Highwater

- Room: `canalport`. Trigger: entering, unless `m3_intro` (today's `harbour` scene, rewritten).

*[fade in 40] Canalport's harbour front: a stone jetty, a long quay, and a beach of grey sand behind a dike of
earth and timber. Beyond it the lower town stands in its canals, tall narrow houses with blue shutters and a
hundred bridges, and the upper town on the bluff above. Today the sea is pouring across the beach through two
breaches beside the tide pools, in a brown band between the jetty and the town. Marines stack sandbags. Townsfolk
carry chairs up the quay. On a crate by the Tidewarden post, a stout man in an ink-stained coat waves a tide book
and shouts.*

**Quayle:** Highwater at four bells! Four
bells! Everything off the ground
floor!

*[crew out] Maren steps out of the lead to stand beside {HERO}, Eevee at her heel. [walk Tully → the jetty's
end]*

**Tully:** Canalport, Deputy. I'll keep the
Kestrel off the jetty till the tide
turns. It's not turning.

*[camera → the breaches] [camera back]*

**Maren:** Two breaches, there and there,
by the tide pools. The sea is
coming in under the dike.

If I Frost the pools, the ice
should plug them from below. Like
a cork in a bottle.

Then the beach drains, and we can
reach the Tidewarden post.

**{HERO}:** Then let's get to work.

*Quiet: [pose {HERO}: nod] and no line.*

*[crew in] [flag m3_intro] Control returns.*

### 3. The beach drains

- Room: `canalport`. Trigger: the second breach frozen (both `m3_breach_west` and `m3_breach_east`, the gate's
  flags), unless `m3_beach`.

*The second pool freezes with a crack like a whip. A pillar of ice stands in the breach. [shake 20, 1] The water
stops. Along the beach the brown band drains away into the sand. [gate: the flood band becomes sand, as built]
Somebody on the quay cheers, then everybody does.*

*Quayle jumps down off his crate and comes at a run, tide book under his arm. [walk Quayle → beside {HERO}]*

**Quayle:** It's stopped! Highwater due at
four bells, and stopped at three!
Ha!

You're the Tidewardens? Come to the
post. I've a sluice that needs
somebody braver than me.

*[walk Quayle → the Tidewarden post] [flag m3_beach] Control returns.*

### 4. The harbourmaster's gift

- Room: `canalport`, the Tidewarden post. Trigger: talking to Quayle (slot 10, cell (12,24)), once `m3_beach`,
  unless `m3_surf` (the quest role, rewritten).

*The Tidewarden post: a stone office on the quay, its door open, tide tables chalked on a board outside. Below
the quay wall is a pen of floating timbers, where a pod of Marill bob in the water, round and blue, towing a
little ferry in circles.*

**Quayle:** Harbourmaster Quayle. Tides,
berths, ferries and Marill. Mostly
Marill.

Here's my trouble. The sea sluice
lets the lower town drain out at
every ebb.

Two nights ago, on the spring tide,
something came up the channel and
jammed its gates shut.

It's still in there. It groans. It
has arms.

**Maren:** Arms?

**Quayle:** Lots of arms. My ferryman saw one
come up out of the channel and take
his hat.

With the sluice shut, the canals
can't drain. They're over the quays
now. Nobody can walk down there.

You'll have to swim it.

*Quayle whistles through his fingers. A Marill paddles out of the pen, climbs the steps and bounces to
{HERO}'s feet. [emote Marill: heart]*

**Quayle:** Take this one. Canal-born, strong
in the water. It's towed my ferry
two summers.

It'll carry you over any calm
water. Face the water and ask it
nicely.

*[give_pokemon Marill, L6] [flag hm_surf] Marill goes into a Set with room (Changes to the build, below).*

**System:** {HERO} received Marill!

**System:** Now you can Surf! Face calm water
and press A to ride on Marill.

**Quayle:** The canal mouth is past the post,
by the lock stair. Follow the Grand
Cut north to the sluice.

And bring me back my sluice. And the
ferryman's hat, if you see it.

*[flag m3_surf] Control returns.*

### 5. The drowned town

- Room: `canalport_canals`. Trigger: entering, unless `m3_canals_in`.

*[phase dusk] [fade in 30] The lower town at dusk. The canals have risen over their quays, and tall houses
stand in brown water to their sills. Boats are tied to upstairs windows. Washing lines sag across the water. The
Grand Cut runs north between the houses toward the sea wall, where the sluice house stands dark against the sky.*

*A long, low groan rolls down the canal. The water shivers. [shake 20, 1] [emote Marill: sweat]*

**Maren:** That's the sluice house. With
its gates shut, the river has
nowhere to go but up.

By tonight this water will be
another foot higher. We'd best be
quick, {HERO}.

*[flag m3_canals_in] Control returns.*

### 6. Barnaby

- Room: `canalport_canals`, a moored barge on the Grand Cut. Trigger: talking to Barnaby, unless `m3_barnaby`.

*A broad bargeman with a wet beard and one boot sits on the roof of a barge, his leg out straight in front of
him.*

**Barnaby:** Oi! Up here! You're not a fish,
are you? No. Good.

I came down to see to my barge and
turned my ankle on the deck. Been
up here since noon.

*[crew out] [walk Maren → the barge] [pose Maren: kneel] She looks at the ankle, then casts Ply over it. [light:
a soft blue glow on the ankle]*

**Maren:** Sprained, not broken. Hold still.
This will feel cold.

**Barnaby:** Ooh! Cold! Cold! ...Oh. That's
much better.

**Maren:** Stay off it for a week. I'll know
if you don't.

**Barnaby:** Lettie sent you? My girl, up at
the harbour? Tell her I'm whole.

That thing in the sluice. I saw it.
Arms like mooring ropes, and eyes
like two lanterns.

It's not guarding anything, mind.
It's thrashing. Like a dog with its
head stuck in a fence.

If you're going up the Cut, the
Tanners' Swing is down. You'll not
get under it.

Flood knocked its weight off the
plinth. Shove the weight back, and
she'll swing open sweet as you like.

*[pose Maren: stand] [crew in] [flag m3_barnaby] Control returns.*

### 7. The sluice beast

- Room: `canalport_canals`, the sluice landing. Trigger: stepping onto the landing (a step-on spot), unless
  `m3_beast`. The fight is the beast's row (slot 13, moved here from `canalport`).

*The sluice house: a squat stone house on the sea wall, and below it two great timber gates shut across the
channel. Something huge is wedged between them, grey-green and glistening, its long arms wound round the gate
posts. Two eyes as big as lanterns open in the water. [emote {HERO}: exclaim] [shake 40, 2] The beast heaves up
out of the channel with a roar that rattles the shutters.*

*[crew out]*

**Maren:** There's our sluice.

Look at its arms, {HERO}. They
are caught round the gate posts.
It's stuck fast.

It can't get out, and it's furious
about it. Mind its arms.

*[crew in] [battle sluice_beast]*

*If the fight is lost, "Try again" plays and the fight restarts as it began (as built). Maren's line as it
restarts:*

**Maren:** Again. Heal first this time,
{HERO}. Hit it second.

### 8. The gates open

- Room: `canalport_canals`. Trigger: winning the fight (the beast's `scene_after`, rewritten).

*The beast slumps against the gates. One by one its arms slip off the gate posts. [shake 50, 2] The gates groan
and swing outward, and the whole canal starts to run toward the sea.*

*The beast is carried with it, out through the gates on the ebb. Beyond the sea wall one grey arm rises above
the waves, waves once, and sinks. [hide the beast]*

*[crew out] [emote Maren: silence]*

**Maren:** It wasn't guarding the sluice. It
was stuck in it.

The spring tide pushed it up the
channel. It wedged itself in the
gates, and jammed them shut.

Two nights stuck in a door, with
everyone shouting at it. I'd have
been cross too.

*[phase night] All down the canals the water drops. Quays come up out of the flood, streaming. Doors drip on
their hinges. Lamps come on in upstairs windows, and somewhere, far off, a cheer. [gate: the drowned quays become
stone, and the quay stair opens]*

*[crew in] [flag m3_beast] [flag m3_done] Control returns. The quay stair leads back up to the harbour on foot.*

### 9. The Kestrel

- Room: `canalport`. Trigger: entering from the canals, once `m3_done`, unless `has_ship`.

*Night on the harbour front. Lanterns along the quay. The beach is dry and the tide far out. Townsfolk carry
their chairs back down. Lettie sits on a bollard beside Barnaby, who has a crutch and a borrowed boot. Quayle
waits at the post with his tide book open. [walk Quayle → beside {HERO}]*

**Quayle:** You did it! The lower town is
draining like a bath. I've written
it in the tide book. In ink!

The harbour's thanks. It isn't much.
It's what the tide fund had.

*[give coins 100]*

**System:** {HERO} received 100 coins!

*[walk Tully → beside {HERO}]*

**Tully:** Deputy. The Commodore's orders,
word for word: "If Canalport
stands, keep her."

Canalport's standing. She's yours.
I'm the mate who comes with her.

*[flag has_ship] [emote {HERO}: exclaim]*

**System:** The Kestrel is {HERO}'s!
The Calm is open.

**Tully:** Talk to me on the jetty when you
want to sail. I'll have the chart
out.

### 10. The jetty

- Room: `canalport`, the end of the jetty. Trigger: straight on from scene 9.

*[fade out 30] [fade in 30] Later. The end of the jetty, under the stars. The Kestrel creaks at her moorings.
Maren sits on a bollard, writing in her notebook by a lantern, with Eevee asleep on her boots. {HERO} sits
beside her. [crew out]*

**Maren:** I'm writing the day up. The order
runs on reports.

One thing the report still needs.
The seal-breaker. Corvin.

The Commodore says you grew up with
him. If it comes to it, can you
bring him in, {HERO}?

**{HERO} replies:**

1. "I'll bring him in." · quiet: (Nod)

   **Maren:** Good. That's what I'll write.

   You took a breath first. I won't
   write that part.

2. "I don't know yet." · quiet: (Shake head)

   **Maren:** Then I'll write that the deputy
   is honest. It's true, and it's
   short.

3. "What will you write?" · quiet: ...

   **Maren:** I'll write the truth. I always
   do. That you're tired, and brave,
   and you haven't eaten since noon.

   Eat the pie, {HERO}. Keeper's
   orders.

*Every reply rejoins here.*

*Maren tears the page out, rolls it into a tube and whistles. A Wingull drops out of the dark onto the next
bollard. She ties the tube to its leg.*

**Maren:** Medical returns. The order
wants them every week. Very dull.

*The Wingull flies off west over the roofs, inland, toward the Pinnacle, not south after Ilse's fleet. Nobody says
so. [walk Wingull → off west] [hide Wingull] [emote Eevee: question]*

**Maren:** Get some sleep, Deputy. The
Kestrel sails when you say.

*[crew in] [fade out 40]*

**Narration:** That same night, far to the
south, a Rimborn skiff came in
under the smoke of Embral.

*[crew 2] [flag m4_started] [warp forge_hall, entrance 0] Mission 4 begins ([mission-04.md](mission-04.md)).
Crew 1 is recorded where it stood, on the jetty, and resumes there in mission 4's last scene.*

## People and signs, by room

### `stonehollow`

This page takes Stonehollow over from mission 1's "after the Vault" state. *The states:* before the voyage
(`m2_done`, until `m3_started`); Act I (`m3_done`, until a later page takes over), for a return by the Kestrel.
Between the two the crew is away, so nobody needs a line. Cells are mission 1's.

- **Keeper Brann**, slot 8, cell (3,9). Before the voyage:

  **Brann:** Ilse's been at the north gate
  since dawn, with a letter and a
  face like weather. Go on.

  *Act I:*

  **Brann:** Back, apprentice? Eat something.
  Then tell me everything. Slowly.
  I'm old.

- **Brann's Sudowoodo.** Before the voyage:

  **Sign:** The Sudowoodo has moved one step
  closer to the cottage door. Nobody
  saw it move.

  *Act I:*

  **Sign:** The Sudowoodo is pretending to
  be a tree. It's getting very good
  at it.

- **Nell**, at the hatchery stall. Her shop lines are mission 1's. Before the voyage:

  **Nell:** Brann says you're sailing. Take
  Herbs. Take more Herbs than that.

  *Act I:*

  **Nell:** Back from the mainland? Tell me
  all about it. After you buy Herbs.

- **Commodore Ilse**, slot 16: scene 1 only. She sails with the tithe fleet, so the row hides from
  `m3_started`, and **her marine** with her. The marine, before the voyage:

  **Marine:** The Commodore's been up since the
  Wingull came. When she's up, we're
  all up.

- **Ada**, slot 15. Before the voyage:

  **Ada:** I'm relighting the lanterns the
  shake put out. Ninety-one so far.
  It's a slow sort of tidy.

  *Act I:*

  **Ada:** All two hundred lit again. Next
  Keeping Night they'll be brighter
  than ever. I've decided.

- **Dunstan**, slot 10. Before the voyage:

  **Dunstan:** Brann's halls are a mess. I've
  offered him a cart. He says the
  Vault doesn't take carts.

  *Act I:*

  **Dunstan:** We're shifting the west road
  rockslide a barrow at a time. Come
  back in about forty years.

- **Old Moss**, slot 11. Before the voyage:

  **Old Moss:** They say the Sleeper rolled over.
  At my age, I roll over too. Takes
  me a while.

  *Act I:*

  **Old Moss:** The crack in the Keeping Stone's
  no wider. I check it every morning.
  It's something to do.

- **Maudie**, slot 9: mission 1's lines, in every state.

- **Gary Rivalson.** Before the voyage:

  **Gary:** Off to the mainland? I'd go too,
  but the mainland isn't ready for
  me yet.

  Smell you next tide!

  *Act I:*

  **Gary:** A ship? They gave YOU a ship?
  They'd have given me two. I said
  no. Twice.

  Smell you next tide!

- **Corla.** Before the voyage:

  **Corla:** The cove's been quiet since the
  dark skiff. Too quiet, Ada says.
  Ada says a lot.

  *Act I:*

  **Corla:** Your own cutter now! Wait till
  the cove hears. I'm the cove. I've
  heard.

- **Tobin.** Before the voyage:

  **Tobin:** I'm being extra good. It's very
  tiring. How long does the Sleeper
  sleep for?

  *Act I:*

  **Tobin:** I gave my Sleeper lantern to
  Brann. He hung it in the hatchery.
  He says the eggs like it.

- **Tully**, slot 17, at the cove. Before the voyage:

  **Tully:** We sail the moment the Commodore
  has spoken to you, Deputy. She's at
  the north gate.

  *Act I:* the Kestrel's row, as in Canalport (below).

**Signs**

- Mission 1's "after the Vault" signs stay: the cracked Keeping Stone, the scratched memorial stone, the notice
  board, the hatchery and inn signs, the Rivalsons' door, the west gate.
- **The Mercury-blue puddle**, with Frost on it: mission 1's line, then Maren's (Maren is always in the crew from
  here, so her line follows the sign's):

  **Sign:** The puddle refuses to freeze. It
  looks rather pleased with itself.

  **Maren:** That isn't in any manual.

### `canalport`

*The states:* the flood (until `m3_beach`); the beach dry (`m3_beach`, until `m3_done`); after the sluice
(`m3_done`). The flood band cuts the jetty off from the town until `m3_beach`, so only the jetty's people speak
in the first state. Cells are on today's 34×30 clip; new people give a place instead.

- **Harbourmaster Quayle**, slot 10, cell (12,24), at the Tidewarden post. The flood: on his crate (scene 2),
  out of reach across the band. The beach dry: scene 4, then:

  **Quayle:** The lock stair's past the post. Up
  the Grand Cut to the sluice. The
  tide won't wait, and nor will I.

  *After the sluice:*

  **Quayle:** In ink, mind. Not pencil. Canalport
  has never had a day like it.

  And the ferryman's hat is up the
  Cut, hung on a gate post. Neatly!
  I've written that down too.

- **Lettie** (the canal girl, slots 11 and 14). The beach dry, until `m3_barnaby`, slot 11, cell (25,22):

  **Lettie:** Papa went down to see to his
  barge at noon. He's not back. He's
  always back for tea.

  *Once `m3_barnaby`, the same row:*

  **Lettie:** You found Papa? On his barge,
  being told off by a medic? That's
  him. That's my papa.

  *After the sluice, slot 14, on the bollard beside Barnaby:*

  **Lettie:** Papa's home! He's got a crutch,
  and he's very grumpy, and I'm so
  happy.

- **Barnaby** (new), after the sluice, beside Lettie:

  **Barnaby:** Your medic says a week off it.
  I say three days. She says she'll
  know.

  She'll know, won't she?

- **A Tidewarden marine** (new), by the sandbags on the beach. The flood:

  **Marine:** Sandbags, Deputy. We've laid two
  hundred. The sea has eaten two
  hundred.

  *The beach dry:*

  **Marine:** The breaches are holding! Ice.
  Who knew? The Frost Adept knew.

  *After the sluice:*

  **Marine:** Highwater's past. I'm going to
  sit down for a week.

- **Effie, the innkeeper**, slot 12, cell (14,26), at The Dry Boot (the inn role). Before the rest menu, the
  beach dry:

  **Effie:** The Dry Boot. Driest beds in
  Canalport, and today that's saying
  something.

  *After the sluice:*

  **Effie:** The whole lower town's dry! I
  was going to rename the inn. Now
  I don't have to.

  *After resting:*

  **Effie:** Slept well? The tide's been in
  and out twice. You missed nothing.

- **Odile, the chandler** (new), at her chandlery on the quay. She opens the Canalport item shop (Herb, Nut,
  Antidote, Elixir, Poké Ball, Escape Rope, Repel; Great Ball from `m6_done`: items-and-economy.md §8) after her
  line. The beach dry:

  **Odile:** Herbs, rope, Poké Balls, and all
  the things sailors forget. Mind the
  puddles.

  *After the sluice:*

  **Odile:** Everything a sailor forgets.
  You'd be amazed what sailors
  forget.

  *Not enough coins, in the shop:*

  **Odile:** That's more than your purse holds.
  The sea's never been kind to
  purses.

  *Leaving the shop:*

  **Odile:** Fair winds.

- **Ivo, the armourer** (new), at the armoury next to the chandlery. He opens the Canalport gear shop (tier 1
  weapons and armour, Wooden Stick 40 to Battle Axe 280, Cotton Shirt to Open Helm 180) after his line. In
  every state from the beach dry:

  **Ivo:** Blades, shirts, shields. Nothing
  rusts in my shop. Everything rusts
  in this town.

  *Not enough coins, in the shop:*

  **Ivo:** Come back with more coin. I'll
  keep it dry for you.

  *Leaving the shop:*

  **Ivo:** Keep your edge dry.

- **Hobb, a docker** (new), on the jetty beside the truck. In every state, until `m3_truck`:

  **Hobb:** That iron wagon's been on this
  quay since my gran's gran. The
  truck, we call it. Don't know why.

  My gran swore she saw a little pink
  something under it once. It looked
  at her and laughed.

  Nobody's ever shifted it. Too heavy
  for anyone without a bit of
  Psynergy.

  *Once `m3_truck`:*

  **Hobb:** You shifted the truck! Anything
  under it? ...A note. Course there
  was. Gran would have loved that.

- **Mother Brindle** (new), at an eel-pie stall on the jetty. The flood and the beach dry:

  **Brindle:** Eel pies! Hot eel pies, flood or
  no flood!

  That rubbery fellow in the hat has
  eaten eleven. He's paid for two.

  *After the sluice:*

  **Brindle:** Pies for the heroes of the sluice!
  Half price. No, full price. I've a
  family.

- **Captain Rufio Maize** (new, the egg), sitting on a bollard at the jetty's root with a pie in each hand. The
  flood and the beach dry:

  **Maize:** Hey! You! Is this whole city
  half under the sea? It is? That's
  amazing!

  Best adventure ever!

  I'm Captain Rufio Maize. I'm going
  to be King of the Open Sea!

  Want to join my crew?

  *[yes/no] (the mirror's yes/no; no flag)*

  - Yes:

    **Maize:** Great! Oh. Wait. You've already
    got a crew. That's fine! Then we'll
    be friends instead.

  - No:

    **Maize:** That's fine! Everybody says no
    the first time. And the second.

  *Then, either way:*

  **Maize:** Hey. You smell like pie. Marrow
  Isle pie. I'd know that crust
  anywhere.

  *[shake 10, 1] A rumble rolls down the jetty. It's Maize's stomach. He looks at the two pies in his hands as if
  they've let him down. [emote Maize: sweat]*

  **Maize:** ...Got any more?

  *After the sluice:*

  **Maize:** You beat a sea monster? Without
  me? Next time, call me!

  I'd have eaten it. Probably. Its
  arms looked chewy.

  Want to join my crew?

  *[yes/no], with the same two answers as above.*

- **Tully, the Kestrel's mate**, slot 15, cell (20,14), at the jetty (the voyage role). Before `has_ship`:

  **Tully:** Commodore's orders. The Kestrel
  waits here till Canalport's safe.
  It isn't safe.

  *From `has_ship`, here and in every room where the Kestrel moors (Stonehollow's slot 17 and the later
  missions' mates): the chart, then the bunk (decision 34):*

  **Tully:** Where to, Deputy? Or a bunk
  below, if you're dead on your
  feet.

  *[menu: the chart's places, Bunk, Not now] Bunk:*

  **Bunk:** A narrow bunk below decks. It
  smells of tar. Sleep until...?

  *[menu: Dusk, Dawn, Not now]*

**Signs and things to examine**

- **The town sign**, at the jetty's root:

  **Sign:** CANALPORT. City of a Hundred
  Bridges. Please keep to the quays.

- **The tide pools**, slots 8 and 9, cells (13,19) and (27,19) (puzzle 1). Before Frost:

  **Sign:** The sea bubbles up through a
  breach under the dike. Frost might
  plug it.

  *After Frost:*

  **Sign:** A pillar of ice stands in the
  breach, sealing it from below.

- **The tide board**, outside the Tidewarden post:

  **Sign:** HIGHWATER: FOUR BELLS.
  LOW WATER: NOT TODAY.
  Chalked under it in a neat hand:

  SLUICE STUCK. SOMETHING IN IT.
  HAS ARMS. Q.

- **The Tidewarden notice**, by the post:

  **Sign:** BY ORDER OF THE PINNACLE: the
  element tithe falls due at the turn
  of the season.

  Canalport pays in rain. Barrels to
  the post by the new moon.

- **The Marill pen**, below the post. Until `m3_surf`:

  **Sign:** Canalport's ferry Marill, bobbing
  in their pen. One of them waves.

  *From `m3_surf`:*

  **Sign:** The Marill pod watches your Marill
  go by. They look very proud.

- **The Merry Wooloo** (new), Maize's sloop, moored off the jetty:

  **Sign:** A little sloop with a woolly
  figurehead. Its name is painted on
  the bow: THE MERRY WOOLOO.

  There are teeth marks on the rail.

- **The truck** (new, the egg), on the jetty beside Hobb. Until `m3_truck`:

  **Sign:** An iron wagon with no shafts and
  no horse, rusted to the quay. It
  would budge, with a push.

  *Move pushes it one cell (`m3_truck`). Where it stood, a square of clean stone, and a scrap of paper:*

  **Note:** A child's drawing of a small pink
  cat with a long tail. Under it, in
  pencil:

  Seen here once. It will come back
  when every Pokémon in the world is
  written down.

  *After `m3_truck`:*

  **Sign:** The truck, one step from where it
  stood for a hundred years. It looks
  embarrassed.

- **The lock stair**, at the canal mouth past the post. Until `m3_surf`:

  **Sign:** Steps down to the Grand Cut. The
  water is over the bottom six. You'd
  have to swim.

- **The south road** (today's south warp, its closed line). Until `m3_done`:

  **Sign:** The road inland runs through the
  lower town. The lower town is
  under water. The sluice first.

  *After `m3_done`, behind progression decision 4's flag until our world map opens it:*

  **Sign:** The road inland is closed. The
  Tidewardens are walking the dikes,
  one by one.

- **The beach glint** (new), on the drained sand, from `m3_beach` until `m3_glint` (Scoop sets it):

  **Sign:** Something glints in the wet sand
  where the flood ran. Scoop would
  dig it out.

### `canalport_canals` (new)

*The states:* drowned (until `m3_done`); drained (`m3_done`). No random battles: the canals are a town, and the
beast is the fight.

- **Barnaby**, on his barge on the Grand Cut. Scene 6, then until `m3_done`:

  **Barnaby:** I'll sit here till the water drops.
  Then I'll limp home. Then I'll
  complain about it.

  *Drained:* he has gone home (`canalport`, beside Lettie).

- **Mrs Pennock** (new), at an upstairs window over the Grand Cut. Drowned:

  **Pennock:** We're fine! We're upstairs! We've
  got the cat, and the bread, and
  Grandad!

  Grandad says he's seen worse. He
  hasn't. He's just like that.

  *Drained:*

  **Pennock:** We can see the street again! It's
  covered in fish. Grandad says he's
  seen worse.

**Signs and things to examine**

- **The canal sign**, at the mouth:

  **Sign:** THE GRAND CUT. To the sea sluice.
  No mooring. No swimming. Today,
  only swimming.

- **The Tanners' Swing** (puzzle 2), until `m3_bridge`:

  **Sign:** A bridge on a pivot lies across
  the Cut. The flood is up to its
  deck. No way under.

  *After `m3_bridge`:*

  **Sign:** The Tanners' Swing stands open,
  turned along the quay. The Cut runs
  free beneath it.

- **The counterweight** (puzzle 2):

  **Sign:** A great stone counterweight,
  knocked off its plinth. It would
  slide, with a push.

- **The plinth** (puzzle 2), until `m3_bridge`:

  **Sign:** An empty plinth, cut square.
  Something heavy sat here once.

- **The mudbank** (the optional dig), in the side canal, until `m3_dug`:

  **Sign:** Flood mud, banked against a water
  door. Something glints in it. Scoop
  would dig it out.

- **The Long Weir** (puzzle 3):

  **Sign:** The Long Weir. The flood pours
  over it in a white rush. Too rough
  to Surf.

- **The weir puddles**, three, until each is frozen:

  **Sign:** A puddle sits in a worn hollow
  on the weir's lip.

  *Frozen:*

  **Sign:** A pillar of ice, its top level
  with the weir's lip. It looks like
  it would take your weight.

- **The sluice house door:**

  **Sign:** THE SEA SLUICE. Keeps the sea
  out at high water. Lets the town
  out at low.

- **The gate post**, after `m3_beast`:

  **Sign:** A ferryman's hat, hung on a gate
  post. Something has hung it there
  quite neatly.

- **The open gates**, drained:

  **Sign:** The sluice gates stand open on the
  ebb. The canals run quietly out to
  sea.

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| Maudie's pie | Scene 1, from Brann | Nothing: a prop (Maize smells it, Maren mentions it) | — |
| Quayle's gift | Scene 4 | Marill, L6, into the crew's Set | Scene 4's system lines |
| The beach glint | `canalport`, the drained sand (Scoop, from `m3_beach`; sets `m3_glint`) | Nut ×1 | **System:** {LEADER} found Nut! (the engine's line) |
| The Tanners' chest | `canalport_canals`, on the Tanners' quay beside the counterweight | Elixir ×2 | The engine's chest line, naming `{LEADER}` |
| The mudbank | `canalport_canals`, the side canal (Scoop, optional) | Great Ball ×2 | **System:** {LEADER} found Great Ball x2! |
| The sluice house | `canalport_canals`, inside the sluice house, from `m3_beast` (the dungeon's gear chest, items §13) | Leather Cap (the hero and Maren already wear Padded Gloves, the roster kit, and neither has a helm) | The engine's chest line |
| The tide fund | Scene 9, from Quayle | 100 coins | Scene 9's system line |
| The truck's note | `canalport`, under the truck | Nothing: a note to read | The Note, above |

**Marill's Kin text** is the Log's, at mission 10 (open question 5); nothing is written for it here.

## Puzzles

The crew's verbs here: {HERO}'s Move and Scoop, Maren's Frost (Sea), and Surf once Marill joins (a kept HM, free).
Cut waits for mission 5. One puzzle on the harbour front and two in the canals, with an optional dig, all on the
main path but the dig. As in missions 1 and 2, pushed things stay where they're pushed (slice 4), so every block
can always be got behind again.

**Puzzle 1. The breaches (Frost, as built).**
1. The flood band cuts the jetty off from the town. Two tide pools on the band bubble with seawater: the breaches
   under the dike.
2. Cast Frost on each pool: it freezes into an ice pillar that plugs its breach (`m3_breach_west`,
   `m3_breach_east`).
3. With both plugged, the band drains to sand (the gate, as built) and scene 3 plays.

It teaches Frost: ice where there was water.

**Puzzle 2. The Tanners' Swing (Move and Surf, new).**
1. Up the Grand Cut, a swing bridge lies across the canal. The flood has lifted the water to its deck, so Surf
   can't pass under it.
2. On the quay beside it, a landing step lets {HERO} climb off Marill. The bridge's counterweight lies on the
   quay, two cells east and one north of its plinth.
3. Push it west twice and south once, in any order that works, so the player walks round it. The quay is open on
   every side of those cells, so it can always be got behind again.
4. On the plinth (`m3_bridge`), the weight drops with a thud and the bridge swings round along the quay (a gate
   turning the bridge's cells to water on the surf layer, and the bridge's tiles onto the quay). Back on Marill,
   the Cut is open. The Tanners' chest sits on the same quay.

Barnaby's lines (scene 6) give the answer to anyone who talked to him.

**Puzzle 3. The Long Weir (Frost three times, new).**
1. The Grand Cut ends at the Long Weir: the flood pours over its lip in a white rush, too rough to Surf. The
   sluice house landing is on the far side.
2. Three puddles sit in worn hollows along the lip, in a line from the west quay to the landing, each one cell
   from the last.
3. From the quay, cast Frost on the first: it becomes a pillar level with the lip, which can be walked on
   (`m3_weir_1`, a gate opening that cell). Step onto it and Frost the second (`m3_weir_2`), then the third
   (`m3_weir_3`). The last step lands on the sluice landing, and scene 7 plays.
4. Each puddle can only be reached from the pillar before it, so the order takes care of itself.

It teaches that Frost makes a way, not only a plug.

**Optional. The mudbank (Scoop, new).**
1. In a side canal off the Cut, flood mud has banked against a house's water door, with a glint in it.
2. Climb off Marill onto the doorstep and cast Scoop: {HERO} digs out two Great Balls (`m3_dug`).

## Eggs

- **Captain Rufio Maize** (story.md §9a, One Piece's captain), on the Canalport jetty in every state. His running
  gags start here: always hungry (eleven eel pies, two paid for, and he can smell Brann's pie on the hero), every
  island is "the best adventure ever", he's going to be "King of the Open Sea", and he asks everyone to join his
  crew. His sloop is the Merry Wooloo, a bent nod to his original's ship and its sheep figurehead. His own look,
  never a copied one: a battered sun hat and arms a little too long. The stretch itself isn't shown; Brindle's
  "that rubbery fellow" carries it. His talk is a short staged scene (decision 10): the join-my-crew menu, then a
  stomach rumble that shakes the jetty.
- **The push-the-truck rumour** (§9a, Pokémon). The truck is an iron wagon nobody can explain, rusted to the
  jetty. Hobb's gran's "little pink something" is the rumour; Move shifts it one cell to find a child's drawing
  and a promise. `m3_truck` stays set for the postgame Mew sighting, the reward for a complete Kin section
  (story.md §8), which can show at the same spot.

## Not in this mission

These rows sit in the same rooms but belong to later scripts: Vesper on Canalport's beach (slot 16, from
`m4_done`, mission 6), and Stonehollow's rows that mission 1's page lists for missions 9 and 10. Canalport's
flooded lower town after the Breaking (story decision 7) is mission 11's.

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **Ilse's part:** news by Wingull (the Tidewardens' post birds); lending the Kestrel with "If Canalport stands,
  keep her", which pays off mission 1's "once the Commodore says so"; sailing south the same day with the tithe
  fleet on her flagship, **the Holdfast**, Embral first (this puts her fleet at Embral for mission 4).
- **Maren:** her look (a medic's white coat with blue cuffs, a satchel, a notebook), "I asked for this posting",
  the best Frost in the cutter fleet, her notes, Ply on Barnaby's ankle, "I'd have been cross too", and her
  weekly "medical returns" sent by Wingull west, toward the Pinnacle, while Ilse sails south: a quiet seed for
  her confession in mission 9 that names nobody.
- **Brann's goodbye** and Maudie's pie, a prop that comes back twice.
- **The voyage:** two days across the Calm and up Saltmarsh Reach's channels, as narration (decision 5).
- **Canalport:** the City of a Hundred Bridges, blue shutters, the beach dike, the spring tide and "Highwater at
  four bells", the sea sluice that drains the lower town at every ebb, the Grand Cut, the Tanners' Swing, the Long
  Weir, the lock stair, The Dry Boot, the tithe paid in rain, the south road closed while the dikes are walked.
- **Canalport's people:** Harbourmaster Quayle and his ferry Marill pod; Lettie and her father Barnaby the
  bargeman; Effie at The Dry Boot; Odile the chandler; Ivo the armourer; Hobb the docker; Mother Brindle and her eel
  pies; Mrs Pennock and Grandad at their window; a Tidewarden marine at the sandbags.
- **The sluice beast** as a sea creature the spring tide pushed up the channel, wedged in the gates (which is
  what jammed them) rather than guarding them, and carried back out to sea on the ebb when it's beaten: nobody
  kills it. The ferryman's hat it hung on a post, and Quayle writing that down too.
- **Maize's sloop,** the Merry Wooloo, his stomach rumble, and the truck's note.
- **The tide board's** "LOW WATER: NOT TODAY", and Quayle's bells.
- **The rewards:** Nut ×1, Elixir ×2, Great Ball ×2, a Leather Cap and 100 coins from the tide fund (proposed
  for slice 10's income pass). The Elixirs and Great Balls are items §13's Canalport suggestion.
- **Stonehollow's lines** before the voyage and for Act I, and Maren's word on the blue puddle.

## Changes to the build

**Rooms**
- **`canalport_canals`** (new, decision 5's canals for Surf): the lower town, clipped from the town half of
  Golden Sun 2's Alhafra (today's `canalport` takes its beach half) or another Lost Age town with channels, the
  builder's pick, with `--water` over the canals and the drowned quays. South to north: the canal mouth (a water
  entrance from `canalport`'s lock stair), the Grand Cut with Barnaby's barge and Mrs Pennock's window, the
  Tanners' Swing with its quay, plinth, counterweight and chest, the side canal with the mudbank, the Long Weir
  with its three puddles, and the sluice landing, house and gates on the sea wall. From `m3_done` a gate turns
  the drowned quays back to stone and opens the quay stair, a warp on foot back to `canalport`.
- **`canalport`:** the sluice beast's row (slot 13) and the west cliff landing move to the canals; a water warp at
  the lock stair, open from `m3_surf`; a second entrance there for the quay stair; new rows for Barnaby, the
  marine, Odile and Ivo (with their shops, slice 4), Hobb, Brindle, Maize, the Merry Wooloo, the truck, the tide
  board, the notice, the Marill pen and the beach glint (a dig spot setting `m3_glint`); names on today's rows:
  slot 10 Quayle, 11 and 14 Lettie, 12 Effie, 15 Tully. The south warp's two closed lines (the second on
  progression decision 4's flag).
- **`stonehollow`:** `to_canalport` becomes scene 1 (Brann walks in for the pie; Ilse and her marine walk off and
  hide from `m3_started`); the two new states for every row above; Maren's line after the puddle's Frost.

**Actors and engine**
- **The crew in scenes:** `[crew out]` and `[crew in]` step the crew's members out of the lead to stand beside
  them and back in, Golden Sun's way, so Maren (and Tamsin in mission 4) can be staged.
- **A gift that carries a needed HM** goes into a crew Adept's Set with a free slot, never to storage: Marill
  goes to {HERO}'s Set, or to Maren's (she only has Eevee here) if {HERO}'s is full, so Surf always works.
- **Coins as a gift:** a `give` of coins, with its system line (today only `take_coins` exists).
- **Quayle's row** keeps its quest role: the scene's lines, `give_pokemon marill` at L6 with the engine's own
  "{HERO} received Marill!", `hm_surf`, `m3_surf`.
- **Surf onto land:** climbing off Marill onto a landing step or quay, and back on (puzzle 2, the dig, the weir).
- **Gates on the surf layer:** the Swing's gate opens cells to Surf; the weir's three gates open single cells on
  foot; the drained state closes the drowned quays' water and opens them as floor.
- **The beast** (slot 13) moves to the canals, with a step-on trigger at the landing, Kraken's battle picture
  rising from the channel (decision 28, slice 8), Maren's retry line, and scene 8 as its `scene_after`;
  `has_ship` and the handover move out of it into scenes 9 and 10.
- **Scene 3's trigger** fires when both breach flags are set (as mission 2's scene 6 fires on its flag).
- **Maize's yes/no** uses the mirror's yes/no menu, with no flag.
- **The Kestrel's mate** in every mooring room: the chart, then a Bunk row with the home bed's menu (decision 34).
- **A Wingull** as an actor that lands and flies off (scene 10 here and scene 15 in mission 4).
- **`m3_truck`:** the truck as a pushable actor whose push shows the note; the flag is kept for the postgame.
- **The canal Marill pod** and Eevee as actors scenes can move; Marill carries the lead on water (the surf mount,
  demo decision 26).

**New scene steps** (README §2): `phase`, `light` (the glow of Ply), `camera` (pan and back), `pose` (nod, kneel,
stand), `choice` (both reply beats, with the quiet set), `crew out` and `crew in`, coins in `give`, a step-on
trigger (scene 7) and a flag trigger (scene 3).

**Checks.** `tools/mission3_check` follows the new flow: Ilse's posting and its reply menu in both voices, the
voyage, the breaches, the gift, the canals' Swing and weir, Barnaby, the beast and its retry line, the drained
quays, the Kestrel, the jetty's reply menu and the handover to crew 2.
