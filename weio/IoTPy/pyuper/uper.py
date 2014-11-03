from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pinouts import UPER1_PINOUT


class UPER1(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, UPER1_PINOUT, serial_port)
