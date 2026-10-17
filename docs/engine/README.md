# Engine: Godot 4.7.2 (chosen 14 Oct 2026)

**Decision:** the game is built in **Godot 4.7.2** with typed GDScript, as a native Android app for the Galaxy
Z Fold 7. You chose it "for now", after two rounds of comparison. The engine code lives in its own private repo,
**GameMaker-Engine** (local folder `C:\Users\aaron\Documents\GameMaker-Engine`). This design repo keeps the
design docs.

## How it was chosen

1. **[GBA sources](gba-sources.md):** which existing projects could save engine work. Main finds:
   - **PascalPixel/alchemy:** a decomp of Golden Sun 1, about 90% done (The Lost Age about 5%).
   - **999sian/tmc (Project Picori):** a native Minish Cap port with an Android build.
   - **jjppof/goldensun_html5:** an open-source Golden Sun-style engine (MIT).
2. **[Route comparison](route-comparison/judge.md):** three routes, each argued by an advocate, then judged.

   | Route | Score | Time to a playable slice |
   |---|---|---|
   | A: native C on pokeemerald-expansion + an SDL3 Android layer | 35 | 11–15 weeks |
   | **B: Godot 4.7.2** | **46** | **6–8 weeks** |
   | C: extend goldensun_html5 in a WebView | 32 | 8–12 weeks |

   [Verification of the sources](route-comparison/verification.md) · [Folders you added](route-comparison/added-folders.md)
3. **[Challengers](challengers/screening.md):** a screen of 20+ further engines, then deep dives on the two
   strongest.
   - [libGDX](challengers/case-libgdx.md): no. About 8–10 weeks to the slice, and weaker for menus, cutscenes
     and the later art and music passes.
   - [Unity 6.6](challengers/case-unity.md): credible but not better. Licence activation needs sign-in, and its
     project files are fragile for an AI to edit.
   - The judging step was cut off by a usage limit; both deep dives reached their verdict on their own.

## What Godot gets from the other sources

| Source | Role |
|---|---|
| **goldensun_html5** (MIT) | Port source for Golden Sun behaviour: field Psynergy, pushable objects, event types, battle phases, Djinn and Summons. Not taken: its collision, and its damage formula, which has a bug. |
| **Our extraction** (`re/`) | The rules and data: formulas (`gs_battle.py`, used as the test oracle), tables, maps (Tiled `.tmj`), sprites, movement constants, field-Psynergy spec. |
| **alchemy** (GS1 C decomp) | Exact Golden Sun 1 behaviour where our notes are thin. **goldensun-master** (GS1 disassembly) supplies addresses. |
| **pokeemerald-expansion, PokeAPI CSVs** | Pokémon species, moves, learnsets and evolutions, converted to JSON. |
| **Minish Cap decomp (tmc)** | Reference for free movement, corner nudging and puzzle objects. |

## Status (14 Oct 2026, evening)

- **Runs on the Fold 7:** the debug APK built by `tools/setup_dev.py` + the Android preset installed and ran on the
  phone (your test). The newest build is `OneDrive\Apps-Roms\_GameMaker-builds\GameMaker-debug.apk` (dated copies
  beside it).
- **Playing:** title → character creator → **Act I, missions 1–10, end to end** (engine PR #48): Stonehollow and the
  Vault, the sea caves and Fallhaven as Corvin, Canalport, the Forgeheart, the Eldergrove, Lantern Reef, Bastion Rock,
  the Tradewind Bazaar, the fall of Fallhaven and the Wayfarer; two crews with swapping and trading; random battles
  against monsters and wild Pokémon with the full command set and **bonded partners** (PR #49); statuses, EXP with
  level evolutions, saves and Continue, touch controls. 250 headless tests and 27 end-to-end checks with screenshots.
- **16 Oct:** the UI-scale seam and re-layout on fold (PR #53), the visible UI fixes (PR #54) and the field seams
  (PR #55) landed; the APK pipeline (PR #56) is in review. The 16 Oct reviews' pages are in `docs/design/`.
- **Next (your order, 17 Oct): a playable Act I demo with great art.** The bug-fix build from the items, equipment,
  menus and bonded-partner reviews; the art Phase 2 probes (LPC Adepts, the 32-px tile spike, the 480×320 picture) so
  the open art questions can be settled by looking; then the art pass over missions 1–10 and the decided screens the
  demo needs. Mission 11 and adult mode come after the demo. Design defaults chosen while building are marked
  "proposed" in `docs/design/`.

## Tools to install first ([full ranked list](resources/ranked.md))

- **Map import:** YATI (Tiled import).
- **Tests:** GUT 9.7.1 (`godot_4_7` branch).
- **Touch controls:** Godot's built-in VirtualJoystick.
- **Pokémon data:** PokeAPI CSVs.
- **Reference:** godot-open-rpg, read only.
- **Later:** Dialogue Manager for dialogue, LimboAI for AI, and FluidSynth to render music to OGG.

**14 Oct audit of your local folder:** [what's on disk worth using, what to add, what to keep disabled]
(resources/local-folder-audit-2026-10-14.md). Short version: lift from the official Godot demos, the
MetroidvaniaDeveloperSystem shaders and `lit`'s post shaders already in `Apps-Roms`; add KoBeWi's palette-swap
shader, controller_icons, gloot and Maaack's menus; never enable ziva_installer, GodotBridge or godot-mcp.

**15 Oct asset audit:** [two CC0 libraries and the LPC character generator](resources/asset-audit-2026-10-15.md),
inventoried pack by pack against the new art scale (64-pixel Adepts, 32-pixel tiles). Short version: LPC for the
Adepts, Kenney Pixel for the dialogue font, Dungeon Crawl icons, Pixel-boy battle backgrounds, CC0 effect sheets
for Pokémon moves; tiles at 32 px, portraits and audio are gaps.

More: [Godot ecosystem survey](resources/godot-ecosystem.md) · [data and references](resources/data-and-references.md)

## Toolchain (installed 14 Oct)

`GameMaker-Engine/tools/setup_dev.py` installed each of these and checked it against its published checksum. They
live in `C:\Users\aaron\Documents\UnboundHack\apps\`:

- **Godot 4.7.2-stable**, in self-contained mode, with its export templates.
- **Eclipse Temurin JDK 17.0.20.**
- **Android command-line tools.**

Godot 4.7.2 builds for Android with compileSdk/targetSdk 36, build-tools 36.1.0, NDK 29.0.14206865 and minSdk 24. You
install those SDK packages yourself with `GameMaker-Engine/tools/android_sdk_packages.ps1`, because it asks you to
accept Google's licence.
