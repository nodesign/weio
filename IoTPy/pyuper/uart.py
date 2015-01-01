from IoTPy.pyuper.utils import IoTPy_IOError, IoTPy_APIError, errmsg

from IoTPy.core.uart import UART


class UPER1_UART(UART):
    """
    I2C communication module.

    :param board: IoBoard with I2C capability.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param port: I2C module number
    :type port: int
    """

    def __init__(self, board):
        self.board = board
        self.board.uper_io(0, self.board.encode_sfp(80, []))

    def __enter__(self):
        errmsg("here")
        return self
