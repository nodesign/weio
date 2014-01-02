import time
from weioLib.weioUserApi import *

import threading
import random

# Simple standalone application, no web interface
# Reads digital potentiometer from A0 pin to blink LED slower or
# faster at digital pin 13

LED_PIN = 13
POTENTIOMETER_PIN = "A0"

lock = threading.RLock()

###
# Threads
###

# These threads are like individual mini programs. Share data between them using shred variables
# In this case shared object is shared.val
# In most of cases this usage will work. If sync problems are encountered use lock library to lock
# shared data between threads
def potentiometer() :
    while (1) :
        print("potentiometer") 
        shared.val += 1
        time.sleep(1)
        
def test1():
    f = open('myfile','a')
    time.sleep (random.random ())
    localVar = shared.val + 1
    time.sleep (random.random ()) # Some long call between 0 and 1
    shared.val = localVar
    print 'Thread1 ends: criticalVar = %d' % shared.val
    
    s="\n>>START<<\n"
    for i in range(100):
        for j in range(100):
            s = s + "1"
        s = s + '\n'
    s = s + "\n>>STOP<<\n"

    #print >>f, s
    console.output(s, file=f)
    f.close()

def test2():
    f = open('myfile','a')
    time.sleep (random.random ())
    localVar = shared.val + 1
    time.sleep (random.random ()) # Some long call between 0 and 1
    shared.val = localVar
    print 'Thread2 ends: criticalVar = %d' % shared.val

    s="\n>>START<<\n"
    for i in range(100):
        for j in range(100):
            s = s + "2"
        s = s + '\n'
    s = s + "\n>>STOP<<\n"
    #print >>f, s
    console.output(s, file=f)
    f.close()
    
    
def test3():
    f = open('myfile','a')
    time.sleep (random.random ())
    localVar = shared.val + 1
    time.sleep (random.random ()) # Some long call between 0 and 1
    shared.val = localVar
    console.output('Thread3 ends: criticalVar = %d' % shared.val)

    s="\n>>START<<\n"
    for i in range(100):
        for j in range(100):
            s = s + "3"
        s = s + '\n'
    s = s + "\n>>STOP<<\n"
    #print >>f, s
    console.output(s, file=f)
    f.close()

    

        
def setup():
    # Attaches sensor function to infinite loop
    attach.process(test1)
    attach.process(test2)
    attach.process(test3)
    
    # Instanciate shared objects
    shared.val = 0
