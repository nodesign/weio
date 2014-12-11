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
"""This module is implementation of smbus specification for IoTPY i2c driver """

from weioLib.weio import initI2C
from struct import pack, unpack

I2C_FUNC_SMBUS_READ_BLOCK_DATA = 32

class SMBus(object):
    _i2c = None
    _addr = -1
    _compat = False

    def __init__(self, bus=-1):
        # WeIO don't care about bus as there is only one.
        # this argument is keeped for compatibility with existing sw
        self.open(bus)

    def close(self):
        """close()

        Disconnects the object from the bus.
        """
        self._i2c = None
        self._addr = -1
        self._pec = 0

    def dealloc(self):
        self.close()

    def open(self, bus):
        """open(bus)

        Connects the object to the specified SMBus.
        """
        self._i2c = initI2C()

    def _set_addr(self, addr):
        """private helper method"""
        self._addr = addr

    def scan(self):
        """scan()

        Perform SMBus devices discovery. Returns array of addresses
        """
        return self._i2c.scan()
        
    def write_quick(self, addr):
        """write_quick(addr)

        Perform SMBus Quick transaction.
        """
        self._set_addr(addr)
        # not sure if IoTPy supprts this option
        self._i2c.transaction(self._addr,"",0)

    def read_byte(self, addr):
        """read_byte(addr) -> result

        Perform SMBus Read Byte transaction.
        """
        self._set_addr(addr)
        result = self._i2c.read(self._addr,1)
        return unpack('B', result[0])[0]

    def write_byte(self, addr, val):
        """write_byte(addr, val)

        Perform SMBus Write Byte transaction.
        """
        self._set_addr(addr)
        self._i2c.write(self._addr, pack('B', val))

    def read_byte_data(self, addr, cmd):
        """read_byte_data(addr, cmd) -> result

        Perform SMBus Read Byte Data transaction.
        """
        self._set_addr(addr)
        result = self._i2c.transaction(self._addr, pack('B', cmd), 1)
        return unpack('B', result[0])[0]

    def write_byte_data(self, addr, cmd, val):
        """write_byte_data(addr, cmd, val)

        Perform SMBus Write Byte Data transaction.
        """
        self._set_addr(addr)
        self._i2c.transaction(self._addr, pack('BB', cmd, val), 0)

    def read_word_data(self, addr, cmd):
        """read_word_data(addr, cmd) -> result

        Perform SMBus Read Word Data transaction.
        """
        self._set_addr(addr)
        result = self._i2c.transaction(self._addr, pack('B', cmd), 2)
        return unpack('H', result[0])[0]

    def write_word_data(self, addr, cmd, val):
        """write_word_data(addr, cmd, val)

        Perform SMBus Write Word Data transaction.
        """
        self._set_addr(addr)
        self._i2c.transaction(self._addr, pack('Bh', cmd, val), 0)

    def process_call(self, addr, cmd, val):
        """process_call(addr, cmd, val)

        Perform SMBus Process Call transaction.

        Note: although i2c_smbus_process_call returns a value, according to
        smbusmodule.c this method does not return a value by default.

        Set _compat = False on the SMBus instance to get a return value.
        """
        self._set_addr(addr)
        if (self._compat) :
            self._i2c.transaction(self._addr, pack('BB', cmd, val), 0)
        else :
            result = self._i2c.transaction(self._addr, pack('BB', cmd, val), 1)
            return unpack('B', result[0])[0]

    def read_block_data(self, addr, cmd):
        """read_block_data(addr, cmd) -> results

        Perform SMBus Read Block Data transaction.
        """
        self._set_addr(addr)
        result = self._i2c.transaction(self._addr, pack('BB', cmd, val), I2C_FUNC_SMBUS_READ_BLOCK_DATA)
        dataFlags = ""
        for flag in range(I2C_FUNC_SMBUS_READ_BLOCK_DATA):
            dataFlags+="B"
        return list(unpack(dataFlags, result[0]))

    def write_block_data(self, addr, cmd, vals):
        """write_block_data(addr, cmd, vals)

        Perform SMBus Write Block Data transaction.
        """
        self._set_addr(addr)

        cmdString = pack('B', cmd)
        for val in vals:
            cmdString+=pack('B', val)
        self._i2c.transaction(self._addr, cmdString, 0)


    def block_process_call(self, addr, cmd, vals):
        """block_process_call(addr, cmd, vals) -> results

        Perform SMBus Block Process Call transaction.
        """
        self._set_addr(addr)
        cmdString = pack('B', cmd)
        for val in vals:
            cmdString+=pack('B', val)

        dataFlags = ""
        for flag in range(I2C_FUNC_SMBUS_READ_BLOCK_DATA):
            dataFlags+="B"

        result = self._i2c.transaction(self._addr, cmdString, I2C_FUNC_SMBUS_READ_BLOCK_DATA)

        return list(unpack(dataFlags, result[0]))

    def read_i2c_block_data(self, addr, cmd, len=32):
        """read_i2c_block_data(addr, cmd, len=32) -> results

        Perform I2C Block Read transaction.
        """
        self._set_addr(addr)
        cmdString = pack('B', cmd)
        for val in vals:
            cmdString+=pack('B', val)

        dataFlags = ""
        for flag in range(len):
            dataFlags+="B"

        result = self._i2c.transaction(self._addr, cmdString, len)

        return list(unpack(dataFlags, result[0]))

    def write_i2c_block_data(self, addr, cmd, vals):
        """write_i2c_block_data(addr, cmd, vals)

        Perform I2C Block Write transaction.
        """
        self._set_addr(addr)
        self.write_block_data(addr,cmd,vals)
