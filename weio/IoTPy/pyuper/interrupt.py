from IoTPy.pyuper.pinouts import CAP_GPIO
from IoTPy.pyuper.utils import IoTPy_APIError, errmsg


class Interrupt:
    """
    GPIO interrupt pin module.

    :param board: IoBoard to which the pin belongs to.
    :type board: :class:`IoTPy.pyuper.ioboard.IoBoard`
    :param pin: GPIO pin number.
    :type pin: int
    """

    LEVEL_LOW = 0
    LEVEL_HIGH = 1
    EDGE_CHANGE = 2
    EDGE_RISE = 3
    EDGE_FALL = 4

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin].capabilities & CAP_GPIO:
            self.logical_pin = self.board.pinout[pin].pinID
        else:
            errmsg("UPER API: Pin No:%d is not GPIO pin, can't attach interrupt.", pin)
            raise IoTPy_APIError("Wrong Pin number.")

    def attach(self, mode, callback, user_object=None, debounce_time=50):
        """
        Attach (enable) or reconfigure GPIO interrupt event.

        :param mode: GPIO interrupt mode. Can have one of these values: Interrupt.EDGE_RISE, Interrupt.EDGE_FALL, \
        Interrupt.EDGE_CHANGE, Interrupt.LEVEL_LOW or Interrupt.LEVEL_HIGH.
        :param callback: User callback function. This function is executed when the interrupt event is received. \
        It should take two arguments: interrupt event description and user object. Interrupt event descriptor is \
        dictionary with three fields: 'id' - the interrupt ID (interrupt channel), 'type' - interrupt event type \
        (same meaning as mode) and 'values' - the logical values on each of interrupt channel (N-th bit represents  \
        logical pin value of interrupt channel N). User object is the same object as user_object.
        :param user_object: User defined object, which will be passed back to the callback function. Optional,  \
        default is None.
        :param debounce_time: Interrupt disable time in milliseconds after the triggering event. This is used to \
        "debounce" buttons or to protect communication channel from data flood. Optional, default is 50ms.

        :return: True
        :raise: IoTPy_APIError
        """
        try:
            interruptID = self.board.interrupts.index(self.logical_pin)
            self.board.uper_io(0, self.board.encode_sfp(7, [interruptID])) 	#detach interrupt
        except ValueError:
            try:
                interruptID = self.board.interrupts.index(None)
                self.board.interrupts[interruptID] = self.logical_pin
            except ValueError:
                errmsg("UPER API: more than 8 interrupts requested")
                raise IoTPy_APIError("Too many interrupts.")
        self.board.callbackdict[self.logical_pin] = {'mode':mode, 'callback':callback, 'userobject':user_object }
        self.board.uper_io(0, self.board.encode_sfp(6, [interruptID, self.logical_pin, mode, debounce_time]))
        return interruptID

    def detach(self):
        """
        Detach (disable) GPIO interrupt.

        :return: True
        :raise: IoTPy_APIError
        """

        try:
            interruptID = self.board.interrupts.index(self.logical_pin)
        except ValueError:
            errmsg("UPER API: trying to detach non existing interrupt.")
            return False
            #raise IoTPy_APIError("trying to detaching non existing interrupt.")
			
        self.board.interrupts[interruptID] = None
		
        try:
            del self.board.callbackdict[self.logical_pin]
        except KeyError:
            errmsg("UPER API: trying to detach non existing interrupt.")
            raise IoTPy_APIError("trying to detaching non existing interrupt.")

        self.board.uper_io(0, self.board.encode_sfp(7, [interruptID]))

        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.detach()