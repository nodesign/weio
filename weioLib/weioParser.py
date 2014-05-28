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

from weioLib.weioIO import *
from weioLib import weioRunnerGlobals
import platform

# WeIO API bindings from websocket to lower levels
# Each data argument is array of data
# Return value is dictionary
def callpinMode(self, data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        inputMode(data[0],data[1])
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
    else :
        print "digitalRead ON PC", data
        bck["data"] = 1 # faked value
        bck["pin"] = data[0] # pin
    return bck
    
def callAnalogRead(data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        #print "From browser ", data
        value = analogRead(data[0]) # this is pin number
        bck["data"] = value
    else :
        print "analogRead ON PC", data
        bck["data"] = 1023 # faked value
        bck["pin"] = data[0]
    return bck

def callSetPwmPeriod(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        setPwmPeriod(data[0],data[1])
        print data[0], data[1]
    else:
        print "setPwmPeriod ON PC", data
    return None
    
def callSetPwmLimit(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        setPwmLimit(data[0])
    else:
        print "setPwmLimit ON PC", data
    return None
    
def callPwmWrite(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        pwmWrite(data[0], data[1])
        print data[0], data[1]
    else :
        print "pwmWrite ON PC", data
    return None
    
def callProportion(data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        #print "From browser ", data
        value = proportion(data[0],data[1],data[2],data[3],data[4],) # this is pin number
        bck["data"] = value
    else :
        print "proportion ON PC", data
        bck["data"] = data
    return bck

def callAttachInterrupt(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        attachInterrupt(data[0], data[1])
    else:
        print "attachInterrupt ON PC", data
    return None

def callDetachInterrupt(data) :
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        detachInterrupt(data[0])
    else:
        print "detachInterrupt ON PC", data
    return None
    
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
        notone(data[0])
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
        bck["pin"] = data[0] # pin
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

def genericInterrupt(data):
    #type = data["type"]
    #data = {}
    #data["requested"] = 'analogRead'
    #data["data"] = value
    #self.write_message(json.dumps(data))
    pass
    
def callUserMesage(data):
    print "USER TALKS", data
    #weioRunnerGlobals.userMain

def pinsInfo(self, data) :
    bck = {}
    if (weioRunnerGlobals.WEIO_SERIAL_LINKED is True):
        #print "*SYSOUT* ", pins
        bck["data"] = weioRunnerGlobals.DECLARED_PINS
        pass
    else:
        print "pinsInfo ON PC", data
        bck["data"] = None # fake data here
    return bck

weioSpells = {
    "digitalWrite":callDigitalWrite,
    "digitalRead":callDigitalRead,
    "analogRead":callAnalogRead,
    "pinMode":callpinMode,
    "setPwmPeriod":callSetPwmPeriod,
    "setPwmLimit":callSetPwmLimit,
    "pwmWrite":callPwmWrite,
    "proportion":callProportion,
    "attachInterrupt":callAttachInterrupt,
    "detachInterrupt":callDetachInterrupt,
    "tone": callTone,
    "notone": callNotone,
    "constrain":callConstrain,
    "millis":callMillis,
    "getTemperature": callGetTemperature,
    "delay":callDelay,
    "pinsInfo": pinsInfo
    #,
   # "message":callUserMesage
    
}

