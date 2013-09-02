import time
import weio

from weioLib.weioUserApi import *

# Simple standalone application, no web interface
# Reads digital potentiometer from A0 pin to blink LED slower or
# faster at digital pin 13

LED_PIN = 13
POTENTIOMETER_PIN = "A0"


def setup() :
    # tells that on LED pin we want output
    #pinMode(LED_PIN, OUTPUT)

    # Attaches sensor function to infinite loop
    attach.process(blinky, ("Test", 10))

    # Attaches sensor function to infinite loop
    attach.process(potentiometer)

    # Instanciate shared objects
    shared.val = 1

###
# Threads
###
def potentiometer() :

    while (1) :
        print("potentiometer") 
        shared.val = analogRead(POTENTIOMETER_PIN)
        time.sleep(1)


def blinky(s, k) :
    i = 0
    while (1) :
        print("blinky")
        i = i+1
        time.sleep(shared.val)
        print s
        print k
        
def analogRead(potar):
    return 500
    
WeioUserSetup()
weio()