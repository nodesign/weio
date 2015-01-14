#######################################
#                                     #
#   Scan wifi cells around WeIO and   #
#   get basic info                    #
#                                     #
#######################################
from weioLib.weio import *
from weioWifi import iwInfo

def setup():
    attach.process(myProcess)
    
def myProcess():
    
    print("wifi scan")
    wifi = iwInfo.IWInfo("wlan0")

    wifi.refresh()
    cells = wifi.parseRawData(wifi.rawdata)
    print "Number of detected Wifi cells =", len(cells)
    
    # list detected cells
    for n in cells:
        cell = cells[n]
        print "ESSID :",cell["ESSID"], "Quality :",cell["Quality"]
        # possible parameters :
        # Number, MAC, ESSID, Protocol, Mode, Frequecy, Channel, Signal, Quality,
        # Encryption, Bit Rates, Extra