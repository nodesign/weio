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
###


BUILD_DIR=$PWD

# Clean Carambola2 SDK
make clean distclean

# Get WeIO
git clone https://github.com/nodesign/weio.git

# Copy WeIO image files
cp -r weio/openWrt/files .

# Get the newest WeIO verion into the `files`
cd weio/productionScripts/
./stripMe.sh
cd $BUILD_DIR
tar -xzvf weio/productionScripts/weio.tar.gz -C files/

# Get installed Python libraries for Carambola and extract them to files (/usr directory)
wget http://www.we-io.net/downloads/weioImage/weioLibs.tar.gz
tar -xzvf weioLibs.tar.gz -C files/
rm weioLibs.tar.gz

# Install needed packages for WeIO
cp weio/openWrt/pkg_install.sh .
./pkg_install.sh

# Copy configuration
cp weio/openWrt/weio-config-carambola2 .config

# Build
echo "Now you can build the image by running: make -j 4"


