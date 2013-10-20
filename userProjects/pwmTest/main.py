from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared
import time

def setup() :
    attach.process(loop)
    
def loop() :
    while True:
        print "fade in"
        # count from 0 to 512 by 5
        for i in xrange(0,255,5):
            pwmWrite(19,i)
            pwmWrite(20,i)
            pwmWrite(21,i)
            time.sleep(0.03)
        print "fade out"    
        for i in xrange(0,255,5):
            pwmWrite(19,255-i)
            pwmWrite(20,255-i)
            pwmWrite(21,255-i)
            time.sleep(0.03)
