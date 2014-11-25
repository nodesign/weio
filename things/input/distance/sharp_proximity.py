import uper, time

up = uper.Uper()

for i in xrange(100):
	val = up.analogRead(23)
	print val, "papugos"
	voltai = 5.0/1024 * val
	print voltai, "V"

	if val >= 3:
		dist = (6787/(val-3))-4
	print dist, "cm"

	time.sleep(0.5)