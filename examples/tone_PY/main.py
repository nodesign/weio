#######################################
#                                     #
#      HOW TO HAVE TONE ON WEIO       #
#                                     #
#######################################


# Description: This example shows how to generates a square wave of the
#              specified frequency (and 50% duty cycle) on a pin. There
#              are 6 pwm pins on weio (23, 22, 21, 20, 19, 18).
#              A duration can be specified, otherwise the wave continues 
#              until a call to notone(pin). The pin can be connected to a
#              piezo buzzer or other speaker to play tones.
# syntax = tone(pin, hertz, duration)  

from weioLib.weio import * 

def setup():
    # attaches myTone function to infinite loop
    attach.process(myTone)
    
def myTone():
    # init variable freq
    freq = 0
    # create infinite loop
    while True:
        # get tone with "freq" frequency on pin 23
        tone(23, freq)
        # increment freq variable
        freq = freq+1
        # print frequency on the console
        print "Frequency = ", freq , "Hz"
        # wait 100ms
        delay(100)
