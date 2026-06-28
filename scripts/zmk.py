#!/usr/bin/env python3
"""do52 / do52pro ZMK build helper.

One tool for setting up the workspace, building, and flashing the firmware.
Replaces the old setup.sh / build.sh / flash.sh.

  ./scripts/zmk.py setup                 # one-time environment bootstrap
  ./scripts/zmk.py update                # `west update` (run after editing west.yml)
  ./scripts/zmk.py build [side] [opts]   # -> ./firmware/<keyboard>_<side>.uf2
  ./scripts/zmk.py flash [side]          # copy the .uf2 to a nice!nano bootloader
  ./scripts/zmk.py deploy [side] [opts]  # build then flash in one step
  ./scripts/zmk.py reset [side]          # flash settings_reset.uf2 to wipe BLE bonds

`side` is one of: left | right | both (default: both).

Defaults: --keyboard do52pro, --board nice_nano//zmk (env KEYBOARD / BOARD also
honored). The RIGHT half is the BLE central. Built against stock upstream ZMK
(zmkfirmware/main) — no trackpoint; mouse keys via CONFIG_ZMK_POINTING.

Stdlib only, so it runs before the venv/toolchain exist. Uses `uv` to manage
the Python env and `west`. The west workspace is this repo; the venv lives at
./.venv. Works on macOS (Homebrew) and inside a Nix devShell (see flake.nix).
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = PROJECT_DIR / ".venv"
FIRMWARE_DIR = PROJECT_DIR / "firmware"
RESET_UF2 = FIRMWARE_DIR / "settings_reset.uf2"

DEFAULT_KEYBOARD = os.environ.get("KEYBOARD", "do52pro")
# HWMv2 board id on current ZMK. The old flat "nice_nano_v2" name is gone:
# it's now the `nice_nano` board (revision 2.0.0 by default) + ZMK variant.
DEFAULT_BOARD = os.environ.get("BOARD", "nice_nano//zmk")
# Fallback toolchain root if arm-none-eabi-gcc is not on PATH (bare macOS).
DEFAULT_TOOLCHAIN = "/Applications/ArmGNUToolchain/15.2.rel1/arm-none-eabi"

NICENANO_VOLUMES = ("/Volumes/NICENANO", "/Volumes/NRF52BOOT", "/Volumes/NICE!NANO")

# --- logging ---------------------------------------------------------------

_TTY = sys.stdout.isatty()
_C = {"red": "\033[0;31m", "green": "\033[0;32m", "yellow": "\033[1;33m",
      "blue": "\033[0;34m", "cyan": "\033[0;36m", "nc": "\033[0m"}


def _col(name: str) -> str:
    return _C[name] if _TTY else ""


def info(msg: str) -> None:
    print(f"{_col('blue')}[INFO]{_col('nc')} {msg}")


def ok(msg: str) -> None:
    print(f"{_col('green')}[OK]{_col('nc')} {msg}")


def warn(msg: str) -> None:
    print(f"{_col('yellow')}[WARN]{_col('nc')} {msg}")


def die(msg: str) -> None:
    print(f"{_col('red')}[ERROR]{_col('nc')} {msg}", file=sys.stderr)
    sys.exit(1)


# --- helpers ---------------------------------------------------------------

def run(cmd: list[str], env: dict | None = None, check: bool = True) -> int:
    """Run a command, echoing it first."""
    info("$ " + " ".join(cmd))
    result = subprocess.run(cmd, cwd=PROJECT_DIR, env=env)
    if check and result.returncode != 0:
        die(f"command failed ({result.returncode}): {' '.join(cmd)}")
    return result.returncode


def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def toolchain_env() -> dict:
    """Build the environment for west: venv on PATH + ARM toolchain located."""
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(VENV_DIR)
    env["PATH"] = f"{VENV_DIR / 'bin'}{os.pathsep}{env.get('PATH', '')}"
    env["ZEPHYR_TOOLCHAIN_VARIANT"] = "gnuarmemb"

    gcc = shutil.which("arm-none-eabi-gcc")
    if gcc:
        # toolchain root = the dir that contains bin/arm-none-eabi-gcc
        env["GNUARMEMB_TOOLCHAIN_PATH"] = str(Path(gcc).resolve().parent.parent)
    else:
        env.setdefault("GNUARMEMB_TOOLCHAIN_PATH", DEFAULT_TOOLCHAIN)
    return env


def sides_for(target: str) -> list[str]:
    return ["left", "right"] if target == "both" else [target]


# --- commands --------------------------------------------------------------

def cmd_setup(args: argparse.Namespace) -> None:
    info("Bootstrapping ZMK build environment...")

    in_nix = bool(os.environ.get("IN_NIX_SHELL"))
    sys_tools = ("cmake", "ninja", "dtc")
    missing = [t for t in sys_tools if not have(t)]

    if in_nix or have("arm-none-eabi-gcc"):
        info("ARM toolchain / nix shell detected — skipping Homebrew installs.")
        if missing:
            warn(f"Missing tools not on PATH: {', '.join(missing)} "
                 "(add them to your devShell).")
    elif sys.platform == "darwin":
        if not have("brew"):
            die("Homebrew not found. Install it, or run inside `nix develop`.")
        if missing:
            run(["brew", "install", *missing, "python3"])
        if not have("arm-none-eabi-gcc"):
            info("Installing ARM GCC toolchain via Homebrew cask...")
            run(["brew", "install", "--cask", "gcc-arm-embedded"])
    else:
        warn("Non-macOS, non-nix host: install cmake/ninja/dtc and the ARM "
             "toolchain yourself (or use `nix develop`).")

    if not have("uv"):
        if sys.platform == "darwin" and have("brew") and not in_nix:
            run(["brew", "install", "uv"])
        else:
            die("`uv` not found. Install it (https://docs.astral.sh/uv/) "
                "or add it to your devShell.")

    info("Creating uv venv at .venv ...")
    run(["uv", "venv", str(VENV_DIR)])
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(VENV_DIR)

    info("Installing west ...")
    run(["uv", "pip", "install", "west"], env=env)

    if not (PROJECT_DIR / ".west").exists():
        info("Initializing west workspace ...")
        run(["uv", "run", "west", "init", "-l", "config"], env=env)

    info("Fetching ZMK + Zephyr (this can take a while) ...")
    run(["uv", "run", "west", "update"], env=env)
    run(["uv", "run", "west", "zephyr-export"], env=env)

    reqs = PROJECT_DIR / "zephyr" / "scripts" / "requirements.txt"
    if reqs.exists():
        info("Installing Zephyr Python requirements ...")
        run(["uv", "pip", "install", "-r", str(reqs)], env=env)

    module_yml = PROJECT_DIR / "zephyr" / "module.yml"
    if not module_yml.exists():
        info("Writing zephyr/module.yml ...")
        module_yml.parent.mkdir(parents=True, exist_ok=True)
        module_yml.write_text("build:\n  settings:\n    board_root: .\n")

    ok("Setup complete. Build with: ./scripts/zmk.py build")


def cmd_update(args: argparse.Namespace) -> None:
    if not VENV_DIR.exists():
        die("No .venv — run `./scripts/zmk.py setup` first.")
    run(["uv", "run", "west", "update"], env=toolchain_env())
    ok("west update complete.")


def cmd_build(args: argparse.Namespace) -> None:
    if not VENV_DIR.exists():
        die("No .venv — run `./scripts/zmk.py setup` first.")
    env = toolchain_env()
    FIRMWARE_DIR.mkdir(parents=True, exist_ok=True)

    for side in sides_for(args.side):
        shield = f"{args.keyboard}_{side}"
        info(f"Building {shield} on {args.board} ...")
        cmd = ["uv", "run", "west", "build", "-s", "zmk/app",
               "-b", args.board]
        if args.pristine:
            cmd.append("--pristine")
        cmd += ["--", f"-DSHIELD={shield}",
                f"-DZMK_CONFIG={PROJECT_DIR / 'config'}",
                f"-DBOARD_ROOT={PROJECT_DIR}"]
        run(cmd, env=env)

        uf2 = PROJECT_DIR / "build" / "zephyr" / "zmk.uf2"
        if not uf2.exists():
            die(f"Build produced no zmk.uf2 for {side}")
        dest = FIRMWARE_DIR / f"{shield}.uf2"
        shutil.copy2(uf2, dest)
        ok(f"Built: {dest}")

    print()
    ok("Build complete. Flash with: ./scripts/zmk.py flash")


def _wait_for_bootloader(timeout: int = 60) -> str | None:
    print(f"{_col('cyan')}")
    print("  Double-tap RESET on the nice!nano now — waiting for the "
          "bootloader drive...")
    print(f"{_col('nc')}", end="", flush=True)
    for elapsed in range(timeout):
        for vol in NICENANO_VOLUMES:
            if os.path.isdir(vol):
                print()
                return vol
        time.sleep(1)
        print(f"\r{_col('yellow')}Waiting... {elapsed + 1}s{_col('nc')}  ",
              end="", flush=True)
    print()
    return None


def _flash_uf2(fw: Path, label: str) -> None:
    """Wait for a nice!nano bootloader drive and copy `fw` onto it."""
    if not fw.exists():
        die(f"Firmware not found: {fw}")

    info(f"Ready to flash {label}: {fw}")
    vol = _wait_for_bootloader()
    if not vol:
        die("Timed out waiting for the bootloader (double-tap RESET quickly).")

    info(f"Found bootloader at {vol} — copying ...")
    # The bootloader reboots the instant the copy finishes, yanking the drive
    # mid-write; macOS reports an I/O error even though the flash succeeded.
    # Ignore the copy error and confirm success by the volume disappearing.
    try:
        shutil.copy(fw, vol)
    except OSError:
        pass
    time.sleep(2)

    if os.path.isdir(vol):
        die(f"Volume still mounted at {vol} — flash may have failed.")
    ok(f"Flashed {label} (board rebooted).")


def _flash_one(keyboard: str, side: str) -> None:
    fw = FIRMWARE_DIR / f"{keyboard}_{side}.uf2"
    if not fw.exists():
        die(f"Firmware not found: {fw}\nRun `./scripts/zmk.py build {side}` first.")
    _flash_uf2(fw, f"{keyboard}_{side}")


def cmd_flash(args: argparse.Namespace) -> None:
    sides = sides_for(args.side)
    for i, side in enumerate(sides):
        print(f"\n{_col('green')}=== Flashing {side.upper()} ==={_col('nc')}")
        _flash_one(args.keyboard, side)
        if i + 1 < len(sides):
            input(f"\n{_col('yellow')}Swap to the {sides[i + 1]} half, then "
                  f"press Enter...{_col('nc')}")
    ok("Done.")


def cmd_deploy(args: argparse.Namespace) -> None:
    """Build then flash in one step (build aborts on failure, so flash only
    runs if every requested side built cleanly)."""
    cmd_build(args)
    cmd_flash(args)


def _build_reset(board: str) -> None:
    """Build ZMK's `settings_reset` shield -> firmware/settings_reset.uf2.

    This UF2 wipes all stored BLE bonds. It's the reliable way to recover when
    the split central role changes and the halves won't re-pair, since the
    peripheral can't clear its bond from the keymap. Built in its own dir so it
    never clobbers the normal `build/` tree.
    """
    if not VENV_DIR.exists():
        die("No .venv — run `./scripts/zmk.py setup` first.")
    env = toolchain_env()
    FIRMWARE_DIR.mkdir(parents=True, exist_ok=True)
    info(f"Building settings_reset on {board} ...")
    run(["uv", "run", "west", "build", "-s", "zmk/app", "-b", board,
         "--pristine", "-d", "build_reset", "--",
         "-DSHIELD=settings_reset", f"-DBOARD_ROOT={PROJECT_DIR}"], env=env)
    uf2 = PROJECT_DIR / "build_reset" / "zephyr" / "zmk.uf2"
    if not uf2.exists():
        die("Build produced no zmk.uf2 for settings_reset")
    shutil.copy2(uf2, RESET_UF2)
    ok(f"Built: {RESET_UF2}")


def cmd_reset(args: argparse.Namespace) -> None:
    """Wipe BLE bonds: flash settings_reset.uf2 to the chosen half/halves.

    settings_reset replaces the keyboard app, so afterwards the board does
    nothing until you reload the real firmware with `flash` / `deploy`. Reset
    BOTH halves when the central role changed — clearing only one leaves a
    mismatched bond and they still won't link."""
    if args.rebuild or not RESET_UF2.exists():
        _build_reset(args.board)
    else:
        info(f"Using existing {RESET_UF2} (pass --rebuild to rebuild it)")

    sides = sides_for(args.side)
    for i, side in enumerate(sides):
        print(f"\n{_col('green')}=== Resetting {side.upper()} ==={_col('nc')}")
        _flash_uf2(RESET_UF2, f"settings_reset ({side})")
        if i + 1 < len(sides):
            input(f"\n{_col('yellow')}Swap to the {sides[i + 1]} half, then "
                  f"press Enter...{_col('nc')}")
    print()
    warn(f"Bonds wiped. Now reload firmware: ./scripts/zmk.py flash {args.side}")


