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

from tornado import web, ioloop, iostream, gen
import os, signal, sys, platform, subprocess, datetime
import functools

import json
from weioLib import weioConfig
from weioLib import weioFiles

# Import globals for main Tornado
from weioLib import weioIdeGlobals
from shutil import copyfile

class WeioPlayer():
    def __init__(self):
        self.errLine = 0
        self.errObject = []
        self.errReason = ""

        # Variable to store SockJSConnection calss instance
        # in order to call it's send() method from MainProgram thread
        self.weioPipe = None

        # Object to store ioloop handlers that drive sterr &
        # stdout from user program
        self.ioloopObj = None

        # Handler sanity, True alive, False dead
        self.stdoutHandlerIsLive = None
        self.stderrHandlerIsLive = None

        self.connection = None

        # Ask this variable is player is plaing at this moment
        self.playing = False

        self.lastLaunched = None

    def setConnectionObject(self, connection):
        # captures only the last connection
        self.connection = connection

    def send(self, data):
        # if no connection object (editor is not opened) than data for editor is lost
        if not(self.connection is None):
            self.connection.send(data)

    def startUserTornado(self):
        data = {}

        processName = './weioRunner.py'

        #print("weioMain indipendent process launching...")

        self.weioPipe = subprocess.Popen([processName], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


    def play(self, rq={'request':'play'}):
        """ This is where all the magic happens.

            "Play" button will spawn a new subprocess
            which will execute users program written in the editor.
            This subprocess will communicate with Tornado wia non-blocking pipes,
            so that Tornado can simply transfer subprocess's `stdout` and `stderr`
            to the client via WebSockets. """

        # stop if process is already running
        if (self.playing is True):
            self.stop()
            
        # Inform client the we run subprocess
        data = {}
        data['requested'] = rq['request']
        data['status'] = "WeIO is running!"
        self.send(json.dumps(data))

        consoleWelcome = {}
        consoleWelcome['data'] = "WeIO user program started"
        consoleWelcome['serverPush'] = "sysConsole"

        self.lastLaunched = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        consoleWelcome['data'] = 'WeIO user server launched ' + self.lastLaunched
        if (weioIdeGlobals.CONSOLE != None):
            #weioIdeGlobals.CONSOLE.send(json.dumps(data))
            weioIdeGlobals.CONSOLE.send(json.dumps(consoleWelcome))
        self.playing = True

        # send *start* command to user tornado
        self.weioPipe.stdin.write("*START*")
            

    def stop(self, rq={'request':'stop'}):
        """Stop running application"""
        self.playing = False

        data = {}
        data['requested'] = rq['request']
        data['status'] = "User program stopped!"
        self.send(json.dumps(data))

        # Send *STOP* command to User Tornado
        self.weioPipe.stdin.write("*STOP*")

        if self.lastLaunched is not None :
            consoleWelcome = {}
            consoleWelcome['serverPush'] = "sysConsole"
            consoleWelcome['data'] = 'WeIO user program stoped. It was runnig since : ' + self.lastLaunched
            if (weioIdeGlobals.CONSOLE != None):
                weioIdeGlobals.CONSOLE.send(json.dumps(consoleWelcome))

            self.lastLaunched = None

    def weioMainHandler(self, data, fd, events):
        """Stream stdout to browser"""
        line = self.weioPipe.stdout.readline()
        print "STDOUT ", line
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
            if (weioIdeGlobals.CONSOLE != None):
                weioIdeGlobals.CONSOLE.send(json.dumps(data))

        if self.weioPipe.poll() is not None :
            """ Child is terminated STDOUT"""
            #print "Child has terminated - removing handler STDOUT"
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
                #print "traceback info is comming..."
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
            if (weioIdeGlobals.CONSOLE != None):
                weioIdeGlobals.CONSOLE.send(json.dumps(data))

        if self.weioPipe.poll() is not None :
            """ Child is terminated STDERR"""
            #print "Child has terminated - removing handler STDERR"
            self.playing = False
            self.errLine = 0
            data = {}
            data['serverPush'] = 'errorObjects'
            if (len(self.errObject)>0):
                self.errObject[len(self.errObject)-1]['reason'] = self.errReason

                data['data'] = self.errObject
                self.errObject = []
                if (weioIdeGlobals.CONSOLE != None):
                    weioIdeGlobals.CONSOLE.send(json.dumps(data))
                print "ERR ",self.errObject
            ioloop.IOLoop.instance().remove_handler(self.weioPipe.stderr.fileno())
            self.stderrHandlerIsLive = False

            return
