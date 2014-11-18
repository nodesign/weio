#######################################
#                                     #
#      HOW TO SEND EVENTS FROM        #
#        JAVASCRIPT TO PYTHON         #
#                                     # 
#######################################

# Description: write digital values to PINS 18, 19 & 20 (connected to
# RGB LED) when an event is emited from user interface.
# WeIO functions: digitalWrite(pin, state) - Available in all PINS

# import all WeIO libs
from weioLib.weio import *

def setup():
    # Associating event "colored" to response "led" 
    attach.event('colorled', led)

# Define "led" function
def led(dataIn):
    # if received data is 0 blue LED is turned on
    if(dataIn == 0):
        digitalWrite(20,LOW)
        digitalWrite(19,HIGH)
        digitalWrite(18,HIGH)
    # if received data is 0 red LED is turned on
    if(dataIn == 1):
        digitalWrite(20,HIGH)
        digitalWrite(19,HIGH)
        digitalWrite(18,LOW)
    # if received data is 0 turn green LED is turned on
    if(dataIn == 2):
        digitalWrite(20,HIGH)
        digitalWrite(19,LOW)
        digitalWrite(18,HIGH)