# Asus fliplock driver

If you find the project useful, do not forget to give project a [![GitHub stars](https://img.shields.io/github/stars/asus-linux-drivers/asus-fliplock-driver.svg?style=flat-square)](https://github.com/asus-linux-drivers/asus-fliplock-driver/stargazers) People already did!

![gif preview](./preview.gif)

## TODO:

- [x] (Configurable support of flip key mapping)
- [x] (Disable backlight of keyboard in tablet mode and use latest level of backlight when is mode changed back to laptop; numpad backlight does the same; history may be done for example via optional file [`brightness_hw_changed`](https://patchwork.kernel.org/project/platform-driver-x86/patch/20170129134252.6185-1-hdegoede@redhat.com/) or temp file located in `/tmp`)
- [x] (Disable backlight of capslock led in tablet mode and use latest level of backlight when is mode changed back to laptop; numpad backlight does the same)
- [x] (When after laptop start does not exist device `Intel HID switches` yet (driver will try find again every 5s) use for first change mode device `Asus WMI hotkeys` and listen for configurable key (in my case `KEY_PROG2`) then is imediatelly added device `Intel HID switches`)

<br/>

Install required packages

- Debian / Ubuntu / Linux Mint / Pop!_OS / Zorin OS:
```
sudo apt install libevdev2 python3-libevdev git
```

- Arch Linux / Manjaro:
```
sudo pacman -S libevdev python-libevdev git
```

- Fedora:
```
sudo dnf install libevdev python-libevdev git
```


Now you can get the latest ASUS fliplock driver for Linux from Git and install it using the following commands.
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
LOG=DEBUG sudo -E ./asus_fliplock.py
```

For some operating systems with boot failure (Pop!OS, Mint, ElementaryOS, SolusOS), before installing, please uncomment in the asus_touchpad.service file, this following property and adjust its value:
```
# ExecStartPre=/bin/sleep 2
```

## Credits

Thank you very much [github.com/mohamed-badaoui](github.com/mohamed-badaoui) and all the contributors of [asus-touchpad-numpad-driver](https://github.com/mohamed-badaoui/asus-touchpad-numpad-driver) for your work.

## Existing similar projects

- [bash] https://github.com/alesya-h/linux_detect_tablet_mode

Why was this project created? Easier installation/uinstallation and usage of python libevdev.
