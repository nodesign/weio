#!/bin/sh
echo "This is WeIO post install procedure"
# migrating old config file to the new one
cd /weio/scripts/
./migrateConfig.py
cd /weio
rm /tmp/config.weio

