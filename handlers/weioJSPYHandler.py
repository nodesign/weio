from weioLib.weioIO import *
import json

from sockjs.tornado import SockJSConnection

from weioLib.weioParser import weioSpells

from weioLib import weioRunnerGlobals

class WeioHandler(SockJSConnection):
    def __init__(self, *args, **kwargs):
        SockJSConnection.__init__(self, *args, **kwargs)
        self.connections = weioRunnerGlobals.WEIO_CONNECTIONS

    def on_open(self, data):
        # Add client to the clients list
        #self.connections.add(self)

        # collect client ip address and user machine info
        # print self.request to see all available info on user connection
        self.userAgent = None
        self.ip = data.ip
        
        print "*SYSOUT* Client with IP address : " + self.ip + " connected to server!"
        
        # list all members of object
        #members = [attr for attr in dir(data) if not callable(attr) and not attr.startswith("__")]
        
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
        command = data["request"]
        #print data
        # treat requests using dictionaries
        # talks to hardware directly
        if command in weioSpells:
            result = weioSpells[command](data["data"])
            if not(result is None):
                #print data
                if not self.connection_closed:
                    if ("callback" in data):
                        result["serverPush"] = data["callback"] # this is specific callback for JS (name of function to call)
                    else:
                        result["serverPush"] = command # this is callback for JS, traceback of called command
                    try:
                        self.send(json.dumps(result))
                    except:
                        self.connection_closed = True
        elif (command == "weioStoreUID"):
            # Client is announcing iit's UID - store it's connection
            uid = data["data"]
            self.connections[uid] = self

            # Update shared UIDs array to be visible in all processes
            weioRunnerGlobals.WEIO_SHARED.addClient(uid)



    def on_close(self):
        self.connection_closed = True
        print "*SYSOUT* Client with IP address : " + self.ip + " disconnected from server!"
        # Remove client from the clients list and broadcast leave message
        self.connections.remove(self)

