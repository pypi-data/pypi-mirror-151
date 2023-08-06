#!/bin/bash

echo "checking for docker installation"
if [[ $(which docker) && $(docker --version) ]]; then
         echo "Dockerce is present in the system"
     else
	 echo "Install docker from devtool"
   fi

echo "checking for the pip installation"
if [[ $(which pip) && $(pip --version) ]]; then
         echo "pip is installed in the system"
     else
         echo "Install pip-package"
	 sudo apt update
	 sudo apt install python3-pip -y
   fi

echo "checking for docker installation"
if [[ $(which docker) && $(docker --version) ]]; then
         echo "Dockerce is present in the system"
     else
         echo "Install docker from devtool"
   fi

#python3 -m pip install -U openvino-workbench
sudo docker pull openvino/workbench:2021.4.2
