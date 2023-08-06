#!/bin/bash



echo "Installing edge-insights-for-amr ..."

pip3 install --upgrade pip --user && pip3 install edgesoftware --user
echo a5c27c74-f62b-4e82-b5f6-ada10d6eca51 | $HOME/.local/bin/edgesoftware install edge-insights-for-amr 625d53879654a8f4bd167b12


