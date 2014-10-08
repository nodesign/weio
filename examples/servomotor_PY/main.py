#######################################
#                                     #
#   how to use servomotor on WEIO     #
#                                     #
#######################################

#servomotor library
# there are 6 pwm pins on weio (23, 22, 21, 20, 19, 18)
# servomotor use pwm pin. 
# initServo(pin) return Servo object and attach the Servo variable to a pwm pin
# write(angle) servo is a vairable of type Servo
# angle is the value to write to the servo, from 0 to 180

# other functions :
# writeMilliseconds(ms)
# readMilliseconds()
# read()

from weioLib.weio import *
from things.servomotor import Servo

def setup():
    attach.process(myProcess)
    
def myProcess():
    s = weioLib(Servo,23)
    while True :
        for i in range(180):
            s.write(i)
            print s.read()
            delay(20)

        for i in range(180):
            s.write(180-i)
            print s.readMilliseconds()
            delay(20)