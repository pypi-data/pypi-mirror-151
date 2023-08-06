#!/bin/bash



echo "Installing automated-checkout ..."
pip3 install edgesoftware
sudo mkdir automated-checkout 
cd automated-checkout 
echo 1b5170bb-4ec2-4333-9593-f622df6ae81e | $HOME/.local/bin/edgesoftware install automated-checkout 61711879d8ecccee551f842b
