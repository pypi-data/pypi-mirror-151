#!/bin/bash
#INTEL_OPENVINO_DIR=/opt/intel/openvino_2021
#SINK_ELEMENT=fps
#DECODE_DEVICE=CPU
#INFERENCE_DEVICE=CPU
#CHANNELS_COUNT=1
USER=/home/intel

cd $USER
DIR=$PWD/pipeline-zoo
#INPUT_VIDEO=$PWD/sample-videos/people-detection.mp4
if [ -d "$DIR" ]; then
    echo "Success"
    sudo ./pipeline-zoo/tools/docker/run.sh
    echo "You have successfully lauched Pipeline zoo"
    echo "-- To list pipelines, run: pipebench list"
    echo "-- To download pipeline, run: pipebench download od-h264-ssd-mobilenet-v1-coco"
    echo "-- Measure Single Stream Throughput, run: pipebench run od-h264-ssd-mobilenet-v1-coco"
    echo "-- Measure Stream Density, run: pipebench run --measure density od-h264-ssd-mobilenet-v1-coco"
else
    echo " Error: ${DIR} not found. Please run installation script."
fi
