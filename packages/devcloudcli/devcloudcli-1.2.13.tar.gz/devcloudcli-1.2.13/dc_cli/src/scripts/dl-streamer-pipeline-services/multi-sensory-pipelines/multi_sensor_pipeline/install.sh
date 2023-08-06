#!/bin/bash

cd ~
DIR=$PWD/multi_sensor_sample
if [ -d "$DIR" ]; then
        echo "Success"
else
	sudo pip3 install gdown
	gdown --folder https://drive.google.com/drive/folders/1iSEjiRlYlTbuEgTb10T76f9y6aLbtavz --output $DIR
	echo "Successfully installed"
fi

