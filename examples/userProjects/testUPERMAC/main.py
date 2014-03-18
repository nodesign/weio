from IoTPy.pyuper.uperio import UperIO
from IoTPy.pyuper.pwm import PWM
from IoTPy.pyuper.utils import UPER_APIError, die

import colorsys
from time import sleep


try:
	u = UperIO()
except UPER_APIError, e: # seems can't establish connection with the UPER board
	details = e.args[0]
	die(details)

try: # let's try to attach PWM object to non PWM pin
	a = u.get_pin(PWM, 23)
except UPER_APIError, e: # got an exception, pin capabilities must be different from requested
	details = e.args[0]
	print details

with u.get_pin(PWM, 27) as R, u.get_pin(PWM, 28) as G, u.get_pin(PWM, 34) as B:
	R.width_us(0)
	R.width_us(2500)
	sleep(0.5)
	R.width_us(10000)
	sleep(0.5)
	R.write(0)
	sleep(0.5)
	R.write(0.25)
	sleep(0.5)
	R.write(0.9)
	print "Red LED duty is:", R.read()
	sleep(0.5)

	for color in range(500):
		rgb = colorsys.hls_to_rgb(color*0.002, 0.1, 1)
		R.write(rgb[0])
		G.write(rgb[1])
		B.write(rgb[2])
		print "R:", R.read(), "G:", G.read(), "B:", B.read()
		sleep(0.01)

	R.width_us(0)
	G.width_us(0)
	B.width_us(0)