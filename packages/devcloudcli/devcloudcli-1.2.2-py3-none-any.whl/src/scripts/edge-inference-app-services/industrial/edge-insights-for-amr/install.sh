#!/bin/bash



echo "Installing edge-insights-for-amr ..."
pip3 install edgesoftware
sudo mkdir edge-insights-for-amr
cd edge-insights-for-amr
echo a5c27c74-f62b-4e82-b5f6-ada10d6eca51 | $HOME/.local/bin/edgesoftware install edge-insights-for-amr 625d53879654a8f4bd167b12


