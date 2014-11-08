#######################################
#                                     #
#   Example of user-defined interrupt #
#   on WEIO                           #
#                                     #
#######################################

from weioLib.weio import *

pin = 5

def setup():
    attach.process(myProcess)
    
    # attach user-defined interrupt handler to pin 5
    attach.interrupt(pin, RISING, testInt)
    
def myProcess():
    m = 0
    while True:
        a=digitalRead(pin)
        print "Value on the pin ",pin," = ",a, " Iteration ", m
        delay(200)
        if (m==50):
            print "detaching"
            detachInterrupt(pin)
        m = m+1
    
        
def testInt(args1, args2):
    print "*** INTERRUPT ***"
    print "ARGS1 = ", args1
    print "ARGS2 = ", args2
    print getInterruptType(args1["type"])
