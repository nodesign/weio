from types import IntType

from IoTPy.pyuper.utils import IoTPy_IOError, IoTPy_ThingError, IoTPy_APIError, errmsg


class I2C:
    def __init__(self, board, port = 0, pins = []):
        self.board = board
        self.port = port
        self.pins = pins
        self.board.uper_io(0, self.board.encode_sfp(40, []))

    def __enter__(self):
        return self

    def transaction(self, address, write_data, read_length, ignore_error=False):
        try:
            result = self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(41, [address, write_data, read_length])))
        except IoTPy_APIError:
            errmsg("UPER API: I2C bus not connected.")
            raise IoTPy_IOError("I2C bus not connected.")
        if type(result[1][0]) == IntType and not ignore_error:
            errmsg("UPER Interface: I2C device with address %#x returned error code %#x.", address, result[1][0] )
            raise IoTPy_ThingError("I2C slave reading error.")
        else:
            return result[1][0]

    def __exit__(self, exc_type, exc_value, traceback):
        self.board.uper_io(0, self.board.encode_sfp( 42, []))

