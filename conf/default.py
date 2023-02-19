from libevdev import EV_KEY

laptop_mode_actions = [
    # setting up saved keyboard backlight brightness (restore from backup)
    "test -f /tmp/kbd_backlight_brightness && cat /tmp/kbd_backlight_brightness | sudo tee /sys/class/leds/asus::kbd_backlight/brightness",
    # setting up saved capslock backlight brightness (restore from backup)
    "test -f /tmp/input3_capslock_brightness && cat /tmp/input3_capslock_brightness | sudo tee /sys/class/leds/input3\:\:capslock/brightness"
]

tablet_mode_actions = [
    # save keyboard backlight brightness (do a backup)
    "cat /sys/class/leds/asus::kbd_backlight/brightness | sudo tee /tmp/kbd_backlight_brightness",
    # disable keyboard backlight brightness
    "echo 0 | sudo tee /sys/class/leds/asus::kbd_backlight/brightness",
    # save capslock led brightness (do a backup)
    "cat /sys/class/leds/input3\:\:capslock/brightness | sudo tee /tmp/input3_capslock_brightness",
    # disable capslock led brightness
    "echo 0 | sudo tee /sys/class/leds/input3\:\:capslock/brightness"
]

flip_key = EV_KEY.KEY_PROG2
