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

from time import sleep
from IoTPy.pyuper.weio import WeIO
from IoTPy.core.gpio import GPIO
from IoTPy.core.adc import ADC
from IoTPy.core.pwm import PWM
from weioLib import weioRunnerGlobals
from IoTPy.pyuper.utils import IoTPy_APIError, errmsg
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

    def HCSR04Read(self, trigger, pulse) :
        """Read the distance from a HC-SR04 ultrasonic distance sensor"""
        weioRunnerGlobals.DECLARED_PINS[trigger] = GPIO.OUTPUT
        weioRunnerGlobals.DECLARED_PINS[pulse] = GPIO.INPUT
        gpio = self.mainGpio[trigger]
        return gpio.hc_sr04_read(self.mainGpio[trigger].logical_pin, self.mainGpio[pulse].logical_pin)

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

    def attachInterrupt(self, pin, mode, callback, obj=None, debounceTime=10):
        weioRunnerGlobals.DECLARED_PINS[pin] = GPIO.INPUT

        interrupt = self.mainGpio[pin]
        interrupt.attach_irq(mode, callback, obj, debounceTime)
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


