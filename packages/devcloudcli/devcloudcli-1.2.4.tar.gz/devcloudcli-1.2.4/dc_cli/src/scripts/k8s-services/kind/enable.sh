#!/bin/bash

if [[ $(which kind) && $(sudo kind -- version) ]]; then
         echo "kind is installed, starting kind single-node cluster"
	 echo
	 kind create cluster
     else
         echo "install kind using install-kind.sh file"
         
fi


