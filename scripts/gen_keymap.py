#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = ["tabulate"]
# ///
"""Generate config/do52pro.keymap from layer data with auto-aligned columns.

The whole point: you edit the LAYERS data below as plain lists of bindings and
`tabulate` pads every column so the file stays readable. No more lining up
`&kp` tokens by hand.

Each layer has:
  * main  : 4 rows x 12 keys  -> aligned 12-col grid, split 6|6 in the middle
  * thumb : 1 row of 12 cells -> "" means an empty thumb position (kept blank
            so the keys line up under the main grid)
  * dpad  : 0+ rows x 5 keys  -> aligned 5-col grid

Usage (uv auto-installs tabulate from the inline metadata above):
    uv run scripts/gen_keymap.py            # write config/do52pro.keymap
    uv run scripts/gen_keymap.py --stdout   # print instead of writing
"""
import sys
from pathlib import Path

from tabulate import tabulate

OUT = Path(__file__).resolve().parent.parent / "config" / "do52pro.keymap"

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


def layer(name, main, thumb, dpad=()):
    body = []
    # align the thumb row together with the 4 main rows so columns line up
    body += grid([*main, thumb], indent=" " * 3, split=6)
    if dpad:
        body += grid(dpad, indent=" " * 36)
    pad = " " * 16
    return [
        f"{pad}{name} {{",
        f"{pad}        bindings = <",
        *body,
        f"{pad}        >;",
        f"{pad}}};",
    ]


# --- layer data (edit me) ----------------------------------------------------

