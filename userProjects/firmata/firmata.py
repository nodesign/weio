#! /usr/bin/env python

"""
Python API for the Firmata protocol
Copyright (C) 2008  laboratorio (info@laboratorio.us)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = "0.3"

import time
import serial

DIGITAL_MESSAGE = 0x90 # send data for a digital port
ANALOG_MESSAGE = 0xE0 # send data for an analog pin (or PWM)
REPORT_ANALOG = 0xC0 # enable analog input by pin #
REPORT_DIGITAL = 0xD0 # enable digital input by port
SET_PIN_MODE = 0xF4 # set a pin to INPUT/OUTPUT/PWM/etc
REPORT_VERSION = 0xF9 # report firmware version
SYSTEM_RESET = 0xFF # reset from MIDI
START_SYSEX = 0xF0 # start a MIDI SysEx message
END_SYSEX = 0xF7 # end a MIDI SysEx message

# pin modes
INPUT = 0
OUTPUT = 1
PWM = 2
SERVO = 3

LOW = 0
HIGH = 1
MAX_DATA_BYTES = 32

class Arduino:
    
    def __init__(self, port, baudrate=115200):

        self.serial = serial.Serial(port, baudrate, bytesize=8, timeout=2)
        
        self.wait_for_data = 0
        self.exec_multibyte_cmd = 0
        self.multibyte_channel = 0
        self.stored_input_data = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0 ]
        self.parsing_sysex = False
        self.sysex_bytes_read = 0
        self.digital_output_data =  [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        self.digital_input_data  = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        self.analog_input_data = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
        self.major_version = 0
        self.minor_version = 0
        self.__report()
        
    def __str__(self):
        return "Arduino: %s" % self.serial.port

    def pin_mode(self, pin, mode):
        """Setting mode to pin"""
        self.serial.write(chr(SET_PIN_MODE))
        self.serial.write(chr(pin))
        self.serial.write(chr(mode))

    def digital_read(self, pin):
        """Reading from digital pin"""
        return (self.digital_input_data[pin >> 3] >> (pin & 0x07)) & 0x01

    def digital_write(self, pin, value):
        """Writing to a digital pin"""
        
        port_number = (pin >> 3) & 0x0F
        
        if value == 0:
          self.digital_output_data[port_number] = self.digital_output_data[port_number] & ~(1 << (pin & 0x07))
        else:
          self.digital_output_data[port_number] = self.digital_output_data[port_number] | (1 << (pin & 0x07))

        self.serial.write(chr(DIGITAL_MESSAGE | port_number))
        self.serial.write(chr(self.digital_output_data[port_number] & 0x7F))
        self.serial.write(chr(self.digital_output_data[port_number] >> 7))

    def analog_read(self, pin):
        """Reading from analog pin"""
        return self.analog_input_data[pin]

    def analog_write(self, pin, value):
        """Writing to a analog pin"""
        self.serial.write(chr(ANALOG_MESSAGE | (pin & 0x0F)))
        self.serial.write(chr(value & 0x7F))
        self.serial.write(chr(value >> 7))
    
    def set_version(self, major, minor):
        """Setting a minor and major version"""
        self.major_version = major
        self.minor_version = minor

    def available(self):
        """Checking serial connection status"""
        return self.serial.isOpen()

    def delay(self, secs):
        """Waiting in seconds"""
        time.sleep(secs)
        
    def parse(self):
        """Preparing the data to be handled"""
        data = self.serial.read()
        if data != "":
            self.__process(ord(data))

    def __process(self, input_data):
        """Handling input data"""
        command = None
        
        if self.parsing_sysex:
            if input_data == END_SYSEX:
                self.parsing_sysex = False
            else:
                self.stored_input_data[self.sysex_bytes_read] = input_data
                self.sysex_bytes_read += 1
                
        elif self.wait_for_data > 0 and input_data < 128:
            self.wait_for_data -= 1
            self.stored_input_data[self.wait_for_data] = input_data

            if self.exec_multibyte_cmd != 0 and self.wait_for_data == 0:
                if self.exec_multibyte_cmd ==  DIGITAL_MESSAGE:
                    self.digital_input_data[self.multibyte_channel] = (self.stored_input_data[0] << 7) + self.stored_input_data[1]
                elif self.exec_multibyte_cmd ==  ANALOG_MESSAGE:
                    self.analog_input_data[self.multibyte_channel] = (self.stored_input_data[0] << 7) + self.stored_input_data[1]
                elif self.exec_multibyte_cmd ==  REPORT_VERSION:
                    self.set_version(self.stored_input_data[1], self.stored_input_data[0])
        else:
            if input_data < 0xF0:
                command = input_data & 0xF0
                self.multibyte_channel = input_data & 0x0F
            else:
                command = input_data # commands in the 0xF* range don't use channel data

            if command == DIGITAL_MESSAGE or \
                command == ANALOG_MESSAGE or \
                command == REPORT_VERSION:
                self.wait_for_data = 2
                self.exec_multibyte_cmd = command

    def __report(self):
        """Reporting analog and digital pins"""

        self.delay(2)
        for port in range(6):
            self.serial.write(chr(REPORT_ANALOG | port))
            self.serial.write(chr(1))
            
        for port in range(2):
            self.serial.write(chr(REPORT_DIGITAL | port))
            self.serial.write(chr(1))