from weioLib.weioGpio import WeioGpio
import platform
import time

###
# Global interface
###
# Shared gpio object over all classes inside project
# There cannot be two instances od WeioGpio
if (platform.machine()=="mips"):
    gpio = WeioGpio()

###
# User API functions for GPIO
###

def mainInterrupt(data):
    return gpio.mainInterrupt(data)

def inputMode(pin, mode):
    return gpio.inputMode(pin, mode)
            
def digitalWrite(pin, state):
    return gpio.digitalWrite(pin, state)
    
def digitalRead(pin) :
    return gpio.digitalRead(pin) 
    
def analogRead(pin) :
    return gpio.analogRead(pin)         
    
def pwmWrite(pin, value) :
    return gpio.pwmWrite(pin, value)

def analogWrite(pin, value):
    """Defining idiom of pwmWrite to match arduino syntax"""
    return gpio.pwmWrite(pin, value)

def proportion(value, istart, istop, ostart, ostop):
    return gpio.proportion(value, istart, istop, ostart, ostop)
    
def setPwm0PortPeriod(period):
    return gpio.setPwm0PortPeriod(period)

def setPwm1PortPeriod(period):
    return gpio.setPwm1PortPeriod(period)

def setPwmPeriod(period):
    return gpio.setPwmPeriod(period)

def setPwm0Limit(limit):
    return gpio.setPwm0Limit(limit)

def setPwm1Limit(limit):
    return gpio.setPwm1Limit(limit)

def setPwmLimit(limit):
    return gpio.setPwmLimit(limit)

def attachInterrupt(pin, mode, callback):
    return gpio.attachInterrupt(pin, mode, callback)

def detachInterrupt(pin):
    return gpio.detachInterrupt(pin)

def getAvailableInterruptId():
    return gpio.getAvailableInterruptId()

def delay(period):
    """Delay expressed in milliseconds. Delay will block current process. Delay can be evil"""
    time.sleep(period/1000.0)
    
def stopWeio():
    if (platform.machine()=="mips"):
        return gpio.stop()

