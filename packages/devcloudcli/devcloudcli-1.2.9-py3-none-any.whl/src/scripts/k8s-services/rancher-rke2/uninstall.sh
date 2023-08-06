#!/bin/bash


echo "Uninstalling RKE2"
sudo /usr/local/bin/rke2-uninstall.sh
sudo rm -rf /var/lib/rancher
echo "RKE2 completely removed"

