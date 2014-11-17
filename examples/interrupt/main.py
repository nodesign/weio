#######################################
#                                     #
#   Example of user-defined interrupt #
#   on WEIO                           #
#                                     #
#######################################

from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
    pin = 5

    # attach user-defined interrupt handler to pin 5
    # in attachInterrupt parameters are :
    # pin for interrupt,
    # mode can be RISING, FALLING, EDGE, CHANGE
    # callback that will be called on interrupt
    # some object that will be returned in callback, this is useful to trace
    # pin on which interrupt has been rised
    attachInterrupt(pin, RISING, testInt, pin)
    
def myProcess():
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
    
    