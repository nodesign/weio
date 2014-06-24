#######################################
#                                     #
#   Example of user-defined interrupt #
#   on WEIO                           #
#                                     #
#######################################

from weioLib.weioIO import *
from weioLib.weioUserApi import attach

pin = 5

def setup():
    attach.process(myProcess)
    
    # attach user-defined interrupt handler to pin 5
    attach.interrupt(pin, 4, testInt)
    
def myProcess():
    while True:
        a=digitalRead(pin)
        print "Value on the pin ",pin," = ",a
        delay(200)
        
def testInt(args1, args2):
    print "*** INTERRUPT ***"
    print "ARGS1 = ", args1
    print "ARGS2 = ", args2