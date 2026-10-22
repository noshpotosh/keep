"""Parametric concept model of the 36-key PG1316S split.

Builds both halves from the numbers in docs/00-requirements.md and
docs/01-layout.md, then exports STEP (for CAD), GLB (for the web viewer)
and a JSON file of key positions and clearance checks.

Two case variants:
- tray (default, the locked design): an open tray with floating keys. The
  wall rises only to the PCB top surface. 17 mm pitch.
- enclosed (Designer-style concept): a top shell whose deck surrounds every
  key, on a flat bottom plate. The deck needs a printable web between key
  openings, so this variant uses an 18 mm pitch.

Both put the battery in a pocket through the floor, covered with Kapton,
and mount the XIAO face-down over a PCB cutout.

Run: uv run --python 3.12 --with build123d python cad/keyboard.py [tray|enclosed]
"""

import json
import sys
from pathlib import Path

from build123d import (
    Align, Axis, Box, Color, Compound, Cylinder, Plane, Pos,
    export_gltf, export_step, fillet,
)

OUT = Path(__file__).parent / "out"
MIN = (Align.CENTER, Align.CENTER, Align.MIN)
MAX = (Align.CENTER, Align.CENTER, Align.MAX)

CASE = sys.argv[1] if len(sys.argv) > 1 else "tray"
if CASE not in ("tray", "enclosed"):
    sys.exit("usage: keyboard.py [tray|enclosed]")

# --- Parameters (mm) -------------------------------------------------------
P = 17.0 if CASE == "tray" else 18.0   # 17: ~0.75 mm between caps; 18: room for deck webs
COLS, ROWS = 5, 4
CAP_W, CAP_D = 16.25, 16.05    # measured stock PG1316S cap
SW_W, SW_D, SW_H = 13.5, 13.0, 1.8
CAP_Z0, CAP_T = 1.93, 1.57     # cap underside / thickness above PCB top (Kailh STEP)
PCB_T = 0.8
FLOOR_T = 0.8
COVER_T = 0.1                  # Kapton over the through-floor battery pocket
BAT_L, BAT_W, BAT_T = 30.0, 20.0, 2.5   # placeholder 252030 pouch, model TBD
BAT_GAP = 0.1                  # battery top to PCB underside
WALL = 2.5
CLEAR = 0.2                    # PCB-to-wall clearance
LEDGE = 1.0                    # perimeter ledge the PCB rests on
CORNER_R = 6.0                 # plan-view corner radius of the body
TOP_EDGE_R = 1.6               # soft rounded top edge
DECK_PROUD = 0.7               # enclosed: how far cap tops stand above the deck
DECK_T = 0.8
KEY_GAP = 0.3                  # enclosed: cap-to-opening clearance per side
OPEN_R = 1.6                   # enclosed: opening corner radius
POST_R = 1.2                   # support posts under the 0.8 mm PCB
D_L, D_W, D_H = 2.5, 1.3, 0.9  # SOD-323 diode with leads
XIAO_L, XIAO_W, XIAO_T = 21.0, 17.8, 1.2
SHIELD_W, SHIELD_D, SHIELD_H = 10.5, 11.5, 1.6
USB_L, USB_W, USB_H = 7.4, 9.0, 3.2
USB_OUT = 1.5                  # USB-C overhang past the XIAO edge
USB_FLOOR = 0.2                # floor left under the USB-C pocket
PINHOLE_R = 0.75               # reset access, approximate button position
HALF_GAP = 60.0                # spacing between the halves in the render

BAT_Z = COVER_T                # battery underside
PCB_Z = BAT_Z + BAT_T + BAT_GAP   # PCB underside
TOP = PCB_Z + PCB_T            # PCB top surface = wall top
CAP_TOP = TOP + CAP_Z0 + CAP_T
DECK_TOP = CAP_TOP - DECK_PROUD
DECK_UNDER = DECK_TOP - DECK_T

# Key centres: row 0 at the top, row 3 is thumbs on columns 2-4.
KEYS = [(c, r) for r in range(3) for c in range(COLS)] + [(c, 3) for c in (2, 3, 4)]

X0, X1 = -P / 2, COLS * P - P / 2
Y1, Y0 = P / 2, -(ROWS - 1) * P - P / 2
BW, BH = X1 - X0, Y1 - Y0
BCX, BCY = (X0 + X1) / 2, (Y0 + Y1) / 2
OW, OH = BW + 2 * (CLEAR + WALL), BH + 2 * (CLEAR + WALL)

