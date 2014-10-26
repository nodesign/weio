from IoTPy.pyuper.utils import IoTPy_APIError, errmsg
from IoTPy.pyuper.pinouts import CAP_ADC

from IoTPy.core.adc import ADC


class UPER1_ADC(ADC):
    """
    UPER1_ADC (Analog to Digital Converter) pin module.

    :param board: IoBoard to which the pin belongs to.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param pin: ADC capable pin number.
    :type pin: int
    """

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin].capabilities & CAP_ADC:
            self.logical_pin = self.board.pinout[pin].pinID
        else:
            errmsg("UPER API: Pin No:%d is not an ADC pin.", pin)
            raise IoTPy_APIError("Trying to assign ADC function to non ADC pin.")
        self.adc_pin = self.board.pinout[pin].extra[0]
        self.board.uper_io(0, self.board.encode_sfp(3, [self.logical_pin, 0]))  # set GPIO to HIGH_Z
        self.board.uper_io(0, self.board.encode_sfp(2, [self.logical_pin]))  # set secondary pin function
        self.primary = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def read(self):
        """
        Read fractional analog value

        :return: A normalized analog value from 0.0 (min) to 1.0 (max)
        :rtype: float
        """
        return self.read_raw()/1023.0

    def read_raw(self):
        """
        Read ADC value

        :return: Raw ADC value.
        :rtype: int
        """
        return self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(10, [self.adc_pin])))[1][1]
