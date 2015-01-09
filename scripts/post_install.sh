#!/bin/sh
echo "This is WeIO post install procedure"

# migrating old config file to the new one
cd /weio/scripts/
./migrateConfig.py
cd /weio
rm /tmp/config.weio

# flashing new firmware to LPC chip
cd /weio/scripts/
./flash_lpc_fw.py
cd /
