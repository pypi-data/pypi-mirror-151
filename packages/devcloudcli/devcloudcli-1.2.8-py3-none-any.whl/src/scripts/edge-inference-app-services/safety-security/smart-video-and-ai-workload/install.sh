#!/bin/bash



echo "Installing smart-video-and-ai-workload ..."
pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo a97926d8-4df0-421a-9579-50c783482051 | $HOME/.local/bin/edgesoftware install smart-video-and-ai-workload 61b0b5a6d8ecccee55ba2d84

