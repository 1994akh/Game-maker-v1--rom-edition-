# Mission 8, "The Tradewind Bazaar", as built (15 Oct 2026)

What the engine plays today for mission 8 (`docs/story/story.md` §7), where its words live, and what is still a
placeholder. The cloud chat owns the story; this page is the hand-off so the lines can be rewritten in place.
Built on Opus 5.5 while Fable 5.1 was rate-limited; the Fable model reviews it when it is back.

## The flow

1. **The hook.** Mission 8 plays after crew 1's second recruitment. Whichever of missions 5 (Sorrel) and 6
   (Vesper) finishes second, with mission 7 already done, ends with the handover: "Meanwhile, far to the east,
   Corvin's crew ties up at the Tradewind Bazaar." The game switches to **Corvin's crew** (Corvin, Tamsin and
   Nerissa).
2. **The bazaar** (`tradewind_bazaar`, placeholder tiles from Golden Sun 2's Lemurian ship at its pier). A floating
   market of lashed hulls in Eastwater. Arrival is a restoration point.
   - **Wynn** the cartographer joins with Ralts on the promise of a heist: the merchant on the next hull holds her
     debt note and her chart.
   - **Whirlwind** (Sky) is refused until Wynn is in the crew.
   - **Mind Read** (Sky) on the purser hears the strongbox combination he is trying not to say.
   - **Whirlwind** on the furled sail swings its spar across the gap to the merchant's hull, which becomes a plank
     bridge.
   - **The strongbox** opens with the code: Wynn's debt note, and her chart.
3. **The escape.** Down the gangway to the skiff. Wynn's chart shows the **Crown under the Pinnacle**, and a tower
   where sky-ships moored. Corvin: whoever built the Crown "didn't come from here". Both crews are now full, four
   Adepts each, and the game returns to **the hero's crew**, where they stood.

Checked end to end by the engine's `tools/mission8_check`, starting from Corvin's note in mission 6.

## Where the words live

| What | File | Where |
|---|---|---|
| The handover narration | `maps_src/eldergrove_heart/events.json` and `maps_src/lantern_reef/events.json` | the last `when` step of each ending |
| Arrival at the bazaar | `maps_src/tradewind_bazaar/events.json` | scene `bazaar_arrival` |
| Wynn joins | `maps_src/tradewind_bazaar/events.json` | scene `wynn_joins` |
| The purser's thought | `maps_src/tradewind_bazaar/events.json` | slot 8, its `mind_read` event's `text` |
| The sail and the strongbox | `maps_src/tradewind_bazaar/events.json` | slot 10; scene `strongbox` |
| The escape and the chart | `maps_src/tradewind_bazaar/events.json` | the gangway warp's `scene` |

## Engine pieces added

- **Whirlwind and Mind Read** work on our own actors. Whirlwind sets the target's event flag (the bridge is a gate
  that opens on it). Mind Read shows the target's hidden thought and sets its flag.
- **Gate tiles the map never used now draw.** The map importer only creates the tiles a map already uses, so a
  repainted bridge could come out invisible; the engine now creates a missing tile before painting it.

## Placeholders and open points

- **The bazaar** is one ship, not a hundred lashed hulls; the "merchant's hull" is its bow, cut off by painted sea.
- **Wynn** borrows a Golden Sun hero's field sprite and Ivan's Wind Seer battle curve until the graphics pass.
- **The code** ("seven, three, nine") is never typed in; holding the flag from Mind Read opens the box.
- **Mission 9** (the Fall of Fallhaven) is next.
