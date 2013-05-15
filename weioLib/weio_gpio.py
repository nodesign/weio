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

import os

def pinMode(pin, dir) :
    """pinMode function defines if GPIO is in OUTPUT mode (actioner) or in INPUT mode (sensor)"""
    s_pin = str(pin)

    # if os.path.exists("/sys/class/gpio/export") :
    #        inputFile = open("/sys/class/gpio/export", "w")
    #        rep = inputFile.write(s_pin)
    #        inputFile.close()

    if os.path.exists("/sys/devices/virtual/gpio/gpio" + s_pin + "/direction") :
        inputFile = open("/sys/devices/virtual/gpio/gpio" + s_pin + "/direction", "w")
        rep = inputFile.write(dir)
        inputFile.close()
    else :
        print "WEIO says : pin " + str(pin) + " is busy or non existant"


def digitalWrite(pin, state) :
    """Digital write will set voltage +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground"""

    s_pin = "/sys/devices/virtual/gpio/gpio" + str(pin) + "/value"
    if os.path.exists(s_pin) :
        inputFile = open(s_pin, "w")
        rep = inputFile.write(state)
        inputFile.close()
    else :
        print "WEIO says : pin " + str(pin) + " is not accessible, did you declare pinmode(pin, direction)?"
        
def digitalRead(pin) :
    """Digital read will read actual voltage on corresponding pin. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected"""
    s_pin = "/sys/devices/virtual/gpio/gpio" + str(pin) + "/value"
    if os.path.exists(s_pin) :
        inputFile = open(s_pin, "r")
        rep = inputFile.read()
        return rep
    else :
        print "WEIO says : pin " + str(pin) + " is not accessible, did you declare pinmode(pin, direction)?"
        return None
