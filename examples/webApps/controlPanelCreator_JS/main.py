#######################################
#                                     #
#      WEB APPLICATION ON WEIO:       #
#       CONTROL PANEL CREATOR         #
#                                     #
#######################################

from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Web Creator address: weio.local")
