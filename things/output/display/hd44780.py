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
# Paul RATHGEB <paul.rathgeb@skynet.be>
#
###

from weioLib.weio import *

LCD_RS = 0x40
LCD_EN = 0x20
LCD_CMD = 0
LCD_STR = 1

class Hd44780:
    LINE1 = 0x80                                                       
    LINE2 = 0xC0 
    
    def __init__(self, port):
        self.port = port
        portMode(self.port, OUTPUT)

        # Initialise display
        self.__lcd_byte(0x33, LCD_CMD)
        self.__lcd_byte(0x32, LCD_CMD)
        self.__lcd_byte(0x28, LCD_CMD)
        self.__lcd_byte(0x0C, LCD_CMD)
        self.__lcd_byte(0x06, LCD_CMD)
        self.__lcd_byte(0x01, LCD_CMD)  
        
    def selectLine(self, line):
        self.__lcd_byte(line, LCD_CMD)

    def writeString(self, message):
        # Send string to display
    
        message = message.ljust(16," ")  
        
        for i in range(16):
            self.__lcd_byte(ord(message[i]),LCD_STR)
        
    def __lcd_byte(self, bits, mode):
        msg = 0
        if mode:
            msg = (LCD_RS | (bits >> 4))
        else:
            msg = (bits >> 4)
        portWrite(self.port, msg)
                                
        msg = msg + LCD_EN
        portWrite(self.port, msg)
        msg = msg - LCD_EN
        portWrite(self.port, msg)
                                                    
        msg = 0
        if mode:
            msg = (LCD_RS | (bits & 0x0F))
        else:
            msg = (bits & 0x0F)
        portWrite(self.port, msg)
                                                                                   
        msg = msg + LCD_EN
        portWrite(self.port, msg)
        msg = msg - LCD_EN
        portWrite(self.port, msg)
