###############################################
#                                             #
#     HCSR04 ultra sound distance sensor      #
#                                             #
###############################################

from weioLib.weio import *
from things.input.distance.HCSR04 import HCSR04

def setup():
    attach.process(myProcess)
    
def myProcess():
    sensor = HCSR04(0,1) # trigger pin, echo pin
    while True:
        print sensor.distCentimeters()
        #print sensor.distInches()
        delay(100)