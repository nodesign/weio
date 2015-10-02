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


"""This module contains functions specifically written for IoTPY SPI driver """

from weioLib.weio import initSPI
from struct import pack, unpack


class SPILib(object):
    _spi = None
    SPI_FUNC_READ_BLOCK_DATA = 32

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

    def get_block_size(self):
        return self.SPI_FUNC_READ_BLOCK_DATA

    def set_block_size(self, block_size):
	self.SPI_FUNC_READ_BLOCK_DATA = block_size

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
        result = self._spi.transaction(pack('B', cmd), read_from_slave=True)
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
	cmdString = pack('B', cmd)
        for flag in range(self.SPI_FUNC_READ_BLOCK_DATA):
            cmdString+=pack('B', 0)
            receiveFlags+="B"

        result = self._spi.transaction(cmdString, read_from_slave=True)
        return list(unpack(receiveFlags, result[0]))

    def write_block_data(self, cmd, vals):
        """write_block_data(cmd, vals)

        Perform SPI Write Block Data transaction.
        """
        cmdString = pack('B', cmd)
        for val in vals:
            cmdString+=pack('B', val)
        self._spi.transaction(cmdString, read_from_slave=False)
