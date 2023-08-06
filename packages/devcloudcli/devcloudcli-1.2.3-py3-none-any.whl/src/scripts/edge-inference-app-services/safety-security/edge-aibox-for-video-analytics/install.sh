#!/bin/bash



echo "Installing edge-aibox-for-video-analytics  ..."
pip3 install edgesoftware
sudo mkdir edge-aibox-for-video-analytics
cd edge-aibox-for-video-analytics
echo 68b20936-6b88-4bc9-9fed-749b2d512ec3 | $HOME/.local/bin/edgesoftware install edge-aibox-for-video-analytics 6244acf19654a8f4bdabc030

