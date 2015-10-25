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
            'reinstallFw' : self.reinstallFw
        }

#        self.downloadTries = 0
#        self.estimatedInstallTime = 80

        self.fwMd5 = None
        self.downloadUpdateLink  = None

        self.fwDownloadLink = None
        self.fwDownloadSize = None
        self.fwSizeWatcherThread = None

        self.updateFileName = None

        if (platform.machine()=="mips") :
            # put file to RAM
            self.fwPath = "/tmp/"
        else :
            # this is where file will be saved on the PC
            self.fwPath = "./"

    # check if there is Internet connection
    # give some address as parameter, file to download address is welcome
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

    # This is entering point for updater
    # First it will download only update.weio to check if there is need for an update
    # If yes than archive will be downloaded and decompressed
    # Put flag in current config.weio that tells to OS that old weio will be removed 
    # at next restart of system
    def checkForUpdates(self, rq):
        # default mode is offline
        wifiMode = "ap"
        #check hardware platform
        if (platform.machine() == 'mips') :
            # check network state, if is STA then we can check if there is Internet
            wifiMode = weioIdeGlobals.WIFI.mode
            print "WIFI MODE ", wifiMode
        else :
            # for local purposes only, testing on PC
            wifiMode = "sta" # local setting

        if (wifiMode=="sta"):
            data = {}
            # check if our server is reachable
            if (self.isConnected("we-io.net")):
                config = weioConfig.getConfiguration()
                repository = config["weio_update_official_repository"]

                # make request for a json file
                req = httpclient.HTTPRequest(repository)

                http_client = httpclient.AsyncHTTPClient()
                # start fetching file at the end execute checkVersion function
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

        lastUpdate = data

        # Read version form json file
        # XXX it supposes that the distant version number is prefixed with 'v'
        # The updater will break here if this prefix is removed in the future
        distantVersion = float(lastUpdate["version"].split("v")[1])

        # Check the current version
        currentVersion = float(config["weio_version"])

        print "current",currentVersion,"distant", distantVersion
        rsp = {}

        rsp['requested'] = "checkVersion"
        rsp['localVersion'] = str(currentVersion)
        rsp['distantVersion'] = str(distantVersion)
        rsp['needsUpdate'] = "NO"

        # version differs so we need an update
        if (distantVersion > currentVersion): 
            print "Update is available"
            # OK we have to update weio version
            rsp['description'] = lastUpdate["title"]
            rsp['whatsnew'] = lastUpdate["body"]
            #rsp['install_duration'] = self.estimatedInstallTime
            self.downloadUpdateLink = ""

            # set all parameters for download, but DON'T download yet
            # this is a just version check
            self.updateFileName = self.fwPath + "weio_recovery.bin"
            rsp['needsUpdate'] = "YES"
            print "setting parameters :"
            self.fwDownloadLink = lastUpdate["download_url"]
            print "download url", self.fwDownloadLink
            self.fwDownloadSize = lastUpdate["size"]
            print "file size", self.fwDownloadSize
            self.fwDownloadMD5 = lastUpdate["md5"]
            print "md5 checksum", self.fwDownloadSize

        self.send(json.dumps(rsp))

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
            # XXX Is it to check the internet connection ?
            if (self.isConnected("we-io.net")):
                print "will download fw from", self.fwDownloadLink

                # prepare for download
                sw = functools.partial(self.sizeWatcher, self.updateFileName, self.fwDownloadSize)
                # each second i'll be checking size on the disk and target size of the file
                sizeCheckerCallback = ioloop.PeriodicCallback(sw, 1000)
                # start donwloading!
                sizeCheckerCallback.start()
                # when finished downloading 
                self.startDownload(self.fwDownloadLink, self.updateFileName)
                sizeCheckerCallback.stop()
                a = {}
                a['serverPush'] = "downloadingFw"
                a['data'] = 100
                self.send(json.dumps(a))

                a = {}
                a['serverPush'] = "readyToReinstallFw"
                a['data'] = ""
                self.send(json.dumps(a))
                print self.updateFileName
                fileMD5 = self.getMd5sum(self.updateFileName)
                print "MD5 matching", self.fwDownloadMD5, fileMD5
                if (self.fwDownloadMD5 == fileMD5):
                    print "MD5 match !"
                    print "now exiting Tornado and executing update procedure"
                    ioloop.IOLoop.instance().stop()
                    exit()
                    # XXX following should be moved in the remote script
                    # protect user files
                    # kill all symlinks first
                    #p = subprocess.Popen(["sh", "/weio/scripts/userProjectsLinking.sh"])
                    #print p.communicate()
                    # move to new directory
                    #os.rename("/weioUser/flash", "/weioUserBackup")
                    # update FW
                    #p = subprocess.Popen(["sysupgrade", "-v", self.fwPath])
                    # don't protect user files
                    #p = subprocess.Popen(["sysupgrade", "-v", "-n", self.fwPath])
                    #print p.communicate()
                else :
                    # XXX errorDownloading need to be linked to a modal view
                    print "MD5 don't match!!! Please retry"
                    a = {}
                    a['serverPush'] = "errorDownloading"
                    a['data'] = "MD5 don't march. Please retry later"
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
