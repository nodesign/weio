from weioLib.weio import *

import time

def setup() :
    # create event and link to function
    attach.event("myEvent", led)

def led(dataIn):
    print "myEvent cached, received data:"
    print dataIn
    print ""
    
    # write received data on pins 18, 19 and 20
    digitalWrite(18, dataIn)
    digitalWrite(19, dataIn)
    digitalWrite(20, dataIn)

