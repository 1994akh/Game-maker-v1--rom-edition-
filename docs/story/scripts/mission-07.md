# Mission 7: Bastion Rock

> **Status:** draft for your yes or notes (19 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 7, §4 (Nerissa) and §9 (Bastion Rock: licensed, registered Pokémon only).
> Today's build: [mission-7-build.md](../../design/mission-7-build.md).

| | |
|---|---|
| Mission | 7, Bastion Rock (Act I; the first Crew 2 interlude) |
| Plays after | Crew 1's first recruitment (mission 5 or 6, either order), at Crew 1's next rest at an inn or a sanctum (demo decision 7; story.md §14 Q1) |
| Crew | Corvin (at his L8 floor, progression 1) and Larvitar, Tamsin and Riolu, with crew 2's own bag; Nerissa (L8) and Froakie join in scene 8 |
| Rooms | Wherever Crew 1 rests (the handover and the hand-back); `bastion_shore` (re-clipped: the strand and the sea-gate); `bastion_jail` (re-clipped larger: the cistern landing, the cell corridor, the guard passage, the key room, the records office, the seized-goods store); `bastion_caves` (new: the sea-cave escape, decision 5) |
| Clock | The rest sets dawn for Crew 1; the handover sets night for Crew 2; night through the break-in; dawn at the cave mouth, and Crew 1 wakes at dawn; Ilse's letter comes later that morning (day) |
| Flags in | `m5_done` or `m6_done`; `m5_sorrel` and `m6_pilot` for Crew 1's lines in the hand-back |
| Flags out | `m7_started`, `m7_intro`, `m7_beacon`, `m7_tunnel`, `m7_jail_intro`, `m7_passage`, `m7_cover`, `m7_key`, `m7_cell_open`, `m7_freed`, `m7_ledger`, `m7_alarm`, `m7_sluice`, `m7_caves_in`, `m7_holm`, `m7_boom_lit`, `m7_boom`, `m7_done`, `m7_letter`; and, optional, `m7_strand_dug`, `m7_flagstone`, `m7_magikarp`, `m7_pen`, `m7_store`, `m7_locker`, `m7_cave_stash` |
| Unlocks | Nerissa (Sea, with Froakie) joins, and with her Frost, Ply and **Douse** (new, built for the boom: decision 6's "whatever Nerissa brings"); Surf for crew 2 (Froakie, under mission 3's `hm_surf`); the Linking Cord in crew 2's bag (story decision 5: Vesper's, usable once the bags merge at mission 10); the word "Crown" for crew 2 |
| Reply beats | 2, Corvin's (README §3): Nerissa's question in her cell (scene 8); Nerissa's question at the ledger (scene 9) |
| Fights | Lieutenant Holm (`bastion_holm`, new) on the cave landing. A loss plays "Try again" |
| Leads into | Crew 1 resumes where it rested, with Ilse's letter (scene 16). Mission 8 plays at Crew 1's next rest after its second recruitment |

**The flow.** The next time Crew 1 rests at an inn or a sanctum after its first recruitment, the story crosses to
Corvin's crew. The Rimborn lanes say the Tidewardens are holding a diver of the Deep Shelf at Bastion Rock, the
order's sea fortress in the west Calm, because she knows the way to Silverdeep. They took her in the Calm, where
she had come up under the storm to trade. Corvin wants the way. By night Tamsin
lights the fortress's cold beacon so the wall sentry stares out to sea, and Corvin digs under the wall by the
sea-gate. In the cells the crew slips past a patrolling guard and blinds the duty sergeant with a pushed crate, takes
the cell keys and frees Nerissa, who has kept her Froakie in her cell's drain all month: it isn't on the register, so
the sergeant says it isn't a Pokémon. In the records office the tithe ledger lists the Calm's fire, rain, seed and
stone, "shipped on, all, to the Crown", with no column for anything coming back. Corvin tears out the page. The bells
ring: the tunnel is found. Down the cistern into the sea caves, Lieutenant Holm stops them on the landing, loses, and
fires the boom across the cave mouth; Nerissa's Douse puts it out, and Froakie carries them out to Ketch at dawn.
Crew 1 wakes where it rested, and later that morning a letter from Ilse finds it.

## Scenes

### 1. The handover

- Room: wherever Crew 1 rests. Trigger: the rest hook (decision 7): an inn's or a sanctum's rest menu closing,
  once `m5_done` or `m6_done`, unless `m7_started`. A bunk or the home bed doesn't count.

*The rest's fade holds on black. The innkeeper's after-rest line is held back until Crew 1 returns (Changes to the
build).*

**Narration:** {HERO} slept. Out in the west
Calm, in the dark, a Rimborn skiff
was running without lights.

It came in under a rock the order
built to keep things in. The
sailors call it Bastion Rock.

*[phase night] [crew 2] [flag m7_started] [warp bastion_shore, entrance 0] Crew 1 is recorded where it rested, and
resumes there in scene 16.*

### 2. Bastion Rock

