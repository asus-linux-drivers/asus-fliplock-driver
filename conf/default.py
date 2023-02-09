from libevdev import EV_KEY

orientation_bottom_up_actions = [
    "cat /sys/class/leds/asus::kbd_backlight/brightness | sudo tee /tmp/kbd_backlight_brightness",
    "echo 0 | sudo tee /sys/class/leds/asus::kbd_backlight/brightness",
    "cat /sys/class/leds/input3\:\:capslock/brightness | sudo tee /tmp/input3_capslock_brightness",
    "echo 0 | sudo tee /sys/class/leds/input3\:\:capslock/brightness"
]

orientation_left_up_actions = [
    "sudo rm -f /tmp/kbd_backlight_brightness",
    "sudo rm -f /tmp/input3_capslock_brightness"
    # TODO: enable touchpad (is disabled by default for every rotation probably)
    #"xinput set-prop 17 'Device Enabled' 0"
]

orientation_right_up_actions = [
    "sudo rm -f /tmp/kbd_backlight_brightness",
    "sudo rm -f /tmp/input3_capslock_brightness",
    # TODO: enable touchpad (is disabled by default for every rotation probably)
]

orientation_normal_actions = [
    # backward setting up saved backlight brightness (only in case inverted was previous state! otherwise tmp file does not exist)
    "test -f /tmp/kbd_backlight_brightness && cat /tmp/kbd_backlight_brightness | sudo tee /sys/class/leds/asus::kbd_backlight/brightness",
    # backward setting up saved capslock led (only in case inverted was previous state! otherwise tmp file does not exist)
    "test -f /tmp/input3_capslock_brightness && cat /tmp/input3_capslock_brightness | sudo tee /sys/class/leds/input3\:\:capslock/brightness"
]

flip_key = EV_KEY.KEY_PROG2