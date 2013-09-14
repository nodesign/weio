from tornado import web, ioloop, options
from sockjs.tornado import SockJSRouter, SockJSConnection

import sys
import json

import threading

import uuid

from user import *

from weioLib.weioUserApi import *

projectModule = "userProjects." + sys.argv[1] + ".main"

#import module from argument list
print projectModule
main = __import__(projectModule, fromlist=[''])

class WeioHandler(SockJSConnection):
    
    
    
    def on_open(self, data):
        print "Opened WEIO API socket"
        shared.websocketOpened = True
        #shared.websocketSend = self.emit
        attach.event('_info', self.clientInfo)
        self.ip = data.ip
         
    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        self.req = json.loads(data)
        self.serve()
        

    def serve(self) :
        for key in attach.events :
            if attach.events[key].event in self.req['request'] :
                attach.events[key].handler(self.req['data'])

    def on_close(self, data):
        shared.websocketOpened = False
            # for client in shared.connectedClients :
            #if self.id in client :
            #   shared.connectedClients.remove(client)
            #    print "client uuid : " + self.id + " closed"


    def clientInfo(self,data) :
        print "New client connected with uuid " + data["uuid"]
        self.id = data["uuid"]
        data["ip"] = self.ip
        
        if (len(shared.connectedClients)==0):
            newClient = WeioClient(data, self.emit) 
            shared.connectedClients.append(newClient)
        else :
            
            present = False
            # don't register multiple times same client
            for client in shared.connectedClients :
                if (self.id in client.info["uuid"]):
                    present = True
                    break
            
            if present is False:
                newClient = WeioClient(data, self.emit) 
                shared.connectedClients.append(newClient)
        
        
    def emit(self, instruction, rq):
        data = {}
        data['serverPush'] = instruction
        data['data'] = rq
        self.send(json.dumps(data))   

if __name__ == '__main__':
    #import logging
    #logging.getLogger().setLevel(logging.DEBUG)
    
    shared.websocketOpened = False
    shared.connectedClients = []
    
    
    WeioRouter = SockJSRouter(WeioHandler, '/api')
    
    options.define("port", default=8082, type=int)
    
    app = web.Application(WeioRouter.urls)
    app.listen(options.options.port, "0.0.0.0")
    
    

    #logging.info(" [*] Listening on 0.0.0.0:8082/api")
    print "Websocket is created at localhost:" + str(options.options.port) + "/api"
    
    # CALLING SETUP IF PRESENT
    if "setup" in vars(main):
        main.setup()
    #else :
    #print "WARNNING : setup() function don't exist."

    for key in attach.procs :
        print key
        #thread.start_new_thread(attach.procs[key].procFnc, attach.procs[key].procArgs)
        t = threading.Thread(target=attach.procs[key].procFnc, args=attach.procs[key].procArgs)
        t.daemon = True
        t.start()

    ioloop.IOLoop.instance().start()