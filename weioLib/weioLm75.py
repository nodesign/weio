# LM75B thermometer driver

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
# This file is part of WEIO and is published under BSD license.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by the WeIO project.
# 4. Neither the name of the WeIO nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY WEIO PROJECT AUTHORS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL WEIO PROJECT AUTHORS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

from fcntl import ioctl
import struct
import platform
import time

class WeioLm75:

    # Kernel driver definition
    # SDA GPIO18
    # SCL GPIO19

    def __init__(self):

        if (platform.machine() == 'mips') :

            # file path
            filePath = "/dev/i2c-0"

            # from i2c-dev.h
            I2C_SLAVE = 0x0703

            # open file
            self.f = open(filePath, "r+")

            # LM75 addreess on weio board
            lm75addr = 0x48

            # set device address
            ioctl(self.f, I2C_SLAVE, lm75addr)

            # i2c device address
            self.deviceAddress = lm75addr
            # set instruction to get temperature - 0x0 to get temperature
            self.inst = struct.pack('B', 0x0)

    def getTemperature(self, unit="C"):
        if (platform.machine() == 'mips') :
            # ask for a temperature
            self.f.write(self.inst)

            # get two bytes as result
            rcv = self.f.read(2)

            # do data conversion see LM75B datasheet
            temp  = struct.unpack('B', rcv[0])[0] << 8
            temp |= struct.unpack('B', rcv[1])[0]

            temp >>= 5
            c = float(temp)*0.125
            if (unit is "C"):
                return c
            elif (unit is "K"):
                return c + 273.15
            elif (unit is "F"):
                return 1.8*c+32
            else:
                print "Bad unit. You can choose between C,K or F"
        else :
            print "This is fake temperature 25.123, testing purposes"
            return 25.123
# Example
# t = WeioLm75()
# while True :
#     print t.getTemperature()
#     time.sleep(0.1)

