from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pinouts import LEONARDO_PINOUT


class Leonardo(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, Leonardo_PINOUT, serial_port)
