#!/usr/bin/python

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

import os, sys, platform, signal

import tornado
import tornado.options
import tornado.httpserver

from sockjs.tornado import SockJSRouter, SockJSConnection

import json, functools
import subprocess

# IMPORT EDITOR CLASSES, this connects editor webapp with tornado server
from handlers import editorHandler #, WeioEditorStopHandler, WeioEditorPlayHandler

# IMPORT WEIOAPI BRIDGE CLASS, this connects user webapp with tornado server
#from weioLib import weioAPIbridgeHandler

# Import basic configuration file all paths are defined inside
from weioLib import weioConfig

#IMPORT DASHBOARD HANDLER
from handlers import dashboardHandler

# Import user settings handler
from handlers import userSettingsHandler

#Import signin and login handler
from handlers import loginHandler
from handlers import signinHandler

# IMPORT WIFI DETECTION AND CONFIGURATION
from handlers import wifiHandler

# IMPORT UPDATER
from handlers import updaterHandler

# IMPORT STATS HANDLER
from handlers import statsHandler


# IMPORT WEIO BUTTONS OBJECT
from weioLib import weioWifiButtons

# IMPORT WEIO FILE SUPPORT
from weioLib import weioFiles

# Import Wifi class for initializing the WIFI object
from weioWifi import weioWifi

# Import WeioPlayer class
from weioPlayer import WeioPlayer

# Import global variables for main Tornado
from weioLib import weioIdeGlobals

