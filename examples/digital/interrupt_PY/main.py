#######################################
#                                     #
#          HOW TO ATTACH AN           #
#         INTERRUPT ON WEIO           #
#                                     #
#######################################

# Descriptions: This example shows how to attach an interrupt on pin 18.
#               Callback that will be called on interrupt retuns an
#               object with interrupt type and pin number, this is
#               useful to trace pin on which interrupt has been rised.
#
# syntax = attachInterrupt(pin, type, callback, object)
#
# Available pins: All pins
# Available modes: RISING, FALLING, HIGH, LOW, CHANGE
    
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    # attach user-defined interrupt handler to pin 18
    pin = 18
    attachInterrupt(pin, RISING, testInt, pin)
    
    # Make one infinite loop with blinking LED
    while True:
        digitalWrite(18,LOW)
        delay(200)
        digitalWrite(18,HIGH)
        delay(200)
    
# This is interrupt callback
def testInt(event,obj):
    print "*** INTERRUPT ***"
    # event dictionary and function that brings in humain readable format
    # interrupt mode
    # Passed object contains pin number of inetrrupt
    eventType = getInterruptType(event["type"])
    print eventType, "on pin", obj