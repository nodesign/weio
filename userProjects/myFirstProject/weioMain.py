import time
import sys
 
sys.path.append(r'./')
from weioLib.weioUserApi import *

# Simple standalone application, no web interface
# Reads digital potentiometer from A0 pin to blink LED slower or
# faster at digital pin 13

LED_PIN = 13
POTENTIOMETER_PIN = "A0"


def WeioUserSetup() :
    # tells that on LED pin we want output
    #pinMode(LED_PIN, OUTPUT)

    # Attaches interrupt from Web client
    attach.event('setColor', buttonHandler)

    # Attaches sensor function to infinite loop
    attach.process(blinky, ("Test", 10))

    # Attaches sensor function to infinite loop
    attach.process(potentiometer)

    # Instanciate shared objects
    shared.val = 1


###
# Event Handlers
###
def buttonHandler(dataIn) :
    #waelice.setColor(dataIn[0], dataIn[1], dataIn[2])
    pass



###
# Threads
###
def potentiometer() :
    #val = analogRead(POTENTIOMETER_PIN)
    # map values between 0-1023 to time intervals 50 millis - 1000 millis
    #val = map(val, 0,1023, 50,1000)

    while (1) :
        print("potentiometer") 
        shared.val = shared.val + 1

        time.sleep(1)


def blinky(s, k) :
    i = 0
    while (1) :
        print("blinky")
        i = i+1
        time.sleep(shared.val)
        print s
        print k
