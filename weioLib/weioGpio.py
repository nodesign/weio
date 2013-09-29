from devices import uper
from weioLib.weioUserApi import shared, pins, adcs, pwms, HIGH, LOW, INPUT, INPUT_PULLDOWN, INPUT_PULLUP, OUTPUT, ADC_INPUT, PWM_OUTPUT, PWM0_OUTPUT, PWM1_OUTPUT

class WeioGpio():
    
    def __init__(self):
        # construct uper device, open serial port
        # send default values
        self.uper = uper.UPER()
        shared.declaredPins = []
        for a in range(0,len(pins)):
            shared.declaredPins.append(-1)
    
        self.pwm0PortPeriod = 20000
        self.pwm1PortPeriod = 20000
    
        self.pwm0Limit = 255
        self.pwm1Limit = 255
        
        self.pwm0BeginCalled = False
        self.pwm1BeginCalled = False
        
        #print "Hello from GPIO"
        
    
    def pinMode(self, pin, mode) :
        """Sets pin to input or output mode. Available modes are : OUTPUT, INPUT (high Z), INPUT_PULLDOWN, INPUT_PULLUP, ADC_INPUT"""
        # Action
        if mode is ADC_INPUT:
            self.uper.setSecondary(pins[pin])
        else :
            self.uper.setPrimary(pins[pin])
            self.uper.pinMode(pins[pin], mode)
        shared.declaredPins[pin] = mode
        
    def digitalWrite(self,pin, state) :
        """Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground"""
        if shared.declaredPins[pin] != OUTPUT:
            self.uper.setPrimary(pins[pin])
            self.uper.pinMode(pins[pin], OUTPUT)
            shared.declaredPins[pin] = OUTPUT
            
        self.uper.digitalWrite(pins[pin], state)

    def digitalRead(self,pin) :
        """Reads actual voltage on corresponding pin. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected"""
        if (shared.declaredPins[pin] != INPUT) or (shared.declaredPins[pin] != INPUT_PULLUP) or (shared.declaredPins[pin] != INPUT_PULLDOWN) :
            self.uper.setPrimary(pins[pin])
            self.uper.pinMode(pins[pin], INPUT)
            shared.declaredPins[pin] = INPUT

        return self.uper.digitalRead(pins[pin])

    def analogRead(self, pin) :
        """Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023"""
        if ((pin >= adcs[0]) and (pin <= adcs[-1])):
            if shared.declaredPins[pin] != ADC_INPUT:
                self.uper.setSecondary(pins[pin])
                shared.declaredPins[pin] = ADC_INPUT

            adcPin = adcs.index(pin)
            return self.uper.analogRead(adcPin)
        else :
            print "*SYSOUT*Error! Pin " + str(pin) + " is not ADC pin, ADCs are on pins 25-32!"
            return -1           
    
    def pwmWrite(self, pin, value) :
        if ((pin >= pwms[0]) and (pin <= pwms[2])):
            #port0
            if shared.declaredPins[pin] != PWM0_OUTPUT:
                self.uper.setSecondary(pins[pin])
                #print "DECLARED pin ", pin, " called ", pins[pin]
                if self.pwm0BeginCalled is False:
                    self.uper.pwm0_begin(self.pwm0PortPeriod)
                    self.pwm0BeginCalled = True
                    
                shared.declaredPins[pin] = PWM0_OUTPUT
        
            pwmPin = pwms.index(pin)
            
            # Security limiters
            if (value < 0) :
                value = 0
            if (value > self.pwm0Limit):
                value = self.pwm0Limit
            
            out = self.proportion(value, 0, self.pwm0Limit, self.pwm0PortPeriod, 0)
            self.uper.pwm0_set(pwmPin, out)
            #print "PWM on ", pwmPin, " value ", out
            
        elif ((pin >= pwms[3]) and (pin <= pwms[-1])):
            #port1
            if shared.declaredPins[pin] != PWM1_OUTPUT:
                self.uper.setSecondary(pins[pin])
                if self.pwm1BeginCalled is False:
                    self.uper.pwm1_begin(self.pwm1PortPeriod)
                    self.pwm1BeginCalled = True
                    
                shared.declaredPins[pin] = PWM1_OUTPUT
        
            pwmPin = 3-pwms.index(pin)
            
            # Security limiters
            if (value < 0) :
                value = 0
            if (value > self.pwm1Limit):
                value = self.pwm1Limit
            out = self.proportion(value, 0, self.pwm1Limit, self.pwm1PortPeriod, 0)
            self.uper.pwm1_set(pwmPin, out)
            #print "PWM on ", pwmPin, " value ", out
                
        else :
            print "*SYSOUT*Error! Pin " + str(pin) + " is not PWM pin, PWMs are on pins 19-24!"
    
    def proportion(self, value,istart,istop,ostart,ostop) :
        return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

    def setPwm0PortPeriod(self, period):
        if ((period >= 0) and (period <= 65535)): 
            self.pwm0PortPeriod = period
            if self.pwm0BeginCalled is False:
                    self.uper.pwm0_begin(self.pwm0PortPeriod)
                    self.pwm0BeginCalled = True
        else :
            print "*SYSOUT*Error! PWM period can be only between 0-65535"

    def setPwm1PortPeriod(self, period):
        if ((period >= 0) and (period <= 65535)): 
            self.pwm1PortPeriod = period
            if self.pwm1BeginCalled is False:
                    self.uper.pwm1_begin(self.pwm1PortPeriod)
                    self.pwm1BeginCalled = True
        else :
            print "*SYSOUT*Error! PWM period can be only between 0-65535"
    
    def setPwmPeriod(self, period):
        if ((period >= 0) and (period <= 65535)): 
            self.pwm0PortPeriod = period
            self.pwm1PortPeriod = period
            
            if self.pwm0BeginCalled is False:
                    self.uper.pwm0_begin(self.pwm0PortPeriod)
                    self.pwm0BeginCalled = True
                    
            if self.pwm1BeginCalled is False:
                    self.uper.pwm1_begin(self.pwm1PortPeriod)
                    self.pwm1BeginCalled = True
        
        else :
            print "*SYSOUT*Error! PWM period can be only between 0-65535"

    def setPwm0Limit(self, limit):
        if ((limit > 0) and (limit <= self.pwm0PortPeriod)):
            self.pwm0Limit = limit
        else:
            print "*SYSOUT*Error! PWM limit can't be superior than " + self.pwm0PortPeriod + " , 0 or inferior than 0"

    def setPwm1Limit(self, limit):
        if ((limit > 0) and (limit <= self.pwm1PortPeriod)):
            self.pwm1Limit = limit
        else:
            print "*SYSOUT*Error! PWM limit can't be superior than " + self.pwm1PortPeriod + " , 0 or inferior than 0"


    def setPwmLimit(self, limit):
        if ((limit > 0) and (limit <= self.pwm0PortPeriod) and (limit <= self.pwm1PortPeriod)):
            self.pwm0Limit = limit
            self.pwm1Limit = limit
        else:
            print "*SYSOUT*Error! PWM limit can't be superior than " + min(self.pwm0PortPeriod, self.pwm1PortPeriod)  + " , 0 or inferior than 0"