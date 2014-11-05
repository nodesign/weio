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

from os.path import isfile, join

from sockjs.tornado import SockJSRouter, SockJSConnection

import functools
import json
# IMPORT BASIC CONFIGURATION FILE
from weioLib import weioConfig

import subprocess
import platform

clients = set()

class WeioSettingsHandler(SockJSConnection):

    def __init__(self, *args, **kwargs):
        SockJSConnection.__init__(self, *args, **kwargs)
        self.errObject = []
        self.errReason = ""

        self.callbacks = {
        'updateSettings' : self.updateUserData,
        'updataNetwork' : self.updateNetworkData
        }

    def updateUserData(self, rq):
        data = {}
        self.user =  rq['data']['user']
        self.password =  rq['data']['password']
        self.play_composition_on_server_boot = rq['data']['play_composition_on_server_boot']
        config = weioConfig.getConfiguration()
        config["user"] = self.user
        config["play_composition_on_server_boot"] = self.play_composition_on_server_boot
        # Check if new password is sent
        if self.password:
            config["password"] = self.password
        

        # ATTENTION, DON'T MESS WITH THIS STUFF ON YOUR LOCAL COMPUTER
        # First protection is mips detection, second is your own OS
        # who hopefully needs sudo to change passwd on the local machine
        if (platform.machine() == 'mips'):
            # Change root password
            command = "sh scripts/change_root_pswd.sh " + self.password
          
            try:
                subprocess.call(command, shell=True)
                firstTimeSwitch = "NO"
                config['first_time_run']=firstTimeSwitch
                data['data'] = "msg_success"
     
            except:
                output = "ERR_CMD PASSWD"
                data['data'] = "msg_fail"
                print output
        else:
             # On PC
            firstTimeSwitch = "NO"
            config['first_time_run']=firstTimeSwitch
            data['data'] = "msg_success"
        
        # Save new user data in config file 
        weioConfig.saveConfiguration(config);
        data['requested'] = "updateSettings"
        self.send(json.dumps(data))

    def updateNetworkData(self, rq):
        data = {}
        self.dns_name = rq['data']['dns_name']
        self.auto_to_ap = rq['data']['auto_to_ap']

        config = weioConfig.getConfiguration()
        config['dns_name'] = self.dns_name + ".local"
        config['auto_to_ap'] = self.auto_to_ap
      
        if (platform.machine() == 'mips'):
            # Change avahi name
            command = "sh scripts/change_boardname.sh " + self.dns_name
            try:
                subprocess.call(command, shell=True)
                firstTimeSwitch = "NO"
                config['first_time_run']=firstTimeSwitch
                data['data'] = "msg_success"
            except:
                output = "ERR_CMD BRDNAME"
                data['data'] = "msg_fail"
                print output
        else:
            # On PC
            firstTimeSwitch = "NO"
            config['first_time_run']=firstTimeSwitch
            data['data'] = "msg_success"
       
        # Save new user data in config file 
        weioConfig.saveConfiguration(config);
        data['requested'] = "updataNetwork"
        self.send(json.dumps(data))

    
    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        req = json.loads(data)
        self.serve(req)

    def serve(self, rq):
        request = rq['request']
        if request in self.callbacks :
            self.callbacks[request](rq)
        else :
            print "unrecognised request"
    
    def on_close(self):
        global clients
        # Remove client from the clients list and broadcast leave message
        clients.remove(self)
