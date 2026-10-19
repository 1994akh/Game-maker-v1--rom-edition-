# The mission scripts

**Status:** drafts for your yes or notes (18 Oct 2026). Nothing here is built until you approve its page.

You decided on 18 Oct ([demo-plan.md](../../design/demo-plan.md) §5, decision 1) that the engine side writes each
mission's full script in [story.md](../story.md)'s tone and posts it for your yes or notes before building it. These
pages are those scripts: every line anyone says, every sign, every chest and every puzzle, written so a builder can
turn each one into the room's `events.json` without inventing a word.

| Page | What it covers | Status |
|---|---|---|
| [opening.md](opening.md) | The narrated intro before the creator (decision 3), with the six stills described for the illustrator | Draft |
| [mission-01.md](mission-01.md) | Mission 1, The Keeping Night | Draft |
| [mission-02.md](mission-02.md) | Mission 2, The Drowned Boy | Draft |
| [mission-03.md](mission-03.md) | Mission 3, Highwater | Draft |
| [mission-04.md](mission-04.md) | Mission 4, The Forgeheart | Draft |
| [mission-05.md](mission-05.md) | Mission 5, The Eldergrove (either order with 6), with the Hive and Celebi's still | Draft |
| [mission-06.md](mission-06.md) | Mission 6, Lantern Reef (either order with 5) | Draft |
| [mission-07.md](mission-07.md) | Mission 7, Bastion Rock: the first Crew 2 interlude, with Nerissa | Draft |
| [mission-08.md](mission-08.md) | Mission 8, The Tradewind Bazaar: the second Crew 2 interlude, with Wynn, the Guild's contracts and the posters | Draft |

Missions 9 and 10 follow in this folder, one page each, in the same format.

## 1. What a page holds, in order

1. **The header:** the mission, its rooms, the crew, the clock phases, the flags it reads and sets, what it unlocks,
   its reply beats and its fights.
2. **The scenes, in play order.** Each scene names its room, its trigger (entering, talking to someone, stepping on
   a spot) and the flags that allow it. Then its stage directions and lines.
3. **The people and signs, by room:** every townsperson's and sign's text, with where they stand and which state of
   the mission each line belongs to.
4. **Items and chests:** what each gives and the words around it.
5. **The puzzles:** 2 to 4 per dungeon (decision 6), from the verbs the crew holds at that point, step by step.
6. **The eggs** placed in the mission (story.md §9a, decision 10).
7. **Inventions:** everything the page adds that story.md doesn't say, so you can strike any of it.
8. **Changes to the build:** the rooms, actors, scene steps and flags the script needs that the engine lacks.

## 2. How a line is written

- A page of the message box is a paragraph that starts with the speaker in bold: `**Brann:** text`. The speaker's
  name isn't part of the text: it shows in the portrait or the name tag beside the box (decision 24).
- **Line breaks are the box's line breaks.** Each line of the paragraph is one line of the box. Rendered Markdown
  runs them together; the raw file keeps them, and that's what the builder copies.
- **A blank line starts the next page.** A plain paragraph straight after a speaker's page is that speaker's next
  page; a new `**Speaker:**` or a stage direction ends the speech.
- `**Narration:**` is the unvoiced narrator (no name tag). `**Sign:**`, `**Note:**` and similar are examined
  objects. `**System:**` marks the engine's own messages ("{HERO} received the Lodestar!"), written out so you see
  them in place.
- `**Dabney, thinking:**` is a thought heard with Mind Read (mission 8 on): the name tag shows, and the words are
  what the person is thinking, not saying.
- The builder turns pages into `{BOX}` breaks and lines into `\n`; scripts never write `{BOX}` themselves.

**Stage directions** are italic paragraphs. They say what is seen, in plain words, then the engine step in square
brackets so the builder knows what to use:

