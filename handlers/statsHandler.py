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


import os, signal, sys, platform

from tornado import web, ioloop, iostream, gen, httpclient
sys.path.append(r'./');

# pure websocket implementation
from tornado import websocket

from weioLib import weioTopStats
from weioLib import weioUnblock
from weioLib import weioIO


import functools
import json
import hashlib
import tarfile

clients = set()

# For shared variables between handlers
from weioLib.weioUserApi import *

# Wifi detection route handler
class WeioStatsHandler(websocket.WebSocketHandler):
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

            temperature = int(weioIO.getTemperature())

            # test only ...
            dd = random.randint(1, 99)
            rr = 100-dd

            cpu = { "user" : cpuUser, "system" : cpuSystem, "idle" : cpuIdle}
            ram = { "free" : freeRam, "used": usedRam }
            flash = { "free" : dd, "used":rr }

            data['requested'] = rq
            data['data'] = {"cpu" : cpu, "ram" : ram, "flash" : flash, "temperature": temperature}

        else :

            cpuRamData = weioTopStats.getTop()
            flashData = weioTopStats.getSpaceUsage("/")
            temperature = int(weioIO.getTemperature())

            data['requested'] = rq
            data['data'] = {"cpu" : cpuRamData["cpu"], "ram" : cpuRamData["mem"], "flash" : flashData, "temperature": temperature}

        self.broadcast(clients, json.dumps(data))

    def getTopOnce(self, data) :
        self.getData('getTop')

    def stopTop(self, rq):
        # stop periodic calls
        self.periodic.stop()

        if (rq is not None):
            data = {}
            data['requested'] = rq['request']
            self.broadcast(clients, json.dumps(data))
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

    def open(self) :
        self.periodic = ioloop.PeriodicCallback(self.getData, self.cadence)
        global clients
        clients.add(self)

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

    def broadcast(self, connectedClients, data):
        for c in connectedClients:
            c.write_message(data)

    def on_close(self) :
        global clients
        # Remove client from the clients list and broadcast leave message
        clients.remove(self)

        print("socket closed")
        self.stopTop(None)

