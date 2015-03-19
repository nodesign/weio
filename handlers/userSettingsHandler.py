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
        self.login_required = rq['data']['login_required']
        self.play_composition_on_server_boot = rq['data']['play_composition_on_server_boot']
        config = weioConfig.getConfiguration()
        config["user"] = self.user
        config["play_composition_on_server_boot"] = self.play_composition_on_server_boot
        config["login_required"] = self.login_required
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
        self.timezone = rq['data']['timezone']
       
        config = weioConfig.getConfiguration()
        config['dns_name'] = self.dns_name + ".local"
        config['auto_to_ap'] = self.auto_to_ap

         # Check timezone
        if self.timezone:
            config["timezone"] = self.timezone
         
        if (platform.machine() == 'mips'):
            # Change avahi name
            command = "sh scripts/change_boardname.sh " + self.dns_name
            if self.timezone:
                commandConfig = "uci set system.@system[0].timezone=" + self.timezone  # Set timezone on openwrt config (required for system reboot)
                commandCommitConfig = "uci commit system.@system[0].timezone"
         
            try:
                subprocess.call(command, shell=True)
                subprocess.call(commandConfig, shell=True)
                subprocess.call(commandCommitConfig, shell=True)
            
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
