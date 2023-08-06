#!/bin/sh
l_AIKit_p_2022.1.2.135.sh -s -a --list-products
cd /opt/intel/oneapi/installer
sudo ./installer --action remove --product-id intel.oneapi.lin.tbb.product --product-ver 2021.1.1-129
