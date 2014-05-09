from weioLib.weioIO import *
from weioLib.weioUserApi import attach

import time
   
def setup() :
    attach.process(loopG)

def loopG() :
    print "hello"
    while True:
        digitalWrite(19,1)
        val = analogRead(24)
        print "value",val
        time.sleep(0.01)
        digitalWrite(19,0)
        time.sleep(0.01)