from IoTPy.pyuper.utils import IoTPy_APIError, errmsg
from IoTPy.pyuper.pinouts import CAP_GPIO

class GPIO:
    """
    GPIO (General Purpose Input and Output) pin module.

    :param board: IoBoard to which the pin belongs to.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param pin: GPIO pin number.
    :type pin: int
    :raise: IoTPy_APIError
    """

    PULL_UP = 4
    PULL_DOWN = 2
    HIGH_Z = 0
    INPUT = 3
    OUTPUT = 1

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin].capabilities & CAP_GPIO:
            self.logical_pin = self.board.pinout[pin].pinID
        else:
            errmsg("UPER API: Pin No:%d is not GPIO pin.", pin)
            raise IoTPy_APIError("Trying to assign GPIO function to non GPIO pin.")
        self.direction = self.INPUT
        self.pull = self.PULL_UP
        self.board.uper_io(0, self.board.encode_sfp(1, [self.logical_pin])) # set primary
        self.primary = True
        self.input_pullmode = self.PULL_UP

    def mode(self, pin_mode):
        """
        Set GPIO pin mode.

        :param pin_mode: GPIO pin mode: GPIO.OUTPUT, GPIO.PULL_UP, GPIO.PULL_DOWN or GPIO.HIGH_Z.
        :raise: IoTPy_APIError
        """
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
        """
        Write a digital value (0 or 1). If GPIO pin is not configured as output, set it's GPIO mode to GPIO.OUTPUT.

        :param value: Digital output value (0 or 1)
        :type value: int
        """
        if self.direction != self.OUTPUT:
            self.mode(self.OUTPUT)
        self.direction = self.OUTPUT
        self.board.uper_io(0, self.board.encode_sfp(4, [self.logical_pin, value]))

    def read(self):
        """
        Read a digital signal value. If GPIO pis in not configure as input, set it to GPIO.PULL_UP pin mode.

        :return: Digital signal value: 0 (LOW) or 1 (HIGH).
        :rtype: int
        """
        if self.direction != self.INPUT:
            self.mode(self.input_pullmode)
            self.pull = self.input_pullmode
        self.direction = self.INPUT
        return self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(5, [self.logical_pin])))[1][1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
