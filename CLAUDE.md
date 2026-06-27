# CLAUDE.md

ZMK firmware for the **do52 / do52pro** split keyboard.

> **Maintenance rule:** keep this file in sync with reality. Whenever you change
> a config path, a build/flash step, the west manifest, the trackpoint wiring,
> or the split roles, update the relevant section here in the same change.

## Current / canonical target

> **Edit the do52 config for current work.** The active hardware is the
> **do52 on nice!nano v2 (nRF52840)** with a **PS/2 trackpoint on the RIGHT
> half**. The `do52pro` shield and the RP2040 board are older variants kept for
> reference — don't edit them unless you specifically mean to.

Split roles: the **RIGHT half is the BLE central** (it connects to the host and
runs the trackpoint); the **LEFT half is the peripheral**. This is set in
`boards/shields/do52/Kconfig.defconfig`. The `do52pro` variant now mirrors this
— RIGHT central with the PS/2 trackpoint on the right half
(`boards/shields/do52pro/Kconfig.defconfig`,
`boards/shields/do52pro/do52pro_ps2_mouse.dtsi`).

## Where the configs live

| What you want to change | File(s) |
| --- | --- |
| Keymap / layers / behaviors | `config/do52.keymap` |
| Per-build Kconfig options | `config/do52.conf` |
| ZMK source + driver modules (west manifest) | `config/west.yml` |
| Key matrix + physical layout | `boards/shields/do52/do52.dtsi` |
| Per-half column pins | `boards/shields/do52/do52_left.overlay`, `do52_right.overlay` |
| **Trackpoint (PS/2) pins & settings** | `boards/shields/do52/do52_ps2_mouse.dtsi` |
| Split central/peripheral role, keyboard name | `boards/shields/do52/Kconfig.defconfig` |
| Shield/board build matrix (local + CI) | `build.yaml`, `.github/workflows/build.yml` |

`do52pro` equivalents live in `config/do52pro.*` and
`boards/shields/do52pro/`.

The committed firmware is tiny (~170K, ~38 files): just `config/`, `boards/`,
`scripts/`, `build.yaml`, and the workflow. Everything heavy is fetched by west
(see below) and gitignored.

## Trackpoint notes

- Driver: [infused-kim/kb_zmk_ps2_mouse_trackpoint_driver](https://github.com/infused-kim/kb_zmk_ps2_mouse_trackpoint_driver),
  pulled in via `config/west.yml`.
- It requires ZMK's mouse PR, so `config/west.yml` points `zmk` at the fork
  `infused-kim @ pr-testing/mouse_ps2_module_base` instead of `zmkfirmware/main`.
  (Stock ZMK main has no mouse support and won't build with the driver.)
- That fork is older and locates the matrix via a `chosen` node, so
  `do52.dtsi` / `do52pro.dtsi` include both a legacy `chosen` block and the
  newer `zmk,physical-layout` node.
- The driver only runs on the BLE **central** — that's why the trackpoint half
  must be the central (currently RIGHT).
- Pins on the right controller (nice!nano "pro_micro" numbering):
  **SCL/clock = D15 (P1.13), SDA/data = D16 (P0.10)**, UART PS/2 driver @ 14400
  baud. No hardware reset pin is wired — the driver uses the PS/2 software
  reset. Change these in `do52_ps2_mouse.dtsi` if the trackpoint is wired
  differently.

## Toolchain & workspace layout

One script drives everything: **`scripts/zmk.py`** (`setup` / `update` /
`build` / `flash`). It's stdlib-only and uses **`uv`** to manage the Python env
and `west`.

Toolchain comes from one of two places, auto-detected by `zmk.py`:

- **Nix:** `nix develop` (see `flake.nix`) provides `cmake ninja dtc
  gcc-arm-embedded uv python3`. If `arm-none-eabi-gcc` is on `PATH`, `zmk.py`
  derives `GNUARMEMB_TOOLCHAIN_PATH` from it.
- **macOS/Homebrew:** `zmk.py setup` installs the brew deps + the
  `gcc-arm-embedded` cask. Fallback toolchain path if not on `PATH`:
  `/Applications/ArmGNUToolchain/15.2.rel1/arm-none-eabi`.

The west workspace is **THIS repo**. `.west/config` points its manifest at
`./config`, and `west update` clones the deps *into the repo root*: `zmk/`
(~45M), `zephyr/` (~600M), `modules/` (~3GB). The uv venv lives at `./.venv`.
All are gitignored, along with `kb_zmk_ps2_mouse_trackpoint_driver/` (the driver
clone — west manages it, never commit it).

## Build & flash (local)

```bash
# One-time (brew on macOS, or run inside `nix develop` first):
./scripts/zmk.py setup

# After ANY change to config/west.yml, refresh the checkout once so zmk/ and
# the modules switch to the manifest's revisions:
./scripts/zmk.py update

# Build -> ./firmware/do52pro_<side>.uf2
./scripts/zmk.py build both      # or: left | right

# Flash a half (double-tap RESET on that nice!nano when prompted)
./scripts/zmk.py flash both      # or: left | right

# Build then flash in one step
./scripts/zmk.py deploy both     # or: left | right
```

Defaults are `--keyboard do52pro` / `--board nice_nano_v2` (env `KEYBOARD`/`BOARD`
also honored). To build the plain do52:
`./scripts/zmk.py build both --keyboard do52`.

After flashing, if the halves or the host won't connect (the central side
changed), clear BLE bonds on both halves (a `&bt BT_CLR` keybind or a
`settings_reset` UF2) and re-pair.

## Build & flash (CI)

Pushing triggers `.github/workflows/build.yml`, which builds `do52_left`,
`do52_right`, `do52pro_left`, `do52pro_right` on `nice_nano_v2` and uploads each
`.uf2` as a workflow artifact.
