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


global pathToDecompressUpdate
global currentWeioConfigurator
global fileToStoreUpdate

fileToStoreUpdate = "weioLibs.tar.gz"

global distantJsonUpdater

# checkForUpdates is entering point for updater
# First it will download only update.weio to check if there is need for an update
# If yes than archive will be downloaded and decompressed
# Put flag in current config.weio that tells to OS that old weio will be removed 
# at next restart of system
def getInfo(url):
    http_client = httpclient.AsyncHTTPClient()
    http_client.fetch(url, callback=processInfo)
    
# checking version
def processInfo(response):
    
    global distantJsonUpdater
    # global currentWeioConfigurator
    
    distantJsonUpdater = json.loads(str(response.body))
      
    #distantVersion = float(distantJsonUpdater["version"])
    
    download(distantJsonUpdater["url"])
# downloading archive    
def download(url):
    http_client = httpclient.AsyncHTTPClient()
    http_client.fetch(url, callback=decompress)
    
# decompressing and adding flag
def decompress(data):
    print "Libs downloaded"
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
        print "Open config.weio"
        inputFile = open(path+"/files/weio/config.weio", 'r')
        rawData = inputFile.read()
        inputFile.close()
        config = json.loads(rawData)

        # Overwrite local configuration file
        config["first_time_run"] = "YES"
        config["port"] = 80

        inputFile = open("../config.weio", 'w')
        ret = inputFile.write(json.dumps(config, indent=4, sort_keys=True))
        inputFile.close()
        
        print "Procedure finished, now you can make carambola2 image"
        sys.exit()
         
        # TODO make system reboot here
        # sys.exit()
    else :
        print "Wrong MD5 checksum. Trying again..."
        checkForUpdates("http://www.we-io.net/downloads/updateLibs.weio")

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
    return md5.hexdigest()
 
print "Welcome to image preparation tool for WeIO"
print "This script will :"
print "     1 Strip current version of WeIO for production"
print "     2 Download external libs package from WeIO server (tornado, sockJS, pip, easy_install)"
print "     3 Set first time boot flag in config.weio"
print "     4 Make files directrory inside carambola2 tree. (Will overwrite previous version of files)"
print "After this procedure you can cd to carambola2 and make image"

if (len(sys.argv)!=2) :
    print "ERROR : Please provide target directory where carambola2 is situated. ex. /Users/me/weio/carambola2"
else :
    path = sys.argv[1]
    if not os.path.isdir(path):
        print "ERROR directory doesn't exist!"
    else :
        if not os.path.isdir(path+"/files"):
           print "Creating and copying scripts to /files"
           p = Popen(["cp", "-r", "../../openWrt/files", path], stdout=PIPE)
           p.wait()
   
        else:
           p = Popen(["rm", "-r", path+"/files"], stdout=PIPE)
           p.wait()
           p = Popen(["cp", "-r", "../../openWrt/files", path], stdout=PIPE, close_fds=True)
           # wait... I have to finish this process before sending
           p.communicate()
        
        print "Stripping WeIO"
        p = Popen(["bash", "stripWeio.sh", path+"/files"], stdout=PIPE, close_fds=True)
           # wait... I have to finish this process before sending
        p.communicate()
        
        print "Downloading external depencencies"
        print "Getting info file and downloading libs"
        pathToDecompressUpdate = path+"/files"
        getInfo("http://www.we-io.net/downloads/weioImage/updateLibs.weio")
        ioloop.IOLoop.instance().start()