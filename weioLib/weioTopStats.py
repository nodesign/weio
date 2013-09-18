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
    
    usedRam = float(mem[0][0].split("K")[0])/1000.0
    usedRam = "%.1f" % usedRam
    
    freeRam = float(mem[1][0].split("K")[0])/1000.0
    freeRam = "%.1f" % freeRam
    
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
    free = float(st.f_bavail * st.f_frsize)/1000000.0
    free = "%.1f" % free
    used = float((st.f_blocks - st.f_bfree) * st.f_frsize)/1000000.0
    used = "%.1f" % used
    
    flash = { "free" : free , "used": used}
    
    #free = st.f_bavail * st.f_frsize
    #total = st.f_blocks * st.f_frsize
    #used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return flash