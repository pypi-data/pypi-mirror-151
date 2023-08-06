#!/bin/bash



echo "Installing brain-tumor-segmentation ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo c4ca3793-5316-492c-8c53-bf4266799781 | $HOME/.local/bin/edgesoftware install brain-tumor-segmentation 617b9f97d8ecccee55878c24
