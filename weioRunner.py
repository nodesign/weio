#!/usr/bin/python -u

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


from tornado import web, ioloop, options, websocket, httpserver

import sys, os, logging, platform, json, signal, datetime

import multiprocessing
import threading

import functools
import subprocess



import pickle

# JS to PYTHON handler
from handlers.weioJSPYHandler import WeioHandler, WeioHandlerRemote

# IMPORT BASIC CONFIGURATION FILE ALL PATHS ARE DEFINED INSIDE
from weioLib import weioConfig

# IMPORT WEIO FILE SUPPORT
from weioLib import weioFiles

from sockjs.tornado import SockJSRouter, SockJSConnection

# Import globals for user Tornado
from weioLib import weioRunnerGlobals

from weioLib import weioParser

# Global list of user processes
userProcessList = []
userEventList = []

from weioLib import weioUserApi
from weioLib import weioGpio
from weioLib import weioIO

import time

# Global httpServer
httpServer = None

###
# HTTP SERVER HANDLER
###
# This is user project index.html
class WeioIndexHandler(web.RequestHandler):
    def get(self):
        firstTimeSwitch = confFile['first_time_run']
        #print firstTimeSwitch

        if (firstTimeSwitch=="YES") :
            path = "www/signin.html"
        else :
            path = "www/userIndex.html"
            
            #if (weioFiles.checkIfFileExists(confFile['last_opened_project'] + "/index.html")):
            #    path = "www/userIndex.html"

            #else :
            #    path = "www/error404.html"
        #path = confFile['last_opened_project'] + "index.html"

        self.render(path, error="")


###
# WeIO User Event Handler
###
class UserControl():
    def __init__(self):
        self.errLine = 0
        self.errObject = []
        self.errReason = ""
        self.lastCalledProjectPath = None

        # Variable to store SockJSConnection calss instance
        # in order to call it's send() method from MainProgram thread
        CONSOLE = None

        self.connection = None

        # Ask this variable is player is playing at this moment
        self.playing = False

        # List of user processes
        self.userProcessList = []
        self.userEventList = []

        # launcherProcess
        self.launcherProcess = None

        self.qIn = weioRunnerGlobals.QOUT
        self.qOut = weioRunnerGlobals.QIN

        self.userMain = {}

    def setConnectionObject(self, connection):
        # captures only the last connection
        self.connection = connection

    def send(self, data):
        # if no connection object (editor is not opened) than data for editor is lost
        if not(self.connection is None):
            self.connection.send(data)

    def start(self, rq={'request':'play'}):
        if (httpServer is not None):
            httpServer.listen(options.options.port, options.options.addr)
            logging.info(" [*] Listening on 0.0.0.0:" + str(options.options.port))
            #print "*SYSOUT* User API Websocket is created at localhost:" + str(options.options.port) + "/api"

        #print "STARTING USER PROCESSES"
        self.launcherProcess = multiprocessing.Process(target=self.launcher)
        self.launcherProcess.start()

    def stop(self):
        if (httpServer is not None):
            httpServer.stop()

        weioRunnerGlobals.running.value = False

        # Removing all User Events
        weioParser.removeUserEvents()

        #print "STOPPING USER PROCESSES"

        #print "=======<> self.launcherProcess ", self.launcherProcess

        if (self.launcherProcess != None):
            self.launcherProcess.terminate()
            self.launcherProcess.join(0.5)
            try:
                # If job is not properly done than kill it with bazooka
                os.kill(self.launcherProcess.pid, 9) # very violent
            except:
                pass

        self.launcherProcess = None

        # Reset user attached elements
        weioUserApi.attach.procs = {}
        weioUserApi.attach.events = {}
        weioUserApi.attach.ints = {}

        # Clear all connetions
        weioRunnerGlobals.weioConnections.clear()

        # Empty the Queue of all messages
        while self.qIn.empty() == False:
            self.qIn.get()

        while self.qOut.empty() == False:
            self.qOut.get()


    def userPlayer(self, fd, events):
        if (fd is not None):
            cmd = os.read(fd,128)
            cmd = cmd.split('*')[-2]
        else:
            return

        if (cmd == "START"):
            # First stop all pending processes
            # and reset all pending events before re-loading new ones
            if (self.launcherProcess is not None):
                self.stop()

            # Then start processes from it
            self.start()

        elif (cmd == "STOP"):
            self.stop()


    def launcher(self):
        #print "======>>> LAUNCHING..."
        # Re-load user main (in case it changed)
        confFile = weioConfig.getConfiguration()

        # Get the last name of project and run it
        projectModule = confFile["last_opened_project"].replace('/', '.') + ".main"
        #print "CALL", projectModule
        # Init GPIO object for uper communication
        if (weioRunnerGlobals.WEIO_SERIAL_LINKED == False):
            try :
                weioIO.gpio = weioGpio.WeioGpio()
            except:
                print "LPC coprocessor is not present"
                weioIO.gpio = None

        # Import userMain from local module
        try :
            self.userMain = __import__(projectModule, fromlist=[''])
        except :
            print "MODULE CAN'T BE LOADED. Maybe you have some errors in modules that you wish to import?"
            result = None


        # Calling user setup() if present
        if "setup" in vars(self.userMain):
            self.userMain.setup()

        # Add user events
        #print "ADDING USER EVENTS"
        for key in weioUserApi.attach.events:
            #print weioUserApi.attach.events[key].handler
            weioParser.addUserEvent(weioUserApi.attach.events[key].event,
                    weioUserApi.attach.events[key].handler)

        # Launching threads
        for key in weioUserApi.attach.procs:
            #print key
            t = threading.Thread(target=weioUserApi.attach.procs[key].procFnc,
                        args=weioUserApi.attach.procs[key].procArgs)
            t.daemon = True
            # Start it
            t.start()
            #print "STARTING PROCESS PID", t.pid

        weioRunnerGlobals.running.value = True

        while (True):
            # Get the command from userTornado (blocking)
            msg = self.qIn.get()
            #print "*** GOT THE COMMAND: ", msg.req
            # Execute the command
            msg.res = None
            if msg.req in weioParser.weioSpells or msg.req in weioParser.weioUserSpells:
                if msg.req in weioParser.weioSpells:
                    msg.res = weioParser.weioSpells[msg.req](msg.data)
                elif msg.req in weioParser.weioUserSpells:
                    msg.res = weioParser.weioUserSpells[msg.req](msg.data)
            else:
                msg.res = None

            # Send back the result
            self.qOut.put(msg)



