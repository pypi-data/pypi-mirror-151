#!/bin/bash


if [[ $(pip3 show openvino-dev) ]]; then
         echo "openvino-dev is installed"
     else
         echo "Installing openvino-dev to download the models"
         sudo  pip3 install openvino-dev==2021.4.2
fi

omz_downloader --name face-detection-retail-0005
echo "model is downloaded under the intel folder"
