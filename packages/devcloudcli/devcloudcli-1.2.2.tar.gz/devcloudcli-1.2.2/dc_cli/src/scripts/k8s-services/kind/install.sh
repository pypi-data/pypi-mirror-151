#!/bin/bash

if [[ $(which docker) && $(docker --version) ]]; then
         echo "Docker is installed "
     else
         echo "Install docker from devtool"
         # command
         #sudo apt-get remove docker docker-engine docker.io containerd runc
fi

#install microk8s
if [[ $(which kind) && $(sudo kind --version) ]]; then
         echo "kind is installed"
     else
         echo "installing kind....."
         echo
         curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.12.0/kind-linux-amd64
         sudo chmod +x ./kind
	 sudo groupadd docker
         sudo usermod -aG docker $USER
         sudo mv ./kind /usr/local/bin/kind
fi

