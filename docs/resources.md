# Resources

## Switch & keycaps
- [Kailh PG1316S, Holykeebs product page](https://holykeebs.com/products/kailh-pg1316s-butterfly-switch-10-pack)
- [PG1316S datasheet (PDF)](https://docs.holykeebs.com/datasheets/CPG1316S01D02.pdf). This is the source of truth for the dimensions in [00-requirements](00-requirements.md)
- [Collected PG1316S KiCad footprints and STEP models](../assets/pg1316s/README.md) (community sources; validate before fabrication)
- [Kailh PG1316S keycaps](https://holykeebs.com/products/kailh-pg1316s-keycaps) — selected keycaps; see [collected local footprints and 3D models](../assets/pg1316s/README.md)
- [PG1316S practice board](https://holykeebs.com/products/pg1316s-practice-board)
- [PG1316M variant](https://holykeebs.com/products/kailh-pg1316m-ultra-thin-butterfly-switch)

## Prior art
- [vuoz/chalk](https://github.com/vuoz/chalk) is a 42-key PG1316S wireless split on XIAO nRF52840 with a 1 mm PCB, about 6 mm thick, a 3D-printed case, and ZMK. **This is the closest reference.**
- [Chalk on kbd.news](https://kbd.news/Chalk-2721.html)
- [r/ErgoMechKeyboards](https://www.reddit.com/r/ErgoMechKeyboards/). Search for "PG1316".

## PCB design
- [KiCad](https://www.kicad.org/)
- [Ergogen docs](https://docs.ergogen.xyz/) and the [web playground](https://ergogen.cache.works)
- [ceoloide/ergogen-footprints](https://github.com/ceoloide/ergogen-footprints) has KiCad 8 footprints for Ergogen v4.1+: diodes, power/reset switches, battery connectors
- [infused-kim/kb_ergogen_fp](https://github.com/infused-kim/kb_ergogen_fp), an older footprint set that includes 3D models
- [Convert KiCad footprints to Ergogen](https://nilnil.notion.site/Convert-Kicad-Footprints-to-Ergogen-8340ce87ad554c69af4e3f92bc9a0898), needed for the PG1316S footprint
- [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities)

## Controller & firmware
- [Seeed XIAO nRF52840 wiki](https://wiki.seeedstudio.com/XIAO_BLE/): pinout, battery charging (P0.13 sets 50/100 mA), battery sense (P0.31 / P0.14)
- [ZMK docs](https://zmk.dev/docs)
- [ZMK new shield guide](https://zmk.dev/docs/development/hardware-integration/new-shield)
- [ZMK user setup (zmk-config)](https://zmk.dev/docs/user-setup)

## Case CAD
- [build123d](https://github.com/gumyr/build123d), Python parametric CAD (recommended)
- [OpenSCAD](https://openscad.org/), an alternative

## MCP & AI tooling
These can be added to Claude Code with `claude mcp add ...`. Re-check each repo before installing; this space moves fast.

| Tool | What it gives us | Link |
|---|---|---|
| **kicad-mcp** | Inspect KiCad projects, run DRC, extract the BOM, analyze netlists. Needs KiCad 9+, Python 3.10+, and uv | [lamaalrajih/kicad-mcp](https://github.com/lamaalrajih/kicad-mcp) |
| **build123d-mcp** | Run build123d code in a persistent session, render views, query dimensions. Claude can "see" the case | [pzfreo/build123d-mcp](https://github.com/pzfreo/build123d-mcp) |
| `kicad-cli` (ships with KiCad) | Headless DRC, Gerber/drill/STEP export, scriptable from Claude Code | [docs](https://docs.kicad.org/) |
| `ergogen` CLI | Regenerate the PCB and outlines from YAML | `npm i -g ergogen` |
| `gh` CLI | Trigger and download ZMK GitHub Actions builds | [cli.github.com](https://cli.github.com/) |
