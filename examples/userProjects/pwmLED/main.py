from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared

def setup() :
    attach.process(loop)
    
def loop() :
    setPwmLimit(512)
    while True:
        print "fade in"
        # count from 0 to 255 by 5
        for i in range(0,512):
            pwmWrite(19,i)
            pwmWrite(20,i)
            pwmWrite(21,i)
            delay(3)
        print "fade out"    
        for i in range(0,512):
            pwmWrite(19,512-i)
            pwmWrite(20,512-i)
            pwmWrite(21,512-i)
            delay(3)