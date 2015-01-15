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

import platform
import time

class WifiButtons :
    
    def __init__(self):

        self.resetStates()
    
    def resetStates(self) :
        
        self.setAPcallback = 0
        self.setSTAcallback = 0
        
        self.buff_buttonAP = 0
        self.buttonAP = 0
        
        self.buff_buttonSTA = 0
        self.buttonSTA = 0
        
        self.timer = -1.0

        self.blockAP = 0
        self.blockSTA = 0
    
    def checkButtons(self) :
        
        if (platform.machine() == 'mips') :
            
            # Read AP button state
            f = open("/sys/class/gpio/gpio23/value","r")
            self.buttonAP = int(f.readline())
            f.close()        

            # Read STA button state
            f = open("/sys/class/gpio/gpio22/value","r")
            self.buttonSTA = int(f.readline())
            f.close()        
            
            
            # deal with signals from buttons
            if ((self.buttonAP == 0) and (self.buff_buttonAP == 1)) :
                if ((self.buttonSTA == 0) and (self.blockAP == 0)):
                    #print "ACTIVATE AP"
                    self.resetStates()
                    return "ap"
                self.timer = -1.0
                self.blockAP = 0
            
            
            if ((self.buttonSTA == 0) and (self.buff_buttonSTA == 1)) :
                if ((self.buttonAP == 0) and (self.blockSTA == 0)):
                    #print "ACTIVATE STA"
                    self.resetStates()
                    return "sta"
                self.timer = -1.0
                self.blockSTA = 0
                    
            # boutons pressed together and 3 secs timer
            if ((self.buttonAP == 1) and (self.buttonSTA == 1)):
                if (self.timer < 0.0):
                    self.timer = time.time()
                    #print "AP+STA TOGETHER BUTTONS"
                elif ((time.time() - self.timer) > 3.0) :
                    #print "3 secs OVER RESET!!"
                    self.resetStates()
                    return "reset"
                    self.timer = -1.0
                self.blockAP = 1
                self.blockSTA = 1

            # put previous state into memory            
            self.buff_buttonAP = self.buttonAP
            self.buff_buttonSTA = self.buttonSTA
            return None
        else:
            return None