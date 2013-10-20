from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared, INPUT_PULLDOWN
import time

def setup() :
    attach.process(loop)
    
def loop() :
    cadence = 0.1
    inputMode(13,INPUT_PULLDOWN)
    while True:
        val =  weio.digitalRead(13)
        print (val)
        time.sleep(cadence)
