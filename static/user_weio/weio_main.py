# Uros Petrevski, Nodesign.net, WEIO
from tornado import ioloop
from tornado import iostream
import socket
import time
import sys
sys.path.append(r'./weioLib');

from weio_gpio import *
from weio_globals import *


import pickle

def send_request():
   
    pin = 16
    
    print "hello"
    #pinMode(pin, OUTPUT)
    
    for a in range(10) :
        #digitalWrite(pin, HIGH)
        #time.sleep(0.5)
        #digitalWrite(pin, LOW)
        print(a)
        time.sleep(0.1)
    
    print "waiting"
    time.sleep(3)
    print "reading"
    pinMode(pin, INPUT)
    val = digitalRead(pin)
    print val
    print "finished"
    
        
    stream.close()
    ioloop.IOLoop.instance().stop()

class StdOutputToSocket():
    global out
    out = {}
    
    def write(self, msg):
        global out
        if "\n" in msg :
            out['stdout'] = out['stdout'] + msg
            stream.write(pickle.dumps(out))
            #stream.write(json.dumps(out))
        else :
            out['stdout'] = msg
         
class StdErrToSocket():
    global out
    out = {}
    
    def write(self, msg):
        global out
        if "\n" in msg :
            out['stdout'] = out['stdout'] + msg
            stream.write(pickle.dumps(out))
            #stream.write(json.dumps(out))
        else :
            out['stdout'] = msg
            
            
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
stream = iostream.IOStream(s)
stream.connect("uds_weio_main", send_request)

sys.stdout = StdOutputToSocket()
sys.stderr = StdErrToSocket()

ioloop.IOLoop.instance().start()
