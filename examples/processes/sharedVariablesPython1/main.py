from weioLib.weio import *

import time

sharedVar[0] = 1
def setup():
    attach.process(myProcess)
    attach.event("tst", myEvent)

def myEvent(dataIn):
    print "EVENT"
    print dataIn
    sharedVar[0] = dataIn
    
def myProcess():
    print("Hello world")
    while True:
        if sharedVar[0] is not None:
           print sharedVar[0]
        time.sleep(1)
