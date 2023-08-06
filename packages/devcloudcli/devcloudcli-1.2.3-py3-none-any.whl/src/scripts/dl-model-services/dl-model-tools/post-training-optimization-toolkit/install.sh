#!/bin/bash

#cd $PWD/models
if !(git clone -b 2022.1.0 https://github.com/openvinotoolkit/openvino.git) then
   exit 1
   echo " git is failing check with version or with the git link"
else
    echo "Success"
    cd openvino/tools/pot/
    python3 setup.py install
    echo "pot is installed"

fi

