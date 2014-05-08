from IoTPy.pyuper.utils import IoTPy_APIError, errmsg


PWM_PORT_RUNNING = [[0,0], [0,0]]
class PWM:
    PWM_PORT_FUNCTIONS = [[50,51,52],[60,61,62]]
    PWM_PERIOD = 10000
    PWM_PORT_MAX = [0xffff, 0xffffffff]      #maxuint16, maxuint32

    def __init__(self, board, pin, polarity = 1):
        self.board = board
        if self.board.pinout[pin][0] & self.board.cap_pwm:
            self.logical_pin = self.board.pinout[pin][1][0]
        else:
            errmsg("UPER API: Pin No:%d is not a PWM pin.", pin)
            raise IoTPy_APIError("Trying to assign PWM function to non PWM pin.")
        self.pwm_port = self.board.pinout[pin][1][1]
        self.pwm_pin = self.board.pinout[pin][1][2]
        self.primary = True
        self.hightime = 0
        self.polarity = polarity
        PWM_PORT_RUNNING[self.pwm_port][0] += 1
        if PWM_PORT_RUNNING[self.pwm_port][0] == 1:
            self.period(self.PWM_PERIOD)

    def period(self, period):
        if 0 <= period <= self.PWM_PORT_MAX[self.pwm_port]:
            if PWM_PORT_RUNNING[self.pwm_port][1] != period:
                self.board.uper_io(0, self.board.encode_sfp(self.PWM_PORT_FUNCTIONS[self.pwm_port][0], [period]))
                PWM_PORT_RUNNING[self.pwm_port][1] = period
                self.PWM_PERIOD = period
        else:
            errmsg("UPER API: PWM period for port %d can be only between 0-%d" % (self.pwm_port, self.PWM_PORT_MAX[self.pwm_port]))
            raise IoTPy_APIError("PWM period is out of range.")

    def width_us(self, hightime):
        if self.primary:
            self.board.uper_io(0, self.board.encode_sfp(2, [self.logical_pin])) # set pin secondary function
            self.primary = False
        if 0 <= hightime <= PWM_PORT_RUNNING[self.pwm_port][1]:
            self.hightime = hightime
            if self.polarity == 1:
                hightime = PWM_PORT_RUNNING[self.pwm_port][1] - hightime
            self.board.uper_io(0, self.board.encode_sfp(PWM.PWM_PORT_FUNCTIONS[self.pwm_port][1], [self.pwm_pin, hightime]))
        else:
            errmsg("UPER error: PWM high time is out of range on logical pin %d." % self.logical_pin)
            raise IoTPy_APIError("PWM high time is out of range.")

    def write(self, duty):
        self.width_us(int((self.PWM_PERIOD)*float(duty)))

    def read(self):
        return float(self.hightime) / PWM_PORT_RUNNING[self.pwm_port][1]

    def __exit__(self, exc_type, exc_value, traceback):
        PWM_PORT_RUNNING[self.pwm_port][0] -= 1
        self.primary = True
        self.board.uper_io(0, self.board.encode_sfp(1, [self.logical_pin])) # set pin primary function
        if PWM_PORT_RUNNING[self.pwm_port][0] == 0:
            PWM_PORT_RUNNING[self.pwm_port][1] = 0
            self.board.uper_io(0, self.board.encode_sfp(PWM.PWM_PORT_FUNCTIONS[self.pwm_port][2], [self.pwm_pin]))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass