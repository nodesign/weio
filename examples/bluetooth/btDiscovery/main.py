##########################################
#                                        #
#   Discovering devices with Bluetooth   #
#                                        #
##########################################
# to run this example you need Bluetooth usb dongle

from weioLib.weio import *
import bluetooth
from subprocess import Popen, PIPE

def setup():

    # Reset BT and make sure that BT is UP
    execute("hciconfig hci0 down")
    execute("hciconfig hci0 up")
    
    result = execute("hciconfig")
    print result
    if ("UP RUNNING" in result):
       attach.process(myProcess)


def myProcess():
    print("performing inquiry...")
    nearby_devices = bluetooth.discover_devices(duration=2, lookup_names=True)
    print("found %d devices" % len(nearby_devices))
    for addr, name in nearby_devices:
        print("  %s - %s" % (addr, name))

 
def execute(cmd): # cmd is string like in command line
    proc = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
    s = proc.communicate()
    # return console output
    return s[0]
    

# Will be called on stop button
def stop():
    # Stopping BT
    execute("hciconfig hci0 down")