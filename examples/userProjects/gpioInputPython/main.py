from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared, INPUT_PULLDOWN
import time

def setup() :
    attach.process(loop)
    
def loop() :
    cadence = 0.1
    pin = 25
    inputMode(pin,INPUT_PULLDOWN)
    while True:
        val =  digitalRead(pin)
        print (val)
        time.sleep(cadence)
