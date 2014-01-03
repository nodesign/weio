#!/bin/sh

# Launching WeIO application, if application crashes WeIO will rerun automaticaly
# On each exit from application script checks if an update is needed
# Update process once decompressed new version to RAM exits application, script will
# do the rest of moving files to good target
while true; 
do
    # Check if there is any orphan (user program) and kill it before starting new server
    
    if [ -n "$(ps | grep  "[w]eioRunner.py")" ]; then
           echo "Stopping user program weioRunner.py..."
           killall weioRunner.py
    fi
       
    sh /weio/userProjectsLinking.sh
    cd /weio
    ./weioServer.py;
        
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
    
