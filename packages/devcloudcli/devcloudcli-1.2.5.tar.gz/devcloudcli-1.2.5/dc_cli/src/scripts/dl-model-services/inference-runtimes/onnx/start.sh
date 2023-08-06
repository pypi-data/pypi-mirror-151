#!/bin/bash

echo "entered into onnx  \

enter exit to come out of the onnx"

docker run -it --rm --device-cgroup-rule='c 189:* rmw' -v /dev/bus/usb:/dev/bus/usb openvino/onnxruntime_ep_ubuntu18:latest

#echo"the onnx is ready to useu" 

