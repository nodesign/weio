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

from subprocess import Popen, PIPE

# pure websocket implementation
#from tornado import websocket

from sockjs.tornado import SockJSRouter, SockJSConnection

from weioLib import weioFiles
from weioLib import weio_config
from weioLib import weioAvahi
from weioLib import weioIpAddress


import functools

import json



# Wifi detection route handler  
class WeioFirstTimeHandler(SockJSConnection):
    
    global callbacks
    
    def runWeio(self,rq):
        
        fullName = rq['fullName']
        passwd1 = rq['password1']
        passwd2 = rq['password2']
        dnsName = rq['dnsName']
        
        passwd = ""
        if (passwd1==passwd2):
            passwd = passwd1 
        
        data = {}
        if (fullName!="" and passwd!="" and dnsName!=""):
            confFile = weio_config.getConfiguration()
            # OK now is time to setup username and password
            confFile['user'] = fullName
            weio_config.saveConfiguration(confFile)
            
            output = "OK PASSWD"
            #echo -e "weio\nweio" | passwd
            command = "sh scripts/change_root_pswd.sh " + passwd
            try :
                # ATTENTION, DON'T MESS WITH THIS STUFF ON YOUR LOCAL COMPUTER
                # First protection is mips detection, second is your own OS
                # who needs sudo to change passwd
                if (platform.machine() == 'mips') : 
                    
                    print Popen(command, stdout=PIPE, shell=True).stdout.read()
                    
                    path = confFile['user_projects_path'] + confFile['last_opened_project'] + "index.html"
                    
                    firstTimeSwitch = "NO"
                    confFile['first_time_run']=firstTimeSwitch
                    weio_config.saveConfiguration(confFile)
                else :
                    print command
                    firstTimeSwitch = "NO"
                    confFile['first_time_run']=firstTimeSwitch
                    weio_config.saveConfiguration(confFile)
            except :
                print("Comand ERROR : " + str(output) + " " + command)
                output = "ERR_CMD"
            print output
        
            #sucess
            data['requested'] = rq['request']
            data['data'] = 'OK'
            self.send(json.dumps(data))
    
        else :

            if (fullName==""):
                data['serverPush'] = 'error'
                data['data'] = 'Please enter your full name'
                self.send(json.dumps(data))
            elif (passwd==""):
                data['serverPush'] = 'error'
                data['data'] = 'Please enter valid password'
                self.send(json.dumps(data))
            elif (dnsName==""):
                data['serverPush'] = 'error'
                data['data'] = 'Please enter valid DNS name'
                self.send(json.dumps(data))
    
    
    def pushBasicInfo(self,rq):
        # here we get basic info from WeIO
        
        myIp = weioIpAddress.getLocalIpAddress()

        if (platform=='mips') :
            myAvahiName = weioAvahi.getAvahiName()
        else :
            myAvahiName = 'weio'

        data = {}
        data['requested'] = rq['request']
        data['ip'] = myIp
        data['dnsName'] = myAvahiName
        self.send(json.dumps(data))
    

    #########################################################################
    # DEFINE CALLBACKS IN DICTIONARY
    # Second, associate key with right function to be called
    # key is comming from socket and call associated function
    callbacks = {
        'runWeio' : runWeio,
        'getBasicInfo' : pushBasicInfo,
    }   
    
    def on_open(self, info) :
        pass
    
    
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
