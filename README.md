# Asus fliplock driver

[![License: GPLv2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
![Maintainer](https://img.shields.io/badge/maintainer-ldrahnik-blue)
[![GitHub Release](https://img.shields.io/github/release/asus-linux-drivers/asus-fliplock-driver.svg?style=flat)](https://github.com/asus-linux-drivers/asus-fliplock-driver/releases)
[![GitHub commits](https://img.shields.io/github/commits-since/asus-linux-drivers/asus-fliplock-driver/v1.1.0.svg)](https://GitHub.com/asus-linux-drivers/asus-fliplock-driver/commit/)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fasus-linux-drivers%2Fasus-fliplock-driver&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

If you find the project useful, do not forget to give project a [![GitHub stars](https://img.shields.io/github/stars/asus-linux-drivers/asus-fliplock-driver.svg?style=flat-square)](https://github.com/asus-linux-drivers/asus-fliplock-driver/stargazers) People already did!

## Changelog

[CHANGELOG.md](CHANGELOG.md)

## Features

- When does not exist device `Intel HID switches` yet, driver will try find again every 5s and will use for first time flip event from `Asus WMI hotkeys`, concretely will catch configurable key, by default `EV_KEY.KEY_PROG2`
- When you do not receive event `EV_KEY.KEY_PROG2` neither `switch tablet-mode state` drivers work together with https://github.com/asus-linux-drivers/asus-accel-tablet-mode-driver (e.g. laptop `UN5401QAB_UN5401QA` and associated issue https://github.com/asus-linux-drivers/asus-fliplock-driver/issues/3)
- By default disable backlight of keyboard in tablet mode, Remember latest backlight levels via temp file located in `/tmp`
- By default disable backlight of NumLock key in tablet mode
- By default disable backlight of NumberPad in tablet mode, remember latest backlight level via temp file located in `/tmp`
- By default disable backlight of MicMute key in tablet mode, remember latest backlight level via temp file located in `/tmp`

## Preview

![gif preview](./preview.gif)

<br/>


## Installation

You can get the latest ASUS fliplock driver for Linux from Git and install it using the following commands.
```
git clone https://github.com/asus-linux-drivers/asus-fliplock-driver
cd asus-fliplock-driver
sudo ./install.sh
```

To uninstall, just run:
```
sudo ./uninstall.sh
```

When you do not receive event `KEY_PROG2` neither `SWITCH_TOGGLE`:

```
$ sudo libinput debug-events
...
-event4   DEVICE_ADDED     Asus WMI hotkeys                  seat0 default group11 cap:k
...
-event4   KEYBOARD_KEY     +0.623s	KEY_PROG2 (149) pressed
 event4   KEYBOARD_KEY     +0.623s	KEY_PROG2 (149) released
-event29  DEVICE_ADDED     Intel HID switches                seat0 default group16 cap:S
 event29  SWITCH_TOGGLE    +0.722s	switch tablet-mode state 1
-event29  SWITCH_TOGGLE    +1.174s	switch tablet-mode state 0
-event4   KEYBOARD_KEY     +1.175s	KEY_PROG2 (149) pressed
 event4   KEYBOARD_KEY     +1.175s	KEY_PROG2 (149) released
```

try install this driver together with https://github.com/asus-linux-drivers/asus-accel-tablet-mode-driver


**Troubleshooting**

To activate logger, do in a console:
```
LOG=DEBUG sudo -E ./asus_fliplock.py "default"
```

## Existing similar projects

- [sh] how to create own script under `/etc/acpi/events` - https://askubuntu.com/questions/980997/how-do-i-disable-the-touchpad-when-the-lid-is-twisted-or-closed
- [ruby] https://github.com/alesya-h/linux_detect_tablet_mode

**Why was this project created?** Easy installation/uninstallation and with default config aimed for Asus laptops.
