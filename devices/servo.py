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


from weioLib.weioIO import setPwmPeriod, pwmWrite, setPwmLimit, proportion

class Servo:
    
    def __init__(self):
        # Set 20ms signal length for PWM
        setPwmPeriod(20000)
        # Set maximum precision for this freq
        setPwmLimit(19999)
        # Down limit frequency expressed in uS
        self.downLimit = 1000 # 5% of 20000
        self.upLimit = self.downLimit*2 # 10% of 20000
        self.minAngle = 0
        self.maxAngle = 180
        self.angle = None
        self.readuS = None

    def write(self, pin, data):
        # Write to coresponding servo motor
        val = int(proportion(data, self.minAngle,self.maxAngle, self.downLimit, self.upLimit))
        self.readuS = val
        self.angle = data
        pwmWrite(pin, 19999-self.readuS)
        
    def setMinLimit(self, val):
        self.downLimit = val
        
    def setMaxLimit(self, val):
        self.upLimit = val
    
    def setMinAngle(self, val):
        self.minAngle = val
        
    def setMaxAngle(self, val):
        self.maxAngle = val    
    
    def read(self):
        return self.angle
        
    def readuS(self):
        return self.readuS