# The day/night clock

**Decided (you, 17 Oct):** the game gets a day/night clock now (story decision 8, the alternative). Story decision 12
picked the clock's model (**decided 17 Oct as recommended**: four phases by walking and rest, never real time);
this page proposes the mechanics around it and lists what the clock changes. The rest is **proposed** until the
page's questions are answered.

## 1. The model (story 12, decided 17 Oct)

- **Four phases:** dawn, day, dusk, night. One clock for the whole game, shared by both crews; switching crews never
  moves it.
- **What advances it:** walking. A phase lasts a set number of hero steps on the field (proposed 600, about five
  minutes of walking); menus, battles and scenes don't count. Resting at an inn or a restoration point moves the
  clock to dawn. A scene may set the phase outright. **Never the phone's real time:** a player who plays at odd
  hours must never find content locked.
- **Where it shows:** rooms marked outdoor (`"outdoor": true` in the room's json) tint by phase; indoor rooms keep
  their look while the clock still runs. Proposed tints: dawn warm and pale, day none, dusk warm and darker, night a
  cool blue-grey.
- **A new game** starts at day. Mission 1's Keeping Night opener sets night for its scene and ends at dawn.

## 2. What reads it

- **Conditions.** Actor rows and scene steps get `{"show": "phase", "phase": "night"}` and `"not_phase"` beside the
  existing `while_set` / `while_clear` (engine `FieldActor.condition_holds`). An actor whose phase doesn't hold isn't
  there, like a flag-gated one; the room re-checks its actors when the phase changes.
- **Lantern Reef's night-only decks** (story §7, mission 6). The planks, booms and the ghost-lights exist only at
  night; by day the decks are closed and Vesper's arrival line says to wait for dark. A bunk on the Cutter lets the
  player sleep until night. The mission's check runs the reef at day (closed) and at night (open).
- **Kin habitats.** A room's encounter table may hold per-phase lists (`"day"`, `"night"`, with `"all"` as the
  default), so a species can live in a place only at night. The Kin entry's "time of day" returns to the Farer's Log
  ([menus-and-navigation.md](menus-and-navigation.md) §8.9) and the Chart's habitat marks say "night" where it applies.
- **Evolutions.** Time-of-day conditions become usable ([progression.md](progression.md) §4): Rockruff's forms by
  phase (day, dusk, night), and Espeon and Umbreon at a day or night level-up as well as by stone (the decided stone
  route stays).
- **Battle backgrounds.** Art decision 11 sets night per room; with the clock, outdoor rooms pick the night scene at
  night and indoor rooms keep their set background.
- **Adult mode** never touches the clock ([adult-mode.md](adult-mode.md) §1).

## 3. What it never changes

Prices, stats, EXP, drops, shop hours (shops are always open), saving, or the encounter rate itself; only which
species appear (decision 1 below).

## 4. Engine seams

- `GameState.clock` as `{"phase": "day", "steps": 0}`, saved with the game: `Save.FORMAT_VERSION` 2, with the first
  migration (a save without a clock loads at day).
- A `Clock` helper on `GameState`: `phase()`, `advance_steps(n)`, `set_phase(p)`, `rest()`, and a `phase_changed`
  signal. `Room` listens: re-tint (a `CanvasModulate` per outdoor room), re-check actor conditions, reload the
  encounter table.
- `FieldScript` steps: `{"clock": "night"}` sets a phase; `{"clock": "rest"}` is an inn's rest.
- Tests: a unit test for the step counter, the wrap and the migration; `mission6_check` at day and at night.
- **Order:** after the bug-fix slices, before mission 6's art pass. About a day of engine work.

## 5. Decisions for you

1. **What night changes besides the look.** Recommended: Kin habitats (some species only at night), the Lantern Reef
   night decks and the night battle backgrounds; never prices, stats or the encounter rate. [Night also raises the
   wild encounter rate by a quarter; night changes nothing but the look.]
2. **How the player sees the phase.** Recommended: no HUD element; the room tint shows it, the pause screen names it
   ("Dusk") and the Chart's habitat marks say "night". [A small sun or moon beside the compass; nothing but the
   tint.]
3. **Skipping ahead.** Recommended: an inn or a restoration point rests to dawn, and a bunk at home or on the ship
   offers "Sleep until dusk" / "until dawn", so no one waits for the reef. [Walking only, no skipping; a Psynergy or
   an item that turns the clock.]
4. **Scenes and the clock.** Recommended: scenes may set the phase (the Keeping Night opener, the reef's arrival at
   dusk), and the phase saves with the game under a new save format version with a migration. [Scenes never touch
   the clock; the player's walking is the only hand.]
