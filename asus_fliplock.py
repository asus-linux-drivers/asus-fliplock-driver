#!/usr/bin/env python3

import importlib
import logging
import os
import re
import sys
import time
import subprocess
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

touchpad_name: Optional[str] = None
touchpad_id = 0
switches: Optional[str] = None
wmi_hotkeys: Optional[str] = None

touchpad_detected = 0
switches_detected = 0
wmi_hotkeys_detected = 0

def search_devices():

    global touchpad_name, touchpad_id, switches, wmi_hotkeys
    global touchpad_detected, switches_detected, wmi_hotkeys_detected

    tries = 5

    # Look into the devices file
    while tries > 0:

        with open('/proc/bus/input/devices', 'r') as f:
            lines = f.readlines()
            for line in lines:

                # Look for the touchpad
                if touchpad_detected == 0 and ("Name=\"ASUE" in line or "Name=\"ELAN" in line) and "Touchpad" in line:
                    touchpad_detected = 1
                    log.info('Detecting touchpad from string: \"%s\"', line.strip())
                    touchpad_name = line.split("\"")[1]
                    
                # Look for the device switches
                if re.search("switches", line):
                    switches_detected = 1
                    log.debug('Detect switches from %s', line.strip())

                # Look for the device wmi hotkeys
                if wmi_hotkeys_detected == 0 and ("Name=\"Asus WMI hotkeys" in line):
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

                if switches_detected == 2 and wmi_hotkeys_detected == 2 and touchpad_detected == 1:
                    break

        if switches_detected != 2:
            tries -= 1
            if tries == 0:
                if switches_detected != 2 and wmi_hotkeys_detected != 2:
                    log.error("Can't find neither switches or wmi hotkeys device")
                    sys.exit(1)
        else:
            break

search_devices()

# Start monitoring the switch device
fd_t_switches = None
d_t_switches = None

fd_t_wmi_hotkeys = open('/dev/input/event' + str(wmi_hotkeys), 'rb')
d_t_wmi_hotkeys = Device(fd_t_wmi_hotkeys)

def execute_cmd(cmd):
    try:
        os.system(cmd)
    except OSError as e:
        log.error(e)


def execute_cmds_in_array(cmds):
    for cmd in cmds:
        execute_cmd(cmd)


def change_touchpad_orientation(orientation):
    global touchpad_name, touchpad_id

    transform_matrix = False
    if orientation == "normal":
        transform_matrix = "1 0 0 0 1 0 0 0 1"
    elif orientation == "bottom-up":
        transform_matrix = "-1 0 1 0 -1 1 0 0 1"
    elif orientation == "right-up":
        transform_matrix = "0 1 0 -1 0 1 0 0 1"
    elif orientation == "left-up":
        transform_matrix = "0 -1 1 1 0 0 0 0 1"

    if transform_matrix:
        transform_matrix_name = "Coordinate Transformation Matrix"
        touchpad_id_regexp = "(?<=id=).*(?=\\t)"

        try:
            cmd_touchpad_id = "xinput | grep '" + touchpad_name + "'"
            touchpad_row_with_id = subprocess.check_output(cmd_touchpad_id, shell=True)
            touchpad_row_with_id_decoded = touchpad_row_with_id.decode()
            matches = re.findall(touchpad_id_regexp, touchpad_row_with_id_decoded)
            if matches:
                touchpad_id = matches[0]

            if touchpad_id:
                if orientation != "bottom-up":
                    cmd_enable_touchpad = "xinput set-prop {} 'Device Enabled' 1".format(touchpad_id)
                    log.debug(cmd_enable_touchpad)
                    subprocess.check_output(cmd_enable_touchpad, shell=True)
                else:
                    cmd_disable_touchpad = "xinput set-prop {} 'Device Enabled' 0".format(touchpad_id)
                    log.debug(cmd_disable_touchpad)
                    subprocess.check_output(cmd_disable_touchpad, shell=True)

            cmd_rotate_touchpad = "xinput set-prop '" + touchpad_name + "' '" + transform_matrix_name + "' " + transform_matrix
            log.debug(cmd_rotate_touchpad)
            subprocess.check_output(cmd_rotate_touchpad, shell=True)
        except subprocess.CalledProcessError as e:
            log.error(e.output)


def execute_cmds_according_to_accelerometer_orientation():

    # inverted when is orientation not recognized
    orientation = "bottom-up"
    orientation_regexp = "(?<=orientation: ).*?(?=\))"

    try:
        monitor_sensors = subprocess.Popen("monitor-sensor", shell=True, stdout=subprocess.PIPE)

        for line in monitor_sensors.stdout:
            utf8_line = line.decode()
            matches = re.findall(orientation_regexp, utf8_line)
            if matches:
                orientation = matches[0]
                log.debug(utf8_line)
                break

    except subprocess.CalledProcessError as e:
        log.error(e.output)

    # change by default matrix of touchpad
    # run custom commands from conf
    if orientation == "bottom-up":
        change_touchpad_orientation(orientation)
        execute_cmds_in_array(fliplock_layouts.orientation_bottom_up_actions)
    elif orientation == "right-up":
        change_touchpad_orientation(orientation)
        execute_cmds_in_array(fliplock_layouts.orientation_right_up_actions)
    elif orientation == "left-up":
        change_touchpad_orientation(orientation)
        execute_cmds_in_array(fliplock_layouts.orientation_left_up_actions)
    elif orientation == "normal":
        change_touchpad_orientation(orientation)
        execute_cmds_in_array(fliplock_layouts.orientation_normal_actions)


# run for first time when is service started
execute_cmds_according_to_accelerometer_orientation()

# If mode has been changed, do something
if switches is None and wmi_hotkeys is not None:

    for e in d_t_wmi_hotkeys.events():

        log.debug(e)

        if switches is not None:
            break

        if e.matches(fliplock_layouts.flip_key):
            time.sleep(2)
            execute_cmds_according_to_accelerometer_orientation()

        search_devices()


if switches is not None:

    fd_t_switches = open('/dev/input/event' + str(switches), 'rb')
    d_t_switches = Device(fd_t_switches)

    for e in d_t_switches.events():

        log.debug(e)

        if e.matches(EV_SW.SW_TABLET_MODE):
            time.sleep(2)
            execute_cmds_according_to_accelerometer_orientation()