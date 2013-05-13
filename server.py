# -*- coding: utf-8 -*-
import os, sys
sys.path.append(r'./');
sys.path.append(r'./static');
sys.path.append(r'./editor');
sys.path.append(r'./weioLib');

from tornado import web, ioloop, iostream, options, httpserver, autoreload, websocket
from sockjs.tornado import SockJSRouter, SockJSConnection

# IMPORT EDITOR CLASSES
from editor import Editor #, WeioEditorStopHandler, WeioEditorPlayHandler 

# IMPORT WEIOAPI BRIDGE CLASS
from weioLib import WeioAPIbridge

class WeioIndexHandler(web.RequestHandler):
    def get(self):
        self.render('static/user_weio/index.html', error="")
        
class WeioEditorWebHandler(web.RequestHandler):
    def get(self):
        self.render('editor/index.html', error="")

class WeioPreviewWebHandler(web.RequestHandler):
    def get(self):
        self.render('static/preview.html', error="")

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
    #WeioEditorPlayRouter = SockJSRouter(WeioEditorPlayHandler, '/editor/play')
    #WeioEditorStopRouter = SockJSRouter(WeioEditorStopHandler, '/editor/stop')
    
    #CONFIGURATOR ROUTES


    
    #SETTINGS ROUTES
    
    
    #HELP ROUTE
    
    
    #GENERAL ROUTES
    CloseRouter = SockJSRouter(CloseConnection, '/close')

    
    

    app = web.Application(list(WeioEditorRouter.urls) +
                          list(CloseRouter.urls) +
                          list(WeioAPIBridgeRouter.urls) +
                          #list(WeioAPIBridgeRouter.urls) +
                          
                          # pure websocket implementation
                          #[(r"/editor/baseFiles", Editor.WeioEditorHandler)] +
                          #[(r"/close", CloseConnection)] +
                          [(r"/preview",WeioPreviewWebHandler)] +
                          [(r"/editor",WeioEditorWebHandler)] +
                          [(r"/", WeioIndexHandler),(r"/(.*)", web.StaticFileHandler,{"path": "./static"})], 
                          debug=True
                          )
                          # DEBUG WILL DECREASE SPEED!!! HOW TO AVOID THIS???
        

                          # app = web.Application(list(WeioEditorRouter.urls) +
                          #                       list(CloseRouter.urls) +
                          #                       #list(WeioAPIBridgeRouter.urls) +
                          #                       [(r"/editor",WeioEditorWebHandler)] +
                          #                       [(r"/", WeioIndexHandler),(r"/(.*)", StaticFileHandlerNoCache,
                          #                                                 {"path": "./static"})
                          #                       ]
                          #                       )
                          # 

    options.define("port", default=8081, type=int)
    
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port, address="0.0.0.0")
    
    #app.listen(8081)
    logging.info(" [*] Listening on 0.0.0.0:8081")
    
    # WATCHERS ONLY FOR DEBUG MODE, no need in debug=True
    
    # when some of these files change, tornado will reboot to serve all modifications, other files than python modules need to 
    # be specified manually
    #autoreload.watch('./editor/index.html')
    #autoreload.watch('./static/user_weio/index.html')
    
    # this will start wathcing process, note that all python modules that has been modified will be reloaded directly
    #autoreload.start(ioloop.IOLoop.instance())
    
    # STARTING SERVER
    ioloop.IOLoop.instance().start()