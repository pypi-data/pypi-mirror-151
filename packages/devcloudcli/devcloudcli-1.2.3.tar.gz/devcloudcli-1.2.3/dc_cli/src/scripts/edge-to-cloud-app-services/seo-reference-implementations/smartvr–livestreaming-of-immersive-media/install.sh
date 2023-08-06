#!/bin/bash

sudo apt-get update
sudo apt-get install expect
HOST_IP=$(hostname -I | cut -d' ' -f1)
echo "Installing smartvr–livestreaming-of-immersive-media ..."  
pip3 install edgesoftware
sudo mkdir smartvr–livestreaming-of-immersive-media
cd smartvr–livestreaming-of-immersive-media

/usr/bin/expect -c '
set timeout -1
spawn edgesoftware install smartvr–livestreaming-of-immersive-media 62342da3905e50fbc0da8ac5
expect "download:" {send "echo 634e374f-b086-411a-916a-53da4b2739db\n"}
expect "Enter correct IP address of this machine (Example: 123.123.123.123):" {send "$HOST_IP\r"}
expect eof'


