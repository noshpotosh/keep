# 00 — Requirements & decisions

## Goals
1. **Thin and portable.** Total height ≤ 7 mm including keycaps and case. The closest prior art, [vuoz/chalk](https://github.com/vuoz/chalk), reaches about 6 mm.
2. **Pure ortholinear.** No row stagger and no column stagger. Each half is a clean rectangle.
3. **Wireless split** with long standby and a rechargeable battery.
4. **36 keys.** 3×5 alphas plus 3 thumbs per half.
5. **Clean, Designer-inspired look.** Each half is a slim, flat slab with soft rounded edges and the body and caps in one matching colour, like a [Microsoft Designer Compact Keyboard](https://www.amazon.com/dp/B08J8BLRZF) cut into two ortholinear pieces. The keys **float** in an open tray. The top deck around each key was dropped (2026-10-22): at 17 mm pitch the web between key openings would be about 0.15 mm, which can't be printed.

## Locked decisions

| Area | Decision | Why |
|---|---|---|
| Switch | Kailh PG1316S | Lowest-profile keyboard switch available (1.8 mm) |
| Controller | Seeed XIAO nRF52840 | Small (21 × 17.8 mm), cheap, has a built-in LiPo charger, ZMK-supported, proven with PG1316S in chalk |
| Firmware | ZMK | Standard for wireless splits |
| Thumbs | 4th row, inner 3 columns | Keeps the grid ortholinear. The 2 empty outer slots house the XIAO |
| Case | 3D-printed open tray, floating keys | Cheap and quick to iterate, and the thinnest option. A top deck doesn't fit at 17 mm pitch |
| PCB thickness | 0.8 mm | Needed to reach ≤ 7 mm. The tray needs extra support posts, because the board flexes more than 1.0 mm (which chalk used) |
| Key pitch | 17.0 × 17.0 mm | Leaves about 0.75 mm between the 16.25 × 16.05 mm caps, which tolerates hand-solder misalignment |
| Keycaps | Stock Kailh PG1316S 1U caps (Holykeebs) | Off the shelf. Measured outer size 16.25 × 16.05 mm |
| PCB strategy | One reversible PCB for both halves | One design and one order of 5. Every footprint needs pads on both sides |
| Solder method | Plated vias in the switch pads, soldered from the back with an iron | No hot plate or stencil needed, and rework is easier |
| Switch frame pads (pad 3) | No net, mechanical only | They don't sink heat into the GND pour, so hand soldering is easier |
| Matrix | 5 × 4 diode matrix, col2row, SOD-323 diodes | The standard XIAO has only 11 GPIO, so going diodeless would need the XIAO Plus mounted face-up |
| XIAO mounting | Face-down over a PCB cutout | Only the XIAO board (about 1.2 mm) stands above the PCB, well below the cap tops |
| Reset | Pinhole in the case floor, plus `&bootloader` / `&sys_reset` in the keymap | The face-down XIAO's reset button faces the floor. No extra parts |
| Screen | None | It keeps all 11 GPIO free for the matrix and keeps the battery small |
| Battery | 2.5 mm pouch, about 100 mAh (252030 class), hidden under the PCB | Meets the ≤ 7 mm target together with the 0.8 mm PCB. Plenty of capacity without a screen |

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

**Decision:** a thin LiPo pouch, **2.5 mm thick, about 100 mAh** (252030 class, 2.5 × 20 × 30 mm). It is hidden in a pocket under the PCB and is not a visible design feature.

The pouch code reads thickness/width/length, so `252030` = 2.5 mm × 20 mm × 30 mm. Choose a cell **with a protection PCB** and bare leads. The XIAO charges at 50 mA by default (P0.13 high-Z) or 100 mA (P0.13 driven LOW). Keep the default 50 mA (0.5 C for a 100 mAh cell).

Rejected options:
- **LIR2032 coin cell** (3.2 mm, about 40 mAh). Its max charge current is about 20 mA, below the XIAO's 50 mA.
- **LIR2450 coin cell** (5.0 mm). Too thick.
- **3.0 mm pouch, about 150 mAh** (302030). About 50% more runtime, but it brings the total to about 7.3 mm.

**Expected life** (ZMK, rough estimate): the central half of a split draws the most. A 100 mAh cell gives roughly 1–3 weeks on the central and months on the peripheral. Sleep settings matter more than capacity. There is no screen, which keeps the draw low.

## Height budget (target ≤ 7 mm)

Measured at the tallest point, over the battery:

| Layer | Thickness |
|---|---|
| Kapton or sticker covering the through-floor battery pocket | about 0.1 mm |
| Battery (2.5 mm) plus 0.1 mm clearance | 2.6 mm |
| PCB | 0.8 mm |
| Switch plus keycap (cap top above PCB, from the Kailh STEP) | 3.5 mm |
| **Total** | **about 7.0 mm** |

This has no margin. The Kailh STEP's cap geometry is known to be off, so measure a real Holykeebs cap on a switch. If it's thinner, the budget gains slack.

Away from the battery, the case floor is 0.8 mm. The cavity under the PCB (about 1.9 mm) holds the SOD-323 diodes.

The XIAO is mounted **face-down** over a PCB cutout. Its PCB (about 1.2 mm) sits on top of the main PCB, well below the cap tops. Its components and USB-C (about 3.2 mm tall) hang down through the cutout, ending about 2.4 mm below the PCB underside. That is deeper than the 1.9 mm cavity, so the floor likely needs a pocket under the USB-C. Confirm by measuring the real part.

## Resolved TBDs
All of the earlier open TBDs are decided (see [Locked decisions](#locked-decisions)): key pitch, battery class, XIAO mounting, keycaps, solder method, and PCB strategy.

## Remaining checks (don't block layout; do before ordering)
- [ ] **Battery part.** Pick a specific 2.5 mm pouch cell with protection and record its exact L × W × T. Use a 20 × 30 mm placeholder pocket until then. The gap is only 0.1 mm, so the cell's real thickness matters.
- [ ] **XIAO measurements.** Measure how far the components and USB-C hang below the XIAO PCB. This sets the cutout size and whether the floor needs a pocket under the USB-C.
- [ ] **USB-C cable clearance.** With the XIAO face-down, the USB-C centre sits only about 1.9 mm above the desk. A standard plug overmold (about 6–7 mm tall) would hit the desk, so charging means lifting the edge, or using a slim or right-angle cable. Test with real cables before committing. If none fit, the fix is to mount the XIAO face-up (USB-C centre about 6.3 mm up, but the XIAO then stands about 0.9 mm above the cap tops).
- [ ] **Keycap height.** Measure the Holykeebs cap to confirm the height budget.
- [ ] **Switch footprint.** Validate the pads against the datasheet, then add vias in the pads and set it up for a reversible board.
- [ ] **Reversible XIAO footprint.** Flipping the board mirrors the XIAO's pin order, which swaps the power pins (5V, GND, 3V3) onto GPIO pads. Use solder jumpers to fix this.
