from weioLib.weio import *

def setup() :
    attach.event("webEvent", webEvent)

def webEvent(data):
    print "web event"
