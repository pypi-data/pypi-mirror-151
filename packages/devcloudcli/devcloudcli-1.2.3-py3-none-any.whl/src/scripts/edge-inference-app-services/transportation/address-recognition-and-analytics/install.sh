#!/bin/bash



echo "Installing address-recognition-and-analytics ..."
pip3 install edgesoftware
sudo mkdir address-recognition-and-analytics
cd address-recognition-and-analytics
echo adef950e-77fd-4dfb-8c50-2defa5aadb05 | $HOME/.local/bin/edgesoftware install address-recognition-and-analytics 623d8c0c9654a8f4bdb5ac8a
