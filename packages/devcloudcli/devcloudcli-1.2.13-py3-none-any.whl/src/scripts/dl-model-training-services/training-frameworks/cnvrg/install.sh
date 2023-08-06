#!/bin/sh
sudo apt-get install
sudo apt-get update
sudo apt-get install -y ruby=2.5 ruby-dev libxslt-dev libxml2-dev zlib1g-dev shared-mime-info
ruby -v
gem install cnvrg
cnvrg --version
cnvrg --api '/api'
cnvrg login

