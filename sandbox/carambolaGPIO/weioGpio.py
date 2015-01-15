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


import os

def pinMode(pin, dir) :
    """pinMode function defines if GPIO is in OUTPUT 
       mode (actioner) or in INPUT mode (sensor)"""
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
    """Digital write will set voltage +3.3V or Ground on corresponding pin.
       This function takes two parameters : pin number and it's state 
       that can be HIGH = +3.3V or LOW = Ground"""

    s_pin = "/sys/devices/virtual/gpio/gpio" + str(pin) + "/value"
    if os.path.exists(s_pin) :
        inputFile = open(s_pin, "w")
        rep = inputFile.write(state)
        inputFile.close()
    else :
        print "WEIO says : pin " + str(pin) + " is not accessible, did you declare pinmode(pin, direction)?"
        
def digitalRead(pin) :
    """Digital read will read actual voltage on corresponding pin. 
       There are two possible answers : 0 if pin is connected to 
       the Ground or 1 if positive voltage is detected"""
    s_pin = "/sys/devices/virtual/gpio/gpio" + str(pin) + "/value"
    if os.path.exists(s_pin) :
        inputFile = open(s_pin, "r")
        rep = inputFile.read()
        return rep
    else :
        print "WEIO says : pin " + str(pin) + " is not accessible, did you declare pinmode(pin, direction)?"
        return None
