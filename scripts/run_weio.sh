#!/bin/sh
### 
#
# WEIO Web Of Things Platform
# Copyright (C) 2013 Nodesign.net, Uros PETREVSKI, Drasko DRASKOVIC
# All rights reserved
#
#               ##      ## ######## ####  #######  
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ######    ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#                ###  ###  ######## ####  #######
#
#                    Web Of Things Platform 
#
# This file is part of WEIO and is published under BSD license.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by the WeIO project.
# 4. Neither the name of the WeIO nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY WEIO PROJECT AUTHORS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL WEIO PROJECT AUTHORS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###


# Launching WeIO application, if application crashes WeIO will rerun automaticaly
# On each exit from application script checks if an update is needed
# Update process once decompressed new version to RAM exits application, script will
# do the rest of moving files to good target

WIFI_READY=0

# Function to check wifi state
check_wifi()
{
    DELAY=5
    COUNTER=0
        
    # Wait for WiFi interface to appear
    while [ ! -e /sys/class/net/wlan0/operstate ]; do
        # WiFi is still down. Wait a bit.
        sleep 1
        COUNTER=`expr $COUNTER + 1`
        if [ $COUNTER -ge $DELAY ]; then
           echo "WiFi interface is DOWN"
           return
        fi
    done
    
    # Reset counter
    COUNTER=0
    while [  $COUNTER -lt $DELAY ]; do
    	OPERSTATE=`cat /sys/class/net/wlan0/operstate`
        if [ "$OPERSTATE" != "up" ]; then
            echo "WiFi is $OPERSTATE. Waiting..."
            sleep 1
            COUNTER=`expr $COUNTER + 1`
        else
            break
        fi
    done

    if [ $COUNTER -ge $DELAY ]; then
        WIFI_READY=0
    else
    	echo "WiFi is READY"
        WIFI_READY=1
    fi
}


###
# Loop forever - restart WeIO if it exits
###
cd /weio

# If led_blink is not running - start it
if [ -z "$(ps | grep  "[l]edBlink.py")" ]; then
    echo "Starting ledBlink.py..."
    /etc/init.d/led_blink start
fi

# First check if WiFi is UP
check_wifi

while [ $WIFI_READY -ne 1 ]; do
    echo "WiFi network is not ready. Switching to RESCUE mode."

    # We did not connect even after whole delay expired
    # Something went wrong - got to RESCUE
    /weio/scripts/wifi_set_mode.sh rescue

    # Re-check WiFi
    check_wifi
done

# Restart avahi
# First kill it
avahi-daemon -k
# The daemonize it
avahi-daemon -D

if grep -q '"first_time_run": "YES"' /weio/config.weio
then
    echo "===> FLASHING LPC FIRMWARE"
    /weio/scripts/flash_lpc_fw.py
    echo "===> RETREIVING BACKUP IF EXISTS"
    if [ -d "/weioUserBackup" ]; then

        # migrating old config file to the new one
        cd /weio/scripts/
        # at this moment old config.weio is here : /weioUserBackup/config.weio
        ./migrateConfig.py

        # destroy old config.weio
        rm /weioUserBackup/config.weio

        # Bringing back user projects
        rm -rf /weioUser/flash
        mv /weioUserBackup /weioUser/flash

        # Be sure that after this step we are no more in the "first time" mode
        sed 's/"first_time_run": "YES",.*$/"first_time_run": "NO",/' -i config.weio
    fi
fi

echo "===> STARTING THE SERVER"

# And start WeIO
./weioServer.py > /dev/null

### WE HAVE EXITED SERVER - CHECK OUT WHY ###
echo "===> EXITED SERVER"
    
if grep -q '"kill_flag": "YES"' /weio/config.weio
then
    echo "Found kill flag"

    if [ -d "/tmp/weio" ]; then
      echo "Running pre install procedure"
      sh /tmp/weio/scripts/pre_install.sh
      # echo "Deleting old WeIO"
      # rm -r /weio
      # echo "Moving from RAM to target place new WeIO"
      # mv /tmp/weio /weio
      # echo "Running post install procedure"
      # sh /weio/scripts/post_install.sh
      # echo "Installation done!"
    fi
fi

# And here we go again!
/etc/init.d/weio_run restart
