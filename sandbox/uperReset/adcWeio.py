from weioLib.weioIO import *
from weioLib import weioIO
from weioLib.weioGpio import WeioGpio


for i in range(0,3):
    w = WeioGpio()
    weioIO.gpio = w
    for a in range(0,10):
        digitalWrite(19,1)
        val = digitalRead(24)
        print val
        delay(10)
        digitalWrite(19,0)
        delay(10)
    w.stopReader()
    w.reset()


# from weioLib.weioGpio import WeioGpio
# import time
# 
# for i in range(0,3):
#     w = WeioGpio()
# 
#     for a in range(0,10):
#         w.digitalWrite(19,1)
#         val = w.analogRead(24)
#         print val
#         time.sleep(0.09)
#         w.digitalWrite(19,0)
#         time.sleep(0.09)
# 
#     w.reset()
