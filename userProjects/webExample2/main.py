from weioLib.weioUserApi import shared
from weioLib import weio
import colorsys

def setup():
    shared.gpio.setPwmPeriod(2000)

def buttonHandler(dataIn) :
    if dataIn is not None :
        print dataIn
        #print "FROM BROWSER: ", dataIn["data"], " uuid: ", dataIn["uuid"]
        beta = float(dataIn)
        
        # put limiters
        if (beta>88):
            beta = 88
        if (beta<-88):
            beta = -88
        
        # map interval between -88 and 88 to 0.0 - 1.0
        hue = proportion(beta,-88,88, 0,1)
        # drive HUE color and transform to rgb for LED 
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        
        # rgb output is 0.0-1.0 transform to 0-255
        red = int(rgb[0]*255.0)
        green = int(rgb[1]*255.0)
        blue = int(rgb[2]*255.0)
        
        colorData = {}
        colorData["red"] = red
        colorData["green"] = green
        colorData["blue"] = blue
        
        #print red, " ", green, " ", blue
        
        # Export color to LED
        setColor(red,green,blue)
        
        for client in weio.shared.connectedClients :
            client.connection.emit("usrMsg", colorData)

      
def setColor(r,g,b):
    global gpio
    
    shared.gpio.pwmWrite(19,255-b)
    shared.gpio.pwmWrite(20,255-r)
    shared.gpio.pwmWrite(21,255-g)


def proportion(value,istart,istop,ostart,ostop) :
        return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))

# Attaches interrupt from Web client to "message" string
weio.attach.event('message', buttonHandler)