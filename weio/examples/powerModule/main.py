#############################################
#                                           #
#   WeIO PowerModule    #
#                                           #
#############################################

# Example presents SPI communication with 74HC595 chip
# Latch pin to LOW to start communication
# Serial output in 8 bit format
# Larch pin to HIGH to end communication and present outputs on chip pins

from weioLib.weio import *
from things.powerModule import PowerModule

def setup():
    attach.process(myProcess)
    
def myProcess():
    pwr = PowerModule(0)
    
    while True:
        pwr.portWrite(0)
        for a in range(16):
            pwr.digitalWrite(a, HIGH)
            delay(100)
