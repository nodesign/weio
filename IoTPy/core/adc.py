

class ADC:

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

    def read(self):
        raise NotImplementedError()

    def read_raw(self):
        raise NotImplementedError()


class ADCProducer:

    def ADC(self, name, *args, **kwargs):
        raise NotImplementedError()
