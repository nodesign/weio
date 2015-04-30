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

import socket
import urllib
import re
import subprocess
import platform

def retry(fn):
    def _inner(*args,**kwargs):
        retry = int(kwargs['retry']) if 'retry' in kwargs and kwargs['retry'] else 0
        opt_exception = kwargs['opt_exception'] if 'opt_exception' in kwargs and kwargs['opt_exception'] else 0
        while True or retry:
            try:
                return fn(*args,**kwargs)
            except Exception,e:
                if not retry: break
                retry = retry - 1 
        if opt_exception:  raise opt_exception 
        else:              raise Exception('No internet or host is down.')
    return _inner

def getLocalIpAddress() :
    """Gets local ip address"""
    
    if (platform.system() == 'Linux') :
        cmd = "ifconfig wlan0 | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'"
        return subprocess.check_output(cmd, shell=True)        
    else : # Darwin
        return socket.gethostbyname(socket.gethostname())

@retry
def getPublicIpAddress(retry=None,opt_exception=Exception) :
    """Gets world ip address. TODO test if internet is reachable
        example: getPublicIpAddress(retry=2,opt_exception=Exception('error occured.'))
        
        @type retry:int 
        @param retry: retries before throwing an exception.
        
        @type opt_exception:Exception
        @param opt_exception: optional exception argument to throw. if not any, Exception is raised.
        
    """
    cmd = 'ping -t 2 -c 1 107.20.89.142 > /dev/null 2>&1; echo $?'
    if int(subprocess.check_output(cmd,shell=True)) == 0:
        f = urllib.urlopen("http://www.canyouseeme.org/")
        html_doc = f.read()
        f.close()
        ipAddress = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
    
        #response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=' + ipAddress.group(0) + '&position=true').read()
        return urllib.urlopen('http://api.hostip.info/get_html.php?ip=' + ipAddress.group(0)).read()
    else:
        raise
