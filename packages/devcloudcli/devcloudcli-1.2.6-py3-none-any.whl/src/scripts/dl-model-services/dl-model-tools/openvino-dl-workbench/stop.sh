#!/bin/bash

if [[ $(sudo docker ps -q -f name=workbench) || $(sudo docker ps -aq -f status=exited -f name=workbench) ]];then
       sudo docker rm -f  workbench
fi

