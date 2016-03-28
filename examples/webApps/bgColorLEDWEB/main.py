from weioLib.weio import *
 
import colorsys
import time
 
def setup():
    # Attaches attaches event/genericMessage "gyro" to function gyroHandler
    attach.event('gyro', gyroHandler)
    sharedVar[0] = 0
 
def gyroHandler(dataIn) :
   if dataIn[0] is not None :
       #print dataIn
       #print "FROM BROWSER: ", dataIn["data"], " uuid: ", dataIn["uuid"]

       # gyroscope angles
       alpha = dataIn[0]
       beta  = dataIn[1]
       gamma = dataIn[2]

       # print gyroscope angles on the console
       #print "Gyroscope angles => alpha = ",alpha,"beta = ",beta,"gamma = ",gamma

       #We normalize Intervalle to [0,1]
       # alpha Intervalle [0,360] to [0,1]
       alphaI = proportion(alpha,0.0,360.0, 0.0,1.0)

       # beta Intervalle [-180,180] to [0,1]
       beta = beta + 180
       betaI = proportion(beta,0.0,360.0, 0.0,1.0)

       #gamma Intervalle [-90,90] to [0,1]
       gamma = gamma +90
       gammaI = proportion(gamma,0.0,180.0, 0.0,1.0)

       #print " Intervale => alphaI = ",alphaI,"betaI =",betaI,"gammaI = ",gammaI

       #rgb output is 0.0-1.0 transform to 0-255
       red = int(alphaI*255.0)
       green = int(betaI*255.0)
       blue = int(gammaI*255.0)
 
       #print red, " ", green, " ", blue
       # Export color to LED
       setColor(red,green,blue)

       # rgb output is 0.0-1.0 transform to 0-100 LED rgb
       redLed = int(alphaI*100.0)
       greenLed = int(betaI*100.0)
       blueLed = int(gammaI*100.0)
       setColorLed(redLed,greenLed,blueLed)

def setColorLed(r,g,b):
    # LED values are comprised between 0 and 100(%).
    # For hardware reasons, LEDs lit when pin is LOW (0V)
    # This is why the value is inverted here : 100% - led value
    pwmWrite(18,100-r)
    pwmWrite(19,100-g)
    pwmWrite(20,100-b)

def setColor(r,g,b):
    colorData = {}
    colorData["red"] = r
    colorData["green"] = g
    colorData["blue"] = b

    serverPush("usrMsg", colorData)

def proportion(value,istart,istop,ostart,ostop) :
       return float(ostart) + (float(ostop) - float(ostart)) * ((float(value) - float(istart)) / (float(istop) - float(istart)))
