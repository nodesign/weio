from struct import unpack
from IoTPy.pyuper.utils import IoTPy_ThingError


class Lm75:
    """
    Lm75 temperature sensor class.

    :param interface:  I2C communication interface.
    :type interface: :class:`IoTPy.pyuper.i2c.I2C`
    :param sensor_address: Lm75 sensor I2C address. Optional, default 0x48 (72).
    :type sensor_address: int
    """

    def __init__(self, interface, address=0x48):
        self.interface = interface
        self.address = address

    def __enter__(self):
        return self

    def temperature(self):
        """
        Read and return temperature.

        :return: Temperature in celsius.
        :rtype: int
        :raise: IoTPy_ThingError
        """
        try:
            result_raw = self.interface.transaction(self.address, '\x00', 2)
            result_integer = unpack('>H', result_raw)[0]
            temperature = result_integer / 256.0
        except IoTPy_ThingError:
            raise IoTPy_ThingError("LM75 - temperature reading error.")
        return temperature

    def __exit__(self, ex_type, ex_value, traceback):
        pass
