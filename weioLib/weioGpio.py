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

from devices import uper
from weioLib.weioUserApi import shared, pins, adcs, pwms, HIGH, LOW, INPUT_HIGHZ, INPUT_PULLDOWN, INPUT_PULLUP, OUTPUT, ADC_INPUT, PWM_OUTPUT, PWM0_OUTPUT, PWM1_OUTPUT
from weioLib.weioUserApi import CHANGE, RISING, FALLING, HARD_INTERRUPTS
import os

class WeioGpio():
    
    def __init__(self):
        # construct uper device, open serial port
        # send default values
        if (os.path.exists("/dev/ttyACM0")) :
            self.uper = uper.UPER(self.mainInterrupt)
        else :
            print "*SYSOUT*Error! LPC coprocessor not present!"
            self.uper = None
            
        shared.declaredPins = []
        for i in range(0,len(pins)):
            shared.declaredPins.append(-1)
        
        self.pwm0PortPeriod = 1000
        self.pwm1PortPeriod = 1000
        
        self.pwm0Limit = 255
        self.pwm1Limit = 255
        
        self.pwm0BeginCalled = False
        self.pwm1BeginCalled = False
        
        
        self.interrupts = []
        for i in range(0,HARD_INTERRUPTS):
            # 1 is available
            self.interrupts.append(None)
    
    #print "Hello from GPIO"
    
    def mainInterrupt(self, data):
        myid = data[1][0]
        for inter in self.interrupts:
            if inter.myid == myid:
                inter.callback(data[1][1])
                break
    
    def inputMode(self, pin, mode) :
        """Sets input mode for digitalRead purpose. Available modes are : INPUT_HIGHZ, INPUT_PULLDOWN, INPUT_PULLUP"""
        self.uper.setPrimary(pins[pin])
        self.uper.pinMode(pins[pin], mode)
        shared.declaredPins[pin] = mode
    
    def digitalWrite(self,pin, state) :
        """Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground"""
        if shared.declaredPins[pin] != OUTPUT:
            self.uper.setPrimary(pins[pin])
            self.uper.pinMode(pins[pin], OUTPUT)
            shared.declaredPins[pin] = OUTPUT
        
        self.uper.digitalWrite(pins[pin], state)
    
    def digitalRead(self,pin) :
        """Reads actual voltage on corresponding pin. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected"""
        if (shared.declaredPins[pin] != INPUT_HIGHZ) and (shared.declaredPins[pin] != INPUT_PULLUP) and (shared.declaredPins[pin] != INPUT_PULLDOWN) :
            self.uper.setPrimary(pins[pin])
            self.uper.pinMode(pins[pin], INPUT_HIGHZ)
            shared.declaredPins[pin] = INPUT_HIGHZ
        
        return self.uper.digitalRead(pins[pin])
    
    def analogRead(self, pin) :
        """Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023"""
        if ((pin >= adcs[0]) and (pin <= adcs[-1])):
            if shared.declaredPins[pin] != ADC_INPUT:
                self.uper.setSecondary(pins[pin])
                shared.declaredPins[pin] = ADC_INPUT
            
            adcPin = adcs.index(pin)
            return self.uper.analogRead(adcPin)
        else :
            print "*SYSOUT*Error! Pin " + str(pin) + " is not ADC pin, ADCs are on pins 25-32!"
            return -1           
    
    def pwmWrite(self, pin, value) :
        """Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 20000ms and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature look functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1."""
        if ((pin >= pwms[0]) and (pin <= pwms[2])):
            #port0
            if shared.declaredPins[pin] != PWM0_OUTPUT:
                self.uper.setSecondary(pins[pin])
                #print "DECLARED pin ", pin, " called ", pins[pin]
                if self.pwm0BeginCalled is False:
                    self.uper.pwm0_begin(self.pwm0PortPeriod)
                    self.pwm0BeginCalled = True
                
                shared.declaredPins[pin] = PWM0_OUTPUT
            
            pwmPin = pwms.index(pin)
            
            # Security limiters
            if (value < 0) :
                value = self.pwm0Limit
            if (value > self.pwm0Limit):
                value = 0
            
            out = self.proportion(value, 0, self.pwm0Limit, self.pwm0PortPeriod, 0)
            self.uper.pwm0_set(pwmPin, int(out))
        #print "PWM on ", pwmPin, " value ", out
        
        elif ((pin >= pwms[3]) and (pin <= pwms[-1])):
            #port1
            if shared.declaredPins[pin] != PWM1_OUTPUT:
                self.uper.setSecondary(pins[pin])
                if self.pwm1BeginCalled is False:
                    self.uper.pwm1_begin(self.pwm1PortPeriod)
                    self.pwm1BeginCalled = True
                
                shared.declaredPins[pin] = PWM1_OUTPUT
            #print "PWM index ", pwms.index(pin)
            pwmPin = abs(3-pwms.index(pin))
            
            # Security limiters
            if (value < 0) :
                value = self.pwm0Limit
            if (value > self.pwm0Limit):
                value = 0
            
            out = self.proportion(value, 0, self.pwm1Limit, self.pwm1PortPeriod, 0)
            self.uper.pwm1_set(pwmPin, int(out))
        #print "PWM on ", pwmPin, " value ", out
        
        else :
            print "*SYSOUT*Error! Pin " + str(pin) + " is not PWM pin, PWMs are on pins 19-24!"
    
    def proportion(self, value,istart,istop,ostart,ostop) :
        return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))
    
    def setPwm0PortPeriod(self, period):
        
        if ((period >= 0) and (period <= 65535)): 
            self.pwm0PortPeriod = period
            if self.pwm0BeginCalled is False:
                self.uper.pwm0_begin(self.pwm0PortPeriod)
                self.pwm0BeginCalled = True
        else :
            print "*SYSOUT*Error! PWM period can be only between 0-65535"
    
    def setPwm1PortPeriod(self, period):
        if ((period >= 0) and (period <= 65535)): 
            self.pwm1PortPeriod = period
            if self.pwm1BeginCalled is False:
                self.uper.pwm1_begin(self.pwm1PortPeriod)
                self.pwm1BeginCalled = True
        else :
            print "*SYSOUT*Error! PWM period can be only between 0-65535"
    
    def setPwmPeriod(self, period):
        """Overrides default value of 20000ms to set new period value for whole 6 PWM pins. Period value must be superior than 0 and inferior than 65535."""
        if ((period >= 0) and (period <= 65535)): 
            self.pwm0PortPeriod = period
            self.pwm1PortPeriod = period
            
            if self.pwm0BeginCalled is False:
                self.uper.pwm0_begin(self.pwm0PortPeriod)
                self.pwm0BeginCalled = True
            
            if self.pwm1BeginCalled is False:
                self.uper.pwm1_begin(self.pwm1PortPeriod)
                self.pwm1BeginCalled = True
        
        else :
            print "*SYSOUT*Error! PWM period can be only between 0-65535"
    
    def setPwm0Limit(self, limit):
        if ((limit > 0) and (limit <= self.pwm0PortPeriod)):
            self.pwm0Limit = limit
        else:
            print "*SYSOUT*Error! PWM limit can't be superior than " + self.pwm0PortPeriod + " , 0 or inferior than 0"
    
    def setPwm1Limit(self, limit):
        if ((limit > 0) and (limit <= self.pwm1PortPeriod)):
            self.pwm1Limit = limit
        else:
            print "*SYSOUT*Error! PWM limit can't be superior than " + self.pwm1PortPeriod + " , 0 or inferior than 0"
    
    
    def setPwmLimit(self, limit):
        """Overrides default limit of 8bits for PWM precision. This value sets PWM counting upper limit and it's expressed as decimal value. This limit will be applied to all 6 PWM pins.
            """
        if ((limit > 0) and (limit <= self.pwm0PortPeriod) and (limit <= self.pwm1PortPeriod)):
            self.pwm0Limit = limit
            self.pwm1Limit = limit
        else:
            print "*SYSOUT*Error! PWM limit can't be superior than " + min(self.pwm0PortPeriod, self.pwm1PortPeriod)  + " , 0 or inferior than 0"
    
    def attachInterrupt(self, pin, mode, callback):
        myid = self.getAvailableInterruptId()
        if not(myid is None) :
            inter = Interrupt(myid, pin, mode, callback)
            self.interrupts[myid] = inter
            self.uper.attachInterrupt(myid, pins[pin], mode)
    
    def detachInterrupt(self, pin):
        
        for m in self.interrupts:
            if not(m is None):
                if (m.pin==pin):
                    #print "pin to be detached ", m.pin
                    self.uper.detachInterrupt(m.myid)
    
    
    def getAvailableInterruptId(self) :
        for i in range(0,HARD_INTERRUPTS):
            if self.interrupts[i] == None:
                return i
        print "*SYSOUT*Error! There is only " + str(HARD_INTERRUPTS) + " interrupts available" 
        return None


class Interrupt():
    def __init__(self, myid, pin, mode, callback):
        self.myid = myid
        self.pin = pin
        self.mode = mode
        self.callback = callback
