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

def attachInterrupt(pin, mode, callback, obj):
    try:
        return gpio.attachInterrupt(pin, mode, callback, obj)
    except:
        print "attachInterrupt(", pin,",",mode,",",callback,",",obj,")"
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

def initSerial(port, baudrate, timeout_=1):
    # toggle RX and TX pins to secondary (UART) mode
    interfaceUART(gpio.u)
    return serial.Serial(port, baudrate, timeout=timeout_)

