#######################################
#                                     #
#   how to read enoder using  WEIO    #
#                                     #
#######################################

from weioLib.weio import *
from things.input.motion.rotary_encoder import RotaryEncoder

def setup():
    encoder = RotaryEncoder(0, 1, callback)
    print "ready"

# this callback will be called each time when encoder is turned
def callback(direction, position):
    print position