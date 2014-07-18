from weioLib.weioIO import *
from weioLib.weioUserApi import attach


def setup() :
    attach.event("webEvent", webEvent)

def webEvent(data):
    print "web event"
