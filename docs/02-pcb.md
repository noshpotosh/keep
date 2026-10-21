# 02 — PCB design (Ergogen → KiCad → fab)

Workflow: **Ergogen** generates the key grid, outlines, and a placed (unrouted) KiCad board from YAML. **KiCad** handles routing, DRC, and export. The fab is **JLCPCB** (or PCBWay).

## 1. Tooling setup
- Install [KiCad 9](https://www.kicad.org/download/) (8 works too). The footprint libraries below target KiCad 8+.
- Install Node.js LTS and the Ergogen CLI: `npm i -g ergogen`, version 4.1+. The web UI at [ergogen.cache.works](https://ergogen.cache.works) is good for quick previews.
- Optional: set up the KiCad MCP server and `kicad-cli` (see [resources](resources.md#mcp--ai-tooling)).

## 2. Footprints
| Part | Source | Notes |
|---|---|---|
| PG1316S switch | [Holykeebs `CPG1316S01D02.kicad_mod`](https://docs.holykeebs.com/footprints/CPG1316S01D02.kicad_mod) | Check it against the datasheet land pattern. Convert to an Ergogen footprint (JS) |
| Diode SOD-123 | [ceoloide/ergogen-footprints](https://github.com/ceoloide/ergogen-footprints) `diode_tht_sod123.js` | |
| XIAO nRF52840 | Write a custom footprint, or adapt one from community repos | 14 castellated pads plus back-side BAT pads |
| Power switch | ceoloide `power_switch_smd_side.js` | |
| Reset switch | ceoloide `reset_switch_smd_side.js` | Optional |
| Battery | ceoloide `battery_connector_jst_ph_2.js`, or bare solder pads | Bare pads are thinner |

**Solder-from-back option.** Add plated through-holes or vias inside each PG1316S pad, as on the Holykeebs practice board and in chalk. You can then hand-solder each switch from the back with an iron instead of using a hot plate and paste. Decide this before you finalize the footprint.

## 3. Ergogen config (`ergogen/config.yaml`)
Sections to write:
- `units`: `kx: 16.5`, `ky: 16.5` (the pitch from requirements).
- `points.zones.matrix`: 5 columns × 3 rows, no `stagger`, no `splay`.
- `points.zones.thumbs`: 3 keys on row 3, aligned to columns 2–4 of the left half. This is still pure grid; just anchor the zone so the keys line up.
- `outlines`:
  - `board`: the rectangle around all key positions plus the XIAO slot.
  - `case_inner` / `case_outer`: offsets for the case CAD.
  - `battery_pocket`: on the back side.
- `pcbs.left` (and `right`, or one reversible board): `template: kicad8`. Place the switches, diodes, XIAO, power switch, and battery pads, and name the nets by matrix row and column.
- Output: `ergogen ergogen/ -o output/`. This produces `output/pcbs/*.kicad_pcb` and `output/outlines/*.dxf`.

## 4. Route in KiCad
1. Open the generated `.kicad_pcb`. Set the board setup to **1.0 mm** thickness, 2 layers, and 1 oz copper.
2. Import the JLCPCB design rules. Use 0.2 mm traces (0.25 mm for power) and 0.3/0.6 mm vias.
3. Route the columns on F.Cu and the rows on B.Cu where possible.
4. Add a **GND pour** on both layers. **Keep copper out of the area under and around the XIAO antenna** (the end opposite USB-C).
5. Add mounting features for the case: M2 holes, or keep-outs for magnets or snap-fits.
6. Run **DRC** and fix everything. Check the 3D viewer for collisions between the XIAO, the switches, and the board edge.

## 5. Order
1. Plot the Gerbers and drill files with `kicad-cli pcb export gerbers` / `drill`, or use the JLCPCB plugin.
2. On JLCPCB, order **1.0 mm** FR4 with an ENIG finish. ENIG is flatter, which helps the SMD switches sit level. Quantity 5 is the minimum.
3. Optional: a stencil, if you are using paste and a hot plate.
4. **Before ordering**, print the PCB at 1:1 on paper and place real switches, keycaps, and the XIAO on it.

## Checklist
- [ ] Footprint pads match the datasheet (14.70 × 14.00 extents, 5.80 mm contact spacing)
- [ ] All 18 switches per half are on unique row/col nets
- [ ] Diode orientation is consistent (col2row)
- [ ] The power switch is in series with BAT+
- [ ] The antenna keep-out is respected
- [ ] DRC is clean and the 1:1 paper print has been tested
