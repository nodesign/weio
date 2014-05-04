"""
Simple ADC value reading example with IoTPy.
"""
from time import sleep
from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.adc import ADC
from IoTPy.pyuper.utils import IoTPy_APIError, die

try:
    u = IoBoard()
except IoTPy_APIError, e: # seems can't establish connection with the board
    details = e.args[0]
    die(details)

try: # let's try to attach ADC object to non ADC pin
    a = u.get_pin(ADC, 27)
except IoTPy_APIError, e: # got an exception, pin capabilities must be different from requested
    details = e.args[0]
    print details

with u.get_pin(ADC, 24) as adc_pin:
    for i in range(10):
        val = adc_pin.read()
        print "RAW ADC value:", val,
        voltage = 5.0/1024 * val
        print "| Voltage:", voltage, "V"
        sleep(0.1)