# User Tornado signal handler
def signalHandler(userControl, sig, frame):
        # CALLING STOP IF PRESENT
        if "stop" in vars(userControl.userMain):
            userControl.userMain.stop()

        if (weioIO.gpio != None):
            if (weioRunnerGlobals.WEIO_SERIAL_LINKED == True):
                weioIO.gpio.stopReader()
                weioIO.gpio.reset()
        sys.exit(0)


def listenerThread():
    #print "*** Starting listenerThread"
    while (True):
        msg = weioRunnerGlobals.QIN.get()
        #print "GOT MSG: ", msg
        if (msg.res is not None):
            #print "MESSAGE", msg.req, msg.res, msg.data, msg.connUuid
            if (msg.connUuid in weioRunnerGlobals.weioConnections or msg.connUuid == "all"):
                result = {}

                if (msg.callbackJS is not None):
                    result["serverPush"] = msg.callbackJS
                    result["data"] = msg.res
                    #print "RESULT",result
                    if (weioRunnerGlobals.remoteConnected.value == True):
                        if (msg.connUuid == "all"):
                            for connUuid, conn in weioRunnerGlobals.weioConnections.iteritems():
                                weioRunnerGlobals.weioConnections[connUuid].send(json.dumps(result))
                        else:
                            weioRunnerGlobals.weioConnections[msg.connUuid].write_message(json.dumps(result))
                    else:
                        if (msg.connUuid == "all"):
                            for connUuid, conn in weioRunnerGlobals.weioConnections.iteritems():
                                weioRunnerGlobals.weioConnections[connUuid].send(json.dumps(result))
                        else:
                            weioRunnerGlobals.weioConnections[msg.connUuid].send(json.dumps(result))

