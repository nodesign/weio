from time import sleep

LOW = 0
HIGH =1
LSBFIRST = 1
MSBFIRST = 0

class SHT1X:
    """
    SHT10, SHT11 and SHT15 humidity and temperature sensor class.

    :param data_pin: GPIO pin connected to DATA line.
    :type data_pin: :class:`IoTPy.pyuper.gpio.GPIO`
    :param clk_pin: GPIO pin connected to SCK line.
    :type clk_pin: :class:`IoTPy.pyuper.gpio.GPIO`
    """

    def __init__(self, data_pin, clk_pin):
        self.data_pin = data_pin
        self.clk_pin = clk_pin

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        pass

    def _shift_out(self, bit_order, byte, bits):
        for i in xrange(bits):
            if bit_order == LSBFIRST:
                self.data_pin.write(byte & (1 << i))
            else:
                self.data_pin.write(byte & (1 << (7 -i)))
            self.clk_pin.write(HIGH)
            sleep(0.0003)
            self.clk_pin.write(LOW)

    def _sht_command(self, command):
        self.data_pin.write(HIGH)
        self.clk_pin.write(HIGH)
        self.data_pin.write(LOW)
        self.clk_pin.write(LOW)
        self.clk_pin.write(HIGH)
        self.data_pin.write(HIGH)
        self.clk_pin.write(LOW)
        self.data_pin.write(LOW)

        self._shift_out(MSBFIRST, command, 8)
        self.clk_pin.write(HIGH)
        ack = self.data_pin.read()
        if ack != LOW:
            raise RuntimeError("No ACK. Sensor not present?")
        self.clk_pin.write(LOW)
        ack = self.data_pin.read()
        if ack != HIGH:
            raise RuntimeError("No ACK. Sensor not present?")

    def _shift_in(self, bits):
        ret = 0
        for i in xrange(bits):
            self.clk_pin.write(HIGH)
            sleep(0.01)
            ret = (ret << 1) + self.data_pin.read()
            self.clk_pin.write(LOW)
        return ret

    def _wait_sht(self):
        for i in xrange(100):
            sleep(0.002)
            ack = self.data_pin.read()
            if ack == LOW:
                break
        if ack == HIGH:
            raise RuntimeError("Measurement wait timeout")

    def _get_data_sht(self):
        val = self._shift_in(8) * 256
        self.data_pin.write(HIGH)
        self.data_pin.write(LOW)
        self.clk_pin.write(HIGH)
        self.clk_pin.write(LOW)
        val |= self._shift_in(8)
        return val

    def _skip_crc(self):
        self.data_pin.write(HIGH)
        self.clk_pin.write(HIGH)
        self.clk_pin.write(LOW)

    def _temperature_raw(self):
        self._sht_command(0x03)
        self._wait_sht()
        val = self._get_data_sht()
        self._skip_crc()
        return val

    def temperature(self):
        """
        Measure and return temperature.

        :return: A measured temperature in celsius.
        :rtype: int
        """
        return (self._temperature_raw() * 0.01) - 40.1

    def humidity(self):
        """
        Measure and return humidity.

        :return: A measured humidity value in percents.
        :rtype: int
        """

        """
        C1 = -4.0       # for 12 Bit
        C2 =  0.0405    # for 12 Bit
        C3 = -0.0000028 # for 12 Bit
        T1 =  0.01      # for 14 Bit @ 5V
        T2 =  0.00008   # for 14 Bit @ 5V
        """
        C1 = -2.0468       # for 12 Bit
        C2 =  0.0367    # for 12 Bit
        C3 = -0.0000015955 # for 12 Bit
        T1 =  0.01      # for 14 Bit @ 5V
        T2 =  0.00008   # for 14 Bit @ 5V

        self._sht_command(0x05)
        self._wait_sht()
        val = self._get_data_sht()
        self._skip_crc()
        linear_humidity = C1 + C2 * val + C3 * val * val
        return((self.temperature() - 25.0 ) * (T1 + T2 * val) + linear_humidity)
