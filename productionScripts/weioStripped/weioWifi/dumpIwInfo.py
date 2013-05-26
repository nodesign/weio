from iwInfo import *
import sys, os, logging

logging.basicConfig()
log = logging.getLogger("IWInfo dumper")
log.setLevel(logging.DEBUG)

if __name__  ==  '__main__':
    iwl = IWInfo("wlan0")
    print iwl.getData()

    
