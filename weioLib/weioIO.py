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

import platform
import time
from weioLib.weioLm75 import WeioLm75
from IoTPy.core.gpio import GPIO
from IoTPy.pyuper.i2c import UPER1_I2C as interfaceI2C
from IoTPy.pyuper.spi import UPER1_SPI as interfaceSPI
from IoTPy.pyuper.uart import UPER1_UART as interfaceUART

# IMPORT BASIC CONFIGURATION FILE
from weioLib import weioConfig

import sys
import glob
import serial

###
# Global interface
###
# Shared gpio object over all classes inside project
# There cannot be two instances of WeioGpio
gpio = None
lm75 = WeioLm75()

PULL_UP =   GPIO.PULL_UP
PULL_DOWN = GPIO.PULL_DOWN
INPUT =     GPIO.INPUT
OUTPUT =    GPIO.OUTPUT
HIGH =      GPIO.HIGH
LOW =       GPIO.LOW
NONE =      GPIO.NONE
CHANGE =    GPIO.CHANGE
RISING =    GPIO.RISE
FALLING =   GPIO.FALL

###
# User API functions for GPIO
###
def mainInterrupt(data):
    try:
        return gpio.mainInterrupt(data)
    except:
        print data
        return -1

def pinMode(pin, mode):
    try:
        return gpio.pinMode(pin, mode)
    except:
        print "pinMode(", pin,",", mode,")"
        return -1

def portMode(port, mode):
    try:
        return gpio.portMode(port, mode)
    except:
        print "portMode(", port,",", mode,")"
        return -1

def digitalWrite(pin, state):
    try:
        return gpio.digitalWrite(pin, state)
    except:
        print "digitalWrite(", pin,",", state,")"
        return -1

def digitalRead(pin) :
    try:
        return gpio.digitalRead(pin)
    except:
        print "digitalRead(", pin,")"
        return -1

def portWrite(port, state):
    try:
        return gpio.portWrite(port, state)
    except:
        print "portWrite(", pin,",", state,")"
        return -1

def portRead(port, mode=NONE) :
    try:
        return gpio.portRead(port, mode)
    except:
        print "portRead(", port,")"
        return -1

def dhtRead(pin) :
    try:
        return gpio.dhtRead(pin)
    except:
        print "dhtRead(", pin,")"
        return -1

def HCSR04Read(trigger, pulse):
    try:
        return gpio.HCSR04Read(trigger, pulse)
    except:
        print "HCSR04Read(", trigger,",",pulse,")"
        return -1

def analogRead(pin) :
    try:
        return gpio.analogRead(pin)
    except:
        print "analogRead(", pin,")"
        return -1

def setPwmPeriod(pin, period):
    try:
        return gpio.setPwmPeriod(pin, period)
    except:
        print "setPwmPeriod(", pin,",",period,")"
        return -1

def setPwmLimit(limit):
    try:
        return gpio.setPwmlimit(limit)
    except:
        print "setPwmLimit(", limit,")"
        return -1

def pwmWrite(pin, value) :
    try:
        return gpio.pwmWrite(pin, value)
    except:
        print "pwmWrite(", pin,",",value,")"
        return -1
def setPwmPulseTime(pin, t):
    try:
        return gpio.setPwmPulseTime(pin, t)
    except:
        print "setPulseTime(", pin,",",t,")"
        return -1

def analogWrite(pin, value):
    """Defining idiom of pwmWrite to match arduino syntax"""
    try:
        return gpio.pwmWrite(pin, value)
    except:
        print "pwmWrite(", pin, ",",value,")"

def proportion(value, istart, istop, ostart, ostop):
    return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))

def constrain(x, a, b):
    if ((x<=b) and (x>=a)):
        return x
    else :
        if (x>b):
            return b
        if (x<a):
            return a

def attachInterrupt(pin, mode, callback, obj=None, debounceTime=50):
    try:
        return gpio.attachInterrupt(pin, mode, callback, obj, debounceTime)
    except:
        print "attachInterrupt(", pin,",",mode,",",callback,",",obj, "debounce time", debounceTime,")"
        return -1

def getInterruptType(mode):
    if (mode is HIGH):
        return "HIGH"
    elif (mode is LOW):
        return "LOW"
    elif (mode is RISING):
        return "RISING"
    elif (mode is FALLING):
        return "FALLING"

def detachInterrupt(pin):
    try:
        return gpio.detachInterrupt(pin)
    except:
        print "detachInterrupt(", pin,")"
        return -1

def delay(period):
    """Delay expressed in milliseconds. Delay will block current process. Delay can be evil"""
    time.sleep(period/1000.0)

def tone(pin, frequency, duration = 0):
    try:
        return gpio.tone(pin,frequency,duration)
    except:
        print "tone(", pin,",",frequency,",",duration,")"
        return -1

def noTone(pin):
    try:
        return gpio.noTone(pin)
    except:
        print "tone(", pin, ")"
        return -1

def pulseIn(pin,level=GPIO.HIGH, timeout=100000):
    try:
        return gpio.pulseIn(pin,level,timeout)
    except:
        print "pulseIn(", pin,",",level,",",timeout,")"
        return -1

def millis():
    return gpio.millis()

def getTemperature(unit="C"):
    return lm75.getTemperature(unit)

def getPinInfo():
    print "INFO", gpio
    return gpio.getPinInfo()

def getCurrentPath():
    config = weioConfig.getConfiguration()
    return config["last_opened_project"]

# LIST SERIAL PORTS ON THE MACHINE
def listSerial():
    ser = []
    dirs = os.listdir("/dev")
    for a in range(len(dirs)):
        if ("tty" in dirs[a]):
            #print dirs[a]
            ser.append(dirs[a])
    return ser

def versionWeIO():
    # get configuration from file
    config = weioConfig.getConfiguration()
    # get WeIO version
    return config["weio_version"]

# NATIVE PROTOCOLES NOT FOR USERS THIS IS FOR DRIVERS ONLY

def initI2C():
    return interfaceI2C(gpio.u)

def initSPI(*args):
    return interfaceSPI(gpio.u, *args)

def initSerial(port='/dev/ttyACM1', baudrate=9600, timeout_=1):
    # toggle RX and TX pins to secondary (UART) mode
    interfaceUART(gpio.u)
    return serial.Serial(port, baudrate, timeout=timeout_)

