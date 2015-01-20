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

from subprocess import Popen, PIPE
import os

def getTop():
    """Return top statistics for ram and cpu usage on OpenWrt"""

    p = Popen(["top", "-n", "1"], stdout=PIPE, close_fds=True)
    f = p.communicate()

    lines = f[0].split("\n")
    mem = lines[0]
    mem = mem.split(",")
    mem[0] = mem[0].split("\x1b[H\x1b[JMem:")[1]

    for i in range(0,len(mem)):
        mem[i] = mem[i].split()

    cpu = lines[1]
    cpu = cpu.split(",")

    for i in range(0,len(cpu)):                                           
        cpu[i] = cpu[i].split()  
        
    usedRam = float(mem[0][0].split("K")[0])/10000.0
    usedRam = "%.2f" % usedRam

    freeRam = float(mem[1][0].split("K")[0])/10000.0
    freeRam = "%.2f" % freeRam

    cpuUser = int(cpu[0][1].split("%")[0])
    cpuSystem = int(cpu[0][3].split("%")[0])
    cpuIdle = int(cpu[0][7].split("%")[0])
    
    cpuData = { "user" : cpuUser, "system" : cpuSystem, "idle" : cpuIdle}
    ramData = { "free" : freeRam, "used": usedRam }
    
    data = {"mem" : ramData, "cpu" : cpuData}
    return data
    
def getSpaceUsage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in Megabytes.
    """
    st = os.statvfs(path)
    
    flash = { "free" : st.f_bavail * st.f_frsize, "used":(st.f_blocks - st.f_bfree) * st.f_frsize }
    
    #free = st.f_bavail * st.f_frsize
    #total = st.f_blocks * st.f_frsize
    #used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return flash