| Tag | Engine step (engine `maps_src/README.md`) |
|---|---|
| `[walk Brann → beside {HERO}]`, `[walk Corvin fast]` | `walk` to a cell, or by an offset; "fast" is speed 2 or more |
| `[face Ilse → {HERO}]` | `face` toward someone or a direction |
| `[emote Brann: exclaim]` | `emote`: exclaim, question, silence, heart, idea, anger, sweat, smile, scowl, squint |
| `[shake 60, 3]` | `shake` for 60 ticks at amount 3 |
| `[fade out 40]`, `[fade in 30]` | `fade` |
| `[flag m1_quake]` | `flag` |
| `[hide Corvin]`, `[show Tanner]` | `hide`, `show` |
| `[give Poké Ball ×5]` | `give` |
| `[give_pokemon Marill, L6]`, `[recruit maren]` | `give_pokemon`, `recruit` (as built, with the engine's own "{HERO} received Marill!" and "Maren joined the crew!") |
| `[give_pokemon Mimikyu, L9, to the Kin Garden]` | `give_pokemon`, **new:** straight to storage with the storage line, never into a Set (a Djinn-style find) |
| `[take_coins 50]` | `take_coins` (as built) |
| `[to_entrance 0]` | `to_entrance` (as built: a guard's `caught` steps) |
| `[battle corvin_vault]` | `battle` |
| `[gate …]` | a room `gate` opening or repainting cells |
| `[crew 2]`, `[resume crew 1]`, `[warp room, entrance]` | `crew`, `resume_crew`, `warp` |
| `[rest point]` | `rest_point` |
| `[phase night]` | **new step:** set the clock's phase (day-night-clock.md decision 4) |
| `[light: …]` | **new step:** a tint or a pulse of coloured light over the room |
| `[camera → the east street]`, `[camera back]` | **new step:** pan the camera to a cell and back |
| `[pose Corvin: kneel]` | **new step:** one of the scripted poses (art part A) |
| `[choice]` | **new step:** a reply menu (section 3) |
| `[sprite Corvin → 35]` | **new step:** swap an actor's sprite mid-scene (the unmasking) |
| `[still name]` | **new step:** an illustrated still (Celebi's vision and Sael's death only, decision 4) |
| `[crew out]`, `[crew in]` | **new step:** the crew's members step out of the lead to stand beside them for a scene, and back in after (Golden Sun's way), so recruits can be staged |
| `[give coins 100]` | `give`, **new:** coins as well as items |
| `[round 2]` | **new step:** a line in a story fight's message bar at the start of that round (Ho-Oh's judgement) |
| `[dial]` | **new step:** a number dial of three rings, 0 to 9 (the Bazaar's strongbox, decision 6); the right code plays on, a wrong one says its line |

Each page's last section lists every new step it uses.

## 3. Replies (decision 2)

- **About two reply beats a mission.** At each, the player picks one of two or three replies.
- **A reply changes only the next few lines,** then the scene rejoins one path. **No reply ever sets a flag**, and
  nothing later reads which one was picked.
- They're written as a numbered list under `**{HERO} replies:**`. Each item gives the label (in quotes, as it shows
  in the menu), then the quiet hero's form, then the lines that follow it, indented:

  ```
  1. "I'll find him." · quiet: (Nod)
     **Ilse:** Good. Find him before someone
     less kind does.
  ```

