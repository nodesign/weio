from weioLib.weio import *
from things.output.motor.stepper import Stepper, FULL_STEP, HALF_STEP


def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello world")
    s = Stepper(45, 0,1,2,3)
    s.setStepperMode(FULL_STEP)
    s.setSpeed(30)
    s.step(2)

    
