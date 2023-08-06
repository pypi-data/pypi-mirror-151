#!/bin/bash



echo "Installing cargo-management ..."
pip3 install edgesoftware
sudo mkdir cargo-management
cd cargo-management
echo 548eba24-4079-47cb-8d89-db324668e301 | $HOME/.local/bin/edgesoftware install cargo-management 61bc6972d8ecccee555fb963
