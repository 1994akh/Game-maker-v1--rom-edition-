# Local folder audit and GitHub additions (14 Oct 2026)

A second look at every folder in `C:\Users\aaron\OneDrive\Apps-Roms`, done by two independent auditors and two
researchers, then re-checked by a verifier that opened the files it cites. Nothing was run or installed. The
earlier pass (`ranked.md`, `route-comparison/added-folders.md`) judged the ROM and decomp folders but never
inventoried the Godot folders dropped on 14 Oct, and three of those have an **empty root README**, so a name-level
read was blind. This page is the result: what on disk is worth using now, what to add, and what to remove.

Labels: VERIFIED = the verifier opened the file or page on 14 Oct; INFERRED = marked as such.

## 1. Already on disk, worth using now

Ranked by how much it saves on the next steps (battle, NPC dialogue, menus, creator, Fold layouts, controllers).

| # | Folder | Licence | Use it for |
|---|---|---|---|
| 1 | **godot-demo-projects-master** (official demos, same 4.7 as ours) | MIT | `2d/role_playing_game/combat/turn_queue.gd` + `combat/combatants/*` as the first battle's turn scaffold (await-driven queue); `gui/multiple_resolutions/main.gd` lines 32–76 (an `AspectRatioContainer` + margin, presets up to 21:9) for the Fold cover/inner layouts; `misc/joypads/remap/*` for the controller screen; `dialogue/dialogue_data/*.json` + `dialogue_player.gd` as the NPC-dialogue data shape; `theme/theme.tres` as the placeholder menu theme; `2d/finite_state_machine/state_machine/*`; `mobile/multitouch_view/touch_helper.gd`; `2d/sprite_shaders/` (outline, aura, glow, dissolve) and `2d/screen_space_shaders/` (whirl, mirage, pixelize) for Psynergy and battle effects; `loading/serialization/*` for saves. No MIDI-file playback demo. Ignore `3d/`, `xr/`, `mono/`, `networking/`, `compute/`. |
| 2 | **MetroidvaniaDeveloperSystem** (the real README is `addons/MetroidvaniaDeveloperSystem/README.md`) | MIT (addon and both asset packs) | 31 `canvas_item` environment shaders in `shaders/environment/`: snow, rain, fog, heat_haze, lightning_flash, water, waterfall, lava, embers, fireflies, light_shafts, dust_storm, swaying_grass, leaves… Direct placeholders for field Psynergy (Frost → snow, Growth → leaves/swaying_grass, Douse → rain, Whirlwind → dust_storm, Reveal → fog + light_shafts) and battle flashes. `nodes/mds_music.gd` is the per-area music crossfade with boss override (the "music hooks" row). `nodes/mds_room_camera.gd` has cut/fade/slide/blend room transitions. `asset_packs/*/vfx/{slash,spark,dust}.png` are placeholder hit effects. Caveat (INFERRED): test the `hint_screen_texture` effects under the Compatibility renderer on the Fold. The genre label hid the most reusable code in the folder. |
| 3 | **lit** (`addons/lit/shaders/post/`) | MIT | 24 `canvas_item` post shaders independent of its lighting: `lit_post_dither` (4×4 Bayer, for a GBA 15-bit look), `lit_post_lut` + 8 LUTs, `posterize`, `letterbox` (cover-screen bars), `outline`, `pixelate`, `grade`, `vignette`. **Do not** enable the lighting (Forward+ only, unusable on Android) and do not copy the precompiler (it spawns desktop processes). Don't ship `branding/`. |
| 4 | **joypads** (Godot's joypad demo, asset 140) | MIT | `remap/remap_wizard.gd` + `joy_mapping.gd` build an SDL mapping string step by step ("press the button for X") for `Input.add_joy_mapping`, with half-axis and inverted-axis handling: the Settings > Controller screen for Backbone and unknown pads. `diagram.png` / `indicators.png` are placeholder art for it. |
| 5 | **Swallowtail** (already installed, `godot-mcp-go-…`) | — | `commands/android_commands.gd`: lists adb devices, exports, installs and launches the APK. That is the Fold 7 deploy loop. It is `OS.execute` on adb, already approved. |
| 6 | **GodotPixelRenderer** | MIT | Lift `quantize_color()` / `apply_palette()` and the outline block from `PixelRenderer/data/PixelArt.gdshader` as a palette-constrained recolour placeholder; `data/scripts/builtin_color_presets.gd` ships Lospec 8-colour palettes as `Color` arrays. The 3D-to-sprite renderer itself is for the graphics pass, only if sprites are remade from models. |
| 7 | **BetterTileEditor** | MPL-2.0; demo art "free to use" | `addons/better-tile-editor/demos/tilesets/*.png`: eleven 16×16 placeholder tilesets (grass, water, trees, pond, cliffs, slopes). The plugin itself stays off (Tiled is the source of truth). Its `DESIGN.md` §A documents a **Godot 4.7.1 gotcha**: editor autoloads now enter the tree unnamed, so `@tool` scripts must not look autoloads up by name. |
| 8 | **tmc-master `tools/src/`** and **godogen `asset-gen/tools/`** | pret tools; MIT | Graphics/audio pass: `gbagfx` (PNG ↔ GBA 4bpp), `mid2agb`/`agb2mid` (a second m4a ↔ MIDI path), `aif2pcm`; `grid_slice.py`, `find_loop_frame.py`, `rembg_matting.py` as offline sprite-sheet helpers. godogen's `docs/gdscript-vs-csharp.md` lists the GDScript `:=` inference footguns, a checklist for the typed-GDScript rule. |

Smaller reference finds: `azgaar_map_generator` (a Godot port, not Azgaar's FMG; MIT) has small dependency-free
Voronoi/heightmap/name generators for a world-map overview texture (strip "Rivendell" from its name list);
`SpatialAudio3D` shows occlusion as a low-pass cutoff tweened over time (the right way to muffle music in caves);
`GDSQL`'s `crypto/crypto.gd` is a clean reference if saves ever need encryption; `goldensun-master/tools/*_strings.c`
and `*_overlay.c` are independent C codecs to cross-check `re/gbax`; `butterfly/INSTRUCTION_FOLDABLE.md` explains
testing fold postures on a PC emulator image; `nxemu`'s `res/drawable/*.xml` is a full touch-overlay glyph set
(GPL-3, placeholder only).

## 2. Add to the local folder

Ranked. All VERIFIED on 14 Oct via github.com or the GitHub API unless marked. Read before use, as with everything.

| # | Get | Licence | Activity | What it saves |
|---|---|---|---|---|
| 1 | `git clone https://github.com/KoBeWi/Godot-Palette-Swap-Shader` | MIT | pushed 2026-08-25, 115★ | `PaletteMaterial` (up to 256 colours, palette rows for animation) plus a "Generate Palette…" editor tool that pulls a sprite's colours. The character creator's palette-swap layer and the Weyard-form recolour path. Copy only `addons/PaletteSwapShader/`. 4.7 fit INFERRED (pure shader + GDScript). |
| 2 | `git clone https://github.com/rsubtil/controller_icons` | MIT code, CC0 art | pushed 2026-07-28, 445★, Godot ≥ 4.1.2 | Button prompts that swap Xbox / Backbone / keyboard glyphs by the active device, in menus and dialogue. No touch glyphs (see #8). |
| 3 | `git clone https://github.com/peter-kish/gloot` | MIT | pushed 2026-07-14, 984★, Godot 4.4+ | Inventory and equipment logic with JSON item prototypes and `serialize()`: our extracted item tables drop in; we build the GBA-style UI on top. |
| 4 | `git clone https://github.com/Maaack/Godot-Game-Template` | MIT | pushed 2026-09-10, 1,693★, "for Godot 4.7" | Main / options / pause menus with controller focus and key rebinding. Cherry-pick the menu and remap scenes and re-theme to 240×160; don't adopt the whole template, and don't enable its plugin-updater addon (network). |
| 5 | `git clone --depth 1 https://github.com/Decryptu/pokerecomp` | MIT (engine source) | pushed 2026-10-13, 41★, alpha | The only active GDScript Pokémon battle (278 animation scripts, save slots), and it decodes its content from the player's own cartridge, the same rule we follow. **Read only:** it needs Godot 4.8 and won't open in 4.7.2. |
| 6 | `git clone https://github.com/justedni/goldensunvst` | LGPL-3.0 | pushed 2026-05-20 | Golden Sun's own synths and reverb as a VST3 (agbplay-based). Renders our extracted MIDI + SF2 to Golden Sun-accurate OGG. Audio pass; needs CMake/VS2022 to build. |
| 7 | `git clone https://github.com/nklbdev/godot-4-importality` | MIT | pushed 2026-03-21, 541★ | Aseprite / Pixelorama / Piskel → `SpriteFrames` / `AnimationPlayer` import for the graphics pass. The Pixelorama path needs no external exe. |
| 8 | Download https://kenney.nl/assets/input-prompts-pixel-16 | CC0 | ~800 glyphs | 16×16 Xbox / Nintendo / PlayStation / generic / **touch** prompts at GBA scale; fills controller_icons' touch gap. |
| 9 | `git clone https://codeberg.org/cookie_cherith/godot-layered-sprites` | MIT | 2026-06-10, Godot 4.6 | `LayeredSprite2D` with per-layer texture variants and colours sharing one `SpriteFrames`: the paper-doll node for the creator. Tiny project; read it first. |
| 10 | `git clone -b godot-4 https://github.com/timothyqiu/gdfxr` | MIT | pushed 2024-08-21, 196★ | An sfxr panel inside the editor for placeholder cursor / confirm / Psynergy sounds until the ROM SFX pass. 14 months stale; 4.7 fit INFERRED. |
| 11 | `pip install "gdtoolkit==4.*"` | MIT | pushed 2025-10-09 | `gdlint` / `gdformat` enforce the typed-GDScript rule mechanically; pairs with the GUT tests. No clone needed. |
| 12 | `git clone --depth 1 https://github.com/Maruno17/pokemon-essentials` | non-commercial | pushed 2026-10-11, 377★, 154 MB | The most complete readable Pokémon battle (turn order, per-move effects, multi-battle targeting, menus), in Ruby. Read for control flow only; never copy text. Large and non-free, so last. |

**Skip, with reasons:** hugemenace/resonate (archived 2026-01-19; use the built-in `AudioStreamInteractive` plus
the MDS crossfade); bbbscarter/event-audio-godot (stale; the fallback-bank idea is ~50 lines); PKGaspi/godot-
LayeredSprite (2023; superseded by #9); WillOnGit/golden-sun (2021; `gs_battle.py` and alchemy are already the
oracle); PokeAPI/sprites (22 GB) and PokemonStudio (AGPL/Electron) as bookmarks only; no Godot 4 MIDI player exists
(arlez80's is Godot 3.5), so music is rendered to OGG offline. Already judged in `godot-ecosystem.md` /
`ranked.md` and not re-proposed: godot_input_helper, phantom-camera, godot-aseprite-wizard, Pixelorama,
Virtual-Joystick-Godot (4.7 has a built-in `VirtualJoystick`), LeviOS31's JRPG addon, gongpha/godot-midi,
godot-open-rpg, the Android plugin template, FluidSynth, agbplay. Optional CC0 placeholder packs the researchers
named but the verifier did not open: Ninja Adventure, Hormelz 8-direction base, Zelda-like tiles, m5x7 and monogram
fonts.

## 3. Housekeeping and risks

Both audits agree on these. None of it has been done; it is your folder.

- **Do not enable** `addons\ziva_installer` (closed binaries plus an env-redirectable downloader that installs more
  binaries), `addon-7445…` GodotBridge (writes a runtime autoload into `project.godot` that ships in the APK, opens
  sockets, runs arbitrary GDScript and `OS.execute`), or `godot-mcp-1b03…` (a third MCP server, TCP listener, no auth
  found, non-commercial licence). Swallowtail is the one approved MCP bridge.
- **GDSQL** has a plugin updater that calls `api.github.com` from inside the editor, and its workbench name is set to
  invisible Unicode. Not needed anyway (our data is JSON).
- **SpatialAudio3D** bundles uncredited third-party audio (a drum solo, YouTube test clips). Never use those as
  placeholder sounds.
- **Executables synced through OneDrive**, none run and none needed: `pikmin2-main\aoi.exe` (84 MB, most of that
  folder), `oot-main\tools\ido*_compiler\`, `luvdis-main\asm\arm-none-eabi-*`, the `godot-git-plugin` DLLs,
  `tilemap-studio-master\install.bat`. `pikmin2-main`, the empty `Designer` folder and the three empty `Pokemon\*`
  subfolders can go.
- **The four ROMs and the debug keystore** sit in a cloud-synced folder. Consider moving the ROMs out of OneDrive.
  The debug keystore is low-risk; a release keystore should never live there.
- **`godogen-master`** ships `CLAUDE.md` and `AGENTS.md`. They are third-party agent instructions and stay untrusted
  data; never load them as a skill.
- **Licence traps** for anything lifted: nxemu art is GPL-3, `lit/branding/`, `tmc-master/translations/` and
  `tmc-master/assets` are not ours.

## 4. Corrections to the earlier pass

- `godot-demo-projects-master`, `MetroidvaniaDeveloperSystem`, `lit` and `BetterTileEditor` all have licence files
  (MIT, MIT, MIT, MPL-2.0) in their addon folders; one researcher reported "none" from the empty roots.
- `godot-psx-look-free` is an incomplete cut: the README promises `psx_screen.gdshader` (15-bit colour + dither) but
  it isn't in the folder, and the loader silently skips it. Take the dither from `lit` instead.
- `azgaar_map_generator` is not Azgaar's Fantasy Map Generator; it's a Godot addon "inspired by" it.
- `Pokemon\` holds only the FireRed ROM; its `Custom Pokemon`, `Fire red GBA` and `Pokemon Unbound` folders are empty.

## 5. Added 15 Oct 2026

Five folders appeared in `OneDrive\Apps-Roms` on 15 Oct. All were read, none run.

| Folder | What it is | Verdict |
|---|---|---|
| `godot-3d-player-controller-addon-…\addons\controls` | Tim Cope's "Controls" HUD (MIT): on-screen button hints that swap art per device, plus a world "Press [button]" prompt | **Lift the art, not the addon.** It bundles **Kenney Input Prompts 1.4a (CC0)**: 737 vector glyphs for keyboard and mouse, Xbox, PlayStation, Switch, Steam Deck and touch. That is the "Kenney prompts" item from §2, now on disk. Use the glyphs for "A: Talk"-style hints in the dialogue box, menus and the touch overlay in the UI pass. Skip the HUD itself: it targets Godot 4.8 (we are on 4.7.2) and duplicates our TouchOverlay |
| `godot-3d-player-controller-addon-…\addons\3d_player_controller` | A 3D third/first-person controller with IK and root motion (174 MB with assets) | Not useful: the game is 2D. Safe to delete |
| `godot-road-generator-…` | TheDuckCow's 3D road and traffic generator (22 MB) | Not useful: 3D roads. Safe to delete |
| `Blendot-…` | Blender round-trip editing for 3D models (MIT) | Not useful: no 3D models. Safe to delete |
| `batch-sprite-keyframe-…` | An editor dock that slices a sheet and writes Sprite2D texture keyframes into an AnimationPlayer (comments in Chinese, no licence file) | Low value now: our sprites are built in code from the exported sheets. Possibly handy in the graphics pass for hand-made animations; no licence, so read-only reference |
| `tile mapper\godot_multilayer_tilemap-…` | Byte-for-byte the same commit as the `godot_multilayer_tilemap-eac6924…` folder already audited in §1 | Duplicate. Safe to delete either copy |

## 6. Added 15 Oct 2026, later

Two more uploads, read only.

| Folder | What it is | Verdict |
|---|---|---|
| `zelda3-master` | snesrev's C reimplementation of *A Link to the Past* (MIT, about 75k lines, SNES PPU from LakeSnes). Its levels and art are extracted from your own ROM at build time; none are in the folder | **Reference only.** Useful reading when we build top-down puzzle verbs Golden Sun lacks (pushable blocks on grids, holes and falling, floors and stairs between layers, switches) and enemy behaviour in rooms. Not to build or run, and none of its extracted assets can ship |
| `tmc-master` (refreshed) | The Minish Cap decomp, now the **"Project Picori" PC and Android port**: a Gradle Android shell around an SDL3 native library (game engine, PPU, audio, ImGui menus and a touch overlay in C), a multi-region "fat binary", CI release workflows | **Reference only.** Shows how a GBA-era game ships natively on Android with a touch overlay; our Godot export already covers that. Two text files are addressed to AI agents: `AGENTS.md` (repo guidelines for its own contributors) and `agent.txt` ("You are my assistant. You will write comments for my code and rename functions…"). Both are third-party data; neither was acted on, and neither should be loaded as instructions |

## 7. Added 15 Oct 2026, evening

| Folder | What it is | Verdict |
|---|---|---|
| `Aseprite-AI-Generator-main` | A local Stable Diffusion server (Flask, PyTorch, diffusers, BiRefNet background removal) plus an Aseprite extension that turns text prompts into palette-quantised pixel sprites. No licence file | **Not usable on this PC, and not run.** It needs an NVIDIA CUDA GPU with 8 GB or more; this machine has AMD Radeon integrated graphics, and Aseprite isn't installed. Its setup script pip-installs CUDA builds of PyTorch and downloads models from Hugging Face, so it should not be started without a review. The idea fits the graphics pass (AI-drafted placeholder sprites cut to a fixed palette), but the palette step is a few lines of Pillow we can write ourselves, and community checkpoints carry their own licence terms |
