# CLAUDE.md

ZMK firmware for the **do52 / do52pro** split keyboard.

## Current / canonical target

> **Edit the do52 config for current work.** The active hardware is the
> **do52 on nice!nano v2 (nRF52840)** with a **PS/2 trackpoint on the RIGHT
> half**. The `do52pro` shield and the RP2040 board are older variants kept for
> reference — don't edit them unless you specifically mean to.

Split roles: the **RIGHT half is the BLE central** (it connects to the host and
runs the trackpoint); the **LEFT half is the peripheral**. This is set in
`boards/shields/do52/Kconfig.defconfig`.

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

## Build & flash (local)

Prereqs (one-time): `./scripts/setup.sh` creates the west workspace +
`~/zmk-workspace/.venv` and expects the ARM toolchain at
`/Applications/ArmGNUToolchain/15.2.rel1/arm-none-eabi`.

```bash
# After ANY change to config/west.yml, refresh the workspace once:
source ~/zmk-workspace/.venv/bin/activate && west update

# Build -> ./firmware/do52_<side>.uf2
./scripts/build.sh both      # or: left | right

# Flash a half (double-tap RESET on that nice!nano when prompted)
./scripts/flash.sh both      # or: left | right
```

Both scripts default to `KEYBOARD=do52` / `BOARD=nice_nano_v2`. To build the
older variant: `KEYBOARD=do52pro ./scripts/build.sh both`.

After flashing, if the halves or the host won't connect (the central side
changed), clear BLE bonds on both halves (a `&bt BT_CLR` keybind or a
`settings_reset` UF2) and re-pair.

## Build & flash (CI)

Pushing triggers `.github/workflows/build.yml`, which builds `do52_left`,
`do52_right`, `do52pro_left`, `do52pro_right` on `nice_nano_v2` and uploads each
`.uf2` as a workflow artifact.
