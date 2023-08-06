#!/bin/bash

sudo apt-get update
sudo apt-get install expect
HOST_IP=$(hostname -I | cut -d' ' -f1)
echo "Installing intelligent-connection-management-for-automated-handover ..."  
pip3 install edgesoftware
sudo mkdir wireless-network-ready-pcb-defect-detection
cd wireless-network-ready-pcb-defect-detection

/usr/bin/expect -c '
set timeout -1
spawn edgesoftware install wireless-network-ready-pcb-defect-detection 6221e257905e50fbc05dc793
expect "download:" {send "echo c259ebe1-e326-46e3-b2fd-1f95e20476ad\n"}
expect "Enter correct IP address of this machine (Example: 123.123.123.123):" {send "$HOST_IP\r"}
expect eof'
