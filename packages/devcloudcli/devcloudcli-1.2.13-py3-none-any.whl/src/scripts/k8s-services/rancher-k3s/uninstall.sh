#!/bin/bash


#if [[ $(which kind) && $(sudo kind --version) ]]; then
#         echo "kind is installed, starting kind"
#     else
#         echo"install kind using install-kind.sh file"
#         echo
#fi

echo "Uninstalling K3s"
sudo /usr/local/bin/k3s-uninstall.sh
sudo rm -rf /var/lib/rancher
echo "k3s completely removed"

