#######################################
#                                     #
#      BLINKING AN LED ON WEIO        #
#                                     # 
#######################################

# Simple standalone application, no web interface
# Description: write digital values HIGH and LOW to PINS 18, 19 & 20 (connecteds to RGB LED). Use delay() functions to do blinking the led.
# WeIO functions: digitalWrite(pin, state) - Available in all PINS

from weioLib.weioIO import *
from weioLib.weioUserApi import attach


def setup() :
    
    # Attaches blinky function to infinite loop
    attach.process(blinky)

def blinky() :
    
    while True:
        
        # write HIGH value to digital PINS 18, 19 & 20
        digitalWrite(18, HIGH) # red led
        digitalWrite(19, HIGH) # green led
        digitalWrite(20, HIGH) # blue led
        
        # wait 100ms
        delay(100)
        
        # write LOW value to digital PINS 18, 19 & 20
        digitalWrite(18, LOW) # red led
        digitalWrite(19, LOW) # green led
        digitalWrite(20, LOW) # blue led
        
        # wait 100ms
        delay(100)