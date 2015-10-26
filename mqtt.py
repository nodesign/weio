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

import sys, json, signal

# WeIO stuff
from weioLib import weioRunnerGlobals
from weioLib import weioControl

# MQTT clinet
mqttClient = None

# weioCtrl
weioCtrl = weioControl.weioControl()

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
    client.subscribe("weio/api/in")   

###
# on_message
###
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    #req = json.loads(msg.payload)

    # Test with: mosquitto_pub -t "weio/api/in" -m '{ "request": "tst-event", "data" : "data" }'
    from StringIO import StringIO
    io = StringIO(msg.payload)
    req = json.load(io)
    print req['request']

    res = weioCtrl.execute(req)

    mqttClient.publish("weio/api/out", res)
        

###
# Signal handler
###
def signalHandler(sig, frame):

    # Stop WeIO
    weioCtrl.stop()

    # Stop the MQTT loop
    if (mqttClient is not None):
        mqttClient.disconnect()

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
    weioCtrl.start()

    ###
    # MQTT stuff
    ###
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message

    mqttClient.connect("localhost", 1883, 60)

    print "if anything goes wrong kill process with: kill -9 `ps aux | grep mqtt | grep python | awk '{print $2}'`"

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqttClient.loop_forever()
