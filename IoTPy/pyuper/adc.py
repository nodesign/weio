from IoTPy.pyuper.utils import IoTPy_APIError, errmsg


class ADC:
    HIGH_Z = 0

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin][0] & self.board.cap_adc:
            self.logical_pin = self.board.pinout[pin][1][0]
        else:
            errmsg("UPER API: Pin No:%d is not an ADC pin.", pin)
            raise IoTPy_APIError("Trying to assign ADC function to non ADC pin.")
        self.adc_pin = self.board.pinout[pin][1][1]
        self.board.uper_io(0, self.board.encode_sfp(3, [self.logical_pin, self.HIGH_Z]))
        self.board.uper_io(0, self.board.encode_sfp(2, [self.logical_pin])) # set secondary pin function
        self.pull = self.HIGH_Z
        self.primary = False

    def read(self):
        return self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(10, [self.adc_pin])))[1][1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

