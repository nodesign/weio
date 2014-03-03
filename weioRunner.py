#!/usr/bin/python -u
from tornado import web, ioloop, options, websocket

import sys,os,logging, platform, json, signal

import threading

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

    # Instantiate all handlers for user Tornado
    app = web.Application([
    (r'/api', WeioHandler),
    ('/', WeioIndexHandler),
    (r"/(.*)", web.StaticFileHandler, {"path": "www/"})
    ])
    app.listen(options.options.port, "0.0.0.0")

    logging.info(" [*] Listening on 0.0.0.0:" + str(options.options.port))
    print "*SYSOUT*Websocket is created at localhost:" + str(options.options.port) + "/api"

    # CALLING SETUP IF PRESENT
    if "setup" in vars(main):
        main.setup()

    # Launching threads
    for key in attach.procs :
        print key
        #thread.start_new_thread(attach.procs[key].procFnc, attach.procs[key].procArgs)
        t = threading.Thread(target=attach.procs[key].procFnc, args=attach.procs[key].procArgs)
        t.daemon = True
        t.start()

    ########################################################## SIGNAL HANDLER
    def sig_handler(sig, frame):
        logging.warning('Caught signal: %s', sig)
        # CALLING STOP IF PRESENT
        if "stop" in vars(main):
            logging.warning('Calling user defined stop function')
            main.stop()
        logging.warning('Shutdown WeIO coprocessor')
        stopWeio()
        logging.warning('Shutdown WeIO user server')
        ioloop.IOLoop.instance().stop()

    ########################################################## INIT SIGNAL HANDLERS

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    ioloop.IOLoop.instance().start()