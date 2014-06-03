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
from weioLib import weioUnblock

# IMPORT BASIC CONFIGURATION FILE 
from weioLib import weioConfig

# Wifi detection route handler  
class WeioEditorHandler(SockJSConnection):
    global callbacks
    
    # DEFINE CALLBACKS HERE
    # First, define callback that will be called from websocket
    
    #@weioUnblock.unblock
    def getFileTree(self,rq):
        # get configuration from file
        config = weioConfig.getConfiguration()
        
        data = {}
        data['requested'] = rq['request']
        lp = config["last_opened_project"]
        if (weioFiles.checkIfDirectoryExists(lp)):
            tree = weioFiles.getFileTree(lp)
            data['data'] = tree
            data['projectRoot'] = lp.split("/")[0]
        else:
            data['data'] = ""
            data['projectRoot'] = ""
        # Send connection information to the client
        self.send(json.dumps(data))
    

    # @weioUnblock.unblock
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
            
            if not(f['type'] is 'other'):
                if (f['type'] is 'image'):
                    print rq
                    # only images
                    data['requested'] = "getImage"
                    filename = f['name']
                    tag = {"jpeg":"jpg","jpg":"jpeg", "png":"png", "tiff":"tif", "tif":"tiff", "bmp":"bmp"}
                    prefix = ""
                    ext = filename.split(".")[1]
                    if (ext in tag):
                        prefix = tag[ext]
                    content = "data:image/"+prefix+";base64,"
                    content += f['data'].encode("base64")
                    f['data'] = content
                    self.send(json.dumps(data))
                else:
                    # all regular editable files
                    self.send(json.dumps(data))
    

    @weioUnblock.unblock    
    def saveFile(self, rq):
        #print "DATA ", rq
        data = {}
        # echo given request
        data['requested'] = rq['request']
        
        f = rq['data']
        contents = f['data']
        path = f['path']
        name = rq['data']['name'] 
        
        #print "NAME " + rq['data']['name']
        weioFiles.saveRawContentToFile(path, contents)
                   
        data['status'] = name + " saved!"
        self.send(json.dumps(data))


    @weioUnblock.unblock    
    def createNewFile(self, rq): 
        data = {}
        # this function is similar to saveFile
        
        # echo given request
        data['requested'] = rq['request']
        
        # don't echo given data to spare unnecessary communication, just return name
        f = rq['data']
        name = f['name']
        contents = f['data']
        
        # get configuration from file
        confFile = weioConfig.getConfiguration()
        print "WILL BE SAVED IN ", name
        
        if ((".html" in name) or (".py" in name) or (".json" in name) or
            (".css" in name) or (".txt" in name) or (".js" in name) or
            (".md" in name) or (".svg" in name) or (".xml" in name) or
            (".less" in name) or (".coffee" in name)):
            
            weioFiles.saveRawContentToFile(confFile["last_opened_project"] + name, contents)
        else:
            #decode from base64, file is binary
            bin = contents
            bin = bin.split(",")[1] # split header, for example: "data:image/jpeg;base64,"
            weioFiles.saveRawContentToFile(confFile["last_opened_project"] + "/" + name, bin.decode("base64"))

        #print (pathCurrentProject+pathname)
                
        data['status'] = name + " has been created"
        self.send(json.dumps(data))

            
    @weioUnblock.unblock
    def deleteFile(self,rq):
        data = {}
        data['requested'] = rq['request']
        data['path'] = rq['path']
        
        path = rq['path']
        
        weioFiles.removeFile(path)
        
        data['status'] = "file has been removed"
        self.send(json.dumps(data))

    # don't unblock saveAll beacuse each saveFile is unblocked already
    def saveAll(self, rq) :
        #print "SAVE ALL FILES FROM ARRAY ", rq
        files = rq['data']
        
        if len(files)>0 :
            for f in files:
                #weioFiles.saveRawContentToFile(f['path'], f['data'])
                saveData = {}
                saveData["request"] = "saveFile"
                saveData["data"] = f
                self.saveFile(saveData)
                              
            data = {}
            data['requested'] = rq['request']
            data['status'] = "Project has been saved"
            self.send(json.dumps(data))
    
    def sendPlatformDetails(self, rq):
        # get configuration from file
        config = weioConfig.getConfiguration()
        
        data = {}
        
        platformS = ""
        
        platformS += "WeIO version " + config["weio_version"] + " with Python " + \
                            platform.python_version() + " on " + platform.system() + "<br>"
        platformS += "GPL 3, Nodesign.net 2013 Uros Petrevski & Drasko Draskovic <br>"
        
        data['serverPush'] = 'sysConsole'
        data['data'] = platformS
        self.send(json.dumps(data))
        #CONSOLE.send(json.dumps(data))

    
    def iteratePacketRequests(self, rq) :
        
        requests = rq["packets"]
        
        for uniqueRq in requests:
            request = uniqueRq['request']
            if request in callbacks:
                callbacks[request](self, uniqueRq)
            else :
                print "unrecognised request ", uniqueRq['request']


        
    
    ##############################################################################################################################
    # DEFINE CALLBACKS IN DICTIONARY
    # Second, associate key with right function to be called
    # key is comming from socket and call associated function
    callbacks = {
        #'getIp' : sendIp,
        #'getLastProjectName' : sendLastProjectName,
        'getFileTree' : getFileTree,
        'getFile': sendFileContent,
        #'play' : play,
        #'stop' : stop,
        'getPlatform': sendPlatformDetails,
        #'getUserProjetsFolderList': getUserProjectsList,
        #'changeProject': changeProject,
        'saveFile': saveFile,
        'createNewFile': createNewFile,
        'deleteFile': deleteFile,
        'saveAll' : saveAll,
        'packetRequests': iteratePacketRequests
        #'getUser': sendUserData,
    
    }
    
    def on_open(self, info) :
        
        global CONSOLE
        # Store instance of the ConsoleConnection class
        # in the global variable that will be used
        # by the MainProgram thread
        CONSOLE = self
        
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
