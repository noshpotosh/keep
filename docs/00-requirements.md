# 00 — Requirements & decisions

## Goals
1. **Thin and portable.** Total height ≤ 7 mm including keycaps and case. The closest prior art, [vuoz/chalk](https://github.com/vuoz/chalk), reaches about 6 mm.
2. **Pure ortholinear.** No row stagger and no column stagger. Each half is a clean rectangle.
3. **Wireless split** with long standby and a rechargeable battery.
4. **36 keys.** 3×5 alphas plus 3 thumbs per half.

## Locked decisions

| Area | Decision | Why |
|---|---|---|
| Switch | Kailh PG1316S | Lowest-profile keyboard switch available (1.8 mm) |
| Controller | Seeed XIAO nRF52840 | Small (21 × 17.8 mm), cheap, has a built-in LiPo charger, ZMK-supported, proven with PG1316S in chalk |
| Firmware | ZMK | Standard for wireless splits |
| Thumbs | 4th row, inner 3 columns | Keeps the grid ortholinear. The 2 empty outer slots house the XIAO |
| Case | 3D printed | Cheap and quick to iterate |
| PCB thickness | 1.0 mm (0.8 mm stretch) | Thinner than the standard 1.6 mm. Chalk proved 1.0 mm works |

## PG1316S switch facts
From the Kailh datasheet [CPG1316S01D02](https://docs.holykeebs.com/datasheets/CPG1316S01D02.pdf):

| Spec | Value |
|---|---|
| Body | 13.50 × 13.00 mm |
| Height | 1.80 ± 0.2 mm free (1.60 mm frame) |
| Total travel | 1.8 ± 0.2 mm |
| Contact travel | 1.0 ± 0.3 mm |
| Operating force | 25 ± 10 gf |
| Tactile peak | 35 ± 10 gf |
| Land pattern extents | 14.70 × 14.00 mm |
| Pads | 4× 2 × 2 mm mechanical, 2× 2 × 1.55 mm contacts (the two contacts sit 5.80 mm apart, centre to centre) |
| Locating holes | Ø1.20 mm and Ø1.00 mm (NPTH) |
| LED window | Optional, centre of switch |
| Hand solder | 280 °C max, 3 s max |
| Life | 20 M cycles |

The switch is **SMD**. Once soldered it is very hard to remove, so buy spares (at least 10 to 15% extra).

## Battery

**Your request:** a thin, watch-style rechargeable cell.

The options:

| Option | Thickness | Capacity | Notes |
|---|---|---|---|
| LIR2032 coin cell | 3.2 mm | about 40 mAh | Rechargeable, but its max charge current is about 20 mA. The XIAO charges at **≥ 50 mA**, so this would over-stress the cell. Not recommended |
| LIR2450 coin cell | 5.0 mm | about 120 mAh | Too thick for the target |
| **Thin LiPo pouch (smartwatch style)** | **2–3 mm** | **100–300 mAh** | **Recommended.** Examples: 301230 (3.0 × 12 × 30 mm, about 100 mAh), 302030 (about 150 mAh), 402030 (4 mm, about 200 mAh) |

The pouch code reads thickness/width/length, so `301230` = 3.0 mm × 12 mm × 30 mm. Choose a cell **with a protection PCB** and bare leads or a JST-SH connector. The XIAO charges at 50 mA by default (P0.13 high-Z) or 100 mA (P0.13 driven LOW). Keep the default 50 mA for cells under 100 mAh.

**Expected life** (ZMK, rough estimate): the central half of a split draws the most, about 0.3–1 mA average while in use. A 150 mAh cell gives roughly 2–6 weeks on the central and months on the peripheral. Sleep settings matter more than capacity.

## Height budget (target ≤ 7 mm)

| Layer | Thickness |
|---|---|
| Case floor | 0.8–1.0 mm |
| Battery pocket (under PCB), or diode clearance | 2.0–2.5 mm |
| PCB | 1.0 mm |
| Switch | 1.8 mm |
| Keycap | about 1.0–1.5 mm |
| **Total** | **about 6.6–7.8 mm** |

The XIAO sits on top of the PCB in the empty outer corner of row 4. Its height (board plus USB-C) must be measured and compared with the switch-plus-keycap height. If it is taller, use a PCB cutout so the XIAO sits lower.

## Open TBDs (resolve before routing)
- [ ] **Key pitch.** Provisional value 16.5 mm × 16.5 mm. The minimum is 14.7 mm, set by the land pattern. Confirm against the Kailh PG1316S 1U keycap datasheet; chalk used about 16 × 16 mm caps.
- [ ] **Battery model.** Choose a specific pouch cell and record its exact L × W × T.
- [ ] **XIAO mounting height.** Surface-mount on castellations vs. PCB cutout, and measure the real part.
- [ ] **Keycaps.** Stock Kailh PG1316S caps vs. custom 3D-printed caps (thinner, possible).
- [ ] **Solder method.** Pads only (hot plate plus paste) vs. through-hole vias under the pads (solder from the back with an iron, as on the Holykeebs practice board and chalk).
- [ ] **PCB strategy.** One reversible PCB vs. separate left and right PCBs.
