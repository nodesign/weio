#!/usr/bin/python -u
from tornado import web, ioloop, options, websocket

import sys,os,logging, platform, json, signal, datetime

import multiprocessing

from weioLib.weioUserApi import *
from weioLib.weioIO import *

# JS to PYTHON handler
from handlers.weioJSPYHandler import WeioHandler
# Connected clients
from handlers.weioJSPYHandler import connections

# IMPORT BASIC CONFIGURATION FILE ALL PATHS ARE DEFINED INSIDE
from weioLib import weio_config

# IMPORT WEIO FILE SUPPORT
from weioLib import weioFiles

from sockjs.tornado import SockJSRouter, SockJSConnection

# Global list of user processes
userProcessList = []

################################################################ HTTP SERVER HANDLER
# This is user project index.html
class WeioIndexHandler(web.RequestHandler):
    def get(self):
        firstTimeSwitch = confFile['first_time_run']
        #print firstTimeSwitch

        if (firstTimeSwitch=="YES") :
           path = "www/firstTime.html"
        else :
           if (weioFiles.checkIfFileExists(confFile['user_projects_path'] + confFile['last_opened_project'] + "index.html")):
              path = "www/userIndex.html"
           else :
              path = "www/error404.html"
        path = "www/userIndex.html"
        self.render(path, error="")


###
# WeIO User Even Handler
###
class UserControl():
    def __init__(self):
        self.errLine = 0
        self.errObject = []
        self.errReason = ""

        # Variable to store SockJSConnection calss instance
        # in order to call it's send() method from MainProgram thread
        CONSOLE = None

        self.connection = None

        # Ask this variable is player is playing at this moment
        self.playing = False

    def setConnectionObject(self, connection):
        # captures only the last connection
        self.connection = connection

    def send(self, data):
        # if no connection object (editor is not opened) than data for editor is lost
        if not(self.connection is None):
            self.connection.send(data)

    def start(self, rq={'request':'play'}):
        print "STARTING USER PROCESSES"
        # Launching threads
        for key in attach.procs :
            print key
            p = multiprocessing.Process(target=attach.procs[key].procFnc, args=attach.procs[key].procArgs)
            p.daemon = True
            # Add it to the global list of user processes
            userProcessList.append(p)
            # Start it
            p.start()

    def stop(self):
        print "STOPPING USER PROCESSES"
        for p in userProcessList:
            p.terminate()
            p.join()
            userProcessList.remove(p)

        # Finally stop UPER
        #logging.warning('Shutdown WeIO coprocessor')
        stopWeio()

    def userPlayer(self, fd, events):
        print "Inside userControl()"

        cmd = os.read(fd,128)
        print "Received: " + cmd

        if (cmd == "*START*"):
            self.start()
        elif (cmd == "*STOP*"):
            self.stop()



class WeioUserControlHandler(SockJSConnection):
    def on_open(self, data):
        userControl.setConnectionObject(self)

    def on_message(self, data):
        global userControl
        """Parsing JSON data that is comming from browser into python object"""
        message = json.loads(data)
        if (message["request"] == "play"):
            userControl.start()
        elif (message["request"] == "stop"):
            userControl.stop()

    


    def on_close(self):
        pass
###


if __name__ == '__main__':

    confFile = weio_config.getConfiguration()

    # Get the last name of project and run it
    projectModule = "userFiles."+confFile["last_opened_project"].replace('/', '.') + "main"

    # 2.6+ WAY TO IMPORT FROM LOCAL
    main = __import__(projectModule, fromlist=[''])

    # set python working directory
    #os.chdir("userFiles/"+sys.argv[1])
    myPort = confFile["userAppPort"]
    options.define("port", default=myPort, type=int)

    apiRouter = SockJSRouter(WeioHandler, '/api')

    # Instantiate all handlers for user Tornado
    app = web.Application(apiRouter.urls + [
    ('/', WeioIndexHandler),
    (r"/(.*)", web.StaticFileHandler, {"path": "www/"})
    ])
    app.listen(options.options.port, "0.0.0.0")

    logging.info(" [*] Listening on 0.0.0.0:" + str(options.options.port))
    print "*SYSOUT* User API Websocket is created at localhost:" + str(options.options.port) + "/api"

    # CALLING SETUP IF PRESENT
    if "setup" in vars(main):
        main.setup()

    ########################################################## SIGNAL HANDLER
    def sig_handler(sig, frame):
        #logging.warning('Caught signal: %s', sig)
        # CALLING STOP IF PRESENT
        if "stop" in vars(main):
            #logging.warning('Calling user defined stop function')
            main.stop()
        exit()
    ########################################################## INIT SIGNAL HANDLERS

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    ioloop = ioloop.IOLoop.instance()

    # Create a userControl object
    userControl = UserControl()
    ioloop.add_handler(sys.stdin.fileno(), userControl.userPlayer, ioloop.READ)

    ioloop.start()