LAYERS = [
    layer(
        "qwerty",
        main=[
            ["&kp GRAVE", "&kp N1", "&kp N2", "&kp N3", "&kp N4", "&kp N5",
             "&kp N6", "&kp N7", "&kp N8", "&kp N9", "&kp N0", "&kp BSPC"],
            ["&kp ESC", "&kp Q", "&kp W", "&kp E", "&kp R", "&kp T",
             "&kp Y", "&kp U", "&kp I", "&kp O", "&kp P", "&kp BSPC"],
            ["&kp TAB", "&kp A", "&kp S", "&kp D", "&kp F", "&kp G",
             "&kp H", "&kp J", "&kp K", "&kp L", "&kp SEMI", "&kp SQT"],
            ["&kp LSHFT", "&kp Z", "&kp X", "&kp C", "&kp V", "&kp B",
             "&kp N", "&kp M", "&kp COMMA", "&kp DOT", "&kp FSLH", "&kp ESC"],
        ],
        thumb=["&kp LCTRL", "&kp LGUI", "", "", "&kp SPACE", "&mo 2",
               "&mo 3", "&lt 4 RET", "", "", "&kp LALT", "&studio_unlock"],
        dpad=[
            ["&kp C_PREV", "&kp C_VOL_DN", "&kp C_PP", "&kp C_VOL_UP", "&kp C_NEXT"],
            ["&kp LEFT", "&kp DOWN", "&kp K_MUTE", "&kp UP", "&kp RIGHT"],
        ],
    ),
    layer(
        "lower_layer",
        main=[
            ["&kp GRAVE", "&kp N1", "&kp N2", "&kp N3", "&kp N4", "&kp N5",
             "&kp N6", "&kp N7", "&kp N8", "&kp N9", "&kp N0", "&kp BSPC"],
            ["&kp TAB", "&none", "&kp BSLH", "&kp UNDER", "&kp MINUS", "&kp PIPE",
             "&kp LEFT", "&kp DOWN", "&kp UP", "&kp RIGHT", "&none", "&none"],
            ["&kp LSHFT", "&none", "&kp CARET", "&kp EQUAL", "&kp PLUS", "&kp TILDE",
             "&none", "&none", "&none", "&none", "&none", "&none"],
            ["&kp LSHFT", "&none", "&kp CARET", "&kp EQUAL", "&kp PLUS", "&kp TILDE",
             "&none", "&none", "&none", "&none", "&none", "&none"],
        ],
        thumb=["&kp LCTRL", "&kp LGUI", "", "", "&kp SPACE", "&trans",
               "&mo 5", "&kp SPACE", "", "", "&kp LALT", "&kp RGUI"],
        dpad=[
            ["&kp C_PREV", "&kp C_VOL_DN", "&kp C_PP", "&kp C_VOL_UP", "&kp C_NEXT"],
            ["&none", "&kp C_VOL_DN", "&kp C_PP", "&kp C_VOL_UP", "&kp C_NEXT"],
        ],
    ),
    layer(
        "upper_layer",
        main=[
            ["&kp GRAVE", "&kp EXCL", "&kp AT", "&kp HASH", "&kp DLLR", "&kp PRCNT",
             "&kp CARET", "&kp AMPS", "&kp ASTRK", "&kp LPAR", "&kp RPAR", "&kp DEL"],
            ["&kp TAB", "&none", "&none", "&kp LBRC", "&kp RBRC", "&kp GRAVE",
             "&none", "&kp LBKT", "&kp RBKT", "&none", "&none", "&none"],
            ["&kp LSHFT", "&none", "&none", "&kp LPAR", "&kp RPAR", "&none",
             "&none", "&kp LBRC", "&kp RBRC", "&none", "&none", "&none"],
            ["&kp LSHFT", "&none", "&none", "&kp LPAR", "&kp RPAR", "&none",
             "&none", "&kp LBRC", "&kp RBRC", "&none", "&none", "&none"],
        ],
        thumb=["&kp LCTRL", "&kp LGUI", "", "", "&kp SPACE", "&mo 5",
               "&trans", "&kp SPACE", "", "", "&kp LALT", "&kp RGUI"],
        dpad=[
            ["&none", "&kp C_BRI_DN", "&none", "&kp C_BRI_UP", "&none"],
            ["&none", "&kp C_BRI_DN", "&none", "&kp C_BRI_UP", "&none"],
        ],
    ),
    layer(
        # Mouse layer: right hand = buttons (top), move (mid), scroll (bottom).
        "func_layer",
        main=[
            ["&kp ESC", "&kp F1", "&kp F2", "&kp F3", "&kp F4", "&kp F5",
             "&kp F6", "&kp F7", "&kp F8", "&kp F9", "&kp F10", "&kp DEL"],
            ["&kp TAB", "&kp F11", "&kp F12", "&none", "&none", "&none",
             "&mkp MB4", "&mkp MB1", "&mkp MB3", "&mkp MB2", "&mkp MB5", "&none"],
            ["&kp LSHFT", "&none", "&none", "&none", "&none", "&none",
             "&mmv MOVE_LEFT", "&mmv MOVE_DOWN", "&mmv MOVE_UP", "&mmv MOVE_RIGHT", "&none", "&none"],
            ["&kp LSHFT", "&none", "&none", "&none", "&none", "&none",
             "&msc SCRL_LEFT", "&msc SCRL_DOWN", "&msc SCRL_UP", "&msc SCRL_RIGHT", "&none", "&none"],
        ],
        thumb=["&kp LCTRL", "&kp LGUI", "", "", "&none", "&none",
               "&none", "&none", "", "", "&kp LALT", "&kp RGUI"],
        dpad=[["&none", "&none", "&none", "&none", "&none"]],
    ),
    layer(
        "config_layer",
        main=[
            ["&none", "&to 0", "&to 1", "&none", "&none", "&none",
             "&bt BT_SEL 0", "&bt BT_SEL 1", "&bt BT_SEL 2", "&bt BT_SEL 3", "&none", "&none"],
            ["&none", "&none", "&none", "&none", "&none", "&none",
             "&none", "&bt BT_PRV", "&bt BT_NXT", "&bt BT_DISC", "&none", "&none"],
            ["&none", "&none", "&none", "&none", "&none", "&none",
             "&none", "&none", "&none", "&none", "&none", "&none"],
            ["&none", "&none", "&none", "&none", "&none", "&none",
             "&none", "&none", "&none", "&none", "&none", "&none"],
        ],
        thumb=["&ext_power EP_OFF", "&ext_power EP_ON", "", "", "&none", "&none",
               "&none", "&none", "", "", "&bt BT_CLR", "&bt BT_CLR_ALL"],
        dpad=[["&none", "&none", "&none", "&none", "&none"]],
    ),
]


def build():
    lines = [HEADER.rstrip("\n")]
    for lyr in LAYERS:
        lines.append("")
        lines.extend(lyr)
    lines.append(FOOTER.rstrip("\n"))
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    text = build()
    if "--stdout" in sys.argv:
        sys.stdout.write(text)
    else:
        OUT.write_text(text)
        print(f"wrote {OUT}")
