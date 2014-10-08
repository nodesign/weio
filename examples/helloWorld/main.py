from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello world")
