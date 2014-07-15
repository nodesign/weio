from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello world")
    digitalWrite(18,HIGH)
    digitalWrite(0,HIGH)
    digitalWrite(15,LOW)
    digitalWrite(16,LOW)
    print getPinInfo()
