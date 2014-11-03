#######################################
#                                     #
#   how to get millis on WEIO         #
#                                     #
#######################################

from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    a = millis() # Millis represents n of milliseconds from first power up of the board
    while True: # loop
        b = millis()
        print "millis = ", b - a # b - a represents n of milliseconds from this process launch
        delay(1000) # sleep during 1s
        

