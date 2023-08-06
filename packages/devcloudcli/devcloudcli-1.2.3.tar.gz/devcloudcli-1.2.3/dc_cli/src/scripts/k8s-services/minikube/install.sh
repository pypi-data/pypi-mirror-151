#!/bin/bash

#sudo apt-get update -y
#sudo apt-get upgrade -y

sudo apt-get install curl
echo "installing curl"
sudo apt-get install apt-transport-https
#sudo docker -v

if [[ $(which docker) && $(docker --version) ]]; then
         echo "Dockerce is present in the system"
     else
         echo "Install docker from devtool"
#curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
#sudo install minikube-linux-amd64 /usr/local/bin/minikube
fi
if [[ $(which minikube) && $(minikube version) ]]; then
	 echo "minikube is present in the system"
     else
	 echo "installing minikube" 	 
	 curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
         sudo install minikube-linux-amd64 /usr/local/bin/minikube
#	 sudo usermod -aG docker $USER && newgrp docker
fi

#sudo usermod -aG docker $USER && newgrp docker





#read -p "start minikube? " -n 1 -r
#echo    # (optional) move to a new line
#if [[ ! $REPLY = ^[Yy]$ ]]
#then
    #sudo usermod -aG docker $USER && newgrp docker
#    echo"starting minikube"
#    minikube start --driver=docker
#fi
~



#sudo apt install virtualbox virtualbox-ext-pack -y --accept-license
#echo yes
#wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
#sudo cp minikube-linux-amd64 /usr/local/bin/minikube
