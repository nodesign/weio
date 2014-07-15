#######################################
#                                     #
#   how to get temperature on WEIO    #
#                                     #
#######################################

from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcess)
    
def myProcess():
    while True: #create an infinite loop
        print getTemperature() 
        delay(300) #stop during 300ms
