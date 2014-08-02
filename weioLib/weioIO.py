import platform
import time
from weioLib.weioLm75 import WeioLm75
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.interrupt import Interrupt
from IoTPy.pyuper.i2c import I2C as interfaceI2C
from IoTPy.pyuper.spi import SPI as interfaceSPI
###
# Global interface
###
# Shared gpio object over all classes inside project
# There cannot be two instances of WeioGpio
gpio = None
lm75 = WeioLm75()

PULL_UP = GPIO.PULL_UP
PULL_DOWN = GPIO.PULL_DOWN
HIGH_Z = GPIO.HIGH_Z
INPUT = GPIO.INPUT
OUTPUT = GPIO.OUTPUT
HIGH = 1
LOW = 0
CHANGE = Interrupt.EDGE_CHANGE
RISING = Interrupt.EDGE_RISE
FALLING = Interrupt.EDGE_FALL

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

def analogWrite(pin, value):
    """Defining idiom of pwmWrite to match arduino syntax"""
    return gpio.pwmWrite(pin, value)

def proportion(value, istart, istop, ostart, ostop):
    return gpio.proportion(value, istart, istop, ostart, ostop)

def attachInterrupt(pin, mode, callback):
    try:
        return gpio.attachInterrupt(pin, mode, callback)
    except:
        print "attachInterrupt(", pin,",",mode,",",callback,")"
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

def notone(pin):
    try:
        return gpio.notone(pin)
    except:
        print "tone(", pin, ")"
        return -1
def constrain(self, x, a, b):
    try:
        return gpio.constrain(x,a,b)
    except:
        print "constrain(", x,",",a,",",b,")"
        return -1

def millis():
    return gpio.millis()

def getTemperature(unit="C"):
    return lm75.getTemperature(unit)

def getPinInfo():
    print "INFO", gpio
    return gpio.getPinInfo()

# NATIVE PROTOCOLES

def initI2C():
    return interfaceI2C(gpio.u)

def initSPI(*args):
    return interfaceSPI(gpio.u, *args)

# CALL FOR THING LIBRARIES
def weioLib(lib, *args):
    return lib(gpio.u,*args)
