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

import os, signal, sys, platform, subprocess, datetime

from tornado import web, ioloop, iostream, gen
sys.path.append(r'./');
from sockjs.tornado import SockJSRouter, SockJSConnection

import functools
import json
from weioLib import weioIpAddress
from weioLib import weioFiles

# For shared variables between handlers
from weioLib.weioUserApi import *


# IMPORT BASIC CONFIGURATION FILE 
from weioLib import weio_config

# Wifi detection route handler  
class WeioEditorHandler(SockJSConnection):
    global callbacks
    
    # DEFINE CALLBACKS HERE
    # First, define callback that will be called from websocket
    
    
    def getTreeInHTML(self,rq):
        
        # get configuration from file
        config = weio_config.getConfiguration()
        
        data = {}
        data['requested'] = rq['request']
        up = config["user_projects_path"]
        lp = config["last_opened_project"]
        
        tree = weioFiles.getHtmlTree((up+lp))
        data['data'] = tree
        # Send connection information to the client
        self.send(json.dumps(data))
    

    
    def sendFileContent(self, rq):
        data = {}
        # echo given request
        data['requested'] = rq['request']
        
        # echo given data
        data['data'] = rq['data']
        
        path = rq['data']
        
        if (weioFiles.checkIfFileExists(path)):
        
            f = {}
            f['name'] = weioFiles.getFilenameFromPath(path)
            f['id']   = weioFiles.getStinoFromFile(path)
            f['type'] = weioFiles.getFileType(path)
            f['data'] = weioFiles.getRawContentFromFile(path)
            f['path'] = path
            
            data['data'] = f
            
            self.send(json.dumps(data))
        
    def saveFile(self, rq):
        data = {}
        # echo given request
        data['requested'] = rq['request']
        
        f = rq['data']
        weioFiles.saveRawContentToFile(f['path'], f['data'])
        
        data['status'] = rq['data']['name'] + " saved!"
        self.send(json.dumps(data))
    
    def createNewFile(self, rq): 
        
        # get configuration from file
        config = weio_config.getConfiguration()
        
        data = {}
        # this function is similar to saveFile
        
        # echo given request
        data['requested'] = rq['request']
        
        # don't echo given data to spare unnecessary communication, just return name
        fileInfo = rq['data']
        pathname = fileInfo['name']
        
        confFile = weio_config.getConfiguration()
        pathCurrentProject = confFile["user_projects_path"] + confFile["last_opened_project"]
        
        #print (pathCurrentProject+pathname)
        # in new file there are no data, it will be an empty string
        rawData = ""
        weioFiles.saveRawContentToFile(pathCurrentProject+pathname, rawData)
        
        data['status'] = fileInfo['name'] + " has been created"
        self.send(json.dumps(data))
    
    def deleteFile(self,rq):
        data = {}
        data['requested'] = rq['request']
        data['path'] = rq['path']
        
        path = rq['path']
        
        weioFiles.removeFile(path)
        
        data['status'] = "file has been removed"
        self.send(json.dumps(data))

    def saveAll(self, rq) :
        #print "SAVE ALL FILES FROM ARRAY ", rq
        files = rq['data']
        
        if len(files)>0 :
            for f in files:
                weioFiles.saveRawContentToFile(f['path'], f['data'])
        
            data = {}
            data['requested'] = rq['request']
            data['status'] = "Project has been saved"
            self.send(json.dumps(data))
        
    
    ##############################################################################################################################
    # DEFINE CALLBACKS IN DICTIONARY
    # Second, associate key with right function to be called
    # key is comming from socket and call associated function
    callbacks = {
        #'getIp' : sendIp,
        #'getLastProjectName' : sendLastProjectName,
        'getFileTreeHtml' : getTreeInHTML,
        'getFile': sendFileContent,
        #'play' : play,
        #'stop' : stop,
        #'getPlatform': sendPlatformDetails,
        #'getUserProjetsFolderList': getUserProjectsList,
        #'changeProject': changeProject,
        'saveFile': saveFile,
        'createNewFile': createNewFile,
        'deleteFile': deleteFile,
        'saveAll' : saveAll
        #'getUser': sendUserData,
    
    }
    
    def on_open(self, info) :
        
        global CONSOLE
        # Store instance of the ConsoleConnection class
        # in the global variable that will be used
        # by the MainProgram thread
        CONSOLE = self
        shared.editor = self.editorSender
        

    def editorSender(self, data):
        self.send(json.dumps(data))
    
    
    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        req = json.loads(data)
        self.serve(req)
    
    def serve(self, rq):
        """Parsed input from browser ready to be served"""
        # Call callback by key directly from socket
        global callbacks
        request = rq['request']
        
        if request in callbacks :
            callbacks[request](self, rq)
        else :
            print "unrecognised request", rq['request']