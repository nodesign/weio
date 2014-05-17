from weioLib.weioIO import *
from weioLib.weioUserApi import attach, weioShared, clientSend



def setup() :
    attach.process(loop)
    
def loop() :
    print "HELLO!!!"
    #print weioShared.i
    #print weioShared.s

    weioShared.setVal(0, 22)
    print "USER: " + str(weioShared.getVal(0))

    clientSend(100, "HOHOHOHOHOHO")

    time.sleep(1)

    print "USER: " + str(weioShared.getVal(0))

    #weioShared.qout.put("SET VALUE TO 2")
    #print "USER: " + str(weioShared.value.value)
