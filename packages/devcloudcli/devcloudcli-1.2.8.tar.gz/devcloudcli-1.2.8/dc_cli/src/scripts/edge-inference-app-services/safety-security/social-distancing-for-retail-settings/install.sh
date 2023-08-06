#!/bin/bash



echo "Installing social-distancing-for-retail-settings ..."
pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 0bc6f800-f667-464d-af07-9ad7fc03606b | $HOME/.local/bin/edgesoftware install social-distancing-for-retail-settings 627a09c506338088f3910d81

