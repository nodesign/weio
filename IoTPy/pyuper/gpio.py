from IoTPy.pyuper.utils import IoTPy_APIError, errmsg


class GPIO:
    PULL_UP = 4
    PULL_DOWN = 2
    HIGH_Z = 0
    INPUT = 3
    OUTPUT = 1

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin][0] & self.board.cap_gpio:
            self.logical_pin = self.board.pinout[pin][1][0]
        else:
            errmsg("UPER API: Pin No:%d is not GPIO pin.", pin)
            raise IoTPy_APIError("Trying to assign GPIO function to non GPIO pin.")
        self.direction = self.INPUT
        self.pull = self.PULL_UP
        self.board.uper_io(0, self.board.encode_sfp(1, [self.logical_pin])) # set primary
        self.primary = True
        self.input_pullmode = self.PULL_UP

    def mode(self, pin_mode):
        if pin_mode in [self.HIGH_Z, self.PULL_UP, self.PULL_DOWN, self.OUTPUT]:
            if pin_mode != self.OUTPUT:
                self.direction = self.INPUT
                self.input_pullmode = pin_mode
                self.pull = pin_mode
            else:
                self.direction = self.OUTPUT
            self.board.uper_io(0, self.board.encode_sfp(3, [self.logical_pin, pin_mode]))
        else:
            errmsg("UPER API: pinMode - Illegal pin mode - %d", pin_mode)
            raise IoTPy_APIError("Illegal pin mode.")

    def write(self, value):
        if self.direction != self.OUTPUT:
            self.mode(self.OUTPUT)
        self.direction = self.OUTPUT
        self.board.uper_io(0, self.board.encode_sfp(4, [self.logical_pin, value]))

    def read(self):
        if self.direction != self.INPUT:
            self.mode(self.input_pullmode)
            self.pull = self.input_pullmode
        self.direction = self.INPUT
        return self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(5, [self.logical_pin])))[1][1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
