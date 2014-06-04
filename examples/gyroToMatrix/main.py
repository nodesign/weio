
from weioLib.weioUserApi import attach

def setup():
    attach.event('gyro', gyroHandler)

def gyroHandler(dataIn):
    if dataIn is not None:
        print dataIn



