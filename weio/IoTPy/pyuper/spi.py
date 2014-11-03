from IoTPy.pyuper.utils import IoTPy_APIError, errmsg

from IoTPy.core.spi import SPI


class UPER1_SPI(SPI):
    """
    SPI communication module.

    :param board: IoBoard with SPI capability.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param port: SPI module number. Optional, default 0 (SPI0 module).
    :type port: int
    :param divider: SPI clock divider. SPI clock speed will be maximum clock speed (2MHz) divided by this value. Optional, default 1.
    :type divider: int
    :param mode: Standard SPI mode number (SPI.MODE_0 to SPI.MODE_3). Optional, default SPI.MODE_0.
    :type mode: int
    """

    def __init__(self, board, port=0, divider=1, mode=SPI.MODE_0):
        divider = min(max(divider, 1), 256)

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

    def read(self, count, value=0):
        return self.transaction(chr(value)*count, True)

    def write(self, data):
        self.transaction(data, False)

    def transaction(self, write_data, read_from_slave=True):
        """
        Perform SPI data transaction.

        :param write_data: Data to be shifted on MOSI line.
        :type write_data: str
        :param read_from_slave: Flag indicating whether the data received on MISO line should be ignored or not. Optional, default True.
        :type read_from_slave: bool

        :return: Data received on MISO line, if read_from_slave is True.
        :rtype: str
        """
        res = self.board.uper_io(read_from_slave, self.board.encode_sfp(21 + self.port * 10, [write_data, int(read_from_slave)]))

        if res:
            return self.board.decode_sfp(res)[1][0]

    def __exit__(self, exc_type, exc_value, traceback):
        self.board.uper_io(0, self.board.encode_sfp(22 + self.port * 10, []))
        if self.port:
            self.board.uper_io(0, self.board.encode_sfp(1, [4]))  # set pin primary function
            self.board.uper_io(0, self.board.encode_sfp(1, [5]))
            self.board.uper_io(0, self.board.encode_sfp(1, [11]))
        else:
            self.board.uper_io(0, self.board.encode_sfp(1, [12]))  # set pin primary function
            self.board.uper_io(0, self.board.encode_sfp(1, [13]))
            self.board.uper_io(0, self.board.encode_sfp(1, [14]))
