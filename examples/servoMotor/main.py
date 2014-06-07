from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcessA)
    attach.process(myProcessB)
    
def myProcessA():
    s = initServo(23)
    print "Hello from processA"
    while True :
        for i in range(180):
            s.write(i)
            delay(20)

        for i in range(180):
            s.write(180-i)
            delay(20)
    
def myProcessB():
    print "Hello from processB"
    while True:
        digitalWrite(19,LOW)
        delay(100)
        digitalWrite(19,HIGH)
        delay(100)
