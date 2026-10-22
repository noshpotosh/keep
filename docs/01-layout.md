# 01 — Layout & matrix

## Grid
Each half is 5 columns × 4 rows on a uniform pitch `P`. The pitch is **P = 17 mm** (see [requirements](00-requirements.md#locked-decisions)). There is no stagger anywhere.

```
 Left half                         col:  0   1   2   3   4
                                       ┌───┬───┬───┬───┬───┐
 row 0                                 │ x │ x │ x │ x │ x │
                                       ├───┼───┼───┼───┼───┤
 row 1                                 │ x │ x │ x │ x │ x │
                                       ├───┼───┼───┼───┼───┤
 row 2                                 │ x │ x │ x │ x │ x │
                                       ├───┴───┼───┼───┼───┤
 row 3 (thumbs)                        │ XIAO  │ x │ x │ x │
                                       └───────┴───┴───┴───┘
```
The right half is the **same reversible PCB, flipped over**. That puts the XIAO at the outer edge (columns 3–4) automatically.

**Outline per half** (keys only): 5P × 4P = 85 × 68 mm at 17 mm pitch. Add 0.2 mm clearance and a 2.5 mm case wall on each side, which gives **90.4 × 73.4 mm** per half.

**The XIAO slot** is 2P × 1P = 34 × 17 mm. The XIAO measures 21 × 17.8 mm, so it fits lengthwise with about 0.4 mm of overhang above and below. It mounts **face-down** on top of the PCB, with its components and USB-C hanging down through a cutout (see [requirements](00-requirements.md#height-budget-target--7-mm)). The USB-C port faces the **outer side edge**. Check this in the KiCad 3D view.

## Matrix
- Each half uses a 5-col × 4-row diode matrix with 18 switches populated, so row 3 has 3 switches.
- That is **9 GPIO** (5 columns + 4 rows). The XIAO has 11 (D0–D10), which leaves **2 spare**.
- Diode direction is **col2row** (ZMK default): switch → diode anode, diode cathode → row.
- Use 1N4148WS (SOD-323) diodes, placed on the side opposite the switches. Keep them outside the battery pocket area.
- The board is reversible, so each diode footprint has pads on both sides. Flipping the board keeps the rows and columns physically the same, so both halves stay col2row.

### Provisional GPIO map (left half; right mirrors the columns)
Finalize this during routing. Choose the pins that give the cleanest traces. On the reversible board the XIAO's pins mirror on the right half. The GPIO swaps are handled in that half's firmware overlay. The power pins (5V, GND, 3V3) need solder jumpers.

| Signal | XIAO pin |
|---|---|
| COL0–COL4 | D0, D1, D2, D3, D4 |
| ROW0–ROW3 | D5, D6, D7, D8 |
| Spare | D9, D10 |
| Battery sense | internal (P0.31 / P0.14, handled by the ZMK board definition) |

Do not use the NFC pins (P0.09 / P0.10) for the matrix unless NFC is disabled in config.

## Other components per half
- **Power switch:** a small SMD side-actuated slide switch (e.g. MSK-12C02 or similar) in series with BAT+. Without it, the battery drains during transport. Place it on the outer edge next to USB-C.
- **Reset:** there's no extra switch. The face-down XIAO's onboard reset button faces the case floor, so you reach it through a pinhole in the floor. For normal use, put `&bootloader` / `&sys_reset` on a keymap layer.
- **Battery pads:** wire BAT+ / BAT− to the XIAO's battery pads through the power switch. With the XIAO face-down, its battery pads face up and are easy to reach.
