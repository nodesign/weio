#######################################
#                                     #
#   how to get AnalogRead on WEIO     #
#                                     #
#######################################

# syntax analogRead(pin) returns adc value
# there are 8 analog pins on weio (between 24 to 31)
# value is between 0 and 1023

from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    pin = 31
    while True:
        print "analogRead pin ",pin," = ",analogRead(pin)
        delay(100)
