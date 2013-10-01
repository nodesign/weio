from weioLib.weioGpio import WeioGpio
from weioLib.weioUserApi import attach, HIGH, LOW

import time

def setup() :
    attach.process(blinky)

def blinky() :
    
    cadence = 0.1
    weio = WeioGpio()
    while True:
        weio.digitalWrite(20, HIGH)
        time.sleep(cadence)
        weio.digitalWrite(20, LOW)
        time.sleep(cadence)