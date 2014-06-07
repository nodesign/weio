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

import os, signal, sys, platform

from tornado import web, ioloop, iostream, gen, httpclient
sys.path.append(r'./');

# pure websocket implementation
#from tornado import websocket

from sockjs.tornado import SockJSRouter, SockJSConnection

from weioLib import weioFiles
from weioLib import weioConfig
from weioLib import weioIdeGlobals

import functools
import json
import hashlib
import tarfile

clients = set()

# Wifi detection route handler  
class WeioUpdaterHandler(SockJSConnection):
    def __init__(self, *args, **kwargs):
        SockJSConnection.__init__(self, *args, **kwargs)
        #########################################################################
        # DEFINE CALLBACKS IN DICTIONARY
        # Second, associate key with right function to be called
        # key is comming from socket and call associated function
        self.callbacks = {
            'checkVersion' : self.checkForUpdates,
            'downloadUpdate' : self.downloadUpdate,
        }
        
        self.downloadTries = 0
        self.estimatedInstallTime = 35
    
    # checkForUpdates is entering point for updater
    # First it will download only update.weio to check if there is need for an update
    # If yes than archive will be downloaded and decompressed
    # Put flag in current config.weio that tells to OS that old weio will be removed 
    # at next restart of system
    def checkForUpdates(self, rq):
        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch("http://www.we-io.net/downloads/update.weio", callback=self.checkVersion)

    # checking version
    def checkVersion(self, response):
        wifiMode = "ap"
        if (platform.machine() == 'mips') :
            wifiMode = weioIdeGlobals.WIFI.mode
            print "WIFI MODE ", wifiMode
        else :
            wifiMode = "sta"
        
        rsp={}
    
        if (wifiMode=="sta") : # check Internet
            global currentWeioConfigurator
            
            self.distantJsonUpdater = json.loads(str(response.body))
            currentWeioConfigurator = weioConfig.getConfiguration()

            print "My software version " + \
                currentWeioConfigurator["weio_version"] + \
                " Version on WeIO server " + \
                self.distantJsonUpdater["version"] + \
                " Needs " + str(self.distantJsonUpdater['install_duration']) + " seconds to install"
        
            # Send response to the browser
            
            rsp['requested'] = "checkVersion"
            rsp['localVersion'] = currentWeioConfigurator["weio_version"]
            rsp['distantVersion'] = self.distantJsonUpdater["version"]
        
            distantVersion = float(self.distantJsonUpdater["version"])
            localVersion = float(currentWeioConfigurator["weio_version"])
            if (distantVersion > localVersion) :
                rsp['needsUpdate'] = "YES"
                rsp['description'] = self.distantJsonUpdater['description']
                rsp['whatsnew'] = self.distantJsonUpdater['whatsnew']
                rsp['install_duration'] = self.distantJsonUpdater['install_duration']
                self.estimatedInstallTime = self.distantJsonUpdater['install_duration']
            else :
                rsp['needsUpdate'] = "NO"
        
            
        elif (wifiMode=="ap") :
            rsp['needsUpdate'] = "NO"
        
        # Send connection information to the client
        self.send(json.dumps(rsp))
        
    def downloadUpdate(self, rq):
        #self.progressInfo("5%", "Downloading WeIO Bundle " + self.distantJsonUpdater["version"])
      
        http_client = httpclient.AsyncHTTPClient()
        http_client.fetch(self.distantJsonUpdater["url"], callback=self.downloadComplete)
        
    def downloadComplete(self, binary):
        # ok now save binary in /tmp (folder in RAM)
        if (platform.machine()=="mips") :    
            fileToStoreUpdate = "/tmp/weioUpdate.tar.gz"
            pathToDecompressUpdate = "/tmp"
        else :
            fileToStoreUpdate = "./weioUpdate.tar.gz"
            pathToDecompressUpdate = "./"
            
        with open(fileToStoreUpdate, "w") as f:
               f.write(binary.body)
               
        # check file integrity with MD5 checksum
        md5local = self.getMd5sum(fileToStoreUpdate)
        
        if (md5local == self.distantJsonUpdater["md5"]) :
            print "MD5 checksum OK"
            self.progressInfo("50%", "MD5 checksum OK")
            print "Bundle decompressing"
            #self.progressInfo("52%", "WeIO Bundle decompressing")
            tar = tarfile.open(fileToStoreUpdate)
            tar.extractall(pathToDecompressUpdate)
            tar.close()
            print "Bundle decompressed"
            #self.progressInfo("80%", "WeIO Bundle decompressed")
            
            # kill arhive that we don't need anymore to free RAM
            os.remove(fileToStoreUpdate)
            global currentWeioConfigurator
            print "Setting kill flag to YES in current config.weio"
            print "Now I'm ready to exit Tornado and install new version"
            currentWeioConfigurator["kill_flag"] = "YES"
            weioConfig.saveConfiguration(currentWeioConfigurator)
            #self.progressInfo("81%", "WeIO installing")
            # Now quit Tornado and leave script to do his job
            exit()
            
        else :
            print "MD5 checksum is not OK, retrying..."
            if (self.downloadTries<2):
                self.progressInfo("5%", "Downloading Bundle again, MD5 checkum was not correct")
                self.downloadUpdate(None)
            else:
                print "Something went wrong. Check Internet connection and try again later"
                self.progressInfo("0%", "Something went wrong. Check Internet connection and try again later")
            
            self.downloadTries+=1
    
    # Automatic status sender
    def progressInfo(self, progress, info):
        data = {}
        data['serverPush'] = "updateProgress"
        data['progress'] = progress # 5%, 10%,... in string format "10%"
        data['info'] = info
        data['estimatedInstallTime'] = self.estimatedInstallTime
        self.send(json.dumps(data))
        
    # Get MD5 checksum from file    
    def getMd5sum(self, filename):
        md5 = hashlib.md5()
        with open(filename,'rb') as f: 
            for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
                 md5.update(chunk)
        return md5.hexdigest()

    def on_open(self, info) :
        global clients
        clients.add(self)

    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        req = json.loads(data)
        self.serve(req)
        
    def serve(self, rq):
        """Parsed input from browser ready to be served"""
        # Call callback by key directly from socket
        request = rq['request']

        if request in self.callbacks :
            self.callbacks[request](rq)
        else :
            print "unrecognised request"
            
    def on_close(self) :
        global clients
        # Remove client from the clients list and broadcast leave message
        clients.remove(self)

