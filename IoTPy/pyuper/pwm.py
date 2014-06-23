from IoTPy.pyuper.pinouts import CAP_PWM
from IoTPy.pyuper.utils import IoTPy_APIError, errmsg


PWM_PORT_RUNNING = [{'channels':0, 'period':0}, {'channels':0, 'period':0}]

class PWM:
    """
    PWM (Pulse Width Modulation) pin module.

    :param board: IoBoard to which the pin belongs to.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param pin: PWM pin number.
    :type pin: int
    :param polarity: Active (on) state signal level: 0 (LOW) or 1 (HIGH). Optional, default 1.
    :type polarity: int
    """

    _PWM_PORT_FUNCTIONS = [[50,51,52],[60,61,62]]
    _PWM_PORT_MAX = [0xffff, 0xffffffff]      #maxuint16, maxuint32

    def __init__(self, board, pin, polarity = 1):
        self.board = board
        if self.board.pinout[pin].capabilities & CAP_PWM:
            self.logical_pin = self.board.pinout[pin].pinID
        else:
            errmsg("UPER API: Pin No:%d is not a PWM pin.", pin)
            raise IoTPy_APIError("Trying to assign PWM function to non PWM pin.")
        self.pwm_port = self.board.pinout[pin].extra[0]
        self.pwm_pin = self.board.pinout[pin].extra[1]
        self.primary = True
        self.hightime = 0
        self.polarity = polarity
        PWM_PORT_RUNNING[self.pwm_port]['channels'] += 1
        if PWM_PORT_RUNNING[self.pwm_port]['channels'] == 1:
            self.period(10000)

    def period(self, period):
        """
        Set PWM period.

        :param period: PWM signal period in microseconds.
        :type period: int
        :raise: IoTPy_APIError
        """
        if 0 <= period <= self._PWM_PORT_MAX[self.pwm_port]:
            if PWM_PORT_RUNNING[self.pwm_port]['period'] != period:
                self.board.uper_io(0, self.board.encode_sfp(self._PWM_PORT_FUNCTIONS[self.pwm_port][0], [period]))
                PWM_PORT_RUNNING[self.pwm_port]['period'] = period
        else:
            errmsg("UPER API: PWM period for port %d can be only between 0-%d" % (self.pwm_port, self._PWM_PORT_MAX[self.pwm_port]))
            raise IoTPy_APIError("PWM period is out of range.")

    def width_us(self, hightime):
        """
        Set PWM high (on state) time.

        :param hightime: On state time in microseconds.
        :type hightime: int
        :raise: IoTPy_APIError
        """
        if self.primary:
            self.board.uper_io(0, self.board.encode_sfp(2, [self.logical_pin])) # set pin secondary function
            self.primary = False
        if 0 <= hightime <= PWM_PORT_RUNNING[self.pwm_port]['period']:
            self.hightime = hightime
            if self.polarity == 1:
                hightime = PWM_PORT_RUNNING[self.pwm_port]['period'] - hightime
            self.board.uper_io(0, self.board.encode_sfp(PWM._PWM_PORT_FUNCTIONS[self.pwm_port][1], [self.pwm_pin, hightime]))
        else:
            errmsg("UPER error: PWM high time is out of range on logical pin %d." % self.logical_pin)
            raise IoTPy_APIError("PWM high time is out of range.")

    def write(self, duty):
        """
        Set PWM duty cycle.

        :param duty: PWM duty cycle in fractions: 1.0 is 100%, 0.5 is 50%, etc.
        :type duty: float
        """
        self.width_us(int(PWM_PORT_RUNNING[self.pwm_port]['period']*float(duty)))

    def read(self):
        """
        Get PWM duty cycle.

        :return: PWM duty cycle.
        """
        return float(self.hightime) / PWM_PORT_RUNNING[self.pwm_port]['period']

    def __exit__(self, exc_type, exc_value, traceback):
        PWM_PORT_RUNNING[self.pwm_port]['channels'] -= 1
        self.primary = True
        self.board.uper_io(0, self.board.encode_sfp(1, [self.logical_pin])) # set pin primary function
        if PWM_PORT_RUNNING[self.pwm_port]['channels'] == 0:
            PWM_PORT_RUNNING[self.pwm_port]['period'] = 0
            self.board.uper_io(0, self.board.encode_sfp(PWM._PWM_PORT_FUNCTIONS[self.pwm_port][2], [self.pwm_pin]))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass