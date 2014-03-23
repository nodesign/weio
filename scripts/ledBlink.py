#!/usr/bin/python

import sys
import time
import signal

# Open AP and STA led control files
apBright = open("/sys/class/leds/weio:green:ap/brightness","w")
staBright = open("/sys/class/leds/weio:green:sta/brightness","w")

def blink(delay):
    # Turn LEDs ON
    apBright.write(str(1))
    apBright.flush()
    
    staBright.write(str(1))
    staBright.flush()

    time.sleep(delay)

    # Turn LEDs OFF
    apBright.write(str(0))
    apBright.flush()
    
    staBright.write(str(0))
    staBright.flush()

    time.sleep(delay)

def out(signum = None, frame = None):
    # Turn LEDs OFF
    apBright.write(str(0))
    staBright.write(str(0))
    
    # Close the files
    apBright.close()
    staBright.close()

    # Exit the program
    sys.exit()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, out)

    delay = sys.argv[1]

    try:
        while True:
            blink(float(delay))
    except (KeyboardInterrupt):
            out()

