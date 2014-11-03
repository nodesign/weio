from weioLib.weioIO import *
import json

from sockjs.tornado import SockJSConnection

from weioLib.weioParser import weioSpells
from weioLib.weioParser import weioUserSpells
from weioLib import weioRunnerGlobals

import uuid
import os


class WeioHandler(SockJSConnection):
    def __init__(self, *args, **kwargs):
        SockJSConnection.__init__(self, *args, **kwargs)
        #self.connections = weioRunnerGlobals.weioConnections

    def on_open(self, request):
        # Add the connection to the connections dictionary
        connUuid = uuid.uuid4()
        weioRunnerGlobals.weioConnections[connUuid] = self

        # collect client ip address and user machine info
        # print self.request to see all available info on user connection
        self.userAgent = None
        self.ip = request.ip

        print "*SYSOUT* Client with IP address: " + self.ip + " connected to server"

        #print "============="
        #print self.session.conn_info.get_header('x-client-ip')
        #print self.session.conn_info.ip
        #print self.session.conn_info.path
        #print self.session.conn_info.arguments

        #print "++++++++++++++"
        #print request.headers['User-Agent']

        # list all members of object
        #members = [attr for attr in dir(request) if not callable(attr) and not attr.startswith("__")]

        #if ("User-Agent" in self.request.headers):
        #    self.userAgent = self.request.headers["User-Agent"]
        #    print "*SYSOUT* " + self.userAgent + " with IP address : " + self.ip + " connected to server!"
        #else :
        #    print "*SYSOUT* Client with IP address : " + self.ip + " connected to server!"
        #print self.request.headers
        self.connection_closed = False

    def emit(self, instruction, rq):
        data = {}
        data['serverPush'] = instruction
        data['data'] = rq
        self.send(json.dumps(data))

    def on_message(self, data):
        if (weioRunnerGlobals.running.value == True):
            """Parsing JSON data that is comming from browser into python object"""
            self.serve(json.loads(data))
        else:
            weioRunnerGlobals.weioConnections.clear()

    def serve(self, data) :
        for connUuid, conn in weioRunnerGlobals.weioConnections.iteritems():
            if (conn == self):
                # Create userAgentMessage and send it to the launcher process
                msg = weioRunnerGlobals.userAgentMessage()

                msg.connUuid = connUuid

                if (type(data) is dict):
                    #print "keys : %s" %  data.keys()
                    for key in data:
                        if key == "request":
                            msg.req = data["request"]
                        elif key == "data":
                            msg.data = data["data"]
                        elif key == "callback":
                            msg.callbackJS = data["callback"]

            # Send message to launcher process
            weioRunnerGlobals.QOUT.put(msg)


    def on_close(self):
        self.connection_closed = True
        print "*SYSOUT* Client with IP address: " + self.ip + " disconnected from server"
        # Remove client from the clients list and broadcast leave message
        #self.connections.remove(self)
        for connUuid, conn in weioRunnerGlobals.weioConnections.iteritems():
            if (conn == self):
                weioRunnerGlobals.weioConnections.pop(connUuid)


###
# This is used for remote apps - Tornado User opens __client__ socket
# and puths everything that comes from this socket to WeioHandlerRemote() 
###
class WeioHandlerRemote():
    def __init__(self):
        self.remoteConn = None
        self.connUuid = None

    def setRemoteConn(self, rc):
        self.remoteConn = rc
        # Add the connection to the connections dictionary
        self.connUuid = uuid.uuid4()
        weioRunnerGlobals.weioConnections[self.connUuid] = self.remoteConn


    def on_message(self, data):
        if (self.remoteConn != None):
            """Parsing JSON data that is comming from browser into python object"""
            self.serve(json.loads(data))

    def serve(self, data) :
        # Create userAgentMessage and send it to the launcher process
        msg = weioRunnerGlobals.userAgentMessage()
        #print "DATA: ", data

        if (type(data) is dict):
            #print "keys : %s" %  data.keys()
            for key in data:
                if key == "request":
                    msg.req = data["request"]
                elif key == "data":
                    msg.data = data["data"]
                elif key == "callback":
                    msg.callbackJS = data["callback"]

        # Send message to launcher process
        weioRunnerGlobals.QOUT.put(msg)

    def on_close(self):
        self.remoteConn = None

        # Remove client from the clients list and broadcast leave message
        weioRunnerGlobals.weioConnections.pop(self.connUuid)
        self.connUuid = None

