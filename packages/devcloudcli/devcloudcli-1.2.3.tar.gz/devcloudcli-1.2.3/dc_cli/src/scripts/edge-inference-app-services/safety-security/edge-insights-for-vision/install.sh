#!/bin/bash



echo "Installing Edge Insights for Vision ..."
pip3 install edgesoftware
sudo mkdir edge-insights-for-vision 
cd edge-insights-for-vision 
echo 9ca70972-ed84-4596-8054-58b3e995a01b | $HOME/.local/bin/edgesoftware install edge-insights-for-vision 619cdb49d8ecccee550fe4f6
