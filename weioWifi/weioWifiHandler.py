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

import os, signal, sys, platform

from tornado import web, ioloop, iostream
sys.path.append(r'./');

# pure websocket implementation
#from tornado import websocket

from sockjs.tornado import SockJSRouter, SockJSConnection

from weioLib import weioFiles
from weioLib import weio_config

import functools

import json

# Wifi detection and configuration module
import weioWifi

# Global weioWifi object
wifi = weioWifi.WeioWifi("wlan0")


# Wifi detection route handler  
class WeioWifiHandler(SockJSConnection):
    def on_open(self, info) :
        msg = {}
        msg['mode'] = wifi.mode
        self.send(json.dumps(msg))

    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        req = json.loads(data)
        self.serve(req)
    
    def serve(self, rq):
        """Parsed input from browser ready to be served"""
        global wifi
        
        # We do WiFi setup __ONLY__ for WEIO machine. PC host should use it's OS tools.
        if (platform.machine() is 'mips') :
            """We have obtained essid, psswd and encryption
            so we can try to connect"""
            
            if 'scan' in rq['request'] :
                data = wifi.scan()
            else :
                if 'goAp' in rq['request'] :
                    wifi.setConnection("ap")
                elif 'goSta' in rq['request'] : 
                    wifi.essid = rq['data']['essid']
                    wifi.passwd = rq['data']['passwd']
                    wifi.encryption = rq['data']['encryption']
                    wifi.setConnection("sta")
                else :
                    print "WeioConnection() handler : UNKNOWN REQ"

                # Check if everything went well, or go to AP mode in case of error
                wifi.checkConnection()
                data['mode'] = wifi.mode
        
        print rq["request"]
        # Send response to the browser
        rsp={}
        rsp['requested'] = rq['request']
        rsp['data'] = "blabla"

        # Send connection information to the client
        self.send(json.dumps(rsp))
