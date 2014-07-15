#######################################
#                                     #
#   how to have tone on WEIO          #
#                                     #
#######################################

#syntax = tone(pin, hertz, duration) 
# there are 6 pwm pins on weio (23, 22, 21, 20, 19, 18)
# tone use pwm pin. 
# duration is optionnal and is in milliseconds 
# notone(pin) is function to detach tone of pin (you don't need this function if you use duration argument

from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcess)
    
def myProcess():
    i = 0
    while True:
        tone(23,i)
        i = i +1
        print "i = ",i
        delay(100)
