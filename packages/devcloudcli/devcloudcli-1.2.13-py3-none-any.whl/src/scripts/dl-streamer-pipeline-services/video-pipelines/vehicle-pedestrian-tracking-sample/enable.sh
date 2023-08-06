#!/bin/bash
INTEL_OPENVINO_DIR=/opt/intel/openvino_2021
#INPUT_VIDEO=$PWD/../face-demographics-walking-and-pause.mp4
INPUT_VIDEO=https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4
SINK_ELEMENT=fps
DEVICE=CPU
TRACKING_TYPE=short-term
DETECTION_INTERVAL=10
echo $SINK_ELEMENT
echo $INPUT_VIDEO
echo $TRACKING_TYPE

DIR=$PWD/dlstreamer

if [ -d "$DIR" ]; then
    echo "Success"
    source $INTEL_OPENVINO_DIR/bin/setupvars.sh
    export MODELS_PATH=$PWD/..
    cd $DIR/samples/gst_launch/vehicle_pedestrian_tracking/
    ./vehicle_pedestrian_tracking.sh $INPUT_VIDEO $DETECTION_INTERVAL $DEVICE $SINK_ELEMENT $TRACKING_TYPE
    #./vehicle_pedestrian_tracking.sh
else
    echo " Error: ${DIR} not found. Please run installation script."
fi
