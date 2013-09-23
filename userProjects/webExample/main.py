from devices import uper
from weioLib import weio
import colorsys

def buttonHandler(dataIn) :
    print "FROM BROWSER: ", dataIn
    beta = float(dataIn)
    
    # put limiters
    if (beta>88):
        beta = 88
    if (beta<-88):
        beta = -88
    
    # map interval between -88 and 88 to 0.0 - 1.0
    hue = mapf(beta,-88,88, 0,1)
    # drive HUE color and transform to rgb for LED 
    rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    
    # rgb output is 0.0-1.0 transform to 0-255
    red = int(rgb[0]*255.0)
    green = int(rgb[1]*255.0)
    blue = int(rgb[2]*255.0)
    
    print red, " ", green, " ", blue
    
    # Export color to LED
    setColor(red,green,blue)
    
def setColor(r,g,b):
    red = (255-r)*78
    green = (255-g)*78
    blue = (255-b)*78
    uper.pwm0_set(2,red)
    uper.pwm0_set(0,green)
    uper.pwm0_set(1,blue)
    

def mapf(value,istart,istop,ostart,ostop) :
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

# Attaches interrupt from Web client to "message" string
weio.attach.event('message', buttonHandler)

uper = uper.UPER()

# blue
uper.setSecondary(22)
# red
uper.setSecondary(29)
# green
uper.setSecondary(28)

# 19890 divided by 255 is 78
uper.pwm0_begin(19890)
