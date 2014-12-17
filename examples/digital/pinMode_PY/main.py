#######################################
#                                     #
#     HOW TO SET pinMode on WEIO      #
#                                     #
#######################################

# Descriptions: This example shows how to set input mode for 
#               digitalRead purpose. 
#
# Syntax: pinMode(pin, mode) or portMode()
# Available modes are : INPUT, PULL_DOWN, PULL_UP

from weioLib.weio import *

def setup() :
    attach.process(loop)
    
def loop() :
    # define pin for reading
    pin = 25
    # set pin 25 to pull_up mode
    pinMode(pin,PULL_UP)
    # create infinite loop
    while True:
        # read digital value on pin 25
        val =  digitalRead(pin)
        # print result
        print (val)
        # wait 200msw
        delay(200)
