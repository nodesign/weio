from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup() :
    attach.process(blinky)

def blinky() :
    while True:
        digitalWrite(18, HIGH)
        digitalWrite(19, HIGH)
        digitalWrite(20, HIGH)
        delay(100)
        digitalWrite(18, LOW)
        digitalWrite(19, LOW)
        digitalWrite(20, LOW)
        delay(100)