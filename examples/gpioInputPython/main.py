from weioLib.weio import *
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
