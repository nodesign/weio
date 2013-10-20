from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared, FALLING, RISING, interruptType
import time

def setup() :
    attach.process(testInterruptions)
    
def testInterruptions():
    # attach interruption on pin 15, activate on Falling edge
    # attach interruption on pin 30, activate on Rising edge
    attachInterrupt(15, FALLING, button0)
    attachInterrupt(30, RISING, button1)
    
    # sleep 10 seconds and test during this time
    time.sleep(10)
    
    # detach interrupts
    detachInterrupt(15)
    print ("interrupt on pin 15 detached")
    detachInterrupt(30)
    print ("interrupt on pin 30 detached")
    
# This is attached callback to interrupt
def button0(iType):
    # callback receives "key", integer that can be decoded using
    # inetrruptKey(key) to know if signal was Rising, Falling, etc...
    print "Interruption    0 : " + interruptType[iType]
    
    
def button1(iType):
    # callback receives "key", integer that can be decoded using
    # inetrruptKey(key) to know if signal was Rising, Falling, etc...
    print "Interruption    1 : " + interruptType[iType]
