![WeIO pinout](http://www.we-io.net/img/weioCarte.jpg)
## digitalWrite(pin, value)
Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach, HIGH, LOW, shared

import time

def setup() :
    attach.process(blinky)

def blinky() :
    pause = 100
    while True:
        digitalWrite(20, HIGH)
        delay(pause)
        digitalWrite(20, LOW)
        delay(pause)
```
***
## digitalRead(pin)
Reads actual voltage on corresponding pin. WeIO board is 5V TOLERANT. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected. If only digitalRead function is provided, pin will be in HIGH Z state. See [inputMode(pin,mode)](http://github.com/nodesign/weio/wiki/Weio-GPIO-API-using-UPER-board#inputmodepin-mode) function for more options. 
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared
import time

def setup() :
    attach.process(loop)
    
def loop() :
    pin = 25
    while True:
        val =  digitalRead(pin)
        print (val)
        delay(20)

```
***
## inputMode(pin, mode)
Sets input mode for digitalRead purpose. Available modes are : INPUT_HIGHZ, INPUT_PULLDOWN, INPUT_PULLUP
This function activates pullups, pulldowns or high Z state on declared pins. If inputMode function is not called and digitalRead is performed pin state will be in high Z by default
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared, INPUT_PULLDOWN
import time

def setup() :
    attach.process(loop)
    
def loop() :
    pin = 25
    inputMode(pin,INPUT_PULLDOWN)
    while True:
        val =  digitalRead(pin)
        print (val)
        delay(20)

```
## analogRead(pin)
Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared
import time

def setup() :
    attach.process(loop)
    
def loop() :
    while True:
        val = analogRead(25)
        print val
        delay(20)
```
***
## pwmWrite(pin, value)
Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 20000ms and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature look functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared

def setup() :
    attach.process(loop)
    
def loop() :
   
    while True:
        print "fade in"
        # count from 0 to 255 by 5
        for i in xrange(0,256,5):
            pwmWrite(19,i)
            pwmWrite(20,i)
            pwmWrite(21,i)
            delay(30)
        print "fade out"    
        for i in xrange(0,256,5):
            pwmWrite(19,255-i)
            pwmWrite(20,255-i)
            pwmWrite(21,255-i)
            delay(30)
```
***
## setPwmPeriod(period)
Overrides default value of 1000us to set new period value for whole 6 PWM pins. Period value must be superior than 0 and inferior than 65535.
```python 
from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared

def setup() :
    attach.process(loop)
    
def loop() :

    setPwmPeriod(500)
    while True:
        print "fade in"
        # count from 0 to 255 by 5
        for i in xrange(0,256,5):
            pwmWrite(19,i)
            pwmWrite(20,i)
            pwmWrite(21,i)
            delay(30)
        print "fade out"    
        for i in xrange(0,256,5):
            pwmWrite(19,255-i)
            pwmWrite(20,255-i)
            pwmWrite(21,255-i)
            delay(30)
```
***
## setPwmLimit(limit)
Overrides default limit of 8bits for PWM precision. This value sets PWM counting upper limit and it's expressed as decimal value. This limit will be applied to all 6 PWM pins.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach, shared

def setup() :
    attach.process(loop)
    
def loop() :
    setPwmLimit(512)
    while True:
        print "fade in"
        # count from 0 to 255 by 5
        for i in range(0,512):
            pwmWrite(19,i)
            pwmWrite(20,i)
            pwmWrite(21,i)
            delay(3)
        print "fade out"    
        for i in range(0,512):
            pwmWrite(19,512-i)
            pwmWrite(20,512-i)
            pwmWrite(21,512-i)
            delay(3)
```
***
## setPwmPeriod0(period) and setPwmPeriod1(period)
Sets specific period frequencies on two different PWM banks. PWM0 bank refers to pins : 19,20,21 and PWM1 bank refers to pins : 22,23,24. See setPwmPeriod(period) function for more details.
***
## setPwmLimit0(limit) and setPwmLimit1(limit)
Sets specific PWM limit precision on two different PWM banks. PWM0 bank refers to pins : 19,20,21 and PWM1 bank refers to pins : 22,23,24. See setPwmLimit(limit) function for more details.
***
## attachInterrupt(pin, mode, callback) and detachInterrupt(pin)
Attaches signal interrupt on pin and calls given function each time when signal condition is fulfilled. Signal can fire interrupt on these conditions : signal is HIGH, signal is LOW, signal CHANGE, signal RISING and signal FALLING. There can be 8 interruptions declared. If you want to stop interruption on pin call detachInterruption(pin) function.
Callback function that is provided will be filled in option by integer type of signal change that occurred. Use interruptType[iType] to decode integer in human readable format : RISING, FALLING,...

Comming soon...

# This is attached callback to interrupt
Comming soon...