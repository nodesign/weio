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

from struct import unpack
from IoTPy.pyuper.utils import IoTPy_ThingError


SI70xx_CMD_RH_HOLD      = '\xE5'  # RH hold master mode
SI70xx_CMD_RH_NOHOLD    = '\xF5'  # RH no hold master mode
SI70xx_CMD_TEMP_HOLD    = '\xE3'  # temp hold master mode
SI70xx_CMD_TEMP_NOHOLD  = '\xF3'  # temp no hold master mode
SI70xx_CMD_ANALOG       = '\xEE'  #
SI70xx_CMD_TEMP_PREVIOUS= '\xE0'  # temp from previous measurement

SI70xx_CMD_RESET        = '\xFE'  # reset

SI70xx_CMD_WRITE_REG1   = '\xE6'  # write user register 1 (RH/T setup)
SI70xx_CMD_READ_REG1    = '\xE7'  # read user register 1 (RH/T setup)
SI70xx_CMD_WRITE_REG2   = '\x50'  # write user register 2 (Analog setup)
SI70xx_CMD_READ_REG2    = '\x10'  # read user register 2 (Analog setup)
SI70xx_CMD_WRITE_REG3   = '\x51'  # write user register 3 (Heater setup)
SI70xx_CMD_READ_REG3    = '\x11'  # read user register 3 (Heater setup)
SI70xx_CMD_WRITE_TCC    = '\xC5'  # write thermistor correction coefficient
SI70xx_CMD_READ_TCC     = '\x84'  # read thermistor correction coefficient

SI70xx_CMD_READ_ID1     = '\xFA\x0F'  # read ID 1st byte
SI70xx_CMD_READ_ID2     = '\xFC\xC9'  # read ID 2nd byte
SI70xx_CMD_FW_REVISION  = '\x84\xB8'  # get firmware revision


class Si7013:
    """
    Si7013 humidity and temperature sensor class.

    :param interface:  I2C communication interface.
    :type interface: :class:`IoTPy.pyuper.i2c.I2C`
    :param int address: Si7013 sensor I2C address. Optional, default 0x40 (64)
    """

    def __init__(self, interface, address=0x40):
        self.interface = interface
        self.address = address

    def __enter__(self):
        return self

    def temperature(self):
        """
        Read, convert and return temperature.

        :return: Temperature value in celsius.
        :rtype: float
        :raise: IoTPy_ThingError
        """
        try:
            result_raw = self.interface.transaction(self.address, SI70xx_CMD_TEMP_HOLD, 2)
            result_integer = unpack('>H', result_raw[:2])[0]
            temp = (175.72 * result_integer)/65536 - 46.85
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - temperature reading error.")
        return temp

    def humidity(self):
        """
        Read, convert and return humidity.

        :return: Humidity value in percent.
        :rtype: float
        :raise: IoTPy_ThingError
        """
        try:
            result_raw = self.interface.transaction(self.address, SI70xx_CMD_RH_HOLD, 2)
            result_integer = unpack('>H', result_raw[:2])[0]
            rh = (125.0 * result_integer)/65536 - 6
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - humidity reading error.")
        return rh

    def analog(self):
        """
        Read, convert and return analog sensor value.

        :return: Analog ADC value
        :rtype: int
        :raise: IoTPy_ThingError
        """
        try:
            result_raw = self.interface.transaction(self.address, SI70xx_CMD_ANALOG, 2)
            result_integer = unpack('>H', result_raw[:2])[0]
            return result_integer
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - analog reading error.")

    def __exit__(self, ex_type, ex_value, traceback):
        pass


class Si7020:
    """
    Si7020 humidity and temperature sensor class.

    :param interface:  I2C communication interface.
    :type interface: :class:`IoTPy.pyuper.i2c.I2C`
    :param int address: Si7020 sensor I2C address. Optional, default 0x40 (64)
    """

    def __init__(self, interface, address=0x40):
        self.interface = interface
        self.address = address

    def __enter__(self):
        return self

    def temperature(self):
        """
        Read, convert and return temperature.

        :return: Temperature value in celsius.
        :rtype: float
        :raise: IoTPy_ThingError
        """
        try:
            result_raw = self.interface.transaction(self.address, SI70xx_CMD_TEMP_HOLD, 2)
            result_integer = unpack('>H', result_raw[:2])[0]
            temp = (175.72 * result_integer)/65536 - 46.85
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - temperature reading error.")
        return temp

    def humidity(self):
        """
        Read, convert and return humidity.

        :return: Humidity value in percent.
        :rtype: float
        :raise: IoTPy_ThingError
        """
        try:
            result_raw = self.interface.transaction(self.address, SI70xx_CMD_RH_HOLD, 2)
            result_integer = unpack('>H', result_raw[:2])[0]
            rh = (125.0 * result_integer)/65536 - 6
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - humidity reading error.")
        return rh

    def __exit__(self, ex_type, ex_value, traceback):
        pass