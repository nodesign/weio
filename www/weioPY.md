Python
======
Boilerplate
-----------
### Python boilerplate
This is "Hello world" program written in Python. It prints "hello world" on console and blinks LED.
```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello world")

```

Digital I/O
-----------
### digitalWrite(pin, value)
Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground.

```python
from weioLib.weio import *

def setup() :
    attach.process(blinky)

def blinky() :
    while True:
        digitalWrite(20, HIGH)
        delay(500)
        digitalWrite(20, LOW)
        delay(500)
```
### digitalRead(pin)
Reads actual voltage on corresponding pin. WeIO inputs are 5V TOLERANT. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected. If only digitalRead function is provided, pin will be in HIGH Z state. See pinMode(pin,mode) function for more options.

```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    pin = 0
    while True:
        a = digitalRead(pin)
        print "Value on the pin ", pin, " = ", a
        delay(100)
```
### portWrite(port, value)
PortWrite allows faster manipulation of the i/o pins of the microcontroller. That means that you can send one byte of data that will be directly exported on 8 pins in form of HIGH and LOW signals instead sending them one by one. There are 4 available ports on the board. Port 0 for pins 0-7, Port 1 for pins 8-15, Port 2 for pins 16-23 and Port 3 for pins 24-31
This example will blink LEDs. There is only one instruction that is called instead calling digitalWrite for each pin separately 
```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    portMode(2, OUTPUT)
    while True:
        # this is direct port manipulation
        # instead calling digitalWrite for each pin
        portWrite(2, 227)
        delay(500)
        portWrite(2, 255)
        delay(500)
```

### portRead(port)
PortRead allows faster manipulation of the i/o pins of the microcontroller. That means that you can read one byte of data instead reading them one by one using digitalRead function. There are 4 available ports on the board. Port 0 for pins 0-7, Port 1 for pins 8-15, Port 2 for pins 16-23 and Port 3 for pins 24-31
```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    portMode(0, INPUT)
    while True:
        print(portRead(0))
        delay(20)
```
### portMode(port, mode)
Sets states on one port (8 pins) at the same time. There are 4 available ports on the board. Port 0 for pins 0-7, Port 1 for pins 8-15, Port 2 for pins 16-23 and Port 3 for pins 24-31 Available modes are : PULL_UP, PULL_DOWN, INPUT and OUTPUT
This function activates pullups, pulldowns or high Z state (INPUT only) on declared ports. 

```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    portMode(0, INPUT)
    while True:
        print(portRead(0))
        delay(20)
```


### pinMode(pin, mode)

Sets state on the pin. Available modes are : PULL_UP, PULL_DOWN, INPUT and OUTPUT
This function activates pullups, pulldowns or high Z state (INPUT only) on declared pins. If pinMode function is not called and digitalRead is performed pin state will be in high Z by default

```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    
    while True :
        # setting pull up resistor, result will print 1
        pinMode(0, PULL_UP)
        for a in range(0,5):
            print digitalRead(0)
            delay(100)
            
        # setting pull down resistor, result will print 0
        pinMode(0, PULL_DOWN)
        for a in range(0,5):
            print digitalRead(0)
            delay(100)
```

Analog I/O
----------
### analogRead(pin, callback)
Reads input on specified Analog to Digital Convertor. 8 ADC are available on pins from 24 to 31. Output is 10bits resolution or expressed in decimal numbers from 0-1023. All WeIO pins are 5V tolerant except ADC pins when they are reading analog signals. Be careful not to administrate more than 3.3V on these pins when performing analog read.

```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    pin = 31
    while True:
        print "analogRead pin ",pin," = ",analogRead(pin)
        # give peace a chance and not push cpu to 100%
        delay(100)
```

### pwmWrite(pin, value)
Pulse with modulation is available at 6 pins from 18 to 23 and has 16bits of precision. By default WeIO sets PWM frequency at 1000us and it's value is expressed as percent of duty cycle from 0-100%. 
```python
from weioLib.weio import *

def setup():
    # attaches "fadeInOut" fuction to infinite loop
    attach.process(fadeInOut)
    
def fadeInOut():
    # create infinite loop
    while True:
        
        # print "fade in" in the console
        print "fade in"
        # count from 0 to 100 % 
        for i in range(0,100):
            # change PWM duty cycle to i
            pwmWrite(20,i)
            
        # print "fade out" in the console
        print "fade out"  
        # count from 0 to 100 % 
        for i in range(0,100):
            # change PWM duty cycle to 100-i
            pwmWrite(20,100-i)
```

### setPwmPeriod(period)
Overrides default value of 1000us to set new period frequency for whole 6 PWM pins.

WeIO info
=========
### versionWeIO
Gets actual version of WeIO software

Interfaces
==========

Serial port
-----------
### listSerials()
List available serial ports on WeIO. By default there are 3 serial ports /dev/ttyACM1, /dev/ttyACM0, /dev/ttyATH0. Each of them has it's own function. ttyACM1 is WeIO serial port that is connected to pins 0-RX and 1-TX. ttyACM0 is reserved for communication with LPC processor and ttyATH0 is reserved for user console via micro USB (you should not touch these two ports).
WeIO has integrated drivers for the most common USB to serial devices so It's perfectly possible to connect some serial device over USB and communicate with it.


