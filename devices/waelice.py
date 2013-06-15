import platform

if (platform.machine() == 'mips') :
    import i2c

    bus = i2c.I2cBus(0)
    addr = 0x03

def setColor(r,g,b) :
    if (platform.machine() == 'mips') :
        global addr
        dev = bus[addr]
        dev[2]
        dev[r]
        dev[g]
        dev[b]
    else :
        print "setting color : " + str(r) + " " + str(g) + " " + str(b)
