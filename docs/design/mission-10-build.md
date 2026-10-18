# Mission 10, "The Two-Earth Door", as built (15 Oct 2026)

What the engine plays today for mission 10 (`docs/story/story.md` §7 and §8), where its words live, and what is
still a placeholder. The engine side writes each mission's final script for your yes (demo decision 1); this
page is the hand-off so the lines can be rewritten in place. Built on Opus 5.5 while Fable 5.1 was rate-limited;
the Fable model reviews it when it is back.

## The flow

1. **Home.** Mission 9's finale lands both crews in Stonehollow. The refugee boats come in under Ilse's flag and
   the village makes room: Rimborn refugees now live there. Corvin asks for the inner door.
2. **The inner door** (`vault_halls`). Where they fought in mission 1, the two Earth leads open it together. It
   opens on a stair down to the sea.
3. **The Wayfarer** (`wayfarer`, placeholder: Golden Sun 1's Tolbi-bound ship). A Farer ship berthed in a sea cave
   under Stonehollow. Her engine drinks from open Wells; with the Flame Well open she can cross the Stillwaters.
   - The crews' **bags and coins merge** into one.
   - **Crew swapping unlocks.**
   - On deck: the helm (the same chart as the Kestrel's, until the sea map exists), the engine, the chart table with
     the Lodestar (it points nowhere yet), and the muster roll.
4. **The warded stair.** Behind the inner door, a stair spirals down toward the Earth Well behind a ward of red
   light. It stays shut.

Checked end to end by the engine's `tools/mission10_check`, from mission 9's landing to a crew swap.

## Crew swapping, as built

The rules come from `party-and-battle.md` §1 (crew logistics, proposed there):
- **The other crew waits on Marrow Isle.** Its lead stands in Stonehollow: Corvin while the hero's crew plays, the
  hero while Corvin's does.
- **Take over:** talking to the waiting lead offers to swap. The other crew takes over right where the player
  stands, and the crew that was playing waits there instead.
- **Trading Adepts** happens on the home island only: at the waiting lead, or at the Wayfarer's muster roll. Pick an
  Adept, then who comes back the other way, or nobody if the other crew has room. Each Adept takes their Set
  Pokémon along. Leads never move, and a crew never holds more than four.
- **Going home:** once swapping is unlocked, every innkeeper away from Marrow Isle offers "Home", so a crew without
  Teleport can't strand itself. Relay stones don't, because the other crew is in the same dungeon.
- **One bag, one purse** from here on; the Kin Garden was always shared.

## Where the words live

| What | File | Where |
|---|---|---|
| The refugees settle | `maps_src/stonehollow/events.json` | scene `refugees_settle`; slots 18 and 19 |
| Corvin before the door | `maps_src/stonehollow/events.json` | slot 20 |
| The waiting leads | `maps_src/stonehollow/events.json` | slots 21 (Corvin) and 22 (the hero) |
| The inner door | `maps_src/vault_halls/events.json` | scene `inner_door`; slot 12 (Corvin) |
| The warded stair | `maps_src/vault_halls/events.json` | slot 13 |
| The Wayfarer found | `maps_src/wayfarer/events.json` | scene `wayfarer_found` |
| The engine, the chart table, the muster roll | `maps_src/wayfarer/events.json` | slots 10, 11, 12 |

## Placeholder fixes along the way

- **Corvin no longer looks like the hero.** He walked as Isaac, the default hero's sprite. He now has his own field
  sprite, Golden Sun's Felix: masked in mission 1 (sprite 34), unmasked after (35).
- **Commodore Ilse and the Kestrel's mates** were drawn with a small white dog's sprite (104) since missions 1 and
  5. Ilse is now a woman in a long coat (122), the mates a sailor (129).

## Placeholders and open points

- **The Wayfarer** is one deck. Crew quarters and the galley (§8) aren't rooms yet, so there are no between-mission
  talks with each Adept.
- **The Lodestar** sits on the chart table; it wakes in mission 12.
- **Crossing the Stillwaters** isn't a destination yet. Mission 11, the maiden voyage, is next.
- **The home island growing** (shops, a shipwright, a daycare, the library, a visible Kin Garden) is not built
  beyond the two refugees.
- Sprites to export on a new machine: `python tools/export_gs_sprites.py 34 35 204 228 236 247 250`.
