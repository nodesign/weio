from types import IntType

from IoTPy.pyuper.utils import IoTPy_IOError, IoTPy_ThingError, IoTPy_APIError, errmsg


class I2C:
    """
    I2C communication module.

    :param board: IoBoard with I2C capability.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param port: UNDOCUMENTED
    :type port: int
    :param pins: UNDOCUMENTED
    """

    def __init__(self, board, port = 0, pins = []):
        self.board = board
        self.port = port
        self.pins = pins
        self.board.uper_io(0, self.board.encode_sfp(40, []))

    def __enter__(self):
        return self

    def scan(self):
        """
        Scan I2C interface for connected devices.

        :return: A list of active I2C device addresses.
        :rtype: list
        """
        dev_list = []
        for address in xrange(1,128):
            try:
                result = self.board.uper_io(1, self.board.encode_sfp(41, [address, '', 0]))
                if result[-1] == 'X':
                    dev_list.append(address)
            except IoTPy_APIError:
                errmsg("UPER API: I2C bus not connected.")
                raise IoTPy_IOError("I2C bus not connected.")
        return dev_list

    def transaction(self, address, write_data, read_length, ignore_error=False):
        """
        Perform I2C data transaction.

        I2C data transaction consists of (optional) write transaction, followed by (optional) read transaction.

        :param address: I2C device address.
        :type address: int
        :param write_data: A byte sequence to be transmitted. If write_data is None, no write transaction will be executed.
        :type write_data: str
        :param read_length: A number of bytes to be received. If read_length is 0, no read trasaction will be executed.
        :type read_length: int
        :param ignore_error:
        :type ignore_error: bool
        :return: Received data or I2C communication error code.
        :rtype: str or int
        :raise: IoTPy_APIError, IoTPy_ThingError
        """
        try:
            result = self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(41, [address, write_data, read_length])))
        except IoTPy_APIError:
            errmsg("UPER API: I2C bus not connected.")
            raise IoTPy_IOError("I2C bus not connected.")
        if type(result[1][0]) == IntType and not ignore_error:
            errmsg("UPER Interface: I2C device with address %#x returned error code %#x.", address, result[1][0])
            raise IoTPy_ThingError("I2C slave reading error.")
        else:
            return result[1][0]

    def __exit__(self, exc_type, exc_value, traceback):
        self.board.uper_io(0, self.board.encode_sfp( 42, []))

