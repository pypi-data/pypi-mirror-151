#!/bin/bash



echo "Installing edge-insights-for-fleet ..."
pip3 install edgesoftware
sudo mkdir edge-insights-for-fleet
cd edge-insights-for-fleet
echo ecac9ea2-9ba2-4996-aeda-9c60d9e213f0 | $HOME/.local/bin/edgesoftware install edge-insights-for-fleet 623c98c39654a8f4bd94fa4b
