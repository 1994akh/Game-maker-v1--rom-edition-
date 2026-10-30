# Mission 6: Lantern Reef

> **Status:** draft for your yes or notes (18 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 6, §4 (Mimikyu) and §9a (Maestro Bonewhistle, the lantern Litwick). Today's
> build: [mission-6-build.md](../../design/mission-6-build.md). The clock: [day-night-clock.md](../../design/day-night-clock.md).

| | |
|---|---|
| Mission | 6, Lantern Reef (Act I) |
| Plays after | Mission 4's letter on Canalport's jetty ([mission-04.md](mission-04.md), scene 15): Vesper waits on Canalport's beach from `m4_done`. **Either order with mission 5** ([mission-05.md](mission-05.md)): it plays the same before or after it |
| Crew | {HERO} and the first partner, Maren and Eevee, Marill in a Set; Sorrel and Rowlet too if mission 5 came first (`m5_sorrel`). Vesper and Gastly join in scene 1, at the mission's recruit floor (progression 1; L8 proposed), on Mia's curve (progression 8) |
| Rooms | `canalport` (the beach: Vesper's hire), `lantern_reef` (re-clipped larger: Marrit's rock, the Last Bell's bow, waist and stern, the Merrow, the sandbar) |
| Clock | Any phase in Canalport. The first arrival sets dusk. **The decks exist only at night** (day-night-clock.md §2): by day the fog stands like a wall, and the Kestrel's bunk sleeps until night. On the reef the night holds while the crew is there; Marrit's bed rests to dawn |
| Flags in | `m4_done`; `m5_sorrel` if Sorrel is in the crew, and `forest_seal_deepened` for one of her lines |
| Flags out | `m6_pilot`, `m6_intro`, `m6_night`, `m6_bonewhistle`, `m6_plank_bow`, `m6_boom_seen`, `m6_plank_stern`, `m6_mark`, `m6_stash`, `m6_note`, `hm_defog`, `m6_done`; and, optional, `m6_fog_cleared`, `m6_mimikyu_seen`, `m6_mimikyu_2`, `m6_mimikyu_3`, `m6_mimikyu`, `m6_litwick_1`, `m6_litwick_2`, `m6_litwick`, `m6_gloam`, `m6_sapling` |
| Unlocks | Vesper (Shadow, with Gastly) joins, and with her Reveal, Halt and Cloak; Defog (`hm_defog`, a kept HM: a Set Pokémon that can learn it, story.md §7); Lantern Reef on the Kestrel's chart (`m6_pilot`); Mimikyu for the Kin Garden (optional, decision 12) |
| Reply beats | 2: Vesper's price (scene 1); Corvin's note (scene 7) |
| Fights | None in the story. Optional: Mimikyu (`mimikyu_reef`, decision 12) and the lantern Litwick (`lantern_litwick`, the §9a egg). A loss plays "Try again"; both can be fled, and no ball works on Mimikyu. Wild battles on the decks at night |
| Leads into | Crew 1's next rest at an inn or a sanctum plays a Crew 2 interlude (decision 7): mission 7 if this is Crew 1's first recruitment, mission 8 if missions 5 and 7 are done |

**The flow.** On Canalport's beach a fog pilot, Vesper, offers the deputy a lead: a Rimborn skiff went into Lantern
Reef running dark, and came out lighter. For fifty coins she takes the crew north into the fog. The reef is a
graveyard of ships, and by day its fog stands like a wall. At dusk Marrit, the old lantern-keeper, lights her
lanterns for the drowned crews she believes come home at night; at dark the fog lies down and the decks stand up
out of it, full of Ghost Pokémon, and a skeleton maestro conducts a drowned orchestra on the bow. Reveal finds the
planks between the broken Last Bell's three pieces, Halt stops a loose boom, and at the stern a Rimborn chalk mark
shows where Corvin left a note: "Ask your Commodore where the tithe goes." The job's done, and Vesper stays on, for
the same rate, to be there when the deputy asks.

**Either order.** Nothing here needs mission 5. Where Sorrel is in the crew (`m5_sorrel`), she has a few lines of her
own and a seedling on the bow will take her Growth; where the Forest seal is deepened, she has one more line at the
note. Each such line is marked *Sorrel in the crew* in place and listed under "Either order", below.

## Scenes

### 1. The fog pilot

- Room: `canalport`, the beach behind the dike. Trigger: talking to Vesper (slot 16), once `m4_done`, unless
  `m6_pilot` (today's `vesper_pilot`, rewritten).

*On the beach behind the dike, a woman sits on an upturned boat, mending a storm lantern: tall, in grey oilskins
with the hood down, her near-black hair tied back, a pilot's spyglass on a cord round her neck. A Gastly hangs in
the boat's shadow and grins at nothing. She doesn't stop mending.*

**Vesper:** You're the deputy. The one
hunting the seal-breaker.

Whole jetty knows. You're not quiet
people.

*[face Vesper → {HERO}] [crew out]*

**Vesper:** Vesper. Fog pilot.

There's a reef in the north fog.
Lantern Reef. A graveyard of ships.
Nobody goes in but me.

A while back a skiff went in there
running dark. Rimborn rig, by the
sail. It came out lighter.

**Maren:** Lighter. It left something
behind.

**Vesper:** People don't sail into a ghost
reef to leave nothing.

Fifty coins, and I take you in. The
ghosts don't give credit, and
neither do I.

**{HERO} replies:**

1. "Fifty it is." · quiet: (Nod)

   **Vesper:** A client who doesn't haggle.
   I'll try not to get attached.

2. "That's steep." · quiet: (Shake head)

   **Vesper:** So's the reef. Fifty, or you
   swim. Nobody swims the reef.

3. "Why so much?" · quiet: ...

   **Vesper:** Fog's dear this season. And I'm
   the only pilot who comes back
   out.

*Every reply rejoins here.*

*With 50 coins or more: [take_coins 50]*

**System:** {HERO} paid 50 coins.

*With fewer: [take_coins: the whole purse]*

**System:** {HERO} paid every last coin.

**Vesper:** That's not fifty. I don't give
credit. I keep a tab. A very good
tab.

*Then, either way:*

**Vesper:** For the job, I'm crew. After
that, we'll see.

*[recruit vesper] Vesper and Gastly join the crew.*

**System:** Vesper joined the crew!

**Vesper:** Shadow's my Psynergy. I see
what's hidden. I stop what moves.

And nobody sees me unless I let
them.

Lantern Reef's on your chart now.
I drew it in. Don't let your mate
rub it out.

We go in at dark. Bring a light, and
don't listen to the singing.

*Sorrel in the crew:*

**Vesper:** A forest girl. You'll hate the
reef.

**Sorrel:** I hate most places. I'll manage.

*[crew in] [flag m6_pilot] Control returns. Lantern Reef is on the Kestrel's chart.*

### 2. Into the fog

- Room: `lantern_reef`, Marrit's rock. Trigger: entering, unless `m6_intro` (today's `reef_arrival`, rewritten).

*Over black, before the fade:*

**Narration:** The water went grey under the
Kestrel, and the sun with it.

Then came the fog. Vesper took the
helm, and for an hour nobody said a
word.

*[phase dusk] [fade in 40] A rock in the fog, with a stone hut on it and a rack of storm lanterns by its door. The
Kestrel ties up at its little quay. All round, the fog stands up out of the sea like a wall, grey and close, and
through it, here and there, the dark bones of ships: masts, ribs, a broken bowsprit. Somewhere in it, a bell rings
once.*

*[crew out]*

**Vesper:** Lantern Reef. Every ship the
north fog ever ate.

**Maren:** It's a wall. We can't go in
through that.

**Vesper:** Not now. Day fog stands up.
Night fog lies down. We go in at
dark.

*The hut's door opens. An old woman comes out with a long pole and a box of matches, and stops dead at the sight
of them. [show Marrit] [emote Marrit: exclaim]*

**Marrit:** Vesper. You've brought
Tidewardens. To my reef. At dusk.

**Vesper:** Paying ones, Marrit.

**Marrit:** Paying ones. Well.

Marrit. I keep the lanterns. Every
dusk I light them, so the crews can
find their way home.

The crews that went down here. They
come back at night, to their ships.
You'll see them.

Don't raise a hand to them unless
they raise one first. Then put
them back to sleep. Gently.

**Maren:** The crews. You mean Ghost
Pokémon?

**Marrit:** That's what they'd like you to
think.

*[walk Marrit → the lantern rack] She starts taking the lanterns down, one by one.*

*Sorrel in the crew:*

**Sorrel:** All this wood, and not one bit of
it alive.

**Vesper:** Nothing grows on the reef.

**Sorrel:** Something always grows.

*[crew in]*

**Tully:** She's tied up, Deputy. There's a
bunk below, if you'd sooner sleep
till dark.

*[flag m6_intro] Control returns. The decks open at night (puzzle 1).*

### 3. The lanterns

- Room: `lantern_reef`. Trigger: the room at night (entering at night, or waking from the bunk at night), once
  `m6_intro`, unless `m6_night`.

*[phase night] [fade in 30] Night. Marrit stands at the end of her rock with her pole, lighting the last lantern
on the rack. [light: lantern gold]*

*Out in the reef, one by one, lanterns kindle on the wrecks by themselves: on masts, on rails, in empty windows.
[light: one gold point after another, out across the reef] The fog sighs and lies down flat on the water,
knee-high, and the ships stand up out of it: a great three-master broken in three on the rocks, an old gangway
running from the rock to her bow, and a small black hull beside her waist.*

*Small cold lights drift among the wrecks. On the broken ship's bow, music starts: a drum, a bottle, a bell, and a
voice that isn't quite singing. [emote Gastly: smile]*

**Marrit:** There. The crews are home.

**Vesper:** There. Now it's a reef.

*[crew out]*

**Vesper:** That's the Last Bell, broken in
three. The skiff tied up at her
stern. Whatever it left is there.

The planks between her pieces are
still there. You just can't see
them. That's what Reveal's for.

And the water's all teeth. Nobody
swims the reef. Not even your
Marill.

**Maren:** And the music?

**Vesper:** Don't listen to the singing.

*Sorrel in the crew:*

**Sorrel:** Something's growing on that bow.
I can feel it from here.

*[crew in] [flag m6_night] Control returns. The gangway to the bow is open. While the crew is on the reef, the night
holds (Changes to the build).*

### 4. The drowned orchestra

- Room: `lantern_reef`, the Last Bell's forecastle. Trigger: talking to Maestro Bonewhistle, unless
  `m6_bonewhistle` (the egg's staged scene, decision 10).

*On the bow's forecastle, a ghost orchestra plays. A Shuppet drums on a barrel. Two Gastly blow across the necks of
bottles. A Duskull rings the ship's bell, once a bar, very solemnly. Before them, on an upturned crate, stands a
tall skeleton in a tattered frock coat and a battered tall hat, conducting with a fishbone. He stops mid-beat, and
turns. [emote Bonewhistle: exclaim]*

**Bonewhistle:** Visitors! Living ones! It has
been ages. Literally. Ages.

Maestro Bonewhistle, late of the
Rumbelow, now of the drowned
orchestra. Delighted!

You'll forgive my looks. I've
been a little thin since the
wreck.

Ha! A bone joke. I have plenty.
Two hundred and six, at last
count.

May I see your Pokédex?

*[yes/no] (the mirror's yes/no; no flag)*

- Yes:

  **Bonewhistle:** Oh! ...Oh, you haven't actually
  got one. How sad. I'd weep, if I
  had the eyes for it.

- No:

  **Bonewhistle:** Quite right. Never show a
  skeleton your Pokédex. We're
  terribly nosy.

*Then, either way:*

**Bonewhistle:** We play every night for the fog.
We only know one song. It's a long
one. Fifty years, so far.

I used to play the violin. The sea
took it, the night we sank.

Somewhere out there, someone is
still waiting for me to play it.
I can feel it in my bones.

All of them. Bone joke!

*[emote Bonewhistle: smile] He turns back to his orchestra and raises the fishbone. The Duskull rings the bell.
[flag m6_bonewhistle] Control returns.*

### 5. The waist

- Room: `lantern_reef`, the Last Bell's waist. Trigger: stepping off the bow plank onto the waist (a step-on spot),
  unless `m6_boom_seen`.

*The Last Bell's waist: a long deck tilted toward the sea, its rails gone, a lantern on the mainmast. Across the
middle of the deck a loose cargo boom swings back and forth on its own, creaking, sweeping the planks clear. [camera
→ the boom] [camera back] [crew out]*

**Vesper:** Loose boom. It swings like it's
still got a crew.

Halt it, and walk past while it's
thinking about it.

**Maren:** And if it hits us?

**Vesper:** Then you'll be busy, medic.

*[crew in] [flag m6_boom_seen] Control returns.*

### 6. The Rimborn mark

- Room: `lantern_reef`, the Last Bell's stern. Trigger: stepping off the stern plank onto the stern (a step-on
  spot), unless `m6_mark`.

*The Last Bell's stern: a high deck with the rudder house at its back, its door nailed shut. On the rudder house
wall someone has chalked a mark: a wave over a line. Below it, a crate is wedged against a low locker. Fresh rope
burns scar the rail where a skiff tied up. [crew out]*

**Vesper:** Rimborn chalk. A wave over a
line. "Something kept here."

**Maren:** You read Rimborn?

**Vesper:** I read anything that tells me
where the rocks are.

*[crew in] [flag m6_mark] Control returns.*

### 7. Corvin's note

- Room: `lantern_reef`, the stern. Trigger: the crate moved aside (`m6_stash`, puzzle 4).

*The crate grinds aside. Behind it the locker door swings open: inside, a roll of oilskin tied up with knots, and a
small bottle. [crew out]*

**{HERO}:** That's Corvin's knot.

*Quiet: [emote {HERO}: exclaim] and no line.*

*{HERO} unties it and reads.*

**Note:** {HERO}. If you're reading this,
you hired a fog pilot. Good. Pay
them well. They're worth it.

I'm not here. I was, for a night.
The Rimborn hide in this fog when
the Holdfast is out hunting.

I opened the Flame Well. A great
bird came out of it, grey as ash,
and screaming.

Something had been hurting it for
a long time. It looked at us as if
we were the ones.

The monks pay their tithe in fire.
Forty braziers this year. Ten,
once. Their flame kept shrinking.

I'm not asking you to forgive me.
I'm asking you one thing.

Ask your Commodore where the tithe
goes.

The Elixir is for you. You never
pack one.
C.

*[give Elixir] [flag m6_note]*

**System:** {HERO} received Elixir!

*[emote Vesper: squint]*

**Vesper:** Your friend gets around. And
he's not wrong to ask.

**Maren:** The tithe goes to the Pinnacle.
Everybody knows that.

**Vesper:** And after the Pinnacle?

*[emote Maren: silence] [wait 20]*

**Maren:** ...That's the Pinnacle's
business.

*Sorrel in the crew:*

**Sorrel:** They take our seed every autumn.
Cartloads. I've never once seen
where it goes.

*Sorrel in the crew, and the Forest seal deepened (`forest_seal_deepened`):*

**Sorrel:** And we buried a seal on the
Commodore's order. Ask her about
that while you're asking.

*[face Vesper → {HERO}]*

**Vesper:** Well, deputy? Going to ask your
Commodore?

**{HERO} replies:**

1. "I'll ask her." · quiet: (Nod)

   **Vesper:** Tell me what she says. I could
   use a laugh.

2. "Ilse has her reasons." · quiet: (Shake head)

   **Vesper:** Loyal. Fine. Loyal is how a
   thing goes on for six hundred
   years.

3. "Where does it go?" · quiet: ...

   **Vesper:** Somewhere it never comes back
   from. I knew an island that wouldn't
   pay. It isn't there any more.

   *[wait 30]*

   **Vesper:** Never mind. Old weather.

*Every reply rejoins here.*

*Maren has her notebook out, and is writing.*

**Vesper:** Writing it down, medic?

**Maren:** I write everything down. It's
for my report.

**Vesper:** Who reads your reports?

*[wait 30]*

**Maren:** ...The order.

**Vesper:** Back to the boat. Marrit will
want her lanterns counted.

*[crew in] [fade out 30] [warp lantern_reef, entrance 1 (the lantern house door)] Straight on to scene 8.*

### 8. Vesper stays

- Room: `lantern_reef`, Marrit's rock. Trigger: straight on from scene 7.

*[fade in 30] The rock, still at night. Marrit sits on the step of her lantern house, counting the lights across
the reef with one finger. The Kestrel creaks at the quay. [crew out] Vesper walks to the end of the rock and looks
out at the fog, her back to the crew.*

**Vesper:** Job's done. You're in, you're
out, and you've got your note.

That was the deal.

*[wait 30] [face Vesper → {HERO}]*

**{HERO}:** Stay with us.

*Quiet: [pose {HERO}: nod] and no line.*

**Vesper:** I was going to. Don't let it go
to your head.

Same rate. I'll send you the bill.

Somebody ought to ask your
Commodore where it goes. I'd like
to be there when you do.

And since I'm staying: any Pokémon
of yours with wings, I'll show it
how to sweep fog.

Fog's only weather that's lost its
nerve. You just shoo it.

*[flag hm_defog]*

**System:** Now you can Defog! Use it where
fog hides the way, if a Set
Pokémon can learn Defog.

*Sorrel in the crew:*

**Sorrel:** Rowlet has wings.

**Vesper:** Rowlet has opinions. We'll see.

*Then, in every crew: [walk Marrit → beside the door]*

**Marrit:** You're taking Vesper? Good. She's
been on this reef too long. Talks
to the crews like they're friends.

Bed's made inside, if you want it.
A coin in the lantern box. That's
the price.

*[crew in] [flag m6_done] Control returns. Marrit's lantern house is a restoration point; Crew 1's next rest at an
inn or a sanctum plays the next Crew 2 interlude (decision 7). Until the crew rests, the night holds, and the decks
are still there: the Defog banks, the Merrow, Mimikyu and the Litwick.*

## The optional finds

### M1. Something at the bow

- Room: `lantern_reef`, the bow's tip. Trigger: Reveal there (Mimikyu's first spot, `m6_mimikyu_seen`, as built).

*At the very tip of the bow, Reveal's light falls on a small heap of ragged cloth: a lumpy costume with a crooked
face drawn on it, very, very still. It is trying hard to be something else. [show Mimikyu]*

*[wait 30] [emote Mimikyu: exclaim] It knows it's been seen. It shuffles round in a circle, then scurries off aft
along the rail, much faster than anything that shape should. [walk Mimikyu fast → off aft] [hide Mimikyu]*

*[crew out]*

**Vesper:** A Mimikyu. Shy ones. It wants
you to like it. It just doesn't
want you to look.

**Maren:** It went aft. There's a thread
caught on the rail.

*[crew in] Control returns.*

### M2. Under the sailcloth

- Room: `lantern_reef`, the waist, by the mainmast. Trigger: Reveal on the sailcloth heap (`m6_mimikyu_2`), once
  `m6_mimikyu_seen`.

*Under a heap of old sailcloth by the mainmast, Reveal shows a crooked drawn face peeping out. [show Mimikyu]
[emote Mimikyu: sweat] It bolts across the deck to the west rail, and runs straight out along the swinging spar
toward the black hull. [walk Mimikyu fast → the Merrow] [hide Mimikyu]*

*[crew out]*

**Vesper:** Onto the Merrow, over the spar.
It's showing you the way.

*[crew in] Control returns.*

### M3. The lantern locker

- Room: `lantern_reef`, the Merrow. Trigger: Reveal on the lantern locker (`m6_mimikyu_3`), once `m6_mimikyu_2`.

*In the Merrow's lantern locker, among the broken glass, a ragged costume sits with its drawn face to the wall.
Reveal's light falls on it, and it turns round, slowly. It has had enough of hiding. [show Mimikyu] [emote Mimikyu:
anger]*

*[crew out]*

**Vesper:** It wants a fight. Give it a good
one, and it'll trust you.

*[crew in] [battle mimikyu_reef]*

*A Poké Ball thrown in this fight isn't used up (decision 12: it joins with no ball):*

**System:** Mimikyu ducks under its costume.
The ball bounces off.

*Fleeing works, and leaves Mimikyu in the locker, ready to fight again.*

*If the fight is lost, "Try again" plays and the fight restarts as it began. Vesper's line as it restarts:*

**Vesper:** Again. It isn't angry. It's
lonely. There's a difference.

*Won (the fight's `scene_after`):*

*The costume droops. Mimikyu shuffles up to {HERO} and holds out one ragged little paw. [emote Mimikyu: heart]*

*[give_pokemon Mimikyu, L9, to the Kin Garden] [flag m6_mimikyu]*

**System:** Mimikyu joined! It was sent to
the Kin Garden.

*[crew out]*

**Vesper:** It'll like a garden. Lots of
places to hide.

*[crew in] Control returns.*

### L. The lantern Litwick

- Room: `lantern_reef`, the waist's mainmast. Trigger: talking to the Litwick, three times (the §9a egg).

*The first time (`m6_litwick_1`; afterwards its row stands one plank nearer the crew's path):*

**Sign:** A Litwick flickers in an old
lantern on the mainmast. It seems
content.

*The second time (`m6_litwick_2`; its row moves one plank nearer again):*

**Sign:** The Litwick's lantern is one plank
closer than it was. It seems
content.

*The third time:*

**Sign:** The Litwick is right beside you.
It has been, for a while.

*[emote Litwick: smile] [battle lantern_litwick]*

*The fight's lines, in its message bar at the start of each round (`[round N]`):*

*[round 1]*

**System:** The Litwick takes a step closer.

*[round 2]*

**System:** The Litwick takes another step.

*[round 3]*

**System:** The Litwick is very close now.

*[round 4]*

**System:** The Litwick raises its lantern...

*Fleeing works in this fight, and leaves the Litwick by the crew's path, where it waits:*

**System:** The Litwick doesn't follow. It's
in no hurry.

*If the fight is lost, "Try again" plays and the fight restarts as it began. Maren's line as it restarts:*

**Maren:** Burns, and a lot of them. Heal
first, {HERO}. Then don't let it
get close.

*Won (the fight's `scene_after`):*

*The Litwick floats back up to its hook and settles into its lantern. Under the hook, something glints. [flag
m6_litwick] [give Psy Crystal]*

**System:** {LEADER} found Psy Crystal!

**Sign:** The Litwick seems content. It
seems very content.

### G. The Merrow's carving

- Room: `lantern_reef`, the Merrow's stern. Trigger: examining the carving, the first time (`m6_gloam`).

*On the black hull's stern, a carving: a lantern with an eye in its flame. Vesper puts her palm flat on it, and
stands there. Gastly goes very still in her shadow. [crew out] [wait 40]*

**Vesper:** Old rig. Westgloam built.

They don't build them any more.

*[crew in] [flag m6_gloam] Control returns.*

### S. The seedling (Sorrel in the crew)

- Room: `lantern_reef`, the bow's foremast. Trigger: Growth on the seedling (`m6_sapling`).

*The seedling in the rotten foremast stirs. A green vine runs up the mast, round and round, to the crow's nest.
[gate: the vine's cells open] [emote Rowlet: smile] [crew out]*

**Sorrel:** Something always grows. Even
here.

**Vesper:** Hm.

*[crew in] Control returns.*

## People and signs, by room

### `canalport` (Vesper's hire)

Mission 3's "after the sluice" lines hold for everyone else, with these:

- **Vesper**, slot 16, cell (27,16), on the beach behind the dike, from `m4_done` until `m6_pilot`: scene 1. She is in
  the crew from then on.

- **Captain Rufio Maize**, at the jetty's root. From `m6_pilot`, his talk opens with this page, then goes on to his
  join-my-crew menu as before:

  **Maize:** Your new pilot! I asked her to join
  my crew. She said no. Twice! I like
  her.

- **Harbourmaster Quayle**, slot 10. From `m6_pilot`, before his after-the-sluice lines:

  **Quayle:** A fog pilot, for the reef! I've a
  tide table for everywhere in the
  Calm but the reef.

  Nobody comes back to tell me. Well.
  Vesper does. She won't tell me
  either.

- **Tully**, slot 15, at the jetty. From `m6_pilot`, before the chart:

  **Tully:** Vesper's drawn the reef on my
  chart. In ink. Without asking.

### `lantern_reef`

*The states:* closed (any phase but night: the rock only); the first night (`m6_night`, until `m6_done`); after
(`m6_done`). The decks, everything on them and their wild battles exist only at night. Positions are places in the
re-clipped room.

- **Marrit, the lantern-keeper** (new), at her lantern house door (the inn role: a restoration point). Before the
  rest menu, while the reef is closed:

  **Marrit:** The lanterns go up at dusk. The
  crews come home at dark. Wait for
  dark.

  Sleep here now and you'll sleep
  right through it. Your boat's bunk
  is the thing.

  *The first night:*

  **Marrit:** Mind the crews. Mind the boom.
  And if the singing starts, don't
  listen.

  *After:*

  **Marrit:** Bed's made. A coin in the lantern
  box. That's the price.

  *After resting:*

  **Marrit:** Slept? The lanterns are out.
  They'll go up again at dusk. They
  always do.

- **Tully, the Kestrel's mate**, at the quay (the voyage role). The first line here, until `m6_done`, then mission
  3's chart and bunk:

  **Tully:** The reef opens at dark, Vesper
  says. Bunk below till then? I'll
  wake you.

  *The bunk, at the reef (the clock's skip, decided; Night in place of Dusk here):*

  **Bunk:** A narrow bunk below decks. It
  smells of tar and fog. Sleep
  until...?

  *[menu: Night, Dawn, Not now]*

- **Maestro Bonewhistle** (the egg), on the forecastle, at night. Scene 4, then:

  **Bonewhistle:** Every night, the same song. Fifty
  years. We're nearly at the chorus.

- **The drowned orchestra**, round him, at night:

  **Sign:** A Shuppet drums on a barrel, with
  great feeling and no rhythm at all.

  **Sign:** Two Gastly blow across bottle
  necks. The note is low and sad and
  nearly in tune.

  **Sign:** A Duskull rings the ship's bell,
  once, very solemnly. Then it looks
  at you.

- **The Litwick** (the egg), at the waist's mainmast, at night: L, above. From `m6_litwick`, its last line.

- **Mimikyu**, hidden at night: M1 to M3, above. Its spots, before Reveal, say:

  **Sign:** The very tip of the bow, over the
  fog. Something here is trying hard
  not to be noticed.

  **Sign:** A heap of old sailcloth. A ragged
  thread trails out from under it.

  **Sign:** A lantern locker full of broken
  glass. Something in it sighs.

**Signs and things to examine**

- **The lantern rack**, by the hut. Closed:

  **Sign:** A rack of storm lanterns, cleaned
  and filled, waiting for dusk.

  *At night:*

  **Sign:** The rack is empty. Every lantern
  is out on the reef.

- **The lantern box**, by the door:

  **Sign:** A tin box nailed by the door: FOR
  THE LANTERNS. It rattles.

- **The fog wall** (the gangway's closed line, any phase but night):

  **Sign:** The fog stands up out of the sea
  like a wall. Vesper won't set foot
  in it. Not till dark.

  *Defog on it, from `hm_defog` (nothing changes):*

  **Vesper:** That's not a bank. That's the
  weather.

- **The reef's water**, everywhere off the rock and the decks (no Surf):

  **Sign:** The water churns white over the
  reef's teeth. Marill won't go near
  it.

- **The gangway**, from the rock to the bow, at night:

  **Sign:** An old gangway, hung with Marrit's
  lanterns. It creaks, but it holds.

- **The gaps** where the hidden planks are (puzzle 2), before Reveal:

  **Sign:** Black water between the wrecks.
  The fog over it stirs, as if
  someone just walked across.

  *After Reveal:*

  **Sign:** An old grey plank across the gap.
  Now you've seen it, it stays seen.

- **The Last Bell's bell**, on the forecastle:

  **Sign:** A ship's bell, green with age.
  Its name is cast in the bronze:
  THE LAST BELL.

- **The seedling**, in the bow's foremast, until `m6_sapling`:

  **Sign:** A seedling has taken root in the
  rotten foremast, pale and stubborn.
  Growth might do something with it.

  *From `m6_sapling`:*

  **Sign:** A vine climbs the foremast to the
  crow's nest.

- **The sweeping boom** (puzzle 3):

  **Sign:** A loose boom, swinging across the
  deck on its own.

- **The swinging spar**, at the waist's west rail:

  **Sign:** A long spar swings out over the
  water toward the black hull, and
  back. Out, and back.

- **The chalk mark**, on the rudder house:

  **Sign:** Chalk on the rudder house: a wave
  over a line.

- **The crate** (puzzle 4), until `m6_stash`:

  **Sign:** A Rimborn crate, wedged against a
  low locker. It would slide, with a
  push.

- **The locker**, from `m6_note`:

  **Sign:** The Rimborn locker. Empty now, but
  for a smell of tar.

- **The rudder house door:**

  **Sign:** Nailed shut from the inside.
  Whoever did it was very sure.

- **The rope burns**, on the stern's rail:

  **Sign:** Rope burns on the rail. A skiff
  tied up here once, and left in a
  hurry.

- **The fog banks**, two (the Defog banks), until `m6_fog_cleared`. Before `hm_defog`:

  **Sign:** A bank of fog sits on the deck,
  thick as wool. It won't lie down.

  *From `hm_defog`:*

  **Sign:** A bank of fog, thick as wool.
  Defog would shift it, with a Set
  Pokémon that can learn it.

- **The stern stair**, from `m6_fog_cleared`:

  **Sign:** Steps down the stern to a sandbar.
  It runs back to Marrit's rock.

- **The Merrow's carving**, on the black hull's stern (G, above, the first time). Afterwards:

  **Sign:** A small black hull, built low and
  fast for fog. On its stern, a
  lantern with an eye in its flame.

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| Corvin's locker | The stern, behind the crate (scene 7) | Elixir ×1 | Scene 7's system line |
| The waist chest | The waist, past the sweeping boom (the dungeon's gear chest, items §13) | Travel Robe | The engine's chest line, naming `{LEADER}` |
| The forecastle head | The bow, behind its fog bank (Defog) | Magic Rod (the artifact, items §13's Lantern Reef suggestion) | The engine's chest line |
| The crow's nest | The bow's foremast, up the seedling's vine (Growth, Sorrel in the crew) | 150 coins (a lookout's purse) | **System:** {LEADER} found 150 coins! |
| The Merrow's chest | The Merrow's deck (over the spar, Halt) | Water of Life ×1 (Golden Sun's revival, loot only; built, where the Mist Potion isn't, items §2) | The engine's chest line |
| The Litwick's hook | The waist, after the fight (L) | Psy Crystal ×1 | L's system line |
| Vesper's fee | Scene 1 | Out: 50 coins, or the whole purse | Scene 1's system lines |
| Mimikyu | M3 | Mimikyu, L9, to the Kin Garden (decision 12) | M3's system line |

Open question 19 (a light blade for Vesper as this mission's gear chest) is still open; the Travel Robe is items
§13's suggestion until it's answered.

## Puzzles

The crew's verbs here: {HERO}'s Move and Scoop, Maren's Frost, Surf on Marill (no use on the reef: its water is all
teeth), and Vesper's Reveal, Halt and Cloak from scene 1; Sorrel's Growth when she is in the crew, for one optional
reward; Defog from scene 8, for the optional banks. The main path needs only the verbs every order of play has. The
clock is a puzzle of its own: the decks are there only at night. Pushed things stay where they're pushed, so the
crate can always be got behind again.

**Puzzle 1. Wait for dark (the clock, new).**
1. By day, at dawn and at dusk the fog stands like a wall at the rock's edge, and the gangway is closed.
2. Tully's bunk sleeps until night; walking on the rock until the phase turns works too.
3. At night scene 3 plays the first time, the gangway opens, and the decks, the planks, the booms, the orchestra and
   the wild battles are there. While the crew is on the reef at night, steps don't move the clock, so the night
   never runs out under them. A rest at Marrit's moves it to dawn, and closes the decks again.

**Puzzle 2. The hidden planks (Reveal twice, as built, laid out again).**
1. The Last Bell lies broken in three: bow, waist and stern, with black water between. The gangway reaches the bow.
2. The planks across the two gaps are there but unseen. Cast Reveal at each gap: the bow plank (`m6_plank_bow`) and
   then the stern plank (`m6_plank_stern`) show, and stay found (as built). The gaps' signs hint where to look.

**Puzzle 3. The sweeping boom (Halt, as built).**
1. Across the waist, a loose boom swings from rail to rail (a patrol), and knocks back anyone it meets.
2. Cast Halt on it: it stops for ten seconds (as built). Walk past it to the stern plank and the waist's chest.

**Puzzle 4. The Rimborn stash (Move, new).**
1. On the stern, under the chalk mark (mission 2's "something kept here"), a crate is wedged against a low locker.
2. Stand in front of it and cast Move: it slides aside one cell (`m6_stash`), and scene 7 plays. The stern is open
   round the crate, so it can always be got behind again.

Corvin played the same mark in mission 2's sea caves, so a player who was Corvin there knows it on sight.

**Optional A. The spar to the Merrow (Halt, new).**
1. From the waist's west rail, a long spar swings out over the water to the black hull's rail and back (a patrol
   over the gap's one cell).
2. Cast Halt while its end is over the gap: for ten seconds that cell can be walked, and the crew crosses to the
   Merrow (and back the same way).

**Optional B. The Defog banks (Defog, new).** From `hm_defog`, a crew with a Set Pokémon that can learn Defog clears
the reef's veil and both banks at once (`m6_fog_cleared`, as built): the bow's bank hides the Magic Rod, the
stern's hides the stair down to the sandbar, a short way back to the rock.

**Optional C. The seedling (Growth, Sorrel in the crew).** Cast Growth on the seedling in the bow's foremast: a vine
climbs to the crow's nest (`m6_sapling`, a gate), where a lookout's purse holds 150 coins.

**Optional D. Mimikyu (Reveal three times, decision 12).** Reveal at the bow's tip shows it (M1), and it runs aft;
Reveal on the sailcloth by the mainmast (M2), and it runs over the spar; Reveal on the Merrow's lantern locker (M3),
and it fights, then joins with no ball and goes to the Kin Garden. The third spot needs Optional A, so it is
Golden Sun's kind of hard Djinn.

## Eggs

- **Maestro Bonewhistle** (story.md §9a, One Piece's musician), on the bow at night, conducting the drowned orchestra
  with a fishbone. His gags start here: bone jokes ("Two hundred and six, at last count"; "All of them. Bone joke!",
  the original's bent), and "May I see your Pokédex?" as §9a has it. His old ship, the Rumbelow, bends his
  original's. His lost violin and "someone still waiting for me to play it" seed his quest, "The Long Wait" (a whale
  Pokémon that has waited fifty years). His own look, never a copied one: a tall battered hat and a tattered frock
  coat. His talk is a short staged scene (decision 10).
- **The lantern Litwick** (§9a, Final Fantasy's lantern-carrier). It sits content in its lantern and is a plank
  closer every time the crew looks, then fights, edging closer every round and hitting very hard on the fourth.
  Optional, with Flee allowed, and a Psy Crystal under its hook.
- **Mimikyu** (story.md §4, "hides in Lantern Reef, visible only with Reveal"; decision 12): a Djinn-style find, three
  hiding places and a fight, then the Kin Garden.

## Either order: the lines that differ

Everything else plays the same before or after mission 5.

| Where | When | What |
|---|---|---|
| Scene 1 | `m5_sorrel` | Vesper's "A forest girl" and Sorrel's "I hate most places" |
| Scene 2 | `m5_sorrel` | Sorrel's "All this wood", Vesper's "Nothing grows on the reef" and Sorrel's answer |
| Scene 3 | `m5_sorrel` | Sorrel's "Something's growing on that bow" |
| Scene 7 | `m5_sorrel` | Sorrel's line on the seed tithe |
| Scene 7 | `m5_sorrel` and `forest_seal_deepened` | Sorrel's "And we buried a seal on the Commodore's order" |
| Scene 8 | `m5_sorrel` | Sorrel's "Rowlet has wings" and Vesper's answer |
| S | `m5_sorrel` (Growth needs a Forest Adept) | The seedling's vine and its two lines |

The two missions can also interleave: Vesper can be hired, then mission 5 played, then the reef. So every Sorrel line
here stands on its own, and none of them answers a line from an earlier scene she may have missed. In Act I
`forest_seal_deepened` always means Sorrel is in the crew too: she joins before the seal, and crews can't
trade Adepts until mission 10. In every `[crew out]`, Sorrel steps out with the others when she is in the crew.

## Not in this mission

Vesper's Linking Cord (Haunter to Gengar) comes from Nerissa after Bastion Rock (story decision 5); Vesper's
regroup at Gloam Shore is mission 20, which the Merrow's carving and "an island that wouldn't pay" seed;
Bonewhistle's quest, "The Long Wait", and his ghost-ship side room come later (§9a). The words of the Crew 2
interlude that the next rest plays belong to mission 7's and mission 8's pages.

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **Vesper's hire:** her look (grey oilskins, near-black hair, a pilot's spyglass), mending a storm lantern on the
  beach; the lead that brings the deputy north (a Rimborn skiff "came out lighter"); fifty coins, or the whole purse
  and a tab ("I don't give credit. I keep a tab. A very good tab"); "For the job, I'm crew"; "I see what's hidden.
  I stop what moves. And nobody sees me unless I let them"; staying on at "the same rate", with the bill to follow.
- **The voyage:** sailed by the player into the north-west Calm, so the arrival names no days (world-map.md §1.8):
  grey water, then an hour of fog.
- **Lantern Reef:** "every ship the north fog ever ate"; why the decks are night-only, in a pilot's words ("Day fog
  stands up. Night fog lies down"); the water "all teeth", so nobody swims it; the lanterns kindling on the wrecks by
  themselves; the Last Bell, a three-master broken in three, and its bell rung by a Duskull; the Merrow, a small
  black Westgloam fog-runner; the sandbar.
- **Marrit, the lantern-keeper,** and the reef's culture of the dead (story.md §9's "Ghost Pokémon feared as the
  dead"): she lights the lanterns every dusk so the drowned crews can find their ships, tells the crew to put them
  back to sleep gently, and believes the "Ghost Pokémon" story is what the dead want you to think. Her lantern house
  as the reef's restoration point, priced "a coin in the lantern box".
- **The night holding on the reef,** so the decks never vanish under the crew.
- **Corvin's note**, in full: the fog pilot "worth it", the Rimborn hiding in the reef from the Holdfast, Ho-Oh
  "grey as ash, and screaming", Embral's forty braziers against ten, the Elixir "you never pack", left in a Rimborn
  stash under mission 2's chalk mark and tied with his knot.
- **Maren and Vesper at the note:** "The tithe goes to the Pinnacle. Everybody knows that." "And after the
  Pinnacle?"; "Who reads your reports?" "...The order." A seed for mission 9's confession that names nobody.
- **Vesper's past, hinted only:** "I knew an island that wouldn't pay. It isn't there any more. Never mind. Old
  weather" (the Tidewardens drowning the Gloam island, story.md §4, never said outright); the Merrow's
  carving, a lantern with an eye in its flame, "Westgloam built. They don't build them any more" (seeds for her
  regroup at Gloam Shore, mission 20); Marrit's "She's been on this reef too long".
- **Defog from Vesper:** "Fog's only weather that's lost its nerve. You just shoo it"; "Rowlet has opinions".
- **Bonewhistle's details:** the Rumbelow, the drowned orchestra (Shuppet, two Gastly, a Duskull), the fifty-year
  song "nearly at the chorus", the lost violin; "Never show a skeleton your Pokédex. We're terribly nosy" (the
  answer to no: the original's question is bent to the Pokédex by §9a, and the answer keeps it a bone joke, with no
  innuendo).
- **The Litwick's field gag** (a plank closer each time it's examined) and its four round lines.
- **Mimikyu's three spots** (the bow's tip, the sailcloth, the Merrow's lantern locker), Vesper's "It isn't angry.
  It's lonely", its level, L9 (proposed: progression.md §6 leaves Djinn-style levels open), and the ball that bounces
  off its costume.
- **Canalport's new lines:** Maize turned down twice, Quayle's missing tide table, Tully's inked chart.
- **The rewards:** Elixir ×1, a Travel Robe and the Magic Rod (items §13's suggestions), 150 coins, Water of Life ×1
  and a Psy Crystal.
- **Corvin's note** says the Forgeheart's flame "kept shrinking", not that it is half as tall: it went out with
  Ho-Oh (mission 4) before he wrote.

## Changes to the build

**Rooms**
- **`lantern_reef`** re-clipped larger from Golden Sun 1's ship rooms (room 109 and its neighbours, the builder's
  pick), with painted sea, to hold: Marrit's rock (her lantern house, the lantern rack and box, the quay with the
  Kestrel; entrance 0 at the quay, entrance 1 at the lantern house door), the gangway to the bow (closed by a gate
  at any phase but night, with the fog wall's line), the Last Bell's bow (the forecastle with the orchestra, the
  foremast with the seedling and its climb gate to the crow's nest, the bow's tip, the forecastle head's bank and
  chest), the bow plank (as built), the waist (the sweeping boom, the mainmast with the Litwick's three places, the
  sailcloth, the chest past the boom, the west rail with the spar), the stern plank (as built), the stern (the rudder
  house, the chalk mark, the crate and locker, the stern bank over the stair), the Merrow west of the waist (the
  carving, the lantern locker, its chest), and the sandbar back to the rock. The reef's water is never on the surf
  layer. Step-on spots at the waist's and the stern's heads.
- **`canalport`:** `vesper_pilot` rewritten as scene 1, with a coins condition; new opening pages for Maize, Quayle
  and Tully from `m6_pilot`.

**Actors and engine**
- **Night-only rows and gates** (day-night-clock.md §2, decided): every deck row, the planks, the booms, the
  orchestra, Mimikyu and the Litwick carry `{"show": "phase", "phase": "night"}`; the gangway is a gate open only at
  night; the decks' encounter zone has a night list only, and the rock has none.
- **The night holds on the reef** (new): a room key, proposed `"clock_hold": "night"`, so steps in `lantern_reef`
  don't advance the clock while it is night. A rest or the bunk still sets it.
- **Scene 3's trigger** fires when the room is at night (on entering, or when the phase turns while in it), once
  `m6_intro`.
- **The bunk at the reef** offers Night in place of Dusk (clock decision 3's skip; the reef's own menu).
- **Marrit's row** is an inn: a restoration point at one coin, "a coin in the lantern box" (an invention: her own
  price, below items §12's inn ladder).
- **The note's row** (slot 11) becomes the crate and locker: `m6_stash` plays scene 7; `m6_note`, the Elixir and the
  reply menu are in it; `hm_defog` and `m6_done` move to scene 8. Today's `scene_after` lines, and the two `when`
  steps that switch to crew 2 for mission 7 or 8, come out.
- **The handover moves out** (decision 7): the interlude starts from the rest hook (an inn's or a sanctum's menu
  closing) once `m6_done` is set, and Crew 1 resumes at that restoration point. Vesper's recruitment in Canalport
  doesn't count: the hook keys on `m5_done` and `m6_done`, never on `m6_pilot`.
- **A coins condition** for scene 1: a `when` on the purse holding 50, and `take_coins` of the whole purse otherwise,
  with the two system lines.
- **The spar as a bridge** (new): while a halted patrol actor stands on a gap cell, that cell can be walked.
- **Mimikyu:** one hidden actor whose row moves between three spots by flag, each found by Reveal and each playing a
  scene; its fight, `mimikyu_reef` (a single Mimikyu, L9, proposed) with "Try again" and Flee allowed; a thrown ball
  isn't used up and shows its line (as Ho-Oh's in mission 4), so it can never be caught with one; `give_pokemon`
  straight to the Kin Garden with the storage line, never into a Set.
- **Vesper's class** shows decision 18's Shadow names (Shade first, then Fogrunner, Gloamcaller, Nightwarden, Umbral
  Sage) over Mia's curve (progression 8), in place of the placeholder Water Seer line (`placeholder_class` in
  `adepts.json` comes off).
- **The Litwick:** three rows, one per place, chosen by `m6_litwick_1` and `m6_litwick_2`; its fight,
  `lantern_litwick` (a Litwick at L13, proposed, whose strongest move lands on round 4, tuned in slice 10 so a crew
  at L9 using Psynergy wins about half the time), with the `[round N]` lines, Flee allowed (a trainer flag), its flee
  line, Maren's retry line, and a Psy Crystal on the win.
- **Bonewhistle's scene** with the mirror's yes/no and no flag, as mission 3's Maize.
- **Defog** (as built) also hides the two bank rows on `m6_fog_cleared`; Defog on the fog wall gives Vesper's line
  and sets nothing.
- **Lines for a crew member who may not be there:** Sorrel's lines are `when` steps on `m5_sorrel` (one also on
  `forest_seal_deepened`), and `crew out` steps out whoever is in the crew.
- **Marrit, the orchestra (Shuppet, two Gastly, the Duskull), Mimikyu, the Litwick, Gastly and Rowlet** as actors
  scenes can move, with the expansion's overworld sprites at 2× (decision 28).

**New scene steps** (README §2): `phase`, `light` (lantern gold, the lanterns kindling across the reef), `camera`,
`pose` (nod), `choice` (both reply beats, with the quiet set), `crew out` and `crew in`, `[round N]`, step-on
triggers (scenes 5 and 6), a phase trigger (scene 3), flag triggers (scene 7, M1 to M3, S), coins in a condition.

**Checks.** `tools/mission6_check` follows the new flow, both with Sorrel in the crew and without: the hire with a
full purse and a light one, Vesper's reply menu in both voices, the reef closed at dusk, the bunk to night, the
lanterns, the two planks, the boom, the crate, the note's reply menu in both voices, the stay, `hm_defog` and
`m6_done`; then that the next rest starts the right interlude and that the decks are gone at dawn. A second check
walks the finds: the spar, Mimikyu's three spots and its fight into the Kin Garden (a thrown ball bounces off), the
Litwick's three talks and its fight (won, and fled), the banks, and the seedling only with Sorrel.
