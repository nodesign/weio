from weioLib.weioIO import *
from weioLib.weioUserApi import shared
from tornado import websocket
import json

from weioLib.weioParser import weioSpells

connections = []

class WeioHandler(websocket.WebSocketHandler):

    def open(self):
        global connections
        if self not in connections:
            connections.append(self)

        # collect client ip address and user machine info
        # print self.request to see all available info on user connection
        self.ip = self.request.remote_ip
        self.userAgent = self.request.headers["User-Agent"]
        print "*SYSOUT* " + self.userAgent + " with IP address : " + self.ip + " connected to server!"
        self.connection_closed = False

    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        self.serve(json.loads(data))

    def serve(self, data) :
        command = data["request"]
        # print data
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
                        self.write_message(json.dumps(result))
                    except:
                        self.connection_closed = True

    def on_close(self):
        self.connection_closed = True
        global connections
        if self in connections:
            connections.remove(self)
            print "*SYSOUT* " + self.userAgent + " with IP address : " + self.ip + " disconnected from server!"
        #print "Websocket closed"
