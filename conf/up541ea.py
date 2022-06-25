from libevdev import EV_KEY

to_tablet_mode_actions = [
    "echo 0 | sudo tee -a /sys/class/leds/asus::kbd_backlight/brightness"
]

to_laptop_mode_actions = [
    "cat /sys/class/leds/asus::kbd_backlight/brightness_hw_changed | sudo tee -a /sys/class/leds/asus::kbd_backlight/brightness"
]

flip_key = EV_KEY.KEY_PROG2