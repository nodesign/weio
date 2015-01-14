#######################################
#                                     #
#       HOW TO HAVE SMARTPHONE        #
#      GYROSCOPE ANGLES ON WEIO       #
#                                     #
#######################################

# Description: This example shows how track and display smartphone 
#              gyroscope angles on user interface and console.
# syntax = genericMessage("gyro",<angle>) is used to send values
#          from JavaScript to python

from weioLib.weio import *

def setup():
    # attaches event/genericMessage "gyro" to function gyroHandler 
    attach.event('gyro', gyroHandler)

def gyroHandler(dataIn):
    # gyroscope angles
    alpha = dataIn[0]
    beta  = dataIn[1]
    gamma = dataIn[2]
    # print gyroscope angles on the console
    print "Gyroscope angles => alpha=",alpha,"beta=",beta,"gamma=",gamma
    



