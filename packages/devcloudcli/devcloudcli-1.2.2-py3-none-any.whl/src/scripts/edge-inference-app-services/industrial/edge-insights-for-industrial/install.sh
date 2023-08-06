#!/bin/bash



echo "Installing edge-insights-for-industrial ..."
pip3 install edgesoftware
sudo mkdir edge-insights-for-industrial
cd edge-insights-for-industrial 
echo 196cc5ee-e133-4b1a-b6c7-fda621e1bc17 | $HOME/.local/bin/edgesoftware install edge-insights-for-industrial 6272959206338088f3910efe
