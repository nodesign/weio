#######################################
#                                     #
#     HOW TO SET pinMode on WEIO      #
#                                     #
#######################################

# Descriptions: This example shows how to set input mode for digitalRead
#               purpose. You can configure pin as a regular input or    
#               enable the internal pullup and pulldown resistors.
#
# Syntax: pinMode(pin, mode) or portMode(pin, mode)
#
# pin : all pins availables
# mode : INPUT, PULL_DOWN, PULL_UP

from weioLib.weio import *

def setup() :
    attach.process(buttonLoop)
    
def buttonLoop() :
    # define pins for reading
    pinDown = 24
    pinUp = 25
    # set pin 25 to pull_up mode
    pinMode(pinDown,PULL_DOWN)
    pinMode(pinUp,PULL_UP)
    # create infinite loop
    while True:
        # read digital value on pin 25
        valDown =  digitalRead(pinDown)
        valUp =  digitalRead(pinUp)
        # print result
        print "Pin",pinDown,"state :",valDown
        print "Pin",pinUp,"state :",valUp
        print ""
        # wait 500ms
        delay(500)
