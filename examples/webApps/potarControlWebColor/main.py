from weioLib.weio import *
 
import colorsys
import time
 
def setup():
    # Attaches interrupt from Web client to "message" string
    attach.process(potar)
    sharedVar[0] = 0
 
def setColorLed(r,g,b):
    pwmWrite(18,100-r)
    pwmWrite(19,100-g)
    pwmWrite(20,100-b)

def setColor(r,g,b):
    # LED values are comprised between 0 and 100(%).
    # For hardware reasons, LEDs lit when pin is LOW (0V)
    # This is why the value is inverted here : 100% - led value
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
 
       if (abs(val-val_p)>4):
           hue = proportion(val,0,1023, 0.0,1.0)
           # drive HUE color and transform to rgb for LED
           rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
           
           # rgb output is 0.0-1.0 transform to 0-255
           red = int(rgb[0]*255.0)
           green = int(rgb[1]*255.0)
           blue = int(rgb[2]*255.0)
        
           # rgb output is 0.0-1.0 transform to 0-100
           redLed = int(rgb[0]*100.0)
           greenLed = int(rgb[1]*100.0)
           blueLed = int(rgb[2]*100.0)
 
 
           setColorLed(redLed,greenLed,blueLed)
           setColor(red,green,blue)
 
       val_p = val
       time.sleep(0.05)
 
def proportion(value,istart,istop,ostart,ostop) :
       return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))
