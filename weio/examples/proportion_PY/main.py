#######################################
#                                     #
#   how to have porportion on WEIO    #
#                                     #
#######################################

#syntax = proportion(value, istart, istop, ostart, ostop)
#return a value proportionned 

from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    while True:
        a=analogRead(31) #value is between 0 and 1024
        print "analogRead = ",a
        a=proportion(a,0,1024,0,255) 
        print "analoRead porportioned = ",a
        pwmWrite(18,a) #value is between 0 and 255
        delay(500)
