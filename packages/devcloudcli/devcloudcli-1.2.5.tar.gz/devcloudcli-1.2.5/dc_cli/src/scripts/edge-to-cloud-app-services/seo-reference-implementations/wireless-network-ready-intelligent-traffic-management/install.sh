#!/bin/bash
#Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
sudo apt-get update
sudo apt-get install expect -y
export HOST_IP=$(hostname -I | cut -d' ' -f1)
echo "Installing edgesoftware ..."
pip3 install --upgrade pip && pip3 install edgesoftware
echo $HOST_IP
/usr/bin/expect -c '
set timeout -1
spawn $::env(HOME)/.local/bin/edgesoftware install wireless-network-ready-intelligent-traffic-management 623c98999654a8f4bd94f55b
expect "download:" {send "04b8af94-ecea-4377-bf8c-19592d3ac4f7\n"}
expect "Enter correct IP address of this machine (Example: 123.123.123.123):" {send $::env(HOST_IP)\r"}
expect eof'
