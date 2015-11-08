#######################################
#                                     #
#    HOW TO READ A PULSEIN ON WEIO    #
#                                     #
#######################################

# Descriptions: This example shows how to reads a pulse (either HIGH or LOW)
#               on a pin and get the length in microseconds or 0 if no
#               complete pulse was received within the timeout.
#
# Syntax: pulseIn(pin, value, timeout)
#
# pin : all pins availables
# mode : HIGH, LOW

from weioLib.weio import *

def setup():
    attach.process(myProcess)

def myProcess():
    while True:
        # Turn on the red LED while the pulse is read
        digitalWrite(18, LOW)
        # Read and input pulse
        time = pulseIn(23, LOW, 900000)
        # Print the value of pulse duration
        print "PulseIn duration = ", time
        # Turn off the red LED at the end of the reading
        digitalWrite(18, HIGH)
        # wait 500ms
        delay(500)