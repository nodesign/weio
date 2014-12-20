#######################################
#                                     #
#   HOW TO USE STEPPERMOTOR ON WEIO   #
#                                     #
#######################################

# Description: This example shows how to use stepper.py class to 
#              control a stepper motor from WeIO using digital outputs.
#
# Syntax: Stepper(stepsIn360, coilApin0, coilApin1, coilBpin0, coilBpin1)
#         setStepperMode(stepMode) - FULL_STEP (0) or HALF_STEP (1) 
#         setSpeed(revolutionsPerSecond) - int
#         step(numberOfSteps) - int

from weioLib.weio import *
from things.output.motor.stepper import Stepper, FULL_STEP, HALF_STEP


def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello Stepper Motor")
    # Create Stepper class: 45 steps. Pins 0, 1, 2 & 3
    s = Stepper(45, 0,1,2,3)
    # Set FULL_STEP mode (360 degree)
    s.setStepperMode(FULL_STEP)
    # Set stepper motor rotation speed to 30 revolutions per second
    s.setSpeed(30)
    # do 2 steps
    s.step(2)

    
