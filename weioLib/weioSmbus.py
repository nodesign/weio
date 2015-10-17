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


"""This module is implementation of smbus specification for IoTPY i2c driver """

from weioLib.weio import initI2C
from struct import pack, unpack


class SMBus(object):
    _i2c = None
    _addr = -1
    _compat = False
    I2C_FUNC_SMBUS_READ_BLOCK_DATA = 32

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

    def get_block_size(self):
        return self.I2C_FUNC_SMBUS_READ_BLOCK_DATA

    def set_block_size(self, block_size):
	self.I2C_FUNC_SMBUS_READ_BLOCK_DATA = block_size

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
        result = self._i2c.transaction(self._addr, pack('B', cmd), self.I2C_FUNC_SMBUS_READ_BLOCK_DATA)
        dataFlags = ""
        for flag in range(self.I2C_FUNC_SMBUS_READ_BLOCK_DATA):
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
        for flag in range(self.I2C_FUNC_SMBUS_READ_BLOCK_DATA):
            dataFlags+="B"

        result = self._i2c.transaction(self._addr, cmdString, self.I2C_FUNC_SMBUS_READ_BLOCK_DATA)

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
