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

from tornado import web, ioloop, iostream, gen, httpclient
sys.path.append(r'./');

# pure websocket implementation
#from tornado import websocket

from sockjs.tornado import SockJSRouter, SockJSConnection

from weioLib import weioTopStats
from weioLib import weioUnblock


import functools
import json
import hashlib
import tarfile


# For shared variables between handlers
from weioLib.weioUserApi import *

# Wifi detection route handler  
class WeioStatsHandler(SockJSConnection):
    global callbacks
    
    # cadence for periodic sampling in millis
    cadence = 2000;
    
  
    def top(self, data) :
        self.periodic.start()
        
    ###
    # This function has to call shell top procedires
    # to determine cpu, flash and ram statistics
    # These are blocking calls and can block ioloop.
    # We assure that function is run in a separate thread with @unblock decorator.
    ###
    @weioUnblock.unblock
    def getData(self, rq='getTopPeriodic'):
        
        data = {}
        
        if (platform.machine() != "mips") :
            import random
            
            ramData = [['42820K', 'used'], ['18952K', 'free'], ['0K', 'shrd'], ['4164K', 'buff'], ['14744K', 'cached']]
            usedRam = float(ramData[0][0].split("K")[0])/1000.0
            usedRam = "%.1f" % usedRam
            
            freeRam = float(ramData[1][0].split("K")[0])/1000.0
            freeRam = "%.1f" % freeRam
            
            cpuData = [['CPU:', '18%', 'usr', '9%', 'sys', '0%', 'nic', '72%', 'idle', '0%', 'io', '0%', 'irq', '0%', 'sirq']]
            cpuUser = int(cpuData[0][1].split("%")[0])
            cpuSystem = int(cpuData[0][3].split("%")[0])
            cpuIdle = int(cpuData[0][7].split("%")[0])
            
            # test only ...
            dd = random.randint(1, 99)
            rr = 100-dd
        
            cpu = { "user" : cpuUser, "system" : cpuSystem, "idle" : cpuIdle}
            ram = { "free" : freeRam, "used": usedRam }
            flash = { "free" : dd, "used":rr }
            
            data['requested'] = rq
            data['data'] = {"cpu" : cpu, "ram" : ram, "flash" : flash}
        
        else :
            
            cpuRamData = weioTopStats.getTop()
            flashData = weioTopStats.getSpaceUsage("/")
            
            
            data['requested'] = rq
            data['data'] = {"cpu" : cpuRamData["cpu"], "ram" : cpuRamData["mem"], "flash" : flashData}
        
        self.send(json.dumps(data))

    def getTopOnce(self, data) :
        self.getData('getTop')
    
    def stopTop(self, rq): 
        # stop periodic calls
        self.periodic.stop()

        if (rq is not None):
            data = {}
            data['requested'] = rq['request']
            self.send(json.dumps(data))
        else:
            pass
    
    #########################################################################
    # DEFINE CALLBACKS IN DICTIONARY
    # Second, associate key with right function to be called
    # key is comming from socket and call associated function
    callbacks = {
        'getTopPeriodic' : top,
        'stopTopPeriodic' : stopTop,
        'getTop' : getTopOnce
    }   
    
    def on_open(self, info) :
        self.periodic = ioloop.PeriodicCallback(self.getData, self.cadence)

    
    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        req = json.loads(data)
        self.serve(req)
    
    def serve(self, rq):
        """Parsed input from browser ready to be served"""
        # Call callback by key directly from socket
        global callbacks
        request = rq['request']
        #print "REQUEST " + request 
        if request in callbacks :
            callbacks[request](self, rq)
        else :
            print "unrecognised request"

    def on_close(self) :
        print("socket closed")
        self.stopTop(None)
