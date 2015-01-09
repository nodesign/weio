#######################################
#                                     #
#   how to have digitalWrite on WEIO  #
#                                     #
#######################################

#syntax = digitalWrite(pin,Value) 
#Value is 0 and 1, or LOW and HIGH 
#pins 18, 19, 20 is connected with RGB LED

from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    while True :
        digitalWrite(18,0)
        delay(70)
        digitalWrite(20,1)
        delay(70)
        digitalWrite(19,0)
        delay(70)
        digitalWrite(18,1)
        delay(70)
        digitalWrite(20,0)
        delay(70)
        digitalWrite(19,1)
        delay(70)

