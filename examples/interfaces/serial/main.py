#######################################
#                                     #
#  Serial port read, write with WeIO  #
#                                     #
#######################################

from weioLib.weio import *
from weioLib.weioSerial import Serial, listSerials

def setup():
    # making two indipendant processes. One that drives with pwm LEDs
    # another that writes and reads from serial port
    attach.process(fadeInOut)
    attach.process(UART)
    
def fadeInOut():
    # defining infinite loop
    while True:
        # count from 0 to 100 % 
        for i in range(0,100):
            # change PWM duty cycle to i
            pwmWrite(18,i)
            pwmWrite(19,i)
            pwmWrite(20,i)
            
        # count from 0 to 100 % 
        for i in range(0,100):
            # change PWM duty cycle to 100-i
            pwmWrite(18,100-i)
            pwmWrite(19,100-i)
            pwmWrite(20,100-i)

def UART():
    # list available serial ports in WeIO
    print listSerials()
    # open WeIO serial port that is attached to pins 0-RX and 1-TX
    # initSerial function return python serial object (pyserial library)
    # it's defined with (path, baud rate, timeout-optional 1 by default)
    ser = Serial(115200)
    
    i = 0
    while True:
        ser.write(str(i))
        ser.write(" - Hello, World!\r\n")
        i+=1
        # print what comes in
        data = "" #ser.read(1)
        n = ser.inWaiting() #look if there is more 
        if n:                                                                 
            data = data + ser.read(n)#and get as much as possible
            print data
        delay(100)