# --- arg parsing -----------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="zmk.py", description="do52 / do52pro ZMK build helper")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("setup", help="one-time environment bootstrap").set_defaults(
        func=cmd_setup)
    sub.add_parser("update", help="run `west update`").set_defaults(
        func=cmd_update)

    def add_target(sp):
        sp.add_argument("side", nargs="?", default="both",
                        choices=["left", "right", "both"],
                        help="which half (default: both)")
        sp.add_argument("--keyboard", default=DEFAULT_KEYBOARD,
                        help=f"shield keyboard (default: {DEFAULT_KEYBOARD})")

    b = sub.add_parser("build", help="build firmware -> ./firmware")
    add_target(b)
    b.add_argument("--board", default=DEFAULT_BOARD,
                   help=f"target board (default: {DEFAULT_BOARD})")
    b.add_argument("--no-pristine", dest="pristine", action="store_false",
                   help="incremental build (default: pristine)")
    b.set_defaults(func=cmd_build, pristine=True)

    f = sub.add_parser("flash", help="flash a built .uf2 to a nice!nano")
    add_target(f)
    f.set_defaults(func=cmd_flash)

    r = sub.add_parser("reset",
                       help="wipe BLE bonds (flash settings_reset.uf2)")
    r.add_argument("side", nargs="?", default="both",
                   choices=["left", "right", "both"],
                   help="which half (default: both)")
    r.add_argument("--board", default=DEFAULT_BOARD,
                   help=f"target board (default: {DEFAULT_BOARD})")
    r.add_argument("--rebuild", action="store_true",
                   help="rebuild settings_reset.uf2 even if it already exists")
    r.set_defaults(func=cmd_reset)

    d = sub.add_parser("deploy", help="build then flash in one step")
    add_target(d)
    d.add_argument("--board", default=DEFAULT_BOARD,
                   help=f"target board (default: {DEFAULT_BOARD})")
    d.add_argument("--no-pristine", dest="pristine", action="store_false",
                   help="incremental build (default: pristine)")
    d.set_defaults(func=cmd_deploy, pristine=True)

    return p


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
