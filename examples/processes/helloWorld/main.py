#######################################
#                                     #
#        HELLO WORLD ON WEIO          #
#                                     #
#######################################

# Description: Print "Hello World" message to the console
# WeIO functions: none

from weioLib.weio import *

def setup():
     # Attaches myProcess function to infinite loop
    attach.process(myProcess)
    
def myProcess():
    # print message to the console
    print("Hello world")
