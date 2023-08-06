#!/bin/bash

if [[ $(docker ps -q -f name=workbench) || $(docker ps -aq -f status=exited -f name=workbench) ]];then
       docker rm -f  workbench
fi

