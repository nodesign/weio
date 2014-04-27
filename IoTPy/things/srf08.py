from time import sleep
from struct import unpack, pack

from IoTPy.pyuper.utils import IoTPy_ThingError, errmsg


class Srf08:
    CMD = '\x00'            # Command byte
    LIGHT = '\x01'          # Byte to read light sensor
    RESULT = '\x02'       	# Byte for start of ranging data
    GAIN_REGISTER = '\x00' 	#
    RANGE_LOCATION = '\xff' # return distance in cm
    INCH = '\x50' 	# return distance in cm
    CM = '\x51' 	# return distance in cm
    MS = '\x52' 	# return distance in cm

    def __init__(self, interface, sensor_address= 0x70):
        self.interface = interface
        self.address = sensor_address

    def __enter__(self):
        return self

    def change_address(self, address):
        if self.address != address:
            byte_address = pack('B', address * 2)
            self.interface.transaction(self.address, Srf08.CMD + '\xa0' + Srf08.GAIN_REGISTER + Srf08.RANGE_LOCATION, 0)
            self.interface.transaction(self.address, Srf08.CMD + '\xaa' + Srf08.GAIN_REGISTER + Srf08.RANGE_LOCATION, 0)
            self.interface.transaction(self.address, Srf08.CMD + '\xa5' + Srf08.GAIN_REGISTER + Srf08.RANGE_LOCATION, 0)
            self.interface.transaction(self.address, Srf08.CMD + byte_address + Srf08.GAIN_REGISTER + Srf08.RANGE_LOCATION, 0)
            self.address = address

    def distance(self, distance_unit = CM):
        if distance_unit not in (Srf08.CM, Srf08.INCH, Srf08.MS):
            errmsg("Wrong units for distance, should be 'c' or 'i' or 'm'.")
            raise IoTPy_ThingError("Wrong units for distance, should be 'c' or 'i' or 'm'.")
        try:
            self.interface.transaction(self.address, Srf08.CMD + distance_unit, 0)
            sleep(0.08)
            distance = unpack('>H', self.interface.transaction(self.address, Srf08.RESULT, 2)[:2])[0]
        except IoTPy_ThingError:
            raise IoTPy_ThingError("srf08 - distance reading error.")
        return distance

    def light(self):
        try:
            self.interface.transaction(self.address, Srf08.CMD + Srf08.CM, 0)
            sleep(0.08)
            light = unpack('>B', self.interface.transaction(self.address, Srf08.LIGHT, 1)[:1])[0]
        except IoTPy_ThingError:
            raise IoTPy_ThingError("srf08 - distance reading error.")
        return light

    def get_revision(self):
        pass

    def __exit__(self, ex_type, ex_value, traceback):
        pass