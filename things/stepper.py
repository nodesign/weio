# Stepper motor driver
# Uros Petrevski, 2014
# Implemented both full step and half-step control
from weioLib.weio import *
from time import sleep

FULL_STEP = 0
HALF_STEP = 1

class Stepper:
    """
    Stepper motor class.

    :param stepsIn360: The number of steps in full (360 degree) rotation.
    :type stepsIn360: int
    :param coilApin0: GPIO ID of coil A pin 0.
    :type coilApin0: int
    :param coilApin1: GPIO ID of coil A pin 1.
    :type coilApin1: int
    :param coilBpin0: GPIO ID of coil B pin 0.
    :type coilBpin0: int
    :param coilBpin1: GPIO ID of coil B pin 1.
    :type coilBpin1: int
    """

    def __init__(self, stepsIn360, coilApin0, coilApin1, coilBpin0, coilBpin1):

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
        self.A0 = coilApin0
        self.A1 = coilApin1

        self.B0 = coilBpin0
        self.B1 = coilBpin1

        # declare motor pins in output mode
        pinMode(self.A0, OUTPUT)
        pinMode(self.A1, OUTPUT)
        
        pinMode(self.B0, OUTPUT)
        pinMode(self.B1, OUTPUT)
        
    def setStepperMode(self, sMode):
        """
        Set stepper motor step mode.

        :param sMode: Step mode: Stepper.FULL_STEP or Stepper.HALF_STEP
        """
        self.stepperMode = sMode

    def setSpeed(self, rpm):
        """
        Set stepper motor rotation speed.

        :param rpm: Revolutions per second.
        :type rpm: int
        """
        self.delayLength = 30.0/(self.totalSteps*rpm)

    def _fireSignal(self, pin0, pin1, data):
        if data == 0:
            digitalWrite(pin0,LOW)
            digitalWrite(pin1,LOW)
        elif data == 1:
            digitalWrite(pin0,HIGH)
            digitalWrite(pin1,LOW)
        elif data == -1:
            digitalWrite(pin0,LOW)
            digitalWrite(pin1,HIGH)

    def step(self, steps):
        """
        Step a specified number of steps.

        :param steps: Number of steps.
        :type steps: int
        """
        nSteps = abs(steps)
        for s in xrange(0,nSteps):
            if (self.stepperMode==FULL_STEP):
                phase = s%4
                if (steps>0):
                    self._fireSignal(self.A0,self.A1, self.fullStepCoilA[phase])
                    self._fireSignal(self.B0,self.B1, self.fullStepCoilB[phase])
                else :
                    self._fireSignal(self.A0,self.A1, self.fullStepCoilB[phase])
                    self._fireSignal(self.B0,self.B1, self.fullStepCoilA[phase])
                sleep(self.delayLength)

            elif (self.stepperMode==HALF_STEP):
                phase = s%8
                if (steps>0):
                    self._fireSignal(self.A0,self.A1, self.halfStepCoilA[phase])
                    self._fireSignal(self.B0,self.B1, self.halfStepCoilB[phase])
                else :
                    self._fireSignal(self.A0,self.A1, self.halfStepCoilB[phase])
                    self._fireSignal(self.B0,self.B1, self.halfStepCoilA[phase])
                sleep(self.delayLength)
