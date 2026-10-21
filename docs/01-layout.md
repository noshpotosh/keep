# 01 — Layout & matrix

## Grid
Each half is 5 columns × 4 rows on a uniform pitch `P`. The provisional value is **P = 16.5 mm** (see [requirements](00-requirements.md#open-tbds-resolve-before-routing)). There is no stagger anywhere.

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
The right half mirrors this, with the XIAO at the outer edge (columns 3–4).

**Outline per half** (keys only): 5P × 4P = 82.5 × 66 mm at 16.5 mm pitch. Add about 1.5 mm of case wall on each side, which gives roughly **86 × 69 mm** per half.

**The XIAO slot** is 2P × 1P = 33 × 16.5 mm. The XIAO measures 21 × 17.8 mm. It fits lengthwise, with about 1.3 mm of overhang into the case wall or the gap above it. The USB-C port faces the **outer side edge**. Check this in the KiCad 3D view.

## Matrix
- Each half uses a 5-col × 4-row diode matrix with 18 switches populated, so row 3 has 3 switches.
- That is **9 GPIO** (5 columns + 4 rows). The XIAO has 11 (D0–D10), which leaves **2 spare**.
- Diode direction is **col2row** (ZMK default): switch → diode anode, diode cathode → row.
- Use 1N4148W (SOD-123) diodes, placed on the **back** of the PCB. Keep them outside the battery pocket area, or use SOD-323 (thinner) if they sit over the pocket.

### Provisional GPIO map (left half; right mirrors the columns)
Finalize this during routing. Choose the pins that give the cleanest traces.

| Signal | XIAO pin |
|---|---|
| COL0–COL4 | D0, D1, D2, D3, D4 |
| ROW0–ROW3 | D5, D6, D7, D8 |
| Spare | D9, D10 |
| Battery sense | internal (P0.31 / P0.14, handled by the ZMK board definition) |

Do not use the NFC pins (P0.09 / P0.10) for the matrix unless NFC is disabled in config.

## Other components per half
- **Power switch:** a small SMD side-actuated slide switch (e.g. MSK-12C02 or similar) in series with BAT+. Without it, the battery drains during transport. Place it on the outer edge next to USB-C.
- **Reset button:** optional, since the XIAO has an onboard reset. Add a low-profile side or top tact switch if the XIAO will be enclosed.
- **Battery pads:** wire BAT+ / BAT− to the XIAO's back-side battery pads through the power switch.
