# Godot 4.7 ecosystem survey for the Golden Sun + Pokémon Android build

Checked 2026-10-13, using 38 tool calls. Nothing was downloaded or cloned.

- **VERIFIED** means I saw it today on the GitHub API, the README, the official docs or the store page.
- **INFERRED** means it comes from my own knowledge or from secondary sources.
- Licence, last push and latest release come from the GitHub API unless a row says otherwise.

Godot 4.7.2-stable exists: it was released 2026-08-18 (VERIFIED).

## 1. Importing Tiled .tmj maps
| Resource | Licence / last activity | Works with 4.7? | What it saves | Verdict |
|---|---|---|---|---|
| **YATI**, https://github.com/Kiamo2/YATI | MIT. v2.2.10 released 2026-10-05 (VERIFIED) | README says it was tested with Godot 4.7.2 and Tiled 1.12.2 (VERIFIED) | Imports .tmx and .tmj, all layer and object kinds, custom properties and class, tile collisions, tile animations and templates. Works as an editor import or as a runtime package; there is also a C# build (VERIFIED). Our warp, event and NPC properties map through class and custom properties. A post-import hook script is INFERRED: check Reference.md. | **ADOPT.** It replaces the importer we would otherwise write. Turn off "Use multiple threads" in the import settings, or Godot can freeze or crash on large maps (VERIFIED). |
| Tiled's built-in Godot 4 export, https://doc.mapeditor.org/en/stable/manual/export-tscn/ | Tiled has no SPDX licence on file; repo active 2026-10-12 | Godot 4 TileMap | Objects export only if they have a `resPath` property. Arbitrary custom properties export only on tiles, as Custom Data Layers (VERIFIED). | **SKIP.** It drops object metadata we need. |
| vnen/godot-tiled-importer | MIT, last push 2023-03-15 | Godot 3 only | — | **SKIP** |

## 2. Unit testing and headless CI
| Resource | Licence / last activity | Works with 4.7? | What it saves | Verdict |
|---|---|---|---|---|
| **GUT**, https://github.com/bitwes/Gut | MIT (per the README; the API shows no licence). Tags v9.7.1 and v9.7.0 exist; the latest release object is v9.6.1 from 2026-07-09 (VERIFIED) | Use v9.7.1 from the `godot_4_7` branch (VERIFIED) | Has a command-line runner and JUnit XML export, enough for the formula-parity tests against our Python reference (VERIFIED) | **ADOPT.** It is already in the plan. |
| gdUnit4, https://github.com/godot-gdunit-labs/gdUnit4 | MIT. v6.2.2 released 2026-10-07 (VERIFIED) | v6.2.x supports 4.7 (VERIFIED) | A scene runner that simulates touch, mouse, keys and actions; mocks and spies; HTML and JUnit reports. There is an official GitHub Action, gdUnit4-action, at v1.3.2 (MIT). Dialogic runs its own tests on gdUnit4 (VERIFIED). | **REFERENCE.** Switch to it only if we need scripted touch or UI tests that GUT can't do. |
| chickensoft-games/setup-godot | MIT. v2.4.3 released 2026-10-01 (VERIFIED) | Any version | Installs headless Godot on GitHub runners, so tests run in CI | **ADOPT**, but only if we use CI |
| abarichello/godot-ci | MIT. Image `4.7.2-stable` published 2026-08-18 (VERIFIED) | Exactly 4.7.2 | A Docker image that can export Android builds in CI | **REFERENCE.** Local exports are enough for a personal app. |

## 3. Dialogue and cutscenes
| Resource | Licence / last activity | Works with 4.7? | What it saves | Verdict |
|---|---|---|---|---|
| **Dialogue Manager**, https://github.com/nathanhoad/godot_dialogue_manager | MIT. v4.1.0 released 2026-09-04, pushed 2026-10-13 (VERIFIED) | v4 needs Godot 4.6 or later (VERIFIED). 4.7 is not named but should be fine (INFERRED). | Dialogue is written as script-like text files, so our extracted GS text can be converted into `.dialogue` files by a script. Has branching and conditions; there is an example with portraits and emotes, plus a C# wrapper (VERIFIED). Mutations with `await` can drive cutscene steps (INFERRED). | **ADOPT.** Build a custom balloon in the GS portrait-box style, and drive scripted events with AnimationPlayer plus a small command-queue runner. |
| Dialogic 2, https://github.com/dialogic-godot/dialogic | MIT. Latest is 2.0-alpha-20 from 2026-07-21; needs Godot 4.5 or later (VERIFIED) | godot-open-rpg ships it under 4.7.2 (VERIFIED) | A visual timeline editor and a character/portrait editor | **SKIP.** It is still alpha, the README warns the API can change between releases, it is built around visual novels, and generating its content from our text is harder. |

