# Mission 1, "The Keeping Night", as built (14 Oct 2026)

What the engine plays today for mission 1 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The cloud chat owns the story; this page is the hand-off so the lines can be rewritten in place.

## The flow

1. **Stonehollow.** A new game starts here with the hero alone. The Vault road leaves by the north gate; until the
   starter is chosen it is closed with a line ("Keeper Brann wanted a word first"). Keeper Brann's hatchery gives
   the first partner (Treecko, Torchic or Mudkip, placeholders until the story's own Kin are drawn up).
2. **The Vault's upper halls** (`vault_halls`, placeholder Sol Sanctum tiles). A corridor north is blocked by
   two Sentinel statues; Move slides one into a side doorway (flag `m1_sentinel_aside` when it reaches the cell).
   Either statue can also be pushed up the corridor into the chamber, which is fine for a first puzzle.
3. **The inner door.** Corvin waits in front of it. His lines, then the fight: Corvin (Squire, level 6, on
   Isaac's curve) with Larvitar (level 6). **If the party is knocked out, the standard defeat plays and the
   fight restarts from its start** with the party, bag and coins as they were (your decision, 14 Oct). Won: his
   closing lines, flag `m1_corvin_fled`, and he is gone from the room.
4. **Back in Stonehollow,** Commodore Ilse stands by the north gate (only while `m1_corvin_fled` is set). Her
   lines deputise the hero and hand over the **Lodestar** (own item 9003, a key item with no use yet); flag
   `m1_done`. Talking again gives her "be ready" line.

Checked end to end by `tools/mission1_check` in the engine (gate refused, starter, Vault, Move, a lost fight at
level 1 restarting with the party restored, the win, Corvin gone, Ilse, the Lodestar).

## Where the words live

All lines are our placeholders, written to the story's beats, in the engine's `maps_src/*/events.json`:

| Who | File | Keys |
|---|---|---|
| Keeper Brann, villagers, Maren | `maps_src/stonehollow/events.json` | `text` (and `text_after`) |
| The closed Vault road | `maps_src/stonehollow/events.json` | the warp's `else_text` |
| Commodore Ilse | `maps_src/stonehollow/events.json` | slot 14: `text` (before the Lodestar), `text_after` |
| Corvin | `maps_src/vault_halls/events.json` | slot 8: `text` (before the fight), `text_after` (after) |
| The Sentinels | `maps_src/vault_halls/events.json` | slots 9–10: `text` |

`{HERO}` and the pronoun tokens work in all of them; `{BOX}` breaks pages. The format is in `maps_src/README.md`.

## Placeholders and proposals (not decided)

- **No cutscenes yet.** The quake that opens the Vault, the hall splitting, Groudon stirring and Corvin's drop
  into the river are told in lines, not shown. The Keeping Night festival is one villager's line. A small script
  runner (walk, turn, shake, fade, sound) is the next engine piece for these.
- **Decided 15 Oct: light random encounters in the Vault.** That means a few weak battles, so the player learns
  the battle screen before Corvin. This replaces the earlier proposal of no encounters; the engine needs a
  low-rate, low-level encounter table for `vault_halls`.
- **Corvin's party and level** (6 + Larvitar 6) are the rival check's numbers; the first fight is meant to be
  losable and the retry rule carries it. Balance is open until more gear and the Set Pokémon line exist.
- **Looks:** Corvin wears Garet's field sprite and the Thief's battle sheet; the Sentinels are Sol Sanctum's
  statues; Ilse a villager sprite; the Vault halls are a clip of Sol Sanctum. All to be redrawn in the graphics
  pass.
- **The Lodestar** does nothing yet. The story gives it a role later (rumours, danger markers, §10); the item is
  in the bag so saves carry it.
- **Save and continue mid-mission:** flags and the bag persist; a pushed Sentinel's position does not (it stands
  where the room places it on re-entry), which only matters for the puzzle's look, not for progress.
