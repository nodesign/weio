from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared

def setup() :
    attach.process(loop)
    
def loop(weioShared) :
    print "HELLO!!!"
    print weioShared.i
    print weioShared.s

    print "USER: " + str(weioShared.value.value)
    weioShared.qout.put("SET VALUE TO 10")

    time.sleep(1)

    print "USER: " + str(weioShared.value.value)

    #weioShared.qout.put("SET VALUE TO 2")
    #print "USER: " + str(weioShared.value.value)
