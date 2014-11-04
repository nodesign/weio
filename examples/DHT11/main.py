from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    import time
    start = time.time()
    while True:
        a = dhtRead(8)
        result = a[0] + a[1] + a[2] + a[3]
        if result == a[4]:
            print "Measured at : %.0f" %(time.time()-start)
            print "Humidity = %d.%d"%(a[0], a[1])
            print "Temperature = %d.%d"%(a[2], a[3])
            print "--------------"
        else:
            print "Read error at %.0f" %(time.time()-start)
            print "Packet : ",a
            print "--------------"
        delay(5000)
