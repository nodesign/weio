from weioLib.weioIO import *
from weioLib.weioUserApi import attach, HIGH, LOW, shared

import time

def setup() :
    attach.process(blinky)

def blinky() :
    cadence = 0.1
    while True:
        digitalWrite(20, HIGH)
        time.sleep(cadence)
        digitalWrite(20, LOW)
        time.sleep(cadence)
