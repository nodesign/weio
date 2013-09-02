import time
from weioLib.weioUserApi import *

# Simple standalone application, no web interface
# Reads digital potentiometer from A0 pin to blink LED slower or
# faster at digital pin 13

LED_PIN = 13
POTENTIOMETER_PIN = "A0"

def setup() :

    # Attaches sensor function to infinite loop
    attach.process(blinky, ("Test", 10))

    # Attaches sensor function to infinite loop
    attach.process(potentiometer)

    # Instanciate shared objects
    shared.val = 1


###
# Threads
###

# These threads are like individual mini programs. Share data between them using shred variables
# In this case shared object is shared.val
# In most of cases this usage will work. If sync problems are encountered use lock library to lock
# shared data between threads
def potentiometer() :
    while (1) :
        print("potentiometer") 
        shared.val+=1
        time.sleep(1)


def blinky(s, k) :
    
    while (1) :
        print("blinky")
        val = shared.val
        print val
        time.sleep(val)