# Global definitions
ONCE = 0
ALWAYS = 1

OUTPUT = 0
INPUT = 1

class WeioSharedVar(object):
    pass


class WeioApiProcess():
    def __init__ (self, procFnc, procArgs) :
        self.procFnc = procFnc
        self.procArgs = procArgs

class WeioApiEvent():
    def __init__ (self, event, handler) :
        self.event = event
        self.handler = handler

class WeioApiInterrupt():
    def __init__ (self, pin, edge, event) :
        self.pin = pin
        self.edge = edge
        self.event = event


class WeioAttach():
    def __init__(self):
        self.procs = {}
        self.events = {}
        self.ints = {}

    def process(self, procFnc, procArgs=()):
        proc = WeioApiProcess(procFnc, procArgs)
        procId = procFnc.__name__
        self.procs[procId] = proc

    def event(self, event, handler):
        event = WeioApiEvent(event, handler)
        self.events[event] = event

    def interrupt(self, pin, edge, event):
        intr = WeioApiInterrupt(pin, edge, event)
        slef.ints[pin] = intr


###
# Global instances
###
attach = WeioAttach()
shared = WeioSharedVar()


