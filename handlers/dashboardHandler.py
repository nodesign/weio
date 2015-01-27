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


import os, signal, sys, platform, subprocess, datetime
from os.path import isfile, join

from tornado import web, ioloop, iostream, gen
sys.path.append(r'./');
from sockjs.tornado import SockJSRouter, SockJSConnection

import functools
import json
from weioLib import weioIpAddress
from weioLib import weioFiles

from shutil import copyfile, copytree, ignore_patterns

# IMPORT BASIC CONFIGURATION FILE
from weioLib import weioConfig

# Import globals for main Tornado
from weioLib import weioIdeGlobals

clients = set()

# Wifi detection route handler
class WeioDashBoardHandler(SockJSConnection):
    global callbacks

    # Handler sanity, True alive, False dead
    global stdoutHandlerIsLive
    global stderrHandlerIsLive

    stdoutHandlerIsLive = None
    stderrHandlerIsLive = None

    def __init__(self, *args, **kwargs):
        SockJSConnection.__init__(self, *args, **kwargs)
        self.errObject = []
        self.errReason = ""

    def setEditor(editor):
        self.editor = editor

    # DEFINE CALLBACKS HERE
    # First, define callback that will be called from websocket
    def sendIp(self,rq):

        # get configuration from file
        config = weioConfig.getConfiguration()

        data = {}
        ip = weioIpAddress.getLocalIpAddress()
        #publicIp = weioIpAddress.getPublicIpAddress()
        data['requested'] = rq['request']
        data['status'] = config["dns_name"] + " on " + ip
        # Send connection information to the client
        self.broadcast(clients, json.dumps(data))

    def sendPreviewPortNumber(self,rq):

        # get configuration from file
        config = weioConfig.getConfiguration()

        data = {}
        data['requested'] = rq['request']
        data['data'] = config["userAppPort"]
        # Send connection information to the client
        self.broadcast(clients, json.dumps(data))


    def sendLastProjectName(self,rq):
        # get configuration from file
        config = weioConfig.getConfiguration()

        data = {}
        data['requested'] = rq['request']
        lp = os.path.basename( config["last_opened_project"].strip("/") )

        storage = config["last_opened_project"].split("/")[0]

        print "USER PRJ NAME", lp

        if (weioFiles.checkIfDirectoryExists(config["last_opened_project"])):
            print "PROJ NAME", config["last_opened_project"]
            data['data'] = config["last_opened_project"].split(storage+"/")[1]
        else :
            data['data'] = "Select project here"
        # Send connection information to the client
        self.broadcast(clients, json.dumps(data))

    def play(self, rq):
        weioIdeGlobals.PLAYER.play(rq)

    def stop(self, rq):
        """Stop running application"""
        weioIdeGlobals.PLAYER.stop(rq)

    def sendPlatformDetails(self, rq):
        # get configuration from file
        config = weioConfig.getConfiguration()

        data = {}

        platformS = ""

        platformS += "WeIO version " + config["weio_version"] + " with Python " + \
                            platform.python_version() + " on " + platform.system() + "<br>"
        platformS += "GPL 3, Nodesign.net 2013-2014 Uros Petrevski & Drasko Draskovic <br>"

        data['serverPush'] = 'sysConsole'
        data['data'] = platformS
        weioIdeGlobals.CONSOLE.send(json.dumps(data))

    def getUserProjectsList(self, rq):
        # get configuration from file
        config = weioConfig.getConfiguration()

        data = {}
        data['requested'] = rq['request']

        allExamples = []
        allUserProjects = []

        # Examples
        examplesDir = "www/examples"

        if (os.path.exists(examplesDir)):
            dirs = get_directory_structure(examplesDir)
            a = {"storageName":"examples", "projects":dirs}
            allExamples.append(a)

        # Flash
        flashDir = "www/flash"
        if (os.path.exists(flashDir)):
            dirs = get_directory_structure(flashDir)
            a = {"storageName":"flash", "projects":dirs}
            allUserProjects.append(a)

        # SD
        flashDir = "www/sd"
        if (os.path.exists(flashDir)):
           dirs = get_directory_structure(flashDir)
           a = {"storageName":"sd", "projects":dirs}
           allUserProjects.append(a)

        # USB flashDir
        flashDir = "www/usbFlash"
        if (os.path.exists(flashDir)):
           dirs = get_directory_structure(flashDir)
           a = {"storageName":"usbFlash", "projects":dirs}
           allUserProjects.append(a)

        data['data'] = allUserProjects
        data['examples'] = allExamples
        self.broadcast(clients, json.dumps(data))

    def changeProject(self,rq):
        #print "CHANGE PROJECT", rq
        # get configuration from file
        print "TO CHANGE ", rq
        config = weioConfig.getConfiguration()

        virtPath = rq['data']
        storage = os.path.dirname(virtPath)
        print 'STORAGE', storage
        path = "www/"+virtPath
        print 'STORAGE', path

        config["last_opened_project"] = path
        weioConfig.saveConfiguration(config);

        # In this way we avoid migrations between pc and weio and other archs
        if (storage != "sd" and storage != "usbFlash"):
            try:
                os.remove(path+"/www")
            except:
                print "Symlink don't exist. Will create new one for www in this project"
            os.symlink(config["absolut_root_path"] + "/www/", path + "/www")
        elif not os.path.exists(path + "/www"):
            print "COPYING TO ", path + "/www"
            copytree(config['absolut_root_path'] + "/www/", path + "/www", ignore=ignore_patterns('sd', 'flash', 'examples', 'usbFlash'))
            print "OK"
        


        data = {}
        data['requested'] = rq['request']
        self.broadcast(clients, json.dumps(data))

        rqlist = ["stop", "getLastProjectName", "getUserProjetsFolderList"]

        for i in range(0,len(rqlist)):
            rq['request'] = rqlist[i]
            callbacks[ rq['request'] ](self, rq)

    def sendUserData(self,rq):
        data = {}
        # get configuration from file
        config = weioConfig.getConfiguration()
        data['requested'] = rq['request']

        data['name'] = config["user"]
        self.broadcast(clients, json.dumps(data))

    def newProject(self, rq):
        config = weioConfig.getConfiguration()
        print "NEW PROJECT", rq
        data = {}
        data['requested'] = rq['request']
        path = ""
        storage = rq['storageUnit']

        path = "www/" + rq['storageUnit'] + "/" + rq['path']

        print "CREATE PROJECT", path
        if (len(path)>0):
            if (weioFiles.checkIfDirectoryExists(path)):
                print "ALREADY EXISTS"
                data['status'] = "Can't create project"
                data['error'] = "already exists"
                data['path'] = path
                self.broadcast(clients, json.dumps(data))
            else :
                weioFiles.createDirectory(path)
                # ADD HERE SOME DEFAULT FILES
                # adding __init__.py
                weioFiles.saveRawContentToFile(path + "/__init__.py", "")

                # make symlink to www/
                if (storage == "sd" or storage == "usbFlash"):
                    if (storage == "sd"):
                        if os.path.isdir(path):
                            if not (os.path.exists(path + "/www")):
                                print "COPYING TO ", path + "/www"
                                copytree(config["absolut_root_path"] + "/www/", path + "/www", ignore=ignore_patterns('sd', 'flash', 'examples', 'usbFlash'))
                                print "OK"
                    else:
                        if not (os.path.exists(path + "/www")):
                            print "COPYING TO ", path + "/www"
                            copytree(config["absolut_root_path"] + "/www/", path + "/www", ignore=ignore_patterns('sd', 'flash', 'examples', 'usbFlash'))
                            print "OK"
                else:
                    try:
                        os.remove(path + "/www")
                    except:
                        print "Symlink don't exist. Will create new one for this project"
                    os.symlink(config["absolut_root_path"] + "/www/", path + "/www")

                # copy all files from directory boilerplate to destination
                mypath = "www/libs/weio/boilerPlate/"
                onlyfiles = [ f for f in os.listdir(mypath) if isfile(join(mypath,f)) ]
                for f in onlyfiles:
                    copyfile(mypath+f, path +"/"+f)

                print "LASTOPENED new project", path
                config["last_opened_project"] = path
                weioConfig.saveConfiguration(config);

                data['status'] = "New project created"
                data['path'] = path
                self.broadcast(clients, json.dumps(data))
        else:
            print "BAD PATHNAME"


    def duplicateProject(self, rq):
        config = weioConfig.getConfiguration()

        print "DUPLICATE",rq

        storage = rq['storageUnit']

        path = "www/" + rq['storageUnit'] + "/" + rq['path']

        print "DUPLICATE PROJECT", path
        data = {}
        if (len(path)>0):
            if (storage != "sd" and storage != "usbFlash"):
                # Destroy symlink
                os.remove(config["last_opened_project"]+"/www")
                # copy all files
                try:
                    copytree(config["last_opened_project"], path)
                except:
                    print sys.exc_info()[0]
            else:
                if (storage == "sd"):
                    if os.path.isdir(path):
                        try:
                            copytree(config["last_opened_project"], path, ignore=ignore_patterns('www'))
                        except:
                            print sys.exc_info()[0]
                else
                    # copy all files
                    try:
                        copytree(config["last_opened_project"], path, ignore=ignore_patterns('www'))
                    except:
                        print sys.exc_info()[0]

            if (storage != "sd" and storage != "usbFlash"):
                # Recreate symlink
                os.symlink(config["absolut_root_path"] + "/www/", config["last_opened_project"] + "/www")
            else:
                if not (os.path.exists(path + "/www")):
                    copytree(config["absolut_root_path"] + "/www/", path + "/www", ignore=ignore_patterns('sd', 'flash', 'examples', 'usbFlash'))

            config["last_opened_project"] = path
            weioConfig.saveConfiguration(config)

            data['status'] = "Project duplicated"

            data['requested'] = "status"
            self.broadcast(clients, json.dumps(data))

            # now go to newely duplicated project

            data['request'] = "changeProject"
            data['data'] = rq['storageUnit'] + "/" + rq['path']

            self.changeProject(data)
        else:
            print "BAD PATHNAME"
            data['status'] = "Error duplicating project"

            data['requested'] = "status"
            self.broadcast(clients, json.dumps(data))


    def deleteCurrentProject(self, rq):
        data = {}
        data['requested'] = rq['request']

        config = weioConfig.getConfiguration()
        projectToKill = config["last_opened_project"]

        print "PROJECT TO KILL ", projectToKill

        weioFiles.removeDirectory(projectToKill)

        folders = weioFiles.listOnlyFolders("www/examples")

        if len(folders) > 0 :
         config["last_opened_project"] = "www/examples/" + folders[0]
         weioConfig.saveConfiguration(config)

         data['data'] = "reload page"
        else :
         data['data'] = "ask to create new project"

        self.broadcast(clients, json.dumps(data))

    def iteratePacketRequests(self, rq) :
        requests = rq["packets"]

        for uniqueRq in requests:
            request = uniqueRq['request']
            if request in callbacks:
                callbacks[request](self, uniqueRq)
            else :
                print "unrecognised request ", uniqueRq['request']

    def sendPlayerStatus(self, rq):
        data = {}
        data['requested'] = rq['request']
        data['status'] = weioIdeGlobals.PLAYER.playing

        self.broadcast(clients, json.dumps(data))

    def createTarForProject(self, rq):
        # TEST IF NAME IS OK FIRST
        # get configuration from file
        config = weioConfig.getConfiguration()
        data = {}
        data['requested'] = "status"
        data['status'] = "Making archive..."
        self.broadcast(clients, json.dumps(data))

        data['requested'] = rq['request']

        splitted = config["last_opened_project"].split("/")
        print "CHOOSE NAME", splitted
        lp = splitted[-1]


        if (weioFiles.checkIfDirectoryExists(config["last_opened_project"])):
            weioFiles.createTarfile(config["last_opened_project"] + "/" + lp + ".tar",
                    config["last_opened_project"]+"/")

            data['status'] = "Project archived"
            print "project archived"
        else :
            data['status'] = "Error archiving project"

        self.broadcast(clients, json.dumps(data))

    def decompressNewProject(self, rq):
        print "decompress"
        f = rq['data']
        name = f['name']
        contents = f['data']
        storageUnit = rq['storageUnit'] +"/"
        #print contents

        # get configuration from file
        confFile = weioConfig.getConfiguration()
        pathCurrentProject = "www/" + storageUnit

        projectName = name.split(".tar")[0]
        data = {}

        if (weioFiles.checkIfDirectoryExists(pathCurrentProject+projectName) is False) :
            #decode from base64, file is binary
            bb = contents
            bb = bb.split(",")[1] # split header, for example: "data:image/jpeg;base64,"
            weioFiles.saveRawContentToFile(pathCurrentProject+name, bb.decode("base64"))
            #print "save to ", pathCurrentProject+name
            weioFiles.createDirectory(pathCurrentProject+projectName)
            #print "mkdir ", pathCurrentProject+"userProjects/"+projectName
            weioFiles.unTarFile(pathCurrentProject+name, pathCurrentProject+projectName)
            #print "untar ", pathCurrentProject+"userProjects/"+projectName

            data['request'] = "changeProject"
            data['data'] = storageUnit+projectName

            self.changeProject(data)
        else :
            data['requested'] = 'status'
            data['status'] = "Error this projet already exists"
            self.broadcast(clients, json.dumps(data))

    def clientPing(self, rq):
        data = {}
        data['requested'] = rq['request']
        data['response'] = 'pong'
        self.broadcast(clients, json.dumps(data))

