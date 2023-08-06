#!/bin/bash



echo "Installing interactive-kiosk-ai-chatbot ..."
pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo 6b90d312-0969-45b6-be28-6f6ac8873d9e | $HOME/.local/bin/edgesoftware install interactive-kiosk-ai-chatbot 62443d3a9654a8f4bd9cbca6

