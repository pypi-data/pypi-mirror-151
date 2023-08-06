#!/bin/bash

#install rke2
if [[ $(which rke2) && $(sudo rke2 --version) ]]; then
         echo "rke2 is installed"
     else
         echo "installing rke2....."
         echo
         sudo curl -sfL https://get.rke2.io | INSTALL_RKE2_CHANNEL=v1.20 sudo sh -
         echo "Installed RKE2 successfully"
fi

