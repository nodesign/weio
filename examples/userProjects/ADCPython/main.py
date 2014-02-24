from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared


def setup() :
    attach.process(loop)
    
def loop() :
    while True:
        val = analogRead(25)
        print val
        delay(20)
