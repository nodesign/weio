#######################################
#                                     #
#      HOW TO SEND EVENTS FROM        #
#    JAVASCRIPT TO PYTHON ON WEIO     #
#                                     # 
#######################################

# Description: write digital values to PINS 18, 19 & 20 (connected to
# RGB LED) when an event is emited from user interface.
# WeIO functions: digitalWrite(pin, state) - Available in all PINS

# import all WeIO libs
from weioLib.weio import *

def setup() :
    # create event and link to function
    attach.event("msgFromJStoPy", led)

def led(dataIn):
    print "msgFromJStoPy cached, received data:", dataIn
    print " "
    
    # write received data on pins 18, 19 and 20
    digitalWrite(18, dataIn)
    digitalWrite(19, dataIn)
    digitalWrite(20, dataIn)

