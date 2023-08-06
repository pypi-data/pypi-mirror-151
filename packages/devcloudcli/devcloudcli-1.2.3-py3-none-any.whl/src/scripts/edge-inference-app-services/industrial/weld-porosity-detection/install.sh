#!/bin/bash



echo "Installing weld-porosity-detection ..."
pip3 install edgesoftware
sudo mkdir weld-porosity-detection
cd weld-porosity-detection
echo 967933fc-26ce-4efa-b674-92e32f59da87 | $HOME/.local/bin/edgesoftware install weld-porosity-detection 61717e49d8ecccee552d3ac6
