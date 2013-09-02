from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

import json
import sys

#import thread
import threading

sys.path.append(r'./')

from user import *

from weioLib.weioUserApi import *
from main import *



class WeioHandler(SockJSConnection):
    """Opens editor route."""
    def on_open(self, data):
        """On open asks weio for last saved project. List of files are scaned and sent to editor.
        Only contents of weioMain.py is sent at first time"""
        print "Opened WEIO API socket"

    def on_message(self, data):
        """Parsing JSON data that is comming from browser into python object"""
        self.req = json.loads(data)
        self.serve()

    def serve(self) :
        for key in attach.events :
            if attach.events[key].event in self.req['request'] :
                attach.events[key].handler(self.req['data'])



if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    WeioRouter = SockJSRouter(WeioHandler, '/api')

    app = web.Application(WeioRouter.urls)
    app.listen(8082)

    logging.info(" [*] Listening on 0.0.0.0:8082/api")

    setup()

    for key in attach.procs :
        print key
        #thread.start_new_thread(attach.procs[key].procFnc, attach.procs[key].procArgs)
        t = threading.Thread(target=attach.procs[key].procFnc, args=attach.procs[key].procArgs)
        t.daemon = True
        t.start()

    ioloop.IOLoop.instance().start()


