#!/bin/bash



echo "Installing workzone-analytics ..."
pip3 install edgesoftware
sudo mkdir workzone-analytics
cd workzone-analytics
echo 83603d3e-f16f-42dc-bfea-62aec06aaced | $HOME/.local/bin/edgesoftware install workzone-analytics 623d8ced9654a8f4bdb5ca20