## 4. Music: MIDI + SF2 played live in Godot, or rendered offline
| Resource | Licence / last activity | Works with 4.7? | What it saves | Verdict |
|---|---|---|---|---|
| **FluidSynth CLI, rendering offline to OGG**, https://github.com/FluidSynth/fluidsynth | LGPL-2.1, pushed 2026-10-11 (VERIFIED) | No engine dependency | Render each song once with something like `fluidsynth -ni -F out.wav -r 44100 game.sf2 song.mid`, then encode to OGG (INFERRED syntax). Set `AudioStreamOggVorbis.loop_offset` to the loop point. AudioStreamInteractive can handle intro→loop and battle transitions (INFERRED, it exists since 4.3). This costs no CPU and needs no native library on the phone. | **ADOPT** |
| arlez80 Godot MIDI Player 4, https://store.godotengine.org/asset/arlez80/godot-midi-player-4/ | MIT. v4.5.0, store page updated 2026-05-28, marked "unstable" (VERIFIED) | Store lists 4.2 to 4.6.2; 4.7 is unconfirmed | A pure-GDScript synth that loads the soundfont. Possible use: a sound-test room or tempo changes at runtime. Its CPU cost on mobile is likely high (INFERRED). | **REFERENCE** |
| gongpha/godot-midi | MIT, 4 stars, no release (VERIFIED) | Unknown | — | **SKIP** |
| nlaha/godot-midi | MIT, 0.3.0 (VERIFIED) | 4.2 or later | Parses MIDI events only; it does not synthesise sound | **SKIP** |
| howhow2315/godot-fluidsynth (4.7 or later, 0 stars) and pattlebass/fluidsynth-gdextension (experimental, Unlicense) | Pushed 2026-09/10 (VERIFIED) | — | Too new and unproven | **SKIP** |

## 5. Android: foldables and plugins
| Resource | Licence / last activity | Works with 4.7? | What it saves | Verdict |
|---|---|---|---|---|
| **Godot-Android-Plugin-Template**, https://github.com/m4gr3d/Godot-Android-Plugin-Template | MIT, pushed 2025-12-11 (VERIFIED) | Godot 4.2+ v2 plugins (VERIFIED) | A starting point for our own small Kotlin plugin (my estimate is about 100 lines). It would wrap Jetpack WindowManager 1.5.1, the current stable; 1.6.0-alpha03 is the newest preview (from release notes found by search). The plugin would emit posture and hinge state from FoldingFeature, plus which screen is active (cover or inner). | **ADOPT** |
| GodotAndroidFoldableScreen (Lunatik Games), https://lunatik-games.itch.io/godot-android-foldable-screen | Paid ($5), closed source, no redistribution. Supports Godot 3.5.3, 4.0 and 4.1.1 only; no date shown (VERIFIED) | No | Flat, Book and Tabletop postures only; no cover-screen handling | **SKIP** |
| Godot 4.7.2's own Android manifest | Seen at the 4.7.2 tag (VERIFIED) | — | `configChanges` covers screenSize and screenLayout, so a fold or unfold doesn't restart the game. But the template also sets `resizeableActivity="false"` and locks to landscape. | **ACTION.** Use the Gradle build template and set `resizeableActivity="true"`. Listen for `NOTIFICATION_WM_SIZE_CHANGED`, because `Viewport.size_changed` doesn't fire in viewport stretch mode (forum, VERIFIED). Android 16 ignores orientation and resizability locks on screens at least 600 dp wide when the app targets API 36 (INFERRED), so plan for a portrait inner screen. |

## 6. Touch controls
| Resource | Licence / last activity | Works with 4.7? | What it saves | Verdict |
|---|---|---|---|---|
| **Built-in `VirtualJoystick` node (new in 4.7)**, https://docs.godotengine.org/en/stable/classes/class_virtualjoystick.html | Engine (MIT) (VERIFIED) | 4.7 docs (VERIFIED) | Fixed, dynamic and following modes; deadzone and clamp settings. It fires InputMap actions directly and has pressed, released, flicked and tapped signals. 8-way movement just reads the same actions. Use the built-in TouchScreenButton for A/B/L/R/Psynergy (INFERRED). | **ADOPT** |
| MarcoFazioRandom/Virtual-Joystick-Godot | MIT, last push 2025-01-19 (VERIFIED) | — | Replaced by the built-in node | **SKIP** |
| Virtual Joystick DX (asset library) | Says "4.6+, tested on 4.7" (search listing, not opened) | — | Haptics and a D-pad style | **SKIP**, unless we need haptics |

