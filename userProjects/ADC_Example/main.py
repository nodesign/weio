# -*- coding: utf-8 -*- 
"""
UPER - ADC example 
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
commands = [['setSecondary',[30]],
            ['setSecondary',[22]],
            ['pwm0_begin',[100]]
            ]

serial_port = "/dev/ttyACM1"
ser = serial.Serial(
    port = serial_port,
    baudrate = 115200,
    parity = serial.PARITY_ODD,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 0.1
    )

print "Starting UPER"
for command in commands:
    UPER( command[0], command[1] )

i = 0
while True:
    UPER( 'analogRead',[3])
    sleep( 0.1 )
    adcstr = ser.readline()
#    print adcstr
    adcsplit = re.split(', |,|\( |\(|\)', adcstr)
#    print adcsplit
    print int(adcsplit[2],0)
    UPER( 'pwm0_set', [2, int(adcsplit[2],0)/11])
    #UPER( 'pwm0_set', [2,])
    
# EOF