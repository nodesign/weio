from weioLib.weioGpio import WeioGpio
from weioLib.weioUserApi import attach, shared
import time

def setup() :
    attach.process(loop)
    
def loop() :
    cadence = 0.1
    while True:
        val = shared.gpio.analogRead(25)
        print val
        time.sleep(cadence)