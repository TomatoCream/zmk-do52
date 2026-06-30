#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["tabulate"]
# ///
"""Generate config/do52pro.keymap from layer data with auto-aligned columns.

The whole point: you edit the LAYERS data below as plain lists of bindings and
`tabulate` pads every column so the file stays readable. No more lining up
`&kp` tokens by hand.

Data model: each layer is split by **hand** (`left` / `right`). A hand is a dict
with two sub-divisions:

  layer(name,
      left ={"main": [ r0, r1, r2, r3, thumb ],   # 5 rows x 6 cells
             "dpad": [ l, d, m, u, r ]},           # one 5-way cluster
      right={"main": [ r0, r1, r2, r3, thumb ],
             "dpad": [ l, d, m, u, r ]},
  )

- `main`  : 5 rows x 6 cells. The thumb is just the last row (merged in, so it
            lines up under the main keys). "" is a blank thumb position.
- `dpad`  : the hand's 5-way cluster (Left, Down, Middle, Up, Right). Each half
            has its own, so it lives inside the hand. Optional.

The builder concatenates left["main"][i] + right["main"][i] into a 12-key row
(tabulate splits it 6|6), then emits the left dpad followed by the right dpad —
matching the matrix-transform order in boards/shields/do52pro/do52pro.dtsi.

Usage (uv auto-installs tabulate from the inline metadata above):
    uv run scripts/gen_keymap.py                 # write config/do52pro.keymap
    uv run scripts/gen_keymap.py --stdout        # print instead of writing

Generate then hand off to zmk.py (so one command edits + builds + flashes):
    uv run scripts/gen_keymap.py --build [SIDE]  # write, then `zmk.py build SIDE`
    uv run scripts/gen_keymap.py --deploy [SIDE] # write, then `zmk.py deploy SIDE`
    # SIDE is left|right|both (default both). Add --incremental for a fast
    # (non-pristine) rebuild — much quicker when only the keymap changed.
    uv run scripts/gen_keymap.py --deploy both --incremental
"""
import argparse
import subprocess
import sys
from pathlib import Path

from tabulate import tabulate

ZMK_PY = Path(__file__).resolve().parent / "zmk.py"

OUT = Path(__file__).resolve().parent.parent / "config" / "do52pro.keymap"

HAND_COLS = 6  # cells per hand per main row (left 6 | right 6 = 12-key row)
DPAD_COLS = 5  # cells in a 5-way dpad cluster (Left, Down, Middle, Up, Right)

HEADER = """\
#include <behaviors.dtsi>
#include <dt-bindings/zmk/keys.h>
#include <dt-bindings/zmk/pointing.h>
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/ext_power.h>

&lt {
    tapping-term-ms = <120>;
};

/ {
        keymap {
                compatible = "zmk,keymap";
"""

FOOTER = """\
        };
};
"""

# --- alignment helpers -------------------------------------------------------

def grid(rows, indent, split=None):
    """Align columns with tabulate. `split` inserts a gap column after N cols."""
    if split is not None:
        rows = [r[:split] + [""] + r[split:] for r in rows]
    table = tabulate(rows, tablefmt="plain", disable_numparse=True)
    return [indent + line for line in table.splitlines()]


def layer(name, left, right):
    lmain, rmain = left["main"], right["main"]
    if len(lmain) != len(rmain):
        raise ValueError(f"{name}: left main has {len(lmain)} rows, right has {len(rmain)}")
    for side, rows in (("left", lmain), ("right", rmain)):
        for i, row in enumerate(rows):
            if len(row) != HAND_COLS:
                raise ValueError(
                    f"{name}: {side} main row {i} has {len(row)} cells, expected {HAND_COLS}"
                )

    # Stitch each hand's main row halves back into a 12-key row; tabulate splits 6|6.
    merged = [l + r for l, r in zip(lmain, rmain)]
    body = grid(merged, indent=" " * 3, split=HAND_COLS)

    # Each half has its own dpad: emit left then right (matrix-transform order).
    dpad_rows = []
    for side in (left, right):
        dpad = side.get("dpad")
        if dpad is None:
            continue
        if len(dpad) != DPAD_COLS:
            raise ValueError(f"{name}: dpad has {len(dpad)} cells, expected {DPAD_COLS}")
        dpad_rows.append(dpad)
    if dpad_rows:
        body += grid(dpad_rows, indent=" " * 36)

    pad = " " * 16
    return [
        f"{pad}{name} {{",
        f"{pad}        bindings = <",
        *body,
        f"{pad}        >;",
        f"{pad}}};",
    ]