# The XIAO sits face-down on the PCB top in the empty outer slot of row 3.
# Its shield and USB-C hang down through a cutout; its battery pads face up.
# If it is wider than a row (17.8 mm vs 17), it is pushed toward the outer
# edge (overhanging the wall top) to keep clear of the row-2 caps.
XIAO_X0 = X0
XIAO_CX = XIAO_X0 + XIAO_L / 2
XIAO_CY = -3 * P - max(0.0, (XIAO_W - P) / 2)
CUT_L, CUT_W = XIAO_L - 1, 13.6   # PCB cutout, open to the outer edge
USB_Z = TOP - USB_H
RESET_XY = (XIAO_X0 + 3.5, XIAO_CY + 6.0)

BAT_CX, BAT_CY = 2.5 * P, -0.5 * P
BAT_X = (BAT_CX - BAT_L / 2, BAT_CX + BAT_L / 2)
BAT_Y = (BAT_CY - BAT_W / 2, BAT_CY + BAT_W / 2)


def key_xy(c, r):
    return c * P, -r * P


def over_battery(x, y, margin):
    return (BAT_X[0] - margin < x < BAT_X[1] + margin
            and BAT_Y[0] - margin < y < BAT_Y[1] + margin)


def diode_xy(c, r):
    """Diode below its switch, moved off the battery pocket where needed."""
    x, y = key_xy(c, r)
    dy = y + 7.6
    if over_battery(x, dy, D_W):
        dy = BAT_Y[0] - D_W - 0.5
    return x, dy


def colored(shape, label, rgb):
    shape.label = label
    shape.color = Color(*rgb)
    return shape


def body_blank(z0, h):
    b = Pos(BCX, BCY, z0) * Box(OW, OH, h, align=MIN)
    return fillet(b.edges().filter_by(Axis.Z), CORNER_R)


def rounded_cut(w, h, z0, depth, r):
    b = Pos(BCX, BCY, z0) * Box(w, h, depth, align=MIN)
    return fillet(b.edges().filter_by(Axis.Z), r)


def wall_openings(body):
    """USB-C opening and power switch slot in the outer wall."""
    body -= Pos(X0 - CLEAR - WALL - 1, XIAO_CY, USB_FLOOR) * Box(
        USB_L + CLEAR + WALL + 1.5, USB_W + 1.0, TOP, align=(Align.MIN, Align.CENTER, Align.MIN))
    body -= Pos(X0 - CLEAR - WALL - 1, -1.5 * P, PCB_Z - 1.6) * Box(6, 7.0, 1.8, align=MIN)
    return body


def floor_features(body, feet):
    """Battery pocket, USB-C pocket, reset pinhole, feet and support posts."""
    # Battery pocket through the floor, with a recess for the Kapton cover.
    body -= Pos(BAT_CX, BAT_CY, -1) * Box(BAT_L + 0.4, BAT_W + 0.4, PCB_Z + 1, align=MIN)
    body -= Pos(BAT_CX, BAT_CY, 0) * Box(BAT_L + 4, BAT_W + 4, COVER_T, align=MIN)
    # USB-C floor pocket under the hanging receptacle, plus the wall openings.
    body = wall_openings(body)
    # Reset pinhole under the XIAO's button.
    body -= Pos(*RESET_XY, -1) * Cylinder(PINHOLE_R, FLOOR_T + 2, align=MIN)
    # Feet in recessed pockets.
    for fx, fy in feet:
        body -= Pos(fx, fy, 0) * Cylinder(4, 0.4, align=MIN)
    # Support posts under each key, except over the battery.
    for c, r in KEYS:
        x, y = key_xy(c, r)
        if not over_battery(x, y, POST_R + 0.5):
            body += Pos(x, y, FLOOR_T - 0.01) * Cylinder(POST_R, PCB_Z - FLOOR_T + 0.01, align=MIN)
    return body


