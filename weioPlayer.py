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

from tornado import web, ioloop, iostream, gen
import os, signal, sys, platform, subprocess, datetime
import functools

import json
from weioLib import weio_config
from weioLib import weioFiles

class WeioPlayer():
    
    def __init__(self):
        self.errObject = []
        self.errReason = ""
    
        # Variable to store SockJSConnection calss instance
        # in order to call it's send() method from MainProgram thread
        self.weioPipe = None
    
        # Variable to store SockJSConnection calss instance
        # in order to call it's send() method from MainProgram thread
        CONSOLE = None
        
        # Object to store ioloop handlers that drive sterr &
        # stdout from user program
        self.ioloopObj = None
        
        # Handler sanity, True alive, False dead
        self.stdoutHandlerIsLive = None
        self.stderrHandlerIsLive = None
    
        self.connection = None
        
        # Ask this variable is player is plaing at this moment
        self.playing = False

    def setConnectionObject(self, connection):
        # captures only the last connection
        self.connection = connection
    
    def send(self, data):
        # if no connection object (editor is not opened) than data for editor is lost
        if not(self.connection is None):
            self.connection.send(data)
    
    def delegateToEditorHandler(self,data):
        # if no connection object (editor is not opened) than data for editor is lost
        if not(self.connection is None):
            self.connection.delegateToEditorHandler(data)
    
    def play(self, rq={'request':'play'}):
        """ This is where all the magic happens.
            
            "Play" button will spawn a new subprocess
            which will execute users program written in the editor.
            This subprocess will communicate with Tornado wia non-blocking pipes,
            so that Tornado can simply transfer subprocess's `stdout` and `stderr`
            to the client via WebSockets. """
        
        # get configuration from file
        config = weio_config.getConfiguration()
        
        # stop if process is already running
        self.stop()
        
        data = {}
        up = config["user_projects_path"]
        lp = config["last_opened_project"]

        processName = './weioRunner.py'
        
        
        # check if user project exists before launching
        
        if (weioFiles.checkIfFileExists(up+lp+"main.py")):
            #launch process
            
            lp = lp.split("/")[0]

            print("weioMain indipendent process launching...")
            
            
            self.weioPipe = subprocess.Popen([processName, lp], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.ioloopObj = ioloop.IOLoop.instance()
            
            # Callback for STDOUT
            #callback = functools.partial(self.socket_connection_ready, sock)
            callback = functools.partial(self.weioMainHandler, data)
            #ioloopObj.add_handler(sock.fileno(), callback, ioloopObj.READ)
            self.ioloopObj.add_handler(self.weioPipe.stdout.fileno(), callback, self.ioloopObj.READ)
            self.stdoutHandlerIsLive = True;
            
            # Callback for STDERR
            callbackErr = functools.partial(self.weioMainHandlerErr, data)
            self.ioloopObj.add_handler(self.weioPipe.stderr.fileno(), callbackErr, self.ioloopObj.READ)
            self.stderrHandlerIsLive = True;
            
            # Inform client the we run subprocess
            data['requested'] = rq['request']
            data['status'] = "Warming up the engines..."
            self.send(json.dumps(data))
            
            
            consoleWelcome = {}
            consoleWelcome['serverPush'] = "sysConsole"
            
            self.lastLaunched = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            consoleWelcome['data'] = 'WeIO user server launched ' + self.lastLaunched
            self.delegateToEditorHandler(data)
            self.playing = True
        
        #CONSOLE.send(json.dumps(consoleWelcome))
        else : # FILE DON'T EXIST
            warning = {}
            warning['requested'] = rq['request']
            warning['status'] = "main.py don't exist!"
            warning['state'] = "error"
            self.send(json.dumps(warning))
    
    def stop(self, rq={'request':'stop'}):
        """Stop running application"""

        self.playing = False
        #print "STDOUT ", self.stdoutHandlerIsLive, " STDERR ", self.stderrHandlerIsLive
        if not(self.weioPipe is None) :
            #print "POLL PIPE ", weioPipe.poll()
            if self.stdoutHandlerIsLive is True:
                self.ioloopObj.remove_handler(self.weioPipe.stdout.fileno())
                self.stdoutHandlerIsLive = False
            if self.stderrHandlerIsLive is True:
                self.ioloopObj.remove_handler(self.weioPipe.stderr.fileno())
                self.stderrHandlerIsLive = False
            
            if self.weioPipe.poll() is None :
                self.weioPipe.kill()
            
            self.weioPipe = None
            
            data = {}
            data['requested'] = rq['request']
            data['status'] = "User program stopped!"
            self.send(json.dumps(data))
            
            if self.lastLaunched is not None :
                consoleWelcome = {}
                consoleWelcome['serverPush'] = "sysConsole"
                consoleWelcome['data'] = 'WeIO user program stoped. It was runnig since : ' + self.lastLaunched
                self.delegateToEditorHandler(consoleWelcome)
                
                self.lastLaunched = None

    def weioMainHandler(self, data, fd, events):
        """Stream stdout to browser"""
        
        
        line = self.weioPipe.stdout.readline()
        if line :
            # parse incoming data
            #stdout = line.rstrip()
            stdout = line
            print(stdout)
            
            #pack and go
            data = {}
            
            if ("*SYSOUT*" in line) :
                stdout = line.split("*SYSOUT*")[1]
                data['serverPush'] = 'sysConsole'
            else :
                data['serverPush'] = 'stdout'
            data['data'] = stdout
            
            # TODO, send this only once, at the beginning
            data['status'] = "Check output console"
            
            # this is raw output, some basic parsing is needed in javascript \n etc...
            self.delegateToEditorHandler(data)
        #   CONSOLE.send(json.dumps(data))
        
        if self.weioPipe.poll() is not None :
            """ Child is terminated STDOUT"""
            print "Child has terminated - removing handler STDOUT"
            self.playing = False
            ioloop.IOLoop.instance().remove_handler(self.weioPipe.stdout.fileno())
            self.stdoutHandlerIsLive = False;
            return
    
    
    def weioMainHandlerErr(self, data, fd, events):
        """Stream stderr to browser"""
        
        self.playing = False
        line = self.weioPipe.stderr.readline()
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
                self.errLine = 0
            
            print "ERR " +  str(self.errLine) + " : " + stderr
            self.errLine+=1
            if 'File "' in stderr :
                
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
                self.errObject.append(oneError)
            
            
            self.errReason = stderr
            
            # this is raw output, some basic parsing is needed in javascript \n etc...
            self.delegateToEditorHandler(data)
        #CONSOLE.send(json.dumps(data))
        
        if self.weioPipe.poll() is not None :
            """ Child is terminated STDERR"""
            print "Child has terminated - removing handler STDERR"
            self.playing = False
            self.errLine = 0
            data = {}
            data['serverPush'] = 'errorObjects'
            if (len(self.errObject)>0):
                self.errObject[len(self.errObject)-1]['reason'] = self.errReason
                
                data['data'] = self.errObject
                self.errObject = []
                self.delegateToEditorHandler(data)
                #CONSOLE.send(json.dumps(data))
                print "ERR ",self.errObject
            ioloop.IOLoop.instance().remove_handler(self.weioPipe.stderr.fileno())
            self.stderrHandlerIsLive = False
            
            return


player = WeioPlayer()
