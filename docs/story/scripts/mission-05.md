# Mission 5: The Eldergrove

> **Status:** draft for your yes or notes (18 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 5, §5 (Celebi) and §9a ("The Hive"). Today's build:
> [mission-5-build.md](../../design/mission-5-build.md).

| | |
|---|---|
| Mission | 5, The Eldergrove (Act I; the Forest site's first visit) |
| Plays after | Mission 4's letter on Canalport's jetty ([mission-04.md](mission-04.md), scene 15), which puts the Greenwild on the Kestrel's chart. **Either order with mission 6** ([mission-06.md](mission-06.md)): it plays the same before or after it |
| Crew | {HERO} and the first partner, Maren and Eevee, Marill in a Set; Vesper and Gastly too if mission 6 came first (`m6_pilot`). Sorrel and Rowlet join in scene 2, at the mission's recruit floor (progression 1; L8 proposed, the mission's target level) |
| Rooms | `eldergrove` (the village), `greenwild` (re-clipped larger: the river, the Sourmire, the Hive Hollow's mouth), `eldergrove_heart` (re-clipped: the root hall, the root pool, the seal hollow), `greenwild_hive` (new: the Hive, optional, decision 9) |
| Clock | Day on arrival and in the forest; dusk from the heart; night from the deed on; the Mossbed rests to dawn |
| Flags in | `m4_done` (the chart's row); `m6_pilot` if Vesper is in the crew |
| Flags out | `m5_intro`, `m5_sorrel`, `m5_forest_intro`, `m5_vine`, `m5_bough`, `m5_mire_in`, `m5_mire_1`, `m5_mire_2`, `m5_mire_3`, `m5_mire_dug`, `m5_heart_in`, `m5_mould`, `m5_ladder`, `m5_vision`, `m5_order`, `forest_seal_deepened`, `hm_cut`, `m5_bush_cut`, `m5_done`; and, optional, `m5_village_dug`, `m5_hive_seen`, `m5_hive_vesper`, `m5_hive_in`, `m5_hive` |
| Unlocks | Sorrel (Forest, with Rowlet) joins, and with her Growth; Cut (`hm_cut`, a kept HM: a Set Pokémon that can learn it, story.md §7); the Forest seal driven deeper (`forest_seal_deepened`, which missions 9 and 14 read); the Hive, once Vesper is in the crew |
| Reply beats | 2: Sorrel at the east path (scene 2); the Commodore's order at the seal (scene 8) |
| Fights | None in the story. Wild battles in the Greenwild and the Hive |
| Leads into | Crew 1's next rest at an inn or a sanctum plays a Crew 2 interlude (decision 7): mission 7 if this is Crew 1's first recruitment, mission 8 if missions 6 and 7 are done |

**The flow.** The Kestrel brings the crew to the Greenwild to hold the Forest seal, as Ilse's letter ordered. Under
the Eldergrove the village is frightened: since spring the great tree's leaves have fallen green, a green light
burns in its heart at night, and Elder Hollin blames Sorrel, the only one who goes near it. Sorrel says the tree
isn't cursed but hungry, and takes the crew in for the tree's sake. Growth binds a rotten bridge, Frost makes a way
across the poison Sourmire, and in the roots under the tree a sprout climbs to the seal. There Celebi shows its
vision further than it has ever gone: six hooded founders closing the Forest Well "so the centre may endure", and
the light running away east under the ground. Then it breaks off. A Tidewarden runner brings the Commodore's order
to drive the seal deeper. Sorrel objects; {HERO} sets it with Earth, Sorrel binds the roots, and the tree falls
silent. Back in the village the Elder calls the curse lifted. Sorrel says it's buried, and leaves with the crew.

**Either order.** Nothing here needs mission 6. Where Vesper is in the crew (`m6_pilot`), she has a few lines of her
own, the Greenwild's Reveal cache shows, and the Hive is open. Each of those lines is marked *Vesper in the crew*
in place and listed under "Either order", below.

## Scenes

### 1. The Greenwild

- Room: `eldergrove`. Trigger: entering, unless `m5_intro` (today's `greenwild_arrival`, rewritten).

*Over black, before the fade:*

**Narration:** The Kestrel sailed west across
the Calm, two days and two nights,
to the coast of the Greenwild.

Long before the coast, they saw the
tree. The Eldergrove stood over the
forest like a green thundercloud.

*[phase day] [fade in 40] The village under the Eldergrove: houses grown into the knees of giant trees, moss on
every roof, rope bridges strung from root to root. Above it all rises the Eldergrove's trunk, wide as a hill, its
crown lost in its own green haze. Leaves come down all the time, and every one of them is green. Kin are
everywhere, a Seedot on a roof, a Shroomish in a window box, and all of them are quiet. Over the east edge of the
village, smoke goes up from a grove on fire.*

*The Kestrel lies at the river landing behind the crew. [crew out] Maren steps out beside {HERO}, Eevee at her
heel. A leaf drifts down, and she catches it.*

**Maren:** A green leaf, falling in summer.
Drought, blight or root rot.

*She turns it over, and frowns.*

**Maren:** ...None of those. I'll need a
new page.

*Vesper in the crew:*

**Vesper:** Smoke, east. Somebody's burning
green wood. It never catches
properly.

*An old woman comes down the root stair from the biggest house, leaning on a staff of living wood that still
has leaves on it. A broad man follows her with an axe on his shoulder and soot on his face. [walk Hollin → before
{HERO}] [walk Brack → beside Hollin] [face Hollin → {HERO}]*

**Hollin:** Tidewardens. The Commodore's
Wingull said you'd come. I am
Hollin, Elder of the Eldergrove.

You've come to hold the Forest
seal. Hold it, then. Nobody here
will stand in your way.

Since spring the great tree has
been sick. Its leaves fall green.
The Kin have gone quiet.

And at night there's a green light
in the heart, where no light should
be.

**Brack:** So we burn the sick groves, on
the Elder's word. It hasn't
stopped it yet.

**Maren:** The heart. Is that where the
seal is?

**Hollin:** Under the tree's roots, past the
river and the Sourmire. The heart
has been closed for years.

Only one fool goes in. Sorrel.

She talks to the tree. And since
spring, the tree talks back. That
is how a curse begins.

**Brack:** She'll be at the east path. She's
always at the east path.

**Hollin:** If you need a guide, she's the
only one there is. I'm sorry for
that.

*[walk Hollin → her house] [walk Brack → the burned grove] [crew in] [flag m5_intro] Control returns.*

### 2. Sorrel

- Room: `eldergrove`, the east path. Trigger: talking to Sorrel (slot 12), unless `m5_sorrel` (today's
  `sorrel_joins`, rewritten).

*At the head of the east path, outside a hut grown out of a living tree, a young woman in a moss-green work coat
kneels by a sapling with a water skin, her sleeves rolled up and her hands stained green to the wrist. A Rowlet sits
on her head. She doesn't look up.*

**Sorrel:** There. Slowly. Nobody's going
to take it off you.

*[face Sorrel → {HERO}] [emote Rowlet: question] Rowlet turns its head right round to look at the crew.*

**Sorrel:** What.

*[crew out]*

**Maren:** Sorrel? We're Tidewardens. The
Elder says you know the way to
the heart.

**Sorrel:** The Elder says a lot. Let me
guess. She told you I'm cursed.

**{HERO} replies:**

1. "She did." · quiet: (Nod)

   **Sorrel:** At least you're honest. Most
   outsiders pretend they weren't
   listening.

2. "I don't believe it." · quiet: (Shake head)

   **Sorrel:** You've known me for a breath.
   Give it a day.

3. "Are you?" · quiet: ...

   **Sorrel:** I hear the tree. If that's a
   curse, then yes.

*Every reply rejoins here.*

**Sorrel:** Since spring, the heart has been
showing me things. Green light.
Pictures that tear before the end.

I told the Elder. Now I'm cursed,
and she burns the trees I can't get
to first.

*[emote Sorrel: anger] She looks at the smoke over the east groves, then down at the sapling.*

**Sorrel:** The tree isn't cursed. It's
hungry. Something is drinking it
from underneath.

**Maren:** From underneath? That's where
the seal is.

**Sorrel:** Is it. Then you'll want to see
what's under it, Tidewarden. So
do I.

Sorrel. I know every root in the
Greenwild. I'll take you to the
heart.

Not for your Commodore. For the
tree.

*[recruit sorrel] Sorrel and Rowlet join the crew.*

**System:** Sorrel joined the crew!

*Vesper in the crew:*

**Sorrel:** And that one?

**Vesper:** Pilot. Paid.

**Sorrel:** Hm. At least you're honest about
it.

*Then, in every crew:*

**Sorrel:** Growth is my Psynergy. Where a
sprout can climb, I can make a way.

Keep up.

*[crew in] [flag m5_sorrel] Control returns. The east path is open.*

### 3. Into the Greenwild

- Room: `greenwild`. Trigger: entering, unless `m5_forest_intro` (today's `rotten_bridge`, rewritten).

*[fade in 30] The Greenwild: trunks as wide as towers, roots like walls, green light coming down in shafts. Leaves
fall without a sound. A river runs across the forest from east to west, fast and brown. The old log bridge over it
sags in the middle, black with rot.*

*[crew out]*

**Sorrel:** The log bridge to the south bank
is rotten through. It wouldn't take
a Rowlet, never mind you.

There's a sprout on this bank by
the bridge. Growth on it, and the
vine will do the rest.

Ask it nicely. It's had a hard
spring.

**Maren:** Do you talk to all of them like
that?

**Sorrel:** Only the ones that listen.

*[crew in] [flag m5_forest_intro] Control returns.*

### 4. The vine bridge

- Room: `greenwild`. Trigger: Growth on the sprout (`m5_vine`, puzzle 1).

*The sprout shivers, then climbs. A green vine runs out along the rotten logs, winds round them again and again,
and pulls them tight. [gate: the bridge's cells open, as built] [emote Rowlet: smile]*

**Sorrel:** There. It'll hold now. Vines
always hold.

*Control returns.*

### 5. The Sourmire

- Room: `greenwild`, the edge of the swamp south of the river. Trigger: stepping onto the Sourmire's edge (a
  step-on spot), unless `m5_mire_in`.

*South of the river the trees stand in black water. Bubbles come up through it, and a sour smell hangs over
everything. [crew out]*

**Sorrel:** The Sourmire. It was always
sour. Since spring, it's been
poison.

**Maren:** Poison. Blistering on contact, by
the smell. Walk through it and
I'll be busy.

The shallows will burn your feet.
The deep pools you can't wade at
all.

...But a deep pool is only a puddle
with ambitions. Frost should take
it.

**Sorrel:** Ice in my swamp. Fine. Don't
freeze the frogs.

*[crew in] [flag m5_mire_in] Control returns.*

### 6. The heart

- Room: `eldergrove_heart`. Trigger: entering, unless `m5_heart_in`.

*[phase dusk] [fade in 30] Under the Eldergrove: a hall of roots as wide as a town square, every root thicker than
a house and grey at the edges. Dusk comes down in threads through cracks far above. A pool fills the middle of the
hall, fed by a spring that wells up pale green. High on the far side a hollow opens in the roots, and something in
it glows.*

*[crew out]*

**Sorrel:** The heart. My gran kept it,
before. When she died, the Elder
closed it. I didn't.

That's the hollow, up there. That's
where it shows me things.

**Maren:** The spring is coming up green,
and the roots are grey. Is that
the sickness?

**Sorrel:** That's what hungry looks like.

*Vesper in the crew:*

**Vesper:** Quiet down here. Not the good
kind.

*[crew in] [flag m5_heart_in] Control returns.*

### 7. Celebi

- Room: `eldergrove_heart`, the seal hollow. Trigger: stepping onto the hollow's threshold (a step-on spot), unless
  `m5_vision`.

*The seal hollow: a round chamber inside the roots, floored with old stone. In the middle lies the Forest seal, a
round stone lid as wide as a cart, carved with six marks. Roots have grown round it and under it, and they are
lifting it: its rim stands a finger's width out of the floor. Green light leaks through the gap. [crew out]*

**Sorrel:** That's the seal. The roots have
pushed it up all spring. As if
they're trying to dig it out.

**{HERO}:** Six marks. The same six as the
Keeping Stone at home.

*Quiet: [emote {HERO}: exclaim] and no line.*

*[wait 30] [light: green, brightening] The light swells up out of the gap and fills the hollow. In it hangs a small
green Pokémon, no bigger than Rowlet, with wings like new leaves and its eyes closed. [show Celebi] [emote Rowlet:
exclaim] [emote Eevee: exclaim]*

**Sorrel:** That's it. That's what talks.

*Celebi opens its eyes. It looks at Sorrel, and then, for a long moment, at {HERO}.*

**Celebi:** You came. And you brought a
keeper.

Look. This is when. Look, and
remember.

*[fade out 30] [still celebi_vision] (The still, for the illustrator, is described below.)*

**Narration:** A young tree, no taller than a
house, over a spring of green
light.

Six figures in hooded robes stand
round it, with their hands on a
round stone lid.

**Hooded figure:** Hold a while. Only a while.
So the centre may endure.

*In the still, the lid closes. The green light narrows to a thread and runs away under the ground, east, toward
the middle of the world. The still pans after it.*

**Celebi:** Every keeper. Every spring. I
show them. Nobody remembers.

I'm so thin now. I can't hold it...

*The still tears from its edges inward, like wet paper. [fade in 20] [light: back to dusk] Celebi flickers once and
is gone. [hide Celebi] The green light sinks back under the seal.*

*[emote Sorrel: silence] [wait 30]*

**Sorrel:** That's further than it's ever
gone. It never got past the tree
before.

It went further with you here.

**Maren:** Founders, sealing the Well. "So
the centre may endure." I'll need
a whole page.

**Sorrel:** The light went somewhere. East,
under the ground. Did you see?

Where does it go?

*Vesper in the crew:*

**Vesper:** I know ghosts. That wasn't one.
That was a memory, with wings.

*[flag m5_vision] Straight on to scene 8.*

### 8. The runner

- Room: `eldergrove_heart`. Trigger: straight on from scene 7.

*Running feet on the roots below. A young Tidewarden in a blue coat soaked to the waist comes up the vine ladder at
a scramble, a sealed oilskin tube in one fist. [show Pell] [walk Pell fast → before {HERO}] She salutes, sways, and
gets her breath.*

**Pell:** Deputy {HERO}? Runner Pell, off
the cutter Dunlin. Orders, from the
Commodore.

The Elder said you'd gone to the
heart. I followed the vines. And
the ice. Thank you for the ice.

The pool, I swam.

*{HERO} breaks the seal and reads.*

**Letter:** Deputy. The Greenwild reports a
green light at the heart since
spring. The Forest seal stirs.

A seal that stirs is a seal that
can be broken. The seal-breaker
will come for this one.

By the Pinnacle's order, which I
pass to you: drive the seal home.
Set it deeper, with Earth.

Then hold it.

I. Graymantle, Commodore. Aboard
the Holdfast.

*[emote Sorrel: anger] [walk Sorrel → between {HERO} and the seal]*

**Sorrel:** No. You saw it. The tree is
starving, and she wants it buried
deeper.

That light is the only thing left
that's trying to tell anyone
anything.

**Maren:** It's the Commodore's seal on the
order, Sorrel. And the Pinnacle's
behind hers.

**Pell:** Begging your pardon. If the
deputy won't, the Commodore will
send someone who will.

*Vesper in the crew:*

**Vesper:** Tidewarden orders. My favourite.

*[face Sorrel → {HERO}]*

**Sorrel:** Well, keeper? You're the one
with Earth in your hands.

**{HERO} replies:**

1. "It's an order." · quiet: (Nod)

   **Sorrel:** It is. That's the trouble with
   orders. They're always somebody
   else's.

2. "Sorrel's right." · quiet: (Shake head)

   *[emote Sorrel: question]*

   **Maren:** Then say so in your report,
   {HERO}. Plainly. But the order
   stands.

3. "What did it want?" · quiet: ...

   **Sorrel:** To be remembered. That's all it
   ever asks.

   **Pell:** Deputy. The order...

*Every reply rejoins here.*

*[wait 30] Sorrel looks at the seal, then at Pell.*

**Sorrel:** ...Fine. If it's done, it's done
gently. Not by marines with fire.

You set it, keeper. I'll bind the
roots. The tree won't fight me.

*[walk Sorrel → beside the seal] [crew in] [flag m5_order] Control returns. The seal waits for Move (puzzle 4).*

### 9. The seal goes down

- Room: `eldergrove_heart`. Trigger: Move on the seal (slot 8), once `m5_order` (its Psynergy event; before the
  order, its refusal line, People and signs).

*[crew out] [pose {HERO}: hands on the lid] [light: amber glow on {HERO}'s hands] {HERO} presses down, and the
Earth answers. The lid sinks a finger's width, then a hand's, grinding against the roots. [shake 40, 2]*

*[pose Sorrel: kneel] [light: green glow on Sorrel's hands] Sorrel lays both palms flat on the roots. They creak,
and close over the lid like the fingers of a fist. [shake 60, 3] The green light goes out.*

*[wait 60] [light: dusk, dimmer] Silence. The spring stops welling. Far above, the leaves stop moving.*

**Sorrel:** ...It's stopped.

It's stopped talking.

*[emote Rowlet: silence] [emote Eevee: sweat]*

**Pell:** Done, then. I'll carry word to
the Commodore. She'll be glad.

*[walk Pell → down the vine ladder] [hide Pell]*

**Maren:** Sorrel. Are you hurt?

**Sorrel:** No. Don't.

*[wait 40] Sorrel gets up and brushes off her knees. She doesn't look at the seal.*

**Sorrel:** You came to learn the Greenwild.
So learn this.

If you must cut a living thing, cut
it clean. A clean cut heals.

Any Kin of yours with an edge on
it, I'll show it how.

*[flag hm_cut]*

**System:** Now you can Cut! Face a small
plant and press A, if a Set
Pokémon can learn Cut.

*[shake 30, 1] On the hall's west side the roots groan and draw apart, and a tunnel opens through them toward
the forest. [gate: the root-way opens]*

**Sorrel:** The root-way. It's showing us
out.

It's never done that for me before.

*[phase night] [flag forest_seal_deepened] [crew in] Control returns. The root-way leads to the Greenwild's north
bank, by the path home.*

### 10. Home by night

- Room: `eldergrove`. Trigger: entering from the Greenwild, once `forest_seal_deepened`, unless `m5_done`.

*[fade in 30] The village at night. Reed lanterns glow in the doors of the root-houses. The smoke over the east
groves is gone. People stand in their doorways looking up at the great tree, where the green light no longer
shows. Elder Hollin waits at the foot of the east path, with Brack and Pell. [walk Hollin → before {HERO}]*

**Hollin:** The light at the heart has gone
out. The whole village watched it
go.

Whatever you did, Deputy, the
Eldergrove thanks you.

Brack. Put out the fires. There'll
be no more burning.

**Brack:** Yes, Elder. Gladly.

*[walk Brack → the burned grove] [hide Brack] [face Hollin → Sorrel] [crew out]*

**Hollin:** Sorrel. The curse is lifted.

**Sorrel:** It isn't lifted. It's buried.

*[emote Hollin: silence] [wait 30]*

**Hollin:** You'll go with them, then.

**Sorrel:** I'll go somewhere the tree can't
hear me thinking.

Somebody out there knows where
that light goes. I mean to ask
them.

**Hollin:** ...Go, then. Mind the roots.

*[walk Hollin → her house] [hide Hollin]*

**Pell:** The Dunlin sails at dawn, Deputy.
The Commodore will have your word
within the week.

*[walk Pell → the landing] [hide Pell]*

**Maren:** And I'll write mine tonight. A
seal, a vision and a very wet
runner.

*Maren writes a page by lantern light, rolls it and whistles. A Wingull drops out of the dark onto a root, and
she ties the tube to its leg. It flies off east over the trees, toward the middle of the world, not south after
Ilse's fleet. [show Wingull] [walk Wingull → off east] [hide Wingull] [emote Sorrel: squint]*

**Sorrel:** East.

**Maren:** Medical returns. Every week.

*[wait 20]*

**Sorrel:** The inn's the Mossbed. Bryony
won't charge much. You look like
you'd pay anything.

Sleep. I won't.

*[crew in] [flag m5_done] Control returns. The Mossbed is a restoration point; Crew 1's next rest at an inn or a
sanctum plays the next Crew 2 interlude (decision 7).*

## The Hive (optional, decision 9)

The Hive Hollow stands off the Greenwild's north path from the start of the mission, but its drones carry off
anyone they see, and only Vesper's Cloak gets past them. Its warp opens once Vesper is in the crew (`m6_pilot`): in
this mission if mission 6 came first, or on any later visit. It never touches the main story's flags.

### H1. The Hive Hollow

- Room: `greenwild`, the north path. Trigger: stepping onto the hollow's mouth (a step-on spot), once
  `m5_sorrel`, unless `m5_hive_seen`.

*A hollow trunk as big as a house, its mouth sealed round with gold wax. Combee drones circle it in slow loops,
humming, and a deep, sweet hum comes from inside. A post by the path says KEEP OUT. [crew out]*

**Sorrel:** The Hive Hollow. Mother Hazel's
boys went in for honey in spring.
They're still in there.

Anything the drones see, they carry
inside. And whatever goes in stays,
humming.

**Maren:** Humming?

**Sorrel:** Happily. That's the worst part.

*Without Vesper in the crew:*

**Sorrel:** You'd need to get past without
being seen. I can't. Nobody can.

*Vesper in the crew:*

**Vesper:** Combee. Lots of them. They see by
light.

Stay in the dark and they won't
see us at all. I'll Cloak us.

*[crew in] [flag m5_hive_seen] (and [flag m5_hive_vesper] when Vesper is in the crew) Control returns.*

*If Vesper joins later, the first time the crew comes back to the mouth with her (once `m6_pilot` and
`m5_hive_seen`, unless `m5_hive_vesper`):*

*[crew out]*

**Sorrel:** The Hive. Hazel's boys are still in
there, humming.

**Vesper:** Bees in a tree, and people who are
happy about it. Lovely.

Stay in the dark. I'll Cloak us.
They see by light.

**Sorrel:** If you get us all turned into
bees, I'll never speak to you
again.

**Vesper:** Promise?

*[crew in] [flag m5_hive_vesper] Control returns. The hollow's mouth is open.*

### H2. Inside the Hive

- Room: `greenwild_hive`. Trigger: entering, unless `m5_hive_in`.

*[fade in 30] Inside the hollow trunk: galleries of honeycomb climbing out of sight, every cell glowing warm gold
from within. The hum is everywhere, in the floor and the walls and the crew's teeth. It's warm, and it smells of
summer, and it's very hard to remember why anyone would want to leave. Between the bright combs run lanes of bare,
dark bark. Drones fly their loops over the light. [crew out]*

**Maren:** It's lovely. Why is it lovely? I
don't like that it's lovely.

**Vesper:** Keep to the dark bark. In the
light they'll see us, Cloak or no
Cloak.

**Sorrel:** And if they see us?

**Vesper:** Then we hum.

*[crew in] [flag m5_hive_in] Control returns.*

### H3. The queen wakes

- Room: `greenwild_hive`, the queen's chamber. Trigger: Reveal on the queen (Hive puzzle 3, `m5_hive`).

*Reveal's light spreads across the royal comb, and the gold comes away from it like old paint. Underneath, the wax
is grey and cracked, and the cells are nearly empty. [light: the gold drains to grey] The queen's wings stop
shining. She shudders, and looks at her comb as if she has never seen it before. [emote Vespiquen: exclaim]*

*[crew out]*

**Sorrel:** The comb's grey. Like the roots.

They make it from the tree's sap,
and since spring the sap's been
wrong.

**Vesper:** She was dreaming the comb was
full. Everyone who came in dreamed
it with her.

*The hum climbs higher, thins, and stops. All through the Hive the drones settle on the comb and fold their
wings. From the gallery behind, two muffled voices.*

**Linn:** ...Osric? Why am I made of honey?

**Osric:** You were a bee. We were both bees.
It was lovely.

*[walk Linn and Osric → the chamber door] They blink at the crew.*

**Linn:** Is it still spring?

**Maren:** It's summer. Sit down, both of
you. Honey in the ears, wax in the
hair, a sunburn, somehow.

You'll live. Go home to your
mother.

*[walk Linn and Osric → the Hive's mouth] [hide Linn and Osric] [emote Vespiquen: silence] The queen bows her
head to the crew. Then she taps a sealed cell beside her with one claw, and it cracks open on a chest. [show the
queen's chest]*

**Sorrel:** That's thanks. Take it. She'll be
offended if you don't.

*[crew in] [flag m5_hive] Control returns. Linn and Osric are home in `eldergrove`, beside Mother Hazel.*

### The drones' catch (the room's `caught` steps)

**System:** A drone has seen the crew!

*The drones swarm in, humming very kindly, and carry everyone gently but firmly back to the hollow's mouth. [fade
out 20] [to_entrance 0] [fade in 20]*

**Sorrel:** Well. That was humiliating.

## The still (for the illustrator)

*Still `celebi_vision`, 480×320, made like the opening's stills ([opening.md](opening.md)): painted from a written
prompt, reduced to the game's palette and pixel size and cleaned by hand, on a contact sheet first (decision 23).
The message box covers the bottom third, so the focal point stays in the top two-thirds, with quiet ground at the
bottom. No text.*

*The still: the seal hollow six hundred years ago. The Eldergrove is a young tree, no taller than a house, its
leaves bright, standing over a round pool of green light where the hollow's stone floor will be. Six figures in
hooded robes, the same robes as the opening's still 2 and the Vault's mural, stand round the pool, their faces lost
under their hoods. Together they lower a round stone lid carved with six marks onto the light, and the light round
its rim is narrowing to a seam. From the seam a single thread of green light runs away under the ground toward the
right of the picture (east), thinning as it goes. At the belt of the figure nearest the viewer hangs a brass
compass with a needle of blue glass (the Lodestar, for those who look; nobody in the scene says so). Celebi hangs
above the young tree, small and bright, watching. Warm green and gold, the light of a summer morning long gone,
the edges soft and faded like an old memory.*

*Motion: a slow pan right, following the thread of light, for Celebi's last two pages. Then the picture tears from
its edges inward like wet paper (a mask over the still, the scene's own transition) to the hollow at dusk.*

## People and signs, by room

### `eldergrove`

*The states:* arrival (`m5_intro`, until `m5_sorrel`); in the forest (`m5_sorrel`, until `forest_seal_deepened`);
after the seal (`forest_seal_deepened` on, Act I). Mother Hazel and her sons also change with `m5_hive`. Cells are on
today's 29×30 clip; new people give a place instead.

- **Elder Hollin**, slot 8 (today's "Elder"), cell (13,11), at the foot of her house's root stair. Arrival, after
  scene 1:

  **Hollin:** The east path, Deputy. Sorrel will
  be there. She always is.

  *In the forest:*

  **Hollin:** You took her in with you. Bring
  her out again. Whatever I think of
  her, she's ours.

  *After the seal:*

  **Hollin:** The tree is quiet. Quiet is
  better than cursed. I tell myself
  so every hour.

- **Sorrel**, slot 12, cell (25,14), at the east path: scene 2, then she is in the crew. Her row hides from
  `m5_sorrel` (as built).

- **Brack, the forester** (new), at the burned grove on the east edge. Arrival:

  **Brack:** We burn the sick groves before
  the sickness spreads. Elder's word.
  I hate every tree of it.

  *In the forest:*

  **Brack:** Three more groves today. The ash
  comes out grey. Ash shouldn't be
  grey.

  *After the seal:*

  **Brack:** No more burning, the Elder says.
  I've put the axe away. I may never
  get it out again.

- **Fennel, the apothecary** (new), at her stall under the Kin-stone's tree. She opens the Eldergrove apothecary
  (Herb, Corn, Nut, Antidote, Elixir; items-and-economy.md §11, decided: no balls, no weapons) after her line. In
  every state:

  **Fennel:** Herbs, Corn, Antidotes. The
  Sourmire's poison since spring.
  Buy Antidotes.

  No Poké Balls, mind. In the
  Greenwild, Kin come with you, or
  they don't.

  *Not enough coins, in the shop:*

  **Fennel:** That's more than your purse holds.
  The forest doesn't give credit
  either.

  *Leaving the shop:*

  **Fennel:** Walk softly.

- **Bryony, the innkeeper**, slot 11 (today's "Innkeeper", the inn role), cell (7,11), at the Mossbed. Before the
  rest menu, arrival and in the forest:

  **Bryony:** The Mossbed. Beds of real moss,
  changed every week. Mostly.

  *After the seal:*

  **Bryony:** The tree's quiet tonight. Fifty
  years I've slept under it, and
  I've never heard it quiet.

  *After resting:*

  **Bryony:** You slept like a root. Good.
  Breakfast is berries. It's always
  berries.

- **Rue, a basket-weaver**, slot 9 (today's first "Villager"), cell (12,7). Arrival:

  **Rue:** Keep clear of the east path. They
  say the tree marked her the day
  she was born.

  I don't know who "they" are. But
  they say it a lot.

  *In the forest:*

  **Rue:** You went in with her? And came out?
  ...Well. Maybe "they" were wrong.

  *After the seal:*

  **Rue:** Sorrel's leaving with you, I hear.
  The east path will be very quiet.
  I might go and look at it.

- **Sedge, a Kin-warden**, slot 10 (today's second "Villager"), cell (17,15), by the Kin-stone. In every state:

  **Sedge:** We don't battle Kin for sport in
  the Greenwild. They're neighbours,
  not toys.

  If a Kin asks you for a fight, give
  it a good one. That's only manners.

- **Clover, a child** (new), with a Seedot, by Sorrel's hut. Arrival:

  **Clover:** Sorrel fixed my Seedot's leaf.
  Don't tell the Elder. I'm not
  allowed to talk to Sorrel.

  *In the forest:*

  **Clover:** You took Sorrel! Is she guiding
  you? She's the best at guiding. She
  knows every root.

  *After the seal:*

  **Clover:** Is Sorrel going away? She said
  she'd write to me. She's never
  written anything.

- **Mother Hazel** (new), at her root-house door by the north path. Until `m5_hive`:

  **Hazel:** My boys, Linn and Osric, went to
  the Hive Hollow for honey in the
  spring. They never came home.

  At dusk they come to its mouth and
  wave at me. Then they go back in.
  They look so happy. It's horrible.

  *From `m5_hive`:*

  **Hazel:** My boys came home! Sticky to the
  ears, and humming. Thank you.
  Thank you.

- **Linn and Osric** (new), beside their mother, from `m5_hive`:

  **Linn:** We were bees, Mam says. I don't
  remember. I remember it was nice.

  **Osric:** I miss being a bee, a bit. Don't
  tell Mam.

- **Tully, the Kestrel's mate**, slot 13, cell (3,17), at the river landing (the voyage role). The first line here,
  then mission 3's chart and bunk:

  **Tully:** The Greenwild, Deputy. I'll keep
  her at the landing. These trees make
  me feel very short.

**Signs and things to examine**

- **The village sign**, at the landing:

  **Sign:** THE ELDERGROVE. Mind the roots.
  The roots were here first.

- **The great tree**, the trunk behind the Elder's house. Before the seal:

  **Sign:** The Eldergrove's trunk, as wide as
  a hill. Its bark is grey at the
  edges. Green leaves drift down.

  *After the seal:*

  **Sign:** The Eldergrove, silent. The
  leaves still fall green.

- **The Kin-stone**, in the middle of the village:

  **Sign:** A mossy stone carved with the
  forest's Kin: Seedot, Shroomish,
  Rowlet. Berries lie at its foot.

  Six small marks are cut into its
  base, older than the carvings.

- **The tithe notice**, by the landing:

  **Sign:** BY ORDER OF THE PINNACLE: the
  element tithe falls due at the turn
  of the season.

  The Greenwild pays in harvest. Seed
  and sap to the coast post.

- **The burned grove**, at the east edge. Before the seal:

  **Sign:** Black stumps where a grove stood.
  The ash is grey, not white.

  *After the seal:*

  **Sign:** The fires are out. Somebody has
  planted one acorn in the ash, and
  watered it.

- **Sorrel's hut**, at the east path. Until `m5_sorrel`:

  **Sign:** A hut grown out of a living tree.
  Its door is a curtain of vines. A
  board on it says GO AWAY.

  *From `m5_sorrel`:*

  **Sign:** The vine curtain is tied back. A
  new board says: STILL GO AWAY.

- **Sorrel's sapling**, by the hut:

  **Sign:** A sapling, freshly watered. It's
  the only thing in the village that
  looks well cared for.

- **The east path** (the warp's closed line, until `m5_sorrel`, as built):

  **Sign:** The path east into the Greenwild.
  Nobody goes in without someone who
  knows the way.

- **The Mossbed's sign:**

  **Sign:** THE MOSSBED. Beds of real moss.
  Shoes off.

- **Fennel's sign:**

  **Sign:** FENNEL'S. Herbs and simples. No
  Poké Balls, no blades, no
  arguments.

- **The root glint** (new), in the roots behind the Kin-stone, until `m5_village_dug` (Scoop sets it):

  **Sign:** Something glints between two roots,
  under a drift of leaves. Scoop would
  dig it out.

### `greenwild`

*The states:* before the seal (until `forest_seal_deepened`); after the seal (night). No people: the forest's lines
are Sorrel's, in the scenes. Wild battles as built: Golden Sun's table 22 (Drone Bees and their kind) and the forest
Kin (Seedot, Combee, Shroomish), now at L7–9 for the mission's target level (progression 3).

- **The path post**, at the village end:

  **Sign:** THE GREENWILD. To the heart:
  south, over the river, through the
  Sourmire. Don't.

- **The river**, along both banks:

  **Sign:** The river runs fast and brown over
  sunk logs. Too rough to Surf.

- **The rotten bridge**, until `m5_vine`:

  **Sign:** The old log bridge, black with
  rot. One step, and it would go.

  *From `m5_vine`:*

  **Sign:** The vine has bound the logs tight.
  It holds.

- **The sprout**, slot 8 (puzzle 1), until `m5_vine`:

  **Sign:** A sprout clings to the bank beside
  the rotten bridge.

  *From `m5_vine`:*

  **Sign:** The vine runs from the sprout
  along the bridge, thick as a rope.

- **The trunk sprout** (new, optional A), at the foot of a giant trunk on the south bank, until `m5_bough`:

  **Sign:** A sprout at the foot of a giant
  trunk. High above, something glints
  on a bough.

  *From `m5_bough`:*

  **Sign:** A vine climbs the trunk to the
  high bough.

- **The Sourmire's sign:**

  **Sign:** THE SOURMIRE. It was always sour.
  Now it's worse.

- **The bog pools**, three (puzzle 2), until each is frozen:

  **Sign:** A deep pool of black water. Far
  too deep to wade. Frost might take
  it.

  *Frozen:*

  **Sign:** A pillar of ice stands in the bog,
  its top dry. It would take your
  weight.

- **The shallows** (the hazard's line, replacing today's "The swamp water burns!"):

  **System:** The Sourmire stings! Its poison
  burns the crew's feet.

- **The mire glint** (new, optional B), on a dry hummock in the Sourmire, until `m5_mire_dug`:

  **Sign:** Something glints in the mud of a
  dry hummock. Scoop would dig it
  out.

- **The Hive post**, on the north path:

  **Sign:** THE HIVE HOLLOW. KEEP OUT. The
  drones take anything they see. By
  order of the Elder.

- **The hollow's mouth** (the Hive warp's closed line, until `m6_pilot`):

  **Sign:** Drones circle the hollow's mouth.
  Anything they see, they carry in.
  You'd need to go unseen.

- **The old stump** (new, optional D: the Reveal cache), on the north bank. A hidden chest shows with Reveal; until
  then the stump says:

  **Sign:** An old stump, split by lightning.
  The air above it shimmers, as if
  something's there.

- **The thick bush**, slot 9 (optional C, Cut), by the root-way's mouth on the north bank. Before `hm_cut`:

  **Sign:** A thick bush, its stems tough as
  wire. Something glints behind it.

  *From `hm_cut`, until `m5_bush_cut`:*

  **Sign:** A thick bush. Something glints
  behind it. A clean cut would clear
  it.

- **The root-way's mouth** (new), on the north bank, from `forest_seal_deepened`:

  **Sign:** A tunnel through the great tree's
  roots, back to the heart. The roots
  opened it themselves.

### `eldergrove_heart`

No people but Celebi and Pell (scenes 7 to 9). No random battles: the heart is the tree's own. The things to
examine:

- **The roots**, round the hall:

  **Sign:** Roots thicker than houses, grey at
  the edges and cold to the touch.

- **The root pool**, in the middle of the hall. Before the seal:

  **Sign:** A still pool, fed by a spring that
  wells up pale green. Calm enough to
  Surf.

  *After the seal:*

  **Sign:** The spring has stopped. The pool
  lies flat and dark.

- **The leaf mould** (puzzle 3), on the ledge under the hollow, until `m5_mould`:

  **Sign:** A heap of leaf mould against the
  root wall. A pale shoot pokes out of
  the top. Scoop would clear it.

- **The pale sprout** (puzzle 3), from `m5_mould`, until `m5_ladder`:

  **Sign:** A pale sprout at the foot of the
  root wall, free of the mould. Growth
  would wake it.

- **The vine ladder**, from `m5_ladder`:

  **Sign:** A vine ladder climbs the root wall
  to the hollow.

- **The Forest seal**, slot 8 (today's "Heart of the tree"). Before `m5_order`:

  **Sign:** The Forest seal: a stone lid in
  the roots, carved with six marks.
  Green light leaks round its rim.

  *Move on it before `m5_order` (the Psynergy event's `else_text`; nothing moves):*

  **System:** The lid won't move. Not without a
  reason.

  *From `m5_order`, before the deed:*

  **Sign:** The lid stands a finger's width
  proud of the roots. It's waiting
  for you.

  *From `forest_seal_deepened` (today's `text_after`, rewritten):*

  **Sign:** The Forest seal, driven deep. The
  roots are knotted over it like a
  fist.

- **The root-way**, on the hall's west side, from `forest_seal_deepened`:

  **Sign:** A tunnel through the roots to the
  forest. It wasn't there this
  morning.

### `greenwild_hive` (new)

*The states:* the dream (until `m5_hive`); awake (`m5_hive`). Wild battles in the dream only: Golden Sun's Drone
Bees and Combee, at a low rate.

- **Linn and Osric, the foragers** (new), in the comb gallery. The dream, both together:

  **Foragers:** We are the Hive. Your sweetness
  will join our own.

  Struggling is sticky.

  *Awake:* they have gone home (scene H3).

- **The drones** (guards), in the dream, if examined from the dark:

  **Sign:** A Combee drone, humming its loop.
  It hasn't seen you. Yet.

  *Awake:*

  **Sign:** A drone dozes on the comb. It
  looks very tired.

- **The queen**, a Vespiquen on the royal comb (Hive puzzle 3). The dream:

  **Sign:** The queen hums. It's a kind hum.
  You'd like to stay. You'd like to
  stay for ever.

  *Awake:*

  **Sign:** The queen is tidying her grey comb.
  She seems embarrassed.

**Signs and things to examine**

- **The comb.** The dream:

  **Sign:** Golden comb, glowing and warm. It
  smells of summer.

  *Awake:*

  **Sign:** Grey comb, cracked and nearly
  empty. It smells of old wax.

- **The dark bark** (the shadow lanes):

  **Sign:** Bare bark between the combs, dark
  enough to hide in.

- **The bright span** (Hive puzzle 2):

  **Sign:** A span of bright comb across a
  drop. Not a shadow on it anywhere.

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| The root glint | `eldergrove`, behind the Kin-stone (Scoop; sets `m5_village_dug`) | Nut ×1 | **System:** {LEADER} found Nut! (the engine's line) |
| The high bough | `greenwild`, up the trunk vine (optional A) | Leather Gloves (items §13's Greenwild suggestion) | The engine's chest line, naming `{LEADER}` |
| The mire glint | `greenwild`, the Sourmire's hummock (Scoop; sets `m5_mire_dug`) | Elixir ×1 | **System:** {LEADER} found Elixir! |
| The stump cache | `greenwild`, the old stump (Reveal; Vesper in the crew) | Elixir ×2 | The engine's chest line |
| The bush chest | `greenwild`, behind the thick bush (Cut, as built) | Nut ×2 | The engine's chest line |
| The pool alcove | `eldergrove_heart`, a root alcove across the pool (Surf; the dungeon's gear chest, items §13) | Circlet | The engine's chest line |
| The ladder nook | `eldergrove_heart`, beside the vine ladder's top | Herb ×3 | The engine's chest line |
| The queen's thanks | `greenwild_hive`, beside the royal comb (scene H3) | Cookie ×2 (Golden Sun's PP food) | The engine's chest line |
| The Commodore's order | Scene 8 | Nothing: words | The Letter, above |

Open question 19 (a staff for Sorrel as this mission's gear chest) is still open; the Circlet is items §13's
suggestion until it's answered.

## Puzzles

The crew's verbs here: {HERO}'s Move and Scoop, Maren's Frost, Surf on Marill, and Sorrel's Growth from scene 2.
Vesper's Reveal, Halt and Cloak only when she is in the crew, and only for optional rewards and the Hive. Cut from
scene 9, for one optional chest. The main path needs only the verbs every order of play has (story.md §7: Crew 1's
Psynergy, or what the named Adept brings). Pushed things stay where they're pushed, so every block can be got
behind again.

**The Greenwild**

**Puzzle 1. The vine bridge (Growth, as built).**
1. The river cuts the forest, too rough to Surf. The only crossing is the old log bridge, rotten through.
2. On the north bank by the bridge, a sprout. Cast Growth on it: a vine binds the logs (`m5_vine`, the bridge's
   gate, as built), and scene 4 plays.

It teaches Sorrel's verb at once.

**Puzzle 2. The Sourmire (Frost three times, new).**
1. South of the river, the way to the heart crosses the Sourmire. Its shallows are a hazard: each step costs a
   little HP, never below 1 (as built).
2. In the middle, three deep bog pools block the way in a line, each one cell from the next. They can't be walked.
3. From the hummock before them, cast Frost on the first: an ice pillar, dry on top, which can be walked on
   (`m5_mire_1`, a gate opening that cell). Step onto it and Frost the second (`m5_mire_2`), then the third
   (`m5_mire_3`). The last pillar reaches the far bank and the path to the heart.
4. A way round through the shallows reaches the hummock; the shortest crosses three stinging cells, so the player
   feels the swamp before the ice saves them from the worst of it.

It shows Maren's Frost making a way, as at the Long Weir (mission 3), in a place that hurts.

**Optional A. The high bough (Growth, new).**
1. On the south bank, a second sprout at the foot of a giant trunk; something glints on a bough far above.
2. Cast Growth: a vine climbs the trunk (`m5_bough`, a gate opening the climb), and the bough holds the Leather
   Gloves.

**Optional B. The mire glint (Scoop, new).** On a dry hummock off the frozen path, a glint: Scoop digs out an Elixir
(`m5_mire_dug`).

**Optional C. The thick bush (Cut, as built).** On the north bank by the root-way's mouth, so the way home passes
it: from `hm_cut`, a Set Pokémon that can learn Cut clears it (`m5_bush_cut`), and the chest behind it holds two Nuts.

**Optional D. The stump cache (Reveal, new).** With Vesper in the crew, Reveal shows a chest tucked inside an old
stump on the north bank (the region's Reveal cache, items §13).

**The heart**

**Puzzle 3. The way up (Surf, Scoop and Growth, new).**
1. The hollow is high on the hall's far side, with a sheer root wall below it. The root pool fills the hall between.
2. Surf across the pool on Marill to the ledge at the wall's foot, and climb off (mission 3's landing steps).
3. On the ledge, a heap of leaf mould with a pale shoot in it. Cast Scoop: the mould slumps away, uncovering a
   sprout (`m5_mould`; the sprout's row shows).
4. Cast Growth on the sprout: a vine ladder climbs the wall to the hollow (`m5_ladder`, a gate). The Herb nook is
   beside its top; the Circlet's alcove is across the pool, by Surf.

Three verbs from three Adepts and a Pokémon, chained, Golden Sun's way.

**Puzzle 4. The seal (Move, scripted, new).**
1. Until the order, Move on the seal gives its refusal line, and nothing moves.
2. From `m5_order`, Move on the seal plays scene 9: {HERO} sets it, Sorrel binds it. It's the only way on, so the
   player's own hand does what the order says.

**The Hive** (optional, from `m6_pilot`)

**Hive puzzle 1. The drone lanes (Cloak, new).**
1. The first gallery is lit comb crossed by lanes of dark bark. Two drones fly loops over the light (patrols, with
   sight along their heading, as mission 7's guards).
2. Cast Cloak: as in Golden Sun, the crew is unseen while it stands on dark cells, and stepping onto lit comb ends
   the Cloak.
3. A winding lane of dark bark runs between the loops to the far door. A drone that sees the crew plays the room's
   `caught` steps (back to the mouth).

**Hive puzzle 2. The bright span (Halt, new).**
1. The way to the queen crosses a span of bright comb with no shadow on it. A sentry drone hovers at its far end,
   watching it.
2. From the last dark cell, cast Halt on the sentry: it freezes, blind, for ten seconds (as built for guards).
3. Cross before it stirs. If it wakes first, the crew is seen.

**Hive puzzle 3. The queen (Reveal, new).** In the queen's chamber, cast Reveal: the glamour comes off the comb, the
queen wakes (scene H3, `m5_hive`), and her chest opens.

## Eggs

- **"The Hive"** (story.md §9a, Star Trek's themed puzzle: a swarm that "absorbs" everything that enters). Cloak past
  the drones, and free the queen's mind with Reveal. The absorbed are Hazel's sons, humming happily since spring,
  and their chant bends the original's line: "We are the Hive. Your sweetness will join our own. Struggling is
  sticky." Decision 9's shape: optional, open once Vesper is in the crew, with a chest at the queen. The glamour
  comes from the grey sap, so the egg also shows the tree's sickness from another side.
- **A quiet Golden Sun nod** (an invention, not on §9a's list): a village that calls one of its own cursed, under a
  great tree that's sick. The placeholder rooms are Golden Sun's Kolima and Tret.

## Either order: the lines that differ

Everything else plays the same before or after mission 6.

| Where | When | What |
|---|---|---|
| Scene 1 | `m6_pilot` | Vesper's line on the smoke |
| Scene 2 | `m6_pilot` | Sorrel's "And that one?", Vesper's "Pilot. Paid." and Sorrel's answer |
| Scene 6 | `m6_pilot` | Vesper's "Quiet down here" |
| Scene 7 | `m6_pilot` | Vesper's "memory, with wings" |
| Scene 8 | `m6_pilot` | Vesper's "Tidewarden orders. My favourite." |
| H1 | without `m6_pilot` | Sorrel's "You'd need to get past without being seen" |
| H1 | `m6_pilot` | Vesper's Cloak plan, and the warp opens |
| H1, later | `m6_pilot`, after `m5_hive_seen` without her | The return to the mouth with Vesper (`m5_hive_vesper`) |
| `greenwild` | `m6_pilot` | The stump cache shows with Reveal (optional D) |

The two missions can also interleave: Vesper can be hired in Canalport, then this mission played, then the reef. So
her lines need only `m6_pilot`, each stands on its own, and none answers a line from a scene she may have missed. In
every `[crew out]`, Vesper steps out with the others when she is in the crew, and back in at `[crew in]`.

## Not in this mission

Celebi is calmed and caught in mission 14 ("Root and Ruin"), where the deepened seal is undone and the village
apologises to Sorrel; the burned groves are Sorrel's heart quest ("Replant the burned groves", story.md §11), which
the acorn in the ash seeds. The ship's living hull comes with the open Forest Well, also mission 14. The words of
the Crew 2 interlude that the next rest plays belong to mission 7's and mission 8's pages.

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **The voyage:** two days west across the Calm, and the Eldergrove seen from far off "like a green thundercloud"
  (story.md §2's landmark).
- **The village:** root-houses, rope bridges and moss roofs; the Kin-stone with six old marks at its base; the
  Mossbed; Fennel's stall; the Greenwild's tithe paid in harvest, "seed and sap"; the village burning its sick
  groves on the Elder's word, with grey ash (a seed for Sorrel's heart quest, and the acorn in the ash after the
  seal).
- **The sickness:** green leaves falling in summer, quiet Kin, grey roots and sap, and a green light at the heart
  at night, all since spring; Sorrel's reading of it, "It's hungry. Something is drinking it from underneath"
  (layer 2's truth, said before anyone can know it).
- **"Kin":** the Greenwild's own word for Pokémon (story.md §9's "forest kin"), used by its people (Sorrel too)
  and on its signs; the rest of the crew say Pokémon (README §8). Fennel's "Kin come with you, or they don't" is
  the forest's reason for selling no balls (items §11).
- **The village's people:** Elder Hollin (frightened, not cruel: "I'm sorry for that", "she's ours", "Mind the
  roots"), Brack the forester, Fennel, Bryony, Rue, Sedge the Kin-warden and the Greenwild's manners ("If a Kin asks
  you for a fight, give it a good one"), Clover and her Seedot, Mother Hazel and her sons Linn and Osric.
- **Sorrel:** her look (a moss-green work coat, hands stained green, Rowlet on her head), her hut grown from a
  living tree with its GO AWAY board, her sapling, her gran who kept the heart until the Elder closed it, "Not for
  your Commodore. For the tree", "Keep up", and why the village calls her cursed: since spring the heart has shown
  her Celebi's torn pictures, and she said so.
- **Celebi:** it speaks, briefly and strangely ("This is when"), has shown its vision to "every keeper, every
  spring", is "so thin now" (drained, as every legendary is), and gets further with a keeper there. Its vision: the
  young tree, six hooded founders, "Hold a while. Only a while. So the centre may endure" (the stopgap meant for one
  generation, story.md §3, hinted), the light running east under the ground (the drain to the Crown, hinted), and
  the Lodestar at a founder's belt in the still, which nobody mentions.
- **The Forest seal:** a round stone lid with the six marks, lifted by the roots all spring; driven down by
  {HERO}'s Earth and bound by Sorrel's roots; the tree's silence after, and the root-way it opens.
- **The order:** Runner Pell off the cutter Dunlin, soaked to the waist ("Thank you for the ice", "The pool, I swam"); Ilse passing on "the
  Pinnacle's order", so the deepening comes from the top (Vey) through a Commodore who believes in it; "If the deputy
  won't, the Commodore will send someone who will".
- **Cut from Sorrel:** "If you must cut a living thing, cut it clean. A clean cut heals."
- **Maren:** "a puddle with ambitions", "I'll need a new page", her honey diagnosis, and a second Wingull report
  flown east toward the centre, which Sorrel notices ("East.") and Maren deflects ("Medical returns").
- **The Greenwild:** the river too rough to Surf, the Sourmire and its three bog pools, the high bough, the Hive
  Hollow off the north path, the old stump, the root-way.
- **The Hive:** its glamour as a dream the queen dreams from the grey sap's honey, which Reveal breaks; the foragers
  absorbed since spring, who come to the mouth at dusk to wave; Cloak working only in the dark, as in Golden Sun;
  the drones carrying intruders "gently but firmly" back out.
- **The rewards:** Nut ×1, Leather Gloves, Elixir ×1, Elixir ×2, Nut ×2 (as built), the Circlet, Herb ×3 and
  Cookie ×2; the gloves and Circlet are items §13's suggestions.

## Changes to the build

**Rooms**
- **`eldergrove`:** today's rows renamed (slot 8 Hollin, 9 Rue, 10 Sedge, 11 Bryony, 12 Sorrel, 13 Tully) with
  text by state; new rows for Brack, Fennel (with the apothecary's shop, slice 4), Clover, Hazel, Linn and Osric
  (from `m5_hive`), and the signs; the root glint (a dig spot); the arrival scene rewritten, with Hollin and Brack
  walking in; Sorrel's scene rewritten with its reply menu; a new enter scene (scene 10) from the Greenwild once
  `forest_seal_deepened`, with Pell and a Wingull as actors.
- **`greenwild`** re-clipped larger from Kolima Forest (Golden Sun 1, room 40 and its neighbours, the builder's
  pick) to hold: the village path, the river with the vine bridge (as built), the south bank's trunk sprout and its
  climb gate, the Sourmire (today's hazard, a dry hummock, three bog pools with gates, the mire glint), the path
  south to the heart, the north path with the Hive post and the hollow's mouth (a step-on spot and a warp to
  `greenwild_hive` on `m6_pilot`, with the closed line), the old stump (a hidden chest), the thick bush and its chest
  (as built, moved to the north bank) and the root-way's mouth (a new entrance from the heart). The river is never
  on the surf layer. The swamp gets tiles from the Essentials parts bin (demo slice 8) in place of today's tint.
- **`eldergrove_heart`** re-clipped from Tret's insides (Golden Sun 1, room 44 and its neighbours) to hold: the root
  hall with the pool (`--water`, the surf layer, with landing steps), the ledge with the leaf mould and the sprout,
  the vine ladder (a gate), the Herb nook, the Circlet's alcove across the pool, the seal hollow (a step-on spot at
  its threshold) with the seal (slot 8), and the root-way on the west side (a gate on `forest_seal_deepened` and a
  warp to the Greenwild's north bank). No random battles.
- **`greenwild_hive`** (new, decision 9): a hollow tree of comb, clipped from a Golden Sun tree or cave room, the
  builder's pick, with comb tiles from the Essentials parts bin: the mouth (entrance 0), the drone gallery with its
  dark lanes, the bright span with the sentry, the foragers' gallery, and the queen's chamber with her chest.
  Encounter table: Drone Bees and Combee at a low rate, until `m5_hive`.

**Actors and engine**
- **Sorrel's scene** keeps `recruit sorrel` and `m5_sorrel`; her pre-recruit row hides on `m5_sorrel` (as built).
- **`celebi_vision` is split** into scenes 7 to 9: the vision on a step-on trigger, the runner straight on, and the
  deed on Move. `forest_seal_deepened` and `hm_cut` are set in scene 9; `m5_done` moves to scene 10, in the village.
- **The handover moves out** (decision 7): today's two `when` steps at the end of `celebi_vision`, which switch to
  crew 2 for mission 7 or 8, come out. The interlude starts from the rest hook (an inn's or a sanctum's menu
  closing) once `m5_done` is set, so the restoration point is the Mossbed or wherever Crew 1 next rests.
- **Psynergy events gated by a flag** (mission 4's `if_flag` with `else_text`): the seal's Move waits for
  `m5_order`, and its event plays scene 9.
- **Scoop that reveals a row:** the leaf mould's dig flag shows the sprout's row.
- **Gates on Frost and Growth flags:** the three bog pillars, the trunk climb and the vine ladder.
- **Surf and the landing steps** in the heart (mission 3's), with the pool on the surf layer.
- **Celebi on the field:** the expansion's overworld sprite at 2× with its appear and vanish (decision 28), in the
  `light` step's green glow.
- **Cloak** (decisions 6 and 9): Golden Sun's rule, unseen on dark cells and broken by lit ones. A room lists its
  dark cells (a `shadows` key), and a guard's sight skips a cloaked crew on them. Built for the Hive, and the Cloak
  Ball backup can use it later.
- **Halt on a guard** (mission 7's): the sentry freezes and is blind for ten seconds.
- **The Hive's `caught` steps:** back to the mouth with the system line and Sorrel's.
- **The apothecary's stock** in `data_src/shops.json` (decided, items §11).
- **Lines for a crew member who may not be there:** Vesper's lines are `when` steps on `m6_pilot`, and `crew out`
  steps out whoever is in the crew.
- **The hazard's text** changes to the Sourmire's line.

**New scene steps** (README §2): `phase`, `light` (the green glow, the amber and green hands, the gold draining
from the comb), `still` (`celebi_vision`, with its tear), `pose` (hands on the lid, kneel), `choice` (both reply
beats, with the quiet set), `crew out` and `crew in`, step-on triggers (scene 5, scene 7, H1), flag triggers (scene
4, H3), a scene played by a Psynergy event (scene 9), and Pell, Celebi, Rowlet, the Wingull, the queen and the
foragers as actors scenes can move.

**Checks.** `tools/mission5_check` follows the new flow, both with Vesper in the crew and without: the arrival,
Sorrel's reply menu in both voices, the bridge, the Sourmire's three pillars and its sting, the way up the root
wall, the vision, the order's reply menu, the seal refusing Move before the order and taking it after, Cut and the
bush, the root-way, the village at night and `m5_done`; then that the next rest starts the right interlude. A
second check walks the Hive: closed without `m6_pilot`, caught on lit comb, the Halt crossing, the queen and the
chest.
