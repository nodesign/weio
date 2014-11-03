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