# Editor web app route handler
class WeioEditorWebHandler(loginHandler.BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        confFile = weioConfig.getConfiguration()
        firstTimeSwitch = confFile['first_time_run']

        if (firstTimeSwitch=="YES") :
            self.redirect("/signin")
            # Create symlinks to external projects
            weioFiles.symlinkExternalProjects()
            return

        if (confFile["login_required"] == "YES"):
            if not self.current_user:
                self.redirect("/login")
                return

        path = confFile['editor_html_path']
        self.render(path, error="")

# Periodic callback that checks button state for AP and STA
# if AP+STA over 3 seconds than reset
def checkWifiButtons() :
    global wifiButtons
    state = wifiButtons.checkButtons()
    if (state is not None) :
        print state
        if (state == "reset"):
            exit() # only tornado reset
        elif (state == "ap"):
            pass
            # go to ap
        elif (state == "sta"):
            pass
            # go to sta

if __name__ == '__main__':
    # Take configuration from conf file and use it to define parameters
    global wifiButtons
    global wifiPeriodicCheck

    confFile = weioConfig.getConfiguration()
    
    # Create symlinks to external projects
    weioFiles.symlinkExternalProjects()

    # put absolut path in conf, needed for local testing on PC
    confFile['absolut_root_path'] = os.path.abspath(".")
    weioConfig.saveConfiguration(confFile)
    firstTimeSwitch = confFile['first_time_run']


    import logging
    logging.getLogger().setLevel(logging.DEBUG)


    ###
    # Routers
    ###
    # EDITOR ROUTES
    WeioEditorRouter = SockJSRouter(editorHandler.WeioEditorHandler, '/editorSocket')

    # DASHBOARD ROUTE websocket
    WeioDashboardRouter = SockJSRouter(dashboardHandler.WeioDashBoardHandler, '/dashboard')

    # USER SETTINGS ROUTE websocket
    WeioSettingsHandler = SockJSRouter(userSettingsHandler.WeioSettingsHandler, '/settings')    
    # WIFI DETECTION ROUTE
    WeioWifiRouter = SockJSRouter(wifiHandler.WeioWifiHandler, '/wifi')

    # UPDATER ROUTE
    WeioUpdaterRouter = SockJSRouter(updaterHandler.WeioUpdaterHandler, '/updater')

    # STATS ROUTER
    WeioStatsRouter = SockJSRouter(statsHandler.WeioStatsHandler, '/stats')


    secret = loginHandler.generateCookieSecret()
    print secret
    settings = {
        "cookie_secret": secret,
        "login_url": "/login",
    }

    # when going in release always put this to false to avoid overheating of CPU, be ecological!
    debugMode = confFile['debug_mode']
    if ("False" in debugMode):
        debugMode = False
    else :
        debugMode = True

    app = tornado.web.Application(list(WeioEditorRouter.urls) +
                            list(WeioDashboardRouter.urls) +
                            list(WeioSettingsHandler.urls) +
                            list(WeioWifiRouter.urls) +
                            list(WeioUpdaterRouter.urls) +
                            list(WeioStatsRouter.urls)+

                            # pure websocket implementation
                            #[(r"/editor/baseFiles", Editor.WeioEditorHandler)] +
                            #[(r"/close", WeioCloseConnection)] +
                            [(r"/", WeioEditorWebHandler),
                                (r"/signin", signinHandler.WeioSigninHandler),
                                (r"/login", loginHandler.WeioLoginHandler),
                           (r"/(.*)", tornado.web.StaticFileHandler,{"path": "www"})],
                            debug=debugMode, **settings
                          )
                          # DEBUG WILL DECREASE SPEED!!! HOW TO AVOID THIS??? see Watchers section down here

    tornado.options.define("port", default=confFile['port'], type=int)

    # If we are on the WEIO machine, we have to assure connection before doing anything
    #wifiHandler.wifi.checkConnection()
    if (confFile["https"] == "YES"):
        # Generate SSL key
        subprocess.check_call(confFile['absolut_root_path'] + "/scripts/generate_ssl_key.sh", shell=True)
        
        # Start the HTTPS server with this key
        http_server = tornado.httpserver.HTTPServer(app,
            ssl_options={
                "certfile": os.path.join(confFile['absolut_root_path'], "weioSSL.crt"),
                "keyfile": os.path.join(confFile['absolut_root_path'], "weioSSL.key"),
            })
    else:
        # Plain ol' HTTP
        http_server = tornado.httpserver.HTTPServer(app)

    http_server.listen(tornado.options.options.port, address=confFile['ip'])


    logging.info(" [*] Listening on " + confFile['ip'] + ":" + str(confFile['port']))

    # WATCHERS works simply with debug=True

    # Other solution is to use autoreload, will be used later for production MAYBE
    # when some of these files change, tornado will reboot to serve all modifications,
    # other files than python modules need to be specified manually
    #tornado.autoreload.watch('./editor/index.html')
    #tornado.autoreload.watch('./static/user_weio/index.html')

    # This will start wathcing process, note that all python modules that has been modified will be reloaded directly
    # tornado.autoreload.start(tornado.ioloop.IOLoop.instance())

    wifiButtons = weioWifiButtons.WifiButtons()

    # Activate buttons only when hardware is ready
    #periodic = tornado.ioloop.PeriodicCallback(checkWifiButtons, 100)
    #periodic.start()

    # Initialize the main Tornado global objects before running all the machiery
    weioIdeGlobals.WIFI = weioWifi.WeioWifi("wlan0")

    # Check WiFi connection every second
    if (platform.machine() == 'mips'):
    	weioIdeGlobals.WIFI.periodicCheck = tornado.ioloop.PeriodicCallback(weioIdeGlobals.WIFI.checkConnection, 5000)
        weioIdeGlobals.WIFI.periodicCheck.start()

    weioIdeGlobals.PLAYER = WeioPlayer()

    # Start User Tornado
    weioIdeGlobals.PLAYER.startUserTornado()

    # Starting the last user program
    if (confFile['play_composition_on_server_boot'] == "YES"):
        weioIdeGlobals.PLAYER.play()

    ########################################################## SIGNAL HANDLER
    def sig_handler(sig, frame):
        logging.warning('Caught signal: %s', sig)
        print "Exiting Tornado"
        tornado.ioloop.IOLoop.instance().stop()

    ########################################################## INIT SIGNAL HANDLERS

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)


    # STARTING SERVER
    tornado.ioloop.IOLoop.instance().start()
