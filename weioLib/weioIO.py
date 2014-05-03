import platform
import time

###
# Global interface
###
# Shared gpio object over all classes inside project
# There cannot be two instances of WeioGpio
gpio = None

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
