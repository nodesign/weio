#!/bin/sh

# Launching WeIO application, if application crashes WeIO will rerun automaticaly
# On each exit from application script checks if an update is needed
# Update process once decompressed new version to RAM exits application, script will
# do the rest of moving files to good target
while true; 
do
    cd /weio
    # restart avahi in every case
    avahi-daemon -k
    avahi-daemon -D
    # export AP and STA LEDs
    if [ -f "/sys/class/gpio/gpio23/value" ]
    then
        echo "gpio 23 declared"
    else
        echo 23 > /sys/class/gpio/export
    fi

    if [ -f "/sys/class/gpio/gpio22/value" ]
    then
        echo "gpio 22 declared"
    else
        echo 22 > /sys/class/gpio/export
    fi

    echo in > /sys/class/gpio/gpio23/direction
    echo in > /sys/class/gpio/gpio22/direction
    python server.py;
        
    if grep -q '"kill_flag": "YES"' /weio/config.weio
    then
        echo "Found kill flag"
    
        if [ -d "/tmp/weio" ]; then
          echo "Running pre install procedure"
          sh /tmp/weio/scripts/pre_install.sh
          echo "Deleting old WeIO"
          rm -r /weio
          echo "Moving from RAM to target place new WeIO"
          mv /tmp/weio /weio
          echo "Running post install procedure"
          sh /weio/scripts/post_install.sh
          echo "Installation done!"
        fi
    fi
      
done
    
