from weioLib.weioIO import *
from weioLib.weioUserApi import attach, HIGH, LOW, shared

import time

def setup() :
    attach.event("pera", peraEvent)

def peraEvent(data):
    print "Jednom Pera"
    #time.sleep(1)
    print "Uvek Pera"
