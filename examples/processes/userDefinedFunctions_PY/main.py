from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    while True:
        ret = userDefinedFunction(200, [0])
        print ret
        delay(500)
        ret = userDefinedFunction(200, [1])
        print ret
        delay(500)

