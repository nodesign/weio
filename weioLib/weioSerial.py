import serial, os
from weioLib.weio import initSerial

class Serial:
    def __init__(self, port='/dev/ttyACM1', baudrate=115200, timeout=1):
        if (port is '/dev/ttyACM1'):
            # Switch GPIO to UART on WeIO, this is not necessary if some other port is asked
            initSerial()
        self.serial = serial.Serial(port, baudrate, timeout=timeout)

# Serial ports
def listSerials():
    ser = []
    dirs = os.listdir("/dev")
    for a in range(len(dirs)):
        if ("tty" in dirs[a]):
            #print dirs[a]
            ser.append(dirs[a])
    return ser