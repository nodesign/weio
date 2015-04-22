##########################################
#                                        #
#   Turning your WeIO into iBeacon       #
#                                        #
##########################################
# to run this example you need Bluetooth usb dongle
# this one is proven to work :
# http://www.amazon.com/IOGEAR-Bluetooth-Micro-Adapter-GBU521/dp/B007GFX0PY

from weioLib.weio import *
import bluetooth
from subprocess import Popen, PIPE

# This is your unique ID address
ID = "E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61"

def setup():

    # Reset BT and make sure that BT is UP
    execute("hciconfig hci0 down")
    execute("hciconfig hci0 up")
    
    print execute("hciconfig hci0 leadv 3")
    print execute("hciconfig hci0 noscan")
    
    result = execute("hciconfig")
    print result
    if ("UP RUNNING" in result):
        print execute("hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 "+ID+" 00 00 00 00 C8 00")
    
    
def execute(cmd): # cmd is string like in command line
    proc = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
    s = proc.communicate()
    # return console output
    return s[0]
    
def stop():
    # stop bluetooth
    execute("hciconfig hci0 down")