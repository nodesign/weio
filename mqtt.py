#!/usr/bin/python -u

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

import paho.mqtt.client as mqtt
import time
import threading

import sys, os, logging, platform, json, signal, datetime, traceback

# WeIO stuff
from weioLib import weioConfig
from weioLib import weioFiles
from weioLib import weioRunnerGlobals
from weioLib import weioParser
from weioLib import weioUserApi
from weioLib import weioGpio
from weioLib import weioIO

###
# MQTT cb handlers
###

###
# on_connect
###
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("weio/api")   

###
# on_message
###
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


###
# WeIO stuff
###
def weioStart():

    weioUserApi.attach =  weioUserApi.WeioAttach()
    #weioUserApi.shared =  weioUserApi.WeioSharedVar()
    weioUserApi.console =  weioUserApi.WeioPrint()

    ###
    # Configuration stuff
    ###
    # Get configuration from file
    confFile = weioConfig.getConfiguration()
    
    # Path of last opened project
    lp = confFile["last_opened_project"]

    # Check if main.py exists in current user project
    if (weioFiles.checkIfFileExists(lp+"/main.py")):
        # set the location of current project main.py
        projectModule = lp.replace('/', '.') + ".main"
    else:
        # Use the location of default www/defaultMain/main.py
        projectModule = "www.defaultMain.main"

    # Init GPIO object for uper communication
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED == False):
        try:
            weioIO.gpio = weioGpio.WeioGpio()
        except:
            print "LPC coprocessor is not present"
            weioIO.gpio = None

    try:
        userMain = __import__(projectModule, fromlist=[''])

        print "userMain = ", userMain
            
        # Calling user setup() if present
        if "setup" in vars(userMain):
            print "SETUP"
            userMain.setup()
    except:
        print "MODULE CAN'T BE LOADED." \
                "Maybe you have some errors in modules that you wish to import?"
        #print traceback.format_exc()
        #result = None

    ###
    # Add user callback handlers for events
    ###
    for key in weioUserApi.attach.events:
        weioParser.addUserEvent(weioUserApi.attach.events[key].event,
                weioUserApi.attach.events[key].handler)

    # Launching threads
    for key in weioUserApi.attach.procs:
        #print key
        t = threading.Thread(target=weioUserApi.attach.procs[key].procFnc,
                    args=weioUserApi.attach.procs[key].procArgs)
        t.daemon = True
        t.start()
        

###
# CLIENT MAIN
###
if __name__ == '__main__':
    
    # Start WeIO stuff
    weioStart()

    ###
    # MQTT stuff
    ###
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("iot.eclipse.org", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()
