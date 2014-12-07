# Ported to WeIO by Uros Petrevski
# Code originally was found on Bitify :
# http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html

from weioLib import smbus
import math

class Mpu6050:
    def __init__(self, address=0x68):
        self.bus = smbus.SMBus()
        self.address = address

        # Power management registers
        power_mgmt_1 = 0x6b
        power_mgmt_2 = 0x6c

        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, power_mgmt_1, 0)

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)
################################################# USER FUNCTIONS
    def getRotationX(self):
        accel = self.getAccelerometer()
        x = accel["x"]
        y = accel["y"]
        z = accel["z"]
        return self.get_x_rotation(x, y, z)

    def getRotationY(self):
        accel = self.getAccelerometer()
        x = accel["x"]
        y = accel["y"]
        z = accel["z"]
        return self.get_y_rotation(x, y, z)

    def getAccelerometer(self):
        accel_xout = self.read_word_2c(0x3b)
        accel_yout = self.read_word_2c(0x3d)
        accel_zout = self.read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        data = {}
        data["x"] = accel_xout_scaled
        data["y"] = accel_yout_scaled
        data["z"] = accel_zout_scaled
        return data

    def getGyroscope(self):
        gyro_xout = self.read_word_2c(0x43)
        gyro_yout = self.read_word_2c(0x45)
        gyro_zout = self.read_word_2c(0x47)

        gyroScaledX = gyro_xout/131
        gyroScaledY = gyro_yout/131
        gyroScaledZ = gyro_zout/131

        data = {}
        data["x"] = gyroScaledX
        data["y"] = gyroScaledY
        data["z"] = gyroScaledZ
        return data
