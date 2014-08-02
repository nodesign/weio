Boilerplate
-----------
### Python boilerplate
This is "Hello world" program written in Python. It prints "hello world" on console and blinks LED.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcess)

def myProcess():
    print("Hello world")
    pause = 100
    while True:
        digitalWrite(20, HIGH)
        delay(pause)
        digitalWrite(20, LOW)
        delay(pause)
```
Digital I/O
-----------
### digitalWrite(pin, value)
Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcess)
    
def myProcess():
    while True :
        digitalWrite(18,LOW)
        delay(70)
        digitalWrite(20,HIGH)
        delay(70)
        digitalWrite(19,LOW)
        delay(70)
        digitalWrite(18,HIGH)
        delay(70)
        digitalWrite(20,LOW)
        delay(70)
        digitalWrite(19,HIGH)
        delay(70)

```
### digitalRead(pin)
Reads actual voltage on corresponding pin. WeIO board is 5V TOLERANT. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected. If only digitalRead function is provided, pin will be in HIGH Z state. If pinMode function is not called and digitalRead is performed pin state will be in high Z by default. See [inputMode(pin,mode)](http://github.com/nodesign/weio/wiki/Weio-GPIO-API-using-UPER-board#inputmodepin-mode) function for more options.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach
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
### pinMode(pin, mode)
Sets pin mode for digitalRead purpose. Available modes are : INPUT_HIGHZ, INPUT_PULLDOWN, INPUT_PULLUP, OUTPUT
This function activates pullups, pulldowns, high Z state or output mode on declared pins. If pinMode function is not called and digitalRead is performed pin state will be in high Z by default
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach
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
Analog I/O
-----------
### analogRead(pin)
Reads input on specified Analog to Digital Convertor. ADC is available on pins from 25 to 32 Output is 10bits resolution or from 0-1023. ATTENTION when used ADC voltage tolerance is 3.3V maximum. ADC circuit is NOT 5V tolerant
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcess)
    
def myProcess():
    pin = 31
    while True:
        print "analogRead pin ",pin," = ",analogRead(pin)
        delay(20)

```
### pwmWrite(pin, value)
Pulse with modulation is available at 6 pins from 19-24 and has 16bits of precision. By default WeIO sets PWM frequency at 20000ms and 8bit precision or from 0-255. This setup is well situated for driving LED lighting. Precision and frequency can be changed separately by calling additional functions for other uses : setPwmPeriod and setPwmLimit. PWM can also drive two different frequencies on two separate banks of 3 pins. For this feature look functions : setPwmPeriod0, setPwmPeriod1, setPwmLimit0 and setPwmLimit1.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup() :
    attach.process(loop)
    
def loop() :
    
    while True:
        print "fade in"
        # count from 0 to 255 
        for i in range(256):
            pwmWrite(18,i)
            pwmWrite(19,i)
            pwmWrite(20,i)
            delay(3)
            
        print "fade out"    
        for i in range(256):
            pwmWrite(18,255-i)
            pwmWrite(19,255-i)
            pwmWrite(20,255-i)
            delay(3)
```

### setPwmPeriod(period)
Overrides default value of 1000us to set new period value for whole 6 PWM pins. Period value must be superior than 0 and inferior than 65535.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup() :
    attach.process(loop)
    
def loop() :

    setPwmPeriod(500)
    while True:
        print "fade in"
        # count from 0 to 255 
        for i in range(256):
            pwmWrite(18,i)
            pwmWrite(19,i)
            pwmWrite(20,i)
            delay(3)
            
        print "fade out"    
        for i in range(256):
            pwmWrite(18,255-i)
            pwmWrite(19,255-i)
            pwmWrite(20,255-i)
            delay(3)
```

### setPwmLimit(limit)
Overrides default limit of 8bits for PWM precision. This value sets PWM counting upper limit and it's expressed as decimal value. This limit will be applied to all 6 PWM pins.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach

def setup() :
    attach.process(loop)

def loop() :
    setPwmLimit(512)
    while True:
        print "fade in"
        # count from 0 to 255 by 5
        for i in range(513):
            pwmWrite(19,i)
            pwmWrite(20,i)
            pwmWrite(21,i)
            delay(3)
        print "fade out"
        for i in range(0,513):
            pwmWrite(19,512-i)
            pwmWrite(20,512-i)
            pwmWrite(21,512-i)
            delay(3)
```

SPI protocol
------------
### initSPI(port, divider=1, mode=0)
Returns SPI object on specified port. There are 2 SPI ports on WeIO board. Port 0 on pins 2(MOSI),3(MISO),4(SCK) and Port 1 on pins 8(MOSI),9(MISO),10(SCK).
Optional parameters :
Divider is SPI clock divider. SPI clock speed will be maximum clock speed (2MHz) divided by this value. Optional, default 1.
Mode is SPI mode number defining clock polarity and clock edge. See SPI specification for more details. There are 4 possible modes (0-3)
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach
import struct

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("SPI starts")
    spi = initSPI(0) # init SPI on port 0 (pins : 2,3,4)
    chipSelect = 5
    while True :
        # run thru all 8 outputs of 74HC595
        b = 0
        for i in range(9):
            digitalWrite(chipSelect, LOW)
            spi.transaction(struct.pack("B", b))
            digitalWrite(chipSelect, HIGH)
            b = 1
            b = b<<i
            delay(100)
```

### transaction(data, response = 0)
Sends byte/bytes of information and returns response if asked.
```python
from weioLib.weioIO import *
from weioLib.weioUserApi import attach
import struct

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("SPI starts")
    spi = initSPI(0) # init SPI on port 0 (pins : 2,3,4)
    chipSelect = 5
    while True :
        # run thru all 8 outputs of 74HC595
        b = 0
        for i in range(9):
            digitalWrite(chipSelect, LOW)
            spi.transaction(struct.pack("B", b))
            digitalWrite(chipSelect, HIGH)
            b = 1
            b = b<<i
            delay(100)
```


Interrupts
----------
### attachInterrupt(pin, mode, callback) 
Attaches signal interrupt on pin and calls given function each time when signal condition is fulfilled. Signal can fire interrupt on these conditions : signal is HIGH, signal is LOW, signal CHANGE, signal RISING and signal FALLING. There can be 8 interruptions declared. If you want to stop interruption on pin call detachInterruption(pin) function.
Callback function that is provided will be filled in option by integer type of signal change that occurred. Use interruptType[iType] to decode integer in human readable format : RISING, FALLING,...

Comming soon...

### detachInterrupt(pin)
Attaches signal interrupt on pin and calls given function each time when signal condition is fulfilled. Signal can fire interrupt on these conditions : signal is HIGH, signal is LOW, signal CHANGE, signal RISING and signal FALLING. There can be 8 interruptions declared. If you want to stop interruption on pin call detachInterruption(pin) function.
Callback function that is provided will be filled in option by integer type of signal change that occurred. Use interruptType[iType] to decode integer in human readable format : RISING, FALLING,...

Comming soon...
### This is attached callback to interrupt
Comming soon...