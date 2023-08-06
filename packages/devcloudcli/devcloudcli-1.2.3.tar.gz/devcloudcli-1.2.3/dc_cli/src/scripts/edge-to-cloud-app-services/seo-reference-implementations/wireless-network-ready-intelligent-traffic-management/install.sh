#!/bin/bash

sudo apt-get update
sudo apt-get install expect
HOST_IP=$(hostname -I | cut -d' ' -f1)
echo "Installing wireless-network-ready-intelligent-traffic-management ..." 
pip3 install edgesoftware
sudo mkdir wireless-network-ready-intelligent-traffic-management
cd wireless-network-ready-intelligent-traffic-management

/usr/bin/expect -c '
set timeout -1
spawn edgesoftware install wireless-network-ready-intelligent-traffic-management 623c98999654a8f4bd94f55b
expect "download:" {send "echo 04b8af94-ecea-4377-bf8c-19592d3ac4f7\n"}
expect "Enter correct IP address of this machine (Example: 123.123.123.123):" {send "$HOST_IP\r"}
expect eof'




