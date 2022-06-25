#!/bin/bash

if [[ $(id -u) != 0 ]]
then
	echo "Please, run this script as root (using sudo for example)"
	exit 1
fi

systemctl stop asus_fliplock
if [[ $? != 0 ]]
then
	echo "asus_fliplock.service cannot be stopped correctly..."
	exit 1
fi

systemctl disable asus_fliplock
if [[ $? != 0 ]]
then
	echo "asus_fliplock.service cannot be disabled correctly..."
	exit 1
fi

rm -f /lib/systemd/system/asus_fliplock.service
if [[ $? != 0 ]]
then
	echo "/lib/systemd/system/asus_fliplock.service cannot be removed correctly..."
	exit 1
fi

rm -rf /usr/share/asus_fliplock-driver/
if [[ $? != 0 ]]
then
	echo "/usr/share/asus_fliplock-driver/ cannot be removed correctly..."
	exit 1
fi

rm -rf /var/log/asus_fliplock-driver
if [[ $? != 0 ]]
then
	echo "/var/log/asus_fliplock-driver cannot be removed correctly..."
	exit 1
fi

echo "Asus fliplock python driver uninstalled"
exit 0
