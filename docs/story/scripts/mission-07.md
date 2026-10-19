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

