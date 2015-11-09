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

from weioLib.weioIO import *
from weioUserApi import serverPush

from weioLib import weioRunnerGlobals
import platform, sys

# WeIO API bindings from websocket to lower levels
# Each data argument is array of data
# Return value is dictionary
def callPinMode(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        pinMode(data[0],data[1])
    else :
        print "pinMode ON PC", data
    return None

def callPortMode(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        portMode(data[0],data[1])
    else :
        print "pinMode ON PC", data
    return None

def callDigitalWrite(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        digitalWrite(data[0], data[1])
    else :
        print "digitalWrite ON PC", data
    return None

def callDigitalRead(data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        value = digitalRead(data[0])
        bck["data"] = value
        bck["pin"]  = data[0]
    else :
        print "digitalRead ON PC", data
        bck["data"] = 1 # faked value
        bck["pin"]  = data[0] # pin
    return bck

def callPulseIn(data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        value = pulseIn(data[0], data[1], data[2])
        bck["data"]    = value
        bck["pin"]     = data[0]
        bck["level"]   = data[1]
        bck["timeout"] = data[1]
    else :
        print "pulseIn ON PC", data
        bck["data"]    = 1       # faked value
        bck["pin"]     = data[0] # pin
        bck["level"]   = data[1] # level
        bck["timeout"] = data[2] # timeout
    return bck

def callPortWrite(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        portWrite(data[0], data[1])
    else :
        print "portWrite ON PC", data
    return None

def callPortRead(data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        value = portRead(data[0])
        bck["data"] = value
        bck["port"] = data[0]
    else :
        print "digitalRead ON PC", data
        bck["data"] = 1 # faked value
        bck["port"] = data[0] # pin
    return bck

def callDHTRead(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        dhtRead(data[0])
    else :
        print "dhtRead ON PC", data
    return None

def callAnalogRead(data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        #print "From browser ", data
        value = analogRead(data[0]) # this is pin number
        bck["data"] = value
        bck["pin"]  = data[0]
    else :
        print "analogRead ON PC", data
        bck["data"] = 1023 # faked value
        bck["pin"]  = data[0]
    return bck

def callSetPwmPeriod(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        setPwmPeriod(data[0],data[1])
    else:
        print "setPwmPeriod ON PC", data
    return None

# def callSetPwmLimit(data) :
#     if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
#         setPwmLimit(data[0])
#     else:
#         print "setPwmLimit ON PC", data
#     return None

def callPwmWrite(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        pwmWrite(data[0], data[1])
    else :
        print "pwmWrite ON PC", data
    return None

def callProportion(data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        #print "From browser ", data
        value = proportion(data[0],data[1],data[2],data[3],data[4])
        bck["data"] = value
    else :
        print "proportion ON PC", data
        bck["data"] = data
    return bck

def callAttachInterrupt(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        iObj = {"pin" : data[0], "jsCallbackString" : data[2]}
        attachInterrupt(data[0], data[1], genericInterrupt, iObj)
    else:
        print "attachInterrupt ON PC", data
    return None

def callDetachInterrupt(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        detachInterrupt(data[0])
    else:
        print "detachInterrupt ON PC", data
    return None

def genericInterrupt(event, obj):
    bck = {}
    bck["data"] = obj["pin"]
    bck["eventType"] = getInterruptType(event["type"])
    serverPush(obj["jsCallbackString"], bck)

def callDelay(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        delay(data[0])
    else :
        print "delay ON PC", data
    return None

def callTone(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        print "TONE VALS", len(data)
        if (len(data)==2):
            tone(data[0], data[1])
        elif (len(data)==3):
            tone(data[0], data[1], data[2])
    else :
        print "tone ON PC", data
    return None

def callNotone(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        noTone(data[0])
    else :
        print "notone ON PC", data
    return None

def callConstrain(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        constrain(data[0], data[1], data[2],)
        bck["data"] = value
    else :
        print "contrain ON PC", data
        bck["data"] = 1 # faked value
        bck["pin"]  = data[0] # pin
    return bck


def callMillis(data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        value = millis() 
        bck["data"] = value
    else :
        print "millis ON PC", data
        bck["data"] = 0 # faked value
    return bck

def callGetTemperature(data):
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        value = getTemperature()
        bck["data"] = value
    else :
        print "getTemperature ON PC", data
        bck["data"] = 0 # faked value
    return bck

def callUserMesage(data):
    print "USER TALKS", data
    #weioRunnerGlobals.userMain

def pinsInfo(data) :
    bck = {}
    bck["data"] = weioRunnerGlobals.DECLARED_PINS
    #print("GET PIN INFO ASKED!", bck["data"])
    return bck

def callListSerials(data):
    bck = {}
    bck["data"] = listSerials()
    return bck

# UART SECTION
clientSerial = None
def callInitSerial(data):
    global clientSerial
    if (clientSerial is None) :
        clientSerial = initSerial(data[0], data[1])

def callSerialWrite(data):
    global clientSerial
    if not(clientSerial is None) :
        clientSerial.write(data)
    else :
        sys.stderr.write("Serial port is not initialized. Use initSerial function first")

def callSerialRead(data):
    global clientSerial
    bck = {}
    if not(clientSerial is None) :
        bck["data"] = clientSerial.read()
    else :
        sys.stderr.write("Serial port is not initialized. Use initSerial function first")
    return bck
    
# SPI SECTION
SPI = None
def callInitSPI(data):
    global SPI
    if (SPI is None) :
        SPI = initSPI(data[0])

def callWriteSPI(data):
    global SPI
    if not(SPI is None) :
        SPI.write(data[0])
    else :
        sys.stderr.write("SPI port is not initialized. Use initSerial function first")

def callReadSPI(data):
    global SPI
    bck = {}
    if not(SPI is None) :
        bck["data"] = SPI.read(data[0])
    else :
        sys.stderr.write("SPI port is not initialized. Use initSerial function first")
    return bck
        
###
# WeIO native spells
###
weioSpells = {
    "digitalWrite"    :callDigitalWrite,
    "digitalRead"     :callDigitalRead,
    "pulseIn"         :callPulseIn,
    "portWrite"       :callPortWrite,
    "portRead"        :callPortRead,
    "dhtRead"         :callDHTRead,
    "analogRead"      :callAnalogRead,
    "pinMode"         :callPinMode,
    "portMode"        :callPortMode,
    "setPwmPeriod"    :callSetPwmPeriod,
    "pwmWrite"        :callPwmWrite,
    "proportion"      :callProportion,
    "attachInterrupt" :callAttachInterrupt,
    "detachInterrupt" :callDetachInterrupt,
    "tone"            :callTone,
    "noTone"          :callNotone,
    "constrain"       :callConstrain,
    "millis"          :callMillis,
    "getTemperature"  :callGetTemperature,
    "delay"           :callDelay,
    "pinsInfo"        :pinsInfo,
    "listSerials"     :callListSerials,
    "initSerial"      :callInitSerial,
    "serialWrite"     :callSerialWrite,
    "initSPI"         :callInitSPI,
    "readSPI"         :callReadSPI,
    "writeSPI"        :callWriteSPI
  # "message":callUserMesage
}

###
# User added spells (handlers)
###
weioUserSpells = {}

def addUserEvent(event, handler):
    global weioUserSpells
    #print "Adding event ", event
    #print "and handler ", handler
    weioUserSpells[event] = handler

def removeUserEvents():
    global weioUserSpells
    weioUserSpells.clear()

