from weioLib.weio import *
import weioLib.weioParser as wp
import json

import time

import paho.mqtt.client as mqtt

def setup():
    attach.process(electrolink)

def electrolink():
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        
        data = json.loads(msg.payload)
        print data
        
        # Call the HW function on the board
        r = wp.weioSpells[data["method"]](data["params"])
        
        # send back result
        rsp = {}
        rsp["jsonrpc"] = "2.0"
        
        if (r is not None):
            rsp["result"] = r["data"]
        else:
            rsp["result"] = "none"
        
        rsp["id"] = data["id"]
        
        client.publish('/electrolink/rsp', json.dumps(rsp))
    
    def on_publish(client, userdata, mid):
        print("mid: "+str(mid))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    client.connect("localhost", 1883, 60)

    wp.weioSpells["digitalWrite"]([18, 1])

    # Start looping
    client.loop_start()
    
    client.subscribe('/electrolink/req')
    
    while True:
        print "tick"
        time.sleep(3)