# --- behavior handle cheatsheet ----------------------------------------------
# Every stock ZMK behavior you can drop into a cell below, with its param count
# (#binding-cells). Full reference + key codes: ../KEYMAP.md.
#
#   keys     &kp KEY        send key while held          (1)
#            &kt KEY        toggle key on/off            (1)
#            &key_repeat    re-send last key             (0)
#            &caps_word     caps until non-word char     (0)
#            &gresc         grave / escape (mod-morph)   (0)
#   layers   &mo N          momentary layer N            (1)
#            &lt N KEY      hold=layer N, tap=KEY        (2)
#            &to N          switch to layer N            (1)
#            &tog N         toggle layer N               (1)
#            &sl N          sticky layer (next key)      (1)
#   mods     &mt MOD KEY    hold=MOD, tap=KEY            (2)
#            &sk KEY        sticky key (next key)        (1)
#   passthru &trans         fall through to layer below  (0)
#            &none          do nothing / block           (0)
#   pointer  &mkp MB1..MB5  mouse button                 (1)
#            &mmv MOVE_*    mouse move                   (1)
#            &msc SCRL_*    mouse scroll                 (1)
#   system   &bt BT_*       bluetooth (BT_SEL n etc.)    (2)
#            &out OUT_*     USB/BLE output select        (1)
#            &ext_power EP_* external power rail         (1)
#            &bl BL_*       backlight                    (2)
#            &rgb_ug RGB_*  rgb underglow                (2)
#            &soft_off      deep-sleep power down        (0)
#            &sys_reset     reboot controller            (0)
#            &bootloader    reboot to USB bootloader     (0)
#            &studio_unlock unlock ZMK Studio editing    (0)
# --- layer data (edit me) ----------------------------------------------------
# Each hand: main is 5 rows x 6 cells (number, top, home, bottom, thumb);
# dpad is the hand's 5-way cluster (Left, Down, Middle, Up, Right).

LAYERS = [
    layer(
        "qwerty",
        left={
            "main": [
                ["&kp GRAVE", "&kp N1",   "&kp N2", "&kp N3", "&kp N4",     "&kp N5"],
                ["&kp ESC",   "&kp Q",    "&kp W",  "&kp E",  "&kp R",      "&kp T"],
                ["&kp TAB",   "&kp A",    "&kp S",  "&kp D",  "&kp F",      "&kp G"],
                ["&kp LSHFT", "&kp Z",    "&kp X",  "&kp C",  "&kp V",      "&kp B"],
                ["&kp LCTRL", "&kp LGUI", "",       "",       "&kp SPACE",  "&mo 2"],
            ],
            "dpad": ["&kp C_PREV", "&kp C_VOL_DN", "&kp C_PP", "&kp C_VOL_UP", "&kp C_NEXT"],
        },
        right={
            "main": [
                ["&kp N6",   "&kp N7",     "&kp N8",    "&kp N9",  "&kp N0",   "&kp BSPC"],
                ["&kp Y",    "&kp U",      "&kp I",     "&kp O",   "&kp P",    "&kp BSPC"],
                ["&kp H",    "&kp J",      "&kp K",     "&kp L",   "&kp SEMI", "&kp SQT"],
                ["&kp N",    "&kp M",      "&kp COMMA", "&kp DOT", "&kp FSLH", "&kp ESC"],
                ["&mkp MB1", "&lt 4 RET",  "",          "",        "&kp LALT", "&studio_unlock"],
            ],
            "dpad": ["&kp LEFT", "&kp DOWN", "&kp K_MUTE", "&kp UP", "&kp RIGHT"],
        },
    ),
    layer(
        "lower_layer",
        left={
            "main": [
                ["&kp GRAVE", "&kp N1",   "&kp N2",    "&kp N3",    "&kp N4",     "&kp N5"],
                ["&kp TAB",   "&none",    "&kp BSLH",  "&kp UNDER", "&kp MINUS",  "&kp PIPE"],
                ["&kp LSHFT", "&none",    "&kp CARET", "&kp EQUAL", "&kp PLUS",   "&kp TILDE"],
                ["&kp LSHFT", "&none",    "&kp CARET", "&kp EQUAL", "&kp PLUS",   "&kp TILDE"],
                ["&kp LCTRL", "&kp LGUI", "",          "",          "&kp SPACE",  "&trans"],
            ],
            "dpad": ["&kp C_PREV", "&kp C_VOL_DN", "&kp C_PP", "&kp C_VOL_UP", "&kp C_NEXT"],
        },
        right={
            "main": [
                ["&kp N6",   "&kp N7",     "&kp N8", "&kp N9",    "&kp N0",   "&kp BSPC"],
                ["&kp LEFT", "&kp DOWN",   "&kp UP", "&kp RIGHT", "&none",    "&none"],
                ["&none",    "&none",      "&none",  "&none",     "&none",    "&none"],
                ["&none",    "&none",      "&none",  "&none",     "&none",    "&none"],
                ["&mo 5",    "&kp SPACE",  "",       "",          "&kp LALT", "&kp RGUI"],
            ],
            "dpad": ["&none", "&kp C_VOL_DN", "&kp C_PP", "&kp C_VOL_UP", "&kp C_NEXT"],
        },
    ),
    layer(
        "upper_layer",
        left={
            "main": [
                ["&kp GRAVE", "&kp EXCL",  "&kp AT",  "&kp HASH",  "&kp DLLR",  "&kp PRCNT"],
                ["&kp TAB",   "&none",     "&none",   "&kp LBRC",  "&kp RBRC",  "&kp GRAVE"],
                ["&kp LSHFT", "&none",     "&none",   "&kp LPAR",  "&kp RPAR",  "&none"],
                ["&kp LSHFT", "&none",     "&none",   "&kp LPAR",  "&kp RPAR",  "&none"],
                ["&kp LCTRL", "&kp LGUI",  "",        "",          "&kp SPACE", "&mo 5"],
            ],
            "dpad": ["&none", "&kp C_BRI_DN", "&none", "&kp C_BRI_UP", "&none"],
        },
        right={
            "main": [
                ["&kp CARET", "&kp AMPS",  "&kp ASTRK", "&kp LPAR", "&kp RPAR", "&kp DEL"],
                ["&none",     "&kp LBKT",  "&kp RBKT",  "&none",    "&none",    "&none"],
                ["&none",     "&kp LBRC",  "&kp RBRC",  "&none",    "&none",    "&none"],
                ["&none",     "&kp LBRC",  "&kp RBRC",  "&none",    "&none",    "&none"],
                ["&trans",    "&kp SPACE", "",          "",         "&kp LALT", "&kp RGUI"],
            ],
            "dpad": ["&none", "&kp C_BRI_DN", "&none", "&kp C_BRI_UP", "&none"],
        },
    ),
    layer(
        # Mouse layer: right hand = buttons (top), move (mid), scroll (bottom).
        "func_layer",
        left={
            "main": [
                ["&kp ESC",   "&kp F1",   "&kp F2",  "&kp F3", "&kp F4", "&kp F5"],
                ["&kp TAB",   "&kp F11",  "&kp F12", "&none",  "&none",  "&none"],
                ["&kp LSHFT", "&none",    "&none",   "&none",  "&none",  "&none"],
                ["&kp LSHFT", "&none",    "&none",   "&none",  "&none",  "&none"],
                ["&kp LCTRL", "&kp LGUI", "",        "",       "&none",  "&none"],
            ],
            "dpad": ["&none", "&none", "&none", "&none", "&none"],
        },
        right={
            "main": [
                ["&kp F6",         "&kp F7",         "&kp F8",       "&kp F9",          "&kp F10",  "&kp DEL"],
                ["&mkp MB4",       "&mkp MB1",       "&mkp MB3",     "&mkp MB2",        "&mkp MB5", "&none"],
                ["&mmv MOVE_LEFT", "&mmv MOVE_DOWN", "&mmv MOVE_UP", "&mmv MOVE_RIGHT", "&none",    "&none"],
                ["&msc SCRL_LEFT", "&msc SCRL_DOWN", "&msc SCRL_UP", "&msc SCRL_RIGHT", "&none",    "&none"],
                ["&none",          "&none",          "",             "",                "&kp LALT", "&kp RGUI"],
            ],
            "dpad": ["&none", "&none", "&none", "&none", "&none"],
        },
    ),
    layer(
        "config_layer",
        left={
            "main": [
                ["&none",             "&to 0",            "&to 1", "&none", "&none", "&none"],
                ["&none",             "&none",            "&none", "&none", "&none", "&none"],
                ["&none",             "&none",            "&none", "&none", "&none", "&none"],
                ["&none",             "&none",            "&none", "&none", "&none", "&none"],
                ["&ext_power EP_OFF", "&ext_power EP_ON", "",      "",      "&none", "&none"],
            ],
            "dpad": ["&none", "&none", "&none", "&none", "&none"],
        },
        right={
            "main": [
                ["&bt BT_SEL 0", "&bt BT_SEL 1", "&bt BT_SEL 2", "&bt BT_SEL 3", "&none",      "&none"],
                ["&none",        "&bt BT_PRV",   "&bt BT_NXT",   "&bt BT_DISC",  "&none",      "&none"],
                ["&none",        "&none",        "&none",        "&none",        "&none",      "&none"],
                ["&none",        "&none",        "&none",        "&none",        "&none",      "&none"],
                ["&none",        "&none",        "",             "",             "&bt BT_CLR", "&bt BT_CLR_ALL"],
            ],
            "dpad": ["&none", "&none", "&none", "&none", "&none"],
        },
    ),
]


