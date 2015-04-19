#######################################
#                                     #
#  HOW TO HAVE DHT11 SENSOR ON WEIO   #
#                                     #
#######################################

# Description: The DHT11 digital sensor is used to measure the ambient 
#              temperature and relative humidity. This example shows how 
#              the dhtRead function can be used to read the sensor.  
# syntax = dhtRead(pin) - available in all PIN's

from weioLib.weio import *

def setup():
    # attaches myProcess to infinite loop
    attach.process(myProcess)
    
def myProcess():
    # define input pin
    pin = 8
    # get start time
    startTime = time.time()
    # create infinite loop
    while True:
        # get data from sensor
        data = dhtRead(pin)
        # parse data
        result = data[0] + data[1] + data[2] + data[3]
        if result == data[4]:
            print "Measured at : %.0f" %(time.time()-startTime)
            print "Humidity = %d.%d"%(data[0], data[1])
            print "Temperature = %d.%d"%(data[2], data[3])
            print "--------------"
        else:
            print "Read error at %.0f" %(time.time()-startTime)
            print "Packet : ",data
            print "--------------"
        # wait 5 seconds    
        delay(5000)
