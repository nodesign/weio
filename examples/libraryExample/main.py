from weioLib.weioIO import *
from weioLib.weioUserApi import attach
# import servo library
from things.servomotor import Servo

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello world")
    # init servo object
    s = Servo(getWeio(), 23)
    # write angle
    s.write(180)
    print "over"