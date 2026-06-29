# CLAUDE.md

ZMK firmware for the **do52 / do52pro** split keyboard.

> **Maintenance rule:** keep this file in sync with reality. Whenever you change
> a config path, a build/flash step, the west manifest, the trackpoint wiring,
> or the split roles, update the relevant section here in the same change.

## Current / canonical target

> **Edit the do52 config for current work.** The active hardware is the
> **do52 on nice!nano v2 (nRF52840)**. The `do52pro` shield and the RP2040
> board are older variants kept for reference — don't edit them unless you
> specifically mean to.

> **Built against stock upstream ZMK (`zmkfirmware/main`).** The PS/2 trackpoint
> (and the infused-kim ZMK fork it required) was removed — see
> [Pointer / trackpoint](#pointer--trackpoint). Mouse-key emulation still works
> via `CONFIG_ZMK_POINTING`, and **ZMK Studio is enabled** — see
> [ZMK Studio](#zmk-studio).

> **Board id is `nice_nano//zmk`, not `nice_nano_v2`.** Current ZMK uses
> Zephyr's HWMv2: the flat `nice_nano_v2` name is gone; it's now the `nice_nano`
> board (revision 2.0.0 by default) plus a ZMK variant. `zmk.py` defaults to the
> new id.

Split roles: the **RIGHT half is the BLE central** (it connects to the host);
the **LEFT half is the peripheral**. This is set in
`boards/shields/do52/Kconfig.defconfig`; `do52pro` mirrors it
(`boards/shields/do52pro/Kconfig.defconfig`). Right-central is a leftover from
the trackpoint era — either half could be central now, but changing it forces a
BLE re-pair, so leave it without a reason.

## Where the configs live

| What you want to change | File(s) |
| --- | --- |
| Keymap / layers / behaviors | `config/do52.keymap` |
| Per-build Kconfig options | `config/do52.conf` |
| ZMK source revision (west manifest) | `config/west.yml` |
| Key matrix + physical layout | `boards/shields/do52/do52.dtsi` |
| Per-half column pins | `boards/shields/do52/do52_left.overlay`, `do52_right.overlay` |
| Split central/peripheral role, keyboard name | `boards/shields/do52/Kconfig.defconfig` |
| Shield/board build matrix (local + CI) | `build.yaml`, `.github/workflows/build.yml` |

`do52pro` equivalents live in `config/do52pro.*` and
`boards/shields/do52pro/`.

The committed firmware is tiny (~170K, ~38 files): just `config/`, `boards/`,
`scripts/`, `build.yaml`, and the workflow. Everything heavy is fetched by west
(see below) and gitignored.

## Pointer / trackpoint

- **Mouse-key emulation is on** (`CONFIG_ZMK_POINTING=y` in `config/do52.conf`
  and `config/do52pro.conf`). Keymaps use `&mkp` / `&mmv` / `&msc` with
  `#include <dt-bindings/zmk/pointing.h>`. Enabling it changes the HID report
  descriptor, so **re-pair BLE hosts** after first flashing it.
- **`main`: no physical trackpoint.** The PS/2 trackpoint was dropped when
  moving to stock ZMK, because the driver's *bundled* `zmk,input-listener-ps2`
  listener targeted the old mouse-PR fork's `zmk/mouse/*` HID API, which no
  longer exists on `zmkfirmware/main`.
- **`trackpoint-mainline` branch: physical trackpoint working on stock ZMK /
  Zephyr 4.1.** **The trackpoint is wired to the RIGHT half — the BLE split
  central — because the PS/2 driver only runs on the central.** This applies to
  both keyboards: `do52_right.overlay` and `do52pro_right.overlay` each
  `#include` their `*_ps2_mouse.dtsi`; the left halves are plain peripherals
  with no pointer hardware. After flashing, if only the right half types,
  that's a BLE bond mismatch, not a keymap bug — clear bonds on **both** halves
  (`./scripts/zmk.py reset both`), reflash both, and re-pair the host.
  The fix was small because
  [infused-kim/kb_zmk_ps2_mouse_trackpoint_driver](https://github.com/infused-kim/kb_zmk_ps2_mouse_trackpoint_driver)
  already emits standard Zephyr input events (`input_report_rel`/`_key`); only
  its bundled HID listener was fork-coupled. The port:
  - Pulls the driver via `config/west.yml` from our fork
    [TomatoCream/kb_zmk_ps2_mouse_trackpoint_driver](https://github.com/TomatoCream/kb_zmk_ps2_mouse_trackpoint_driver),
    branch `zephyr-4.1`, into a gitignored, west-managed checkout at
    `kb_zmk_ps2_mouse_trackpoint_driver/`.
  - Wires it in `boards/shields/{do52,do52pro}/{do52,do52pro}_ps2_mouse.dtsi`
    (included from each `*_right.overlay`) using the
    **stock** `zmk,input-listener` (NOT the bundled `-ps2` one), so
    `src/mouse/input_listener_ps2.c` is never compiled. Axis swap is done in
    software on the listener via `&zip_xy_transform INPUT_TRANSFORM_XY_SWAP`
    (works on any trackpoint, unlike the hardware `tp-xy-swap` config bit).
    Pins: SCL/clock = D15 (P1.13), SDA/data = D16 (P0.10), UART @ 14400.
  - The fork's `zephyr-4.1` branch carries the only source change needed for
    Zephyr 4.1: `K_THREAD_STACK_MEMBER` → `K_KERNEL_STACK_MEMBER` in
    `input_mouse_ps2.c` (also kept as `patches/kb_ps2_zephyr-4.1.patch` for
    reference). Because `west.yml` points at the fork, a fresh `west update`
    pulls the fix automatically — no patching needed. To pull upstream driver
    updates, rebase the fork's `zephyr-4.1` branch onto infused-kim/main.

### Switching back to the legacy trackpoint firmware

The whole pre-migration setup (infused-kim ZMK fork + a *working* PS/2
trackpoint) is preserved on the **`trackpoint-legacy`** branch. Switching is a
branch checkout **plus a forced `west update`** — not just a checkout — because
the two lines pin different ZMK *and* Zephyr revisions, and the `zmk/ zephyr/
modules/` trees are shared on disk (west-managed, gitignored).

Stock `main` → legacy trackpoint:

```bash
git checkout trackpoint-legacy
# the shared zmk/ checkout is on stock main and will block the switch; it's
# disposable, so wipe it, then refetch the fork + the trackpoint driver:
git -C zmk reset --hard && git -C zmk clean -fd
./scripts/zmk.py update
./scripts/zmk.py build both      # legacy zmk.py defaults to board nice_nano_v2
./scripts/zmk.py flash both
```

Legacy → back to stock `main` (same dance in reverse):

```bash
git checkout main
git -C zmk reset --hard && git -C zmk clean -fd
./scripts/zmk.py update          # refetches zmkfirmware/main + Zephyr 4.1
./scripts/zmk.py build both      # board is nice_nano//zmk on this branch
```

Notes:
- Each `update` re-downloads Zephyr/modules for that line (GBs, slow) since the
  fork and main pin different versions. After a major Zephyr change also re-run
  the Python deps (see the workspace note below).
- Board id differs by branch — `nice_nano_v2` (legacy) vs `nice_nano//zmk`
  (main); each branch's `zmk.py` already defaults to the right one.
- The two firmwares have different HID report descriptors, so **re-pair your
  BLE hosts** after switching. If the halves won't link, wipe bonds on both
  with `./scripts/zmk.py reset both`, then reflash.

## ZMK Studio

Live keymap editing at <https://studio.zmk.dev> (Chrome/Edge — needs WebSerial;
Safari/Firefox won't work). Enabled by:

- `CONFIG_ZMK_STUDIO=y` in both `.conf` files.
- The `studio-rpc-usb-uart` snippet on the **central (RIGHT)** build only. Locally
  `zmk.py` adds it to the right half automatically (`CENTRAL_SIDE`); in CI it's
  the `snippet:` on the `*_right` rows of `build.yaml`. Studio and `zmk-usb-logging`
  both claim the USB CDC ACM, so a build can't have both.
- `&studio_unlock` bound on the **base layer**, right-outer thumb (the old
  `RGUI` position) so unlock is one press on the half you plug in.
- A `keys = <&key_physical_attrs ...>` list on each `zmk,physical-layout`
  (Studio refuses to build without key positions). These are **approximate**
  auto-generated coordinates (flat ortho split + DPADs as a `+`), regenerated by
  `scripts/gen_layout.py` if the matrix changes — not the true board geometry.

To use it: plug the RIGHT half into the host over USB, open studio.zmk.dev,
connect, then tap the right-outer thumb (`&studio_unlock`) to unlock.

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
All are gitignored.

> After a `west.yml` revision change, `west update` may abort with "local
> changes would be overwritten" if the old `zmk/` checkout was dirty. It's
> west-managed and disposable: `git -C zmk reset --hard && git -C zmk clean -fd`,
> then re-run `update`. The current Zephyr (4.1.0) also needs its Python deps
> (e.g. `pyelftools`); `zmk.py setup` installs `zephyr/scripts/requirements.txt`
> — re-run that install after a major Zephyr bump. ZMK Studio's RPC codegen
> additionally needs `protobuf` + `grpcio-tools` in the venv
> (`uv pip install protobuf grpcio-tools`).

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

# Wipe BLE bonds when the halves/host won't connect (e.g. central role changed).
# Builds + flashes ZMK's settings_reset shield; afterwards reload real firmware.
./scripts/zmk.py reset both      # or: left | right
```

Defaults are `--keyboard do52pro` / `--board nice_nano//zmk` (env
`KEYBOARD`/`BOARD` also honored). To build the plain do52:
`./scripts/zmk.py build both --keyboard do52`.

After flashing, if the halves or the host won't connect (the central side
changed), clear BLE bonds on **both** halves with `./scripts/zmk.py reset both`
(it flashes the `settings_reset` UF2), then reload the real firmware with
`./scripts/zmk.py flash both` (or `deploy both`) and re-pair. Resetting only one
half leaves a mismatched bond and the halves still won't link.

## Build & flash (CI)

Pushing triggers `.github/workflows/build.yml`, which builds `do52_left`,
`do52_right`, `do52pro_left`, `do52pro_right` on `nice_nano//zmk` and uploads
each `.uf2` as a workflow artifact. (CI board id updated alongside the local
default but not yet verified on a push.)