- Room: `bastion_shore`. Trigger: entering, unless `m7_intro` (today's `bastion_arrival`, rewritten).

*[fade in 40] Night under Bastion Rock: a wall of dressed black stone rising straight out of the sea, its towers lost
in the dark, a lantern here and there along the wall walk. At its foot a narrow strand of shingle runs east to the
sea-gate, two iron leaves taller than a mast, chained shut for the night. A lamp on a post beside the gate throws a
ring of light across the strand. West of the landing, on a spur of rock, stands a cold iron beacon. Ketch's skiff
noses onto the shingle at the strand's west end.*

*[crew out] Tamsin steps out beside Corvin, and Riolu beside Larvitar. Ketch stays in the skiff with the oars and a
bag of ship's biscuit.*

**Ketch:** Bastion Rock. Every Rimborn who
ever sailed dark has a bad story
about this rock.

I've got four. I'm saving them for
the song.

**Corvin:** The diver's in there. The one
from the Deep Shelf.

**Tamsin:** The one who knows the way to
Silverdeep. You said. Twice.

**Corvin:** The Sea Well is under Silverdeep.
Nobody knows the way down but the
divers of the Shelf.

The order took one of them a month
ago, Ketch says. For knowing it.

**Ketch:** That's what the lanes say. The
lanes are never wrong. Mostly.

*[camera → the wall walk over the lamp] A Tidewarden sentry stands on the wall walk above the lamp, looking straight
down at the lit strand. [camera back] [face Tamsin → the wall]*

**Tamsin:** One sentry, over the lamp. He's
watching the light. Anything that
crosses it, he sees.

**Corvin:** And the soft ground by the
sea-gate is on the far side of the
light. Of course it is.

*[emote Corvin: idea] [face Corvin → the beacon]*

**Corvin:** Tamsin. That beacon. What does a
fortress do when its beacon lights
up in the middle of the night?

**Tamsin:** Looks out to sea, for whatever
lit it.

...Oh. Ha! Eight out of ten.

**Ketch:** I'll stay with the boat. Come back
running, and I'll be rowing. Don't
come back, and I'll be singing.

*[crew in] [rest point] [flag m7_intro] Control returns. The beacon and the soft ground are puzzle 1.*

### 3. The beacon

- Room: `bastion_shore`, the spur. Trigger: Blaze on the beacon (`m7_beacon`, puzzle 1).

*Tamsin points two fingers at the beacon's iron basket. Fire catches in the tarred wood and roars up, orange against
the night. [light: orange flare on the spur] On the wall walk, a shout. The sentry runs to the parapet's west end
and stares out to sea, his back to the strand. [hide the sentry over the lamp] [show the sentry at the west parapet]
Lanterns gather beside him.*

**Sentry:** The beacon's lit! Is there a
ship? Who lit it?

**Second sentry:** Nobody's out there. Is anybody
out there? Hello?

*[crew out]*

**Tamsin:** They're all looking at the sea. Go,
Landslide. Before they work out the
sea didn't do it.

*[crew in] [flag m7_beacon] Control returns. The lit strand is safe to cross.*

### 4. Under the wall

- Room: `bastion_shore`, by the sea-gate. Trigger: Scoop on the soft ground (slot 8, `m7_tunnel`, as built; puzzle
  1).

*[pose Corvin: dig] Corvin digs. The wet earth slides away under his hands, and keeps sliding, down and in under the
footings of the wall. Larvitar helps with its head. [shake 20, 1] [wait 40] A dark hole opens under the stones.*

**Corvin:** Soft as porridge. The sea's been
washing out under this quay for a
hundred years.

*[crew out]*

**Tamsin:** You dig like a Sandshrew. That's a
compliment. They're very good at
it.

*[crew in] [flag m7_tunnel] Control returns. The hole leads under the wall (the warp, as built).*

### 5. The cells

- Room: `bastion_jail`. Trigger: entering, unless `m7_jail_intro` (today's `jail_arrival`, rewritten).

*[fade in 30] The tunnel comes up through a broken flagstone into the cistern landing: a low vault of wet stone, with
an iron grate in the floor over black water and a sluice gurgling somewhere under it. East, a doorway opens on the
cell corridor: a long passage lit by wall lamps, cell doors along its north side, each set back in a deep stone
doorway. A guard in Tidewarden blue walks the corridor from end to end with a lantern, slowly, as if he has done it
every night of his life. [crew out]*

**Corvin:** One guard, walking the row. He
sees straight ahead of him, and
nothing else.

When he walks away, follow him.
When he turns, get in a doorway.

**Tamsin:** And if he sees us?

**Corvin:** Then we come back down this hole
and try it quieter.

*Larvitar puts its head into the tunnel, and pulls it back out. [emote Larvitar: sweat]*

**Corvin:** Larvitar would rather we didn't.

*[crew in] [flag m7_jail_intro] Control returns. The corridor is puzzle 2.*

### 6. The sergeant

- Room: `bastion_jail`, the corridor's east end. Trigger: stepping onto the last cell before the guard passage (a
  step-on spot), unless `m7_passage`.

*The corridor ends at the guard passage, which runs north to the key room and the records office. At its south end,
behind a desk with a brass bell and a register as thick as a loaf, sits a sergeant with a moustache like a yard
broom, looking straight up the passage. He doesn't blink. Anyone crossing to the north end would walk right through
his gaze. [camera → the desk] [camera back] [crew out]*

**Tamsin:** That one doesn't walk. He just
looks.

**Corvin:** Right up the passage, where we
have to cross. And the keys are at
the other end.

*[face Corvin → the bay] Beside the passage, in a bay off the corridor, stands a laundry crate.*

**Corvin:** He can't see through a crate.
Nobody can see through a crate.

**Tamsin:** I've never tried.

*[crew in] [flag m7_passage] Control returns. The crate is puzzle 3.*

### 7. The keys

- Room: `bastion_jail`, the key room. Trigger: talking to the key board (slot 9, `m7_key`, today's quest role).

*A narrow room lined with hooks, a label under every hook in a neat hand. One heavy ring hangs on a hook labelled
CELLS. [crew out]*

**Tamsin:** "Cells." Very helpful. Thank you,
whoever you are.

*[pose Tamsin: reach] She lifts the ring off its hook and pockets it.*

**System:** Tamsin took the cell keys.

*[crew in] [flag m7_key] Control returns.*

### 8. Nerissa

- Room: `bastion_jail`, the last cell, at the passage's north end. Trigger: talking to the cell door (slot 10,
  today's `cell_door`) with `m7_key`; the scene runs on into Nerissa's (slot 11, `nerissa_joins`, rewritten).
  Before the keys, the door and the voice behind it (People and signs).

*The key turns. [flag m7_cell_open] The door swings in on a stone cell: a cot, a bucket, a slit of window too high
to see from, and a drain in the floor that breathes cold salt air. A woman sits cross-legged on the cot with her
eyes shut: a diver's white wrap, wavy hair tied back with a cord, very still. She doesn't open them.*

**Nerissa:** Four of you. One walks like a
landslide. One walks like she's
about to hit someone.

And two have very small feet.

**Tamsin:** Ha! She's got you, Landslide.

**Nerissa:** You're not the night watch. The
night watch walks like a man who
hates his boots.

*[face Nerissa → Corvin] She opens her eyes.*

**Nerissa:** Took you long enough. Nerissa.

I'd shake your hand, but I've been
in here a month.

**Corvin:** Corvin, of Fallhaven. And this
is Tamsin.

**Nerissa:** The seal-breaker. The guards talk
about nothing else. You burned down
a monastery.

**Tamsin:** A bird burned it. We were
standing near it.

**Corvin:** We heard the order took a diver
who knows the way to Silverdeep.

**Nerissa:** Everyone wants the way to
Silverdeep. That's why I'm in here.

This spring some Rimborn came to
Coralreach, over our domes, asking.
A man in a coat made of old sails.

**Corvin:** ...Hask.

**Nerissa:** He didn't give a name. I said no.
Then I came up under the storm to
trade in the Calm. Divers do.

The Tidewardens took me on the
quay. They didn't ask.

"Knowledge of restricted waters."
That's the charge. I know where the
water is. It's a crime now.

*[wait 20]*

**Nerissa:** So, seal-breaker. What do you
want with the way?

**Corvin replies:**

1. "To open its seal."

   **Nerissa:** Honest. The man in the sail coat
   said the same. With more teeth.

2. "Nothing, yet."

   **Nerissa:** "Yet." A short word with a long
   tail on it.

3. "To get you out."

   **Nerissa:** Kind. Nobody does anything for
   nothing. But kind.

*Every reply rejoins here.*

**Nerissa:** Then here are my terms. Get me
out. One day, get me home to
Pearlhollow.

And I'll think about the way. Only
think. I'm a slow thinker. Divers
are.

**Corvin:** Deal.

**Nerissa:** Good. Froakie.

*A Froakie climbs up out of the drain, shakes the water off its head and sits on her knee. [show Froakie] [emote
Froakie: smile] [emote Riolu: exclaim] [emote Larvitar: question]*

**Nerissa:** My partner. It lives in the drain.
The drain runs to the sea, and
Froakie runs with it.

The sergeant checked his register.
There's no Froakie in it. So it
isn't a Pokémon.

He says it's a frog. He's half
right.

*[recruit nerissa] Nerissa and Froakie join the crew.*

**System:** Nerissa joined the crew!

*Nerissa stands and stretches, slowly, like someone coming up from a long way down. [crew out]*

**Tamsin:** They didn't take your knife? You
look like somebody who has a knife.

**Nerissa:** They took my purse. They looked
for a knife. They didn't look very
hard.

They keep what they take in a store
off the corridor. My purse is in it.
I'd like it back.

And on the way out, read their
ledger. Next door. The clerk reads
it aloud every night.

*[crew in] [flag m7_freed] Control returns.*

### 9. The ledger

- Room: `bastion_jail`, the records office. Trigger: talking to the tithe ledger (slot 12), once `m7_freed`,
  unless `m7_ledger`. Before `m7_freed`, the ledger's line (People and signs).

*The records office: shelves of ledgers bound in blue up to the ceiling, and a lectern under a lamp turned low, with
a ledger open on it. [crew out]*

**Nerissa:** Every night the clerk reads this
to the commandant, through that
wall. I learned it like a song.

*Corvin turns the ledger to the lamp, and reads.*

**Ledger:** THE ELEMENT TITHE OF THE CALM.
Received at Bastion Rock, this
season.

Embral: fire. Forty braziers.
Canalport: rain. Two hundred
barrels.

The Greenwild: seed and sap. Thirty
carts. Marrow Isle: quarry stone.
Four hundred blocks.

Shipped on, all. To the Crown.

*[emote Tamsin: exclaim]*

**Tamsin:** Forty braziers. That's the
Forgeheart. That's our fire.

**Corvin:** And Marrow Isle. Quarry stone.

{HERO} cuts it. So did I, once.
In Dunstan's quarry.

*[wait 20] Corvin runs a finger down the page, then across it, then down again.*

**Corvin:** Received. Shipped on. Where's the
column for what comes back?

**Nerissa:** There isn't one. I listened for
it every night.

**Tamsin:** What's the Crown?

**Corvin:** I don't know. Not in the lanes.
Not on any of Sael's charts.

I left {HERO} a question, on
Lantern Reef. Where does the tithe
go?

*[face Corvin → the ledger]*

**Corvin:** To the Crown. Wherever that is.

*[face Nerissa → Corvin]*

**Nerissa:** Now you know where it goes. What
will you do about it?

**Corvin replies:**

1. "Find the Crown."

   **Nerissa:** Then you'll want a chart with it
   on. I've seen a lot of charts. None
   of them had a crown.

2. "Tell Sael."

   **Nerissa:** Your captain? Good. Tell somebody
   old enough to be frightened.

3. "Tell {HERO}."

   **Nerissa:** The deputy you keep talking
   about. Will they listen?

   **Corvin:** Always. Then they do what they
   think is right. It's very annoying.

*Every reply rejoins here.*

*Corvin tears the page out of the ledger, folds it small and puts it inside his coat.*

**Corvin:** Proof.

*[flag m7_ledger] [shake 30, 2] Far above, a bell starts to ring, deep and fast. Then another. [emote Corvin, Tamsin,
Nerissa, Larvitar, Riolu and Froakie: exclaim]*

**Tamsin:** That's for us.

**Nerissa:** That's the strand bell. They've
found your hole.

**Corvin:** It was a very good hole.

*Boots on stone. Out in the corridor the patrolling guard runs past, toward the fortress stair. [walk the guard fast
→ off] [hide the guard] At the desk, the sergeant rings his own bell, slaps his register shut and runs after him.
[walk Pruitt fast → off]*

**Pruitt:** Everybody to the strand! And
somebody register that hole!

*[hide Pruitt]*

**Nerissa:** Not the way you came in. There'll
be lanterns all over the strand by
now.

Down. The cistern runs out to the
sea. Froakie comes and goes that way
every night.

*[crew in] [flag m7_alarm] Control returns. The corridor is empty, and the tunnel is closed (People and signs).*

### 10. The sluice

- Room: `bastion_jail`, the cistern landing. Trigger: talking to the cistern grate, once `m7_alarm`, unless
  `m7_sluice`.

*The cistern grate, rusted into the floor. Under it, black water runs away into the dark with a sound like
breathing. [crew out]*

**Nerissa:** Froakie fits through that. We
don't.

**Tamsin:** Stand back.

*[pose Tamsin: strike] [shake 20, 2] Tamsin hits the grate with the heel of her hand, once, then again. The rusted
bars burst out of the stone and drop into the water with a splash. [hide the grate] [emote Riolu: smile]*

**Tamsin:** Four out of ten. It was rusty.

**Nerissa:** Where were you a month ago?

*[crew in] [flag m7_sluice] [warp bastion_caves, entrance 0]*

### 11. The sea caves

- Room: `bastion_caves` (new). Trigger: entering, unless `m7_caves_in`.

*[fade in 30] The sea caves under Bastion Rock: a long throat of black rock. The cistern's outflow falls in a white
rope into a pool, and the pool runs away north as a channel toward a grey blur of open sea. The sea comes in and
goes out with a slow boom that shakes the walls. Along the east side a ledge of rock runs down past a stone landing,
where a stair comes down from the fortress above. Far down the channel, across the cave mouth, a line of black barrels
rides the swell on a chain. [crew out]*

**Nerissa:** The sea caves. Every wave in the
west Calm comes in here to shout.

I've only ever heard them. It's good
to see them.

*Froakie hops into the pool and paddles a circle, waiting. [emote Froakie: smile]*

**Nerissa:** Froakie will carry us out. It knows
the way. It's swum it every night.

**Corvin:** What are the barrels?

**Nerissa:** The boom. Tar barrels on a chain.
If a boat runs for the mouth, they
light it.

Nobody's ever run for the mouth.

**Tamsin:** Somebody is now.

*[crew in] [flag m7_caves_in] Control returns. The water steps are on the landing.*

### 12. The lieutenant

- Room: `bastion_caves`, the landing. Trigger: stepping onto the landing (a step-on spot), unless `m7_holm`. The
  ledge from the pool reaches the water only at the landing's steps, so the crew always meets her.

*Lantern light comes down the fortress stair at a run. A young officer in a Tidewarden lieutenant's coat jumps the
last three steps onto the landing, a lantern held high, and plants herself between the crew and the water steps. A
Wingull lands on her shoulder. A Spheal flops down at her feet. [show Holm] [walk Holm fast → the water steps]*

**Holm:** Halt! In the name of the Pinnacle!

Lieutenant Holm, of the Bastion
watch. You're all under arrest.
And that frog.

**Nerissa:** It isn't on your register.

**Holm:** Then I'll register it! Right after
I've arrested it!

*[emote Holm: anger] [emote Wingull: anger] [emote Spheal: anger] [crew out]*

**Tamsin:** Ha! I like her. Can I hit her?

**Corvin:** Gently.

*[crew in] [battle bastion_holm]*

*If the fight is lost, "Try again" plays and the fight restarts as it began. Nerissa's line as it restarts:*

**Nerissa:** Again. Slower, this time. Let her
spend herself first.

### 13. The boom

- Room: `bastion_caves`. Trigger: winning the fight (Holm's `scene_after`; the win sets `m7_holm`).

*Holm's Spheal rolls onto its back, done. Holm backs up the first steps of the stair, breathing hard, her lantern
still held high. [walk Holm → the stair's foot]*

**Holm:** You'll never get out past the
boom. Nobody does!

*She hurls the lantern down the channel. It turns over and over in the air and lands among the barrels at the cave
mouth. [light: orange flare at the cave mouth] With a thump the tar catches, and the whole boom goes up, a wall of
fire across the channel from rock to rock. [shake 30, 2] Smoke rolls along the roof. [walk Holm fast → up the stair]
[hide Holm]*

**Holm:** Ring the bell! They're in the
caves!

*[crew out]*

**Tamsin:** She set the sea on fire. Now I
like her even more.

**Corvin:** Can Froakie swim through that?

**Nerissa:** No. But it can take me close.

And I can make it stop burning.

*[face Nerissa → the boom] [crew in] [flag m7_boom_lit] Control returns. The boom waits for Douse (puzzle 4).*

### 14. Rain

- Room: `bastion_caves`, the channel before the boom. Trigger: Douse on the boom (`m7_boom`, puzzle 4).

*[crew out] Nerissa lifts both hands from Froakie's back. Under the cave roof a small grey cloud gathers out of the
smoke and the spray, darkens, and opens. [light: grey; the firelight dimming] Rain hammers down on the boom. The fire
hisses, spits and goes out, barrel by barrel, in a great white cloud of steam. [hide the fire]*

**Tamsin:** I set things on fire. I've never
seen anybody un-set one.

That's ten out of ten. I hate it.

**Nerissa:** Douse. It's not much use in a
cell. It's very good in a fire.

*[crew in] [flag m7_boom] Control returns. The channel is open to the cave mouth.*

### 15. Ketch

- Room: `bastion_caves`, the cave mouth. Trigger: surfing into the mouth, once `m7_boom` (today's sea warp on
  `bastion_shore`, moved here and rewritten).

*[phase dawn] Past the steaming boom the cave opens on a grey sea under the first light of dawn. Ketch's skiff bobs
just outside, its sail half up. [show the skiff] Ketch stands up in it, waving both arms.*

**Ketch:** There you are! I saw the fire, and
I thought, that'll be Tamsin.

**Tamsin:** It wasn't me. For once.

**Ketch:** In you get. Who's this? Hello!
Mind the nets. Mind the song. I've
written a prison verse.

*They climb into the skiff. Froakie hops in last and sits on the bow. [hide the crew] Behind them the bells of
Bastion Rock are still ringing. [fade out 40]*

**Narration:** Ketch ran the skiff north into
the fog, where no Tidewarden ship
likes to follow.

*Over black:*

**Corvin:** The Crown. Nerissa, have you ever
heard of it? Anywhere?

**Nerissa:** Not in the sea. And I know most
of the sea.

**Ketch:** If it's on a chart anywhere, it's
for sale at the Tradewind Bazaar.
Everything is.

**Corvin:** Then that's where we go next.

**Nerissa:** Pearlhollow is the other way.

**Corvin:** I know. One day. I promised.

**Nerissa:** You did. I'll remember it for
you.

*[wait 20]*

**Nerissa:** Here. For the crew.

*Nerissa unwinds a cord of braided silk from her wrist, a loop at each end.*

**Nerissa:** A linking cord. Pearlhollow divers
tie one between them on the long
drops.

Some Pokémon change when they're
tied to someone. A Haunter, they
say. A Kadabra. Never a Froakie.

Keep it. One day somebody's Pokémon
will want it more than mine does.

*[give Linking Cord]*

**System:** {LEADER} received the Linking
Cord!

*[flag m7_done] [phase dawn] [resume crew 1] Crew 1 plays again where it rested.*

### 16. Ilse's letter

- Room: wherever Crew 1 rested. Trigger: Crew 1 resuming there, once `m7_done`, unless `m7_letter` (mission 4's
  enter scene on resuming, played in whatever room Crew 1 rested in).

*[fade in 40] Dawn, where Crew 1 rested. The innkeeper's after-rest line plays (it was held back). [fade out 20]
[phase day] [fade in 20] Later that morning a Wingull finds the crew, as Wingulls always do, and lands at Maren's
feet with a letter tube on its leg. [show Wingull] [crew out]*

**Maren:** The Commodore's seal again. It's
for you, Deputy.

*{HERO} breaks the seal and reads.*

**Letter:** Deputy. Bastion Rock was broken
last night: the order's own
fortress, in the west Calm.

The seal-breaker went in under the
walls, and out again under them, by
the sea caves.

He took a prisoner of the order with
him: a diver of the Deep Shelf, held
on the Pinnacle's warrant.

He tore a page out of the fortress's
tithe ledger. I cannot think why.

He has a Rimborn pilot, a monk of
the Forgeheart, and now a Sea
Adept. He is building a crew.

The Pinnacle will set a price on
him. Leave him to the fleet, and
hold to your own work.

I. Graymantle, Commodore. Aboard
the Holdfast.

*[walk Wingull → off] [hide Wingull]*

**Maren:** Bastion Rock. Nobody has ever got
out of Bastion Rock. Not in the
order's whole history.

**{HERO}:** He isn't running. He's looking for
something.

*Quiet: [emote {HERO}: question] and no line.*

**Maren:** A page of a tithe ledger. What
would anyone want with that?

*Vesper in the crew (`m6_pilot`):*

**Vesper:** Somebody wants to know where the
tithe goes. That makes two of us.

*Sorrel in the crew (`m5_sorrel`):*

**Sorrel:** They write our seed in a book like
that. Every autumn. I've never seen
the book.

*Then, in every crew:*

**Maren:** The tithe goes to the Pinnacle.

*[wait 20]*

**Maren:** ...Hold to our own work, she says.
So we hold to it.

*She folds the letter away, takes out her notebook and writes a line. She doesn't say who it's for.*

*[crew in] [flag m7_letter] Control returns. Crew 1 plays on from where it rested.*

## People and signs, by room

### Where Crew 1 rests

No lines of its own. The handover (scene 1) and the letter (scene 16) play there, and the innkeeper's after-rest
line from that one rest is held back until the letter. Every inn's other lines are its own page's (missions 1 to 6).

### `bastion_shore`

*The states:* before the beacon (until `m7_beacon`); after the beacon (`m7_beacon`). Crew 2 leaves by the sea caves
and never comes back, and Bastion Rock is on neither ship's chart in the demo, so nothing is written for after the
break. Positions are places in the re-clipped room.

- **Ketch**, in the skiff at the strand's west end: crew 2's restoration point, free (as Fen's inn in mission 2).
  Before the beacon:

  **Ketch:** Light the beacon, and they all look
  at the sea. Clever. I'd have thought
  of that. Eventually.

  *After the beacon:*

  **Ketch:** Go on, while they're busy looking
  at nothing. I'll be here. Probably.

  *Then, in both:*

  **Ketch:** A nap in the boat? I'll keep
  watch. And eat. Quietly.

  *[menu: Rest, Pokémon, Not now] (the inn's menu, at no charge)*

  *After resting:*

  **Ketch:** You snored. I sang over it. The
  sentry never heard a thing.

- **The sentry**, on the wall walk over the lamp, until `m7_beacon`: a guard row with no patrol, facing down across
  the lit strand (range 4), out of reach. From `m7_beacon` a second row stands at the parapet's west end facing out
  to sea, and the first hides. No lines but scene 3's and the caught steps.

- **The shore's caught steps** (the sentry sees the crew in the lamp's light):

  **Sentry:** Who's that on the strand? Lights!
  Lights!

  *[fade out 20] [to_entrance 0] [fade in 20]*

  **Corvin:** He watches the light. We have to
  give him something better to look
  at.

**Signs and things to examine**

- **The fortress sign**, at the landing:

  **Sign:** BASTION ROCK. Property of the
  Pinnacle. No landing. No mooring.
  No exceptions.

- **The licence notice**, beside it:

  **Sign:** NOTICE. All Pokémon on this rock
  shall be licensed and registered.
  By order of the Commandant.

  Unregistered Pokémon will be held
  until registered. Or for ever.

- **The sea-gate:**

  **Sign:** The sea-gate: two iron leaves,
  taller than a mast, chained shut
  for the night.

- **The lamp.** Before the beacon:

  **Sign:** A lamp on a post, throwing a ring
  of light across the strand. Above
  it, the sentry watches the light.

  *After the beacon:*

  **Sign:** A lamp on a post. Above it, the
  wall walk is empty.

- **The beacon**, on the spur. Before Blaze:

  **Sign:** A cold iron beacon on a spur of
  rock, its basket stacked with tarred
  wood. Nobody's lit it in years.

  *After the beacon:*

  **Sign:** The beacon roars. Every lantern on
  the wall is looking out to sea.

- **The soft ground**, slot 8, by the sea-gate, until `m7_tunnel`:

  **Sign:** Soft, wet earth under the quay's
  edge, washed out by the tides.
  Scoop would dig it.

  *From `m7_tunnel`:*

  **Sign:** A hole under the wall. It goes
  down a long way.

- **The strand glint** (optional A), on the shingle west of the light, until `m7_strand_dug`:

  **Sign:** Something glints in the shingle
  where the tide just left it. Scoop
  would dig it out.

- **Ketch's skiff:**

  **Sign:** Ketch's skiff, mast down, oars
  shipped. A coat of patches hangs off
  the bow.

### `bastion_jail`

*The states:* the night (until `m7_alarm`); the alarm (`m7_alarm`): the guard and the sergeant have gone up to the
strand, and the tunnel is closed. Positions are places in the re-clipped room.

- **The guard** (Marine Dobbs, by the roster), slot 8, walking the corridor (patrol and sight as built, range 4).
  Talking to him is never possible: he sees whoever stands in front of him. The room's caught steps (as built,
  rewritten):

  **Guard:** Hey! Who's down there?

  *[fade out 20] [to_entrance 0] [fade in 20]*

  **Tamsin:** Back in the hole. ...Again. Quieter
  this time. Watch which way he's
  facing.

  *From `m7_alarm`:* gone (scene 9).

- **Sergeant Pruitt** (new), at his desk at the guard passage's south end: a guard row with no patrol, facing north
  up the passage (range 4). A pushed block in his line stops his sight (puzzle 3). His own caught steps (Changes to
  the build):

  **Pruitt:** You! Name! Number! Licence!

  *[fade out 20] [to_entrance 0] [fade in 20]*

  **Corvin:** He sees all the way up the
  passage. We need something in his
  way.

  *From `m7_alarm`:* gone (scene 9).

- **Old Tarrant** (new, the egg), behind the bars of a cell on the corridor's north side. The night, until
  `m7_magikarp`:

  **Tarrant:** Psst. You. Not a guard. Good.
  Tarrant. Rimborn, same as you. It's
  in the boots.

  In for unlicensed Magikarp. Forty of
  them. They were going to be a
  surprise.

  Want one? A very special Magikarp.
  Five hundred coins.

  *[wait 20]*

  **Tarrant:** ...Five. Five coins. I'm in no
  position to haggle.

  *[yes/no] (the mirror's yes/no) Yes, with 5 coins or more: [take_coins 5]*

  **System:** {LEADER} paid 5 coins.

  *Yes, with fewer: [take_coins: the whole purse]*

  **System:** {LEADER} paid every last coin.

  *Then, after either:*

  **Tarrant:** Pleasure doing business.

  *He reaches into his bucket and passes a Magikarp through the bars. It flops. [give_pokemon Magikarp, L5, to the
  Kin Garden] [flag m7_magikarp]*

  **System:** Magikarp joined! It was sent to
  the Kin Garden.

  **Tarrant:** Don't tell the sergeant. He thinks
  that's a bucket of water.

  *No:*

  **Tarrant:** Your loss. I'll be here. Eleven
  more years, the sergeant says.

  *From `m7_magikarp`, the night:*

  **Tarrant:** Thirty-nine left. Every one very
  special.

  *The alarm:*

  **Tarrant:** Go on, go! I'll tell them you went
  the other way. For a fee.

- **The registry pen** (new), the first cell on the corridor, by the cistern landing (optional E). Until `m7_pen`:

  **Sign:** A cell full of Pokémon: a
  Zigzagoon, a Wingull and a Psyduck.
  A board on the door:

  AWAITING REGISTRATION. To be held
  at the Commandant's pleasure.

  *From `m7_key`, then:*

  **Sign:** One of the cell keys fits. Open
  the pen?

  *[yes/no] Yes:*

  *The Zigzagoon is gone before the door is fully open. The Wingull follows it, low, toward the cistern. The
  Psyduck stays where it is, holding its head. [hide the Zigzagoon] [hide the Wingull] [flag m7_pen]*

  **Tamsin:** Two out of three. The duck's
  thinking about it.

  *From `m7_pen`:*

  **Sign:** The pen stands open. The Psyduck
  is still thinking about it.

- **Nerissa**, slot 11, in the last cell. Before the keys, the cell door (slot 10):

  **Sign:** A cell door, locked. Through the
  grille, somebody sits very still on
  a cot.

  *Then, from inside:*

  **Calm voice:** If you're the night watch, you're
  early. If you're not, the keys are
  next door.

  *With the keys:* scene 8. From `m7_freed` she is in the crew, and the row hides (as built).

- **The laundry crate**, in the bay beside the guard passage (puzzle 3). Until `m7_cover`:

  **Sign:** A laundry crate full of grey
  blankets. It would slide, with a
  push.

  *From `m7_cover`:*

  **Sign:** The crate sits square in front of
  the desk. The sergeant can see a
  crate. That's all.

**Signs and things to examine**

- **The rules board**, in the cistern landing:

  **Sign:** RULES OF BASTION ROCK.
  1. No talking. 2. No singing.
  3. No unregistered Pokémon.

  4. See rule 1.

- **The duty roster**, by the corridor door:

  **Sign:** NIGHT WATCH. Corridor: Marine
  Dobbs. Desk: Sgt. Pruitt. Strand
  bell: whoever is awake.

- **The sergeant's desk**, from `m7_alarm`:

  **Sign:** THE REGISTER OF BASTION ROCK.
  Every Pokémon on the rock, by
  number. There's no Froakie.

  A brass plate on the desk: SGT.
  PRUITT. HAS NEVER ONCE SLEPT ON
  DUTY.

- **The key board**, from `m7_key`:

  **Sign:** A hook labelled CELLS, empty. The
  other hooks are labelled too. Very
  neatly.

- **The seized-goods store's door** (optional C), on the corridor's south side. Until `m7_key`:

  **Sign:** A door marked SEIZED GOODS.
  Locked.

  *From `m7_key` the door opens (a gate on the flag).*

- **The store's shelves:**

  **Sign:** Seized goods, every one tagged
  UNLICENSED. A fiddle. A fishing rod.
  A barrel of pickled eggs.

- **The evidence chest**, in the store (the dungeon's gear chest), with a tag read before the engine's chest line:

  **Sign:** A long chest, tagged SEIZED FROM
  A PIRATE. EVIDENCE. DO NOT OPEN.

- **Nerissa's locker**, in the store. Before `m7_freed`:

  **Sign:** A locker tagged THE DIVER. A purse
  inside, sealed with the order's
  wax. It isn't yours.

  *From `m7_freed`, until `m7_locker`:*

  **Nerissa:** My purse. Light, but mine.

  *[give coins 120] [flag m7_locker]*

  **System:** {LEADER} received 120 coins!

- **The flagstone** (optional B), in the middle of the corridor's row, until `m7_flagstone`:

  **Sign:** A loose flagstone, a chalk mark
  scratched on it: a wave over a
  line. Rimborn. Something kept.

  *Scoop on it: [flag m7_flagstone] [give coins 60]*

  **System:** {LEADER} found 60 coins!

  **Tarrant:** Oi! That's my... Oh, keep it. I'm
  not going anywhere.

- **The records office's shelves:**

  **Sign:** Ledgers bound in blue, a season to
  a book, back further than anybody
  could count.

- **The tithe ledger**, slot 12. Before `m7_freed`:

  **Sign:** A ledger open on the lectern,
  columns of figures in a neat hand.
  It would take a while to read.

  *From `m7_freed`:* scene 9. *From `m7_ledger`:*

  **Sign:** The tithe ledger. Where this
  season's page was, a torn edge.

- **The cistern grate.** Until `m7_alarm`:

  **Sign:** An iron grate over the cistern.
  Black water runs away under it,
  somewhere, toward the sea.

  *From `m7_alarm`:* scene 10. *From `m7_sluice`, the hole where it was (the warp to `bastion_caves`):*

  **Sign:** The grate is gone. The water runs
  down into the dark, and out.

- **The tunnel**, the warp back to the strand: open until `m7_alarm`, then closed with this line:

  **Sign:** Lanterns, at the far end of the
  tunnel. And voices. Not that way.

- **The drain**, in Nerissa's cell, from `m7_freed`:

  **Sign:** A drain in the floor, breathing
  cold salt air. Froakie's front door.

### `bastion_caves` (new)

*The states:* before the boom burns (until `m7_boom_lit`); burning (until `m7_boom`); out (`m7_boom`). No people
but Holm (scenes 12 and 13). No random battles: the caves are the escape, and Holm is the fight.

**Signs and things to examine**

- **The outfall**, by the pool:

  **Sign:** The cistern's outflow falls into
  the pool in a white rope, loud and
  cold.

- **The fortress stair**, at the landing:

  **Sign:** A stair up into the fortress.
  Boots, a long way up, and bells.

- **The boom.** Until `m7_boom_lit`:

  **Sign:** A boom of tar barrels on a chain,
  rock to rock across the cave mouth.

  *Burning (also the line when Surf meets it):*

  **Sign:** The boom is burning from rock to
  rock. Froakie won't swim near it.

  *From `m7_boom`:*

  **Sign:** Wet black barrels, steaming. The
  way to the sea is open.

- **The tide marks**, on the cave wall:

  **Sign:** Lines of old weed on the rock, one
  above another. The sea comes a long
  way in, here.

- **The chalk mark** (optional D), on the wall above a niche off the ledge:

  **Sign:** Chalk on the cave wall: a wave over
  a line. Rimborn, under the order's
  own fortress.

  **Corvin:** Of course. Of course there's a
  Rimborn stash under Bastion Rock.

- **The wedged rock** (optional D), in the niche, until `m7_cave_stash`:

  **Sign:** A rock wedged into the niche under
  the chalk mark. It would slide, with
  a push.

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| The strand glint | `bastion_shore`, west of the light (Scoop; sets `m7_strand_dug`) | Nut ×1 | **System:** {LEADER} found Nut! (the engine's line) |
| Tarrant's stash | `bastion_jail`, the marked flagstone in the guard's row (Scoop; sets `m7_flagstone`) | 60 coins | The flagstone's lines, above |
| The evidence chest | `bastion_jail`, the seized-goods store (the dungeon's gear chest, items §13) | Bandit's Sword (the artifact items §13 lists for a dungeon chest) | The tag, then the engine's chest line, naming `{LEADER}` |
| Nerissa's purse | `bastion_jail`, her locker in the store, with her in the crew (sets `m7_locker`) | 120 coins (items §12's "Bastion locker") | The locker's lines, above |
| Tarrant's Magikarp | `bastion_jail`, his cell (the egg) | Magikarp, L5, to the Kin Garden, for 5 coins | Tarrant's lines, above |
| The cave stash | `bastion_caves`, the niche under the chalk mark (Move; sets `m7_cave_stash`) | Herb ×2 | The engine's chest line, naming `{LEADER}` |
| Holm's purse | The fight | The fight's coins (a Tidewarden officer's: slice 10 sets them) | The fight's own line |
| The ledger page | Scene 9 | Nothing: a prop Corvin keeps (mission 8 uses it) | — |
| The Linking Cord | Scene 15, from Nerissa (story decision 5) | Linking Cord ×1, into crew 2's bag | Scene 15's system line |

**The Linking Cord's item text** (the Items screen):

**Item:** A Pearlhollow linking cord of
braided silk, a loop at each end.
Some Pokémon change, tied to it.

## Puzzles

The crew's verbs here: Corvin's Move and Scoop, Tamsin's Blaze (decision 6: built), and from scene 8 Nerissa's
Frost, Ply and Douse (new). Surf comes with Froakie: a kept HM under mission 3's `hm_surf`, which crew 2 can use as
soon as a Set Pokémon in it can learn Surf. There is no Halt or Cloak: those are crew 1's. Guards see along their
heading, four cells, unless a wall is in the way (as built); here a pushed block stops them too. Pushed things stay
where they're pushed (slice 4), so every block can always be got behind again, or can't be pushed anywhere useless.

**Puzzle 1. The strand (Blaze, then Scoop; new and as built).**
1. From the skiff at the strand's west end, the strand runs east under the wall to the sea-gate. The lamp lights
   the cells beneath it, from the wall's foot to the water's edge, and the sentry on the wall walk above looks
   straight down them (a guard row, range 4). The soft ground lies east of the light, by the sea-gate.
2. West of the light, on a spur off the strand, stands the cold beacon. Cast Blaze on it: it flares (scene 3,
   `m7_beacon`), and the sentry's row swaps for one at the parapet's west end, looking out to sea.
3. Now the light can be crossed. Cast Scoop on the soft ground: the tunnel opens (scene 4, `m7_tunnel`, as built),
   and the hole is the warp to the cells.
4. Crossing the light before the beacon plays the shore's caught steps: back to the skiff, with Corvin's hint.

It teaches Blaze away from a brazier stair, and a guard's sight before the cells.

**Puzzle 2. The corridor (sight-lines, as built, laid out again).**
1. The cell corridor runs east from the cistern landing. Cell doors line its north side, each set back a cell in a
   deep doorway; on its south side are the store's door and the crate's bay.
2. The guard walks the corridor's row from end to end (as built: a patrol, sight four cells along his heading).
   Doorways are off his row, so he never sees into one.
3. Follow him while his back is turned, and step into a doorway before he turns. There is cover every few cells.
4. Seen, the room's caught steps play: back to the tunnel's mouth, with Tamsin's line.

**Puzzle 3. The sergeant's line (Move, new).**
1. At the corridor's east end the guard passage runs north to the key room, the records office and the last cell.
   Pruitt sits at its south end, facing north, so he sees the cell in front of his desk, the junction with the
   corridor and the two cells beyond it. Every way north crosses his line.
2. In a bay off the corridor, beside the passage, a laundry crate stands one cell west of the cell in front of his
   desk. The bay opens onto the corridor, so the cell west of the crate can be reached without crossing his line.
3. Stand west of the crate and cast Move: it slides east one cell, square in front of his desk (`m7_cover`). His
   sight stops at it (new: a pushed block cuts a guard's line).
4. Now the junction and the passage's north end are safe. The crate can't be pushed again (his desk is behind it
   and the passage wall beside it), and it is never in the way.

It teaches that a guard's line can be cut, not only dodged.

**Puzzle 4. The boom (Douse and Surf, new).**
1. In the sea caves the channel runs from the pool to the cave mouth. Surf on Froakie from the landing's water
   steps, once Holm is beaten.
2. After the fight the boom burns across the mouth (`m7_boom_lit`): a row of burning cells on the surf layer that
   Surf won't enter, with the boom's line.
3. Surf down the channel to within Douse's reach and cast Douse on the boom: rain puts it out (scene 14,
   `m7_boom`), and its cells are water again.
4. Douse is Nerissa's, and the boom only burns after the fight, so nothing can come out of order.

It shows off the new Adept's Psynergy, as the party rules ask of each recruitment (party-and-battle.md §7), and it
is Tamsin's Blaze turned round.

**Optional A. The strand glint (Scoop).** West of the light, on the shingle: Nut ×1 (`m7_strand_dug`).

**Optional B. Tarrant's flagstone (Scoop, in the guard's row).** A loose flagstone with the Rimborn chalk mark
(mission 2's "something kept here") lies in the middle of the corridor's row. Scoop it while the guard's back is
turned: 60 coins (`m7_flagstone`), and Tarrant's line. It is the corridor's risk, for a reward.

**Optional C. The seized-goods store (the keys and Move).**
1. From `m7_key` the store's door opens.
2. Inside, two crates of seized goods stand in a row in front of the evidence chest and Nerissa's locker, with an
   empty corner bay north of the first.
3. Push the first crate north into the corner bay, then the second west into the space it left (`m7_store`). The
   store is laid out so neither crate can be pushed anywhere it can't be got behind again.
4. The evidence chest holds the Bandit's Sword; the locker, with Nerissa in the crew, her purse (`m7_locker`).

**Optional D. The cave stash (Move).** On the ledge under the chalk mark, a rock is wedged in a niche. Move it one
cell aside: the stash holds Herb ×2 (`m7_cave_stash`).

**Optional E. The registry pen (the keys).** From `m7_key` the pen opens to the cell keys: the Zigzagoon and the
Wingull bolt, and the Psyduck stays (`m7_pen`). Nothing is gained but the line; nothing is lost either.

## Eggs

story.md §9a places no egg in mission 7. As mission 2 placed Pip and mission 4 the Elder, one of §9a's unplaced
Pokémon nods fits here and is placed as an invention: **"A suspicious Magikarp salesman"** is **Old Tarrant**, a
Rimborn smuggler jailed for forty unlicensed Magikarp and still selling them through the bars. His opening price is
the original's, bent by the haggle that follows: five hundred coins, then five. The Magikarp is real (L5, to the Kin
Garden), and the sergeant thinks the bucket is water.

## Either order: the lines that differ

Everything in the interlude plays the same after mission 5 or mission 6. Only the hand-back (scene 16) differs:

| Where | When | What |
|---|---|---|
| Scene 16 | `m6_pilot` | Vesper's "That makes two of us" |
| Scene 16 | `m5_sorrel` | Sorrel's "They write our seed in a book like that" |

If Crew 1 finished both recruitments before resting, both lines play, each standing on its own, and mission 8 plays
at the following rest. In every `[crew out]` of scene 16, whoever is in Crew 1 steps out.

## Not in this mission

The way to Silverdeep and Nerissa's home (missions 16 and 18), which her terms seed; Hask's own search for the way
(mission 18); the price Ilse promises (mission 8's posters); the Linking Cord's use (Vesper's Haunter, once the bags
merge at mission 10, whose page can stage the cord changing hands); Crew 1 at Bastion Rock, which isn't on the chart
in the demo; Maren's Douse, which follows the shared Sea list by level once Douse is built.

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **The handover's words,** written for any restoration point ("{HERO} slept. Out in the west Calm..."), with no
  direction from wherever Crew 1 sleeps, and the innkeeper's after-rest line held back until the letter.
- **Why Corvin goes:** the Rimborn lanes' word that the order took a diver who knows the way to Silverdeep, the Sea
  Well's site; Corvin wants the way, and Nerissa's terms are "Get me out. One day, get me home to Pearlhollow. And
  I'll think about the way".
- **Hask at Coralreach:** the Rimborn in a coat of old sails (mission 2's coat) who came asking Nerissa for the way
  this spring; she refused (a seed for the Breakers recruiting at Coralreach, mission 16, and Hask at Silverdeep,
  mission 18).
- **Divers of the Shelf come and go under the Galeway** ("I came up under the storm to trade in the Calm. Divers
  do"), so the order took Nerissa on a Calm quay, on "knowledge of restricted waters". This keeps mission 4's rule
  that the order's ships turn back at the Galeway: they never sailed to Southdeep for her. The order and the
  Breakers both wanted the way, each half right.
- **Bastion Rock:** the strand, the sea-gate, the lamp and the wall sentry, the cold beacon, the soft fill under the
  quay; the cistern landing, the cell corridor with deep doorways, the guard passage, a key room labelled in a neat
  hand, the records office, the seized-goods store, the registry pen and the rules board; the sea caves, the outfall,
  the landing and stair, and the boom of tar barrels that the watch lights against fleeing boats. story.md §9's
  "licensed, registered Pokémon only" becomes the register, the pen and the frog joke.
- **Bastion's people:** Sergeant Pruitt ("Name! Number! Licence!", never once slept on duty), Marine Dobbs on the
  roster, Lieutenant Holm with her Wingull and Spheal, and Old Tarrant (the egg).
- **Nerissa:** her look (a diver's white wrap, wavy hair tied back with a cord); hearing people by their walk;
  "Took you long enough" and "I'd shake your hand" kept from today's build; "I know where the water is. It's a crime
  now"; "a slow thinker. Divers are"; the knife the guards didn't find; Froakie living in her cell's drain, off the
  register; Douse as her first field verb.
- **The tithe ledger:** the Calm's tithe received at Bastion Rock and "shipped on, all. To the Crown": Embral's forty
  braziers (mission 4), Canalport's two hundred barrels of rain (mission 3's notice), the Greenwild's thirty carts of
  seed and sap (mission 5's notice), and **Marrow Isle's four hundred blocks of quarry stone**, the Earth tithe, which
  no earlier page names; no column for anything coming back; Corvin's torn page, kept as proof.
- **Corvin's lines:** "I left {HERO} a question, on Lantern Reef" (mission 6's note, left before this mission in
  either order), "{HERO} cuts it. So did I, once. In Dunstan's quarry" (mission 1's quarry foreman and the
  hero's work), "It was a very good hole", "Then that's where we go next".
- **Tamsin:** the beacon "Eight out of ten", breaking the grate ("Four out of ten. It was rusty"), "I've never seen
  anybody un-set one".
- **Ketch:** his four bad stories about the rock, the prison verse, the skiff as crew 2's free restoration point,
  and the Bazaar as the place every chart is for sale (the seed for mission 8).
- **The Linking Cord** (story decision 5): a Pearlhollow diver's cord, given by Nerissa in the skiff "for the crew",
  with "A Haunter, they say", which points at Vesper's Gastly without naming her.
- **Ilse's letter:** the breakout, the torn ledger page ("I cannot think why"), "He is building a crew", the price
  to come and "Leave him to the fleet"; it comes later the same morning, not at dawn, so a Wingull has had time to
  fly it.
- **Crew 1's lines:** "He isn't running. He's looking for something"; Maren's "Nobody has ever got out of Bastion
  Rock" and her "The tithe goes to the Pinnacle"; Vesper's and Sorrel's lines; Maren writing a line in her notebook
  for no one she names (the reports' thread, missions 5, 6 and 9).
- **Ketch** eating as he waits (a bag of ship's biscuit), as in missions 2 and 4.
- **Lieutenant Holm's fight** on the landing, which story.md doesn't name: the dungeon's one fight, for crew 2's
  EXP and coins (items §12's "interlude fights") and Nerissa's first battle in the crew.
- **The rewards:** Nut ×1, 60 coins, 120 coins (the Bastion locker), the Bandit's Sword, Herb ×2, Magikarp and
  Holm's purse.

## Changes to the build

**Rooms**
- **`bastion_shore`** re-clipped from Golden Sun 1's Kalay Docks (room 107, as today) or a better walled shore, the
  builder's pick: the strand with the skiff's landing (entrance 0) and Ketch's row, the lamp and its lit cells, the
  wall walk with the sentry's two rows, the spur and the beacon, the sea-gate, the soft ground (slot 8) and the
  tunnel's warp, and the strand glint. The sea warp and its escape scene move to `bastion_caves`; entrance 1, back
  from the jail, is used only until `m7_alarm`.
- **`bastion_jail`** re-clipped larger from Golden Sun 2's Madra jail (room 45) and its neighbours: the cistern
  landing (entrance 0, the tunnel's mouth, with the grate and the rules board), the cell corridor with deep doorways
  (the registry pen, Tarrant's cell, two empty cells), the flagstone, the store's door and the crate's bay on its
  south side, the guard passage with Pruitt's desk, the key room (slot 9), the records office (slot 12), the last
  cell (slots 10 and 11) and the seized-goods store with its two crates, chest and locker. The grate becomes a warp
  to `bastion_caves` from `m7_sluice`.
- **`bastion_caves`** (new, decision 5): a sea cave clipped from a Lost Age water dungeon (Aqua Rock or the like,
  the builder's pick) with `--water`: the outfall and the pool (entrance 0, from the cistern), the ledge with the
  chalk mark and the niche, the landing with its water steps and the fortress stair, the channel on the surf layer,
  the boom across the mouth, and the mouth's exit, which plays scene 15. No random battles.

**Actors and engine**
- **The rest hook** (decision 7): scene 1 plays as an inn's or a sanctum's rest menu closes, from a shared events
  file rather than one room (proposed: `maps_src/_interludes/events.json`), on `m5_done` or `m6_done` and unless
  `m7_started`; it holds back that rest's after-rest line. Today's `when` steps at the ends of `celebi_vision`
  (`eldergrove_heart`) and the note's `scene_after` (`lantern_reef`) come out, as missions 5 and 6 ask.
- **A scene on resuming, in any room** (scene 16): from the same shared file, it plays when `resume_crew` returns
  Crew 1, once `m7_done` and unless `m7_letter`, wherever Crew 1 rested, after the held-back after-rest line; its
  `phase day` and fades stand for the morning passing before the Wingull comes.
- **Guards:** a guard row with no patrol (the sentry, Pruitt) keeps one heading; **a pushed block in a guard's line
  stops his sight**, as a wall does (puzzle 3); **caught steps per guard** (the sentry's and Pruitt's own), the
  room's as the default.
- **Douse** on the field (Sea Psynergy, DESIGN.md's Sea list): it puts out a burning actor or burning cells and sets
  their flag (`m7_boom`). Nerissa has it at her join level; Maren follows the shared Sea list. The Douse Drop stays
  its backup item (party-and-battle.md §7).
- **Burning cells on the surf layer:** the boom's cells refuse Surf, with the boom's line, from `m7_boom_lit` until
  `m7_boom`.
- **Nerissa's recruit:** `recruit nerissa` at L8 with Froakie and her kit (a light blade, equipment decision 11),
  on Golden Sun's Sea class line and Summons (Mia's), as decisions 17 and 18 keep Golden Sun's names for the Golden
  Sun elements. She wears Mia's field sprite until art part B2 gives her her LPC look.
- **Corvin's L8 floor** applied when crew 2 starts here (progression 1).
- **Ketch's skiff** as a free restoration point (mission 2's `restoration_price` 0 for Fen's inn).
- **`bastion_holm`** (new): Lieutenant Holm, a Tidewarden Sea Adept at about L9 with a Wingull and a Spheal
  (proposed; slice 10 measures it with `balance_fight` against crew 2 at L8 with Nerissa), "Try again" with
  Nerissa's line, and scene 13 as its `scene_after`.
- **Tarrant's sale:** the mirror's yes/no with mission 6's coins condition, `take_coins 5` or the whole purse, and
  `give_pokemon Magikarp, L5, to the Kin Garden`.
- **Gates and warps:** the store's door and the pen's door open on `m7_key`; the tunnel's warp closes from
  `m7_alarm` with its line; the cistern's warp opens on `m7_sluice`; the beacon's Blaze event swaps the sentry's
  rows.
- **The alarm:** from `m7_alarm` the guard and Pruitt hide, and Tarrant's row says its alarm line.
- **Today's lines replaced:** `bastion_arrival`, `jail_arrival`, `caught`, `cell_door`, `nerissa_joins`, the key
  ring's text, the ledger's text and the sea warp's escape scene.
- **`{LEADER}`** in the give, chest and coin lines (mission 2's).
- **Froakie, Larvitar, Riolu, Ketch, the two sentries, Holm's Wingull and Spheal, the pen's Pokémon and Tarrant's
  Magikarp** as actors scenes can move.

**New scene steps** (README §2): `phase`, `light` (the beacon's flare, the boom's fire, the rain's grey), `camera`,
`pose` (dig, reach, strike), `choice` (Corvin's two beats, with no quiet set), `crew out` and `crew in`, step-on
triggers (scenes 6 and 12), Psynergy-flag triggers (scenes 3, 4 and 14), and the rest-hook and resume triggers
(scenes 1 and 16).

**Checks.** `tools/mission7_check` follows the new flow twice, from a rest at the Mossbed after mission 5 and from
Marrit's lantern house after mission 6: the handover, the strand caught before the beacon and safe after it, the
tunnel, the corridor caught and safe, the crate cutting Pruitt's line, the keys, both reply menus, the recruit, the
ledger and the alarm, the tunnel closed after it, the grate, Holm and her retry line, the boom refusing Surf until
Douse, the cave mouth, the Linking Cord in crew 2's bag, and Crew 1 back where it rested, with the letter.
