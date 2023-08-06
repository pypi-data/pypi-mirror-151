#!/bin/bash

#sudo usermod -aG docker $USER && newgrp docker

#sudo groupadd docker
#sudo usermod -aG docker $USER

if [[ $(which minikube) && $(minikube version) ]]; then
         echo "minikube is installed, starting minikube"
     else
         echo"install minikube using install-minikube.sh file"
         echo
fi

#dockerd-rootless-setuptool.sh install -f
#docker context use rootless
#minikube start --driver=docker --container-runtime=containerd
#sudo groupadd docker
minikube start --driver=docker
#sudo usermod -aG docker $USER
#sudo minikube start --vm-driver=docker 
#sudo /usr/local/bin/minikube --vm-driver=none --bootstrapper=localkube start
#minikube start --driver=docker --container-runtime=containerd
#sudo minikube start
