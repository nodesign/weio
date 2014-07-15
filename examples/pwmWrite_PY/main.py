#######################################
#                                     #
#   how to have PWM on WEIO           #
#                                     #
#######################################

#syntax = pwmWrite(pin, value) or analogWrite(pin, value)
# there are 6 pwm pins on weio (23, 22, 21, 20, 19, 18)
# default value is between 0 and 255
# pins 18, 19, 20 are connected on RGB LED on the board


from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared

def setup() :
    attach.process(loop)
    
def loop() :
    
    while True:
        print "fade in"
        # count from 0 to 255 
        for i in range(0,256):
            pwmWrite(18,i)
            pwmWrite(19,i)
            pwmWrite(20,i)
            delay(3)
            
        print "fade out"    
        for i in range(0,256):
            pwmWrite(18,255-i)
            pwmWrite(19,255-i)
            pwmWrite(20,255-i)
            delay(3)
