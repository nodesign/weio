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


# Stepper motor driver
# Uros Petrevski, 2014
# Implemented both full step and half-step control
from weioLib.weio import *
from time import sleep

FULL_STEP = 0
HALF_STEP = 1

class Stepper:
    """
    Stepper motor class.

    :param stepsIn360: The number of steps in full (360 degree) rotation.
    :type stepsIn360: int
    :param coilApin0: GPIO ID of coil A pin 0.
    :type coilApin0: int
    :param coilApin1: GPIO ID of coil A pin 1.
    :type coilApin1: int
    :param coilBpin0: GPIO ID of coil B pin 0.
    :type coilBpin0: int
    :param coilBpin1: GPIO ID of coil B pin 1.
    :type coilBpin1: int
    """

    def __init__(self, stepsIn360, coilApin0, coilApin1, coilBpin0, coilBpin1):

        self.totalSteps = stepsIn360
        self.delayLength = 0.01

        # Wave stepping scheme, full step
        self.fullStepCoilA = [1,0,-1,0]
        self.fullStepCoilB = [0,1,0,-1]

        # Half stepping scheme
        self.halfStepCoilA = [1,1,0,-1,-1,-1,0,1]
        self.halfStepCoilB = [0,1,1,1,0,-1,-1,-1]

        self.stepperMode = FULL_STEP

        # declare pins
        self.A0 = coilApin0
        self.A1 = coilApin1

        self.B0 = coilBpin0
        self.B1 = coilBpin1

        # declare motor pins in output mode
        pinMode(self.A0, OUTPUT)
        pinMode(self.A1, OUTPUT)
        
        pinMode(self.B0, OUTPUT)
        pinMode(self.B1, OUTPUT)
        
    def setStepperMode(self, sMode):
        """
        Set stepper motor step mode.

        :param sMode: Step mode: Stepper.FULL_STEP or Stepper.HALF_STEP
        """
        self.stepperMode = sMode

    def setSpeed(self, rpm):
        """
        Set stepper motor rotation speed.

        :param rpm: Revolutions per second.
        :type rpm: int
        """
        self.delayLength = 30.0/(self.totalSteps*rpm)

    def _fireSignal(self, pin0, pin1, data):
        if data == 0:
            digitalWrite(pin0,LOW)
            digitalWrite(pin1,LOW)
        elif data == 1:
            digitalWrite(pin0,HIGH)
            digitalWrite(pin1,LOW)
        elif data == -1:
            digitalWrite(pin0,LOW)
            digitalWrite(pin1,HIGH)

    def step(self, steps):
        """
        Step a specified number of steps.

        :param steps: Number of steps.
        :type steps: int
        """
        nSteps = abs(steps)
        for s in xrange(0,nSteps):
            if (self.stepperMode==FULL_STEP):
                phase = s%4
                if (steps>0):
                    self._fireSignal(self.A0,self.A1, self.fullStepCoilA[phase])
                    self._fireSignal(self.B0,self.B1, self.fullStepCoilB[phase])
                else :
                    self._fireSignal(self.A0,self.A1, self.fullStepCoilB[phase])
                    self._fireSignal(self.B0,self.B1, self.fullStepCoilA[phase])
                sleep(self.delayLength)

            elif (self.stepperMode==HALF_STEP):
                phase = s%8
                if (steps>0):
                    self._fireSignal(self.A0,self.A1, self.halfStepCoilA[phase])
                    self._fireSignal(self.B0,self.B1, self.halfStepCoilB[phase])
                else :
                    self._fireSignal(self.A0,self.A1, self.halfStepCoilB[phase])
                    self._fireSignal(self.B0,self.B1, self.halfStepCoilA[phase])
                sleep(self.delayLength)
