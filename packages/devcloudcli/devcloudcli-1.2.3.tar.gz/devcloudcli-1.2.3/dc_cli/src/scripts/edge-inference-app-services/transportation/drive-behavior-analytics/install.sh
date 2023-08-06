#!/bin/bash



echo "Installing drive-behavior-analytics ..."
pip3 install edgesoftware
sudo mkdir drive-behavior-analytics
cd drive-behavior-analytics
echo 35aaed01-8674-44ed-a865-834183abff3c | $HOME/.local/bin/edgesoftware install drive-behavior-analytics 61bc69a8d8ecccee555fc0fa

