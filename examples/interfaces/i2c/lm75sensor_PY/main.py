#######################################################
#                                                     #
#   Read temperature in C using i2c sensor LM75       #
#   Use pullup resistors 4k7 for SDA and SCL signals  #
#                                                     #
#######################################################

from weioLib.weio import *
from things.input.environmental.lm75 import Lm75

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Init I2C object")
    i2c = initI2C()
    # scan i2c to discover your device
    print i2c.scan()
    
    # call lm75 library object and init with good address
    t = Lm75(72)
    
    while True:
        # print temperature
        print t.getTemperature()       
        delay(100)