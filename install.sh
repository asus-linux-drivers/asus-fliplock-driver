#!/bin/bash

# Checking if the script is runned as root (via sudo or other)
if [[ $(id -u) != 0 ]]
then
	echo "Please run the installation script as root (using sudo for example)"
	exit 1
fi

if [[ $(sudo apt install 2>/dev/null) ]]; then
    echo 'apt is here' && sudo apt -y install libevdev2 python3-libevdev i2c-tools git
elif [[ $(sudo pacman -h 2>/dev/null) ]]; then
    echo 'pacman is here' && sudo pacman --noconfirm -S libevdev python-libevdev i2c-tools git
elif [[ $(sudo dnf install 2>/dev/null) ]]; then
    echo 'dnf is here' && sudo dnf -y install libevdev python-libevdev i2c-tools git
fi

if [[ -d conf/__pycache__ ]] ; then
    rm -rf conf/__pycache__
fi

echo
echo "Select configuration layout:"
PS3='Please enter your choice '
options=($(ls conf) "Quit")
select opt in "${options[@]}"
do
    opt=${opt::-3}
    case $opt in
        "up541ea" )
            layout=up541ea
            break
            ;;
        "Q")
            exit 0
            ;;
        *)
            echo "invalid option $REPLY";;
    esac
done

echo "Add asus fliplock service in /etc/systemd/system/"
cat asus_fliplock.service > /etc/systemd/system/asus_fliplock.service

mkdir -p /usr/share/asus_fliplock-driver/conf
mkdir -p /var/log/asus_fliplock-driver
install asus_fliplock.py /usr/share/asus_fliplock-driver/
install -t /usr/share/asus_fliplock-driver/conf conf/*.py

echo "i2c-dev" | tee /etc/modules-load.d/i2c-dev.conf >/dev/null

systemctl enable asus_fliplock

if [[ $? != 0 ]]
then
	echo "Something gone wrong while enabling asus_fliplock.service"
	exit 1
else
	echo "Asus fliplock service enabled"
fi

systemctl restart asus_fliplock
if [[ $? != 0 ]]
then
	echo "Something gone wrong while enabling asus_fliplock.service"
	exit 1
else
	echo "Asus fliplock service started"
fi

exit 0

