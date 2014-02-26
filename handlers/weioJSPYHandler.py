from weioLib.weioUserApi import *
from weioLib.weioIO import *
from tornado import websocket
import json

connections = []

class WeioHandler(websocket.WebSocketHandler):

    def open(self):
        global connections
        if self not in connections:
            connections.append(self)

        #print "*SYSOUT*Opened WEIO API socket"

        #shared.websocketSend = self.emit
        attach.event('_info', self.clientInfo)
        attach.event('_getBoardData', self.sendBoardData)
        #self.ip = data.ip

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
            attach.event('packetRequests', self.iteratePacketRequests)

        attach.event('getConnectedUsers', self.getConnectedUsers)
        attach.event('talkTo', self.talkTo)
        # collect client ip address and user machine info
        # print self.request to see all available info on user connection
        self.ip = self.request.remote_ip
        self.userAgent = self.request.headers["User-Agent"]

    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        self.serve(json.loads(data))

    def serve(self, data) :
        for key in attach.events :
            if attach.events[key].event in data['request'] :
                attach.events[key].handler(data['data'])

    def iteratePacketRequests(self, rq) :
        #print rq
        for uniqueRq in rq:
            request = uniqueRq['request']
            self.serve(uniqueRq)

    def on_close(self):
        global connections
        if self in connections:
            connections.remove(self)
            print "*SYSOUT* " + self.userAgent + " with IP address : " + self.ip + " disconnected from server!"
        #print "Websocket closed"

    def clientInfo(self,data) :
        #print "Client info called"
        print "*SYSOUT* " + self.userAgent + " with IP address : " + self.ip + " connected to server!"

    def sendBoardData(self, rq) :
        data = {}
        data["requested"] = '_getBoardData'

        #print "*SYSOUT* ", pins
        data["data"] = shared.declaredPins
        self.write_message(json.dumps(data))

    def emit(self, instruction, rq):
        data = {}
        data['serverPush'] = instruction
        data['data'] = rq
        self.write_message(json.dumps(data))

    def getConnectedUsers(self, rq):
        #print "USERS"
        allClients = {}
        allClients['serverPush'] = rq[0]
        data = []
        for client in shared.connectedClients :
            data.append(client.info)
        allClients['data'] = data
        self.write_message(json.dumps(allClients))

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
        self.write_message(json.dumps(bck))

    def callInputMode(self, data) :
        inputMode(data[0],data[1])

    def callAnalogRead(self, data) :
        #print "From browser ", data
        value = analogRead(data[0]) # this is pin number
        bck = {}
        bck["serverPush"] = data[1] # this is callback for JS
        bck["data"] = value
        bck["pin"] = data[0]
        self.write_message(json.dumps(bck))

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
        #self.write_message(json.dumps(data))
        pass
