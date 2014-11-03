

class GPIO:

    # GPIO directions
    INPUT = 0
    OUTPUT = 1

    # GPIO resistors
    NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    # GPIO events
    LOW = 0
    HIGH = 1
    CHANGE = 2
    RISE = 3
    FALL = 4

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

    def setup(self, direction, resistor=PULL_UP):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()

    def write(self, value):
        raise NotImplementedError()

    def attach_irq(self, event, callback=None, user_object=None, debounce_time=50):
        raise NotImplementedError()

    def detach_irq(self):
        raise NotImplementedError()

    def get_irq_count(self):
        raise NotImplementedError()

    def clear_irq_count(self, clear_to=0):
        raise NotImplementedError()


class GPIOProducer:

    def GPIO(self, name, *args, **kwargs):
        raise NotImplementedError()
