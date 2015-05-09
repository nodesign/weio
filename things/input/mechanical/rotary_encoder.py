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

from weioLib.weio import *

class RotaryEncoder:

    FORWARD = 1
    BACKWARD = -1

    _backward_states = [
        [[0, 0], [1, 0], [1, 1]],  # missing 1st
        [[0, 1], [1, 0], [1, 1]],  # missing 2nd
        [[0, 1], [0, 0], [1, 1]],  # missing 3rd
        [[0, 1], [0, 0], [1, 0]],  # missing 4th
    ]

    _forward_states = [
        [[0, 0], [0, 1], [1, 1]],  # missing 1st or perfect
        [[1, 0], [0, 1], [1, 1]],  # missing 2nd
        [[1, 0], [0, 0], [1, 1]],  # missing 3rd
        [[1, 0], [0, 0], [0, 1]],  # missing 4th
    ]

    _null_state = [[-1, -1], [-1, -1], [-1, -1]]
    
    def __init__(self, chan0, chan1, callback=None):
        #obj = {'previous_states': list(self._null_state), 'position': 0}

        self._previous_states = list(self._null_state)
        self.pin1 = 0
        self.pin2 = 0
        self.position = 0

        self._chan0 = chan0
        self._chan1 = chan1

        self._user_callback = callback

        self._id0 = attachInterrupt(self._chan0, CHANGE, self.cb1, self._chan0, 1)
        self._id1 = attachInterrupt(self._chan1, CHANGE, self.cb2, self._chan1, 1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def cb1(self, event, obj):
        self.pin1 = (event['values'] >> event['id']) & 0x01
        self.call_back(event, obj)

    def cb2(self, event, obj):
        self.pin2 = (event['values'] >> event['id']) & 0x01
        self.call_back(event, obj)

    def call_back(self, event, obj):
        if [self.pin1, self.pin2] != self._previous_states[2]:
            self._previous_states[0:2] = self._previous_states[1:3]
            self._previous_states[2] = [self.pin1, self.pin2]

            if self._previous_states in self._forward_states:
                self.position += 1
                self._previous_states = list(self._null_state)
                if self._user_callback:
                    self._user_callback(RotaryEncoder.FORWARD, self.position)
            elif self._previous_states in self._backward_states:
                self.position -= 1
                self._previous_states = list(self._null_state)
                if self._user_callback:
                    self._user_callback(RotaryEncoder.BACKWARD, self.position)
