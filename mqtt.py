#!/usr/bin/python -u
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
# All rights not explicitly granted in the BSD license are reserved.
# See the included LICENSE file for more details.
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

# MQTT clinet
mqttClient = None


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

        # Calling user setup() if present
        if "setup" in vars(userMain):
            userMain.setup()
    except:
        print "MODULE CAN'T BE LOADED." \
                "Maybe you have some errors in modules that you wish to import?"

    # Add user callback handlers for events
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

        weioRunnerGlobals.WEIO_SERIAL_LINKED = True
        

###
# Signal handler
###
def signalHandler(sig, frame):

    # Stop the MQTT loop
    if (mqttClient is not None):
        mqttClient.disconnect()

    if (weioIO.gpio != None):
        if (weioRunnerGlobals.WEIO_SERIAL_LINKED == True):
            weioIO.gpio.stopReader()
            weioIO.gpio.reset()

    # Bail out
    sys.exit(0)


###
# CLIENT MAIN
###
if __name__ == '__main__':

    # Install signal handlers
    signal.signal(signal.SIGTERM, signalHandler)
    signal.signal(signal.SIGINT, signalHandler)
    
    # Start WeIO stuff
    weioStart()

    ###
    # MQTT stuff
    ###
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message

    mqttClient.connect("iot.eclipse.org", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqttClient.loop_forever()
