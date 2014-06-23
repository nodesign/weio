from types import IntType

from IoTPy.pyuper.utils import IoTPy_IOError, IoTPy_ThingError, IoTPy_APIError, errmsg


class SPI:
    """
    SPI communication module.

    :param board: IoBoard with SPI capability.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param port: SPI module number. Optional, default 0 (SPI0 module).
    :type port: int
    :param divider: SPI clock divider. SPI clock speed will be maximum clock speed (2MHz) divided by this value. Optional, default 1.
    :type divider: int
    :param mode: Standard SPI mode number (0-3). Optional, default 0.
    :type mode: int
    """

    def __init__(self, board, port=0, divider=1, mode=0):
        self.board = board
        self.port = port
        self.divider = divider
        self.mode = mode
        if self.port == 1:
            self.board.uper_io(0, self.board.encode_sfp(2, [4]))
            self.board.uper_io(0, self.board.encode_sfp(2, [5]))
            self.board.uper_io(0, self.board.encode_sfp(2, [11]))
            self.board.uper_io(0, self.board.encode_sfp(30, [self.divider, self.mode]))
        elif self.port == 0:
            self.board.uper_io(0, self.board.encode_sfp(2, [12]))
            self.board.uper_io(0, self.board.encode_sfp(2, [13]))
            self.board.uper_io(0, self.board.encode_sfp(2, [14]))
            self.board.uper_io(0, self.board.encode_sfp(20, [self.divider, self.mode]))
        else:
            errmsg("UPER API: Wrong SPI port number.", self.port)
            raise IoTPy_APIError("SPI port must be 0 or 1, trying to assign something else.")


    def __enter__(self):
        return self

    def transaction(self, write_data, read_from_slave=False):
        """
        Perform SPI data transaction.

        :param write_data: Data to be shifted on MOSI line.
        :type write_data: str
        :param read_from_slave: Flag indicating whether the data received on MISO line should be ignored or not. Optional, default False.
        :type read_from_slave: bool

        :return: Data received on MISO line, if read_from_slave is True.
        :rtype: str
        """
        result = self.board.decode_sfp(self.board.uper_io(read_from_slave, self.board.encode_sfp(21 + self.port * 10, [write_data, read_from_slave])))
        if read_from_slave:
            return result[1][0]

    def __exit__(self, exc_type, exc_value, traceback):
        self.board.uper_io(0, self.board.encode_sfp( 22 + self.port * 10, []))
        if self.port:
            self.board.uper_io(0, self.board.encode_sfp(1, [4]))  # set pin primary function
            self.board.uper_io(0, self.board.encode_sfp(1, [5]))
            self.board.uper_io(0, self.board.encode_sfp(1, [11]))
        else:
            self.board.uper_io(0, self.board.encode_sfp(1, [12]))  # set pin primary function
            self.board.uper_io(0, self.board.encode_sfp(1, [13]))
            self.board.uper_io(0, self.board.encode_sfp(1, [14]))


