from weioLib.weio import *

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("webCreator address: weio.local")
