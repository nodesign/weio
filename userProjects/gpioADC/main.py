from weioLib.weioGpio import WeioGpio
from weioLib.weioUserApi import attach
import time

def setup() :
    attach.process(loop)
    
def loop() :
    weio = WeioGpio()
    cadence = 0.1
    while True:
        val = weio.analogRead(30)
        print val
        time.sleep(cadence)