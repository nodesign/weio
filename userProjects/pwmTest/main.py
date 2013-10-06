from weioLib.weioGpio import WeioGpio
from weioLib.weioUserApi import attach, shared
import time

def setup() :
    attach.process(loop)
    
def loop() :
    weio = shared.gpio
    #weio.setPwmLimit(512)
    while True:
        print "fade in"
        # count from 0 to 512 by 5
        for i in xrange(0,255,5):
            weio.pwmWrite(19,i)
            weio.pwmWrite(20,i)
            weio.pwmWrite(21,i)
            time.sleep(0.03)
        print "fade out"    
        for i in xrange(0,255,5):
            weio.pwmWrite(19,255-i)
            weio.pwmWrite(20,255-i)
            weio.pwmWrite(21,255-i)
            time.sleep(0.03)