def build_half():
    parts = []

    feet = [(X0 + 8, Y1 - 8), (X1 - 8, Y1 - 8), (X0 + 18, Y0 + 6), (X1 - 8, Y0 + 8)]
    case_rgb = (0.86, 0.85, 0.82)
    inner_r = CORNER_R - WALL
    if CASE == "tray":
        # Tray: floor and walls in one piece, wall top flush with the PCB top.
        base = body_blank(0, TOP)
        base = fillet(base.edges().group_by(Axis.Z)[-1], TOP_EDGE_R)
        base = fillet(base.edges().group_by(Axis.Z)[0], 0.5)
        base -= rounded_cut(BW + 2 * CLEAR, BH + 2 * CLEAR, PCB_Z, TOP, inner_r)
        base -= rounded_cut(BW - 2 * LEDGE, BH - 2 * LEDGE, FLOOR_T, PCB_Z - FLOOR_T + 0.01,
                            max(inner_r - LEDGE, 0.5))
    else:
        # Bottom plate: flat floor plus a ledge ring the PCB rests on. The
        # seam with the shell sits low on the side, as on the Designer keyboard.
        base = body_blank(0, FLOOR_T)
        base = fillet(base.edges().group_by(Axis.Z)[0], 0.5)
        ring = rounded_cut(BW + 2 * CLEAR - 0.1, BH + 2 * CLEAR - 0.1, FLOOR_T - 0.01, PCB_Z - FLOOR_T + 0.01, inner_r)
        ring -= rounded_cut(BW - 2 * LEDGE, BH - 2 * LEDGE, FLOOR_T - 1, PCB_Z, max(inner_r - LEDGE, 0.5))
        base += ring
    base = floor_features(base, feet)
    parts.append(colored(base, CASE if CASE == "tray" else "plate", case_rgb))

    if CASE == "enclosed":
        # Top shell: walls plus a deck with one rounded opening per key. The
        # empty thumb slot is plain deck over the face-down XIAO.
        shell = body_blank(FLOOR_T, DECK_TOP - FLOOR_T)
        shell = fillet(shell.edges().group_by(Axis.Z)[-1], TOP_EDGE_R)
        shell -= rounded_cut(BW + 2 * CLEAR, BH + 2 * CLEAR, FLOOR_T - 1, DECK_UNDER - FLOOR_T + 1, inner_r)
        opening = Box(CAP_W + 2 * KEY_GAP, CAP_D + 2 * KEY_GAP, 10, align=MIN)
        opening = fillet(opening.edges().filter_by(Axis.Z), OPEN_R)
        for c, r in KEYS:
            x, y = key_xy(c, r)
            shell -= Pos(x, y, TOP) * opening
        shell = wall_openings(shell)
        parts.append(colored(shell, "shell", case_rgb))

    for fx, fy in feet:
        parts.append(colored(Pos(fx, fy, 0.05) * Cylinder(3.8, 0.4, align=MIN), "foot", (0.15, 0.15, 0.15)))
    parts.append(colored(Pos(BAT_CX, BAT_CY, 0) * Box(BAT_L + 3.6, BAT_W + 3.6, COVER_T, align=MIN),
                         "cover", (0.85, 0.55, 0.15)))

    # PCB with the cutout the XIAO's shield and USB-C hang through.
    pcb = Pos(BCX, BCY, PCB_Z) * Box(BW, BH, PCB_T, align=MIN)
    pcb -= Pos(X0 - 1, XIAO_CY, PCB_Z - 1) * Box(CUT_L + 1, CUT_W, 3, align=(Align.MIN, Align.CENTER, Align.MIN))
    parts.append(colored(pcb, "pcb", (0.08, 0.09, 0.10)))

    # XIAO nRF52840, face-down: board on top, shield and USB-C below.
    parts.append(colored(Pos(XIAO_CX, XIAO_CY, TOP) * Box(XIAO_L, XIAO_W, XIAO_T, align=MIN),
                         "xiao_pcb", (0.10, 0.32, 0.62)))
    parts.append(colored(Pos(XIAO_CX + 2.0, XIAO_CY, TOP) * Box(SHIELD_W, SHIELD_D, SHIELD_H, align=MAX),
                         "xiao_shield", (0.75, 0.76, 0.78)))
    usb = Pos(XIAO_X0 - USB_OUT, XIAO_CY, USB_Z) * Box(USB_L, USB_W, USB_H, align=(Align.MIN, Align.CENTER, Align.MIN))
    parts.append(colored(fillet(usb.edges().filter_by(Axis.X), 1.2), "usb_c", (0.70, 0.71, 0.73)))

    # Power switch on the PCB underside at the outer edge.
    parts.append(colored(Pos(X0 + 1.5, -1.5 * P, PCB_Z - 1.4) * Box(4.0, 6.7, 1.4, align=MIN),
                         "power_switch", (0.70, 0.71, 0.73)))

    bat = Pos(BAT_CX, BAT_CY, BAT_Z) * Box(BAT_L, BAT_W, BAT_T, align=MIN)
    parts.append(colored(fillet(bat.edges().filter_by(Axis.Z), 1.0), "battery", (0.78, 0.66, 0.30)))

    # Switches, diodes and caps.
    cap_proto = Box(CAP_W, CAP_D, CAP_T, align=MIN)
    cap_proto = fillet(cap_proto.edges().filter_by(Axis.Z), 1.2)
    cap_proto = fillet(cap_proto.edges().group_by(Axis.Z)[-1], 0.5)
    sw_proto = Box(SW_W, SW_D, SW_H - 0.2, align=MIN)
    d_proto = Box(D_L, D_W, D_H, align=MAX)
    for c, r in KEYS:
        x, y = key_xy(c, r)
        parts.append(colored(Pos(x, y, TOP) * sw_proto, "switch", (0.92, 0.92, 0.90)))
        parts.append(colored(Pos(*diode_xy(c, r), PCB_Z) * d_proto, "diode", (0.12, 0.12, 0.12)))
        parts.append(colored(Pos(x, y, TOP + CAP_Z0) * cap_proto, f"cap_{c}_{r}", (0.20, 0.21, 0.23)))
    return parts


