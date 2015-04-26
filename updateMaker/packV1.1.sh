#!/bin/sh
mkdir V1.1
cd V1.1
mkdir weio
cd weio
mkdir scripts
cd scripts
cp ../../../../scripts/pre_install.sh .
cp ../../../../scripts/downloadFW.py .
cp ../../../../weioLib/weioConfig.py .
cd ../../
tar -zcvf weio.tar.gz weio/
echo "WeIO stripped and compressed has been created in directory V1.1"
rm -rf weio
python ../size.py .