# Mission 4: The Forgeheart

> **Status:** draft for your yes or notes (18 Oct 2026). Format and rules: [README.md](README.md). Beats:
> [story.md](../story.md) §7, mission 4, and §5 (Ho-Oh). Today's build:
> [mission-4-build.md](../../design/mission-4-build.md).

| | |
|---|---|
| Mission | 4, The Forgeheart (prologue; the Flame site) |
| Plays after | Mission 3's jetty scene, which switches to crew 2 ([mission-03.md](mission-03.md), scene 10) |
| Crew | Corvin (at his L7 floor, progression 1) and Larvitar, with crew 2's own bag; Tamsin (L7) and Riolu join in scene 6 |
| Rooms | `forge_hall` (re-clipped larger: the gate court, the great hall, the stone court and the ash court), `forge_sanctum` (re-clipped longer: the Well stair and the seal chamber), and `canalport` for the hand-back |
| Clock | Day on arrival and through the trials; dusk from the bell; night from the Well stair on; dawn in Canalport |
| Flags in | `m3_done`, `m4_started` |
| Flags out | `m4_intro`, `m4_asked`, `m4_trial` (the stone, as built), `m4_ash`, `m4_tamsin`, `m4_boon`, `m4_sanctum_in`, `m4_brazier_1`, `m4_brazier_2`, `m4_brazier_3`, `m4_ward`, `m4_seal`, `m4_judged`, `well_flame`, `m4_fire`, `m4_beam`, `m4_done`, `m4_letter`. No longer `calmed_flame` (progression 20) |
| Unlocks | Tamsin (Flame, with Riolu) joins, and with her Blaze, first used here (decision 6); the Flame Well open (`well_flame`, the Wayfarer's engine at mission 10). **Nothing legendary:** Ho-Oh judges the crew and flies off, and the top Flame Summon stays locked until its catch after the Breaking (progression 20, decision 17) |
| Reply beats | 2, Corvin's (README §3): the abbot's question (scene 2); Tamsin's question at the seal (scene 9) |
| Fights | Tamsin (`tamsin_forge`, re-measured at Corvin's L7 floor); Ho-Oh's judgement (`ho_oh_judge`, a fixed-length fight it ends itself: story decision 9, progression 18 and 20). A loss plays "Try again" |
| Leads into | Crew 1 resumes on Canalport's jetty (scene 15), and Act I opens: missions 5 and 6 in either order |

**The flow.** Ketch lands Corvin on Embral, where the Forgeheart's sacred flame burns low and the tithe fleet is
due. Abbot Haldor refuses him the Well, but the Forgeheart turns nobody from its trials: pass the stone, the ash
and the fist, and ask one thing. Corvin moves the stone, digs up the bell and beats Tamsin, the monastery's best.
He asks for the seal. Haldor refuses, until Tamsin holds him to the Open Door's word. A monk's word doesn't bend,
so Haldor keeps it past sense: the Well stair is Corvin's, since no hand has moved the lid in six hundred years,
and Tamsin goes down as the Forgeheart's eyes. On the stair she tells him why she came: forty tithe braziers this
year, ten when she was a novice, and the flame half its height. They light the stair, reach the seal, and pull it
together. Ho-Oh rises from the Well grey and in agony, judges them in a fight it ends itself, takes back its
colour and bursts up through the roof, and the sacred flame goes with it. The crew gains nothing legendary. The
Forgeheart burns, and Haldor sends Tamsin away for the night. Ketch runs the skiff past the tithe fleet into the
Galeway. Two days later a Wingull brings Ilse's letter to Canalport's jetty: the Forest seal is next.

## Scenes

### 1. Embral

- Room: `forge_hall`, the gate court. Trigger: entering, unless `m4_intro` (today's `forge_arrival`, rewritten).

*[phase day] [fade in 40] Morning on Embral Isle, after a night at anchor in the cove: black rock and grey ash,
the volcano's plume leaning over everything. The Forgeheart is built into the mountainside, all red stone and iron
roofs: a gate court where monks spar with their Pokémon, and beyond it the great hall, where a tall brazier burns
at the heart of the floor. Its flame is small for its bowl.*

*Corvin comes up the cove stair with Larvitar. Ketch's skiff is a speck on the black sand below.*

**Corvin:** The Forgeheart. Sael says they've
kept the Flame seal six hundred
years.

And never once let a Rimborn near
it. No pressure.

*[emote Corvin: sweat] He tugs at his collar.*

**Corvin:** And Sael made me bring a coat.
To a volcano.

*Larvitar stops to watch a monk and a Machop trade blows in the court. [emote Larvitar: exclaim] A broad, bald
monk with a face like a closed door steps out of the gate's shadow.*

**Grist:** Halt. Name.

**Corvin:** Corvin. Of Fallhaven.

**Grist:** Business.

**Corvin:** The abbot. And then, with luck,
the Flame Well.

**Grist:** Hm. Luck.

The tithe fleet is due. The abbot
is busy. Hall. Mind the sparring.

*[walk Grist → the stone court] [rest point] [flag m4_intro] Control returns.*

### 2. The abbot

- Room: `forge_hall`, the great hall. Trigger: talking to Abbot Haldor (slots 8 and 9, merged), unless
  `m4_asked`.

*Abbot Haldor stands before the sacred brazier: a huge old man, white-bearded, in a red monk's robe with the
sleeves tied back, his knuckles scarred white. A Hariyama sleeps on its feet behind him.*

**Corvin:** Abbot. I'm Corvin, of Fallhaven.
I've come to see the Flame Well.

**Haldor:** No.

**Corvin:** You haven't heard why.

**Haldor:** Then tell me why, Rimborn. Make
it short. The tithe fleet is due,
and I am old.

**Corvin replies:**

1. "My town is falling."

   **Haldor:** Every town on the rim is falling.
   I'm sorry for it. The seals are not
   why.

2. "I mean to open it."

   *[emote Haldor: anger] [wait 20] [emote Haldor: silence]*

   **Haldor:** Honest. I'd throw a liar down
   the stair. An honest fool, I only
   refuse.

3. "To understand it."

   **Haldor:** The flame is understood. It burns.
   We keep it. The Pinnacle takes its
   tithe. There is nothing else.

*Every reply rejoins here.*

**Haldor:** No outsider walks the Well stair.
Six hundred years, and you will not
be the first.

*[wait 30] He looks at Corvin for a long moment.*

**Haldor:** But the Forgeheart turns nobody
from its trials. That is the Open
Door, older than the tithe.

Pass the three trials, and you may
ask the Forgeheart one thing.

Stone. Ash. The fist. In that
order.

**Corvin:** And if the one thing I ask for
is the Well?

**Haldor:** Then you will hear the Forgeheart's
answer. Go.

*[flag m4_asked] Control returns.*

### 3. The Trial of Stone

- Room: `forge_hall`, the stone court. Trigger: the training stone reaching the mat (slot 10, `m4_trial`, as
  built; puzzle 1). Before that, talking to Grist gives the trial (People, below).

*The stone settles on the mat with a thump that shakes dust off the posts. [shake 10, 1] Grist looks at it for a
while.*

**Grist:** Hm.

Good. The Earth answers you. Ash
court next. Sister Wren.

*[flag m4_trial] Control returns.*

### 4. The Trial of Ash

- Room: `forge_hall`, the ash court. Trigger: Scoop on the cold heap (puzzle 2, `m4_ash`). Before that, talking to
  Wren gives the trial (People, below).

*[phase dusk] The cold ash slides away from something green with age: a bronze bell as big as a barrel, on its
side. Larvitar puts its shoulder to it and rolls it the last cell to the empty frame. [walk Wren → the frame]
Sister Wren hangs it on its hook and looks at Corvin.*

**Wren:** The mountain keeps what it loves
under its coldest ash. You listened.
Most don't.

Ring it. The bell calls the fist.

*[pose Corvin: pull the rope] The bell rings out across the Forgeheart, deep and long. [shake 20, 1] In the
gate court every monk stops sparring and turns to look. In the great hall, someone laughs.*

**Wren:** Tamsin heard that. Everyone hears
that bell.

*[flag m4_ash] Control returns.*

### 5. The fist

- Room: `forge_hall`, the sparring ring in the great hall. Trigger: talking to Tamsin (slot 11), once `m4_trial`
  and `m4_ash`, unless `m4_tamsin` (the battle role).

*Tamsin waits in the sparring ring, bouncing on her toes: a tall young woman in a red sparring wrap with the sleeves
torn off, her red hair cropped short under a tied orange headband (her LPC look), her knuckles taped, a burn scar
up one forearm. Riolu bounces beside her, in time. [face Tamsin → Corvin]*

**Tamsin:** So. The Rimborn who moved our stone
and dug up our bell. Not bad.

I did both when I was nine. Before
breakfast.

Tamsin. Best fighter in the
Forgeheart. That isn't a boast. It's
a ranking.

The last trial is me. Nobody's
passed it in four years. Let's see
how hard you hit, Rimborn.

**Corvin:** Go easy on me. I've had a long
week.

**Tamsin:** No.

*[emote Riolu: anger] [emote Larvitar: anger] [battle tamsin_forge]*

*If the fight is lost, "Try again" plays and the fight restarts as it began. Tamsin's line as it restarts:*

**Tamsin:** Again? Good. I was only warming
up. Tell me you were too.

### 6. The Open Door

- Room: `forge_hall`. Trigger: winning the fight (Tamsin's `scene_after`, rewritten).

*Tamsin sits down hard on the mat. For a moment she just breathes. Then she laughs. [pose Tamsin: sit] [emote
Riolu: question]*

**Tamsin:** Ha! That hit like a landslide.

Eight out of ten. Nobody's had me
on the mat since I was fourteen.

I'm calling you Landslide. You don't
get a say.

*[pose Tamsin: stand] Haldor crosses the hall from the sacred brazier, slow and heavy. [walk Haldor → beside
Corvin] Monks drift in from the courts to watch.*

**Haldor:** Stone, ash and the fist. The Open
Door is open to you, Rimborn.

Ask your one thing.

**Corvin:** Open the Flame seal.

*[emote Haldor: silence]*

**Haldor:** No. Ask anything else.

*[emote Tamsin: exclaim] [walk Tamsin → between them]*

**Tamsin:** Abbot. The Open Door says one
thing. Any one thing.

You taught me a monk's word doesn't
bend. You taught me that before you
taught me to punch.

*[wait 40] The hall is very quiet. Haldor looks at the sacred flame, then at Tamsin.*

**Haldor:** ...It doesn't bend.

Then hear the Forgeheart's answer.
The Well stair is yours, Rimborn.
Go down. Try the seal.

No hand has moved that lid in six
hundred years. Yours will not be
the first.

Tamsin goes with you, as the
Forgeheart's eyes. What you do down
there, she sees.

**Tamsin:** Eyes and fists. Gladly.

*[recruit tamsin] Tamsin and Riolu join the crew.*

**System:** Tamsin joined the crew!

**Haldor:** The shaft is by the sacred flame.
Go down, and come back up the
same.

*[walk Haldor → the sacred brazier] [flag m4_boon] Control returns. The shaft is open.*

### 7. The Well stair

- Room: `forge_sanctum`, the head of the stair. Trigger: entering, unless `m4_sanctum_in`.

*[phase night] [fade in 30] A long stair cut down into the heart of the mountain, hot and close, lit red from
somewhere far below. Three cold braziers stand on its landings. At the bottom, a door of black stone. [crew out]
Tamsin steps out beside Corvin, and Riolu beside Larvitar.*

**Tamsin:** Right. Down here, Landslide, I'm
not just the abbot's eyes.

**Corvin:** No?

**Tamsin:** Forty tithe braziers this year.
Forty. When I was a novice, it was
ten.

And the sacred flame is half the
height it was. The abbot says we
don't pray hard enough.

I pray very hard. I want to know
why. So I'm here.

**Corvin:** You could have just said.

**Tamsin:** In front of the abbot? I'm brave.
I'm not stupid.

*[emote Riolu: sweat] Riolu presses its paws to the sides of its head. [pose Riolu: paws to head]*

**Tamsin:** Riolu? ...It reads what people
feel. It's reading something down
there.

Something that hurts.

*[pose Riolu: stand] [crew in] [flag m4_sanctum_in] Control returns.*

### 8. The ward door

- Room: `forge_sanctum`. Trigger: the third brazier lit in order (`m4_brazier_3`, puzzle 3), unless `m4_ward`.

*The three carvings glow in a row on the black door: spirit, beast, dragon. [light: red glow on the door] [shake
30, 1] The door sinks into the floor.*

*[crew out]*

**Tamsin:** Spirit, beast, dragon. Same as the
panels upstairs. Every novice learns
that one.

*[crew in] [flag m4_ward] Control returns.*

### 9. The Flame seal

- Room: `forge_sanctum`, the seal chamber. Trigger: talking to the seal (slot 8), once `m4_ward`, unless `m4_seal`
  (today's `flame_seal` scene, rewritten).

*The seal chamber: round, its walls black glass, the air shimmering with heat. In the middle of the floor the
Well's mouth is closed by a round stone lid as wide as a cart, bound with six bronze bands and carved with six
marks. A red glow seeps round its rim, faint and choked. A low hum comes up through the floor. [crew out]*

**Corvin:** Six marks. The same six as the
Keeping Stone at home.

Same hands made both, six hundred
years ago.

**Tamsin:** It's so quiet. The Well's under
there? It should be roaring.

**Corvin:** It isn't roaring. It's being held
down.

*[emote Riolu: sweat] [face Tamsin → Corvin]*

**Tamsin:** Last chance, Landslide. Tell me
why you'd pull it.

Make it good. I rate answers
too.

**Corvin replies:**

1. "Fallhaven is falling."

   **Tamsin:** Short. Hits hard. Seven out of
   ten.

2. "One seal, done right."

   **Tamsin:** Sounds like somebody said it to
   you first. Five out of ten. Still
   true.

3. "Nobody else will."

   **Tamsin:** Ha. Nine out of ten. That's a
   monk's answer.

*Every reply rejoins here.*

**Tamsin:** Pull it, and there's no going
back.

*[wait 30]*

**Tamsin:** ...Do it.

*[pose Corvin: hands on the lid] [light: amber glow on Corvin's hands] Larvitar sets its shoulder to the lid.
[pose Tamsin: hands on the lid] [light: red glow on Tamsin's hands]*

**Corvin:** On three. One. Two.

*[shake 60, 3] The bronze bands snap, one after another, six of them. The lid grinds aside. [flag m4_seal]*

*[wait 40] Silence. Then heat, like an oven door opening.*

*A cry comes up out of the Well from far below, long and raw. [shake 90, 3] Every brazier on the stair behind
them roars up at once. [light: red flare] Fire wells up out of the pit, and something rises in it on wide, slow
wings: a great bird, its feathers grey as cold ash, its eyes burning. [show Ho-Oh] [light: Ho-Oh tinted grey] It
screams. [emote Corvin, Tamsin, Larvitar and Riolu: exclaim]*

**Tamsin:** That's the firebird. From the
panels. The fourth one.

**Corvin:** It's hurt. Look at its feathers.

*Ho-Oh's head turns. It looks at the open Well, then at the broken lid, then at them.*

**Corvin:** It's looking at us like we did it.

**Tamsin:** We did do it.

**Corvin:** Fair.

*[crew in] [battle ho_oh_judge]*

### 10. The judgement

- Room: `forge_sanctum`. The fight itself: a fixed-length judgement that Ho-Oh ends itself (story decision 9),
  with its moves filtered to damaging ones (progression 18). The lines below show in the battle's message bar at
  the start of each round (a new step, `[round N]`).

*[round 1]*

**System:** Ho-Oh looks down at the crew.
It is weighing them.

*[round 2]*

**System:** Ho-Oh's eyes burn on Corvin.

*[round 3]*

**System:** Ho-Oh turns its gaze on Tamsin.

*[round 4]*

**System:** Gold flickers in Ho-Oh's grey
feathers.

*The end: after round 5, or as soon as Ho-Oh's HP falls below two thirds, whichever comes first (proposed
numbers; slice 3 builds the rule and slice 10 tunes it, so that an attack-only crew lives through all five rounds).
The fight ends there, with its EXP and no coins.*

**System:** Ho-Oh folds its wings. It has
seen enough.

*A Poké Ball thrown in this fight isn't used up:*

**System:** Ho-Oh turns the ball aside with
one wing. It is no one's to catch
tonight.

*If the crew falls anyway, "Try again" plays and the judgement restarts as it began. Corvin's line as it
restarts:*

**Corvin:** Up. It isn't finished with us.
And I'm not finished either.

### 11. The firebird goes

- Room: `forge_sanctum`. Trigger: the judgement's end (the seal's `scene_after`).

*Ho-Oh hangs over the open Well with its wings spread wide. Fire pours up out of the pit into its feathers, and
the grey burns off them: red, then gold, then every colour at once. [light: Ho-Oh's grey tint clears; a gold
flare] It looks at each of them in turn: Corvin, Larvitar, Tamsin, Riolu. [wait 60]*

*[crew out]*

**Tamsin:** ...Did we pass?

**Corvin:** We're not ash. I'll take that.

*Ho-Oh cries once and goes straight up. [walk Ho-Oh fast → up the shaft] The chamber's roof bursts. Burning
feathers and broken stone come down. [shake 80, 4] [hide Ho-Oh] Fire rains down the shaft after it. [light: red,
flickering] On the stair behind, the old banners catch.*

**Tamsin:** It went through the roof. The
hall is right above us.

**Corvin:** Then so is everyone. Up. Now!

*[crew in] [flag m4_judged] [flag well_flame] [warp forge_hall, entrance 1]*

### 12. The Forgeheart burns

- Room: `forge_hall`, the great hall. Trigger: entering from the shaft, once `m4_judged`, unless `m4_fire`.

*[fade in 20] [light: red firelight, flickering] The great hall is burning. Flame runs along the roof beams, and
embers fall like snow. Smoke rolls under the ceiling. The sacred brazier at the heart of the floor is cold and
black: its flame has gone, torn up through the roof after Ho-Oh. Monks pass buckets hand to hand from the
cistern. Brother Olm's Poliwrath stands in the doorway, spraying the beams very seriously.*

*In the middle of the floor sits a Bidoof, chewing, quite unbothered. [crew out]*

**Tamsin:** The Elder! Not without the Elder.

*[walk Tamsin → the Elder] She scoops up the Bidoof [hide the Elder] and hands it to Brother Olm as he runs past.
[walk Olm → the gate court] [hide Olm]*

**Olm:** Bless you, Tamsin!

*Haldor stands alone before the empty brazier, his Hariyama beside him. He doesn't turn.*

**Haldor:** Six hundred years it burned. Six
hundred years, and not once did it
go out.

*[face Haldor → Corvin]*

**Haldor:** I kept my word to you, Rimborn.
Look what my word has bought.

**Corvin:** I didn't know it would do this.

**Haldor:** No. You didn't know. That is what
the seals were for.

*[face Haldor → Tamsin]*

**Haldor:** I sent you down as the
Forgeheart's eyes.

**Tamsin:** I didn't just watch. I told him
to pull, and I pulled with him.

*[emote Haldor: silence] [wait 40]*

**Haldor:** Then go with him. The Forgeheart
has no room for you tonight.

*[emote Tamsin: silence] [emote Riolu: sweat]*

**Haldor:** Go! All of you. The tithe fleet
is in the bay.

They came for the tithe. They will
find a fire, and they'll want
someone to blame.

**Corvin:** Sorry about your roof, Abbot.

*[wait 20] [emote Corvin: silence]*

**Corvin:** ...I mean it.

**Haldor:** Sorry is a word. Go and make it
into something.

*[walk Haldor → the bucket chain] [crew in] [flag m4_fire] Control returns. The way out is the east door, across
the burning floor (puzzle 4).*

### 13. The east door

- Room: `forge_hall`. Trigger: the beam rolled off the east door (puzzle 4, `m4_beam`).

*The beam rolls off the threshold in a burst of sparks. [crew out]*

**Tamsin:** Six out of ten. Hurry up.

*[crew in] Control returns.*

### 14. The Galeway

- Room: `forge_hall`, the gate court. Trigger: stepping onto the head of the cove stair (a step-on spot), once
  `m4_beam`, unless `m4_done`.

*The gate court in the firelight. Monks carry what they can out of the burning hall and set it down on the stones.
Below the monastery the bay is full of lanterns: a dozen ships with white-and-blue sails, the order's wave and
ring on each. Boats are rowing for the shore. [camera → the bay] [camera back]*

*Grist stands at the head of the cove stair. [crew out]*

**Grist:** Tidewarden sails. Hm.

The cove stair. Go. I didn't see
you.

*[face Grist → Tamsin]*

**Grist:** Tamsin. Come back.

**Tamsin:** ...I will.

*Ketch is at the foot of the stair, waving both arms. [walk Corvin, Tamsin, Larvitar and Riolu → down the
stair]*

**Ketch:** In the boat! In the boat! I've
written another verse!

*[crew in] [fade out 40]*

**Narration:** Ketch ran the skiff out of the
cove with no lights, low under the
smoke.

**Distant voice:** Heave to! In the name of the
Pinnacle! Heave to!

**Ketch:** That's the Holdfast. The
Commodore's own flag. Hold on to
something.

**Corvin:** Graymantle herself. I'll bet
she's made {HERO} her deputy
by now.

**Narration:** A dozen sails came after them,
white in the firelight. Ahead, the
Galeway stood up like a wall.

At its edge the tithe fleet turned
back, as the order's ships always
do. Ketch didn't.

**Tamsin:** I've been hit by a lot of things.
That storm is ten out of ten.

**Corvin:** Welcome to the crew.

**Narration:** Behind them, the Forgeheart
burned until dawn.

And far beneath it, for the first
time in six hundred years, the
Flame Well ran free.

*[flag m4_done] [phase dawn] [resume crew 1] Crew 1 plays again on Canalport's jetty, where mission 3 left it.*

### 15. Ilse's letter

- Room: `canalport`, the end of the jetty. Trigger: crew 1 resuming here, once `m4_done`, unless `m4_letter`.

*[fade in 40] Dawn on the jetty, two days on. Tully is coiling rope on the Kestrel's deck. Maren sits on her
bollard with Eevee. A Wingull comes in low from the south and lands beside her, a letter tube on its leg. [show
Wingull] [crew out]*

**Maren:** Two days shovelling Canalport's
mud, and now this. The Commodore's
seal. It's for you, Deputy.

*{HERO} breaks the seal and reads.*

**Letter:** Deputy. The seal-breaker was at
Embral. He pulled the Flame seal.

A great firebird rose out of the
Well, and the Forgeheart burned.

The abbot says no lives were lost.
Not one. I do not know how.

He fled into the Galeway with a
Rimborn pilot, and a monk of the
Forgeheart beside him.

My ships cannot follow there. He
will try another seal.

The Forest seal, in the Greenwild,
has no fleet to guard it. Go to the
Eldergrove.

Hold it until my orders come.

I. Graymantle, Commodore. Aboard
the Holdfast.

*[walk Wingull → off south] [hide Wingull]*

**Maren:** A firebird out of a Well. Nothing
in the manuals covers that.

And a monk at his side. Your
seal-breaker is gathering a crew.

**{HERO}:** He really did it.

*Quiet: [emote {HERO}: silence] and no line.*

**Maren:** Then we hold the next one. The
Greenwild, Deputy.

**Tully:** The Greenwild's on the chart. Say
the word and we sail.

*[crew in] [flag m4_letter] Control returns. Act I is open: the Kestrel's chart marks the Greenwild as the next
bearing (story decision 1), and Vesper waits on the beach (mission 6).*

## People and signs, by room

### `forge_hall`

*The states:* the trials (`m4_intro`, until `m4_judged`), which change as `m4_trial`, `m4_ash` and `m4_boon` are
set; the fire (`m4_judged`, until `m4_done`). Crew 1 never comes to Embral in Act I (it isn't on the Kestrel's
chart), so nothing is written for after the fire. Positions are places in the re-clipped room.

- **Abbot Haldor**, slots 8 and 9 merged, at the sacred brazier. Scene 2. Then, until `m4_tamsin`:

  **Haldor:** Stone, then ash, then the fist. The
  Forgeheart is patient. Be quicker.

  *From `m4_boon`:*

  **Haldor:** Go down, Rimborn, and come back up
  the same.

  *The fire: scene 12, then at the bucket chain:*

  **Haldor:** Go.

- **Haldor's Hariyama**, behind him. The trials:

  **Sign:** The abbot's Hariyama, asleep on its
  feet. It was a champion once. So
  was he.

  *The fire:*

  **Sign:** The Hariyama is holding a burning
  doorframe up with both hands, so
  the novices can get out.

- **Brother Grist**, at the gate (scene 1), then in the stone court. Until `m4_asked`:

  **Grist:** The abbot first. Then the stone.

  *From `m4_asked`, until `m4_trial`:*

  **Grist:** The Trial of Stone. The stone, on
  the mat. Earth only.

  Hands won't do it. Nor will
  shouting.

  *From `m4_trial`, in the trials:*

  **Grist:** Hm. Good.

  *The fire:* at the cove stair (scene 14).

- **Sister Wren**, in the ash court. Until `m4_trial`:

  **Wren:** Stone first, then ash. The mountain
  can wait. It's very good at
  waiting.

  *From `m4_trial`, until `m4_ash`:*

  **Wren:** The Trial of Ash. Each spring the
  mountain buries our bell, and a
  novice digs it up.

  Three heaps. One holds the bell.

  The mountain keeps what it loves
  under its coldest ash.

  *From `m4_ash`, in the trials:*

  **Wren:** The bell has rung. Go to the fist.
  Tamsin doesn't like waiting.

  *The fire, at the head of the cove path, waving novices through:*

  **Wren:** Novices, down to the cove! Walk!
  Don't run! ...Run!

- **Brother Olm, the cook** (new), at the kitchen door. The trials:

  **Olm:** Bean stew tonight. It's always
  bean stew. Nobody's ever asked me
  for anything else.

  You've met the Elder? Our oldest
  brother. Never won a fight in his
  life. We love him dearly.

  *The fire:* scene 12.

- **The Elder** (the egg), a Bidoof in the middle of the great hall. The trials:

  **Sign:** A Bidoof sits in the middle of the
  hall, chewing. The monks step round
  it with great respect.

  *[emote the Elder: smile]*

- **Sister Ama** (new), sparring with her Machop in the gate court. Until `m4_tamsin`:

  **Ama:** Machop and I spar every morning.
  It wins most days. I've stopped
  minding.

  *From `m4_tamsin`, in the trials:*

  **Ama:** You put Tamsin on the mat. I've
  been trying for six years. I hate
  you a little.

  *The fire:*

  **Ama:** Machop, the tithe store! Shift the
  braziers before the roof comes
  down!

- **Dorrin, a novice** (new), with a broom and a Meditite, in the gate court. Until `m4_tamsin`:

  **Dorrin:** I'm a novice. I mostly sweep.
  Meditite mostly meditates. We're
  very good at it.

  *From `m4_tamsin`, in the trials:*

  **Dorrin:** You beat Tamsin? Are you allowed
  to beat Tamsin? Nobody told me you
  were allowed.

  *The fire:*

  **Dorrin:** I swept the hall this morning.
  This morning!

- **Tamsin**, slot 11, in the sparring ring. Until `m4_trial` and `m4_ash` are both set:

  **Tamsin:** Stone first, Rimborn. Then ash.
  Then me. I'll be here. I'm always
  here.

  *Then scene 5.*

- **Ketch**, at the foot of the cove stair. The trials:

  **Ketch:** I'll mind the skiff. Shout if you
  need rescuing. Shout loud. I'll be
  eating.

  The funeral song's coming on. It's
  got a volcano verse now.

  *The fire:* scene 14.

- **The bucket chain** (new), monks in a line from the cistern, in the fire:

  **Monk:** Buckets! More buckets! Mind the
  Poliwrath!

- **Brother Olm's Poliwrath**, in the hall's doorway, in the fire:

  **Sign:** Brother Olm's Poliwrath sprays the
  beams with great seriousness.

**Signs and things to examine**

- **The gate**, the trials:

  **Sign:** THE FORGEHEART. The flame tests
  what the hand claims.

- **The Open Door**, a plaque in the great hall:

  **Sign:** THE OPEN DOOR. Any who pass the
  three trials may ask the Forgeheart
  one thing.

  Stone. Ash. The fist.

- **The four panels**, on the great hall's north wall. The trials:

  **Sign:** Three panels of red stone: a fire
  spirit, a beast with a burning mane,
  a dragon coiled in flame.

  Carved under them: MARS. KIRIN.
  TIAMAT.

  The fourth panel is scorched blank,
  but for the shape of one great
  wing.

  Under it: THE FIREBIRD KEEPS THE
  FOURTH.

  *The fire:*

  **Sign:** The panels are black with smoke.
  The fourth is still blank.

- **The sacred flame**, the trials:

  **Sign:** The Forgeheart's sacred flame, low
  in a brazier as tall as a man. It
  looks tired.

  *The fire:*

  **Sign:** The sacred brazier is cold and
  black. Its flame went up through
  the roof.

- **The tithe store**, a side room off the hall:

  **Sign:** Iron tithe braziers, lidded and
  stacked to the beams. Each one
  glows faintly.

  Chalked on the door, one a year:
  10, 12, 16, 22, 30, 40.

- **The training stone**, slot 10 (puzzle 1), until `m4_trial`:

  **Sign:** A training stone, worn smooth by a
  thousand novices' shoulders. It
  would slide, with Move.

  *Move on it before `m4_asked` (the Psynergy event's `else_text`; the stone stays put):*

  **System:** The stone won't budge. The
  trials start with the abbot.

- **The mat**, in the stone court:

  **Sign:** A straw mat, flat and square. The
  stone's place.

- **The ash heaps**, three (puzzle 2), until `m4_ash`. The two warm ones:

  **Sign:** A heap of warm ash. A thread of
  smoke rises from it.

  *The cold one:*

  **Sign:** A heap of cold ash. Not a thread of
  smoke. Larvitar sniffs it hopefully.

  *Scoop on any heap before `m4_trial` (nothing moves):*

  **System:** The ash won't give. Stone
  first, then ash.

  *Scoop on the first warm heap, from `m4_trial` (text only, no flag):*

  **System:** Only warm ash.

  *Scoop on the second warm heap, from `m4_trial` (text only, no flag):*

  **System:** Warm ash, and a very old
  sandal.

  *Scoop on the cold heap, from `m4_trial`:* scene 4.

- **The bell frame**, until `m4_ash`:

  **Sign:** An empty bell frame. The hook is
  polished bright from years of
  hanging.

  *From `m4_ash`:*

  **Sign:** The Forgeheart's bell, green with
  age, back on its hook.

- **The kitchen door:**

  **Sign:** It smells of bean stew. It always
  smells of bean stew.

- **The shaft**, beside the sacred flame (the warp's closed line, until `m4_boon`):

  **Sign:** A shaft drops into the hot dark.
  The monks would never let a stranger
  near it.

- **The cove stair**, the trials:

  **Sign:** Steps down to the black-sand cove,
  where Ketch minds the skiff.

- **The fallen beam** (puzzle 4), the fire, until `m4_beam`:

  **Sign:** A roof beam lies across the east
  door, one end still burning. It
  would roll, with a push.

- **The burning floor** (the hazard's line, the fire):

  **System:** The floor is burning! It scorches
  the crew's feet.

### `forge_sanctum`

No people but the crew and Ho-Oh (scenes 7 to 11). The things to examine, from the head of the stair down:

- **The braziers**, three, on three landings (puzzle 3). The first landing's, until lit:

  **Sign:** A cold brazier. On its bowl, a
  dragon coiled in flame.

  *The second landing's:*

  **Sign:** A cold brazier. On its bowl, a
  fire spirit with its arms raised.

  *The third landing's:*

  **Sign:** A cold brazier. On its bowl, a
  beast with a burning mane.

  *Blaze out of order (the brazier stays cold, and nothing is set):*

  **System:** The flame catches, gutters and
  dies. Not this one. Not yet.

  *Lit:*

  **Sign:** The brazier burns. The carving on
  its bowl glows red.

- **The ward door**, until `m4_ward`:

  **Sign:** A door of black stone, carved with
  a spirit, a beast and a dragon, in
  a row.

  Above them: CALL THEM AS THE FORGE
  CALLS THEM.

- **The chest**, in an alcove off the second landing: Elixir ×1, with the engine's chest line (naming
  `{LEADER}`).

- **The gear chest**, in an alcove off the third landing (the dungeon's gear chest, items §13): Padded Gloves, with
  the engine's chest line.

- **The Flame seal**, slot 8, until `m4_seal`:

  **Sign:** A stone lid over the Well's mouth,
  bound in bronze. Six marks are cut
  into it.

  *From `m4_judged` (today's `text_after`, extended):*

  **Sign:** The seal lies open, its bronze
  bands snapped. The lid will never
  sit straight again.

- **The open Well**, from `m4_judged`:

  **Sign:** The Flame Well, open. Far down it
  roars like a forge. It doesn't
  sound hurt any more.

### `canalport` (the hand-back)

Scene 15 only. Mission 3's "after the sluice" lines hold for everyone else in the room. Vesper's row appears from
`m4_done` (mission 6's script).

## Items and chests

| What | Where | Gives | The words |
|---|---|---|---|
| The stair chest | `forge_sanctum`, the second landing's alcove | Elixir ×1 | The engine's chest line, naming `{LEADER}` |
| The gear chest | `forge_sanctum`, the third landing's alcove (the dungeon's gear chest, items §13) | Padded Gloves (Corvin and Tamsin's kits have no gloves; the hero and Maren start with a pair each) | The engine's chest line, naming `{LEADER}` |
| Tamsin's purse | The fight, as built | 40 coins | The fight's own line |
| Ho-Oh | The judgement | **Nothing legendary** (progression 20): no catch, no Summon, no item, no coins. The fight's ordinary EXP only | Scene 10's lines |
| The letter | Scene 15 | Nothing: words | The Letter, above |

## Puzzles

Corvin's verbs are Move and Scoop. Tamsin brings Blaze (Flame Psynergy, built for her: decision 6) from scene 6.
Two trials in the hall, the brazier stair below it with Tamsin's first Blaze, and the escape through the fire.
Pushed things stay where they're pushed, so every block can be got behind again.

**Puzzle 1. The Trial of Stone (Move, as built, laid out again).**
1. In the stone court, the training stone (slot 10) sits one row north and three cells east of the mat. A
   sparring post stands west of the stone, in its row.
2. Push it south once (from the north), then west three times (from the east), so the player has to walk round
   it. The mat's cell is today's target, (5,9) on today's clip; the re-clip keeps the same shape.
3. On the mat (`m4_trial`), scene 3 plays. The court is open round every cell the stone can reach.
4. The stone only moves once the abbot has set the trials (`m4_asked`); before that Move gives the stone's
   refusal line (People and signs), as Grist says, so the trials keep their order.

**Puzzle 2. The Trial of Ash (Scoop, new).**
1. In the ash court, three heaps of ash and an empty bell frame. Wren's riddle: the mountain keeps what it loves
   under its coldest ash.
2. Examining the heaps tells them apart: two have a thread of smoke, one has none (and Larvitar sniffs it).
3. Scoop on a warm heap only says so ("Only warm ash." on one, the sandal on the other: People and signs).
4. Scoop on the cold heap uncovers the bell (scene 4, `m4_ash`). The heaps answer Scoop only from `m4_trial`;
   before that the ash won't give, as Wren says.

It reads before it digs: Golden Sun's habit of hiding the answer in what people say.

**Puzzle 3. The brazier stair (Blaze three times, in order, new).**
1. Three cold braziers stand on the stair's three landings, carved with a dragon (first landing), a spirit
   (second) and a beast (third). The ward door at the bottom says: call them as the Forge calls them.
2. The order is the great hall's panels and the door's carving: spirit, beast, dragon (Mars, Kirin, Tiamat).
3. Blaze lights a brazier only in its turn: the spirit first (`m4_brazier_1`), then the beast (`m4_brazier_2`),
   then back up to the dragon (`m4_brazier_3`). Out of turn the flame gutters and nothing is set, so nothing ever
   needs resetting.
4. The third opens the ward door (scene 8). The chests' alcoves are off the second and third landings.

It shows off the new Adept's Psynergy, as the party rules ask of each recruitment (party-and-battle.md §7).

**Puzzle 4. The east door (Move, new, in the fire).**
1. With the hall burning, the way out is the east door to the gate court. A burning roof beam lies across its
   threshold.
2. Some floor cells burn (a hazard: each step on one costs a little HP, never below 1). A path round them exists;
   the shortest way crosses two.
3. Stand west of the beam and cast Move: it rolls east one cell, off the threshold and into the gutter beside the
   door (`m4_beam`). The door is open (scene 13).

## Eggs

story.md §9a places no egg in mission 4. One of its unplaced Pokémon nods fits the Forgeheart and is placed here
as an invention, as mission 2 placed Pip: **"A Bidoof everyone loves"** is **the Elder**, the monastery's oldest
brother, who has never won a fight and is loved dearly; Tamsin won't leave the burning hall without him.

## Not in this mission

Ho-Oh's caldera nest and its classic catch after the Breaking (story.md §5, items 25), with the top Flame Summon
it unlocks (progression 20); the Forgeheart smith (Act II, items-and-economy.md §8); Tamsin's heart quest,
"Rekindle the Forgeheart flame" (story.md §11), which this mission seeds.

## Inventions

Things story.md doesn't say, for you to keep or strike:

- **The Forgeheart:** red stone and iron roofs on Embral's mountainside; the gate court, the great hall, the stone
  and ash courts, the kitchen and the tithe store; "The flame tests what the hand claims"; the sacred flame burning
  low in its brazier.
- **The Open Door:** any who pass the three trials (stone, ash and the fist) may ask the Forgeheart one thing, a
  law older than the tithe; the bell the mountain buries each spring; Haldor bound by it, and Tamsin holding him to
  it. Haldor keeps it past sense: the Well stair is Corvin's, because no hand has moved the lid in six hundred
  years, and Tamsin goes down as "the Forgeheart's eyes" ("Eyes and fists"). She ends up pulling with Corvin, which
  is why he sends her away.
- **The Forgeheart's people:** Abbot Haldor (an old champion, with his Hariyama), Brother Grist at the gate
  ("Hm."), Sister Wren and her riddle, Brother Olm the cook and his bean stew and Poliwrath, Sister Ama and her
  Machop, Dorrin the novice and her Meditite, and the Elder (the egg, above).
- **The fire tithe:** the Forgeheart pays in iron tithe braziers filled from the sacred flame (the opening's tithe
  barge carries such braziers), forty this year against ten when Tamsin was a novice, chalked one a year on the
  store's door; the tithe fleet due at the turn of the season (mission 1's notice), which puts Ilse's ships in the
  bay.
- **Tamsin:** her look (the LPC recipe's red hair and tied headband, with a sparring wrap, taped knuckles and a
  burn scar); "out of ten" for everything; "Landslide" for Corvin; her reason for coming (the braziers
  and the flame); "I'm brave. I'm not stupid"; the Elder; sent away "tonight", not forever, with Grist's "Come
  back" (seeds for her heart quest).
- **Riolu** reading pain from the Well before anyone sees Ho-Oh.
- **The four panels:** Golden Sun's Flame Summons (Mars, Kirin, Tiamat, as decision 17 names them) carved in the
  hall, and the fourth panel blank, "the firebird keeps the fourth": the in-world reason the top Flame Summon waits
  for Ho-Oh (progression 20). They are also the brazier stair's order.
- **The Flame seal:** a bronze-banded stone lid over the Well's mouth, with the Keeping Stone's six marks ("same
  hands made both"); pulled by Corvin, Larvitar and Tamsin together.
- **Ho-Oh:** rising grey and drained from the Well, its colour coming back as the Well's fire returns to it, its
  judgement wordless (it never speaks), the ball it turns aside, and its flight straight up through the roof.
- **The sacred flame** torn out and gone with Ho-Oh, leaving the brazier cold: a seed for Tamsin's heart quest and
  for the caldera nest after the Breaking.
- **Haldor's lines:** "I kept my word. Look what my word has bought", and "You didn't know. That is what the seals
  were for": the order's side, half right, said by someone who isn't the order.
- **Corvin's lines:** the coat Sael made him bring "to a volcano" (mission 2's coat), "Sorry about your roof,
  Abbot. ...I mean it", and "I'll bet she's made {HERO} her deputy by now" as the Holdfast gives chase.
- **No lives lost** in the fire, by Ilse's letter.
- **The escape:** Ketch's new verse, the tithe fleet with Ilse's flagship the Holdfast (mission 3), "Heave to!",
  the fleet turning back at the Galeway's edge, Tamsin's "ten out of ten" storm.
- **Ilse's letter** by Wingull: the Forest seal "has no fleet to guard it", and she holds the hero to it "until my
  orders come", which mission 5's runner then gives (drive it deeper). The two days crew 1 spends shovelling
  Canalport's mud while it waits.
- **The rewards:** Elixir ×1 and Padded Gloves (the dungeon's gear chest) on the stair.

## Changes to the build

**Rooms**
- **`forge_hall`** re-clipped from a larger part of Golden Sun 1's Fuchin Temple (room 61 and the rooms round it,
  the builder's pick) to hold: the gate court with the sparring monks and the cove stair (a step-on spot at its
  head), the great hall with the sacred brazier, the panels, the Open Door plaque, the sparring ring, the shaft and
  the east door, the stone court with its posts and mat, the ash court with three heaps and the bell frame, the
  kitchen door and the tithe store. Entrance 1 stays at the shaft's top.
- **The fire state** of `forge_hall` from `m4_judged`: red flickering light; `hazards` on the burning cells; the
  fallen beam as a pushable actor across the east door; the monks' fire rows; the sacred brazier and the Elder
  swapped; the shaft closed behind the crew.
- **`forge_sanctum`** re-clipped longer: the stair with three landings, three braziers and two alcove chests, the
  ward door (a gate on `m4_ward`), and the seal chamber with the lid (slot 8) and the Well's mouth; the roof
  opening after Ho-Oh goes.
- **`canalport`:** scene 15, an enter scene that plays when crew 1 resumes there (once `m4_done`).

**Actors and engine**
- **Corvin's L7 floor** (progression 1) applied when crew 2 starts here, and Tamsin recruited at L7.
- **Haldor's two rows** (slots 8 and 9) become one with text by state; the shaft's warp opens on `m4_boon` (today
  `m4_tamsin`).
- **Tamsin** (slot 11): her pre-fight text, the retry line, and scene 6 as her `scene_after` (the boon, then
  `recruit`).
- **Scoop with text only:** the warm heaps answer Scoop with a line and no flag.
- **Blaze** (decision 6) on the field.
- **Psynergy events gated by a flag:** an `if_flag` with an `else_text` on a Psynergy event, so the stone moves
  only from `m4_asked`, the heaps answer only from `m4_trial`, and each brazier lights only in its turn.
- **Ho-Oh's judgement** (story decision 9, progression 18 and 20): it ends after round 5 or below two thirds of its
  HP, whichever is first (proposed); damaging moves only; EXP and no coins; a thrown ball isn't used up and shows
  its line; the `[round N]` step for the message-bar lines; "Try again" with Corvin's line. `forge_sanctum` stops
  setting `calmed_flame`, Mars's top Summon (Meteor) stays locked, and `tools/mission4_check` and any check that
  expected `calmed_flame` change to match.
- **Ho-Oh on the field:** the expansion's overworld sprite at 2× with its appear and flight animations (decision
  28), tinted grey from scene 9 until scene 11 (a tint on one actor through the `light` step).
- **A crowd walk** (mission 2's step): the crew down the cove stair; Haldor, Olm and Wren walking off.
- **Ketch, the Elder, the Hariyama, the Poliwrath, the Machop, the Meditite, Riolu and Larvitar** as actors
  scenes can move.
- **Lines over black** for the Galeway, then `phase dawn` and `resume_crew 1`, which today ends the sanctum scene.
- **`{LEADER}`** in the chest line (as mission 2 asks).

**New scene steps** (README §2): `phase`, `light` (the glows, the flare, the firelight and the grey tint),
`camera`, `pose` (sit, stand, pull the bell rope, paws to head, hands on the lid), `choice` (Corvin's replies,
with no quiet set), `crew out` and `crew in`, `[round N]`, step-on triggers (scene 14), a trigger on a Psynergy
flag (scenes 3, 4 and 8) and an enter scene on resuming (scene 15).

**Checks.** `tools/mission4_check` follows the new flow: the arrival, Haldor's reply menu, the two trials, the
fight and its retry line, the boon and the recruit, the stair's order (an out-of-turn Blaze sets nothing), the
seal and Tamsin's reply menu, the judgement ending on its own (by rounds and by HP) with no Summon, the fire's
hazards and the beam, the Galeway, and the letter in Canalport.
