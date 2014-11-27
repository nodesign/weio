### 
#
# WEIO Web Of Things Platform
# Copyright (C) 2013 Nodesign.net, Uros PETREVSKI, Drasko DRASKOVIC
# All rights reserved
#
#               ##      ## ######## ####  #######  
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ######    ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#                ###  ###  ######## ####  #######
#
#                    Web Of Things Platform 
#
# This file is part of WEIO
# WEIO is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WEIO is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

from weioLib.weio import *
import struct

class PowerModule:
    def __init__(self, port):
        if (port>1):
            print "Error! PowerModule can be only on ports 0 or 1"
        else :
            self.spi = initSPI(port) # init SPI on port 0 (pins : 2,3,4)

            if (port==0):
                self.latchPin = 5
            else :
                self.latchPin = 13

            self.output = 0

    def digitalWrite(self, pin, value):
        mask = value << (15-pin)
        self.output = self.output ^ mask
        self.fire()

    def portWrite(self, value): # 16 bit value here please
        self.output = self.reverseBits(value)
        self.fire()

    def fire(self):

        first = self.output & 0xFF
        second = (self.output>>8) & 0xFF

        digitalWrite(self.latchPin, LOW)
        self.spi.transaction(struct.pack("BB", first,second))
        digitalWrite(self.latchPin, HIGH)

    def reverseBits(self, x):
        x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
        x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
        x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
        x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8) # for 16bits
        #x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16) # for 32 bits etc..
        return x
