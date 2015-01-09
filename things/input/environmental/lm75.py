from struct import unpack
from weioLib.weio import *


class Lm75:
    def __init__(self, address=0x48):
        self.address = address
        self.i2c = initI2C()
    
    def getTemperature(self):
        val = self.i2c.transaction(self.address, "\x00", 2)
        temp = unpack('>H', val[0])[0]
        return temp/256.0