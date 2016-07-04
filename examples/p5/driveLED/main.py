from weioLib.weio import *

def setup():
    attach.process(myProcess)
    attach.event("getIn", fromWeb)
    
def fromWeb(data):
    print data
    
def myProcess():
    print("Hello world")
