#######################################
#                                     #
#   how to get temperature on WEIO    #
#                                     #
#######################################

from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    while True: #create an infinite loop
        print getTemperature() 
        delay(300) #stop during 300ms
