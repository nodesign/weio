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

import os, sys, platform, subprocess

import tornado
import tornado.options
import tornado.httpserver

from sockjs.tornado import SockJSRouter, SockJSConnection

import json, functools

# IMPORT EDITOR CLASSES, this connects editor webapp with tornado server
from handlers import editorHandler #, WeioEditorStopHandler, WeioEditorPlayHandler 

# IMPORT WEIOAPI BRIDGE CLASS, this connects user webapp with tornado server
from weioLib import weioAPIbridgeHandler

# IMPORT BASIC CONFIGURATION FILE ALL PATHS ARE DEFINED INSIDE
from weioLib import weio_config

#IMPORT DASHBOARD HANDLER
from handlers import dashboardHandler

#IMPORT LOGIN HANDLER
from handlers import loginHandlers

# IMPORT WIFI DETECTION AND CONFIGURATION
from handlers import wifiHandler

# IMPORT UPDATER
from handlers import updaterHandler

# IMPORT FIRST TIME HANDLER
from handlers import firstTimeHandler

# IMPORT WEIO BUTTONS OBJECT
from weioLib import weioWifiButtons


# This is user project index.html
class WeioIndexHandler(tornado.web.RequestHandler):
    
    def get(self):
        global firstTimeSwitch
        confFile = weio_config.getConfiguration()
        firstTimeSwitch = confFile['first_time_run']
        #print firstTimeSwitch
        
        if (firstTimeSwitch=="YES") :
            path = "www/firstTime.html"
        else :
            path = confFile['user_projects_path'] + confFile['last_opened_project'] + "index.html"
        
        self.render(path, error="")

        
# Editor web app route handler      
class WeioEditorWebHandler(loginHandlers.BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        global confFile
        global firstTimeSwitch
        confFile = weio_config.getConfiguration()
        firstTimeSwitch = confFile['first_time_run']
        
        if (firstTimeSwitch=="YES") :
            path = "www/firstTime.html"
        else :
            path = confFile['editor_html_path']
        
        self.render(path, error="")
        

# pure websocket implementation
class WeioCloseConnection(SockJSConnection):
    def on_open(self, info):
        self.close()

    def on_message(self, msg):
        pass

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
    global confFile
    global firstTimeSwitch
    global wifiButtons
    
    confFile = weio_config.getConfiguration()

    # put absolut path in conf, needed for local testing on PC
    confFile['absolut_root_path'] = os.path.abspath(".")
    weio_config.saveConfiguration(confFile)
    firstTimeSwitch = confFile['first_time_run']
    
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    
    # WEIO API BRIDGE
    WeioAPIBridgeRouter = SockJSRouter(weioAPIbridgeHandler.WeioAPIBridgeHandler, '/api')

    # EDITOR ROUTES
    WeioEditorRouter = SockJSRouter(editorHandler.WeioEditorHandler, '/editor/editorSocket')    
  
    # DASHBOARD ROUTE websocket
    WeioDashboardRouter = SockJSRouter(dashboardHandler.WeioDashBoardHandler, '/dashboard')
        
    # WIFI DETECTION ROUTE
    WeioWifiRouter = SockJSRouter(wifiHandler.WeioWifiHandler, '/wifi')
    
    # UPDATER ROUTE
    WeioUpdaterRouter = SockJSRouter(updaterHandler.WeioUpdaterHandler, '/updater')
    
    # FIRST TIME ROUTER
    WeioFirstTimeRouter = SockJSRouter(firstTimeHandler.WeioFirstTimeHandler, '/firstTime')
    
    #GENERAL ROUTES
    CloseRouter = SockJSRouter(WeioCloseConnection, '/close')
    
    
    

    secret = loginHandlers.generateCookieSecret()
    print secret
    settings = {
        "cookie_secret": secret,
        "login_url": "/login",
    }
    
    # when going in release always put this to false to avoid overheating of CPU, be ecological!
    debugMode = confFile['debug_mode']

    app = tornado.web.Application(list(WeioEditorRouter.urls) +
                            list(CloseRouter.urls) +
                            list(WeioAPIBridgeRouter.urls) +
                            list(WeioDashboardRouter.urls) +
                            list(WeioWifiRouter.urls) +
                            list(WeioUpdaterRouter.urls) +
                            list(WeioFirstTimeRouter.urls) +
                            #list(WeioHeaderRouter.urls) +
                            #list(WeioAPIBridgeRouter.urls) +
                          
                            # pure websocket implementation
                            #[(r"/editor/baseFiles", Editor.WeioEditorHandler)] +
                            #[(r"/close", WeioCloseConnection)] +
                            [(r"/editor", WeioEditorWebHandler)] +
                            [(r"/login", loginHandlers.WeioLoginHandler)] +
                            [(r"/", WeioIndexHandler),
                                (r"/(.*)", tornado.web.StaticFileHandler,
                                {"path": confFile["dependencies_path"]})], 
                            debug=debugMode, **settings
                          )
                          # DEBUG WILL DECREASE SPEED!!! HOW TO AVOID THIS??? see Watchers section down here
    
    tornado.options.define("port", default=confFile['port'], type=int)

    # If we are on the WEIO machine, we have to assure connection before doing anything
    if (platform.machine() == 'mips') :
        wifiHandler.wifi.checkConnection()
    
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port, address=confFile['ip'])
    

    logging.info(" [*] Listening on " + confFile['ip'] + ":" + str(confFile['port']))
    
    # WATCHERS works simply with debug=True
    
    # Other solution is to use autoreload, will be used later for production MAYBE
    # when some of these files change, tornado will reboot to serve all modifications,
    # other files than python modules need to be specified manually
    #tornado.autoreload.watch('./editor/index.html')
    #tornado.autoreload.watch('./static/user_weio/index.html')
    
    # this will start wathcing process, note that all python modules that has been modified will be reloaded directly
    #tornado.autoreload.start(tornado.ioloop.IOLoop.instance())
    
    wifiButtons = weioWifiButtons.WifiButtons()
    periodic = tornado.ioloop.PeriodicCallback(checkWifiButtons, 100)
    periodic.start()


    # STARTING SERVER
    tornado.ioloop.IOLoop.instance().start()
