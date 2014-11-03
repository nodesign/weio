#######################################
#                                     #
#   how to use I2C on WEIO //LM75     #
#                                     #
#######################################

#syntax:
#transaction(address, write_data, read_length, ignore_error=False)
#scan()

#it's exemple to show how to use LM75 sensor with I2C communication 

from struct import unpack
from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcess)
    
def myProcess():
    i = initI2c()
    while True:
        a=i.scan() #scan of I2C devices connected on board 
        print a
        print int(a[0])
        #print int(a[1])
        delay(500) #optional 
        result_raw = i.transaction(0x48,'\x00', 2)
        result_integer = unpack('>H', result_raw)[0]
        print result_integer / 256.0 #print the value converted to have degree 
        delay(500) #optional 
        result_raw = i.transaction(0x00,'\x00', 2)
        result_raw = i.transaction(0x00,'\x00', 2)
        result_raw = i.transaction(0x00,'\x00', 2)
        delay(500) #optional 


