#!/bin/bash

if [[ $(which docker) && $(docker --version) ]]; then
         echo "Docker is installed "
     else
         echo "Install docker from devtool"
         # command
         #sudo apt-get remove docker docker-engine docker.io containerd runc
fi

#install k3s
if [[ $(which k3s) && $(sudo k3s --version) ]]; then
         echo "k3s is installed"
     else
         echo "installing k3s....."
         echo
         curl -sfL https://get.k3s.io | sh -
	 sudo groupadd docker
         sudo usermod -aG docker $USER
	 echo "Installed K3s successfully"
fi

