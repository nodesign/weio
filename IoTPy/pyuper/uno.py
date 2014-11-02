from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pinouts import UNO_PINOUT


class UNO(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, UNO_PINOUT, serial_port)