def checks():
    """Clearances worth watching, printed after each build."""
    row2_cap_edge = -2 * P - CAP_D / 2
    xiao_top_edge = XIAO_CY + XIAO_W / 2
    diode_low = PCB_Z - D_H
    return {
        "total_height": CAP_TOP,
        "xiao_to_row2_cap": row2_cap_edge - xiao_top_edge,
        "xiao_top_below_cap_underside": TOP + CAP_Z0 - (TOP + XIAO_T),
        "usb_bottom_above_desk": USB_Z,
        "usb_centre_above_desk": USB_Z + USB_H / 2,
        "diode_to_floor": diode_low - FLOOR_T,
        "cavity_under_pcb": PCB_Z - FLOOR_T,
    } | ({
        "deck_web_x": P - CAP_W - 2 * KEY_GAP,
        "deck_web_y": P - CAP_D - 2 * KEY_GAP,
        "xiao_top_below_deck": DECK_UNDER - (TOP + XIAO_T),
    } if CASE == "enclosed" else {})


def main():
    OUT.mkdir(exist_ok=True)
    stem = "keyboard" if CASE == "tray" else "keyboard-enclosed"
    left = build_half()
    dx = X1 + CLEAR + WALL + HALF_GAP / 2
    right = []
    for part in left:
        m = part.mirror(Plane.YZ)
        m.label, m.color = part.label, part.color
        right.append(m)
    left_c = Pos(-dx, 0, 0) * Compound(children=left, label="left")
    right_c = Pos(dx, 0, 0) * Compound(children=right, label="right")
    kb = Compound(children=[left_c, right_c], label="keyboard")

    export_step(kb, OUT / f"{stem}.step")
    export_gltf(kb, str(OUT / f"{stem}.glb"), binary=True,
                linear_deflection=0.02, angular_deflection=0.2)

    keys = []
    for side, sx in (("left", 1), ("right", -1)):
        for c, r in KEYS:
            x, y = key_xy(c, r)
            keys.append({"side": side, "col": c, "row": r,
                         "x": (x - dx) if sx == 1 else (dx - x), "y": y})
    chk = checks()
    layout = {"case": CASE, "pitch": P, "cap": [CAP_W, CAP_D], "total_height": CAP_TOP,
              "half_size": [OW, OH], "cap_gap": [P - CAP_W, P - CAP_D],
              "checks": chk, "keys": keys}
    (OUT / f"{stem}.json").write_text(json.dumps(layout, indent=1))
    print("%s: half %.1f x %.1f mm, pitch %.1f mm" % (CASE, OW, OH, P))
    for k, v in chk.items():
        print("%-30s %6.2f mm" % (k, v))


if __name__ == "__main__":
    main()
