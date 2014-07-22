#!/usr/bin/python -u
from tornado import web, ioloop, options, websocket

import sys,os,logging, platform, json, signal, datetime

import multiprocessing
import threading

import functools
import subprocess

from weioLib import weioUserApi
from weioLib import weioIO

import pickle

# JS to PYTHON handler
from handlers.weioJSPYHandler import WeioHandler

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

        path = "www/userIndex.html"

        #path = confFile['last_opened_project'] + "index.html"

        self.render(path, error="")


###
# WeIO User Even Handler
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
        weioRunnerGlobals.running = False
        fRunning = open('/weio/running.p', 'wb')
        pickle.dump(weioRunnerGlobals.running, fRunning)
        fRunning.close()
        
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

                # Initialize globals for the user Tornado
                weioRunnerGlobals.DECLARED_PINS = weioIO.gpio.declaredPins
            except:
                print "LPC coprocessor is not present"
                weioIO.gpio = None

        # Import userMain from local module
        try :
            userMain = __import__(projectModule, fromlist=[''])
        except :
            print "MODULE CAN'T BE LOADED. Maybe you have some import errors?"
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
        
        weioRunnerGlobals.running = True
        fRunning = open('/weio/running.p', 'wb')
        pickle.dump(weioRunnerGlobals.running, fRunning)
        fRunning.close()

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

        if (msg.res is not None):
            #print "MESSAGE",msg.req, msg.res, msg.data, msg.connUuid
            if (msg.connUuid in weioRunnerGlobals.weioConnections):
                result = {}

                if (msg.callbackJS is not None):
                    result["serverPush"] = msg.callbackJS
                    result["data"] = msg.res
                    #print "RESULT",result
                    weioRunnerGlobals.weioConnections[msg.connUuid].send(json.dumps(result))

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
    app.listen(options.options.port, "0.0.0.0")

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
