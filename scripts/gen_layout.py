#!/usr/bin/env python3
"""Insert a `keys = <...>` block into each board's zmk,physical-layout node so
ZMK Studio has key positions to render.

ZMK Studio refuses to build a physical layout that has no key positions. These
coordinates are APPROXIMATE (centi-keyunits, 1u = 100), not the true board
geometry: a flat ortho split with a 1.5u gap between halves, thumbs on row 4,
and each 5-way DPAD drawn as a `+` cross. They're emitted in matrix-transform
order so Studio maps them to the right keys.

Re-run after changing a board's matrix transform. Idempotent-ish: it refuses to
patch a file that already contains a keys block (remove it first to regenerate).

    ./scripts/gen_layout.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GAP = 150  # added to right-half x (cols >= 6)


def xy_main(col, row):
    return col * 100 + (GAP if col >= 6 else 0), row * 100


def dpad(bx, by):  # transform order: Left, Down, Middle, Up, Right
    return [(bx, by + 100), (bx + 100, by + 200), (bx + 100, by + 100),
            (bx + 100, by), (bx + 200, by + 100)]


def points(dpads):
    pts = [xy_main(c, r) for r in range(4) for c in range(12)]   # 4x12 main
    pts += [xy_main(c, 4) for c in (0, 1, 4, 5, 6, 7, 10, 11)]   # thumb row 4
    for bx, by in dpads:                                         # dpad cluster(s)
        pts += dpad(bx, by)
    return pts


def keys_block(pts):
    out = ["        /* auto-generated approximate layout for ZMK Studio "
           f"({len(pts)} keys, matrix-transform order) — see scripts/gen_layout.py */",
           "        keys"]
    for i, (x, y) in enumerate(pts):
        lead = "            = " if i == 0 else "            , "
        out.append(f"{lead}<&key_physical_attrs 100 100 {x:>4} {y:>4} 0 0 0>")
    out.append("            ;")
    return "\n".join(out)


def patch(rel, dpads):
    path = REPO / rel
    text = path.read_text()
    anchor = "        kscan = <&kscan0>;\n"
    if anchor not in text:
        raise SystemExit(f"anchor not found in {rel}")
    if "key_physical_attrs" in text:
        raise SystemExit(f"{rel} already has a keys block; remove it to regenerate")
    block = keys_block(points(dpads))
    path.write_text(text.replace(anchor, anchor + "\n" + block + "\n"))
    print(f"patched {rel}: {len(points(dpads))} keys")


if __name__ == "__main__":
    # do52: one DPAD (right). do52pro: two DPADs (left + right).
    patch("boards/shields/do52/do52.dtsi", [(900, 520)])
    patch("boards/shields/do52pro/do52pro.dtsi", [(150, 520), (900, 520)])
