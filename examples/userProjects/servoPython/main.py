from weioLib.weioUserApi import attach, shared, LOW, HIGH
from weioLib.weioIO import *
import devices.servo

servoPin = 23

def setup() :
    digitalWrite(servoPin, LOW)
    attach.process(loop)
    
def loop() :
    

    while True :
        val = analogRead(25)
        val = int(proportion(val, 0,1024, 0,180))
        
        s = devices.servo.Servo()
        s.setMinLimit(650)
        s.setMaxLimit(3000)
        s.write(servoPin, val)