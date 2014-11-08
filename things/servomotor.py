###
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
###

###
# Controling servo motor with PWM signal
# Pulse length is constant of 20ms, variate impulse from 1ms to 2ms
#
#   +---+                +---+
#   |   |                |   |
#   |   |                |   |
#   |   |                |   |
#---+   +----------------+   +------
# -->   <--1 ms = 5%
#   <-------- 20 ms ----> 
#
#
#   +------+            +------+
#   |      |            |      |
#   |      |            |      |
#   |      |            |      |
#---+      +------------+      +------
# -->      <--2 ms = 10%
#   <------- 20 ms ----->
###
from weioLib.weio import *

class Servo:

    def __init__(self, pin, minangle=0.0, maxangle=180.0):
        self.minangle = float(minangle)
        self.maxangle = float(maxangle)
        self.pin = pin
        # At first angle is unknown after first setting of angle this variable is updated
        # This is just simple mechanism of tracking no real feedback
        self.angle = None
        # Set PWM period to fire every 20ms
        setPwmPeriod(self.pin, 20000)

    def write(self, data):
        """Move servo to n degrees. Every 20ms variate signal from 5% - 10% with PWM"""

        # Make proportion calculation here, map angle to percrents
        if (data>self.maxangle):
            data = self.maxangle
            print "Warning, max allowed angle is ", self.maxangle , " value is set to " , self.maxangle

        if (data<self.minangle):
            data = self.minangle
            print "Warning, min allowed angle is " , self.minangle , " value is set to " , self.minangle

        self.angle = proportion(data, self.minangle, self.maxangle, 5.0, 10.0)

        pwmWrite(self.pin, self.angle)

    def read(self):
        return self.angle