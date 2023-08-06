#!/bin/bash

INTEL_OPENVINO_DIR=/opt/intel/openvino_2021
MODEL_PATH=$PWD/..
DIR=$PWD/dlstreamer
if [ -d "$DIR" ]; then
        echo "Success"
else
    git clone https://github.com/dlstreamer/dlstreamer.git
fi
export INTEL_OPENVINO_DIR=$INTEL_OPENVINO_DIR
export MODELS_PATH=$MODEL_PATH
pip3 install numpy networkx onnx
pip3 install -r $INTEL_OPENVINO_DIR/deployment_tools/open_model_zoo/tools/downloader/requirements.in
cd $DIR/samples
sh ./download_models.sh

