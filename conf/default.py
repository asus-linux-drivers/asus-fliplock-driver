from libevdev import EV_KEY

to_tablet_mode_actions = [
    "cat /sys/class/leds/asus::kbd_backlight/brightness | sudo tee /tmp/kbd_backlight_brightness",
    "echo 0 | sudo tee /sys/class/leds/asus::kbd_backlight/brightness",
    "cat /sys/class/leds/input3\:\:capslock/brightness | sudo tee /tmp/input3_capslock_brightness",
    "echo 0 | sudo tee /sys/class/leds/input3\:\:capslock/brightness"
]

to_laptop_mode_actions = [
    "cat /tmp/kbd_backlight_brightness | sudo tee /sys/class/leds/asus::kbd_backlight/brightness",
    "cat /tmp/input3_capslock_brightness | sudo tee /sys/class/leds/input3\:\:capslock/brightness"
]

flip_key = EV_KEY.KEY_PROG2