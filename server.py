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

import os, sys, platform

from tornado import web, ioloop, iostream, options, httpserver, autoreload, websocket
from sockjs.tornado import SockJSRouter, SockJSConnection

import json, functools

# IMPORT EDITOR CLASSES, this connects editor webapp with tornado server
from editor import editorHandler #, WeioEditorStopHandler, WeioEditorPlayHandler 

# IMPORT WEIOAPI BRIDGE CLASS, this connects user webapp with tornado server
from weioLib import weioAPIbridgeHandler

# IMPORT BASIC CONFIGURATION FILE ALL PATHS ARE DEFINED INSIDE
from weioLib import weio_config

from weioWifi import weioWifiHandler

# This is user project index.html
class WeioIndexHandler(web.RequestHandler):
    def get(self):
        global confFile
        path = confFile['user_projects_path'] + confFile['last_opened_project'] + "index.html"
        self.render(path, error="")
        #self.redirect(path)
        
        
# Editor web app route handler      
class WeioEditorWebHandler(web.RequestHandler):
    def get(self):
        global confFile
        path = confFile['editor_html_path']
        self.render(path, error="")
        

# Preview web app route handler     
class WeioPreviewWebHandler(web.RequestHandler):
    def get(self):
        global confFile
        path = confFile['preview_html_path']
        self.render(path, error="")


# pure websocket implementation
class WeioCloseConnection(SockJSConnection):
    def on_open(self, info):
        self.close()

    def on_message(self, msg):
        pass
        

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # WEIO API BRIDGE
    WeioAPIBridgeRouter = SockJSRouter(weioAPIbridgeHandler.WeioAPIBridgeHandler, '/api')

    # EDITOR ROUTES
    WeioEditorRouter = SockJSRouter(editorHandler.WeioEditorHandler, '/editor/baseFiles')    
  
    # HEADER WEB SOCKET
    #WeioHeaderRouter = SockJSRouter(Header.WeioHeaderHandler, '/header')

    # WIFI DETECTION ROUTES
    WeioWifiRouter = SockJSRouter(weioWifiHandler.WeioWifiHandler, '/wifi')
    
    
    #CONFIGURATOR ROUTES


    #SETTINGS ROUTES
    
    
    #HELP ROUTE
    
    
    #GENERAL ROUTES
    CloseRouter = SockJSRouter(WeioCloseConnection, '/close')

    
    # Take configuration from conf file and use it to define parameters
    global confFile
    confFile = weio_config.getConfiguration()

    # put absolut path in conf, needed for local testing on PC
    confFile['absolut_root_path'] = os.path.abspath(".")
    weio_config.saveConfiguration(confFile)
 
    
    app = web.Application(list(WeioEditorRouter.urls) +
                            list(CloseRouter.urls) +
                            list(WeioAPIBridgeRouter.urls) +
                            list(WeioWifiRouter.urls) +
                            #list(WeioHeaderRouter.urls) +
                            #list(WeioAPIBridgeRouter.urls) +
                          
                            # pure websocket implementation
                            #[(r"/editor/baseFiles", Editor.WeioEditorHandler)] +
                            #[(r"/close", WeioCloseConnection)] +
                            [(r"/preview",WeioPreviewWebHandler)] +
                            [(r"/editor",WeioEditorWebHandler)] +
                            [(r"/", WeioIndexHandler),
                                (r"/(.*)", web.StaticFileHandler,
                                {"path": confFile["dependencies_path"]})], 
                            debug=True
                          )
                          # DEBUG WILL DECREASE SPEED!!! HOW TO AVOID THIS??? see Watchers section down here
    
    options.define("port", default=confFile['port'], type=int)

    # If we are on the WEIO machine, we have to assure connection before doing anything
    if (platform.machine() is 'mips') :
        weioWifiHandler.wifi.checkConnection()
    
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port, address=confFile['ip'])
    

    logging.info(" [*] Listening on " + confFile['ip'] + ":" + str(confFile['port']))
    
    # WATCHERS works simply with debug=True
    
    # Other solution is to use autoreload, will be used later for production MAYBE
    # when some of these files change, tornado will reboot to serve all modifications,
    # other files than python modules need to be specified manually
    #autoreload.watch('./editor/index.html')
    #autoreload.watch('./static/user_weio/index.html')
    
    # this will start wathcing process, note that all python modules that has been modified will be reloaded directly
    #autoreload.start(ioloop.IOLoop.instance())
    
    # STARTING SERVER
    ioloop.IOLoop.instance().start()
