#!/usr/bin/env python
# encoding: utf-8
from devices import uper
import time 

def myCallBack(interrupt):
    print " this is my UPER1 callback working!"
    print "        interrupt No:        ", interrupt[1][0]
    print "        interrupt reason:    ", interrupt[1][1]

uper = uper.UPER(myCallBack) #on Windows try --> uper = UPER(myCallBack"COM5")

uper.setSecondary(30)
print "analogRead = %x" % uper.analogRead(3)

uper.attachInterrupt(2,33,4)

# blue
uper.setSecondary(22)
# red
uper.setSecondary(29)
# green
uper.setSecondary(28)

uper.pwm0_begin(20000)
#uper.pwm0_set(2,20000)
uper.pwm0_set(0,20000)
#uper.pwm0_set(1,20000)
print "20"
time.sleep(1)
#uper.pwm0_set(2,0)
uper.pwm0_set(0,0)
#uper.pwm0_set(1,0)
print "0"
time.sleep(1)


#while True :
    
#    for i in range(0,50):
#        val = (50-i)*400
#        uper.pwm0_set(2,val)
#        uper.pwm0_set(3,val)
#        time.sleep(0.1)
        #print val
        
        
#    for i in range(0,50):
#        val = i*400
#        uper.pwm0_set(2,val)
#        uper.pwm0_set(3,val)
#       time.sleep(0.1)
        #print val
        
    
#time.sleep(10)
#uper.pwm0_set(2,1000)
uper.stop()
