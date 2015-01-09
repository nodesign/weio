###########################################
#                                         #
#    Thermometer LM75 on i2c bus          #
#    Use implementation of smbus for      #
#    WeIO to communicate to i2c devices   #
#                                         #
###########################################

from weioLib.weio import *
from weioLib.weioSmbus import SMBus

def setup():
    attach.process(myProcess)
    
def myProcess():

    # LM75 i2c address:
    addr = 0x4F
    
    i2c1 = SMBus()
    
    print "list i2c devices on the bus", i2c1.scan()
    
    while True:
        temp = i2c1.read_word_data(addr, 0)
        tempA = temp & 0xFF;
        tempB = (temp >> 8) & 0xFF
        temp = (tempA << 8) | tempB
        
        print "read: %04x = %.1f C (%.1f F)" % (temp, parse(temp), ctof(temp))
        delay(500)
        
def parse(t):
   # 9 bits of resolution stored in 2 bytes
   r = t >> 7
   # MSB set?
   if (t & 0x8000):
      # one's complement
      r = (~r & 0x1FF)
      # two's complement
      r = r - 1
      # significance: means negative temp
      r = -r
   r = r / 2.0
   return r
    
def ctof(t):
   return ((9.0/5.0) * parse(t)) + 32.0