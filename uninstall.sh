#!/bin/bash

#Require sudo
if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

echo "removing service..."
systemctl stop fan-controller
systemctl disable fan-controller
echo "done"


echo "removing /usr/local/bin/fan-controller/..."
rm -r /usr/local/bin/fan-controller
rm -r /usr/bin/fan-controller 2>/dev/null
echo "done"

echo "removing service from /lib/systemd/system/..."
rm /lib/systemd/system/fan-controller.service
rm /lib/systemd/system/fan-controller.service
echo "done"

echo "removing config at /etc/fan-controller/"
rm -r /etc/fan-controller/
echo "done"

echo "reloading services"
systemctl daemon-reload
echo "done"

echo "fan-controller uninstalled sucessfully!"
