from devices import uper
from weioLib.weioUserApi import shared, pins, adcs, HIGH, LOW, INPUT, INPUT_PULLDOWN, INPUT_PULLUP, OUTPUT, ADC_INPUT


class WeioGpio():
    
    def __init__(self):
        # construct uper device, open serial port
        # send default values
        self.uper = uper.UPER()
        shared.declaredPins = set()
    
    def pinMode(self, pin, mode) :
        """Sets pin to input or output mode. Available modes are : OUTPUT, INPUT (high Z), INPUT_PULLDOWN, INPUT_PULLUP, ADC_INPUT"""
        if mode is ADC_INPUT:
            self.uper.setSecondary(pins[pin])
        else :
            self.uper.setPrimary(pins[pin])
            self.uper.pinMode(pins[pin], mode)
        
        shared.declaredPins.add(pin)
        
    def digitalWrite(self,pin, state) :
        """Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground"""
        if pin not in shared.declaredPins:
            self.uper.setPrimary(pins[pin])
            self.uper.pinMode(pins[pin], OUTPUT)
            shared.declaredPins.add(pin)
        
        self.uper.digitalWrite(pins[pin], state)

    def digitalRead(self,pin) :
        """Reads actual voltage on corresponding pin. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected"""
        if pin not in shared.declaredPins:
            self.uper.setPrimary(pins[pin])
            self.uper.pinMode(pins[pin], INPUT)
            shared.declaredPins.add(pin)

        return self.uper.digitalRead(pins[pin])

    def analogRead(self, pin) :
        """Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023"""
        if ((pin >= adcs[0]) and (pin <= adcs[-1])):
            if pin not in shared.declaredPins:
                self.uper.setSecondary(pins[pin])
                shared.declaredPins.add(pin)

            adcPin = adcs.index(pin)
            return self.uper.analogRead(adcPin)
        else :
            print "*SYSOUT*Error! Pin " + str(pin) + " is not ADC pin, ADCs are on pins 25-32!"
            return -1