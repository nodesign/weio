# -*- coding: utf-8 -*- 
"""
UPER - RegisterRead example 
"""
import serial
import re
from types import *
from time import sleep

def UPER( command, params ):
    outstr = command + '(' + ','.join(str(c) for c in params) + ')'
    print "====",outstr
    ser.write( outstr )
    
###### main ######

serial_port = "/dev/ttyACM1"
ser = serial.Serial(
    port = serial_port,
    baudrate = 115200,
    parity = serial.PARITY_ODD,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 0.1
    )

UPER( 'registerRead', [0x3f4])
regstr = ser.readline()
print regstr

# EOF