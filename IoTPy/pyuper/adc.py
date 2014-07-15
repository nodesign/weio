from IoTPy.pyuper.gpio import GPIO
from IoTPy.pyuper.utils import IoTPy_APIError, errmsg
from IoTPy.pyuper.pinouts import CAP_ADC

class ADC:
    """
    ADC (Analog to Digital Converter) pin module.

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
        self.board.uper_io(0, self.board.encode_sfp(3, [self.logical_pin, GPIO.HIGH_Z]))
        self.board.uper_io(0, self.board.encode_sfp(2, [self.logical_pin])) # set secondary pin function
        self.primary = False

    def read(self):
        """
        Read analog value. The maximum value might depend on the ADC resolution: for 10bit ADC it is 1023,
        for 8bit ADC - 255, etc.

        :return: Measured ADC value.
        :rtype: int
        """
        return self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(10, [self.adc_pin])))[1][1]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

