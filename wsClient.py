#!/usr/bin/python -u
#
# WEIO Web Of Things Platform
# Copyright (C) 2013 Nodesign.net, Uros PETREVSKI, Drasko DRASKOVIC
# All rights reserved
#
#               ##      ## ######## ####  #######
#               ##  ##  ## ##        ##  ##     ##
#               ##  ##  ## ##        ##  ##     ##
#               ##  ##  ## ######    ##  ##     ##
#               ##  ##  ## ##        ##  ##     ##
#               ##  ##  ## ##        ##  ##     ##
#                ###  ###  ######## ####  #######
#
#                    Web Of Things Platform
#
# This file is part of WEIO and is published under BSD license.
# All rights not explicitly granted in the BSD license are reserved.
# See the included LICENSE file for more details.
#
###

import websocket
import time
import threading

import sys, json, signal

# WeIO stuff
from weioLib import weioControl

# weioCtrl
weioCtrl = weioControl.weioControl()

###
# WS cb handlers
###

###
# on_message
###
def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")

###
# on_open
###
def on_open(ws):
    def run(*args):
        for i in range(3):
            # send the message, then wait
            # so thread doesnt exit and socket
            # isnt closed
            ws.send("Hello %d" % i)
            time.sleep(1)

        time.sleep(1)
        print("Thread terminating...")

    #thread.start_new_thread(run, ())

    t = threading.Thread(target=run,
                        args=[])
    t.daemon = True
    t.start()

        

###
# Signal handler
###
def signalHandler(sig, frame):

    weioCtrl.stop()

    # Close WS connections
    ws.close()

    # Bail out
    sys.exit(0)


###
# CLIENT MAIN
###
if __name__ == '__main__':

    # Install signal handlers
    signal.signal(signal.SIGTERM, signalHandler)
    signal.signal(signal.SIGINT, signalHandler)
    
    # Start WeIO stuff
    weioCtrl.start()

    ###
    # WS stuff
    ###
    websocket.enableTrace(True)
    if len(sys.argv) < 2:
        host = "ws://echo.websocket.org/"
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    print "if anything goes wrong kill process with: kill -9 `ps aux | grep ws | grep python | awk '{print $2}'`"
    ws.run_forever()
