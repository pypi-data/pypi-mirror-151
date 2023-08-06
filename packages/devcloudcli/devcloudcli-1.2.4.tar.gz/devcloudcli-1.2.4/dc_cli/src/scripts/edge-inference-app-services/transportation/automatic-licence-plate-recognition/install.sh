#!/bin/bash



echo "Installing automatic-licence-plate-recognition ..."
pip3 install --upgrade pip && pip3 install edgesoftware
echo fe86f27f-7ec8-4550-a964-be67d3d895b5 | $HOME/.local/bin/edgesoftware install automatic-licence-plate-recognition 61f38cca14e68bcc9220ccb8
