#!/bin/bash
DIR=$PWD/dlstreamer

if [ -d "$DIR" ]; then
	cd $DIR
	source "/opt/intel/openvino_2021/bin/setupvars.sh"
        gst-launch-1.0 filesrc location=../sample-videos/classroom.mp4 ! decodebin ! videoconvert ! gvadetect model=../intel/face-detection-adas-0001/FP16/face-detection-adas-0001.xml ! gvaclassify model=../intel/emotions-recognition-retail-0003/FP16/emotions-recognition-retail-0003.xml model-proc=samples/gst_launch/metapublish/model_proc/emotions-recognition-retail-0003.json ! gvawatermark ! autovideosink sync=false
else
         echo "Folder doesnot exist. Please install the package first."
         
fi

