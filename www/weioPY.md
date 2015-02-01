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

### digitalWrite(pin, value)
Sets voltage to +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be : 
* HIGH = +3.3V 
* LOW = Ground.

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
*Note : Before writing a port value, the port must be configured. See __portMode__ for more details.*

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
*Note : Before reading a port value, the port must be configured. See __portMode__ for more details.*

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
Pulse Width Modulation (PWM) is available on 6 pins from 18 to 23 and has a 16bits resolution. By default WeIO sets PWM frequency at 1kHz and it's value is expressed as percent of duty cycle from 0-100%.
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

### tone(pin, frequency, duration=0)
Generates a square wave of the specified frequency (and 50% duty cycle) on a pin. A duration can be specified, otherwise the wave continues until a call to noTone(). The pin can be connected to a piezo buzzer or other speaker to play tones. Tone function can be used only on PWM pins on WeIO (18,19,20,21,22,23)

```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    f = 0
    while True:
        tone(23, f)
        f+=1
        print "freq = ", f
        if (f>3000):
            f = 0
        delay(20)
```

### noTone(pin)
Stops the generation of a square wave triggered by tone(). Has no effect if no tone is being generated.
```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    tone(23, 1500)
    delay(3000)
    noTone(23)
```

Time
----
### millis()
Returns the number of milliseconds since the user program began running on the WeIO board.


### delay(milliseconds)
Pauses the program for the amount of time (in miliseconds) specified as parameter. (There are 1000 milliseconds in a second.)
from weioLib.weio import *

```python
def setup() :
    
    # Attaches blinky function to infinite loop
    attach.process(blinky)

def blinky() :
    
    while True:
        
        # write HIGH value to digital PINS 18, 19 & 20
        digitalWrite(18, HIGH) # red led
        digitalWrite(19, HIGH) # green led
        digitalWrite(20, HIGH) # blue led
        
        # wait 100ms
        delay(100)
        
        # write LOW value to digital PINS 18, 19 & 20
        digitalWrite(18, LOW) # red led
        digitalWrite(19, LOW) # green led
        digitalWrite(20, LOW) # blue led
        
        # wait 100ms
        delay(100)
```
Calculation
-----------
### constrain(x, a, b)
Constrains a number to be within a range.
```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    val = analogRead(24)
    # constrain values between 300 & 500
    p = constrain(val, 300,500)
    print p
```

### proportion(value, fromLow, fromHigh, toLow, toHigh)
Re-maps a number from one range to another. That is, a value of fromLow would get mapped to toLow, a value of fromHigh to toHigh, values in-between to values in-between, etc. Does not constrain values to within the range, because out-of-range values are sometimes intended and useful. The constrain() function may be used either before or after this function, if limits to the ranges are desired. It returns floating point number. Proportion is called map() in Arduino jargon but as this word is already reserved in Python in WeIO is called proportion()

```python
from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    val = analogRead(24)
    
    p = proportion(val, 300,500, 0,255)
    print p
```

WeIO info
---------
### versionWeIO()
Returns actual version of WeIO software

Interfaces
----------

Serial port
-----------
### Serial(baudrate, port='/dev/ttyACM1', timeout=1)
This function initialize serial port interface on WeIO board and returns a pySerial object. All documentation and code that is written for pySerial can be used directly inside WeIO. Reason why we are using our weioSerial module instead of pySerial is that WeIO needs to execute a few operations to put pins 0 - RX and 1 - TX into serial port mode before initializing pySerial. Complete pySerial documentation can be found here : http://pyserial.sourceforge.net/pyserial_api.html

### listSerials()
List available serial ports on WeIO. By default there are 3 serial ports /dev/ttyACM1, /dev/ttyACM0, /dev/ttyATH0. Each of them has it's own function. ttyACM1 is WeIO serial port that is connected to pins 0-RX and 1-TX. ttyACM0 is reserved for communication with LPC processor and ttyATH0 is reserved for user console via micro USB (you should not touch these two ports).
WeIO has integrated drivers for the most common USB to serial devices so It's perfectly possible to connect some serial device over USB and communicate with it.

### read(size=1)
Performs reading of one byte (size=1 by default) from serial port. Size argument (optional) express number of bytes to read. If a timeout is set (for example in constructor of serial object) it may return less characters as requested. With no timeout it will block until the requested number of bytes is read.

### write(data)
Performs writing the string data to the serial port. 


I2C via SMBus
-------------
__Important note about I2C__ : To work properly, the I2C bus needs two external pull-up on both SDA and SCL line. The typical value for these pull-up is 4k7.

### SMBus()
WeIO uses SMBus interface to talk to i2c devices. All SMbus instructions are supported and all drivers written in Python for SMBus can be directly used inside WeIO. Only the most commonly used instructions will be documented here for all SMBus features please refer to official Python SMBus documentation.

As WeIO uses it's own port of SMBus interface SMBus is imported in your project by calling from weioLib.weioSmbus import SMBus. 
```python
from weioLib.weio import *
# Comment this line below and use WeIO implementation
# from smbus import SMBus
from weioLib.weioSmbus import SMBus

myI2C = SMBus()
```
As WeIO has only one i2c interface any argument that is passed to constructor regarding i2c port will be ignored.

### scan()
Scans i2c bus for all connected devices and returns their addresses inside an array. This function is not part of standard SMBus driver, it exists only in WeIO implementation.

```python
from weioLib.weio import *
from weioLib.weioSmbus import SMBus

def setup():
    attach.process(myProcess)
    
def myProcess():
    myI2C = SMBus()
    
    print "list i2c devices on the bus", myI2C.scan()
```
### read_byte(address)
Perform i2c read byte from given address

### write_byte(address, value)
Perform write one byte of data to given device address

### read_byte_data(address, command)
Perform read byte operation from given address of device and given command

### write_byte_data(address, command)
Perform write byte operation to given address of device and given command

SPI
---
WeIO has two SPI bus with the following pinout :
* SPI0 : pin2 : MOSI; pin3 : MISO; pin4 : SCK
* SPI1 : pin8 : MOSI; pin9 : MISO; pin5 : SCK
Since there's no dedicated chip select (CS) pin, the chip select must be managed with a digital IO.

Here's an example of the SPI initialization.
```python
from weioLib.weio import *
from weioLib.weioSPI import SPILib

mySPI = SPILib()
```
SPILib can take three arguments which are : port, divider and mode. By default, if no arguments are passed to the constructor, port=0, divider=1 and mode=0.
*Port* specify the SPI bus number (0 or 1). *Divider* allow to divide the default SPI frequency (2MHz / *divider*). *Mode* specify the behavior of polarity and phase of the SCK signal, as described here : http://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus#Mode_numbers

### read_byte()
Read one byte on the SPI bus

### write_byte(value)
Write one byte on the SPI bus

### read_byte_data(cmd)
This command will write the byte sepcified by **cmd** and read the value returned by the device.

### write_byte_data(cmd, val)
This command will write two bytes (**cmd** and **val**). 

### read_word_data(cmd)
This command write a byte specified by *cmd* and read a word (two bytes) from the device.

### write_word_data(cmd, val)
This command write a byte specified by *cmd* followed by a word specified by *val*.

### read_block_data(cmd)
This command write the *cmd* byte and then read 32 bytes from the device. The returned value is a *list*. This command is useful for accessing memory devices.

### write_block_data(cmd, vals)
This command write the *cmd* byte followed by the bytes contained in *vals*. *vals* must be a *list*. 
