#######################################
#                                     #
#  MPU6050 accelerometer & gyroscope  #
#                                     #
#######################################

from weioLib.weio import *
from things.input.motion.mpu6050 import Mpu6050

def setup():
    attach.process(myProcess)
    
def myProcess():
    
    i2c = initI2C()
    print "sensor on address", i2c.scan()
    
    mpu6050 = Mpu6050() 
    
    while True :
        
        gyro = mpu6050.getGyroscope()
        #print gyro["x"], gyro["y"], gyro["z"]
        
        accel = mpu6050.getAccelerometer()
        #print accel["x"], accel["y"], accel["z"]
        
        rotX = mpu6050.getRotationX()
        rotY = mpu6050.getRotationY()
        
        print rotX, rotY
        
        delay(50)