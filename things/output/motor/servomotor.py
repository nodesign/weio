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

###
# Controling servo motor with PWM signal
# Pulse length is constant of 20ms, variate impulse from 1ms to 2ms
#
#   +---+                +---+
#   |   |                |   |
#   |   |                |   |
#   |   |                |   |
#---+   +----------------+   +------
# -->   <--1 ms = 5%
#   <-------- 20 ms ----> 
#
#
#   +------+            +------+
#   |      |            |      |
#   |      |            |      |
#   |      |            |      |
#---+      +------------+      +------
# -->      <--2 ms = 10%
#   <------- 20 ms ----->
###
from weioLib.weio import *

class Servo:

    def __init__(self, pin, minangle=0.0, maxangle=180.0, minperiod=5.0, maxperiod=10.0):
        self.minangle = float(minangle)
        self.maxangle = float(maxangle)
        self.minperiod = float(minperiod)
        self.maxperiod = float(maxperiod)
        self.pin = pin
        # At first angle is unknown after first setting of angle this variable is updated
        # This is just simple mechanism of tracking no real feedback
        self.angle = None
        # Set PWM period to fire every 20ms
        setPwmPeriod(self.pin, 20000)

    def write(self, data):
        """Move servo to n degrees. Every 20ms variate signal from 5% - 10% with PWM"""

        # Make proportion calculation here, map angle to percrents
        if (data>self.maxangle):
            data = self.maxangle
            print "Warning, max allowed angle is ", self.maxangle , " value is set to " , self.maxangle

        if (data<self.minangle):
            data = self.minangle
            print "Warning, min allowed angle is " , self.minangle , " value is set to " , self.minangle
        
        self.angle = data
        out = proportion(data, self.minangle, self.maxangle, self.minperiod, self.maxperiod)

        pwmWrite(self.pin, out)

    def read(self):
        return self.angle