## 7. Input remapping and gamepad databases
| Resource | Licence / last activity | Works with 4.7? | What it saves | Verdict |
|---|---|---|---|---|
| nathanhoad/godot_input_helper, https://github.com/nathanhoad/godot_input_helper | MIT. v4.7.0 released 2025-06-08, no push since (VERIFIED) | Godot 4; 4.7 unverified | Detects the active device and joypad type (useful for switching button icons), gets and sets action bindings, rumble | **REFERENCE.** Copy the detection logic; save bindings ourselves with InputMap and ConfigFile. |
| mdqinc/SDL_GameControllerDB | Zlib, pushed 2026-10-02 (VERIFIED) | — | Godot 4.5+ uses SDL3 only on desktop. On Android it uses its own controller code (docs, VERIFIED), so this database doesn't apply to the phone. Test the Backbone and Xbox pads on the device; `Input.add_joy_mapping` is available if a pad maps wrongly. | **SKIP** |

## 8. Pixel-perfect scaling, including the 21:9 cover screen
Nothing to install; the engine settings cover it. The 4.7 docs recommend Stretch Mode `viewport`, Aspect `expand` and Scale Mode `integer`, with Controls anchored (VERIFIED). Integer mode rounds the scale down, so leftover pixels become thin bars.

The screen sizes below are INFERRED, and the arithmetic assumes the GBA's 240×160 base:
- **Cover screen, 2520×1080:** scale 6, giving a 420×180 view with no bars.
- **Inner screen, 2184×1968:** scale 9, giving 242×218 with 6 px of margin.

With `expand`, the cover screen simply shows more world to the sides, which also gives the 8-versus-6 battle layout more room. **Verdict: ADOPT the built-in settings; SKIP pixel-scaling addons.**

## 9. Save systems
- **Our own versioned JSON or ConfigFile saves (built-in): ADOPT.** Store a schema number, migrate old saves forward, and test it in GUT. Restoration points become snapshots of the same dictionary.
- **derkork/godot-safe-resource-loader** (MIT, pushed 2026-04-28, VERIFIED): **REFERENCE.** Only needed if saves are `.tres` files, which can contain scripts (INFERRED).
- **AdamKormos/SaveMadeEasy** (MIT, last push 2025-01-01, VERIFIED): **SKIP.**

## 10. AI and state machines
- **LimboAI**, https://github.com/limbonaut/limboai (MIT, v1.8.1 released 2026-08-20). The release ships a GDExtension for 4.6 or later, Godot 4.7.2 Android libraries and export templates (VERIFIED). It has behaviour trees, a hierarchical state machine, a blackboard, a visual debugger, and tasks can be written in GDScript (VERIFIED). **ADOPT when AI work starts**, using the GDExtension, for partner Pokémon and field enemies. Golden Sun and Pokémon battle choices themselves are weighted tables, so they don't need a behaviour tree.
- **bitbrain/beehave** (MIT, v2.9.3 released 2026-08-18, VERIFIED): **SKIP.** It overlaps LimboAI.
- **derkork/godot-statecharts** (MIT, v0.22.5 released 2026-06-26, VERIFIED): **REFERENCE** for the player's field states (walk, cast, Surf, Dive, climb). A plain enum state machine may be enough.

## 11. Turn-based RPG frameworks and open-source projects worth reading
- **gdquest-demos/godot-open-rpg**, https://github.com/gdquest-demos/godot-open-rpg (MIT code, 3.0k stars, pushed 2026-10-13; README says it needs Godot 4.7.2; uses Dialogic) (VERIFIED). **REFERENCE.** Read its combat turn queue and battler/action structure, and how overworld objects trigger events. It's a learning project, not a framework.
- **ramokz/phantom-camera** (MIT, pushed 2026-10-07, VERIFIED): **REFERENCE.** Useful if the battle scene uses Golden Sun's rotating pseudo-3D camera.
- **Other turn-based addons: SKIP.**
  - LeviOS31 JRPG addon: 6 stars.
  - Cute-Fame-Studio/3D-TurnBasedCombat: 3D, Godot 4.0–4.4.
  - TurnBasedSystem: C# only.
  - All from search listings.
