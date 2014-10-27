from IoTPy.core.pwm import PWM
from IoTPy.pyuper.pinouts import CAP_PWM
from IoTPy.pyuper.utils import IoTPy_APIError, errmsg


PWM_PORT_RUNNING = [{'channels': 0, 'period': 0}, {'channels': 0, 'period': 0}]


class UPER1_PWM(PWM):
    """
    PWM (Pulse Width Modulation) pin module.

    :param board: IoBoard to which the pin belongs to.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param pin: PWM pin number.
    :type pin: int
    :param freq: PWM frequency in Hertz.
    :type freq: float
    :param polarity: Active (on) state signal level: 0 (LOW) or 1 (HIGH). Optional, default 1.
    :type polarity: int
    """

    _PWM_PORT_FUNCTIONS = [[50, 51, 52], [60, 61, 62]]
    _PWM_PORT_MAX = [0xffff, 0xffffffff]

    def __init__(self, board, pin, freq=100, polarity=1):
        self.board = board
        if self.board.pinout[pin].capabilities & CAP_PWM:
            self.logical_pin = self.board.pinout[pin].pinID
        else:
            errmsg("UPER API: Pin No:%d is not a PWM pin.", pin)
            raise IoTPy_APIError("Trying to assign PWM function to non PWM pin.")
        self.pwm_port = self.board.pinout[pin].extra[0]
        self.pwm_pin = self.board.pinout[pin].extra[1]
        self.primary = True
        self.pulse_time = 0
        self.polarity = polarity
        PWM_PORT_RUNNING[self.pwm_port]['channels'] += 1
        if PWM_PORT_RUNNING[self.pwm_port]['channels'] == 1:
            self.set_frequency(freq)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        PWM_PORT_RUNNING[self.pwm_port]['channels'] -= 1
        self.primary = True
        self.board.uper_io(0, self.board.encode_sfp(1, [self.logical_pin]))  # set pin primary function
        if PWM_PORT_RUNNING[self.pwm_port]['channels'] == 0:
            PWM_PORT_RUNNING[self.pwm_port]['period'] = 0
            self.board.uper_io(0, self.board.encode_sfp(UPER1_PWM._PWM_PORT_FUNCTIONS[self.pwm_port][2], [self.pwm_pin]))

    def set_frequency(self, freq):
        self.set_period(int(round(1e6/freq)))

    def set_period(self, period_us):
        """
        Set PWM period.

        :param period_us: PWM signal period in microseconds.
        :type period_us: int
        :raise: IoTPy_APIError
        """
        if 0 <= period_us <= self._PWM_PORT_MAX[self.pwm_port]:
            if PWM_PORT_RUNNING[self.pwm_port]['period'] != period_us:
                self.board.uper_io(0, self.board.encode_sfp(self._PWM_PORT_FUNCTIONS[self.pwm_port][0], [period_us]))
                PWM_PORT_RUNNING[self.pwm_port]['period'] = period_us
        else:
            errmsg("UPER API: PWM period for port %d can be only between 0-%d" % (self.pwm_port, self._PWM_PORT_MAX[self.pwm_port]))
            raise IoTPy_APIError("PWM period is out of range.")

    def set_duty_cycle(self, duty_cycle):
        """
        Set PWM duty cycle.

        :param duty_cycle: PWM duty cycle in percents.
        :type duty_cycle: float
        """
        self.set_pulse_time(int(round(PWM_PORT_RUNNING[self.pwm_port]['period']*float(duty_cycle/100.0))))

    def set_pulse_time(self, pulse_us):
        """
        Set PWM high (on state) time.

        :param pulse_us: Pulse time in microseconds.
        :type pulse_us: int
        :raise: IoTPy_APIError
        """
        if self.primary:
            self.board.uper_io(0, self.board.encode_sfp(2, [self.logical_pin]))  # set pin secondary function
            self.primary = False
        if 0 <= pulse_us <= PWM_PORT_RUNNING[self.pwm_port]['period']:
            self.pulse_time = pulse_us

            high_time = pulse_us
            if self.polarity == 0:
                high_time = PWM_PORT_RUNNING[self.pwm_port]['period'] - pulse_us

            self.board.uper_io(0, self.board.encode_sfp(UPER1_PWM._PWM_PORT_FUNCTIONS[self.pwm_port][1], [self.pwm_pin, high_time]))
        else:
            errmsg("UPER error: PWM high time is out of range on logical pin %d." % self.logical_pin)
            raise IoTPy_APIError("PWM high time is out of range.")