class WeioRemote():
    conn = None
    keepalive = None

    def __init__(self, uri, remoteHandler):
        self.uri = uri
        self.connectRemote()
        self.rh = remoteHandler

    def connectRemote(self):
        w = websocket.websocket_connect(self.uri)
        w.add_done_callback(self.wsConnectionCb)

    def dokeepalive(self):
        stream = self.conn.protocol.stream
        #if not stream.closed():
        #    self.keepalive = stream.io_loop.add_timeout(timedelta(seconds=PING_TIMEOUT), self.dokeepalive)
        #    self.conn.protocol.write_ping("")
        #else:
        #self.keepalive = None # should never happen

    def wsConnectionCb(self, conn):
        self.conn = conn.result()

        # Set this connection for WeioHandlerRemote
        self.rh.setRemoteConn(self.conn)
        weioRunnerGlobals.remoteConnected.value = True

        self.conn.on_message = self.message
        self.conn.write_message('Hello from WeIO')
        #self.keepalive = IOLoop.instance().add_timeout(timedelta(seconds=PING_TIMEOUT), self.dokeepalive)

    def message(self, message):
        if message is not None:
            #print('>> %s' % message)
            self.rh.on_message(message)
        else:
            self.close()

    def close(self):
        weioRunnerGlobals.remoteConnected.value = False
        self.rh.on_close()
        print('conn closed')

        #if self.keepalive is not None:
        #    keepalive = self.keepalive
        #    self.keepalive = None
        #    IOLoop.instance().remove_timeout(keepalive)

        #self.connectRemote()


if __name__ == '__main__':
    ###
    # Initialize global USER API instances
    ###
    m = multiprocessing.Manager()
    weioUserApi.attach =  weioUserApi.WeioAttach()
    #weioUserApi.shared =  weioUserApi.WeioSharedVar()
    weioUserApi.console =  weioUserApi.WeioPrint()

    manager = multiprocessing.Manager()
    weioUserApi.sharedVar = manager.dict()

    # weioMsg
    weioUserApi.weioServerMsg = weioUserApi.WeioServerMsg(weioRunnerGlobals.QIN, weioRunnerGlobals.userAgentMessage())

    # weioConnUuids
    weioRunnerGlobals.weioConnUuids = manager.list()
    weioUserApi.weioConns = weioRunnerGlobals.weioConnUuids

    confFile = weioConfig.getConfiguration()
    # set python working directory
    #os.chdir("userFiles/"+sys.argv[1])
    myPort = confFile["userAppPort"]
    options.define("port", default=myPort, type=int)

    options.define("addr", default=confFile['ip'])

    apiRouter = SockJSRouter(WeioHandler, '/api')

    # Instantiate all handlers for user Tornado
    app = web.Application(apiRouter.urls + [
    ('/', WeioIndexHandler),
    (r"/(.*)", web.StaticFileHandler, {"path": "www"})
    ])
    #app.listen(options.options.port, "0.0.0.0")

    if (confFile["remote"] != ""):
        rHdlr = WeioHandlerRemote()
        print "Connecting to remote app..."
        rUri = os.path.join("ws://", confFile['remote'], "weio")
        #print rUri
        r = WeioRemote(rUri, rHdlr)

    else:
        if (confFile["https"] == "YES"):
            httpServer = httpserver.HTTPServer(app,
                ssl_options={
                    "certfile": os.path.join(confFile['absolut_root_path'], "weioSSL.crt"),
                    "keyfile": os.path.join(confFile['absolut_root_path'], "weioSSL.key"),
                })
        else:
            # Plain ol' HTTP
            httpServer = httpserver.HTTPServer(app)

    # Create a userControl object
    userControl = UserControl()
    #print "start user script"
    #userControl.start()

    # Install signal handlers
    signalCallback = functools.partial(signalHandler, userControl)
    signal.signal(signal.SIGTERM, signalCallback)
    signal.signal(signal.SIGINT, signalCallback)

    # Start listener thread
    t = threading.Thread(target=listenerThread)
    t.daemon = True
    # Start it
    t.start()

    # Create ioloop
    ioloop = ioloop.IOLoop.instance()

    # Add user control via stdin pipe
    ioloop.add_handler(sys.stdin.fileno(), userControl.userPlayer, ioloop.READ)

    # Before starting ioloop, stop led blinking,
    # which will light up correct LED and give information to the user
    # that all is ready
    if (platform.machine() == 'mips'):
        subprocess.call(["/etc/init.d/led_blink", "stop"])

    ioloop.start()
