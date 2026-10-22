# PG1316S design assets

These files are collected for the 36-key keeb project. They are community CAD assets, not yet checked against a physical switch or the selected Holykeebs keycaps. Verify pad dimensions and clearances before ordering a PCB or case.

## Contents

- `footprints/CPG1316S01D02_kailhspecsheet_mikefive.kicad_mod` — standard front-side footprint based on the Kailh specification sheet.
- `footprints/CPG1316S01D02_reversible_mikefives.kicad_mod` — alternate reversible-board footprint. Its overlapping front/back pads are intentional; inspect the pad and solder-mask behavior before using it.
- `3d/PG1316S-assembly.STEP` — original Kailh PG1316S assembly model, shared by Mike Holscher. Use for PCB and mechanical layout. The provided keycap exterior in this model is reported undersized; measured outer size is 16.25 × 16.05 mm.
- `3d/PG1316S-keycap-normal.step` — optional custom keycap model by Mike Holscher. This is an alternate design, not confirmed to be the stock Holykeebs cap.

## Attribution and source

Footprints and original switch assembly: Mike Holscher, [zmk-config-mikefive](https://github.com/mikeholscher/zmk-config-mikefive), `files/footprint-and-cad/`.

Alternate custom keycap: Mike Holscher, same repository, `files/custom-keycaps/`. The author's keycap README permits use and modification with attribution. See the source folder for print-fit guidance.

The author's notes report the PG1316S footprint uses pads 1 and 2 for switch contacts and four pad-3 switch-frame mounts. The spec-sheet footprint's pad 3s are separate pads; determine whether/how to connect them (the Mikefive design connects them to GND) and validate all land patterns against the Kailh datasheet.

## KiCad use

The collected footprint files point to the assembly model at this project-relative path:

```text
${KIPRJMOD}/assets/pg1316s/3d/PG1316S-assembly.STEP
```

For a personal `.pretty` library outside this project, update the model path to match your asset location. Do not treat this as a validated production footprint. The project PCB checklist requires a datasheet and physical-part review before fabrication.
