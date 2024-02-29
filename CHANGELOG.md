# Changelog

## 1.2.0 (29.2.2024)

### Fixed

- Fixed changing numbers in path `/sys/class/leds/input<number>` used in preconfigured layout
- Fixed triggering only by event key (default `EV_KEY.KEY_PROG2`)

### Feature

- To preconfigured layout added example how to disable LEDs using `/sys/kernel/debug/asus-nb-wmi` with no kernel support yet
- Added support for installed driver [asus-accel-tablet-mode-driver](https://github.com/asus-linux-drivers/asus-accel-tablet-mode-driver)

## 1.1.1 (25.12.2023)

### Fixed

- Usage #!/usr/bin/env instead of hardcoded path bash/sh