#!/bin/bash

# Checking if the script is runned as root (via sudo or other)
if [[ $(id -u) != 0 ]]
then
	echo "Please run the installation script as root (using sudo for example)"
	exit 1
fi

if [[ $(apt install 2>/dev/null) ]]; then
    echo 'apt is here' && apt -y install libevdev2 python3-libevdev
elif [[ $(pacman -h 2>/dev/null) ]]; then
    echo 'pacman is here' && pacman --noconfirm -S libevdev python-libevdev
elif [[ $(dnf install 2>/dev/null) ]]; then
    echo 'dnf is here' && dnf -y install libevdev python-libevdev
fi

if [[ -d conf/__pycache__ ]] ; then
    rm -rf conf/__pycache__
fi

echo
echo "Select configuration layout:"
PS3='Please enter your choice '
options=($(ls conf) "Quit")
select selected_opt in "${options[@]}"
do
    if [ "$selected_opt" = "Quit" ]
    then
        exit 0
    fi

    for option in $(ls conf);
    do
        if [ "$option" = "$selected_opt" ] ; then
            model=${selected_opt::-3}
            break
        fi
    done

    if [ -z "$model" ] ; then
        echo "invalid option $REPLY"
    else
        break
    fi
done

echo "Add asus fliplock service in /etc/systemd/system/"
cat asus_fliplock.service | LAYOUT=$model envsubst '$LAYOUT' > /etc/systemd/system/asus_fliplock.service

mkdir -p /usr/share/asus_fliplock-driver/conf
mkdir -p /var/log/asus_fliplock-driver
install asus_fliplock.py /usr/share/asus_fliplock-driver/
install -t /usr/share/asus_fliplock-driver/conf conf/*.py

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

