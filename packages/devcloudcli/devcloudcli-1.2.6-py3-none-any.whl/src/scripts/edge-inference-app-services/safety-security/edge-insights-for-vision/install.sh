#!/bin/bash



echo "Installing Edge Insights for Vision ..."
pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 9ca70972-ed84-4596-8054-58b3e995a01b | $HOME/.local/bin/edgesoftware install edge-insights-for-vision 619cdb49d8ecccee550fe4f6
