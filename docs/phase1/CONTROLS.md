# CONTROLS.md: Phone controls and controller spec (draft v0.1, 2026-10-12)

> Phase-1 investigator report, written so it can go into the repo as `docs/CONTROLS.md`. It covers the ROM edition played on a Samsung Galaxy Z Fold 7 and on ordinary phones, and keeps a path open to a native Android port later.
> **Labels:** **[V]** = verified this session in code or docs (path:line or URL given). **[I]** = inferred, or general knowledge not re-checked. These need a device test or a source check before anyone relies on them.
---

## 0. Summary of proposals (for the user to decide)

1. **Play-test now in an existing emulator: Lemuroid (free, mGBA core) or Pizza Boy A Pro.** Then build a small custom **"player" app** from LibretroDroid, RadialGamePad and the mGBA libretro core. Only the custom app can handle fold postures, keep a touch layout per posture, and add the extra shortcut buttons this design needs.
2. **Every feature must work on a plain GBA control set through in-game menus.** Extra phone and controller buttons are only shortcuts.
3. **Shortcut channel ("V-keys"):** the player app sends D-pad chords that a real D-pad cannot make, such as Up+Down plus another button. One small hook in the ROM's `ReadKeys()` turns them into up to 22 virtual buttons, used for auto-run, DexNav, map, Summon and an 8-slot Psynergy wheel. Anywhere else they simply never happen.
4. **GBA button roles:**
   * L and R = Golden Sun-style Psynergy shortcuts.
   * Select = 8-slot quick wheel. Its pattern copies CFRU's registered-item wheel.
   * DexNav moves off R onto a V-key and the Start menu.
   * Auto-run is a toggle; holding B walks while it is on (CFRU's behaviour).
5. **Game image:** always an integer multiple of 240×160, chosen per posture: cover 4× portrait / 6× landscape, inner 8× portrait, tabletop 6× on the top half, inner landscape with a controller 9×.
6. **Build the player app's input and layout code around semantic actions** (MOVE8, CONFIRM, QUICK_WHEEL, PSY_n, …), not GBA buttons. The ROM edition turns those actions into GBA buttons and chords; a native engine would read them directly. That layer carries over to the native port unchanged.

---

## 1. Galaxy Z Fold 7: device facts

| Item | Value | Status / source |
|---|---|---|
| Main (inner) screen | 8.0" QXGA+ Dynamic AMOLED 2X, **2184 × 1968**, 368 ppi, **1–120 Hz** adaptive | [V] Samsung Newsroom spec table |
| Cover screen | 6.5" FHD+ Dynamic AMOLED 2X, **2520 × 1080, 21:9**, 422 ppi, **1–120 Hz** adaptive. Viewable area is smaller because of rounded corners and the camera hole | [V] same |
| Size | Folded 72.8 × 158.4 × 8.9 mm; unfolded 143.2 × 158.4 × 4.2 mm; 215 g | [V] same |
| Inner aspect / orientation | 2184/1968 = 1.11 (nearly square). 158.4/143.2 = 1.106 matches, so held as a book the inner screen is **1968 wide × 2184 tall** and the hinge is vertical. Turned 90°, it is 2184 × 1968 with a horizontal hinge (tabletop) | [I] from the [V] dimensions |
| Cover aspect | 1080 × 2520 portrait = 65 × 152 mm active area | [I] from px ÷ ppi |
| OS at launch | **Android 16, One UI 8** | [V] Newsroom |
| Current OS (Oct 2026) | Probably updated since launch (One UI 8.x or later). Not checked | [I] |
| Chip / RAM | Snapdragon 8 Elite for Galaxy; 12 GB (256/512 GB storage) or 16 GB (1 TB) | [V] Newsroom |
| Connectivity | 5G, LTE, Wi-Fi 7, **Bluetooth v5.4** | [V] Newsroom |
| USB-C | Charging "with 3A USB-C cable", 25 W. **USB generation is not in Samsung's table** (third-party sites say USB 3.2 Gen 1, unchecked). Irrelevant to controllers, which are HID | [V] port / [I] generation |
| Water resistance | IP48 | [V] |
| Sensors | Accelerometer, gyro, Hall sensor, among others | [V] |
| Hinge angle | **Not exposed by the API**: `FoldingFeature` gives FLAT or HALF_OPENED only | [V] Android fold-aware doc |
| Flex Mode / half-folded | Samsung's "Flex mode panel" is a Labs feature that adds a control panel to apps not built for it. Turn it off for our app, because the app handles tabletop itself | [I] Samsung support page title only |
| Cover-screen continuity | Settings > Display > **Continue apps on cover screen**: a switch per app on the Fold 7 (the Fold 8 has Always / Swipe up / Never). **Must be on for the player app**, or folding locks the cover screen | [V] Samsung support pages, seen as search excerpts only |
| Inner camera / cutout position | Not verified. Always read `DisplayCutout` insets; never hard-code | [I] |

**Refresh-rate note:** the GBA runs at 16,777,216 Hz ÷ 280,896 cycles per frame = **59.7275 Hz**. Both panels are 1–120 Hz adaptive [V]. Call `Surface.setFrameRate(59.7275f, FRAME_RATE_COMPATIBILITY_FIXED_SOURCE)` (API 30) to ask for a 60 Hz mode [I].

**Fold 8 already exists** (Samsung support pages mention a Z Fold8) [V]. So the layout code must work from runtime window metrics and the `FoldingFeature` bounds. Never hard-code Fold 7 pixel positions.

---

## 2. How the ROM edition runs on the phone

### 2a. Existing Android emulators

| | Touch layout customisation | Fold posture support | Controllers | Per-game layout | Can send extra shortcut buttons (chords) |
|---|---|---|---|---|---|
| **RetroArch + mGBA core** | Overlays: config files plus images; third-party RetroPad Editor; portrait/landscape auto-rotate only if overlay names contain "portrait"/"landscape" [I, forum posts] | None found; follows orientation only [I] | Full: autoconfig, remaps, hot-plug [I] | Yes, via game overrides [I] | **Possibly**: overlay buttons can be bound to several RetroPad inputs, and the core option `mgba_allow_opposing_directions` exists [V option / I overlay syntax] |
| **Lemuroid** (mGBA core: `CoreID.kt:39-42`) [V] | Scale, rotation and margins (`TouchControllerSettingsManager.kt:122-131`) [V]. Stored **per touch-controller ID × orientation** (`…:134-138`, key `touch_controller_settings_${controllerID}_${orientation.ordinal}`) [V] | **No `FoldingFeature`/`WindowInfoTracker`/`HALF_OPENED` code anywhere in HEAD** [V, full-source grep]. Does handle config changes without restarting (`AndroidManifest.xml:52` lists `screenSize|smallestScreenSize|density|…`) [V]. Cutout padding on the game view (`MobileGameScreen.kt:163`) [V] | Hot-plug through `InputManager.InputDeviceListener` (`InputDeviceManager.kt:180-196`); D-pad hat axes (`GameViewModelInput.kt:99,151`) [V] | **No**: keyed by system and orientation only [V] | No. Fixed GBA button set [I] |
| **Pizza Boy A Pro** (closed source, paid, updated Oct 2 2026) | "Fully customizable on-screen buttons", "Customizable skins and button layouts" [V Play listing] | Not mentioned [I: none] | "Physical controller support" [V]; hides on-screen controls when a controller is detected [V, user review only] | Unknown | Unknown. Can't be extended |
| **My Boy!** and others | Not researched (closed source) | — | — | — | — |

### 2b. Custom "player" app: LibretroDroid + RadialGamePad + mGBA libretro core

* **LibretroDroid** (`GLRetroView`) [V]:
  * Input: `sendKeyEvent(action, keyCode, port)` at :129, `sendMotionEvent(source, x, y, port)` at :133 (sources `MOTION_SOURCE_DPAD/ANALOG_LEFT/ANALOG_RIGHT`, :278-290).
  * Saves: `serializeState()` :165, `unserializeState()` :177, `serializeSRAM()` :183.
  * Display: `viewport: RectF` :64, which allows exact integer-scale placement; shaders include `Sharp` :415, for scales that are not whole numbers.
  * Other: `frameSpeed` :56 (fast-forward), `updateVariables()` :223 (core options), rumble :83/:491, `preferLowLatencyAudio` and `immersiveMode` (`GLRetroViewData.kt:34,37`).
* **RadialGamePad** [V]:
  * Cross D-pad with **`useDiagonals = true` by default** (`CrossConfig.kt:29,39`).
  * Analog `Stick` dial (`PrimaryDialConfig.kt:42`).
  * `HapticConfig` with off / on press / on press and release (`HapticConfig.kt:22-30`).
  * Emits Direction events with x/y values (README:34).
* **mGBA libretro core** [V]: the core option `mgba_allow_opposing_directions` exists (`libretro_core_options.h:257-260`). This is required for the chord channel. Its default is presumably "no" [I]; the player app sets it to "yes".
* **Licences:** LibretroDroid and RadialGamePad are **GPL-3.0** [V, LICENSE files]; Lemuroid is presumably GPL-3.0 [I]; mGBA is **MPL-2.0** [V]. For personal use this changes nothing. If the app is ever shared, its source must be GPL-3.0.

### 2c. Recommendation

* **Now (no code):** sideload the built `.gba` into **Lemuroid** for early tests on the Fold 7. It's free, uses the mGBA core, handles controller hot-plug, survives folding, and keeps separate portrait and landscape layouts. Use **Pizza Boy A Pro** as a second opinion on accuracy. Every feature stays reachable through menus, so nothing is blocked.
* **When the ROM first needs V-keys** (Psynergy beyond L/R, DexNav, auto-run), build the **custom player app**. No existing emulator offers posture-specific layouts, a tabletop split, per-posture saved layouts or extra shortcut buttons. Forking Lemuroid is possible, but it is a full multi-system frontend; a single-game app is smaller and maps directly onto the native port.
* **Carry-over to a native engine:** structure the app as `input/` (devices, mapping, semantic actions), `layout/` (posture to layout, integer viewport), `touch/` (RadialGamePad configs and editor) and `core/` (a LibretroDroid adapter plus `GbaChordEncoder`). For the native app, replace only `core/` with the engine bridge. Semantic actions then go straight to the engine and the chord encoder is deleted. The layout engine is reused with the native logical resolution, which could also be something other than 240×160.

---

## 3. Android platform requirements for the player app

| Topic | Spec | Status / source |
|---|---|---|
| Posture detection | `WindowInfoTracker.windowLayoutInfo` → `FoldingFeature`. **Tabletop** = `state == HALF_OPENED && orientation == HORIZONTAL`. **Book** = `HALF_OPENED && VERTICAL`. Use `bounds` for the hinge keep-out band. HALF_OPENED always reports `isSeparating = true`. "Don't place UI controls too close to a fold". Compose: `currentWindowAdaptiveInfoV2().windowPosture.isTabletop` | [V] Android "Make your app fold aware" |
| Window size | Use `WindowSizeClass` and `WindowMetrics` to choose the layout family. Expected: cover ≈ compact width; inner ≈ medium or expanded. Breakpoints 600/840 dp. Never assume density | [I] |
| Android 16 large screens | If targeting API 36, on displays with **sw ≥ 600 dp (the inner screen)** the system **ignores** `screenOrientation`, `resizableActivity`, min/max aspect ratio and `setRequestedOrientation()` — **unless the app is a game per `android:appCategory`**. The opt-out property ends at API 37. **Declare `android:appCategory="game"`** and design every layout for every orientation anyway | [V] Android 16 behaviour changes |
| Fold/unfold continuity | Declare `configChanges="orientation\|screenSize\|smallestScreenSize\|screenLayout\|density\|keyboard\|keyboardHidden\|navigation\|uiMode"` so the emulator survives cover↔inner switches without restarting the Activity (Lemuroid's precedent, `AndroidManifest.xml:52`). Recompute the layout in `onConfigurationChanged` or on a WindowMetrics change. **Safety net:** auto-save state and SRAM in `onPause`. Turn on Samsung's "Continue apps on cover screen" for the app | [V] Lemuroid / [V] LibretroDroid APIs / [V] Samsung setting |
| Back gesture | **Targeting API 36: `onBackPressed` is not called and `KEYCODE_BACK` is not dispatched.** Use an `OnBackPressedCallback` that **opens the pause menu**, never exits | [V] Android 16 behaviour changes |
| Edge gestures | Use `View.setSystemGestureExclusionRects()` over the D-pad and A/B zones next to the screen edges (games may do this "during gameplay"). **Home and quick-switch gestures can't be excluded**: keep buttons out of `getMandatorySystemGestureInsets()`. Each edge's exclusion is capped at about 200 dp of height | [V] gesture-nav guide / [I] the 200 dp figure, from the API reference |
| Edge-to-edge | Mandatory when targeting API 36 (the opt-out is disabled). Run fullscreen immersive (`WindowInsetsControllerCompat.hide(systemBars())`, `BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE`) and pad for `displayCutout` | [V] edge-to-edge / [I] immersive API details |
| Samsung Game Booster | Can block navigation gestures while playing, once the app is seen as a game | [I] |
| Haptics | Touch buttons: `performHapticFeedback(VIRTUAL_KEY or KEYBOARD_TAP)`, which respects the system setting, or RadialGamePad's `HapticConfig.PRESS`. Controller rumble: optional, through `InputDevice.getVibratorManager()` (API 31) | [V] RadialGamePad / [I] Android APIs |
| Frame pacing | `setFrameRate(59.7275f, FIXED_SOURCE)`; LibretroDroid `preferLowLatencyAudio = true` | [I] / [V] |

---

## 4. Controllers

### 4a. Hardware

| Controller | Facts | Status |
|---|---|---|
| **Backbone One** | Clip-on controller made in USB-C and Lightning versions. **Only USB-C works on Android.** The Lightning version is for iPhone 14 and earlier | [I] (not re-checked this session) |
| **Backbone Pro** | **Exists.** USB-C "handheld mode" with a low-latency wired link, **plus Bluetooth "Wireless mode"** ("FlowState" Bluetooth LE pairing, up to 40 h). Full-size ALPS sticks, **2 rear buttons with customisable mapping**, larger **Hall-effect triggers**, remapping and trigger sensitivity in the Backbone app. Android 10 or later. Lightning not compatible. Listed at $169.99 | [V] backbone.com/pages/pro and product JSON |
| Backbone on the Fold | The case-compatibility list names the **Galaxy Z Fold 5, not the Fold 7**. The Fold 7 fits only **folded** (72.8 × 158.4 × 8.9 mm, so the cover screen in landscape). It may need an adapter; test the fit. **Unfolded or tabletop play means a Bluetooth controller** (Xbox, or the Backbone Pro in wireless mode) | [V] list / [I] fit |
| **Xbox Wireless Controller** over Bluetooth | Android's USB key layout for the Xbox Series pad (`Vendor_045e_Product_0b12.kl`):<br>• Buttons: A/B/X/Y → `BUTTON_A/B/X/Y`; LB/RB → `BUTTON_L1/R1`; L3/R3 → `BUTTON_THUMBL/THUMBR`<br>• Sticks: `AXIS_X/Y` and `AXIS_Z/RZ` (flat 4096); triggers `AXIS_LTRIGGER/RTRIGGER`; D-pad `AXIS_HAT_X/HAT_Y`<br>• Other: View → `BUTTON_SELECT`; Menu → `BUTTON_START`; Xbox → `BUTTON_MODE`; Share → `MEDIA_RECORD`<br>No layout file exists under the guessed Bluetooth product ID (0b13, HTTP 404), so the Bluetooth mapping may differ. The controller test screen must confirm it | [V] AOSP file / [I] Bluetooth |

### 4b. How Android reports controllers (implementation rules)

* **Detect:** `supportsSource(SOURCE_GAMEPAD) || supportsSource(SOURCE_JOYSTICK)` [V]. Skip virtual and built-in devices. Lemuroid keeps a blocklist of devices that falsely claim SOURCE_GAMEPAD (`InputDeviceManager.kt:256`) [V].
* **Hot-plug:** `InputManager.registerInputDeviceListener` for added, removed and changed devices [V, Lemuroid].
* **Buttons:** `KeyEvent` `KEYCODE_BUTTON_*`. Ignore `repeatCount > 0`. Return `true` only for handled events and call `super` otherwise [V, Android doc].
* **D-pad:** handle **both** `KEYCODE_DPAD_*` and `AXIS_HAT_X/Y` (−1 = up/left, +1 = down/right) as one input [V].
* **Sticks:** left = `AXIS_X/Y`, right = `AXIS_Z/RZ`. Dead zone = `getMotionRange(axis, source).flat`. Process historical samples first [V].
* **Triggers:** `AXIS_LTRIGGER/RTRIGGER`, also mirrored on `AXIS_BRAKE/GAS`, **and** `KEYCODE_BUTTON_L2/R2`. Support all of them [V]. Press at 0.5, release at 0.35 [proposal].
* **Left stick → 8-way D-pad** [proposal]:
  * Engage at a magnitude of at least max(flat, 0.30); release below 0.20.
  * Eight 45° sectors, with ±7.5° hysteresis so diagonals don't flicker.
  * Diagonals set **both** GBA direction bits.
* **Touch overlay visibility:** hide it while any real gamepad is connected. Tapping the screen shows it again for 5 s. It comes back when the last pad disconnects.
* **Remapping:** a per-controller profile keyed by `InputDevice.descriptor` [I: stable across reconnects], mapping keycodes or axes to semantic actions. Include a **Controller test** screen that logs name, vendor/product, sources, keycodes and axes. Use it to settle the Backbone rear-button, Backbone-button and Xbox Bluetooth questions.

---

## 5. The control map

### 5a. What the engine already does (expansion 1.17.2, the build target)

* **Field:**
  * Start = menu; **Select = registered key item** (`src/field_control_avatar.c:237`); **R = DexNav search** (`:240`).
  * **Hold B = run**, gated by `FLAG_SYS_B_DASH` (`src/field_player_avatar.c:910-915`). Running indoors is allowed (`include/config/overworld.h:5`).
  * L is unused on the field (no `L_BUTTON` in `field_control_avatar.c`) [V].
  * **Diagonals are discarded:** `dpadDirection` takes Up, then Down, then Left, then Right (`field_control_avatar.c:142-149`) [V]. This belongs to the movement topic.
* **No auto-run** found in `include/config/*.h`, `field_control_avatar.c` or `field_player_avatar.c` [V, grep].
* **DexNav** is off by default (`include/config/dexnav.h:4`); `DN_FLAG_DEXNAV_GET` adds it to the Start menu (`:9`) [V].
* **Battle:**
  * Start in the action menu swaps HP bars and HP text (`battle_controller_player.c:394-396`).
  * **Start in the move menu toggles the gimmick (Mega/Z/Dynamax)** (`:908-915`).
  * **L = move description** (`include/config/battle.h:360`).
  * **R = throw last-used Ball** (`battle.h:381`).
  * Select = move rearrangement when `B_MOVE_REARRANGEMENT_IN_BATTLE < GEN_4` (`:865`) [V].
* **Key input** is read in `ReadKeys()` (`src/main.c:269-296`, with `REG_KEYINPUT` at :271) [V]. This is the hook point for chords.

**CFRU / Unbound precedent** [V]:
* Auto-run is toggled by **L** (`src/config.h:54` `FLAG_AUTO_RUN`), and **holding B walks while auto-run is on** (`src/overworld.c:1731-1735`).
* R's function is set by `VAR_R_BUTTON_MODE`: DexNav, Pokémon menu, Bag, Mission Log, … (`include/global.h:139-144`).
* **Select opens a registered-item wheel where Select/L/R/Start/←/→ each fire one slot** (`src/overworld.c:2955-2980`). This is the model for our quick wheel.

### 5b. Semantic actions, and how the ROM edition carries each one

| Action | ROM edition carrier | Reachable without the player app? |
|---|---|---|
| MOVE8 (8-way) | D-pad, two bits for diagonals | Yes |
| CONFIRM / CANCEL | A / B | Yes |
| WALK_WHILE_AUTORUN (hold) | Hold B (CFRU behaviour) | Yes |
| MAIN_MENU | Start (Adepts, Set/Standby, Psynergy, Bag, Pokédex, **DexNav**, **Map**, Save, Options) | Yes |
| QUICK_WHEEL | Select → 8-slot wheel. Pick a slot by direction, including diagonals, then A; or press its button (Select/L/R/Start/←/→ as in CFRU). Slots hold Psynergy, item Psynergy, Surf/Dive/Waterfall, **auto-run toggle**, DexNav, key items | Yes |
| PSY_SHORTCUT_1 / 2 | **L / R** on the field (Golden Sun style; assigned in the Psynergy menu) | Yes |
| AUTORUN_TOGGLE | V-key V01 + quick-wheel slot + Options | Yes (wheel or Options) |
| DEXNAV | V-key V02 + Start-menu entry. **ROM change: take DexNav off R** (`field_control_avatar.c:240`) | Yes (menu) |
| WORLD_MAP | V-key V03 + Start menu | Yes |
| SUMMON (battle) | **Start in the move menu** (reusing the gimmick toggle, `:908-915`) + V-key V04 to open the Summon list directly | Yes (Start) |
| SET_STANDBY screen | V-key V05 + Start menu | Yes |
| WHEEL_SLOT_1..8 (direct cast) | V-keys V09–V16 | Yes (through the wheel) |
| Surf / Dive / Waterfall | **Context prompt with A** facing water, a dive spot or a waterfall (vanilla style), and also in the wheel | Yes |
| APP_MENU, FAST_FORWARD, SAVE/LOAD_STATE | Player app only. Never sent to the ROM | n/a |

Golden Sun's L/R Psynergy shortcut slots are taken from the task brief [I]. Check in-game whether The Lost Age also offered a Select slot.

### 5c. V-key chord protocol (ROM edition only)

A real GBA D-pad can't press opposite directions at once, so these chords never occur in normal play.

| Chord (held 3 frames, then 1 neutral frame) | Codes |
|---|---|
| **Up+Down** + {A, B, L, R, Start, Select, ←, →} | V01–V08 (V01 auto-run, V02 DexNav, V03 map, V04 Summon, V05 Set/Standby, V06–V08 spare) |
| **←+→** + {A, B, L, R, Start, Select, Up, Down} | V09–V16 (wheel slots 1–8) |
| **Up+Down+←+→** + {A, B, L, R, Start, Select} | V17–V22 spare |

* **ROM hook** (in `ReadKeys`, `src/main.c:269+`):
  * If both Up+Down or both ←+→ are held, decode the code into `gExtKeysNew` / `gExtKeysHeld`.
  * **Clear all bits** that frame so no stray A or B gets through.
  * Run it before the soft-reset check (A+B+Start+Select is never a chord).
  * The field, battle and menu code then reads `gExtKeysNew` per context.
* **Player app:** set `mgba_allow_opposing_directions = yes` with `updateVariables()`. Emit each chord atomically through `sendKeyEvent` and hold back user D-pad input for those 4 frames (about 67 ms).
* **Other emulators:** with opposing input off, chords never arrive and everything works through menus. RetroArch overlays could possibly send chords [I].
* **Menu safety:** add a ROM-side filter (about 15 lines) that collapses a diagonal to the most recent axis whenever the overworld field-control callback is not active. This stops 8-way sticks from double-moving grid cursors.

### 5d. Physical controller mapping (Xbox labels; Backbone One/Pro are Xbox-style)

| Controller | Field | Battle | Menus |
|---|---|---|---|
| Left stick / D-pad | MOVE8 | Cursor | Cursor |
| **A** | A (interact, confirm) | A | A |
| **B** | B (cancel; hold = walk while auto-run is on) | B | B |
| **X** | Select → quick wheel | Select | Select |
| **Y** | V01 auto-run toggle | V04 Summon list | — |
| **LB / RB** | L / R = Psynergy shortcuts 1 / 2 | L move info / R last Ball | L / R page |
| **LT** | V02 DexNav | — | — |
| **RT** | App: hold for fast-forward (can be remapped to a V-key) | same | same |
| **Menu ≡** | Start (main menu) | Start (Summon toggle in move menu; HP text) | Start |
| **View ⧉** | Select (same as X) | Select | Select |
| **L3** | V03 world map | — | — |
| **R3** | App menu (states, settings, layout editor) | same | same |
| **Right stick flick** (8 directions) | V09–V16: cast wheel slot n directly | — | — |
| Xbox / Backbone button | Leave to the system or the Backbone app | | |
| Share / capture | App screenshot (`MEDIA_RECORD` on Xbox) | | |
| Backbone Pro rear buttons | Default suggestion: remap in the Backbone app to L3 and R3 | | |

* **Face-button option:** "Label" (A→A, the default) or "Position" (the GBA's right-hand A button → the controller's right-hand B button).
* **Fallback app menu** for controllers without R3: hold View+Menu for 0.5 s.

### 5e. Touch mapping

* **Core controls:**
  * Cross D-pad with diagonals (RadialGamePad `useDiagonals`), or an optional floating stick quantised to 8 sectors.
  * A, B, L, R, Start, Select.
* **Extra buttons:**
  * **PSY** = Select (opens the wheel).
  * **RUN** = V01 toggle. Its icon shows only that it toggles; the ROM shows the actual state.
  * **DEX** = V02; **MAP** = V03.
  * **SUM** = V04, shown in battle when context detection is on [I: optional RAM peek, phase 2].
  * **≡** = app menu; **FF** = fast-forward.
* **Behaviour:**
  * Multi-touch, one pointer per control.
  * The thumb can slide from B to A.
  * Haptic tick on press.
  * Opacity 30–60 %, chosen by the user.
* **Layout storage:** a per-posture layout editor (drag, scale, opacity), saved for each of: `phonePortrait`, `phoneLandscape`, `coverPortrait`, `coverLandscape`, `innerPortrait`, `innerLandscape`, `tabletop`.

---

## 6. Layouts per posture

**Game scale rule:** `scale = max(1, min(zoneW / 240, zoneH / 160))`, rounded down to a whole number, where the zone is the area the layout gives the game. If the integer image would fill less than about 70 % of the zone, offer "Fit + Sharp shader" as an option. Place the image with `GLRetroView.viewport`.

**Size conversions:** cover 16.6 px/mm, inner 14.5 px/mm. Target sizes: D-pad Ø 28 mm, A/B Ø 13 mm, L/R 18 × 7 mm, small buttons at least 48 dp (about 8 mm).

| Layout | Screen (px) | Game | Image size (px / mm) | Control zone |
|---|---|---|---|---|
| Cover portrait | 1080 × 2520 | **4×** | 960 × 640 / 58 × 39 (≈ original GBA screen size) | Bottom ≈ 1,750 px |
| Cover landscape | 2520 × 1080 | **6×** | 1440 × 960 / 87 × 58 | Side columns 540 px (32 mm) each |
| Inner portrait (flat or book) | 1968 × 2184 | **8×** (7× optional) | 1920 × 1280 / 132 × 88 | Bottom 904 px (62 mm) |
| Inner landscape, flat, touch | 2184 × 1968 | **6×** (same as tabletop, so half-folding moves nothing) | 1440 × 960 | Bottom half |
| Tabletop (HALF_OPENED, hinge horizontal) | 2184 × ≈984 per half | **6×** in the top half | 1440 × 960 / 99 × 66 | Whole bottom half, minus a hinge keep-out band ≥ 48 dp |
| Inner landscape + controller | 2184 × 1968 | **9×** | 2160 × 1440 / 149 × 99 | Overlay hidden |
| Book (HALF_OPENED, hinge vertical) | 2 × ≈984 × 2184 | Same as inner portrait; controls kept outside the hinge bounds | — | — |
| Phone portrait (1080-wide FHD+) | 1080 × 2340 | 4× | 960 × 640 | Bottom ≈ 1,600 px |
| Phone landscape (FHD+) | 2340 × 1080 | 6× | 1440 × 960 | Sides 450 px each |
| Phone portrait / landscape (QHD+ 1440 × 3120) | — | 6× / 9× | 1440 × 960 / 2160 × 1440 | Bottom / sides 480 px |
| Phone 720p | 720 × 1600 | 3× portrait / 4× landscape | 720 × 480 / 960 × 640 | Bottom / sides 320 px |

**Cover screen, portrait** (also the standard phone portrait layout):
```
+----------------------------------+ y=0
|            ( o ) cutout          |  read DisplayCutout inset
| +------------------------------+ | y~120
| |      GAME 960 x 640  (4x)    | |
| +------------------------------+ | y~760
|  [= app]                  [FF]   |
|  [   L    ]        [    R    ]   | y~1250
|      [^]                  (A)    |
|  [<]     [>]          (B)        | y~1700  D-pad ~465px, A/B ~215px
|      [v]                         |
|  [PSY] [RUN]        [DEX] [MAP]  | y~2050
|       [SELECT]    [START]        | y~2250
|   (home-gesture inset: no buttons)| y=2520
+----------------------------------+
```

**Cover screen, landscape** (Backbone play is the same but with the overlay hidden; also the standard phone landscape layout):
```
+------------+----------------------------------+------------+
| [ L ] (o)* |                                  |      [ R ] |
| [=]        |                                  |       [FF] |
|     [^]    |      GAME 1440 x 960  (6x)       |      (A)   |
|  [<]   [>] |                                  |   (B)      |
|     [v]    |                                  | [DEX][MAP] |
| [PSY][RUN] |                                  |            |
| [SELECT]   |                                  |   [START]  |
+------------+----------------------------------+------------+
   540 px      * the punch hole sits on one short edge: shift L/R by the inset
```

**Inner screen, portrait (book held flat):**
```
+------------------------------------------+
| +--------------------:-----------------+ |
| |      GAME 1920 x 1280  (8x)          | |   ':' = crease (cosmetic only when FLAT)
| +--------------------:-----------------+ | y~1290
| [ L ]  [PSY][RUN]    :    [DEX][MAP] [ R ]|
|    [^]               :             (A)    |
| [<]   [>]            :          (B)       |  bottom 904 px
|    [v]               :                    |
|   [SELECT]           :          [START]   |
+------------------------------------------+
```

**Tabletop (game on the top half, controls on the bottom half); also inner landscape flat with touch:**
```
+----------------------------------------------------------+
| [=][FF] +----------------------------+  button legend /   |  top half ~2184 x 984
|         |   GAME 1440 x 960  (6x)    |  Psynergy slots   |
|         +----------------------------+  (app UI only)    |
|====================== hinge: FoldingFeature.bounds ======|
|                  keep-out band >= 48 dp                  |
| [  L  ]        [PSY] [RUN] [DEX] [MAP]          [  R  ]  |
|     [^]                                       (A)        |  bottom half
|  [<]   [>]        [SELECT]  [START]       (B)            |
|     [v]                                                  |
+----------------------------------------------------------+
  With a Bluetooth controller: overlay hidden; the bottom half shows the
  button legend or stays black (OLED). Laid flat, the game goes to 9x.
```

---

## 7. ROM-side work items (controls only; Psynergy, Summon and movement systems are separate topics)

| # | Work | Files / functions | Lines (approx.) |
|---|---|---|---|
| R1 | V-key chord decoder + `gExtKeysNew/Held` | `src/main.c` `ReadKeys()` (:269-296), `include/main.h` | 60–100 |
| R2 | Menu-safe diagonal filter (outside the field) | `ReadKeys()` or `field_control_avatar.c` | 15–25 |
| R3 | L/R → Psynergy shortcut dispatch; take DexNav off R; V01–V05 dispatch | `src/field_control_avatar.c` (`ProcessPlayerFieldInput` around :237-240) | 80–120 |
| R4 | Auto-run flag + B inversion (CFRU logic) + Options entry | `src/field_player_avatar.c` (:910-915), `src/option_menu.c` | 40–70 |
| R5 | 8-slot quick wheel (UI, registration from the Psynergy menu, slot cast) replacing Select's registered item | new `src/quick_wheel.c`, `field_control_avatar.c:237` | 400–600 |
| R6 | Battle: V04 → Summon list; Start toggle stays as the gimmick toggle | `src/battle_controller_player.c` (:394, :908-915) | 30–60 |
| R7 | Enable DexNav (flags and vars) + Start-menu entries for DexNav, Map, Set/Standby | `include/config/dexnav.h`, `src/start_menu.c` | 30–60 |

---

## 8. Effort estimates

**Basis:** an AI-assisted solo developer, with Claude Code doing the coding and the user play-testing.

| Package | Content | Lines | Calendar time | Confidence |
|---|---|---|---|---|
| **ROM controls (R1–R7)** | As above | ~700–1,000 | **5–8 days** (R5 and R6 wait on the Psynergy and Summon systems) | Medium |
| **P1: player app skeleton** | Gradle project; LibretroDroid; mGBA core `.so` (prebuilt from the libretro buildbot [I]); ROM load; SRAM and state auto-save; pause menu | ~500 | 2–3 days | Medium–high |
| **P2: input layer** | Device listener; key, hat, stick and trigger handling; 8-sector quantiser; semantic actions; chord encoder; remap storage; controller test screen | ~700 | 3–4 days | Medium |
| **P3: touch layouts** | RadialGamePad configs for 7 postures; layout editor; haptics | ~800–1,000 | 4–6 days | Medium |
| **P4: posture engine** | `WindowInfoTracker`; WindowMetrics; integer viewport; cutout and gesture exclusion; immersive; `configChanges`; frame rate; `appCategory="game"` | ~400 | 2–3 days | Medium |
| **P5: device test passes** | Fold 7 cover, inner and tabletop; Backbone wired; Xbox and Backbone Pro over Bluetooth; fold/unfold during battle | — | 3–5 days of user testing | Low–medium |
| **Player app total** | | **~2.5–3.5 k** | **≈ 3–5 weeks** | Medium |

**What would change the estimate:**
* LibretroDroid key events might not land on exact frames, which would make chords unreliable. A small native patch, or polling input inside `retro_run`, would add about 1 week.
* Backbone or Xbox Bluetooth may report keycodes that aren't standard (more remap UI).
* Samsung's continuity or Flex-mode behaviour could interfere with folding during play.
* Context-aware touch buttons (reading ROM RAM to detect field vs battle) would add about 3–5 days.
* Starting from a Lemuroid fork instead would make P3 faster but P1, P4 and long-term maintenance slower.

---

## 9. Acceptance tests (Fold 7)

1. Fold or unfold in the field and in a battle: no restart, no state loss, and the new layout appears in under 0.5 s.
2. Half-fold to tabletop: the game moves to the top half and the controls stay at least 48 dp from the hinge.
3. Connecting an Xbox controller over Bluetooth hides the overlay within 1 s; disconnecting brings it back.
4. Backbone (cover landscape): every button shows up correctly on the test screen.
5. Edge swipes over the D-pad never trigger Back. The system back action opens the pause menu.
6. Diagonal input on stick or touch produces diagonal movement (once the movement topic lands) and never double-moves menu cursors.
7. Each V-key (V01–V05, V09–V16) fires exactly once per press. In another emulator, the same features work through menus.
8. Steady 59.73 fps with no audio crackle at 1× speed.

## 10. Open questions

* Which Psynergy goes to L and R by default, and should the wheel hold 8 slots or 6 (CFRU uses 6)?
* Face-button default: by label or by position?
* Should RT be fast-forward or a third Psynergy shortcut?
* Should the ROM show the auto-run state on screen (an icon in the GS-style HUD, polish phase)?
* Needs device checks: Backbone fit on the Fold 7, the Backbone Pro's rear-button and Backbone-button keycodes, and the Xbox Bluetooth layout.

---

## Sources

**Local code** [V]:
* pokeemerald-expansion: `src/field_control_avatar.c:105-149,237,240`; `src/field_player_avatar.c:905-915`; `src/battle_controller_player.c:247-292,394-399,865,900-915`; `include/config/battle.h:360,380-381`; `include/config/dexnav.h:4-20`; `include/config/overworld.h:5`; `src/main.c:269-296`. All under `expansion/`.
* CFRU: `src/config.h:54-55`; `src/overworld.c:1731-1735,2838-2867,2955-2980`; `include/global.h:131,139-144`; `src/dexnav.c:2341-2342`. All under `…\external\Complete-Fire-Red-Upgrade\`.
* Design: `DESIGN.md:41,51,98,114,137,164-166`.

**Samsung:**
* [Samsung Newsroom: Galaxy Z Fold7 launch and spec table](https://news.samsung.com/global/samsung-galaxy-z-fold7-raising-the-bar-for-smartphones)
* [Samsung US: Fold7 cover/main screen tips](https://www.samsung.com/us/support/answer/ANS10006882/)
* [Samsung US: Flex mode](https://www.samsung.com/us/support/answer/ANS10003223/)
* [Samsung Dev: app continuity](https://developer.samsung.com/one-ui/foldable-and-largescreen/app-cont-and-multi.html)
* [Wikipedia: Galaxy Z Fold 7](https://en.wikipedia.org/wiki/Samsung_Galaxy_Z_Fold_7) (cross-check only)

**Android:**
* [Handle controller input](https://developer.android.com/develop/ui/views/touch-and-input/game-controllers/controller-input)
* [Make your app fold aware](https://developer.android.com/develop/ui/compose/layouts/adaptive/foldables/make-your-app-fold-aware)
* [Android 16 behaviour changes](https://developer.android.com/about/versions/16/behavior-changes-16)
* [Gesture navigation](https://developer.android.com/develop/ui/views/touch-and-input/gestures/gesturenav)
* [AOSP `Vendor_045e_Product_0b12.kl`](https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/main/data/keyboards/Vendor_045e_Product_0b12.kl)

**Controllers:**
* [Backbone Pro page](https://backbone.com/pages/pro)
* [Backbone Pro product](https://backbone.com/products/Backbone-Pro)

**Emulators and libraries:**
* [Lemuroid](https://github.com/Swordfish90/Lemuroid) (HEAD tarball 2026-10-12: `MobileGameScreen.kt`, `TouchControllerSettingsManager.kt`, `InputDeviceManager.kt`, `CoreID.kt`, `AndroidManifest.xml`)
* [LibretroDroid](https://github.com/Swordfish90/LibretroDroid) (`GLRetroView.kt`, `GLRetroViewData.kt`, LICENSE)
* [RadialGamePad](https://github.com/Swordfish90/RadialGamePad) (`CrossConfig.kt`, `PrimaryDialConfig.kt`, `HapticConfig.kt`, README, LICENSE)
* [mGBA libretro core options](https://raw.githubusercontent.com/libretro/mgba/master/src/platform/libretro/libretro_core_options.h) and [LICENSE](https://raw.githubusercontent.com/libretro/mgba/master/LICENSE)
* [Pizza Boy A Pro (Google Play)](https://play.google.com/store/apps/details?id=it.dbtecno.pizzaboygbapro)
* RetroArch overlays (forum posts, secondary): [RetroPad Editor](https://forums.libretro.com/t/retropad-editor-create-and-edit-onscreen-gamepads/38331), [RGPAD](https://forums.libretro.com/t/rgpad-a-universal-gamepad-overlay/41134)