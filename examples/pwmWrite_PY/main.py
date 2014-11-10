#######################################
#                                     #
#   how to have PWM on WEIO           #
#                                     #
#######################################

# syntax = pwmWrite(pin, value) or analogWrite(pin, value)
# there are 6 pwm pins on weio (23, 22, 21, 20, 19, 18)
# default value is between 0 and 100% floating points are
# permitted for greater precision, PWM has 16bits precision
# pins 18, 19, 20 are connected on RGB LED on the board


from weioLib.weio import *

def setup():
    attach.process(loop)
    
def loop():
    while True:
        print "fade in"
        # count from 0 to 100 % 
        for i in range(0,101):
            pwmWrite(18,i)
            pwmWrite(19,i)
            pwmWrite(20,i)
            delay(3)
            
        print "fade out"    
        for i in range(0,101):
            pwmWrite(18,100-i)
            pwmWrite(19,100-i)
            pwmWrite(20,100-i)
            delay(3)

