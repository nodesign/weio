#######################################
#                                     #
#   how to have digitalRead on WEIO   #
#                                     #
#######################################

#syntax = digitalread(pin) 
#Value returned is 0 and 1
#it's possible to choose the mode with function pinMode(pin, mode)
#mode is PULL_UP or PULL_DOWN

from weioLib.weio import *

pin = 2

def setup():
    attach.process(myProcess)
    
def myProcess():
    while True:
        a = digitalRead(pin)
        print "Value on the pin ", pin, " = ", a
        delay(100)
        
