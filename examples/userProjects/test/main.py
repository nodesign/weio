from weioLib.weioIO import *
from weioLib.weioUserApi import attach

class ClientMessage():
    def __init__(self):
        self.uid = None
        self.msg = ""

def setup() :
    attach.process(loop)
    
def loop(weioShared) :
    print "HELLO!!!"
    #print weioShared.i
    #print weioShared.s

    print "USER: " + str(weioShared.val.value)

    msg = ClientMessage()
    msg.uid = 100
    msg.msg = "HELLO THERE"
    weioShared.qout.put(msg)

    time.sleep(1)

    print "USER: " + str(weioShared.val.value)

    #weioShared.qout.put("SET VALUE TO 2")
    #print "USER: " + str(weioShared.value.value)
