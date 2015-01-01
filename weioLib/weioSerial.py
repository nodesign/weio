import serial, os
from weioLib.weio import initSerial

def Serial(baudrate, port='/dev/ttyACM1', timeout=1):
    if (port is '/dev/ttyACM1'):
        # Switch GPIO to UART on WeIO, this is not necessary if some other port is asked
        initSerial()
    return serial.Serial(port, baudrate, timeout=timeout)

# Serial ports
def listSerials():
    ser = []
    dirs = os.listdir("/dev")
    for a in range(len(dirs)):
        if ("tty" in dirs[a]):
            #print dirs[a]
            ser.append(dirs[a])
    return ser