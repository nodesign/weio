from weioLib.weio import *

def setup():
    attach.event('gyro', gyroHandler)

def gyroHandler(dataIn):
    print dataIn
    



