# 05 — Assembly & test

Practise first. The [Holykeebs PG1316S practice board](https://holykeebs.com/products/pg1316s-practice-board) is cheap, and these switches are close to impossible to desolder.

## Order of operations (per half)
1. **Inspect the PCB.** Check for shorts between BAT+ and GND, and between VCC and GND.
2. **Diodes** on the back. Check orientation against the silkscreen **before** soldering. Use minimal solder, because blobs can lift whatever sits on top.
3. **XIAO.** Solder the castellations flat. Flash the firmware **now** and confirm it enumerates over USB.
4. **Matrix test before switches:** short each switch's pads with tweezers and confirm the keypress (use the ZMK keymap or a key tester site).
5. **Switches:**
   - **Pads method:** use a thin layer of paste and a hot plate or hot air at ≤ 260 °C for < 5 s.
   - **Through-hole method:** place the switch, then solder from the back through the via-in-pad with the iron at ≤ 280 °C for ≤ 3 s.
   - **Use very little solder.** Excess solder stops the switch sitting flat.
   - Test continuity on each column after soldering a column.
6. **Power switch and battery.** **Check polarity with a multimeter before connecting.** Solder BAT− to XIAO BAT−, and BAT+ through the power switch to XIAO BAT+.
7. **Full test on battery:** pairing, every key, battery % reporting, and sleep/wake.
8. **Into the case.** Fix the battery with Kapton or foam, then fit the PCB and screws.
9. **Keycaps.** Optionally add a 0.5 mm Poron foam layer to quiet them (a tip from chalk).

## Debug tips
- A whole row or column dead means a trace or XIAO pin joint problem. Reflow it.
- A single key dead means the diode orientation or a switch pad joint.
- The halves don't pair: flash `settings_reset` to both, then reflash the firmware.
