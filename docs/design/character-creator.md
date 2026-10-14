# Character creator (the hero)

**Decided (14 Oct 2026):** the player customises the main / first Adept (the hero, Crew 1's Earth lead) in a
character creator, including **gender** and **some cosmetic choices**.

Everything below is **Proposed** until you confirm it.

## What can be chosen

| Choice | Options | Notes |
|---|---|---|
| Name | Free text, up to 10 characters | Defaults to a placeholder name. Used in dialogue through `{HERO}` |
| Gender | Boy / girl, picking the body base | Changes the field sprite, battle sprite and portrait base |
| Pronouns | He / she / they, picked separately from gender | Dialogue uses tokens like `{HERO_SUBJ}`, `{HERO_OBJ}` and `{HERO_POSS}` |
| Skin tone | 6 presets | Palette swap |
| Hair style | 4–6 per body base | A separate sprite layer |
| Hair colour | 10 presets | Palette swap on the hair layer |
| Eye colour | 6 presets | Palette swap, mostly visible on the portrait |
| Outfit | 3 styles, all Earth-Adept themed (e.g. tunic + scarf, like the Golden Sun leads) | A layer; the colours come from the next row |
| Outfit colours | Primary and accent, 10 presets each | Palette swap |
| Scarf / accessory | Scarf, headband, none | A layer |

What the creator never changes:
- The hero's **element (Earth)**, stats, Psynergy and story role. It's cosmetic only.
- The rival and the other Adepts. They are fixed characters.

## When it appears

- **At the start of a new game,** before the opening battle against the rival. It shows a live preview of the
  field sprite (walking in 8 directions), the battle sprite and the dialogue portrait.
- **Afterwards:** cosmetics (not name or gender) can be changed at a mirror in the hero's house on the home island.
  Changing name or gender later is open question 4.

## How it works in the engine

- **Paper-doll layers:** body base, then outfit, accessory and hair, plus a separate face layer for portraits. Every
  layer shares the same animation frames: 8 directions for walk, run, idle and cast in the field, plus the battle
  poses.
- **Colours** come from a palette-swap shader. Each layer uses indexed colour ramps (skin, hair, eyes, outfit
  primary, outfit accent). The shader swaps those ramps for the chosen presets, so one sprite sheet covers every
  colour combination.
- **Saved data:** one appearance record, with name, gender, pronouns and one index per choice. That record feeds
  the sprite, the portrait and the dialogue tokens.
- **Until the graphics pass:** the boy and girl bases use existing Golden Sun field and battle sprites (for example
  the Isaac and Jenna bodies), with palette swaps only. The hair, outfit and accessory layers arrive with the
  graphics pass, when the sprites are remade. That pass plans every sheet as layers from the start, so the creator
  doesn't need a redraw later.

## Open questions

1. Are these the right cosmetic options, or do you want more or fewer (e.g. body type, a face or expression set,
   more outfits)?
2. Should pronouns be a separate choice, or follow gender (boy = he, girl = she)?
3. Should the hero's starter partner Pokémon also be picked in this screen, or later in the story?
4. Should name or gender be changeable after the start, or fixed for the run?
