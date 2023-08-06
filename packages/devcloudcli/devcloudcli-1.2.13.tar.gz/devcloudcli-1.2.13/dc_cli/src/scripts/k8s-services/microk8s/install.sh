#!/bin/bash

if [[ $(which docker) && $(docker --version) ]]; then
         echo "Docker is installed "
     else
         echo "Install docker from devtool"
         # command
         #sudo apt-get remove docker docker-engine docker.io containerd runc
fi

#install microk8s
if [[ $(which microk8s) && $(sudo microk8s ctr version) ]]; then
         echo "Microk8s is installed"
     else
         echo "installing microk8s ....."
	 echo
	 #sudo snap set system proxy.http=
	 #sudo snap set system proxy.https=
	 sudo apt install snapd 
         sudo snap install microk8s --classic --channel=1.21
	 sudo usermod -a -G microk8s $USER
         sudo chown -f -R $USER ~/.kube
	 echo "intel123" | sudo -S sleep 1 && sudo su $USER
	 
         #sudo ufw allow in on cni0 && sudo ufw allow out on cni0
         #sudo ufw default allow routed
fi


#start the service
#sudo microk8s kubectl get all --all-namespaces
