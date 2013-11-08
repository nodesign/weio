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
