#!/usr/bin/env python3

import importlib
import logging
import os
from time import sleep
import re
import sys
from typing import Optional
from libevdev import Device, EV_SW

# Setup logging
# LOG=DEBUG sudo -E ./asus_fliplock.py "default" # all messages
# LOG=ERROR sudo -E ./asus_fliplock.py "default" # only error messages
logging.basicConfig()
log = logging.getLogger('Asus fliplock')
log.setLevel(os.environ.get('LOG', 'INFO'))

# Layout
layout = 'default'
if len(sys.argv) > 1:
    layout = sys.argv[1]

fliplock_layouts = importlib.import_module('conf.'+ layout)

switches: Optional[str] = None
wmi_hotkeys: Optional[str] = None

switches_detected = 0
wmi_hotkeys_detected = 0

def search_devices():

    global switches, wmi_hotkeys
    global touchpad_detected, switches_detected, wmi_hotkeys_detected

    tries = 5

    # Look into the devices file
    while tries > 0:

        with open('/proc/bus/input/devices', 'r') as f:
            lines = f.readlines()
            for line in lines:

                # Look for the device switches
                if re.search("switches", line):
                    switches_detected = 1
                    log.debug('Detect switches from %s', line.strip())

                # Look for the device wmi hotkey or https://github.com/asus-linux-drivers/asus-accel-tablet-mode-driver
                if wmi_hotkeys_detected == 0 and (("Name=\"Asus WMI hotkeys" in line and tries == 4) or ("Name=\"Asus WMI accel tablet mode" in line and tries == 5)):
                    wmi_hotkeys_detected = 1
                    log.debug('Detect wmi hotkeys from %s', line.strip())

                if wmi_hotkeys_detected == 1:
                    if "H: " in line:
                        wmi_hotkeys = line.split("event")[1]
                        wmi_hotkeys = wmi_hotkeys.split(" ")[0]
                        wmi_hotkeys_detected = 2
                        log.debug('Set wmi hotkeys id %s from %s', wmi_hotkeys, line.strip())
                        break

                if switches_detected == 1:
                    if "H: " in line:
                        switches = line.split("event")[1]
                        switches = switches.split(" ")[0]
                        switches_detected = 2
                        log.debug('Set switches id %s from %s', switches, line.strip())
                        break

                if switches_detected == 2 and wmi_hotkeys_detected == 2:
                    break

        if switches_detected != 2 or wmi_hotkeys_detected != 2:
            tries -= 1
            if tries == 0:
                if switches_detected != 2 and wmi_hotkeys_detected != 2:
                    log.error("Can't find neither switches or wmi hotkeys device")
                    sys.exit(1)
            sleep(0.1)
        else:
            break

search_devices()

# Start monitoring the switch device
fd_t_switches = None
d_t_switches = None

fd_t_wmi_hotkeys = open('/dev/input/event' + str(wmi_hotkeys), 'rb')
d_t_wmi_hotkeys = Device(fd_t_wmi_hotkeys)

# When we listen only key we predict start state is laptop mode
intel_hid_switches_tablet_mode = 1

def execute_cmd(cmd):
    try:
        os.system(cmd)
    except OSError as e:
        log.error(e)


def execute_cmds_in_array(cmds):
    for cmd in cmds:
        execute_cmd(cmd)


def flip(intel_hid_switches_tablet_mode):
    if intel_hid_switches_tablet_mode:
        execute_cmds_in_array(fliplock_layouts.tablet_mode_actions)
    else:
        execute_cmds_in_array(fliplock_layouts.laptop_mode_actions)


# If mode has been changed, do something
if switches is None and wmi_hotkeys is not None:

    for e in d_t_wmi_hotkeys.events():

        log.debug(e)

        if switches is not None:
            break

        # Pressed and released event is called during one! flipping simultanously
        if e.matches(fliplock_layouts.flip_key) and e.value == 1:
            flip(intel_hid_switches_tablet_mode)
            intel_hid_switches_tablet_mode = not intel_hid_switches_tablet_mode

        # TODO: first flip is ommited because device for swithes is added immediately when is flip_key (usually EV_KEY.KEY_PROG2) triggered
        search_devices()


if switches is not None:

    fd_t_switches = open('/dev/input/event' + str(switches), 'rb')
    d_t_switches = Device(fd_t_switches)

    for e in d_t_switches.events():

        log.debug(e)

        if e.matches(EV_SW.SW_TABLET_MODE):
            flip(e.value)