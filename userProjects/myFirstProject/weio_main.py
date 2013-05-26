import time, os, sys
# only during devel time, in production weioLib will be in path
sys.path.append(r'./');
from weioLib import weio_gpio 
from weioLib import weio_globals

print "Hello from Weio"


for a in range(4) :
    weio_gpio.digitalWrite(21, weio_globals.HIGH)
    print(str(a))
    time.sleep(0.5)
    weio_gpio.digitalWrite(21, weio_globals.LOW)
    time.sleep(0.5)

             

