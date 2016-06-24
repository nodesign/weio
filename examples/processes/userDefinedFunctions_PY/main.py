#                                     
#   Call a firmware defined function  
#                                     
# This example explains how to call a user defined function
# in the co-processor firmware.
# This example will call the example user function, compiled
# in the co-processor firmware. See this page :
# https://github.com/nodesign/UPER/tree/master/UserFunctions
# to understand how to write your own function.
#
# Usage :
# ret = userDefinedFunction(FID, ret, args)
# param FID : The SFP command ID to call
# param ret : 1 if a return value is expected, otherwise 0
# param args : A list of arguments (the arguments of your
#              own co-processor function
# return : A list containing the returned value of your
#          own co-processor function
#

from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    while True:
        ret = userDefinedFunction(200, 0, [0])
        print ret
        delay(500)
        ret = userDefinedFunction(200, 0, [1])
        print ret
        delay(500)

