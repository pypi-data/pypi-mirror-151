#!/bin/bash 

echo "intel123" | sudo apt-get update
#sudo apt-get install -y jq

if (git clone -b 2022.1.0 https://github.com/openvinotoolkit/openvino.git); then
	exit 1
       echo " git is failing check with version or with the git link"
  else
    echo "Success"
    cd openvino/
    ./install_build_dependencies.sh
    echo"dependencies installed"
    cd ..
  fi

#wget -r -nH --cut-dirs=6 --no-parent --reject="index.html*"  https://github.com/openvinotoolkit/open_model_zoo/tree/master/models/$1/$2


#prerequisite_list=$(jq -r '.eval_configuration | with_entries(select(.value != false)) | keys[]' /home/intel/evalConfig.json)
#app_list=$(jq -r '.market_configuration | .market_title | .[]' /home/intel/evalConfig.json)


#echo ${prerequisite_list}
#echo ${app_list}
omz_downloader --name $1


