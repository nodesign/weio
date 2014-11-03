from weioLib.weioUserApi import attach

def setup():
    attach.process(myProcess)
    
def myProcess():
    print("Hello world")
