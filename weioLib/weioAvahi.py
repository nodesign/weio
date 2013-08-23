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

import os, subprocess

global pathToAvahi

pathToAvahi = "/etc/avahi/"

def setAvahiName(newName) :
    """Setting Avahi daemon name in configuration file.
        Use resetAvahiDaemon to apply changes."""
    global pathToAvahi
    inputFile = open(pathToAvahi+"avahi-daemon.conf", 'r')
    rawData = inputFile.read()
    inputFile.close()
    
    lines = rawData.splitlines()
    for l in lines :
        if ("host-name=" in l) :
            lines[lines.index(l)] = "host-name="+newName
            break
    
    inputFile = open(pathToAvahi+"avahi-daemon.conf", 'w')
    inputFile.write('\n'.join(lines))
    inputFile.close()

def getAvahiName():
    global pathToAvahi
    """Getting current Avahi name from configuration file."""
    inputFile = open(pathToAvahi+"avahi-daemon.conf", 'r')
    rawData = inputFile.read()
    inputFile.close()
    
    lines = rawData.splitlines()
    for l in lines :
        if ("host-name=" in l) :
            name = l.split("host-name=")
            return name[1]

def resetAvahiDeamon():
    """Kill and reset Avahi daemon"""
    subprocess.check_output("avahi-daemon -k", shell=True)
    subprocess.check_output("avahi-daemon -D", shell=True)