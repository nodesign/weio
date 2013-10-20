from tornado import web, ioloop, options
from sockjs.tornado import SockJSRouter, SockJSConnection

import sys
import json

import threading

from weioLib.weioUserApi import *
from weioLib.weioIO import *
import platform

# add SD card path
sys.path.append('/sd')

projectModule = "userProjects." + sys.argv[1] + ".main"

#import module from argument list
#print projectModule

# WAY TO IMPORT FROM SD CARD
#import imp
#main = imp.load_source(projectModule, '/sd/userProjects/'+sys.argv[1]+'/main.py')

# WAY TO IMPORT FROM LOCAL
main = __import__(projectModule, fromlist=[''])

class WeioHandler(SockJSConnection):
    
    connections = []
    
    def on_open(self, data):
        #print "*SYSOUT*Opened WEIO API socket"
        shared.websocketOpened = True
        #shared.websocketSend = self.emit
        attach.event('_info', self.clientInfo)
        attach.event('_getBoardData', self.sendBoardData)
        self.ip = data.ip
        self.connections.append(self)
        
        if (platform.machine()=="mips"):
            # WeIO API bindings from websocket to lower levels
            attach.event('digitalWrite', self.callDigitalWrite)
            attach.event('digitalRead', self.callDigitalRead)
            attach.event('inputMode', self.callInputMode)
            attach.event('analogRead', self.callAnalogRead)
            attach.event('pwmWrite', self.callPwmWrite)
            attach.event('setPwmPeriod', self.callSetPwmPeriod)
            attach.event('setPwmLimit', self.callSetPwmLimit)
            attach.event('setPwmPeriod0', self.callSetPwmPeriod0)
            attach.event('setPwmPeriod1', self.callSetPwmPeriod1)
            attach.event('setPwmLimit0', self.callSetPwmLimit0)
            attach.event('setPwmLimit1', self.callSetPwmLimit1)
            attach.event('attachInterrupt', self.callAttachInterrupt)
            attach.event('detachInterrupt', self.callDetachInterrupt)
    
        attach.event('getConnectedUsers', self.getConnectedUsers)
        attach.event('talkTo', self.talkTo)
    
    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        #self.req = json.loads(data)
        self.serve(json.loads(data))
        

    def serve(self, data) :
        #print data
        for key in attach.events :
            if attach.events[key].event in data['request'] :
                attach.events[key].handler(data['data'])

    def on_close(self, data):
        shared.websocketOpened = False
            # for client in shared.connectedClients :
            #if self.id in client :
            #   shared.connectedClients.remove(client)
            #    print "client uuid : " + self.id + " closed"


    def clientInfo(self,data) :
        
        self.id = data["uuid"]
        data["ip"] = self.ip
        
        if (len(shared.connectedClients)==0):
            print "*SYSOUT* "+ data["appVersion"] + " connected with uuid " + data["uuid"] + " from " + data["ip"]
            newClient = WeioClient(data, self.connections[-1]) 
            shared.connectedClients.append(newClient)
        else :
            
            present = False
            # don't register multiple times same client
            for client in shared.connectedClients :
                if (self.id in client.info["uuid"]):
                    present = True
                    break
            
            if present is False:
                print "*SYSOUT* "+ data["appVersion"] + " connected with uuid " + data["uuid"] + " from " + data["ip"]
                newClient = WeioClient(data, self.connections[-1]) 
                shared.connectedClients.append(newClient)

    def sendBoardData(self, rq) :
        data = {}
        data["requested"] = '_getBoardData'
        
        #print "*SYSOUT* ", pins
        data["data"] = shared.declaredPins 
        self.send(json.dumps(data))
        
        
    def emit(self, instruction, rq):
        data = {}
        data['serverPush'] = instruction
        data['data'] = rq
        self.send(json.dumps(data))

    def getConnectedUsers(self, rq):
        #print "USERS"
        allClients = {}
        allClients['serverPush'] = rq[0]
        data = []
        for client in shared.connectedClients :
            data.append(client.info)
        allClients['data'] = data
        self.send(json.dumps(allClients))
    
    def talkTo(self, rq) :
        print rq
        data = {}
        data['data'] = rq[1]
        data['from'] = self.id
        for client in shared.connectedClients :
            #print client.info
            mm = client.info
            #print mm['uuid']
            if (mm['uuid'] == rq[0]):
                wsocket = client.connection
                wsocket.emit("inbox", data)
                break
                


##########################################################################################################################################
    # WeIO API bindings from websocket to lower levels
    def callDigitalWrite(self, data) :
        #print "FROM JS ", data
        digitalWrite(data[0], data[1])

    def callDigitalRead(self, data) :
        value = digitalRead(data[0])
        bck = {}
        bck["serverPush"] = data[1] # this is callback for JS
        bck["data"] = value 
        bck["pin"] = data[0]
        self.send(json.dumps(bck))

    def callInputMode(self, data) :
        inputMode(data[0],data[1])

    def callAnalogRead(self, data) :
        #print "From browser ", data
        value = analogRead(data[0]) # this is pin number
        bck = {}
        bck["serverPush"] = data[1] # this is callback for JS
        bck["data"] = value 
        bck["pin"] = data[0]
        self.send(json.dumps(bck))

    def callPwmWrite(self, data) :
        pwmWrite(data[0], data[1])

    def callSetPwmPeriod(self, data) :
        pwmPeriod(data[0])  

    def callSetPwmPeriod0(self, data) :
        pwmPeriod0(data[0])

    def callSetPwmPeriod1(self, data) :
        pwmPeriod1(data[0])

    def callSetPwmLimit(self, data) :
        pwmLimit(data[0])

    def callSetPwmLimit0(self, data) :
        pwmLimit0(data[0])

    def callSetPwmLimit1(self, data) :
        pwmLimit1(data[0])

    def callAttachInterrupt(self, data):
        attachInterrupt(data[0], data[1])

    def callDetachInterrupt(self, data) :
        detachInterrupt(data[0])

    def genericInterrupt(self, data):
        #type = data["type"]
        #data = {}
        #data["requested"] = 'analogRead'
        #data["data"] = value 
        #self.send(json.dumps(data))
        pass

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
    print "*SYSOUT*Websocket is created at localhost:" + str(options.options.port) + "/api"
    
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

