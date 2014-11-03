from IoTPy.pyuper.utils import IoTPy_APIError, errmsg
from IoTPy.pyuper.pinouts import CAP_GPIO
from IoTPy.core.gpio import GPIO


class UPER1_GPIO(GPIO):
    """
    GPIO (General Purpose Input and Output) pin module.

    :param board: IoBoard to which the pin belongs to.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param pin: GPIO pin number.
    :type pin: int
    :raise: IoTPy_APIError
    """

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin].capabilities & CAP_GPIO:
            self.logical_pin = self.board.pinout[pin].pinID
        else:
            errmsg("UPER API: Pin No:%d is not GPIO pin.", pin)
            raise IoTPy_APIError("Trying to assign GPIO function to non GPIO pin.")

        # Configure default state to be input with pull-up resistor
        self.direction = GPIO.INPUT
        self.resistor = GPIO.PULL_UP
        self.setup(self.direction, self.resistor)
        self.board.uper_io(0, self.board.encode_sfp(1, [self.logical_pin]))  # set primary

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.detach_irq()

    def setup(self, direction, resistor=GPIO.PULL_UP):
        """
        Configure GPIO.

        :param direction: GPIO direction: GPIO.OUTPUT or GPIO.INPUT
        :param resistor: GPIO internal resistor mode. Used when direction is GPIO.INPUT. Should be GPIO.PULL_UP, \
        GPIO.PULL_DOWN or GPIO.NONE.

        :raise: IoTPy_APIError
        """
        if not direction in [GPIO.OUTPUT, GPIO.INPUT]:
            raise IoTPy_APIError("Invalid GPIO direction. Should be GPIO.INPUT or GPIO.OUTPUT")

        if direction == GPIO.INPUT and not resistor in [GPIO.NONE, GPIO.PULL_UP, GPIO.PULL_DOWN]:
            raise IoTPy_APIError("Invalid GPIO resistor setting. Should be GPIO.NONE, GPIO.PULL_UP or GPIO.PULL_DOWN")

        self.direction = direction

        if direction == GPIO.INPUT:
            self.resistor = resistor

            if resistor == GPIO.PULL_UP:
                mode = 4  # PULL_UP
            elif resistor == GPIO.PULL_DOWN:
                mode = 2  # PULL_DOWN
            else:
                mode = 0  # HIGH_Z
        else:
            mode = 1  # OUTPUT

        self.board.uper_io(0, self.board.encode_sfp(3, [self.logical_pin, mode]))

    def write(self, value):
        """
        Write a digital value (0 or 1). If GPIO pin is not configured as output, set it's GPIO mode to GPIO.OUTPUT.

        :param value: Digital output value (0 or 1)
        :type value: int
        """
        if self.direction != GPIO.OUTPUT:
            self.setup(GPIO.OUTPUT)

        self.board.uper_io(0, self.board.encode_sfp(4, [self.logical_pin, value]))

    def read(self):
        """
        Read a digital signal value. If GPIO pis in not configure as input, set it to GPIO.PULL_UP pin mode.

        :return: Digital signal value: 0 (LOW) or 1 (HIGH).
        :rtype: int
        """
        if self.direction != self.INPUT:
            self.setup(GPIO.INPUT, self.resistor)

        return self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(5, [self.logical_pin])))[1][1]

    def attach_irq(self, event, callback=None, user_object=None, debounce_time=50):
        """
        Attach (enable) or reconfigure GPIO interrupt event.

        :param event: GPIO interrupt event. Can have one of these values: GPIO.RISE, GPIO.FALL, GPIO.CHANGE, \
        GPIO.LOW or GPIO.HIGH.
        :param callback: User callback function. This function is executed when the interrupt event is received. \
        It should take two arguments: interrupt event description and user object. Interrupt event descriptor is \
        dictionary with three fields: 'id' - the interrupt ID (interrupt channel), 'event' - interrupt event type \
        and 'values' - the logical values on each of interrupt channel (N-th bit represents logical pin value of \
        interrupt channel N). User object is the same object as user_object.
        :param user_object: User defined object, which will be passed back to the callback function. Optional,  \
        default is None.
        :param debounce_time: Interrupt disable time in milliseconds after the triggering event. This is used to \
        "debounce" buttons or to protect communication channel from data flood. Optional, default is 50ms.

        :return: Logical interrupt ID
        :rtype: int
        :raise: IoTPy_APIError
        """
        try:
            irq_id = self.board.interrupts.index(self.logical_pin)
            self.board.uper_io(0, self.board.encode_sfp(7, [irq_id])) 	# detach interrupt
        except ValueError:
            try:
                irq_id = self.board.interrupts.index(None)
                self.board.interrupts[irq_id] = self.logical_pin
            except ValueError:
                errmsg("UPER API: more than 8 interrupts requested")
                raise IoTPy_APIError("Too many interrupts.")
        self.board.callbackdict[self.logical_pin] = {'mode': event, 'callback': callback, 'userobject': user_object}
        self.board.uper_io(0, self.board.encode_sfp(6, [irq_id, self.logical_pin, event, debounce_time]))
        return irq_id

    def detach_irq(self):
        """
        Detach (disable) GPIO interrupt.

        :return: True on success, False otherwise
        :raise: IoTPy_APIError
        """

        try:
            irq_id = self.board.interrupts.index(self.logical_pin)
        except ValueError:
            errmsg("UPER API: trying to detach non existing interrupt.")
            return False

        self.board.interrupts[irq_id] = None
        return True

    def get_irq_count(self):
        raise NotImplementedError()

    def clear_irq_count(self, clear_to=0):
        raise NotImplementedError()

    def read_pulse(self, level=GPIO.HIGH, timeout=100000):
        if self.direction != self.INPUT:
            self.setup(GPIO.INPUT, self.resistor)

        return self.board.decode_sfp(self.board.uper_io(1, self.board.encode_sfp(9, [self.logical_pin, level, timeout])))[1][0]