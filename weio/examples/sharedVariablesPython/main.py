import time
from weioLib.weioUserApi import attach, shared, HIGH, LOW
from weioLib.weioIO import *

# Simple standalone application, no web interface
# Reads digital potentiometer from pin 25 to blink LED slower or
# faster at digital pin 20

LED_PIN = 20
POTENTIOMETER_PIN = 25

###
# Threads
###

# These threads are like individual mini programs. Share data between them using shred variables
# In this case shared object is shared.val
# In most of cases this usage will work. If sync problems are encountered use lock library to lock
# shared data between threads
def potentiometer() :
    while (1) :
        shared.val = analogRead(POTENTIOMETER_PIN)
        time.sleep(0.1)


def blinky() :
    
    while (1) :
        val = shared.val
        print val
        
        digitalWrite(LED_PIN, HIGH)
        delay(val)
        digitalWrite(LED_PIN, LOW)
        delay(val)
        
        
def setup():
    # Attaches sensor function to infinite loop
    attach.process(blinky)
    
    # Attaches sensor function to infinite loop
    attach.process(potentiometer)
    
    # Instanciate shared objects
    shared.val = 0