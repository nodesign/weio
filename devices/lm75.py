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

import os
from fcntl import ioctl
import struct
import platform

# i2c device address
deviceAddress = 0x4f
# set instruction to get temperature - 0x0 to get temperature
inst = struct.pack('B', 0x0)

# file path
filePath = "/dev/i2c-0"

# from i2c-dev.h
I2C_SLAVE = 0x0703

# file descriptor
global f

def __init__():
   
    if (platform.machine() == 'mips') :
        global f    
        # open file
        f = open(filePath, "r+")

        # set device address
        ioctl(f, I2C_SLAVE, 0x4f)
    
def getTemperature():
    if (platform.machine() == 'mips') :
        # ask for a temperature
        f.write(inst)

        # get two bytes as result
        rcv = f.read(2)
    
        # do data conversion see LM75B datasheet
        temp  = struct.unpack('B', rcv[0])[0] << 8
        temp |= struct.unpack('B', rcv[1])[0]

        temp >>= 5
        return float(temp)*0.125
    else :
        print "This is fake temperature 25.123, only for testing purposes on this architecture"
        return 25.123
