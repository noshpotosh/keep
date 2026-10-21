# 04 — Case (3D printed)

## Design approach
- **Parametric CAD in code**, so it stays reproducible and can be driven by Claude. Use [build123d](https://github.com/gumyr/build123d), which has an MCP server (see [resources](resources.md#mcp--ai-tooling)). OpenSCAD is an alternative.
- Import the Ergogen `output/outlines/*.dxf` (`board`, `case_outer`, `battery_pocket`) so the case always matches the PCB.
- Expose these as parameters: key pitch, PCB thickness, battery L × W × T, wall thickness, and floor thickness.

## Structure
```
  keycaps ─────────▄▄▄▄  ▄▄▄▄  ▄▄▄▄
  switches ────────████  ████  ████
  PCB (1.0 mm) ═══════════════════════════  ← rests on ledge in wall
  diodes / battery ─  ▪    [ battery ]  ▪
  floor (0.8–1.0 mm) ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
```
- It is a **tray**: the floor and walls are one piece, and the PCB drops in and sits on a perimeter ledge.
- **Retention:** use 3–4 M2 screws through the PCB into heat-set inserts (or into thin magnets), or a snap lip. The wall rises only to the PCB top surface, so the switches and keycaps stand proud. This is the "floating key" look and it is the thinnest option.
- **Support:** add ribs or posts under the PCB between the diodes, so the 1.0 mm PCB doesn't flex when typing.
- **Cutouts:** USB-C on the outer edge, the power switch slot, and an optional reset access hole.
- **Battery pocket** in the floor. Hold the cell with Kapton tape or a thin foam pad, and never compress it.
- Put rubber feet in recessed pockets so they don't add height.

## Print settings
| Method | Notes |
|---|---|
| Resin (SLA) | Best for 0.8 mm floors and crisp cutouts |
| FDM, 0.2–0.4 mm nozzle | PETG or PLA+, 0.1–0.12 mm layers, print floor-down |
| JLC3DP / PCBWay 3D | Resin or MJF, good once the design is stable |

Iterate cheaply: print a **single-key test coupon** and a **PCB-edge fit test** before you print a full half.

## Checklist
- [ ] PCB fits with about 0.2 mm clearance per side
- [ ] Battery pocket depth ≥ cell thickness + 0.2 mm
- [ ] USB-C cable plugs in fully (check the plug overmold clearance)
- [ ] Total height measured with calipers and recorded here
