# This is port of smbus for python to IoTPY of WeIO project 
# port is done by Uros Petrevski
#
# smbus.py - cffi based python bindings for SMBus based on smbusmodule.c
# Copyright (C) 2013 <david.schneider@bivab.de>
#
# smbusmodule.c - Python bindings for Linux SMBus access through i2c-dev
# Copyright (C) 2005-2007 Mark M. Hoffman <mhoffman@lightlink.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

"""This module is a port of smbus for IoTPY i2c driver """

from weioLib.weio import initI2C
from struct import pack, unpack
from smbusUtil import validate

I2C_FUNC_SMBUS_READ_BLOCK_DATA = 32

class SMBus(object):
    """SMBus([bus]) -> SMBus
    Return a new SMBus object that is (optionally) connected to the
    specified I2C device interface.
    """

    i2c = None
    _addr = -1
    _pec = 0
    # compat mode, enables some features that are not compatible with the
    # original smbusmodule.c
    _compat = False

    def __init__(self, bus=-1):
        self.open(bus)

    def close(self):
        """close()

        Disconnects the object from the bus.
        """
        self.i2c = None
        self._addr = -1
        self._pec = 0

    def dealloc(self):
        self.close()

    def open(self, bus):
        """open(bus)

        Connects the object to the specified SMBus.
        """
        self.i2c = initI2C()

    def _set_addr(self, addr):
        """private helper method"""
        self._addr = addr

    @validate(addr=int)
    def write_quick(self, addr):
        """write_quick(addr)

        Perform SMBus Quick transaction.
        """
        self._set_addr(addr)
        # not sure if IoTPy supprts this option
        self.i2c.transaction(self._addr,"",0)

    @validate(addr=int)
    def read_byte(self, addr):
        """read_byte(addr) -> result

        Perform SMBus Read Byte transaction.
        """
        self._set_addr(addr)
        result = self.i2c.read(self._addr,1)
        return unpack('B', result[0])[0]

    @validate(addr=int, val=int)
    def write_byte(self, addr, val):
        """write_byte(addr, val)

        Perform SMBus Write Byte transaction.
        """
        self._set_addr(addr)
        self.i2c.write(self._addr, pack('B', val))

    @validate(addr=int, cmd=int)
    def read_byte_data(self, addr, cmd):
        """read_byte_data(addr, cmd) -> result

        Perform SMBus Read Byte Data transaction.
        """
        self._set_addr(addr)
        result = self.i2c.transaction(self._addr, pack('B', cmd), 1)
        return unpack('B', result[0])[0]

    @validate(addr=int, cmd=int, val=int)
    def write_byte_data(self, addr, cmd, val):
        """write_byte_data(addr, cmd, val)

        Perform SMBus Write Byte Data transaction.
        """
        self._set_addr(addr)
        self.i2c.transaction(self._addr, pack('BB', cmd, val), 0)

    @validate(addr=int, cmd=int)
    def read_word_data(self, addr, cmd):
        """read_word_data(addr, cmd) -> result

        Perform SMBus Read Word Data transaction.
        """
        self._set_addr(addr)
        result = self.i2c.transaction(self._addr, pack('BB', cmd, val), 2)
        return unpack('H', result[0])[0]

    @validate(addr=int, cmd=int, val=int)
    def write_word_data(self, addr, cmd, val):
        """write_word_data(addr, cmd, val)

        Perform SMBus Write Word Data transaction.
        """
        self._set_addr(addr)
        self.i2c.transaction(self._addr, pack('Bh', cmd, val), 0)

    @validate(addr=int, cmd=int, val=int)
    def process_call(self, addr, cmd, val):
        """process_call(addr, cmd, val)

        Perform SMBus Process Call transaction.

        Note: although i2c_smbus_process_call returns a value, according to
        smbusmodule.c this method does not return a value by default.

        Set _compat = False on the SMBus instance to get a return value.
        """
        self._set_addr(addr)
        if (self._compat) :
            self.i2c.transaction(self._addr, pack('BB', cmd, val), 0)
        else :
            result = self.i2c.transaction(self._addr, pack('BB', cmd, val), 1)
            return unpack('B', result[0])[0]

    @validate(addr=int, cmd=int)
    def read_block_data(self, addr, cmd):
        """read_block_data(addr, cmd) -> results

        Perform SMBus Read Block Data transaction.
        """
        self._set_addr(addr)
        result = self.i2c.transaction(self._addr, pack('BB', cmd, val), I2C_FUNC_SMBUS_READ_BLOCK_DATA)
        dataFlags = ""
        for flag in range(I2C_FUNC_SMBUS_READ_BLOCK_DATA):
            dataFlags+="B"
        return list(unpack(dataFlags, result[0]))

    @validate(addr=int, cmd=int, vals=list)
    def write_block_data(self, addr, cmd, vals):
        """write_block_data(addr, cmd, vals)

        Perform SMBus Write Block Data transaction.
        """
        self._set_addr(addr)

        cmdString = pack('B', cmd)
        for val in vals:
            cmdString+=pack('B', val)
        self.i2c.transaction(self._addr, cmdString, 0)


    @validate(addr=int, cmd=int, vals=list)
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

        result = self.i2c.transaction(self._addr, cmdString, I2C_FUNC_SMBUS_READ_BLOCK_DATA)

        return list(unpack(dataFlags, result[0]))

    @validate(addr=int, cmd=int, len=int)
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

        result = self.i2c.transaction(self._addr, cmdString, len)

        return list(unpack(dataFlags, result[0]))

    @validate(addr=int, cmd=int, vals=list)
    def write_i2c_block_data(self, addr, cmd, vals):
        """write_i2c_block_data(addr, cmd, vals)

        Perform I2C Block Write transaction.
        """
        self._set_addr(addr)
        self.write_block_data(addr,cmd,vals)

    @property
    def pec(self):
        # not supported by IoTPy
        return self._pec

    @pec.setter
    def pec(self, value):
        """True if Packet Error Codes (PEC) are enabled"""
        # not supported by IoTPy
        pass