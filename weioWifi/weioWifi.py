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
# This file is part of WEIO
# WEIO is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WEIO is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

import subprocess
import re
import shutil
import time

import sys, os, logging

import iwInfo

# IMPORT BASIC CONFIGURATION FILE ALL PATHS ARE DEFINED INSIDE
from weioLib import weio_config

logging.basicConfig()
log = logging.getLogger("WeioWifi")
log.setLevel(logging.DEBUG)

def weioCommand(command) :
    output = "PLACEHOLDER"

    print(str(command))

    try :
        output = subprocess.check_output(command, shell=True)
    except :
        print("Comand ERROR : " + str(output))
        output = "ERR_CMD"
	
    print output
    return output


class WeioWifi() :
    def __init__(self, interface):
        self.data = None
        self.interface = interface
        self.mode = None

        self.reconfTime = 10

        confFile = weio_config.getConfiguration()
        self.root = confFile['absolut_root_path']

    def checkConnection(self) :
        command = "iwconfig " + self.interface

        print "CHECK CONNECTION"

        status = weioCommand(command)

        print(str(status))
        # We are in STA mode, so check if we are connected
        if (status == "ERR_CMD") or "No such device" in status :
            # WiFi is DOWN
            print "Wifi is DOWN"
            self.mode = None
        # Check if wlan0 is in Master mode
        elif "Mode:Master" in status :
            print "AP Mode"
            self.mode = "ap"
            #self.essid = status.strip().startswith("ESSID:").split(':')[1]
        elif "Mode:Managed" in status :
            if "Access Point: Not-Associated" in status :
                self.mode = None
            else :
                self.mode = "sta"

        # We can not serve anything if we are not in sta or ap mode
        while (self.mode == None) :
            # Move to Master mode
            print "Trying to move to AP mode..."
            weioCommand("/weio/wifi_set_mode.sh ap")
            # Wait for network to reconfigure
            time.sleep(self.reconfTime)
            # Check what happened
            self.checkConnection()

        # Ath this point connection has been maid, and all we have to do is check ESSID
        for word in status.split(" ") :
            if word.startswith("ESSID") :
                self.essid = word.split('\"')[1]
                break

    def setConnection(self, mode) :
        """ First shut down the WiFi on Carambola """
        weioCommand("wifi down")

        if (mode is 'ap') :
            fname = "/etc/config/wireless.ap"
            shutil.copy(fname, "/etc/config/wireless")

            if (self.essid != ""):
                cmd = "sed 's/option ssid.*$/option ssid " + self.essid + "/' -i /etc/config/wireless"
                weioCommand(cmd)

            cmd = self.root + "/scripts/wifi_set_mode.sh ap"
            weioCommand(cmd)

        elif (mode is 'sta') :
            """ Change the /etc/config/wireless.sta : replace the params """
            fname = "/etc/config/wireless.sta"

            with open(fname) as f:
                out_fname = fname + ".tmp"
                out = open(out_fname, "w")
                for line in f:
                    line = re.sub(r'option\s+ssid\s.*$', r'option ssid ' + self.essid, line)
                    line = re.sub(r'option\s+key\s.*$', r'option key ' + self.passwd, line)
                    line = re.sub(r'option\s+encryption\s.*$', r'option encryption ' + self.encryption, line)
                    out.write(line)
                out.close()
                os.rename(out_fname, fname)
                shutil.copy(fname, "/etc/config/wireless")

            cmd = self.root + "/scripts/wifi_set_mode.sh sta"
            weioCommand(cmd)

    def scan(self) :
        iwi = iwInfo.IWInfo(self.interface)
        return iwi.getData()
