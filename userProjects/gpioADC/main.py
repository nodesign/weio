from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared
import time

def setup() :
    attach.process(loop)
    
def loop() :
    cadence = 0.1
    while True:
        val = analogRead(25)
        print val
        time.sleep(cadence)
