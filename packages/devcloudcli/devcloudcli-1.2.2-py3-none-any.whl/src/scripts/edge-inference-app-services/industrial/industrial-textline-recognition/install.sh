#!/bin/bash



echo "Installing industrial-textline-recognition ..."
pip3 install edgesoftware
sudo mkdir industrial-textline-recognition
cd industrial-textline-recognition
echo 7ef58969-f6ef-49f0-8439-cdb7f782485c | $HOME/.local/bin/edgesoftware install industrial-textline-recognition 61703884d8ecccee5501e4b8
