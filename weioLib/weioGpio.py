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
from time import sleep
from IoTPy.pyuper.weio import WeIO
from IoTPy.core.gpio import GPIO
from IoTPy.core.adc import ADC
from IoTPy.core.pwm import PWM
from weioLib import weioRunnerGlobals
import signal, time,sys

import os

class WeioGpio():
    def __init__(self):
        # set all pins to -1 (nothing selected), this is just information no real action on pins will be performed
        weioRunnerGlobals.DECLARED_PINS = []
        for a in range(32):
            weioRunnerGlobals.DECLARED_PINS.append(-1)

        self.pwmPrecision = 255
        numberOfTries = 1000
        cnt = 0
        closed = True
        # This array will keep interrupt object on corresponding pin number
        self.interrupts = []
        for i in range(32):
            self.interrupts.append(None)
        while closed:
            try:
                self.u = WeIO()
                #print "opened port"
                closed = False
                weioRunnerGlobals.WEIO_SERIAL_LINKED = True
            except IoTPy_APIError, e: # seems can't establish connection with the UPER board
                #details = e.args[0]
                closed = True
                weioRunnerGlobals.WEIO_SERIAL_LINKED = False
                cnt = cnt+1
                if (cnt>numberOfTries):
                    closed = False
                    print "uper not present"
                #die(details)

        # This array represents all gpio objects they are keeping their last state that can be easily followed
        self.mainGpio = []
        for i in range(len(self.u.pinout)):
            pin = self.u.GPIO(i)
            self.mainGpio.append(pin)

    def pinMode(self, pin, mode) :
        """Sets input mode for digitalRead purpose. Available modes are : INPUT, PULL_DOWN, PULL_UP"""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT
        gpio = self.mainGpio[pin]
        if (mode is GPIO.OUTPUT):
            gpio.setup(GPIO.OUTPUT)
        else :
            gpio.setup(GPIO.INPUT, mode)

    def portMode(self, port, mode) :
        """Sets input mode for portRead purpose. Available modes are : INPUT, PULL_DOWN, PULL_UP"""
        for i in range(8):
            pin = (8 * port) + i
            gpio = self.mainGpio[pin]
            weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT
            if (mode is GPIO.OUTPUT):
                gpio.port_mode(GPIO.OUTPUT, port)
            else:
                gpio.port_mode(GPIO.INPUT, port, mode)

    def digitalWrite(self, pin, state) :
        """Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground"""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.OUTPUT
        gpio = self.mainGpio[pin]
        #gpio.setup(GPIO.OUTPUT)
        gpio.write(state)

    def digitalRead(self,pin) :
        """Reads actual voltage on corresponding pin. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected"""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT
        gpio = self.mainGpio[pin]
        return gpio.read()

    def portWrite(self, port, value) :
        """Sets voltage to +3.3V or Ground on corresponding port. This function takes two parameters : port number and a byte representing the port value"""
        for i in range(8):
            pin = (8 * port) + i
            weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.OUTPUT
            gpio = self.mainGpio[pin]
        gpio.write_port(value, port)

    def portRead(self,port, mode=GPIO.NONE) :
        """Reads actual voltage on corresponding port. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected"""
        for i in range(8):
            pin = (8 * port) + i
            weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT
            gpio = self.mainGpio[pin]
        return gpio.read_port(port)

    def analogRead(self, pin) :
        """Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023"""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT
        adc = self.u.ADC(pin)
        return int(adc.read()*1023)

    def dhtRead(self, pin) :
        """Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023"""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT
        gpio = self.mainGpio[pin]
        return gpio.dht_read()

    def pwmWrite(self, pin, value) :
        """Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 20000ms and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature look functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1."""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.OUTPUT
        pwm = self.u.PWM(pin)
        pwm.set_duty_cycle(value)

    def pwmDutyCycle(self, pin, value) :
        """Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 20000ms and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature look functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1."""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.OUTPUT
        pwm = self.u.PWM(pin)
        pwm.set_duty_cycle(value)

    def setPwmFrequency(self, pin, value) :
        """Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 20000ms and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature look functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1."""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.OUTPUT

        pwm = self.u.PWM(pin)
        pwm.set_frequency(value)

    def setPwmPulseTime(self, pin, value) :
        """Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 20000ms and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature look functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1."""
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.OUTPUT
        pwm = self.u.PWM(pin)
        pwm.set_pulse_time(value)

    def setPwmPeriod(self, pin, period):
        pwm = self.u.PWM(pin)
        pwm.set_period(period)

    def analogWrite(self, pin,value):
        self.pwmWrite(pin,value)

    def setPwmLimit(self, limit):
        if (limit>65535.0):
            self.pwmPrecision = 65535.0
        elif (limit<=0):
            self.pwmPrecision = 0.1
        else:
            self.pwmPrecision = limit

    def analogWriteResolution(self, res):
        if (res==8):
            self.pwmPrecision = 255.0
        elif (res==16):
            self.pwmPrecision = 65535.0
        else:
            sys.stderr.write("Only 8bit or 16bit precisions are allowed")

    def attachInterrupt(self, pin, mode, callback, obj):
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT

        interrupt = self.mainGpio[pin]
        interrupt.attach_irq(mode, callback, obj)
        self.interrupts[pin] = interrupt

    def detachInterrupt(self, pin):
        interrupt = self.interrupts[pin]
        if not(interrupt is None):
            interrupt.detach_irq()
            self.interrupts[pin] = None

    def reset(self):
        weioRunnerGlobals.WEIO_SERIAL_LINKED = False
        self.u.reset()
        self.u.ser.close()

    def stop(self):
        weioRunnerGlobals.WEIO_SERIAL_LINKED = False
        self.u.stop()

    def stopReader(self):
        self.u.reader.stop()

    def tone(self, pin, frequency, duration = 0):
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.OUTPUT
        pwm = self.u.PWM(pin)
        pwm.set_frequency(frequency)
        pwm.set_duty_cycle(50)
        if(duration > 0):
           sleep(duration*0.001)
           pwm.set_period(10000)
           pwm.set_duty_cycle(0)

    def pulseIn(self, pin, level=GPIO.HIGH, timeout=100000):
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT
        gpio = self.mainGpio[pin]
        return gpio.read_pulse(level, timeout)

    def noTone(self, pin):
        pwm = self.u.PWM(pin)
        pwm.set_period(10000)
        pwm.set_duty_cycle(0)

    def millis(self):
        a = 1000*time.time()
        return a


