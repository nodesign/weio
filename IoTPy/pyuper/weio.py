from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.pinouts import WEIO_PINOUT


class WeIO(IoBoard):

    def __init__(self, serial_port=None):
        IoBoard.__init__(self, WEIO_PINOUT, serial_port)
