# -*- coding: utf-8 -*- 
"""
UPER - PWM example 
"""
import serial
from types import *
from time import sleep

def UPER( command, params ):
    outstr = command + '(' + ','.join(str(c) for c in params) + ')'
    print "====",outstr
    ser.write( outstr )
    
###### main ######
commands = [['setSecondary',[29]],
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
    while i < 100:
        i += 1
        UPER( 'pwm0_set', [2, i])
        sleep( 0.02 )
    print "Day :-)", i
    sleep( 0.5 )
    
    while i >= 1:
        i -= 1
        UPER( 'pwm0_set', [2, i])
        sleep( 0.02 )
    print "Night :-(", i
    sleep( 0.5 )
    #raw_input(">>")
# EOF
