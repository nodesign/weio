

class PWM:

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

    def set_frequency(self, freq):
        raise NotImplementedError()

    def set_period(self, period_us):
        raise NotImplementedError()

    def set_duty_cycle(self, duty_cycle):
        raise NotImplementedError()

    def set_pulse_time(self, pulse_us):
        raise NotImplementedError()


class PWM_Producer:

    def PWM(self, name, freq=100, polarity=1, *args, **kwargs):
        raise NotImplementedError()
