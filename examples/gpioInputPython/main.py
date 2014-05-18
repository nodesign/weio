from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared, INPUT_PULLDOWN
import time

def setup() :
    attach.process(loop)
    
def loop() :
    pin = 25
    inputMode(pin,INPUT_PULLDOWN)
    while True:
        val =  digitalRead(pin)
        print (val)
        delay(20)
