#######################################
#                                     #
#       HOW TO HAVE PWM ON WEIO       #
#                                     #
#######################################

# syntax = pwmWrite(pin, value) 
# avalaible on pins 18, 19, 20, 21, 22, 23
# default value is between 0 and 100%, floating points are
# permitted for greater precision, PWM has 16bits precision
# pins 18, 19, 20 are connected on RGB LED on the board

from weioLib.weio import *

def setup():
    # attaches "fadeInOut" fuction to infinite loop
    attach.process(fadeInOut)
    
def fadeInOut():
    # create infinite loop
    while True:
        
        # print "fade in" in the console
        print "fade in"
        # count from 0 to 100 % 
        for i in range(0,100):
            # change PWM duty cycle to i
            pwmWrite(18,i)
            pwmWrite(19,i)
            pwmWrite(20,i)
            
        # print "fade out" in the console
        print "fade out"  
        # count from 0 to 100 % 
        for i in range(0,100):
            # change PWM duty cycle to 100-i
            pwmWrite(18,100-i)
            pwmWrite(19,100-i)
            pwmWrite(20,100-i)

