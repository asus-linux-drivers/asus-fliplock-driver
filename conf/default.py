from libevdev import EV_KEY

laptop_mode_actions = [
    # setting up saved keyboard backlight brightness (restore from backup)
    "test -f /tmp/kbd_backlight_brightness && cat /tmp/kbd_backlight_brightness | sudo tee /sys/class/leds/asus::kbd_backlight/brightness",
    # setting up saved capslock backlight brightness (restore from backup)
    "test -f /tmp/input_capslock_brightness && cat /tmp/input_capslock_brightness | sudo tee /sys/class/leds/input*::capslock/brightness",
    # setting up saved micmute backlight brightness (restore from backup)
    "test -f /tmp/micmute_brightness && cat /tmp/micmute_brightness | sudo tee /sys/class/leds/platform::micmute/brightness",
    # setting up saved camera backlight brightness (restore from backup)
    "test -f /tmp/camera_brightness && echo '0x60079' | sudo tee '/sys/kernel/debug/asus-nb-wmi/dev_id' >/dev/null && cat /tmp/camera_brightness | sudo tee '/sys/kernel/debug/asus-nb-wmi/ctrl_param' && sudo cat '/sys/kernel/debug/asus-nb-wmi/devs' >/dev/null"
]

tablet_mode_actions = [
    # save keyboard backlight brightness (do a backup)
    "cat /sys/class/leds/asus::kbd_backlight/brightness | sudo tee /tmp/kbd_backlight_brightness",
    # disable keyboard backlight brightness
    "echo 0 | sudo tee /sys/class/leds/asus::kbd_backlight/brightness",
    # save capslock led brightness (do a backup)
    "cat /sys/class/leds/input*::capslock/brightness | head -n 1 | sudo tee /tmp/input_capslock_brightness",
    # disable capslock led brightness
    "echo 0 | sudo tee /sys/class/leds/input*::capslock/brightness",
    # save micmute led brightness (do a backup)
    "cat /sys/class/leds/platform::micmute/brightness | sudo tee /tmp/micmute_brightness",
    # disable micmute led brightness
    "echo 0 | sudo tee /sys/class/leds/platform::micmute/brightness",
    # save camera led brightness (do a backup)
    "echo '0x60079' | sudo tee '/sys/kernel/debug/asus-nb-wmi/dev_id' >/dev/null && VALUE=$(sudo cat '/sys/kernel/debug/asus-nb-wmi/dsts' | rev | cut -d' ' -f1 | rev) && echo -n $VALUE | tail -c 1 | sudo tee /tmp/camera_brightness",
    # disable camera led brightness
    "echo '0x60079' | sudo tee '/sys/kernel/debug/asus-nb-wmi/dev_id' >/dev/null && echo '0' | sudo tee '/sys/kernel/debug/asus-nb-wmi/ctrl_param' && sudo cat '/sys/kernel/debug/asus-nb-wmi/devs' >/dev/null"
]

flip_key = EV_KEY.KEY_PROG2
