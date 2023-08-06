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
spawn $::env(HOME)/.local/bin/edgesoftware install smartvr–livestreaming-of-immersive-media 62342da3905e50fbc0da8ac5
expect "download:" {send "634e374f-b086-411a-916a-53da4b2739db\n"}
expect "(Example:: 123.123.123.123):" {send $::env(HOST_IP)\n"}
expect eof'
