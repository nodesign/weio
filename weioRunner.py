#!/usr/bin/python -u
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

###
# HTTP SERVER HANDLER
###
# This is user project index.html
class WeioIndexHandler(web.RequestHandler):
    def get(self):
        firstTimeSwitch = confFile['first_time_run']
        #print firstTimeSwitch

        if (firstTimeSwitch=="YES") :
           path = "www/firstTime.html"
        else :
            if (weioFiles.checkIfFileExists(confFile['last_opened_project'] + "/index.html")):
                path = "www/userIndex.html"

            else :
                path = "www/error404.html"

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

    def setConnectionObject(self, connection):
        # captures only the last connection
        self.connection = connection

    def send(self, data):
        # if no connection object (editor is not opened) than data for editor is lost
        if not(self.connection is None):
            self.connection.send(data)

    def start(self, rq={'request':'play'}):
        #print "STARTING USER PROCESSES"

        self.launcherProcess = multiprocessing.Process(target=self.launcher)
        self.launcherProcess.start()

    def stop(self):
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
            if (self.launcherProcess != None):
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
            userMain = __import__(projectModule, fromlist=[''])
        except :
            print "MODULE CAN'T BE LOADED. Maybe you have some errors in modules that you wish to import?"
            result = None


        # Calling user setup() if present
        if "setup" in vars(userMain):
            userMain.setup()

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
        #logging.warning('Caught signal: %s', sig)
        #print "CALLING STOP IF PRESENT"
        #if "stop" in vars(userControl.userMain):
        #    logging.warning('Calling user defined stop function')
        #    userControl.userMain.stop()
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
            if (msg.connUuid in weioRunnerGlobals.weioConnections):
                result = {}

                if (msg.callbackJS is not None):
                    result["serverPush"] = msg.callbackJS
                    result["data"] = msg.res
                    #print "RESULT",result
                    if (weioRunnerGlobals.remoteConnected.value == True):
                        weioRunnerGlobals.weioConnections[msg.connUuid].write_message(json.dumps(result))
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
    weioUserApi.attach =  weioUserApi.WeioAttach()
    weioUserApi.shared =  weioUserApi.WeioSharedVar()
    weioUserApi.console =  weioUserApi.WeioPrint()

    confFile = weioConfig.getConfiguration()
    # set python working directory
    #os.chdir("userFiles/"+sys.argv[1])
    myPort = confFile["userAppPort"]
    options.define("port", default=myPort, type=int)

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
            http_server = httpserver.HTTPServer(app,
                ssl_options={
                    "certfile": os.path.join(confFile['absolut_root_path'], "weioSSL.crt"),
                    "keyfile": os.path.join(confFile['absolut_root_path'], "weioSSL.key"),
                })
        else:
            # Plain ol' HTTP
            http_server = httpserver.HTTPServer(app)

        http_server.listen(options.options.port, address=confFile['ip'])

        logging.info(" [*] Listening on 0.0.0.0:" + str(options.options.port))
        print "*SYSOUT* User API Websocket is created at localhost:" + str(options.options.port) + "/api"

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
