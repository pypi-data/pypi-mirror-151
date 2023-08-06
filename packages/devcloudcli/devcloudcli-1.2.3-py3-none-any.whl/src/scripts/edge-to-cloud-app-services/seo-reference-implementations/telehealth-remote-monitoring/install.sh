#!/bin/bash

sudo apt-get update
sudo apt-get install expect
HOST_IP=$(hostname -I | cut -d' ' -f1)
echo "Installing telehealth-remote-monitoring ..."  
pip3 install edgesoftware
sudo mkdir telehealth-remote-monitoring
cd telehealth-remote-monitoring

/usr/bin/expect -c '
set timeout -1
spawn edgesoftware install telehealth-remote-monitoring 6221e295905e50fbc05dd07c
expect "download:" {send "echo 8cd89fbf-351e-4d5a-ac5c-c11a33f9d819\n"}
expect "Enter correct IP address of this machine (Example: 123.123.123.123):" {send "$HOST_IP\r"}
expect eof'

