#!/bin/bash

#install rke2

export HOST_IP=$(hostname -I | cut -d' ' -f1)

if [[ $(which rke2) && $(sudo rke2 --version) ]]; then
         echo "rke2 is installed"
	 echo "Installed RKE2 successfully, Control plane can be accessed from" "http://"$HOST_IP":8080"
     else
         echo "installing rke2....."
         echo
         sudo curl -sfL https://get.rke2.io | INSTALL_RKE2_CHANNEL=v1.20 sudo sh -
	 sudo docker run -d --restart=unless-stopped -p 8080:8080 rancher/server:stable
         echo "Installed RKE2 successfully, Control plane can be accessed from"  "http://"$HOST_IP":8080"
         #echo "Installed RKE2 successfully"
fi

