# keeb — ultra-thin 36-key wireless split

A pocketable, pure-ortholinear 36-key split keyboard built on Kailh PG1316S laptop-style butterfly switches, Seeed XIAO nRF52840 controllers, ZMK firmware, and a 3D-printed case. Target total thickness: **≤ 7 mm**.

## At a glance

| | |
|---|---|
| Keys | 36 (18 per half) |
| Layout | Ortholinear, zero row/column stagger. Each half is a 5×4 grid, with the bottom row holding 3 inner thumb keys |
| Switch | Kailh PG1316S (`CPG1316S01D02-01`), soldered SMD, 25 gf actuation / 35 gf tactile, 1.8 mm travel |
| Controller | Seeed XIAO nRF52840 ×2 |
| Firmware | ZMK (split BLE, ZMK Studio) |
| Power | Thin rechargeable cell per half (thin LiPo pouch preferred, see [requirements](docs/00-requirements.md#battery)) |
| PCB | 1.0 mm FR4, 2-layer, designed with Ergogen + KiCad |
| Case | 3D printed, parametric |

```
 Left half (top view)                Right half (top view)
┌───┬───┬───┬───┬───┐             ┌───┬───┬───┬───┬───┐
│ Q │ W │ E │ R │ T │             │ Y │ U │ I │ O │ P │
├───┼───┼───┼───┼───┤             ├───┼───┼───┼───┼───┤
│ A │ S │ D │ F │ G │             │ H │ J │ K │ L │ ; │
├───┼───┼───┼───┼───┤             ├───┼───┼───┼───┼───┤
│ Z │ X │ C │ V │ B │             │ N │ M │ , │ . │ / │
├───┴───┼───┼───┼───┤             ├───┼───┼───┼───┴───┤
│ XIAO  │ T1│ T2│ T3│             │ T4│ T5│ T6│ XIAO  │
└───────┴───┴───┴───┘             └───┴───┴───┴───────┘
```

## Build phases

- [ ] **0. Requirements locked.** Resolve the open TBDs in [docs/00-requirements.md](docs/00-requirements.md)
- [ ] **1. Layout & matrix.** See [docs/01-layout.md](docs/01-layout.md)
- [ ] **2. PCB design (Ergogen → KiCad → JLCPCB).** See [docs/02-pcb.md](docs/02-pcb.md)
- [ ] **3. Firmware (ZMK shield).** See [docs/03-firmware.md](docs/03-firmware.md). This can run in parallel with phase 2
- [ ] **4. Case (3D printed).** See [docs/04-case.md](docs/04-case.md)
- [ ] **5. Assembly & test.** See [docs/05-assembly.md](docs/05-assembly.md)

Supporting docs:
- [docs/bom.md](docs/bom.md) is the parts list
- [docs/resources.md](docs/resources.md) holds links, footprints, prior art, and MCP / CLI tooling
