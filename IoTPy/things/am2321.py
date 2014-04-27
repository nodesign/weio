from time import sleep
from struct import unpack

from IoTPy.pyuper.utils import IoTPy_ThingError


I2C_ADDR_AM2321 = 0x5c # 0xB8 >> 1
PARAM_AM2321_READ = '\x03'
REG_AM2321_HUMIDITY_MSB = '\x00'
REG_AM2321_HUMIDITY_LSB = '\x01'
REG_AM2321_TEMPERATURE_MSB = '\x02'
REG_AM2321_TEMPERATURE_LSB = '\x03'
REG_AM2321_DEVICE_ID_BIT_24_31 = '\x0B'


class AM2321:
    def __init__(self, interface, sensor_address= 0x5c):
        self.interface = interface
        self.address = sensor_address
        self.temperature = -1000.0
        self.humidity = -1

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        pass

    def _read_raw(self, command, regaddr, regcount):
        self.interface.transaction(self.address, '', 1, True)
        self.interface.transaction(self.address, command+regaddr+chr(regcount), 0)
        sleep(0.002)
        buf = self.interface.transaction(self.address, '', regcount + 4)
        crc = unpack('<H', buf[-2:])[0]
        if crc != self._am_crc16(buf[:-2]):
            raise IoTPy_ThingError("AM2321 reading CRC error.")
        return buf[2:-2]

    def _am_crc16(self, buf):
        crc = 0xFFFF
        for c in buf:
            crc ^= ord(c)
            for i in range(8):
                if crc & 0x01:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def read_uid(self):
        resp = self._read_raw(PARAM_AM2321_READ, REG_AM2321_DEVICE_ID_BIT_24_31, 4)
        uid = unpack('>I', resp)[0]
        return uid

    def read(self):
        raw_data = self._read_raw(PARAM_AM2321_READ, REG_AM2321_HUMIDITY_MSB, 4)
        self.temperature = unpack('>H', raw_data[-2:])[0]/10.0
        self.humidity = unpack('>H', raw_data[-4:2])[0]/10.0

    def temperature(self):
        return self.temperature

    def humidity(self):
        return self.humidity
