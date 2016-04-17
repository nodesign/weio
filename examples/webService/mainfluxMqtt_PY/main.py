from weioLib.weio import *
import time

import paho.mqtt.client as mqtt

def setup():
    attach.process(myProcess)

def myProcess():
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
    
    def on_publish(client, userdata, mid):
        print("mid: "+str(mid))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    client.connect("mainflux.io", 1883, 60)

    # Start looping
    client.loop_start()
    
    while True:
        temperature = getTemperature()
        print "TEMP: ", temperature
        (rc, mid) = client.publish("/1234/DevID1/attributes/temperature", str(temperature), qos=1)
        time.sleep(1)