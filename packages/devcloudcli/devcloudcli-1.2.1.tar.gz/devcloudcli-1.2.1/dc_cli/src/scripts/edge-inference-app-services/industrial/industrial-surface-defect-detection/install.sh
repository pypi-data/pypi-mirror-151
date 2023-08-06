#!/bin/bash



echo "Installing industrial-surface-defect-detection ..."
pip3 install edgesoftware
sudo mkdir industrial-surface-defect-detection
cd industrial-surface-defect-detection
echo cdddcd7a-3269-40dc-a555-1275a2f30585 | $HOME/.local/bin/edgesoftware install industrial-surface-defect-detection 61706d8bd8ecccee5508e49d
