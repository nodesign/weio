from weioLib.weio import *

def setup():
    attach.event('gyro', gyroHandler)

def gyroHandler(dataIn):
    if dataIn is not None:
        print dataIn



