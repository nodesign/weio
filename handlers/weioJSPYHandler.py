from weioLib.weioIO import *
import json

from sockjs.tornado import SockJSConnection

from weioLib.weioParser import weioSpells
from weioLib.weioParser import weioUserSpells
from weioLib import weioRunnerGlobals

class WeioHandler(SockJSConnection):
    def __init__(self, *args, **kwargs):
        SockJSConnection.__init__(self, *args, **kwargs)
        self.connections = weioRunnerGlobals.weioConnections

    def on_open(self, request):
        # Add client to the clients list
        self.connections.add(self)

        # collect client ip address and user machine info
        # print self.request to see all available info on user connection
        self.userAgent = None
        self.ip = request.ip

        #print "*SYSOUT* Client with IP address : " + self.ip + " connected to server!"

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
        """Parsing JSON data that is comming from browser into python object"""
        self.serve(json.loads(data))

    def serve(self, data) :
        print "=== SERVE ==="
        command = data["request"]
        #print data

        # treat requests using dictionaries
        # talks to hardware directly
        result = None
        if command in weioSpells or command in weioUserSpells:
            if command in weioSpells:
                result = weioSpells[command](data["data"])
            elif command in weioUserSpells:
                result = weioUserSpells[command](data["data"])
            else:
                result = None

            if not(result is None):
                if not self.connection_closed:
                    if ("callback" in data):
                        result["serverPush"] = data["callback"] # this is specific callback for JS (name of function to call)
                    else:
                        result["serverPush"] = command # this is callback for JS, traceback of called command
                    try:
                        self.send(json.dumps(result))
                    except:
                        self.connection_closed = True

    def on_close(self):
        self.connection_closed = True
        print "*SYSOUT* Client with IP address : " + self.ip + " disconnected from server!"
        # Remove client from the clients list and broadcast leave message
        self.connections.remove(self)

