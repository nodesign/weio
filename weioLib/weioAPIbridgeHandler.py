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

# -*- coding: utf-8 -*-
import subprocess
import os, signal

from tornado import web, ioloop, iostream

from sockjs.tornado import SockJSRouter, SockJSConnection
import json


from weioLib import weio_gpio
from weioLib import weio_globals


class WeioAPIBridgeHandler(SockJSConnection):

    """Opens editor route."""
    def on_open(self, data):
        """On open asks weio for last saved project. List of files are scaned and sent to editor.
        Only contents of weio_main.py is sent at first time"""
        print "Opened WEIO API socket"

    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        req = json.loads(data)
        self.serve(req)

    def serve(self, rq) :


        if 'digitalWrite' in rq['request'] :

            ins = rq['data']
            weio_gpio.digitalWrite(str(ins[0]), str(ins[1]))
            #print ins

        elif 'pinMode' in rq['request'] :
            ins = rq['data']
            weio_gpio.digitalWrite(ins[0], ins[1])

