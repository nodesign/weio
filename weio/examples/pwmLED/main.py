from weioLib.weio import *

def setup():
    attach.process(loop)
    
def loop():
    while True:
        print "fade in"
        # count from 0 to 255 by 5
        for i in range(0,255):
            pwmWrite(18,i)
            pwmWrite(19,i)
            pwmWrite(20,i)
            delay(3)
        print "fade out"    
        for i in range(0,255):
            pwmWrite(18,255-i)
            pwmWrite(19,255-i)
            pwmWrite(20,255-i)
            delay(3)