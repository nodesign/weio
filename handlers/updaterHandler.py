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

import os, signal, sys, platform, subprocess, urllib2

from tornado import web, ioloop, iostream, gen, httpclient, httputil
sys.path.append(r'./');

# pure websocket implementation
#from tornado import websocket

from sockjs.tornado import SockJSRouter, SockJSConnection

from weioLib import weioFiles
from weioLib import weioConfig
from weioLib import weioIdeGlobals
from weioLib import weioUnblock

from threading import Thread
from time import sleep

import functools
import json
import hashlib
import tarfile

import socket

# IMPORT BASIC CONFIGURATION FILE
from weioLib import weioConfig

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
            'reinstallFw' : self.reinstallFw
        }
        
        self.downloadTries = 0
        self.estimatedInstallTime = 80

        self.fwMd5 = None
        self.downloadUpdateLink  = None

        self.fwDownloadLink = None
        self.fwDownloadSize = None
        self.fwSizeWatcherThread = None
        
        if (platform.machine()=="mips") :
            self.fwPath = "/tmp/weio_recovery.bin"
        else :
            self.fwPath = "./weio_recovery.bin"

    def isConnected(self, address):
        try:
          # see if we can resolve the host name -- tells us if there is
          # a DNS listening
          host = socket.gethostbyname(address)
          # connect to the host -- tells us if the host is actually
          # reachable
          s = socket.create_connection((host, 80), 2)
          return True
        except:
           pass
        return False

    # checkForUpdates is entering point for updater
    # First it will download only update.weio to check if there is need for an update
    # If yes than archive will be downloaded and decompressed
    # Put flag in current config.weio that tells to OS that old weio will be removed 
    # at next restart of system
    def checkForUpdates(self, rq):
        wifiMode = "ap"
        if (platform.machine() == 'mips') :
            wifiMode = weioIdeGlobals.WIFI.mode
            print "WIFI MODE ", wifiMode
        else :
            wifiMode = "sta" # local setting

        if (wifiMode=="sta"):

            if (self.isConnected("we-io.net") or self.isConnected("www.github.com")):
                config = weioConfig.getConfiguration()
                repository = ""
                print "REPO", config["weio_use_official_repository"]
                if (config["weio_use_official_repository"] == "YES") :
                    repository = config["weio_update_official_repository"]
                else :
                    repository = config["weio_update_alternate_repository"]

                h = httputil.HTTPHeaders({"Accept" : "application/vnd.github.v3+json","User-Agent" : "weio"})
                req = None
                if (config["weio_use_official_repository"] == "YES"):
                    req = httpclient.HTTPRequest(repository, headers=h)
                else :
                    req = httpclient.HTTPRequest(repository)

                http_client = httpclient.AsyncHTTPClient()
                http_client.fetch(req, callback=self.checkVersion)
            else :
                # not connected to the internet
                print "NO INTERNET CONNECTION"
        else :
            print "NO INTERNET CONNECTION"

    # checking version
    def checkVersion(self, response):
        print response.body
        config = weioConfig.getConfiguration()

        data = json.loads(response.body)
        #f = open("github.json", "w")
        #f.write(json.dumps(data, indent=4, sort_keys=True))
        #f.close()
        #print json.dumps(data, indent=4, sort_keys=True)
        lastUpdate = data[0]
        distantVersion = float(lastUpdate["tag_name"].split("v")[1])

        currentVersion = float(config["weio_version"])
        print "current",currentVersion,"distant", distantVersion
        rsp = {}

        rsp['requested'] = "checkVersion"
        rsp['localVersion'] = str(currentVersion)
        rsp['distantVersion'] = str(distantVersion)

        if (distantVersion > currentVersion): 
            print "OK update is needed"
            # OK we have to update weio version
            rsp['needsUpdate'] = "YES"
            rsp['description'] = lastUpdate["name"]
            rsp['whatsnew'] = lastUpdate["body"]
            rsp['install_duration'] = self.estimatedInstallTime
            self.downloadUpdateLink = ""

            for file in lastUpdate["assets"]:
                if ("weio.tar.gz" in file["name"]):
                    self.downloadUpdateLink = file["browser_download_url"]
                    self.downloadSize = file["size"]
                    print self.downloadUpdateLink, "size", file["size"]

                if ("weio_recovery.bin" in file["name"]):
                    print "found weio_recovery"
                    self.fwDownloadLink = file["browser_download_url"]
                    self.fwDownloadSize = file["size"]
        else :
            rsp['needsUpdate'] = "NO"
        self.send(json.dumps(rsp))

    def downloadUpdate(self, rq):
        #self.progressInfo("5%", "Downloading WeIO Bundle " + self.distantJsonUpdater["version"])
        if not(self.downloadUpdateLink is None):
            http_client = httpclient.AsyncHTTPClient()
            http_client.fetch(self.downloadUpdateLink, callback=self.downloadComplete)

    def downloadComplete(self, binary):
        config = weioConfig.getConfiguration()

        # ok now save binary in /tmp (folder in RAM)
        print "downloaded"

        if (platform.machine()=="mips") :
            fileToStoreUpdate = "/tmp/weioUpdate.tar.gz"
            pathToDecompressUpdate = "/tmp"
        else :
            fileToStoreUpdate = "./weioUpdate.tar.gz"
            pathToDecompressUpdate = "./"

        with open(fileToStoreUpdate, "w") as f:
               f.write(binary.body)

        # Check is file size is the same as on the server
        sizeOnDisk = os.path.getsize(fileToStoreUpdate)

        if (sizeOnDisk == self.downloadSize):
            # OK
            print "File size is OK"
            self.progressInfo("50%", "File size OK")
            print "Bundle decompressing"
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
            config["kill_flag"] = "YES"
            weioConfig.saveConfiguration(config)
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

    @weioUnblock.unblock
    def reinstallFw(self, data):
        if not(self.fwDownloadLink is None):
            self.fwSizeWatcherThread = Thread(target = self.sizeWatcher)
            self.fwSizeWatcherThread.start()
            a = {}
            a['serverPush'] = "readyToReinstallFw"
            a['data'] = ""
            self.send(json.dumps(a))
            p = subprocess.Popen(["curl", "-k", "-L", "-o", self.fwPath, self.fwDownloadLink])
            print p.communicate()
            self.fwSizeWatcherThread.join()
            sizeOnDisk = os.path.getsize(self.fwPath)
            print "Size matching", self.fwDownloadSize, sizeOnDisk
            if (self.fwDownloadSize == sizeOnDisk):
                p = subprocess.Popen(["sysupgrade", "-v", "-n", self.fwPath])
                print p.communicate()
            else :
                a = {}
                a['serverPush'] = "errorDownloading"
                a['data'] = ""
                self.send(json.dumps(data))

    def sizeWatcher(self):
        print "sizeeee"
        sizeOnDisk = 0
        while (sizeOnDisk<self.fwDownloadSize):
            if os.path.exists(self.fwPath):
                sizeOnDisk = os.path.getsize(self.fwPath)
            else :
                break
            progress = int((100.0/self.fwDownloadSize)*sizeOnDisk)
            print "SIZEEEEEE", sizeOnDisk, self.fwDownloadSize, "percent", progress
            a = {}
            a['serverPush'] = "downloadingFw"
            a['data'] = progress
            self.send(json.dumps(a))
            sleep(1)

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

