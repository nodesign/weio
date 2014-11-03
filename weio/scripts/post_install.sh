#!/bin/sh
echo "This is WeIO post install procedure"
# Getting backup configuration file from /tmp and storing back to /weio directory
cp /tmp/config.weio /weio

#cd /
#cp /weio/scripts/weio_run.sh .
#pkill -f "./weio_run.sh"
#pkill -f "python server.py"
#./weio_run.sh&
