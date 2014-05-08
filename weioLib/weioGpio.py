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

from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.adc import ADC
from IoTPy.pyuper.pwm import PWM
from IoTPy.pyuper.interrupt import Interrupt
from IoTPy.pyuper.utils import IoTPy_APIError, die
from weioLib import weioRunnerGlobals

import os

class WeioGpio():
    def __init__(self):
        self.declaredPins = []
        self.pwmPrecision = 255

        closed = True
        while closed:
            try:
                self.u = IoBoard()
                print "opened port"
                closed = False
            except IoTPy_APIError, e: # seems can't establish connection with the UPER board
                #details = e.args[0]
                closed = True
                #die(details)

        weioRunnerGlobals.WEIO_SERIAL_LINKED = True

    def inputMode(self, pin, mode) :
        """Sets input mode for digitalRead purpose. Available modes are : INPUT_HIGHZ, INPUT_PULLDOWN, INPUT_PULLUP"""
        gpio = self.u.get_pin(GPIO, pin)
        gpio.mode(mode)

    def digitalWrite(self, pin, state) :
        """Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground"""
        gpio = self.u.get_pin(GPIO, pin)
        gpio.write(state)

    def digitalRead(self,pin) :
        """Reads actual voltage on corresponding pin. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected"""
        gpio = self.u.get_pin(GPIO, pin)
        return gpio.read()

    def analogRead(self, pin) :
        """Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023"""
        adc = self.u.get_pin(ADC, pin)
        return adc.read()

    def pwmWrite(self, pin, value) :
        """Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 20000ms and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature look functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1."""
        pwm = self.u.get_pin(PWM, pin)
        value = 1.0/self.pwmPrecision*value
        pwm.write(value)

    def setPwmPeriod(self, pin, period):
        pwm = self.u.get_pin(PWM, pin)
        pwm.width_us(period)

    def analogWrite(self, pin,value):
        self.pwmWrite(pin,value)

    def analogWriteResolution(self, res):
        if (res==8):
            self.pwmPrecision = 255.0
        elif (res==16):
            self.pwmPrecision = 65535.0
        else:
            print "Only 8bit or 16bit precisions are allowed"

    def proportion(self, value,istart,istop,ostart,ostop) :
        return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))

    def attachInterrupt(self, pin, mode, callback):
        interrupt = self.u.get_pin(Interrupt, pin)
        interrupt.attach(mode, callback)

    def detachInterrupt(self, pin):
        pass

    def reset(self):
        weioRunnerGlobals.WEIO_SERIAL_LINKED = False
        self.u.reset()

    def stop(self):
        self.u.stop()

    def stopReader(self):
        self.u.reader.stop()
