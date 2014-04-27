# Stepper motor driver
# Uros Petrevski, 2014
# Implemented both full step and half-step control
from IoTPy.pyuper.gpio import GPIO
from time import sleep

FULL_STEP = 0
HALF_STEP = 1


class Stepper:

    def __init__(self, uperObj, stepsIn360, coilApin0, coilApin1, coilBpin0, coilBpin1):
        self.u = uperObj
        self.totalSteps = stepsIn360
        self.delayLength = 0.01

        # Wave stepping scheme, full step
        self.fullStepCoilA = [1,0,-1,0]
        self.fullStepCoilB = [0,1,0,-1]

        # Half stepping scheme
        self.halfStepCoilA = [1,1,0,-1,-1,-1,0,1]
        self.halfStepCoilB = [0,1,1,1,0,-1,-1,-1]

        self.stepperMode = FULL_STEP

        # declare pins
        self.A0 = self.u.get_pin(GPIO, coilApin0)
        self.A1 = self.u.get_pin(GPIO, coilApin1)

        self.B0 = self.u.get_pin(GPIO, coilBpin0)
        self.B1 = self.u.get_pin(GPIO, coilBpin1)

        # declare motor pins in output mode
        self.A0.mode(GPIO.OUTPUT)
        self.A1.mode(GPIO.OUTPUT)

        self.B0.mode(GPIO.OUTPUT)
        self.B1.mode(GPIO.OUTPUT)

    def setStepperMode(self, sMode):
        self.stepperMode = sMode

    def setSpeed(self, rpm):
        self.delayLength = 30.0/(self.totalSteps*rpm)

    def fireSignal(self, pin0, pin1, data):
        if data == 0:
            pin0.write(0)
            pin1.write(0)
        elif data == 1:
            pin0.write(1)
            pin1.write(0)
        elif data == -1:
            pin0.write(0)
            pin1.write(1)

    def step(self, steps):
        nSteps = abs(steps)
        for s in range(0,nSteps):
            if (self.stepperMode==FULL_STEP):
                phase = s%4
                if (steps>0):
                    self.fireSignal(self.A0,self.A1, self.fullStepCoilA[phase])
                    self.fireSignal(self.B0,self.B1, self.fullStepCoilB[phase])
                else :
                    self.fireSignal(self.A0,self.A1, self.fullStepCoilB[phase])
                    self.fireSignal(self.B0,self.B1, self.fullStepCoilA[phase])
                sleep(self.delayLength)

            elif (self.stepperMode==HALF_STEP):
                phase = s%8
                if (steps>0):
                    self.fireSignal(self.A0,self.A1, self.halfStepCoilA[phase])
                    self.fireSignal(self.B0,self.B1, self.halfStepCoilB[phase])
                else :
                    self.fireSignal(self.A0,self.A1, self.halfStepCoilB[phase])
                    self.fireSignal(self.B0,self.B1, self.halfStepCoilA[phase])
                sleep(self.delayLength)
