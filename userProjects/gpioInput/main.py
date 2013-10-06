from weioLib.weioGpio import WeioGpio
from weioLib.weioUserApi import attach, shared, INPUT_PULLDOWN
import time

def setup() :
    attach.process(loop)
    
def loop() :
    weio = shared.gpio
    cadence = 0.1
    weio.inputMode(13,INPUT_PULLDOWN)
    while True:
        val =  weio.digitalRead(13)
        print (val)
        time.sleep(cadence)