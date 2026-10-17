# Menus and navigation: menus, pause, settings, saves, maps and the compass

From the menus review (15–16 Oct): five areas, each checked by an adversarial verifier, then a synthesis and a
critic, with the critic's corrections applied. Statuses:
- **Built:** engine main 0e18d55 does it.
- **Decided:** a doc records your answer.
- **Proposed:** a recommendation.
- **Open:** needs a device check or a decision.
- **Inferred:** Godot behaviour recalled, not yet checked.

Decided items come from:
- story.md §10, §13 and §14 (Q9, Q10, Q16);
- party-and-battle.md §1 and §6;
- DESIGN.md (function first, DexNav, auto-run);
- the 15 Oct battle-layout decision (CHANGELOG).

## 1. The short answer

**Built today:**
- A Start menu (Psynergy, Items, Status, Save, Close), the title and creator, the restoration-point Pokémon menu,
  one shared choice list (inn, relay stone, crew, trade, hatchery, voyage), the battle menus and the touch overlay.
- The title, creator, battle, dialogue box, field menu and touch overlay re-lay out when the phone folds (engine
  PR #53).

**Not built:** pause, settings, audio, any map, the Lodestar's function, danger stars, place names, an objective
line, the Farer's Log, save slots and autosave, scrolling menus, stick control in menus, tapping menu rows, Flee,
and the field Pokémon entry. Nothing pauses: under the menu, patrols keep walking and Reveal and Halt timers run
down. Android Back is unhandled and probably quits without saving.

**Proposed:**
- **Start menu.** It freezes the world, Golden Sun style: Psynergy, Pokémon, Items, Equip, Status, Log, Map, Save,
  Settings.
- **Pause box.** A small one for everywhere else: Resume, Settings, Return to title.
- **Settings and saves.** A Settings screen saved on the phone, separate from the game save. Three save files with
  autosave.
- **Maps.** No always-on minimap in rooms; a full-screen map of the room on a button; a Chart for the sea and
  regions (replacing today's "Set sail" list); an optional sea mini-chart.
- **Lodestar** as decided: world map and sea only, waking at mission 12.
- **Objective line.** One line with the crew's orders until then.

## 2. Screen architecture (proposed)

- **One screen stack.** A `Screens` autoload holds one layer; each screen is pushed onto it, and only the top screen
  gets input. That ends double input, such as the menu cursor also pushing a Move block. Today's menu methods stay
  as shims, so the end-to-end checks keep working.
- **Layers.** The built ones are kept and listed in one constants file:

  | Layer | Use |
  |---|---|
  | 4 | Field HUD: the Lodestar dial and the optional sea mini-chart (world map only) |
  | 5 | Battle (built) |
  | 8 | Room fog (built); must hide while a battle is up (bug) |
  | 9 | Fades (built) |
  | 10 | Message box (built) |
  | 11 | Choice list (built) |
  | 12 | Field menu and Pokémon menu (built) |
  | 15 | Banners (place name, new bearing); hidden while any menu is open; never take input |
  | 30 | The screen stack |
  | 50 | Touch overlay (20 today) |
  | 90 | Debug menu |

- **Theme and metrics.** A Godot Theme built in code from the built UiStyle. Widths are given in text columns, so a
  later font or picture change is one constant.
- **Shared widgets:**
  - MenuList: scrolling, paging, key repeat, tappable rows, greyed rows;
  - a detail pane, a prompt bar, a target picker, a yes/no prompt, a quantity picker, the compare table (equipment
    and items), and a naming keyboard driven by the game's own buttons (creator, mirror, nicknames);
  - a party session that rebuilds units after any partner or Set change, since the bond changes max HP.

### 2.1 Input (proposed)

| Action | Pad | Touch | Field | In menus | Battle | Scenes and dialogue |
|---|---|---|---|---|---|---|
| Move | D-pad and **left stick** | stick | walk | cursor (the stick in menus is new, with repeat) | cursor | Yes/No |
| Confirm | A | A, or tap a row | talk or act | pick | pick | advance |
| Cancel | B | B | hold to run | back one level | back one level | advance; No on Yes/No (new) |
| Start | Menu | START | Start menu | close the whole stack | pause box | pause box |
| L / R | LB / RB | L / R | cast the assigned Psynergy | previous or next page or tab | — | — |
| Auto-run | Y | a Settings row (a RUN button later) | toggle auto-run | — | — | — |
| Quick wheel | X | later | 8-slot wheel (later) | — | — | — |
| Map | L3 | Start → Map, or tap the dial | Map | — | — | — |
| Android Back | system | edge swipe | Start menu, which works as a pause since the world freezes | back one level | back; the pause box at top level | pause box |

Menus mark their input handled, so X and Y never toggle field actions underneath. Face buttons go by their labels by
default, and a "Position" option swaps confirm and cancel only. This supersedes CONTROLS.md's "back opens the pause
menu" for the free field.

### 2.2 Touch in menus (proposed)

- **Selecting rows.** Short command lists (pause box, inn, battle commands, Yes/No): one tap picks. Lists with a
  detail pane (items, Psynergy, Pokémon, Log, shop): the first tap shows details, the second picks. A drag scrolls.
- **Row size.** Rows are at least about 7 mm tall when touch is in use. On the cover that is about 19 UI units, so
  short command lists use two columns or a horizontal strip there, and every list scrolls. The 10-px row applies
  to pad play only.
- **Overlay modes:**
  - **Field:** everything shows.
  - **Menu:** the stick hides. A, B, L and R stay, and every layout keeps clear of them.
  - **Map:** the stick hides, and tap and drag pan the map.

  A floating stick, if chosen, captures only the lower-left quadrant, never the top strip or a tap target.
- **While paused.** The overlay keeps working, and tapping the message box advances it.

## 3. Menu tree (proposed unless marked)

```
TITLE  [built: Continue / New Game]
  Continue   -> the newest valid save of any file
  Load       -> files with summaries (if more than one is used)
  New Game   -> an empty file, or confirm overwrite -> Creator
  Settings
  Credits    -> asset licences (needed for CC-BY art)
  (hidden)   -> debug menu, controller test

FIELD (free field): Start / Back -> START MENU   [built: Psynergy, Items, Status, Save, Close]
  Psynergy -> Adept -> ability: heal or cure -> target; field verb -> close and cast; the chosen Adept pays
              Set to L / Set to R; Summon and Teleport pickers; item Psynergy grouped here
  Pokémon  -> Adept -> its 3 Set Pokémon and Standby (DESIGN.md's Set/Standby screen)
              Summary | Make partner (any time outside battle, decided) | Nickname
              Make partner is greyed for a mid-game legendary until Act III (decided Q9); on confirm the class
              and bond are recalculated and shown
              (To / From Kin Garden only at restoration points, built)
  Items    -> pockets (items-and-economy.md) -> Use | Info
              HP/PP/revive effects target Adepts only; Pokémon-use items (stones, Exp. Candy) target Set and
              Kin Garden Pokémon through the Pokémon screen
  Equip    -> equipment.md
  Status   -> a page per Adept; a Crews tab shows the waiting crew and guests (read only)
  Log      -> the Farer's Log (once given)
  Map      -> Area tab always; Chart tab once you have a ship
  Save     -> pick a file, confirm overwrite; greyed with the reason at sea, while surfing, or mid-cast
  Settings
  Side panel: coins, the objective line, an Adept summary

ANYWHERE ELSE (battle, scene, dialogue, back from another app): PAUSE BOX
  Paused: Resume | Settings | Return to title (asks: progress since your last save is lost)

PLACE SCREENS (by talking to someone; never in the Start menu)
  Inn and relay stone [built]: To <other crew> (relay stones, once the other crew is placed) | Rest | Pokémon |
                               Home (inns away from home, once crew swapping is unlocked) | Leave
  Ship helm / deckhand: the Chart in Sail mode (replaces "Set sail")
  Waiting lead / muster roll [built]: Take over | Trade Adepts -> a two-column trade screen that shows the rules
                               (leads can't be traded; guests after the Breaking can't change Set)
  Kin Garden: a browser with paging and sorting (summary, use an item, move to a Set at a restoration point)
  Mirror: the creator in cosmetics mode (decided, not built)
  Shop, forge: items-and-economy.md and equipment.md. Bounty board: §10

BATTLE [built: Attack, Psynergy, Pokémon, Unleash, Summon, Item, (Catch), Defend; revive window: Rouse, Item, Pass]
  Start -> pause box. A one-line help strip shows the description, cost or uses, and why a pick was refused.

OVERLAYS: the message box; toasts and banners; the level-up popup (decided);
  evolution "Which way? / Not now" and story-loss "Try again?" as choice prompts
```

## 4. Pause and what blocks what (proposed)

- **Two tiers.** The Start menu opens only on a free field; it is refused during scenes, which is built (engine
  PR #34). The pause box opens anywhere else.
- **Freezing.** Blocking screens freeze the world: patrols, timers and Reveal stop. Menus, input and the touch
  overlay keep running. Scene and battle waits must become pause-aware.
- **When the Start menu may open:** controls on, no scene, no dialogue, no Move or other effect in progress, no warp
  or fade. Today Start can open during Move Psynergy (a bug).
- **Folding** only releases held input and re-lays out. It never pops the pause box.
- **Leaving the app.** The pause box shows on return only after a real absence of about a second or more. If it is
  safe, the game autosaves when you leave.
- **Android Back** never quits: `quit_on_go_back` is set false and Back is routed as in §2.1. If the device test shows
  Back still closes the app, a small plugin is needed (open).
- **Screen sleep:** allowed on the title and in the pause box; kept awake in play.

## 5. Saves (proposed)

- **Safe writes.** A save is written to a temporary file, then renamed over the old one, with a backup kept. A
  failed read falls back to the backup. This lands before autosave.
- **Three files**, each with a manual save and its own rolling autosave.
  - Continue loads the newest valid save.
  - New Game takes an empty file or asks first.
  - A failed read shows an error. Today it silently starts a new game, and the next save overwrites the old file.
- **Header.** Each save carries the lead, place, crew, highest level, play time and date, for the title's summaries.
- **Autosave, at safe points only:** arriving in a room, after the post-battle pages, after a rest, after a scene
  ends, and on leaving the app. Never mid-scene, mid-battle, at sea or while surfing. A "Saved" mark shows for
  about a second.
- **Saving at sea.** It stays greyed until the location remembers the ship or surf mode; today a reload would probably
  put the hero on foot on water.
- **Character settings.** Name, gender, pronouns and appearance stay in the save (decided).

## 6. Settings (proposed; saved on the phone in `user://settings.cfg`, never in a save)

Every row previews live and is saved on change. Remapping asks "Keep these controls?" with a 10-second revert.

| Setting | Values | Default |
|---|---|---|
| Text speed | Slow, Normal, Fast, Instant | Normal |
| Battle animation speed | 1×, 2×, 3× (the decided "fast animations") | 1× |
| Battle text | Wait for A / Auto (story text never auto-advances) | Wait |
| Repeat last turn | a battle command (decided, party-and-battle.md §6) | on |
| Run style | Hold B / Auto-run (Y toggles) | Hold B |
| Autosave | on / off | on |
| Objective and place banners | on / off | on |
| Sea mini-chart | on / off | off |
| Lodestar dial | on / off | on |
| Volume: music, effects, voice | 0–10 (hidden until audio exists) | 6 / 8 / 6 |
| Face buttons | by label / by position | by label |
| Remap controls, controller test | per action | — |
| Rumble | on / off | on |
| Touch size, opacity, left-handed, stick type, haptics, edge inset | | Auto, 55%, off, fixed, on, Auto |
| Orientation | decision S-6 | |
| Window colour | presets, high contrast | |

Left out on purpose: difficulty, language, frame rate, and a colour-blind filter. Instead, colour never carries
meaning alone: danger is a count of stars, and HP shows as numbers.

## 7. Fold and unfold layouts

| Posture | View in UI units | Form |
|---|---|---|
| Base | 240×160 | list plus side box (built) |
| Cover, landscape | about 373×160 (docs say 420×180; open until measured) | wide: list, detail and preview in three panes |
| Inner, landscape | about 240×216 (docs say 242×218; open) | square: list and detail on top, a strip below |
| Inner held as a book, cover portrait | only if orientation isn't locked (decision S-6) | |

- **One layout path.** Every screen has one layout function, and every screen on the stack re-lays out when the view
  size changes.
- **Which signal fires.** The engine's screen rule and PR #53 disagree about which signal fires on a fold. The
  diagnostics counter on the phone settles it, and a size-polling fallback stays until then.
- **Tests.** The layout test runs every screen at all postures and checks that every box stays inside the view. That
  includes the choice and Pokémon menus, which don't re-lay out today.

## 8. Navigation

### 8.1 Data (proposed; no save-format change)

- **Visited flags.** `visited:<room path>` is set on entering a room. It uses the full path, because GS1 and GS2
  share room names.
- **Rumours and known places** are flags set through dialogue (decided Q10).
- **The Lodestar** has stage flags and a `lodestar_target` field ("" means the story goal).
- **Data files:**
  - `data_src/places.json`: name, region, chart position, rooms, a hand-set danger of 1–5 (decided), landmark,
    voyage and Teleport targets. voyages.json folds into it.
  - `data_src/regions.json`.
  - `data_src/goals.json`: per mission and crew, with a condition, place and text. Rows for missions 1–10 can be
    written from today's flags, and a check tool validates them.
- **The Log's records** (Kin and enemies seen, caught and defeated) start being kept now. Sightings missed now can't
  be rebuilt later.

### 8.2 Mini map (decision N-4)

- **In rooms, none always on.** One screen already shows 20–93% of a built room; a whole room in a corner would get
  about 1.4 px per cell.
- **At sea and on the world map:** an optional scrolling mini-chart, off by default. It hides while a banner shows,
  and banners sit at the bottom centre when it's on.

### 8.3 Area map (decision N-6)

- Opens with the map button in a room, Start → Map, or a tap on a place banner. Available from mission 1.
- It is drawn from the room's live collision grid on the player's layer.
- **Labels:** exits by their target (a lock and its text if closed), services (inn, chart, relay stone, the other
  crew's lead, muster roll, hatchery), you, and the goal.
- **Never shown:** chests, hidden actors before they're revealed, quest and battle actors, or any room under fog. A
  room can opt out (mazes, the Hollow).
- The header shows the place name only; danger stars stay on the Chart and world map (decided Q10).
- The visited flags and the map-button wiring need no decision; the map's contents are decision N-6.

### 8.4 The Chart (Map → Chart tab)

- **Pages.** Act I builds the Calm first, with edge markers toward Eastwater and the rim. The Cloudreach comes at
  m17, the Deep Shelf at m18, then the Farside. Variants appear at the midpoint and after the ending (decided).
- **Place states:** unknown, rumoured (?), known (name and 1–5 danger stars), visited, fully explored.
- **Landmarks** show once their region is known (decided).
- **Choosing a place:**
  - Set bearing.
  - Sail here (from a helm or deckhand only).
  - Teleport here, only if the active crew knows Teleport or holds the Teleport Lapis. When Teleport arrives is open.
  - Details.
  - A place you can't reach says why.
- **The look:** drawn now from the world's terrain grid with Kenney Cartography icons (CC0, on disk); a painted chart
  comes in the art pass.
- Golden Sun's Angara placeholder isn't charted. Stonehollow's west gate is progression.md decision 4.
- **Fast travel.** The built innkeeper "Home" warp is a second fast travel next to Teleport, while field-abilities.md
  says one is enough. That is decision N-13.

### 8.5 The Lodestar (behaviour decided, form proposed)

- **Stages** (story.md §10: "mission 12 is its first full use"):
  - **Act I, dormant.** A key item with no needle; the Kestrel's chart marks the story destination.
  - **Mission 10.** Its cradle on the Wayfarer "points nowhere yet", which is where it stirs.
  - **From mission 12, full use.** It points at the story goal by default and can be retargeted.

  story.md line 175 still says the Lodestar gives bearings in Act I, which conflicts with lines 238 and 528. That's
  for the cloud chat to settle; a third stage would be a question for you.
- **Default target:** the current main goal for the active crew. When several are open, the nearest; the Chart lists
  them all (decision N-3).
- **Aim:** a straight bearing to the goal place, with no routing through warps.
- **Where it shows:** the world map and sea only (decided Q10), as a 24×24 dial at the top centre. It hides during
  battles, dialogue, scenes and menus. Near the goal it spins and glows.
- **Retargeting** (story: "tap it"): tapping the dial opens the Chart in Set-bearing mode. On a pad, use the map
  button on the world map, or Start → Map → Chart. "Story bearing" resets it.
- **Crew 2** never has the Lodestar before mission 10 (bags are per crew), so it relies on the objective line.
- Torro's "The Wrong Way" side story needs a scripted in-room bearing, or the beat rewritten.

### 8.6 Objective line (decision N-7)

- One line of about 40 characters from goals.json: the crew's orders, per crew in the interludes.
- It shows at the top of the Start menu's side panel and in the area map's footer, and as a banner when the goal
  changes.
- Side contracts and heart quests go in the Log, not here.

### 8.7 Place-name banner

When you enter a new place, its name fades in for about 2 seconds, as Golden Sun's map-name window does. On the
world map it fires when the region changes and adds the danger stars. It has a settings toggle.

### 8.8 Landmarks on a small screen (decision N-10)

The decided "camera pulled back to see the nearest landmark" can't hold at 240–373 px wide, since the world is
4,096×5,120 px. Instead, each off-screen landmark of a known region gets a tiny edge marker on the world map. A
zoom-out can come after the 480×320 picture.

### 8.9 The Farer's Log (sections decided, screen proposed)

- **Tabs:** Kin, Bestiary, Charts, Relics and Cultures (the four decided sections), plus the Guild Ledger (decided) and Bearings (main
  goals, heart quests, taken contracts). Each tab has a completion %.
- **DexNav** is decided (DESIGN.md). Proposed form: "Search here" on a Kin entry, with habitat marks on the Chart. A
  separate DexNav screen with chains is decision N-9.
- **Story notes** (Corvin's note, the Ledger) sit in the Key Items pocket and are cross-listed under Relics.
- Kin's "time of day" is dropped until a clock exists.

## 9. Battle menu

- **The fix, no decision needed.** The 15 Oct decision puts the menu at the bottom centre, hidden while words play
  and clear of the touch stick and buttons. Today it runs off the bottom of the screen, showing 4 of its 8 commands,
  and that breaks the decision. The fix:
  - anchor it at the bottom and grow it upward;
  - scroll it;
  - keep it clear of the overlay;
  - add a help strip showing why a pick was refused.

  The art Phase 1 build is landing this.
- **Questions:** a Golden Sun icon row later (decision B-1), and Flee (decision B-2).

## 10. Screens still to specify

These came up in the critic's pass and aren't designed yet:
- **Credits:** on the title and in Settings for asset licences, plus the ending credits that return you to Marrow
  Isle "the day after" with a save prompt (decided Q19).
- **Debug menu** for testing on the phone: warp, flags, jump to a mission, give items or coins, toggle encounters,
  the fold counter.
- **Kin Garden browser** for hundreds of Pokémon.
- **Bounty board** at the Freeport Guild: contracts and timers, your bounty level, rival-hunter warnings (decided
  §9b, Q17).
- **Mini-games** from Act II (decided Q18): the language puzzle, the Dodo Derby, the Glimmer Saucer.
- **Help:** a controls page showing the current bindings and the touch layout.

## 11. Bugs found

**Fixes need no decision:**
- **The battle menu shows only 4 of its 8 commands**, and the Psynergy, item and target lists are cut off too; START
  covers a row. Being fixed in the art Phase 1 build.
- **The choice and Pokémon menus are placed only when they open.** Unfolding with one open leaves it off-screen.
- **Field Psynergy casts from, and charges, the first Adept who knows it**, whichever row you picked. Not enough PP, or
  nothing to heal, fails silently.
- **Start can open during Move Psynergy**, so the menu cursor also pushes the block.
- **The fog layer draws over the battle**, so every battle in Lantern Reef is under a 50% veil.
- **The world keeps running under menus and dialogue**, so a patrolling guard can catch you as the menu closes.
- **Saves are written in place with no backup**, so a crash mid-write destroys the save.
- **An unreadable save makes Continue silently start a new game**, and New Game then Save overwrites without asking.
- **Saving at sea or while surfing** probably reloads you on foot on water (to confirm with a test).
- **Android Back is unhandled** and probably quits without saving (device check).
- **The analog stick can't move any menu cursor**, and holding a direction doesn't repeat.
- **Field item targets and Status list the bonded and benched Pokémon**, and Status overflows with no scrolling.
- **With nothing to react to, R casts Defog or Reveal anyway**, wasting PP.
- **A refused battle command silently redraws the menu**, and B from a target list skips back to the command menu.
- **The creator's name box traps all input until Enter**, so a pad-only player can't leave it.
- **The touch overlay covers menu text at 240×160:** L and R over titles, START over battle rows, B over "No".
- **Chest and quest flags use only the room's file name**, and GS1 and GS2 share some names, so flags would collide.
- **Group-scoped flags clear on every room entry** instead of when the place changes. This waits for places.json.

**Doc conflicts** (for you or the cloud chat):
- story.md line 175 against lines 238 and 528 on the Lodestar in Act I.
- party-and-battle.md §6's per-partner tactics under bonded partners (decision B-4).
- DESIGN.md's "Pokémon menus in battle" against the decided 15 Oct Golden Sun-style battle boxes.

## 12. Decisions for you

Recommended first. The alternatives are in brackets.

Answered on the decision page: accepted items are marked **Decided** with the date, the rest **To talk over**.
1. **Decided (16 Oct):** **N-0, Start menu.** Recommended: Psynergy, Pokémon, Items, Equip, Status, Log, Map, Save, Settings, Close, with Log
   and Map appearing once unlocked; a list now, Golden Sun's icon bar in polish. [Golden Sun's four plus System;
   Equip inside Items.]
2. **Decided (16 Oct):** **S-1, pause.** Recommended: two tiers, the Start menu on a free field and a pause box elsewhere. Back never quits,
   and inside menus it goes back. [Settings only in the Start menu and title; Back asks "Quit?".]
3. **Decided (16 Oct):** **S-2, freeze the world under the Start menu.** Recommended: yes, as Golden Sun does. [Keep it running and only
   block your controls, as today.]
4. **Decided (16 Oct):** **S-3, saves.** Recommended: 3 files, each with a manual save and an autosave, safe writes, summaries on the title.
   [One slot plus a suspend save; 3 manual slots only.]
5. **Decided (16 Oct):** **S-4, autosave timing.** Recommended: safe points only, on by default. [Only when leaving the app; only at
   restoration points; never.]
6. **Decided (16 Oct):** **S-5, first Settings screen.** Recommended: the table in §6. [Text speed and touch opacity only; the full
   CONTROLS.md set with a touch layout editor.]
7. **Decided (16 Oct):** **S-6, orientation.** Recommended: lock to landscape until the portrait probe. [Allow any orientation and build
   book and portrait layouts for every screen.]
8. **Decided (16 Oct):** **S-7, back up saves off the phone.** Recommended: turn on Android backup, so saves follow your Google account.
   [An "Export saves" action; accept that an uninstall wipes saves.]
9. **Decided (16 Oct):** **B-1, battle menu shape.** The fix in §9 is a bug fix of your 15 Oct decision. The question is only a Golden Sun
   icon row later. Recommended: later, placed above the touch stick. [A two-column grid of words.]
10. **Decided (16 Oct):** **B-2, running from battles.** Recommended: yes, from random and wild battles only, with Golden Sun's flee chance
    on Adept levels. [No running; running only with an item.] Same as progression.md decision 2.
11. **Decided (16 Oct):** **B-3, after losing a story fight.** Recommended: "Try again?"; No returns to the last restoration point, with the
    fight still waiting. [Keep the endless restart.] Same as progression.md decision 2.
12. **Decided (16 Oct):** **B-4, partner tactics.** party-and-battle.md §6 decided optional per-partner tactics. Bonded partners act only in
    their revive window, so recommended: move the tactics option to Adepts (an "Auto" setting per Adept), keeping
    "repeat last turn" and fast animations. [Drop tactics; keep them for the revive window only.]
13. **Decided (16 Oct):** **T-1, touch selects rows.** Recommended: one tap for short lists, first tap previews and the second picks where
    there's a detail pane. [Stick and A only; always one tap.]
14. **Decided (16 Oct):** **T-2, Start inside a submenu.** Recommended: Start closes the whole stack, B goes back one level. [Start goes
    back one level.]
15. **Decided (16 Oct):** **N-1, the Lodestar before mission 12.** Recommended: dormant in Act I, stirring at the Wayfarer (m10), full use
    from m12, as story §10 says. [A needle from mission 3; a third "points home only" stage at m12.]
16. **Decided (16 Oct):** **N-2, pointing it at a marker.** Recommended: pick the marker on the Chart; tapping the dial opens the Chart.
    [Tapping the dial cycles targets.]
17. **Decided (16 Oct):** **N-3, default target with several open goals.** Recommended: the nearest. [The last one you picked; the lowest
    mission number.]
18. **Decided (16 Oct):** **N-4, mini map.** Recommended: none always on in rooms, a full-screen area map on a button, an optional sea
    mini-chart. [An always-on corner minimap; one in Settings, off by default; no map at all.]
19. **Decided (16 Oct):** **N-5, danger stars and rumours.** Recommended: on the Chart, plus a name-and-stars banner on the world map
    (decided Q10 keeps them to world-map UI). [Icons on the walkable world map.]
20. **Decided (16 Oct):** **N-6, the area map's contents.** Recommended: §8.3. [Also chests; cell-by-cell fog of war.]
21. **Decided (16 Oct):** **N-7, objective tracking.** DESIGN.md calls a Mission Log "not a must-have". Recommended: the one-line objective
    plus a small Bearings page in the Log. [Lodestar and Guild Ledger only; Unbound's full Mission Log.]
22. **Decided (16 Oct):** **N-8, Log pages.** Recommended: the four decided sections plus Guild Ledger and Bearings. [Strictly the four.]
23. **Decided (16 Oct):** **N-9, DexNav's form.** DexNav is decided. Recommended: "Search here" on Kin entries plus habitat marks on the
    Chart; a separate screen with chains later. [Unbound's DexNav screen now.]
24. **Decided (16 Oct):** **N-10, landmarks on a small screen.** Recommended: edge markers. [A world-map zoom-out after the 480 picture.]
25. **Decided (16 Oct):** **N-11, where Lantern Reef sits.** Recommended: north-west of Meridia, which fits both the world sketch and
    mission 6. [Due north; due west.] Probably the cloud chat's call.
26. **Decided (16 Oct):** **N-12, L/R shortcuts.** Recommended: assignable in the Psynergy menu (default L = Move, R = the newest verb), and
    an 8-slot wheel on X later. [Keep today's fixed shortcuts.]
27. **Decided (16 Oct):** **N-13, fast travel.** The built "Home" warp at inns is a second fast travel next to Teleport. Recommended: keep
    Home as a deliberate exception for crew logistics, and keep Teleport's timing open. [Remove Home once Teleport
    exists.]
28. **Decided (16 Oct):** **C-1, pronouns at the mirror.** Recommended: allow changing pronouns at the mirror; name and gender stay
    permanent. [Keep pronouns fixed, the current decision.]
