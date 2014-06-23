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

        :param mode: GPIO interrupt mode.
        :param callback: User callback function. This function is executed when the interrupt event is received.
        :param user_object: Optional user defined object, which will be passed back to the callback function.
        :param debounce_time: Interrupt disable time in milliseconds after the triggering event. This is used to "debounce" buttons or \
        to protect communication channel from data flood. Optional, default is 50ms.

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
        return True

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
            IoTPy_APIError("trying to detaching non existing interrupt.")
        self.board.interrupts[interruptID] = None
        try:
            del self.board.callbackdict[self.logical_pin]
        except KeyError:
            errmsg("UPER API: trying to detach non existing interrupt.")
            IoTPy_APIError("trying to detaching non existing interrupt.")
        self.board.uper_io(0, self.board.encode_sfp(7, [interruptID]))
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.detach()