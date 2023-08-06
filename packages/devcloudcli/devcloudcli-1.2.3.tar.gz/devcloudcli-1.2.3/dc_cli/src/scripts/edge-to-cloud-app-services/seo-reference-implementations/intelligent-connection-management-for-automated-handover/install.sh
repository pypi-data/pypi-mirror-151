#!/bin/bash

sudo apt-get update
sudo apt-get install expect
HOST_IP=$(hostname -I | cut -d' ' -f1)
echo "intelligent-connection-management-for-automated-handover ..."  
pip3 install edgesoftware
sudo mkdir intelligent-connection-management-for-automated-handover
cd intelligent-connection-management-for-automated-handover

/usr/bin/expect -c '
set timeout -1
spawn edgesoftware install intelligent-connection-management-for-automated-handover 6241499a9654a8f4bd360ec5
expect "download:" {send "echo 54459efe-476d-4574-b1e2-aadb9482a78a\n"}
expect "Enter correct IP address of this machine (Example: 123.123.123.123):" {send "$HOST_IP\r"}
expect eof'


