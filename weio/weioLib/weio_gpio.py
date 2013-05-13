import os

def pinMode(pin, dir) :
    """pinMode function defines if GPIO is in OUTPUT mode (actioner) or in INPUT mode (sensor)"""
    s_pin = str(pin)

    # if os.path.exists("/sys/class/gpio/export") :
    #        inputFile = open("/sys/class/gpio/export", "w")
    #        rep = inputFile.write(s_pin)
    #        inputFile.close()

    if os.path.exists("/sys/devices/virtual/gpio/gpio" + s_pin + "/direction") :
        inputFile = open("/sys/devices/virtual/gpio/gpio" + s_pin + "/direction", "w")
        rep = inputFile.write(dir)
        inputFile.close()
    else :
        print "WEIO says : pin " + str(pin) + " is busy or non existant"


def digitalWrite(pin, state) :
    """Digital write will set voltage +3.3V or Ground on corresponding pin. This function takes two parameters : pin number and it's state that can be HIGH = +3.3V or LOW = Ground"""

    s_pin = "/sys/devices/virtual/gpio/gpio" + str(pin) + "/value"
    if os.path.exists(s_pin) :
        inputFile = open(s_pin, "w")
        rep = inputFile.write(state)
        inputFile.close()
    else :
        print "WEIO says : pin " + str(pin) + " is not accessible, did you declare pinmode(pin, direction)?"
        
def digitalRead(pin) :
    """Digital read will read actual voltage on corresponding pin. There are two possible answers : 0 if pin is connected to the Ground or 1 if positive voltage is detected"""
    s_pin = "/sys/devices/virtual/gpio/gpio" + str(pin) + "/value"
    if os.path.exists(s_pin) :
        inputFile = open(s_pin, "r")
        rep = inputFile.read()
        return rep
    else :
        print "WEIO says : pin " + str(pin) + " is not accessible, did you declare pinmode(pin, direction)?"
        return None
