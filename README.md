# Asus fliplock driver

[![License: GPLv2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
![Maintainer](https://img.shields.io/badge/maintainer-ldrahnik-blue)
[![GitHub Release](https://img.shields.io/github/release/asus-linux-drivers/asus-fliplock-driver.svg?style=flat)](https://github.com/asus-linux-drivers/asus-fliplock-driver/releases)
[![GitHub commits](https://img.shields.io/github/commits-since/asus-linux-drivers/asus-fliplock-driver/v1.0.1.svg)](https://GitHub.com/asus-linux-drivers/asus-fliplock-driver/commit/)

If you find the project useful, do not forget to give project a [![GitHub stars](https://img.shields.io/github/stars/asus-linux-drivers/asus-fliplock-driver.svg?style=flat-square)](https://github.com/asus-linux-drivers/asus-fliplock-driver/stargazers) People already did!

![gif preview](./preview.gif)

## Features

- Disable backlight of keyboard in tablet mode and use latest level of backlight when is mode changed back to laptop mode; NumberPad backlight does the same; CapsLock led too; history may be done for example via optional file [`brightness_hw_changed`](https://patchwork.kernel.org/project/platform-driver-x86/patch/20170129134252.6185-1-hdegoede@redhat.com/) or temp file located in `/tmp`
- When does not exist device `Intel HID switches` yet, driver will try find again every 5s and use for first flip event from `Asus WMI hotkeys`, concretely will catch configurable key, by default `EV_KEY.KEY_PROG2`

<br/>

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

**Troubleshooting**

To activate logger, do in a console:
```
LOG=DEBUG sudo -E ./asus_fliplock.py "default"
```

## Existing similar projects

- [bash] https://github.com/alesya-h/linux_detect_tablet_mode
- [bash] https://gist.github.com/ACamposPT/6794aa02a6e5e341f123d447b3645b93

Why was this project created? Easy installation/uninstallation and with default config aimed for Asus laptops.
