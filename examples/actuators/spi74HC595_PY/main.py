#############################################
#                                           #
#   74HC595, 8bit Serial-in Parallel out    #
#                                           #
#############################################

# Example presents SPI communication with 74HC595 chip
# Latch pin to LOW to start communication
# Serial output in 8 bit format
# Latch pin to HIGH to end communication and present outputs on chip pins

from weioLib.weio import *

import struct

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("SPI starts")
    spi = initSPI(0) # init SPI on port 0 (pins : 2,3,4)
    latchPin = 5
    while True :
        # run thru all 8 outputs of 74HC595
        b = 0
        for i in range(9):
            digitalWrite(latchPin, LOW)
            spi.transaction(struct.pack("B", b))
            digitalWrite(latchPin, HIGH)
            b = 1
            b = b<<i
            delay(100)