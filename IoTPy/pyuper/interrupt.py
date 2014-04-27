from IoTPy.pyuper.utils import IoTPy_APIError, errmsg


class Interrupt:
    LEVEL_LOW = 0
    LEVEL_HIGH = 1
    EDGE_CHANGE = 2
    EDGE_RISE = 3
    EDGE_FALL = 4

    def __init__(self, board, pin):
        self.board = board
        if self.board.pinout[pin][0] & self.board.cap_gpio:
            self.logical_pin = self.board.pinout[pin][1][0]
        else:
            errmsg("UPER API: Pin No:%d is not GPIO pin, can't attach interrupt.", pin)
            raise IoTPy_APIError("Wrong Pin number.")

    def attach(self, mode, callback):
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
        self.board.callbackdict[self.logical_pin] = [mode, callback]
        self.board.uper_io(0, self.board.encode_sfp(6, [interruptID, self.logical_pin, mode]))
        return True

    def detach(self):
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