from struct import unpack

from IoTPy.pyuper.utils import IoTPy_ThingError


class Si7020:
    ADDRESS = 0x40             # Address of the si7020
    RH_HOLD = '\xe5'           # RH hold master mode
    RH_NOHOLD = '\xf5'         # RH no hold master mode
    TEMP_HOLD = '\xe3'         # temp hold master mode
    TEMP_NOHOLD = '\xf3'       # temp no hold master mode
    TEMP_PREVIOUS = '\xe0'     # temp from previous measurement
    RESET = '\xfe'             # reset
    WRITE_REG = '\xe6'         # write user register 1
    READ_REG = '\xe7'          # read user register 1
    READ_ID1 = '\xfa\x0f'      # read ID 1st byte
    READ_ID2 = '\xfc\xc9'      # read ID 2nd byte
    FW_REVISION = '\x84\xb8'   # get firmware revision

    def __init__(self, interface):
        self.interface = interface

    def __enter__(self):
        return self

    def temperature(self):
        try:
            self.interface.transaction(Si7020.ADDRESS, Si7020.TEMP_HOLD, 0)
            result_raw = self.interface.transaction(Si7020.ADDRESS, '', 2)
            result_integer = unpack('>H', result_raw[:2])[0]
            temp = (175.72 * result_integer)/65536 - 46.85
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - temperature reading error.")
        return temp

    def humidity(self):
        try:
            self.interface.transaction(Si7020.ADDRESS, Si7020.RH_HOLD, 0)
            result_raw = self.interface.transaction(Si7020.ADDRESS, '', 2)
            result_integer = unpack('>H', result_raw[:2])[0]
            rh = (125.0 * result_integer)/65536 - 6
        except IoTPy_ThingError:
            raise IoTPy_ThingError("Si7020 - humidity reading error.")
        return rh

    def __exit__(self, ex_type, ex_value, traceback):
        pass