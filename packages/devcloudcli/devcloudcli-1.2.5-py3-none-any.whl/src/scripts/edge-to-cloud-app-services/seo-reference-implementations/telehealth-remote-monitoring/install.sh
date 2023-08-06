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
spawn $::env(HOME)/.local/bin/edgesoftware install telehealth-remote-monitoring 6221e295905e50fbc05dd07c
expect "Please enter the Product Key. The Product Key is contained in the email you received from Intel confirming your download:" {send "8cd89fbf-351e-4d5a-ac5c-c11a33f9d819\n"}
expect "(Example:: 123.123.123.123):" {send $::env(HOST_IP)\n"}
expect EOF'
