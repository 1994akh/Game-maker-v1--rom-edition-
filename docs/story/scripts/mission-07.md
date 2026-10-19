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
| Clock | The rest sets dawn for Crew 1; the handover sets night for Crew 2; night through the break-in; dawn at the cave mouth, and Crew 1 wakes at dawn |
| Flags in | `m5_done` or `m6_done`; `m5_sorrel` and `m6_pilot` for Crew 1's lines in the hand-back |
| Flags out | `m7_started`, `m7_intro`, `m7_beacon`, `m7_tunnel`, `m7_jail_intro`, `m7_passage`, `m7_cover`, `m7_key`, `m7_cell_open`, `m7_freed`, `m7_ledger`, `m7_alarm`, `m7_sluice`, `m7_caves_in`, `m7_holm`, `m7_boom_lit`, `m7_boom`, `m7_done`, `m7_letter`; and, optional, `m7_strand_dug`, `m7_flagstone`, `m7_magikarp`, `m7_store`, `m7_locker`, `m7_cave_stash` |
| Unlocks | Nerissa (Sea, with Froakie) joins, and with her Frost, Ply and **Douse** (new, built for the boom: decision 6's "whatever Nerissa brings"); Surf for crew 2 (Froakie, under mission 3's `hm_surf`); the Linking Cord in crew 2's bag (story decision 5: Vesper's, usable once the bags merge at mission 10); the word "Crown" for crew 2 |
| Reply beats | 2, Corvin's (README §3): Nerissa's question in her cell (scene 8); Nerissa's question at the ledger (scene 9) |
| Fights | Lieutenant Holm (`bastion_holm`, new) on the cave landing. A loss plays "Try again" |
| Leads into | Crew 1 resumes where it rested, with Ilse's letter (scene 16). Mission 8 plays at Crew 1's next rest after its second recruitment |

**The flow.** The next time Crew 1 rests at an inn or a sanctum after its first recruitment, the story crosses to
Corvin's crew. The Rimborn lanes say the Tidewardens are holding a diver of the Deep Shelf at Bastion Rock, the
order's sea fortress in the west Calm, because she knows the way to Silverdeep. Corvin wants the way. By night Tamsin
lights the fortress's cold beacon so the wall sentry stares out to sea, and Corvin digs under the wall by the
sea-gate. In the cells the crew slips past a patrolling guard and blinds the duty sergeant with a pushed crate, takes
the cell keys and frees Nerissa, who has kept her Froakie in her cell's drain all month: it isn't on the register, so
the sergeant says it isn't a Pokémon. In the records office the tithe ledger lists the Calm's fire, rain, seed and
stone, "shipped on, all, to the Crown", with no column for anything coming back. Corvin tears out the page. The bells
ring: the tunnel is found. Down the cistern into the sea caves, Lieutenant Holm stops them on the landing, loses, and
fires the boom across the cave mouth; Nerissa's Douse puts it out, and Froakie carries them out to Ketch at dawn.
Crew 1 wakes where it rested, to a letter from Ilse.

## Scenes

### 1. The handover

- Room: wherever Crew 1 rests. Trigger: the rest hook (decision 7): an inn's or a sanctum's rest menu closing,
  once `m5_done` or `m6_done`, unless `m7_started`. A bunk or the home bed doesn't count.

*The rest's fade holds on black. The innkeeper's after-rest line is held back until Crew 1 returns (Changes to the
build).*

**Narration:** {HERO} slept. Far to the west,
in the dark of the Calm, a Rimborn
skiff was running without lights.

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

*[crew out] Tamsin steps out beside Corvin, and Riolu beside Larvitar. Ketch stays in the skiff with the oars.*

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

A month ago some Rimborn came down
to Pearlhollow asking for it. A man
in a coat made of old sails.

**Corvin:** ...Hask.

**Nerissa:** He didn't give a name. I said no.
Then the Tidewardens came, and they
didn't ask.

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
to the commandant. Every night, a
month. I learned it like a song.

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

{HERO} cuts that stone. Every
summer, out of Brann's quarries.

*[wait 20] Corvin runs a finger down the page, then across it, then down again.*

**Corvin:** Received. Shipped on. Where's the
column for what comes back?

**Nerissa:** There isn't one. I listened every
night for a month.

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

**Nerissa:** I've been in here a month. I could
have used you a month ago.

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

I've listened to them for a month.
It's good to see them.

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

- Room: `bastion_caves`. Trigger: winning the fight (Holm's `scene_after`).

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

*[fade in 40] Dawn, where Crew 1 rested. The innkeeper's after-rest line plays (it was held back). Then a Wingull
finds the crew, as Wingulls always do, and lands at Maren's feet with a letter tube on its leg. [show Wingull]
[crew out]*

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

*[crew in] [flag m7_letter] Control returns. Crew 1 plays on from where it rested.*

