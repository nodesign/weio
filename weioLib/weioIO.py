import platform
import time
from weioLib.weioLm75 import WeioLm75
from IoTPy.pyuper.gpio import GPIO
import IoTPy.things.servomotor as servoLib
import IoTPy.things.am2321 as am2321Lib
import IoTPy.things.si70xx as si70xxLib
import IoTPy.things.srf08 as srf08Lib
import IoTPy.things.stepper as StepperLib


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
        return gpio.inputMode(pin, mode)
    except:
        print "inputMode(", pin,",", mode,")"
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

def getTemperature():
    return lm75.getTemperature()

# BINDINGS TO LIBRARIES
def initServo(pin):
    return servoLib.Servo(gpio.u, pin)

def initAm2321():
    return am2321Lib.AM2321(gpio.u)

def initSi7020():
    return si7020Lib.Si7020(gpio.u)

def initSrf08Lib():
    return srf08Lib.Srf08(gpio.u)

def initStepper(steps360, coilA0, coilA1, coilB0, coilB1):
    return StepperLib.Stepper(gpio.u, steps360, coilA0, coilA1, coilB0, coilB1)
