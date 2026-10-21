# 03 — Firmware (ZMK)

You can do this in parallel with the PCB work once the GPIO map in [01-layout](01-layout.md) is settled.

## 1. Config repo
- Create a `zmk-config` repo from the [ZMK user setup](https://zmk.dev/docs/user-setup), or keep it in this repo under `firmware/`.
- Builds run on GitHub Actions, and the artifacts are `.uf2` files.

## 2. Custom shield
Follow the [ZMK new shield guide](https://zmk.dev/docs/development/hardware-integration/new-shield). The files go in `boards/shields/<name>/`:

| File | Purpose |
|---|---|
| `Kconfig.shield` | `SHIELD_<NAME>_LEFT` / `SHIELD_<NAME>_RIGHT` |
| `Kconfig.defconfig` | Keyboard name, `ZMK_SPLIT`, and the left side as `ZMK_SPLIT_ROLE_CENTRAL` |
| `<name>.dtsi` | kscan (col2row matrix, row GPIOs), matrix transform for 36 keys, physical layout |
| `<name>_left.overlay` / `<name>_right.overlay` | Per-side `col-gpios`, and `col-offset` on the right |
| `<name>-layouts.dtsi` | Physical layout for ZMK Studio |
| `<name>.keymap` | Default keymap |
| `<name>.zmk.yml` | Metadata |

The board target is the XIAO nRF52840. Check the current board ID in the ZMK docs, since board naming changed with the Zephyr 4.x migration (e.g. `xiao_ble//zmk`).

## 3. Config (`<name>.conf` in the zmk-config, not the shield)
```
CONFIG_ZMK_SLEEP=y
CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000      # 15 min to deep sleep
CONFIG_ZMK_BLE_EXPERIMENTAL_CONN=y
CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_FETCHING=y
CONFIG_ZMK_SPLIT_BLE_CENTRAL_BATTERY_LEVEL_PROXY=y
CONFIG_ZMK_STUDIO=y                        # central side only
```

## 4. Keymap
For 36 keys, start from a Miryoku-style or Callum-style layout with home-row mods and 3 thumb keys per side. Tweak it later in ZMK Studio without reflashing.

## 5. Flash and test
1. Double-tap reset on the XIAO to mount the UF2 drive, then copy the `.uf2` for that side.
2. Before the case is done, short each row/col pair with tweezers to confirm every key.
3. Flash `settings_reset` if pairing between the halves gets stuck.
