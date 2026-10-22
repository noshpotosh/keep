# 04 — Case (3D printed)

## Design approach
- **Parametric CAD in code**, so it stays reproducible and can be driven by Claude. Use [build123d](https://github.com/gumyr/build123d), which has an MCP server (see [resources](resources.md#mcp--ai-tooling)). OpenSCAD is an alternative.
- Import the Ergogen `output/outlines/*.dxf` (`board`, `case_outer`, `battery_pocket`) so the case always matches the PCB.
- Expose these as parameters: key pitch, PCB thickness, battery L × W × T, wall thickness, and floor thickness.
- The concept model is [`cad/keyboard.py`](../cad/keyboard.py). It builds both halves with placeholder switches, the XIAO and the battery, and exports STEP and GLB. Pass `enclosed` to build the Designer-style concept instead: a top shell with a deck around every key on a flat bottom plate, at 18 mm pitch, because the deck webs need room. It is a comparison, not the locked design. The viewer switches between the two with the **Case** buttons. It prints clearance checks after each build. Run `node cad/render.mjs` to regenerate the renders in [`renders/`](renders/) from the viewer (it needs `playwright`).

## Switch and keycap models
Use the collected [PG1316S STEP and keycap assets](../assets/pg1316s/README.md) to preview switch clearance and case height. The original Kailh assembly model has a reported undersized keycap exterior; use the measured 16.25 × 16.05 mm outer cap dimensions for initial spacing and confirm with the Holykeebs caps before finalizing the case. The separate custom keycap STEP is an alternate shape, not the selected stock cap.

## Structure
```
  keycaps ─────────▄▄▄▄  ▄▄▄▄  ▄▄▄▄
  switches ────────████  ████  ████
  PCB (0.8 mm) ═══════════════════════════  ← rests on ledge in wall
  diodes / battery ─  ▪    [ battery ]  ▪
  floor (0.8 mm; open under the battery) ▔▔▔▔▔▔▔▔▔▔▔▔
```
- It is a **tray**: the floor and walls are one piece, with soft rounded edges and 6 mm plan-view corner radii. The PCB drops in and sits on a perimeter ledge.
- **Floating keys.** The wall rises only to the PCB top surface, so the switches and keycaps stand proud. There is no top deck, because at 17 mm pitch the webs would be about 0.15 mm.
- **Retention:** 3–4 M2 screws through the PCB into heat-set inserts (or thin magnets), or a snap lip.
- **Mirrored halves.** One reversible PCB serves both halves, so the left and right trays are mirror images.
- **Support:** add ribs or posts under the PCB between the diodes. The 0.8 mm PCB flexes, so place supports densely, roughly one per key.
- **Cutouts:** USB-C on the outer edge (it sits low, because the XIAO is face-down), the power switch slot, and a **reset pinhole** in the floor under the XIAO's button.
- **USB-C pocket:** the face-down XIAO's USB-C ends about 2.4 mm below the PCB, which is deeper than the 1.9 mm cavity. Thin the floor under it, and confirm with the measured part.
- **Battery pocket** goes **through the floor** and is covered with Kapton or a sticker. That saves about 0.8 mm. Hold the cell with Kapton tape, and never compress it.
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
- [ ] Battery pocket depth ≥ cell thickness + 0.1 mm
- [ ] USB-C cable plugs in fully (check the plug overmold clearance)
- [ ] Total height measured with calipers and recorded here
