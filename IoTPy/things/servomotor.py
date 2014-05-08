###
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Ronan Yvergniaux <ronan@yvergniaux.fr
#		7 May 2014
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


from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pwm import PWM
from IoTPy.pyuper.utils import IoTPy_APIError, die

class Servo:
	def __init__(self, board, pin, msmin = 1,msmax = 2, minangle = 0, maxangle=180 ):
		self.board = board
		self.pwm = self.board.get_pin(PWM, pin)
		self.msmin = float(msmin)
		self.msmax = float(msmax)
		self.minangle = minangle
		self.maxangle = maxangle
		self.pwm.period(20000)

	def write(self, data):
		"""Move servo to n degrees"""
		valmin = self.msmin/20.0
		valmax = self.msmax/20.0
		val = (data-self.minangle)*(valmax-valmin)/(self.maxangle-self.minangle)+valmin
		self.pwm.write(1-val)

	def writeMilliseconds(self, milli):
		"""Move servo expressed by pulses in ms"""
		milli = milli/20.0
		self.pwm.write(1-milli)

	def readMilliseconds(self):
		"""Read servo in ms"""
		val = 1 - self.pwm.read()
		val = val*20
		return val

	def read(self):
		"""Read servo in degree"""
		val = 1 - self.pwm.read()
		val = val*20
		val = (val-self.msmin)*(self.maxangle-self.minangle)/(self.msmax-self.msmin)+self.minangle
		return val
