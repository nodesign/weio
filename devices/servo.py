from weioLib.weioIO import setPwmPeriod, pwmWrite, setPwmLimit, proportion

class Servo:
    
    def __init__(self):
        # Set 20ms signal length for PWM
        setPwmPeriod(20000)
        # Set maximum precision for this freq
        setPwmLimit(19999)
        # Down limit frequency expressed in uS
        self.downLimit = 1000 # 5% of 20000
        self.upLimit = self.downLimit*2 # 10% of 20000
        self.minAngle = 0
        self.maxAngle = 180
        self.angle = None
        self.readuS = None

    def write(self, pin, data):
        # Write to coresponding servo motor
        val = int(proportion(data, self.minAngle,self.maxAngle, self.downLimit, self.upLimit))
        self.readuS = val
        self.angle = data
        pwmWrite(pin, 19999-self.readuS)
        
    def setMinLimit(self, val):
        self.downLimit = val
        
    def setMaxLimit(self, val):
        self.upLimit = val
    
    def setMinAngle(self, val):
        self.minAngle = val
        
    def setMaxAngle(self, val):
        self.maxAngle = val    
    
    def read(self):
        return self.angle
        
    def readuS(self):
        return self.readuS