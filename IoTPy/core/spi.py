

class SPI:

    MODE_0 = 0
    MODE_1 = 1
    MODE_2 = 2
    MODE_3 = 3

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError()

    def read(self, count, value=0):
        raise NotImplementedError()

    def write(self, data):
        raise NotImplementedError()

    def transaction(self, data_out):
        raise NotImplementedError()


class SPIProducer:

    def SPI(self, name, clock=1000000, mode=SPI.MODE_0, *args, **kwargs):
        raise NotImplementedError()
