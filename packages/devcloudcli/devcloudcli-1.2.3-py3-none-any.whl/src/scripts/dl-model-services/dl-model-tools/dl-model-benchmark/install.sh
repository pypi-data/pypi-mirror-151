#!/bin/bash

if !(git clone -b 2022.1.0 https://github.com/openvinotoolkit/openvino.git) then
   exit 1
   echo " git is failing check with version or with the git link"
else
    echo "Success"
    cd openvino/tools/
    python3 -m pip install benchmark_tool/
    echo " benchmark-tool installed"
    
fi

