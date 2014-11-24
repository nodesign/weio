#######################################
#                                     #
#   HOW TO GET MILLIS ON WEIO         #
#                                     #
#######################################

# Description: how to get time (in milliseconds) from first power up of the 
#              board.
# WeIO functions: millis() 

from weioLib.weio import *

def setup():
    # attaches process myProcess
    attach.process(myProcess)
    
def myProcess():
    
    # get time from first power up of the board
    t1 = millis() 
    # create infinite loop
    while True:
        # get time from first power up of the board
        t2 = millis()
        # t2 - t1 represents n of milliseconds from this process launch
        print "millis = ", t2 - t1 
        # sleep during 1s
        delay(1000)
        

