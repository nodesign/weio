#!/bin/sh
echo "This is WeIO pre install procedure"
# This will backup configuration file to /tmp directory and in post install procedure will copy back to /weio directory
# If any changements are required for config.weio they have to be done here in this script
cp /weio/config.weio /tmp