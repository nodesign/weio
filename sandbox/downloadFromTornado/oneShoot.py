#!/usr/bin/env python
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

from tornado import ioloop, httpclient
import json
import hashlib
import sys,os
import tarfile
from subprocess import Popen
from subprocess import PIPE

global fileToStoreUpdate
global pathToDecompressUpdate
global currentWeioConfigurator

# Do settings here for right paths
fileToStoreUpdate = "/tmp/weioUpdate.tar.gz"
pathToDecompressUpdate = "/tmp"
# currentWeioConfigPath = '/weio/weio/config.weio'

global distantJsonUpdater

# checkForUpdates is entering point for updater
# First it will download only update.weio to check if there is need for an update
# If yes than archive will be downloaded and decompressed
# Put flag in current config.weio that tells to OS that old weio will be removed 
# at next restart of system
def checkForUpdates(url):
    http_client = httpclient.AsyncHTTPClient()
    http_client.fetch(url, callback=checkVersion)
    
# checking version
def checkVersion(response):
    
    global distantJsonUpdater
    # global currentWeioConfigurator
    
    distantJsonUpdater = json.loads(str(response.body))
    # currentWeioConfigurator = json.loads(open(currentWeioConfigPath, 'r').read())
    
    # print "My software version " + currentWeioConfigurator["weio_version"] + " Version on WeIO server " + distantJsonUpdater["version"]
    
    distantVersion = float(distantJsonUpdater["version"])
    # localVersion = float(currentWeioConfigurator["weio_version"])
    
    download(distantJsonUpdater["url"])
# downloading archive    
def download(url):
    http_client = httpclient.AsyncHTTPClient()
    http_client.fetch(url, callback=doUpdate)
    
# decompressing and adding flag
def doUpdate(data):
    print "Update downloaded"
    with open(fileToStoreUpdate, "w") as f:
        f.write(data.body)
    
    md5local = md5sum(fileToStoreUpdate)
    
    if (md5local == distantJsonUpdater["md5"]) :
        print "MD5 checksum OK"
        tar = tarfile.open(fileToStoreUpdate)
        tar.extractall(pathToDecompressUpdate)
        tar.close()
        print "Archive decompressed"
        
        # global currentWeioConfigurator
        #         print "Setting kill flag to YES in current config.weio"
        #         currentWeioConfigurator["kill_flag"] = "YES"
        #         
        os.remove(fileToStoreUpdate)
        
        p = Popen(["mv", pathToDecompressUpdate + "/weio", "/weio"], stdout=PIPE)
        p.wait()   
        
        p = Popen(["cp", "/weio/scripts/weio_run_forever.sh", "/weio_run_forever.sh"], stdout=PIPE)
        p.wait()
        
        print "Now you can go to / and launch ./weio_run_forever.sh"
        
        # TODO make system reboot here
        sys.exit()
    else :
        print "Wrong MD5 checksum. Trying again..."
        checkForUpdates("http://www.we-io.net/downloads/update.weio")

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
    return md5.hexdigest()
    
checkForUpdates("http://www.we-io.net/downloads/update.weio")
ioloop.IOLoop.instance().start()
