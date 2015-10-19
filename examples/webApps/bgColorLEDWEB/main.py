from weioLib.weio import *
 
import colorsys
import time
 
def setup():
    # Attaches interrupt from Web client to "message" string
    attach.event('message', buttonHandler)
    attach.process(potar)
    sharedVar[0] = 0
 
def buttonHandler(dataIn) :
   if dataIn is not None :
       #print dataIn
       #print "FROM BROWSER: ", dataIn["data"], " uuid: ", dataIn["uuid"]
       beta = float(dataIn)
 
       # put limiters
       if (beta>88):
           beta = 88
       if (beta<-88):
           beta = -88
 
       # map interval between -88 and 88 to 0.0 - 1.0
       hue = proportion(beta,-88.0,88.0, 0.0,1.0)
       # drive HUE color and transform to rgb for LED
       rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
 
 
       # rgb output is 0.0-1.0 transform to 0-255
       red = int(rgb[0]*100.0)
       green = int(rgb[1]*100.0)
       blue = int(rgb[2]*100.0)
 
       print red, " ", green, " ", blue
       # Export color to LED
       setColor(red,green,blue)
 
def setColor(r,g,b):
    pwmWrite(18,100-r)
    pwmWrite(19,100-g)
    pwmWrite(20,100-b)
 
    colorData = {}
    colorData["red"] = r
    colorData["green"] = g
    colorData["blue"] = b
 
    serverPush("usrMsg", colorData)
 
def potar() :
   val = 0
   val_p = 0
   while True:
       val = analogRead(25)
 
       if (abs(val-val_p)>10):
           hue = proportion(val,0,1023, 0.0,1.0)
           # drive HUE color and transform to rgb for LED
           rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
 
           # rgb output is 0.0-1.0 transform to 0-255
           red = int(rgb[0]*100.0)
           green = int(rgb[1]*100.0)
           blue = int(rgb[2]*100.0)
 
           setColor(red,green,blue)
 
       val_p = val
       time.sleep(0.05)
 
def proportion(value,istart,istop,ostart,ostop) :
       return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))