- **The quiet hero** (the creator's Voice row, character-creator.md) sees the same menu with the quiet forms: option
  1 is always **(Nod)**, option 2 **(Shake head)** and option 3 **...**, the Golden Sun nod from story.md §9a. So
  option 1 is the "yes" reply, option 2 the "no" or the doubt, and option 3 the question or the silence, and the
  lines after each are written to fit both the spoken and the quiet form. A two-option beat uses 1 and 2.
- **The hero's other lines.** The hero speaks short lines at a few moments. Each has a quiet form written under it
  (`*Quiet: …*`): an emote, a pose, or nothing, and the lines around it still make sense without the spoken line.
  The hero never carries information the scene needs; someone else always says it too.
- **A mission played as another lead** (mission 2 is Corvin's) gives that lead the reply beats under
  `**Corvin replies:**`. They always speak: the quiet setting is the hero's alone. The same rules hold.

## 4. Tokens

| Token | Becomes | Longest |
|---|---|---|
| `{HERO}` | The hero's name (default Rowan) | 10 letters (the creator's limit) |
| `{HERO_SUBJ}` | he / she / they | 4 |
| `{HERO_OBJ}` | him / her / them | 4 |
| `{HERO_POSS}` | his / her / their | 5 |
| `{LEADER}` | The active crew's lead, for system lines while Corvin's crew plays. **New:** the engine has only the four `HERO` tokens today; mission 2's build list asks for it | 10 |

Rules, because the pronouns are the player's choice:
- The pronoun tokens are lower case, so **never start a sentence with one.** Start with `{HERO}` instead.
- **Don't put `{HERO_SUBJ}` before a verb that changes with "they"** (is, was, has, does). Use the name, a past
  tense that doesn't change ("{HERO_SUBJ} went"), or a modal ("{HERO_SUBJ} can", "will").
- **No gendered words for the hero:** no lad, lass, boy, girl, son, daughter, sir, ma'am, brother, sister. Other
  people may use them of each other.
- `{BOX}` is never written in a script (section 2).

## 5. The line budget

- **At most 36 characters a line**, counted with `{HERO}` as 10 letters and the pronouns at their longest, so the
  longest name and pronoun still fit the 480×320 box in Kenney Pixel 16 (art decision 6).
- **At most 3 lines a page** (`DialogueBox.PAGE_LINES`). One thought a page; a long speech is several pages.
- **Reply labels at most 24 characters**, so the menu fits beside the box.
- **The font's safe set:** plain ASCII and é (for Pokémon). Three full stops `...`, never the ellipsis character;
  straight quotes; no dashes. The quiet reply "…" shows as `...`.
- **The check:** `python -X utf8 docs/story/scripts/check_lines.py` reads every page here and fails on a line,
  page or label over budget, a character outside the safe set, or a pronoun token used against section 4. Run it
  before posting a page; every page in this folder passes it. The real text-fit test at the new font comes with
  slice 5 (demo-plan.md §3, slice 9).

## 6. States: when a line is said

Townsfolk and signs change with the mission. Each is written as a short list of states, named by what has
happened, with the flag that starts each one:

```
- Festival (until m1_quake)
- After the quake (m1_quake, until m1_corvin_fled)
- After the Vault (m1_corvin_fled)
```

A person with one state says the same thing throughout the mission. The builder turns states into actor rows with
`condition`s, or into one row whose text follows the flags (each page's build list says which it needs).

**Lines for a crew member who may not be there.** Missions 5 and 6 come in either order (story.md §6), so Sorrel
or Vesper may or may not be in the crew. Their lines are marked in place, *Vesper in the crew:* or *Sorrel in the
crew:*, with the flag that means it (`m6_pilot`, `m5_sorrel`); the builder makes them `when` steps. A scene always
makes sense without them, and each page lists them under "Either order". `[crew out]` steps out whoever is in the
crew. Mission 7's hand-back to Crew 1 marks Sorrel's and Vesper's lines the same way.

**Flags** are named `m<mission>_<what>` (`m1_quake`), as the engine's are today. A page keeps the engine's existing
flag names and lists every new one in its header.

## 7. Voices

story.md §4 gives each person a line or two; these notes keep them distinct from page to page. Anything beyond
story.md is an invention, listed on the page where it's first used.

| Who | How they talk |
|---|---|
| {HERO} | Short and plain. Steady. Says less than they feel. The player fills the rest |
| Corvin | Warm and quick, teasing, a little theatrical. Jokes when it hurts. Apologises lightly and means it heavily |
| Keeper Brann | Old, slow, dry. Talks in eggs and stone. Gruff on top, soft underneath. Calls the hero "apprentice" |
| Commodore Ilse | Clipped and exact, a naval officer. Kind in what she does more than what she says. Believes in the order. Calls the hero by name, then "deputy"; "apprentice" is Brann's word |
| Captain Sael | Dry, blunt, a sea captain. Fierce love said as scolding. Never wastes a word |
| Hask | Low and level, never shouts. Speaks in absolutes: every, all, now. Needles Corvin as "Sael's stray" |
| Maren | By the book, precise, a medic's calm; a careful listener (mission 3 on). Diagnoses in lists ("a split knuckle, a bruised jaw"; "drought, blight or root rot"), takes notes on everything ("I'll need a new page"), "I'll know if you don't". Calls the hero "Deputy", then by name. Never says who her reports go to: asked, she says "Medical returns" or "The order" |
| Sorrel | Prickly, short, kinder to plants than to people (mission 5 on). Clipped sentences, often one word ("What.", "East."); gentle only with plants and Kin ("Slowly. Nobody's going to take it off you"). Says the blunt true thing ("It isn't lifted. It's buried"). Never thanks anyone outright; does the kind thing and scowls. Says "Kin", the Greenwild's word. Calls the hero "keeper" when she wants something of them, Maren "Tidewarden" |
| Vesper | Dry wit, few words, a pilot's eye for weather (mission 6 on). Deadpan, two or three words where others use ten ("Pilot. Paid."); talks in weather ("Day fog stands up. Night fog lies down"); money-minded ("I don't give credit. I keep a tab"). Treats Ghost Pokémon as friends. Calls the hero "deputy", Maren "medic". Dislikes the Tidewardens and takes their coin ("Tidewarden orders. My favourite"). Never says where she's from; when it nearly slips, "Never mind. Old weather" |
| Tamsin | Proud, blunt and funny; rates everything by how hard it hits, out of ten (mission 4 on). Calls Corvin "Landslide". Brave, "not stupid"; soft about the Elder |
| Nerissa | Calm and wry; a diver's patience (mission 7 on). Slow, short and dry ("'Yet.' A short word with a long tail on it"); hears people by their walk; talks in breath and depth ("Breathe when I breathe. In. Out."); kind without fuss ("Kind. Nobody does anything for nothing. But kind"). Calls Corvin "seal-breaker" while she's testing him. Wants to go home to Pearlhollow, and says so once, not often |
| Wynn | Chatty, quick, always mid-thought; afraid of heights and says so (mission 8 on). Starts in the middle of a sentence ("...which it is, which I said. Hello!"); runs on, then takes it back ("Ask anyone. Don't ask anyone"); says she's scared of heights every time ("Why is there so much down?"); hears loud thoughts and says that too ("You think very loudly"). Fierce only about her chart |
| Gary Rivalson | Smug, sure he's the main character, never in danger. Signs off "Smell you next tide!" |
| Ketch | Corvin's Rimborn skiff pilot: chatty, cheerful under fire, always mid-way through Corvin's funeral song, with a new verse for every place (a volcano verse, a prison verse, a market verse); always eating or about to (missions 2, 4, 7 and 8) |
| Abbot Haldor | The Forgeheart's abbot, an old champion: formal, slow, few words, fighting sayings. Keeps his word past sense. Calls Corvin "Rimborn" (mission 4) |
| Harbourmaster Quayle | Canalport's harbourmaster: fussy, kind, talks in tide times and bells, loves his ferry Marill (mission 3) |
| Captain Rufio Maize | The One Piece cameo (story.md §9a): loud, delighted, always hungry; "Best adventure ever!", "King of the Open Sea", asks everyone to join his crew (mission 3 on) |
| Tully | The Kestrel's mate: cheerful and practical, proud of the cutter and calls her "she"; says the plain thing ("It's not turning"). Calls the hero "Deputy" once there is one (missions 1 on) |
| Celebi | The Forest legendary, which talks (story.md §5): rarely, in short strange lines out of time ("This is when"). Tired and thin, and wants only to be remembered (mission 5) |
| Elder Hollin | The Eldergrove's elder: stern, frightened, proud of the grove's ways. Not cruel: says sorry for what she believes ("I'm sorry for that"), calls Sorrel a fool and "ours" in one breath (mission 5) |
| Runner Pell | A young Tidewarden runner off the cutter Dunlin: earnest, breathless, very correct ("Begging your pardon"); thanks people for small things ("Thank you for being so easy to find") (missions 5 and 8) |
| Marrit | Lantern Reef's lantern-keeper: old, certain and practical. The Ghost Pokémon are the drowned crews come home, and "that's what they'd like you to think". Short sentences, kind under them (mission 6) |
| Maestro Bonewhistle | The One Piece cameo (story.md §9a): a grand, delighted skeleton; announces his own bone jokes ("Bone joke!"), asks "May I see your Pokédex?", sad about his lost violin underneath (mission 6 on) |
| Sergeant Pruitt | Bastion Rock's duty sergeant: barks in forms ("Name! Number! Licence!"); if it isn't on the register, it isn't there, so Froakie is a frog. Has never once slept on duty, and says so on his desk (mission 7) |
| Lieutenant Holm | A young officer of the Bastion watch: brave, loud, by the book ("Halt! In the name of the Pinnacle!"); would arrest a frog and register it after. Does her duty to the end, even when the end is setting the sea on fire (mission 7) |
| Old Tarrant | A jailed Rimborn smuggler, the Magikarp-salesman egg: "Psst", haggles against himself (five hundred, then five), cheerful about eleven more years (mission 7) |
| Guildmistress Tally | Head of the Freeport Guild at the Tradewind Bazaar: brisk, fair, counts and weighs everything on her brass scales ("The Guild doesn't care who you are. The Guild cares what you owe"); fines to the coin. Calls Corvin's crew "Bronze" once they're in the Guild (mission 8) |
| Factor Plumb | A Bazaar moneylender: oily courtesy, "my friend", "my dear", "Business is business"; menace said smiling; fond of the old laws, "paid in coin or paid in kind" (mission 8) |
| Purser Dabney | Plumb's clerk: nervous, honest underneath, and thinks very loudly ("Don't think it, Dabney") (mission 8) |
| The Tumbleweed Trio | The Pokémon cameo (story.md §9a): Bramble, grand and theatrical ("Thank you SO much, dears"); Burr, soft, stuck with burrs, always complaining about his legs; Scratch, a talking Meowth in a tricorn hat, bossy ("Do the motto!"). A rhyming call-and-answer motto, bent, never quoted; they leave on "We're tumbling off agaaain!" (mission 8 on) |
| Townsfolk | Each has one small life of their own, a job, a worry or a joke, and talks about that first |

## 8. Content rules

- **No adult content anywhere in the demo** (adult mode comes after it). No innuendo, no adult-mode seeds.
- **Spoofs** follow story.md §9a: original names and looks, catchphrases bent, never quoted.
- **Canon first.** Where story.md speaks, the script follows it; where it's silent, the script invents in its spirit
  and lists the invention.
- **Pokémon** is the word people use. A partner is the Pokémon bonded to an Adept.
