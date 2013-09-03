#!/bin/bash

###
# This is the script that installs WeIO
# into Carambola2 OpenWRT Buildroot SDK.
#
# Usage: place the script into Carambola2 SDK root dir
# and run it.
#
# The script will:
#   - Clone WeIO from GitHub
#   - Copy needed files from it
#   - Install Carambola2 OpenWRT packages needed for WeIO
#   - Copy appropriate configuration for WeIO
#
# Usage:    Either supply weio dir as the first argument,
#           or it will be cloned from GitHub
###


BUILD_DIR=$PWD

if [ $# -eq 0 ]
  then
    # No local WeIO dir supplied, get WeIO from GitHub
    git clone https://github.com/nodesign/weio.git
    WEIO=weio
else
    WEIO=$1
fi

# Clean Carambola2 SDK
make clean distclean

# Copy WeIO image files
cp -r $WEIO/openWrt/files .

# Get the newest WeIO verion into the `files`
cd $WEIO/productionScripts/
./stripMe.sh
cd $BUILD_DIR
tar -xzvf $WEIO/productionScripts/weio.tar.gz -C files/

# Setting first time run flag
python $WEIO/openWrt/firstTimeFlag.py files/weio/config.weio

# Install needed packages for WeIO
cp $WEIO/openWrt/pkg_install.sh .
./pkg_install.sh

# Copy Carambola configuration file
cp $WEIO/openWrt/weio-config-carambola2 .config

# Build
echo ""
echo "Now you can build the image by running: make -j 4"


