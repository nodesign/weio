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

global weioPipe
global CONSOLE
global ioloop

# Global variable to store SockJSConnection calss instance
# in order to call it's send() method from MainProgram thread
CONSOLE = None

# Global variable to store SockJSConnection calss instance
# in order to call it's send() method from MainProgram thread
weioPipe = None

# Global object to store ioloop handlers that drive sterr &
# stdout from user program
ioloopObj = None

# Date and time string when process was launched last time
lastLaunched = None


# Wifi detection route handler  
class WeioDashBoardHandler(SockJSConnection):
    global callbacks

    # Handler sanity, True alive, False dead
    global stdoutHandlerIsLive
    global stderrHandlerIsLive
    
    global errObject
    global errLine
    global errReason
    
    errReason = ""
    errLine = 0
    errObject = []
    stdoutHandlerIsLive = None
    stderrHandlerIsLive = None

    # DEFINE CALLBACKS HERE
    # First, define callback that will be called from websocket
    def sendIp(self,rq):
        
        # get configuration from file
        config = weio_config.getConfiguration()
        
        data = {}
        ip = weioIpAddress.getLocalIpAddress()
        #publicIp = weioIpAddress.getPublicIpAddress()
        data['requested'] = rq['request']
        data['status'] = config["dns_name"] + " on " + ip
        # Send connection information to the client
        self.send(json.dumps(data))
        
    def sendLastProjectName(self,rq):
        
        # get configuration from file
        config = weio_config.getConfiguration()
        
        data = {}
        data['requested'] = rq['request']
        lp = config["last_opened_project"].split("/")
        data['data'] = lp[0]
        # Send connection information to the client
        self.send(json.dumps(data))
        
    def play(self, rq):
        """ This is where all the magic happens.
        
        "Play" button will spawn a new subprocess
        which will execute users program written in the editor.
        This subprocess will communicate with Tornado wia non-blocking pipes,
        so that Tornado can simply transfer subprocess's `stdout` and `stderr`
        to the client via WebSockets. """
        
        global stdoutHandlerIsLive
        global stderrHandlerIsLive
    
        # get configuration from file
        config = weio_config.getConfiguration()

        # stop if process is already running
        self.stop(rq)

        data = {}
        #processName = './userProjects/myFirstProject/weioMain.py'
        up = config["user_projects_path"]
        lp = config["last_opened_project"]
        lp = lp.split("/")[0] 
        processName = 'weioRunner.py'


        # check if file exists before launching

        if (os.path.exists(processName)):
            #launch process
            
            print("weioMain indipendent process launching...")
            
            global weioPipe
            weioPipe = subprocess.Popen(['python', '-u', processName, lp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            global ioloopObj
            ioloopObj = ioloop.IOLoop.instance()
            
            # Callback for STDOUT
            #callback = functools.partial(self.socket_connection_ready, sock)
            callback = functools.partial(self.weioMainHandler, data)
            #ioloopObj.add_handler(sock.fileno(), callback, ioloopObj.READ)
            ioloopObj.add_handler(weioPipe.stdout.fileno(), callback, ioloopObj.READ)
            stdoutHandlerIsLive = True;
            
            # Callback for STDERR
            callbackErr = functools.partial(self.weioMainHandlerErr, data)
            ioloopObj.add_handler(weioPipe.stderr.fileno(), callbackErr, ioloopObj.READ)
            stderrHandlerIsLive = True;
            
            # Inform client the we run subprocess
            data['requested'] = rq['request']
            data['status'] = "User program is running!"
            self.send(json.dumps(data))
            
            
            consoleWelcome = {}
            consoleWelcome['serverPush'] = "sysConsole"
            global lastLaunched
            lastLaunched = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            consoleWelcome['data'] = 'WeIO user server launched ' + lastLaunched
            shared.editor(data)
            #CONSOLE.send(json.dumps(consoleWelcome))
        else : # FILE DON'T EXIST
            warning = {}
            warning['requested'] = rq['request']
            warning['status'] = "weioUserServer.py don't exist!"
            warning['state'] = "error"
            self.send(json.dumps(warning))

    def stop(self, rq):
        """Stop running application"""
        
        global weioPipe
        global stdoutHandlerIsLive
        global stderrHandlerIsLive
        
        #print "STDOUT ", stdoutHandlerIsLive, " STDERR ", stderrHandlerIsLive
        if weioPipe != None :
            #print "POLL PIPE ", weioPipe.poll()
            if stdoutHandlerIsLive is True:
                ioloopObj.remove_handler(weioPipe.stdout.fileno())
                stdoutHandlerIsLive = False
            if stderrHandlerIsLive is True:
                ioloopObj.remove_handler(weioPipe.stderr.fileno())
                stderrHandlerIsLive = False
        
            if weioPipe.poll() is None :
                weioPipe.kill()
                    
            weioPipe = None
            
            data = {}
            data['requested'] = rq['request']
            data['status'] = "User program stopped!"
            self.send(json.dumps(data))
            
            if lastLaunched is not None :
                consoleWelcome = {}
                consoleWelcome['serverPush'] = "sysConsole"
                consoleWelcome['data'] = 'WeIO user program stoped. It was runnig since : ' + lastLaunched
                shared.editor(consoleWelcome)
                
                global lastLaunched
                lastLaunched = None

    def weioMainHandler(self, data, fd, events):
        """Stream stdout to browser"""
        
        global weioPipe
        line = weioPipe.stdout.readline()
        if line :
            # parse incoming data
            #stdout = line.rstrip()
            stdout = line
            print(stdout)
            
            #pack and go
            data = {}
            
            data['serverPush'] = 'stdout'
            data['data'] = stdout
            
            # TODO, send this only once, at the beginning
            data['status'] = "Check output console"
            
            # this is raw output, some basic parsing is needed in javascript \n etc...
            shared.editor(data)
        #   CONSOLE.send(json.dumps(data))
        
        if weioPipe.poll() is not None :
            """ Child is terminated STDOUT"""
            print "Child has terminated - removing handler STDOUT"
            global stdoutHandlerIsLive
            ioloop.IOLoop.instance().remove_handler(weioPipe.stdout.fileno())
            stdoutHandlerIsLive = False;
            return


    def weioMainHandlerErr(self, data, fd, events):
        """Stream stderr to browser"""
        global weioPipe
        global errLine
        
        line = weioPipe.stderr.readline()
        if line :
            # parse incoming data
            #stdout = line.rstrip()
            stderr = line
            print(stderr)
            
            #pack and go
            data = {}
            
            data['serverPush'] = 'stderr'
            data['data'] = stderr
            
            # TODO, send this only once, at the beginning
            data['status'] = "Check output console for errors!"
            
            if 'Traceback (most recent call last):' in stderr :
                print "traceback info is comming..."
                errLine = 0
            
            print "ERR " +  str(errLine) + " : " + stderr
            errLine+=1
            if 'File "' in stderr :
                global errObject
                global errCoords
                
                errCoords = 1
                oneError = {}
                
                arg = stderr.split(",")
                errInFile = arg[0].split('"')
                errInFile = errInFile[1]

                print "error in file : ", errInFile
                #data['errFile'] = errInFile
                oneError['file'] = errInFile
                
                errInLine = arg[1].split("line")
                errInLine = errInLine[1]
                oneError['line'] = errInLine.split()
                
                print "error in line : ", errInLine
                #data['errLine'] = errInLine
                
                # add error object to array
                errObject.append(oneError)
            
                
            errReason = stderr
            
            # this is raw output, some basic parsing is needed in javascript \n etc...
            shared.editor(data)
            #CONSOLE.send(json.dumps(data))
        
        if weioPipe.poll() is not None :
            """ Child is terminated STDERR"""
            print "Child has terminated - removing handler STDERR"
            global stderrHandlerIsLive
            global errObject
            global errLine
            global errReason
            errLine = 0
            data = {}
            data['serverPush'] = 'errorObjects'
            
            if (len(errObject)>0):
                errObject[len(errObject)-1]['reason'] = errReason
            
                data['data'] = errObject
                errObject = []
                shared.editor(data)
                #CONSOLE.send(json.dumps(data))
                print "ERR ",errObject
            ioloop.IOLoop.instance().remove_handler(weioPipe.stderr.fileno())
            stderrHandlerIsLive = False
            
            return

    def sendPlatformDetails(self, rq):
        
        # get configuration from file
        config = weio_config.getConfiguration()
        
        data = {}
        
        platformS = ""
        
        platformS += "WeIO version " + config["weio_version"] + " with Python " + platform.python_version() + " on " + platform.system() + "<br>"
        platformS += "GPL 3, Nodesign.net 2013 Uros Petrevski & Drasko Draskovic <br>"
        
        data['serverPush'] = 'sysConsole'
        data['data'] = platformS
        shared.editor(data)
        #CONSOLE.send(json.dumps(data))

    def getUserProjectsList(self, rq):
        
        # get configuration from file
        config = weio_config.getConfiguration()
        
        data = {}
        data['requested'] = rq['request']
        data['data'] = weioFiles.listOnlyFolders(config["user_projects_path"])
        self.send(json.dumps(data))
        
    def changeProject(self,rq):
        
        # get configuration from file
        config = weio_config.getConfiguration()
        
        config["last_opened_project"] = rq['data']+"/"
        weio_config.saveConfiguration(config);
        
        data = {}
        data['requested'] = rq['request']
        self.send(json.dumps(data))
        
        rqlist = ["stop", "getLastProjectName", "getUserProjetsFolderList"]
        
        for i in range(0,len(rqlist)):
            rq['request'] = rqlist[i]
            callbacks[rq['request']](self, rq)
        
                    
    def sendUserData(self,rq):
        data = {}
        # get configuration from file
        config = weio_config.getConfiguration()
        data['requested'] = rq['request']
        
        data['name'] = config["user"]
        self.send(json.dumps(data))

    def newProject(self, rq):
        
        config = weio_config.getConfiguration()
        
        data = {}
        data['requested'] = rq['request']
        path = rq['path']

        weioFiles.createDirectory(config["user_projects_path"] + path)
        # ADD HERE SOME DEFAULT FILES
        # adding __init__.py
        weioFiles.saveRawContentToFile(config["user_projects_path"] + path + "/__init__.py", "")
        
        data['status'] = "New project created"
        data['path'] = path
        self.send(json.dumps(data))

    def deleteCurrentProject(self, rq):
        
        data = {}
        data['requested'] = rq['request']

        config = weio_config.getConfiguration()
        projectToKill = config["last_opened_project"]
        
        weioFiles.removeDirectory(config["user_projects_path"]+projectToKill)
        
        folders = weioFiles.listOnlyFolders(config["user_projects_path"])
        
        if len(folders) > 0 :
            config["last_opened_project"] = folders[0]
            weio_config.saveConfiguration(config)
        
            data['data'] = "reload page"
        else :
            data['data'] = "ask to create new project"
        
        self.send(json.dumps(data))

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
        'packetRequests': iteratePacketRequests
        
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
            print "unrecognised request ", rq['request']