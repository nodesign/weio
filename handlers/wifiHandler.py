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

from tornado import web, ioloop, iostream, gen
sys.path.append(r'./');

# pure websocket implementation
#from tornado import websocket

from sockjs.tornado import SockJSRouter, SockJSConnection

from weioLib import weioFiles
from weioLib import weio_config

import functools

import json

# Wifi detection and configuration module
from weioWifi import weioWifi

# Global weioWifi object
wifi = weioWifi.WeioWifi("wlan0")

def weioWifiParseScan() :
    global wifi

    scaninfo = wifi.scan()

    data = {}

    for cell in  scaninfo.keys() :
        s = {}
        s['mac'] = scaninfo[cell]['MAC']
        s['essid'] = scaninfo[cell]['ESSID']
        s['quality'] = scaninfo[cell]['Quality']
        s['encryption'] = scaninfo[cell]['Encryption']
        if (s['encryption'] == 'none') :
            s['opened'] = True
        else :
            s['opened'] = False

        s['mode'] = scaninfo[cell]['Mode']

        if (wifi.mode != 'ap'):
            # Check if we are connected to this ESSID
            if (scaninfo[cell]['ESSID'] == wifi.essid) :
                s['connected'] = True
            else :
                s['connected'] = False
        
        # Placeholeder for client to fill
        s['passwd'] = None

        data[cell] = s

    return data


# Wifi detection route handler  
class WeioWifiHandler(SockJSConnection):
    global wifi
    global callbacks
    
    def scanCells(self, rq):
        if (platform.machine() == 'mips') :
            """We have obtained essid, psswd and encryption
            so we can try to connect"""
            data = {}
            data = weioWifiParseScan()
            
            # Send response to the browser
            rsp={}
            rsp['requested'] = rq['request']
            rsp['data'] = data

            # Send connection information to the client
            self.send(json.dumps(rsp))
        else :
            # send test file
            testString = {'02': {'opened': False, 'passwd': None, 'encryption': 'mixed WPA/WPA2 PSK (TKIP, CCMP)', 'mac': '00:05:59:1F:D2:F0', 'connected': False, 'mode': 'Master', 'quality': '28/70', 'essid': 'jetSpeed IAD 2 (PSTN)'}, '03': {'opened': False, 'passwd': None, 'encryption': 'mixed WPA/WPA2 PSK (TKIP, CCMP)', 'mac': 'F8:D1:11:A0:03:88', 'connected': False, 'mode': 'Master', 'quality': '24/70', 'essid': 'DeepNetPocket'}, '01': {'opened': False, 'passwd': None, 'encryption': 'WPA PSK (TKIP, CCMP)', 'mac': '94:0C:6D:FA:1B:EA', 'connected': True, 'mode': 'Master', 'quality': '70/70', 'essid': 'BECA'}, '06': {'opened': False, 'passwd': None, 'encryption': 'mixed WPA/WPA2 PSK (CCMP)', 'mac': '90:F6:52:24:CF:26', 'connected': False, 'mode': 'Master', 'quality': '19/70', 'essid': 'Pavlovici'}, '04': {'opened': False, 'passwd': None, 'encryption': 'mixed WPA/WPA2 PSK (TKIP)', 'mac': 'E8:39:DF:7B:BB:1C', 'connected': False, 'mode': 'Master', 'quality': '19/70', 'essid': 'KAPIS'}, '05': {'opened': False, 'passwd': None, 'encryption': 'mixed WPA/WPA2 PSK (TKIP, CCMP)', 'mac': '70:54:D2:46:98:53', 'connected': False, 'mode': 'Master', 'quality': '21/70', 'essid': 'petra'}}
            
            # Send response to the browser
            rsp={}
            rsp['requested'] = rq['request']
            rsp['data'] = testString

            # Send connection information to the client
            self.send(json.dumps(rsp))
    
    def goToApMode(self,rq):
        if (platform.machine() == 'mips') :
            wifi.essid =  rq['data']['essid']
            wifi.setConnection("ap")
        
    def goToStaMode(self,rq):
        if (platform.machine() == 'mips') :
            wifi.essid = rq['data']['essid']
            wifi.passwd = rq['data']['passwd']
            wifi.rawEncryption = rq['data']['encryption']

            # Parse rawEncryption (iwinfo format) to OpenWRT format
            if ('WPA2' in wifi.rawEncryption):
                if ('mixed' in wifi.rawEncryption):
                    wifi.encryption = 'mixed-psk'
                else:
                    wifi.encryption = 'psk2'
            elif ('WPA' in wifi.rawEncryption):
                wifi.encryption = 'psk'

            if ('TKIP' in wifi.rawEncryption):
                wifi.encryption = wifi.encryption + "+tkip"
                if ('CCMP' in wifi.rawEncryption):
                    wifi.encryption = wifi.encryption + "+ccmp"
            elif ('CCMP' in wifi.rawEncryption):
                wifi.encryption = wifi.encryption + "+ccmp"
                
            wifi.setConnection("sta")
            
            data = {}
            # Check if everything went well, or go to AP mode in case of error
            wifi.checkConnection()
            data['mode'] = wifi.mode
            
            # Send response to the browser
            rsp={}
            rsp['requested'] = rq['request']
            rsp['data'] = data

            # Send connection information to the client
            self.send(json.dumps(rsp))
        

    #########################################################################
    # DEFINE CALLBACKS IN DICTIONARY
    # Second, associate key with right function to be called
    # key is comming from socket and call associated function
    callbacks = {
        'scan' : scanCells,
        'goAp' : goToApMode,
        'goSta' : goToStaMode,
    }   

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
        # Call callback by key directly from socket
        global callbacks
        request = rq['request']

        if request in callbacks :
            callbacks[request](self, rq)
        else :
            print "unrecognised request"
