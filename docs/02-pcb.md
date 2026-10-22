# 02 — PCB design (Ergogen → KiCad → fab)

Workflow: **Ergogen** generates the key grid, outlines, and a placed (unrouted) KiCad board from YAML. **KiCad** handles routing, DRC, and export. The fab is **JLCPCB** (or PCBWay).

## 1. Tooling setup
- Install [KiCad 9](https://www.kicad.org/download/) (8 works too). The footprint libraries below target KiCad 8+.
- Install Node.js LTS and the Ergogen CLI: `npm i -g ergogen`, version 4.1+. The web UI at [ergogen.cache.works](https://ergogen.cache.works) is good for quick previews.
- Optional: set up the KiCad MCP server and `kicad-cli` (see [resources](resources.md#mcp--ai-tooling)).

## 2. Footprints
| Part | Source | Notes |
|---|---|---|
| PG1316S switch | [Collected KiCad footprints](../assets/pg1316s/README.md) | Start with the spec-sheet footprint; reversible variant is experimental. Compare pad geometry with the datasheet and physical switch. Convert selected footprint to Ergogen (JS). |
| Diode SOD-323 | [ceoloide/ergogen-footprints](https://github.com/ceoloide/ergogen-footprints) diode footprint | Must be reversible (pads on both sides) |
| XIAO nRF52840 | Write a custom footprint, or adapt one from community repos | Mounted **face-down** on top, with a cutout for the shield and USB-C (about 20 × 13.6 mm, open to the outer edge; size it from the measured part). The 14 castellated pads stay outside the cutout. Reversible, with solder jumpers for the mirrored power pins. The BAT pads face up, so wire them by hand |
| Power switch | ceoloide `power_switch_smd_side.js` | Reversible placement |
| Battery | ceoloide `battery_connector_jst_ph_2.js`, or bare solder pads | Bare pads are thinner |

**Switch footprint requirements (decided):**
- **Vias in the pads.** Put plated through-holes inside each PG1316S pad, including the pad 3s, as on the Holykeebs practice board and in chalk. You then solder each switch from the far side with an iron.
- **Reversible.** Pads go on both sides, tied together by the vias.
- **Pad 3s have no net.** They are mechanical only.

## 3. Ergogen config (`ergogen/config.yaml`)
Sections to write:
- `units`: `kx: 17`, `ky: 17` (the pitch from requirements).
- `points.zones.matrix`: 5 columns × 3 rows, no `stagger`, no `splay`.
- `points.zones.thumbs`: 3 keys on row 3, aligned to columns 2–4 of the left half. This is still pure grid; just anchor the zone so the keys line up.
- `outlines`:
  - `board`: the rectangle around all key positions plus the XIAO slot.
  - `case_inner` / `case_outer`: offsets for the case CAD.
  - `battery_pocket`: on the side opposite the switches. Use a 20 × 30 mm placeholder until the cell is chosen.
  - `xiao_cutout`: the opening under the face-down XIAO.
- `pcbs.board`: one reversible board, `template: kicad8`. Place the switches, diodes, XIAO, power switch, and battery pads, and name the nets by matrix row and column.
- Output: `ergogen ergogen/ -o output/`. This produces `output/pcbs/board.kicad_pcb` and `output/outlines/*.dxf`.

## 4. Route in KiCad
1. Open the generated `.kicad_pcb`. Set the board setup to **0.8 mm** thickness, 2 layers, and 1 oz copper.
2. Import the JLCPCB design rules. Use 0.2 mm traces (0.25 mm for power) and 0.3/0.6 mm vias.
3. Route the columns on F.Cu and the rows on B.Cu where possible. You route once, because both halves use this board. Keep traces clear of the pads used on the opposite side.
4. Add a **GND pour** on both layers. **Keep copper out of the area under and around the XIAO antenna** (the end opposite USB-C).
5. Add mounting features for the case: M2 holes, or keep-outs for magnets or snap-fits. Make them symmetric so the flipped board fits the mirrored tray. Leave room for support posts, because a 0.8 mm board flexes.
6. Run **DRC** and fix everything. Check the 3D viewer for collisions between the XIAO, the switches, and the board edge.

## 5. Order
1. Plot the Gerbers and drill files with `kicad-cli pcb export gerbers` / `drill`, or use the JLCPCB plugin.
2. On JLCPCB, order **0.8 mm** FR4 with an ENIG finish. ENIG is flatter, which helps the SMD switches sit level. Quantity 5 is the minimum.
3. **Before ordering**, print the PCB at 1:1 on paper and place real switches, keycaps, and the XIAO on it.

## Checklist
- [ ] Footprint pads match the datasheet (14.70 × 14.00 extents, 5.80 mm contact spacing)
- [ ] All 18 switches per half are on unique row/col nets
- [ ] Diode orientation is consistent (col2row) on both sides of the reversible footprint
- [ ] XIAO power-pin jumpers are correct for both orientations
- [ ] The XIAO cutout clears the measured components and USB-C
- [ ] The power switch is in series with BAT+
- [ ] The antenna keep-out is respected
- [ ] DRC is clean and the 1:1 paper print has been tested
