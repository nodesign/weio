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