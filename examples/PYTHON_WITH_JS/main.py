from weioLib.weio import *

def setup():
    attach.event('colorled', led)

def led(dataIn):
    if(dataIn == 0):
        digitalWrite(20,LOW)
        digitalWrite(19,HIGH)
        digitalWrite(18,HIGH)
    if(dataIn == 1):
        digitalWrite(20,HIGH)
        digitalWrite(19,HIGH)
        digitalWrite(18,LOW)
    if(dataIn == 2):
        digitalWrite(20,HIGH)
        digitalWrite(19,LOW)
        digitalWrite(18,HIGH)