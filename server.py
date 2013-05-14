# -*- coding: utf-8 -*-
import os, sys

from tornado import web, ioloop, iostream, options, httpserver, autoreload, websocket
from sockjs.tornado import SockJSRouter, SockJSConnection

# IMPORT EDITOR CLASSES, this connects editor webapp with tornado server
from editor import Editor #, WeioEditorStopHandler, WeioEditorPlayHandler 

# IMPORT WEIOAPI BRIDGE CLASS, this connects user webapp with tornado server
from weioLib import WeioAPIbridge

# IMPORT BASIC CONFIGURATION FILE ALL PATHS ARE DEFINED INSIDE
from weioLib import weio_config



# This is user project index.html
class WeioIndexHandler(web.RequestHandler):
    
    def get(self):
        global confFile
        path = confFile['user_projects_path'] + confFile['last_opened_project'] + "index.html"
        self.render(path, error="")
        
        
# This is editor web app      
class WeioEditorWebHandler(web.RequestHandler):
    
    def get(self):
        global confFile
        path = confFile['editor_html_path']
        self.render(path, error="")
        
# This is preview web app      
class WeioPreviewWebHandler(web.RequestHandler):
    
    def get(self):
        global confFile
        path = confFile['preview_html_path']
        self.render(path, error="")


# pure websocket implementation
#class CloseConnection(websocket.WebSocketHandler):
class CloseConnection(SockJSConnection):

    def on_open(self, info):
        self.close()

    def on_message(self, msg):
        pass
        


if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # WEIO API BRIDGE
    WeioAPIBridgeRouter = SockJSRouter(WeioAPIbridge.WeioAPIBridgeHandler, '/api')

    # EDITOR ROUTES
    WeioEditorRouter = SockJSRouter(Editor.WeioEditorHandler, '/editor/baseFiles')    
  
    
    #CONFIGURATOR ROUTES


    
    #SETTINGS ROUTES
    
    
    #HELP ROUTE
    
    
    #GENERAL ROUTES
    CloseRouter = SockJSRouter(CloseConnection, '/close')

    
    
    # Take configuration from conf file and use it to define parameters
    global confFile
    confFile = weio_config.getConfiguration()

    # put absolut path in conf, needed for local testing on PC
    confFile['absolut_root_path'] = os.path.abspath(".")
    weio_config.saveConfiguration(confFile)
 
    
    app = web.Application(list(WeioEditorRouter.urls) +
                          list(CloseRouter.urls) +
                          list(WeioAPIBridgeRouter.urls) +
                          #list(WeioAPIBridgeRouter.urls) +
                          
                          # pure websocket implementation
                          #[(r"/editor/baseFiles", Editor.WeioEditorHandler)] +
                          #[(r"/close", CloseConnection)] +
                          [(r"/preview",WeioPreviewWebHandler)] +
                          [(r"/editor",WeioEditorWebHandler)] +
                          [(r"/", WeioIndexHandler),(r"/(.*)", web.StaticFileHandler,{"path": confFile["dependencies_path"]})], 
                          debug=True
                          )
                          # DEBUG WILL DECREASE SPEED!!! HOW TO AVOID THIS??? see Watchers section down here
    
    options.define("port", default=confFile['port'], type=int)
    
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port, address=confFile['ip'])
    

    logging.info(" [*] Listening on " + confFile['ip'] + ":" + str(confFile['port']))
    
    # WATCHERS works simply with debug=True
    
    # Other solution is to use autoreload, will be used later for production MAYBE
    # when some of these files change, tornado will reboot to serve all modifications, other files than python modules need to 
    # be specified manually
    #autoreload.watch('./editor/index.html')
    #autoreload.watch('./static/user_weio/index.html')
    
    # this will start wathcing process, note that all python modules that has been modified will be reloaded directly
    #autoreload.start(ioloop.IOLoop.instance())
    
    # STARTING SERVER
    ioloop.IOLoop.instance().start()