##############################################################################################################################
    # DEFINE CALLBACKS IN DICTIONARY
    # Second, associate key with right function to be called
    # key is comming from socket and call associated function
    callbacks = {
        'getIp' : sendIp,
        'getLastProjectName' : sendLastProjectName,
        #'getFileTreeHtml' : getTreeInHTML,
        #'getFile': sendFileContent,
        'play' : play,
        'stop' : stop,
        'getUserProjetsFolderList': getUserProjectsList,
        'changeProject': changeProject,
        #'saveFile': saveFile,
        #'createNewFile': createNewFile,
        #'deleteFile': deleteFile,
        'getUser': sendUserData,
        'createNewProject': newProject,
        'deleteProject' : deleteCurrentProject,
        'packetRequests': iteratePacketRequests,
        'getPlayerStatus': sendPlayerStatus,
        'archiveProject' : createTarForProject,
        'addNewProjectFromArchive' : decompressNewProject,
        'duplicateProject': duplicateProject,
        'getPreviewPortNumber': sendPreviewPortNumber,
        'ping': clientPing

    }

    def on_open(self, info) :
        global clients
        clients.add(self)
        # Store instance of the ConsoleConnection class
        # in the global variable that will be used
        # by the MainProgram thread
        weioIdeGlobals.CONSOLE = self
        # connect interfaces to player object
        weioIdeGlobals.PLAYER.setConnectionObject(self)


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
            print "unrecognised request ", rq['request']

    def on_close(self):
        global clients
        # Remove client from the clients list and broadcast leave message
        clients.remove(self)


## Get examples directory structure (folders with subfolders)
def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(dirs)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir
