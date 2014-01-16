from weioLib.weioUserApi import attach, LOW, HIGH
from weioLib.weioIO import *
import devices.servo

servoPin = 23
potentiometerPin = 25

def setup() :
    digitalWrite(servoPin, LOW)
    attach.process(loop)
    
def loop() :
    s = devices.servo.Servo()
    s.setMinLimit(650)
    s.setMaxLimit(2450)

    while True :
        # read value from potentiometer
        val = analogRead(potentiometerPin)
        val = int(proportion(val, 0,1023, 0,180))
        
        s.write(servoPin, val)
        delay(10)
        # with reading s.readuS you can make fine calibration of your 
        # servo motor limits
        #print s.readuS