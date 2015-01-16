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

import time
from weioLib.weioUserApi import *

import threading
import random

# Simple standalone application, no web interface
# Reads digital potentiometer from A0 pin to blink LED slower or
# faster at digital pin 13

LED_PIN = 13
POTENTIOMETER_PIN = "A0"

lock = threading.RLock()

###
# Threads
###

# These threads are like individual mini programs. Share data between them using shred variables
# In this case shared object is shared.val
# In most of cases this usage will work. If sync problems are encountered use lock library to lock
# shared data between threads
def potentiometer() :
    while (1) :
        print("potentiometer") 
        shared.val += 1
        time.sleep(1)
        
def test1():
    f = open('myfile','a')
    time.sleep (random.random ())
    localVar = shared.val + 1
    time.sleep (random.random ()) # Some long call between 0 and 1
    shared.val = localVar
    print 'Thread1 ends: criticalVar = %d' % shared.val
    
    s="\n>>START<<\n"
    for i in range(100):
        for j in range(100):
            s = s + "1"
        s = s + '\n'
    s = s + "\n>>STOP<<\n"

    #print >>f, s
    console.output(s, file=f)
    f.close()

def test2():
    f = open('myfile','a')
    time.sleep (random.random ())
    localVar = shared.val + 1
    time.sleep (random.random ()) # Some long call between 0 and 1
    shared.val = localVar
    print 'Thread2 ends: criticalVar = %d' % shared.val

    s="\n>>START<<\n"
    for i in range(100):
        for j in range(100):
            s = s + "2"
        s = s + '\n'
    s = s + "\n>>STOP<<\n"
    #print >>f, s
    console.output(s, file=f)
    f.close()
    
    
def test3():
    f = open('myfile','a')
    time.sleep (random.random ())
    localVar = shared.val + 1
    time.sleep (random.random ()) # Some long call between 0 and 1
    shared.val = localVar
    console.output('Thread3 ends: criticalVar = %d' % shared.val)

    s="\n>>START<<\n"
    for i in range(100):
        for j in range(100):
            s = s + "3"
        s = s + '\n'
    s = s + "\n>>STOP<<\n"
    #print >>f, s
    console.output(s, file=f)
    f.close()

    

        
def setup():
    # Attaches sensor function to infinite loop
    attach.process(test1)
    attach.process(test2)
    attach.process(test3)
    
    # Instanciate shared objects
    shared.val = 0
