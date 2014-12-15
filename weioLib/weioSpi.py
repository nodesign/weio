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
# Paul RATHGEB <paul.rathgeb@skynet.be
#
###
"""This module contains functions specifically written for IoTPY SPI driver """

from weioLib.weio import initSPI
from struct import pack, unpack

SPI_FUNC_READ_BLOCK_DATA = 32

class SPILib(object):
    _spi = None

    def __init__(self, port=0, divider=1, mode=0):
        self.open(port, divider, mode)

    def close(self):
        """close()

        Disconnects the object from the port.
        """
        self._spi = None

    def dealloc(self):
        self.close()

    def open(self, port, divider, mode):
        """open(port)

        Connects the object to the specified SPI port.
        """
        self._spi = initSPI(port, divider, mode)

    def read_byte(self):
        """read_byte(self) -> result

        Perform SPI Read Byte transaction.
        """
        result = self._spi.read(1)
        return unpack('B', result[0])[0]

    def write_byte(self, val):
        """write_byte(val)

        Perform SPI Write Byte transaction.
        """
        self._spi.write(pack('B', val))

    def read_byte_data(self, cmd):
        """read_byte_data(cmd) -> result

        Perform SPI Read Byte Data transaction.
        """
        result = self._spi.transaction(pack('BB', cmd, 0), read_from_slave=True)
        return unpack('B', result[0])[0]

    def write_byte_data(self, cmd, val):
        """write_byte_data(cmd, val)

        Perform SPI Write Byte Data transaction.
        """
        self._spi.write(pack('BB', cmd, val))

    def read_word_data(self, cmd):
        """read_word_data(cmd) -> result

        Perform SPI Read Word Data transaction.
        """
        result = self._spi.transaction(pack('BBH', cmd, val, 0), read_from_slave=True)
        return unpack('H', result[0])[0]

    def write_word_data(self, cmd, val):
        """write_word_data(cmd, val)

        Perform SPI Write Word Data transaction.
        """
        self._spi.transaction(pack('Bh', cmd, val), read_from_slave=True)

    def read_block_data(self, cmd):
        """read_block_data(cmd) -> results

        Perform SPI Read Block Data transaction.
        """
        receiveFlags = ""
        sendFlags = "B"
        for flag in range(SPI_FUNC_READ_BLOCK_DATA):
            sendFlags+="B"
            receiveFlags+="B"

        result = self._spi.transaction(pack(sendFlags, cmd, char(0)*SPI_FUNC_READ_BLOCK_DATA), read_from_slave=True)
        return list(unpack(receiveFlags, result[0]))

    def write_block_data(self, cmd, vals):
        """write_block_data(cmd, vals)

        Perform SPI Write Block Data transaction.
        """
        cmdString = pack('B', cmd)
        for val in vals:
            cmdString+=pack('B', val)
        self._spi.transaction(cmdString, read_from_slave=False)