- **viniciusgerevini/godot-aseprite-wizard** (MIT, pushed 2026-08-17, VERIFIED): **ADOPT later** for the graphics remake if we draw in Aseprite.

## 12. Pokémon-like and Golden Sun-like Godot projects
- **Arman-HKB/PokemonEmeraldGodot** (GPL-3.0, 18 stars, pushed 2026-05-26, Godot 4; has no battle system, VERIFIED): **REFERENCE** for overworld feel only, such as the frame-by-frame ledge-jump timing. Its code is GPL.
- **acedogblast/Project-Uranium-Godot** (MIT, last push 2025-03-14, VERIFIED): **SKIP.** Its Godot version is uncertain (INFERRED to be 3.x-era).
- **SKIP:**
  - OpMonTeam/OpMon: no clear licence, "not really playable", last push 2025-09.
  - Mu-L/PokeBuilder: no licence, 0 stars.
  - BrunoSalasR/Nexos.
  - whomera Monstercollector demos: Godot 4.3.
- **Golden Sun in Godot:** the only one I found is badnewsgoonies-dot/vale-village-v2-godot (no licence, 1 commit, 0 stars, Godot 4.3, VERIFIED): **SKIP.** goldensun_html5 is still the reference.
- **GoldenSunHacking/Psynergy** (GPL-3.0 modding tools, last push 2023-05, VERIFIED): **SKIP.** Our own extraction already covers it.

## Helper script
The metadata checks used a small script I saved for reuse: (a local scratch script, not kept). Run it as `python -I gh_repo_meta.py [--releases] owner/repo ...`. It uses the unauthenticated GitHub API, which allows 60 requests per hour.

Sources:
- [YATI](https://github.com/Kiamo2/YATI)
- [Tiled Godot 4 export](https://doc.mapeditor.org/en/stable/manual/export-tscn/)
- [GUT](https://github.com/bitwes/Gut)
- [gdUnit4](https://github.com/godot-gdunit-labs/gdUnit4)
- [Dialogue Manager](https://github.com/nathanhoad/godot_dialogue_manager)
- [Dialogic](https://github.com/dialogic-godot/dialogic)
- [LimboAI](https://github.com/limbonaut/limboai)
- [godot-open-rpg](https://github.com/gdquest-demos/godot-open-rpg)
- [VirtualJoystick docs](https://docs.godotengine.org/en/stable/classes/class_virtualjoystick.html)
- [Multiple resolutions docs](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html)
- [Godot 4.7.2 AndroidManifest](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/platform/android/java/app/src/main/AndroidManifest.xml)
- [Controllers docs](https://docs.godotengine.org/en/latest/tutorials/inputs/controllers_gamepads_joysticks.html)
- [Foldable plugin (itch)](https://lunatik-games.itch.io/godot-android-foldable-screen)
- [Make apps fold aware](https://developer.android.com/guide/topics/large-screens/make-apps-fold-aware)
- [WindowManager releases](https://developer.android.com/jetpack/androidx/releases/window?hl=vi)
- [Godot MIDI Player 4](https://store.godotengine.org/asset/arlez80/godot-midi-player-4/)
- [MIDI & Soundfont2 asset](https://www.godotengine.org/asset-library/asset/edit/21199)
- [godot-midi 4.0](https://github.com/nlaha/godot-midi-4.0)
- [FluidSynthGodot](https://noisy-gate.itch.io/fluidsynthgodot)
- [Input Helper](https://github.com/nathanhoad/godot_input_helper)
- [Vale Village V2](https://github.com/badnewsgoonies-dot/vale-village-v2-godot)
- [Emerald remake thread](https://forum.godotengine.org/t/i-tried-remaking-pokemon-emerald-with-godot-4/79417)
- [Project Uranium Godot](https://github.com/acedogblast/Project-Uranium-Godot)
- [OpMon Godot](https://github.com/OpMonTeam/OpMon-Godot)
- [3D TurnBasedCombat](https://github.com/Cute-Fame-Studio/3D-TurnBasedCombat)
- [Godot 4.7 dev 1 notes](https://planet.freegamedev.net/category/engine/page/8/)
- [Kakao Galaxy Fold notes](https://kakaogames.atlassian.net/wiki/spaces/KS3GFC/pages/425721907)
- [Viewport size forum thread](https://forum.godotengine.org/t/cant-determine-when-viewport-or-window-size-changes/101771)