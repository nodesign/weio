#######################################
#                                     #
#   HOW TO GET TEMPERATURE ON WEIO    #
#                                     #
#######################################

# Description: This example shows you how to get temperature value from 
#              WeIO thermometer every 300ms.
# syntax: getTemperature() 

from weioLib.weio import *

def setup():
    # Attaches myProcess fucntion to infinite loop
    attach.process(myProcess)
    
def myProcess():
    #create an infinite loop
    while True:
        # print returned temperatur in the console
        print getTemperature() 
        # wait 300ms
        delay(300)
