#!/bin/bash

if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

echo "install python3.7 and pigpio"
 apt-get update
 apt-get install pigpio python-pigpio python3-pigpio python3.7 python python-setuptools python3-setuptools -y


echo "settling to /usr/local/bin/fan-controller/..."
rm -r /usr/bin/fan-controller/ 2>/dev/null
mkdir /usr/local/bin/fan-controller
cp fan_controller.py /usr/local/bin/fan-controller/
cp FanController.py /usr/local/bin/fan-controller/
cp Mail.py /usr/local/bin/fan-controller/
cp RequestClient.py /usr/local/bin/fan-controller/
cp constant_fan.sh /usr/local/bin/fan-controller/
echo "done"

echo "adding service to /lib/systemd/system/..."
cp fan-controller.service /lib/systemd/system/
cp fan-controller.timer /lib/systemd/system
chmod 644 /lib/systemd/system/fan-controller.service
chmod 644 /lib/systemd/system/fan-controller.timer 
echo "done"

echo "creating config at /etc/fan-controller/"
mkdir /etc/fan-controller/
cp config.json /etc/fan-controller/
chmod 664 /etc/fan-controller/config.json
echo "done"

echo "starting and enabling service..."
systemctl daemon-reload
systemctl enable fan-controller.service
systemctl enable fan-controller.timer
systemctl start fan-controller.timer
echo "done"

echo "fan-controller installed sucessfully!"
echo ""
echo "To configure, edit /etc/fan-controller/config.json (needs sudo)"