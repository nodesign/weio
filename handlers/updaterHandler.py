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

import functools

# pure websocket implementation
#from tornado import websocket

from sockjs.tornado import SockJSRouter, SockJSConnection

from weioLib import weioFiles
from weioLib import weioConfig
from weioLib import weioIdeGlobals
from weioLib import weioUnblock

from time import sleep

import functools
import json
import hashlib
import tarfile

import socket

# IMPORT BASIC CONFIGURATION FILE
from weioLib import weioConfig

import urllib2, urllib

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
            data = {}
            if (self.isConnected("we-io.net") or self.isConnected("www.github.com")):
                config = weioConfig.getConfiguration()
                repository = ""
                print "REPO", config["weio_update_use_official_repository"]
                if (config["weio_update_use_official_repository"] == "YES") :
                    repository = config["weio_update_official_repository"]
                else :
                    repository = config["weio_update_alternate_repository"]

                h = httputil.HTTPHeaders({"Accept" : "application/vnd.github.v3+json","User-Agent" : "weio"})
                req = None
                if (config["weio_update_use_official_repository"] == "YES"):
                    req = httpclient.HTTPRequest(repository, headers=h)
                else :
                    req = httpclient.HTTPRequest(repository)

                http_client = httpclient.AsyncHTTPClient()
                http_client.fetch(req, callback=self.checkVersion)
            else :
                # not connected to the internet
                print "NO INTERNET CONNECTION"
                data['serverPush'] = "noInternetConnection"
                data['data'] = "Can't reach Internet servers"
                self.send(json.dumps(data))
        else :
            print "NO INTERNET CONNECTION"
            data['serverPush'] = "noInternetConnection"
            data['data'] = "Can't reach Internet servers"
            self.send(json.dumps(data))

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
                    self.updateDownloadSize = file["size"]
                    print self.updateDownloadSize, "size", file["size"]
        else :
            rsp['needsUpdate'] = "NO"

        # You can always reflash with last version even if there are no new updates
        for file in lastUpdate["assets"]:
            if ("weio_recovery.bin" in file["name"]):
                print "found weio_recovery"
                self.fwDownloadLink = file["browser_download_url"]
                self.fwDownloadSize = file["size"]

        self.send(json.dumps(rsp))

    @weioUnblock.unblock
    def downloadUpdate(self, data):
        config = weioConfig.getConfiguration()

        # ok now save binary in /tmp (folder in RAM)
        print "downloaded"

        fileToStoreUpdate = ""
        if (platform.machine()=="mips") :
            fileToStoreUpdate = "/tmp/weioUpdate.tar.gz"
            pathToDecompressUpdate = "/tmp"
        else :
            fileToStoreUpdate = "./weioUpdate.tar.gz"
            pathToDecompressUpdate = "./"

        if not(self.downloadUpdateLink is None):

            sw = functools.partial(self.sizeWatcher, fileToStoreUpdate, self.updateDownloadSize)
            sizeCheckerCallback = ioloop.PeriodicCallback(sw, 500)
            sizeCheckerCallback.start()
            self.startDownload(self.downloadUpdateLink, fileToStoreUpdate)
            sizeCheckerCallback.stop()

        # Check is file size is the same as on the server
        sizeOnDisk = os.path.getsize(fileToStoreUpdate)
        print "comparing sizes", sizeOnDisk, self.updateDownloadSize
        if (sizeOnDisk == self.updateDownloadSize):
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
            ioloop.IOLoop.instance().stop()
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

    @weioUnblock.unblock
    def reinstallFw(self, data):
        if not(self.fwDownloadLink is None):
            if (self.isConnected("we-io.net") or self.isConnected("www.github.com")):
                print "will download fw from", self.fwDownloadLink

                sw = functools.partial(self.sizeWatcher, self.fwPath, self.fwDownloadSize)
                sizeCheckerCallback = ioloop.PeriodicCallback(sw, 1000)
                sizeCheckerCallback.start()
                self.startDownload(self.fwDownloadLink, self.fwPath)
                sizeCheckerCallback.stop()
                a = {}
                a['serverPush'] = "downloadingFw"
                a['data'] = 100
                self.send(json.dumps(a))

                a = {}
                a['serverPush'] = "readyToReinstallFw"
                a['data'] = ""
                self.send(json.dumps(a))

                sizeOnDisk = os.path.getsize(self.fwPath)
                print "Size matching", self.fwDownloadSize, sizeOnDisk
                if (self.fwDownloadSize == sizeOnDisk):
                    # protect user files
                    p = subprocess.Popen(["sysupgrade", "-v", self.fwPath]) 
                    # don't protect user files
                    #p = subprocess.Popen(["sysupgrade", "-v", "-n", self.fwPath])
                    print p.communicate()
                else :
                    a = {}
                    a['serverPush'] = "errorDownloading"
                    a['data'] = ""
                    self.send(json.dumps(data))
            else :
                data = {}
                data['serverPush'] = "noInternetConnection"
                data['data'] = "Can't reach Internet servers"
                self.send(json.dumps(data))
        else :
            self.checkForUpdates()

    def startDownload(self, fwUrl, targetFile):
        print "download init"
        try:
            req = urllib2.Request(fwUrl)
            handle = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print "Can't download firmware, error code - %s." % e.code
            return
        except urllib2.URLError:
            print "Bad URL for firmware file: %s" % fwUrl
            return
        else:
            print "download starts"
            urllib.urlretrieve(fwUrl, targetFile)
            print "download finished"

    def sizeWatcher(self,targetFile, targetSize):
        sizeOnDisk = 0
        if os.path.exists(targetFile):
            sizeOnDisk = os.path.getsize(targetFile)
            progress = int((100.0/targetSize)*sizeOnDisk)
            print "percent downloaded", progress
            a = {}
            a['serverPush'] = "downloadingFw"
            a['data'] = progress
            self.send(json.dumps(a))

    def downloadProgress(self,data):
        print "progress", data

    # MD5 is not used at this moment
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