def build():
    lines = [HEADER.rstrip("\n")]
    for lyr in LAYERS:
        lines.append("")
        lines.extend(lyr)
    lines.append(FOOTER.rstrip("\n"))
    return "\n".join(lines) + "\n"


def parse_args():
    p = argparse.ArgumentParser(description="Generate config/do52pro.keymap.")
    p.add_argument("--stdout", action="store_true",
                   help="print the keymap instead of writing the file")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--build", nargs="?", const="both", metavar="SIDE",
                   choices=["left", "right", "both"],
                   help="after writing, run `zmk.py build SIDE` (default both)")
    g.add_argument("--deploy", nargs="?", const="both", metavar="SIDE",
                   choices=["left", "right", "both"],
                   help="after writing, run `zmk.py deploy SIDE` (default both)")
    p.add_argument("--incremental", action="store_true",
                   help="pass --no-pristine to zmk.py for a fast rebuild")
    return p.parse_args()


def main():
    args = parse_args()
    text = build()

    if args.stdout:
        sys.stdout.write(text)
        return  # --stdout is a dry run; never build off unsaved output

    OUT.write_text(text)
    print(f"wrote {OUT}")

    action = "deploy" if args.deploy else "build" if args.build else None
    if action:
        side = args.deploy or args.build
        cmd = [sys.executable, str(ZMK_PY), action, side]
        if args.incremental:
            cmd.append("--no-pristine")
        print(f"$ {' '.join(cmd)}")
        raise SystemExit(subprocess.run(cmd).returncode)


if __name__ == "__main__":
    main()
