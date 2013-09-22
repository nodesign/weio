from __future__ import print_function
from threading import Lock, RLock
import sys

# Global definitions
ONCE = 0
ALWAYS = 1

OUTPUT = 0
INPUT = 1


#####################
# WeIO User Classes
#####################
###
# LockProxy is used to lock methods of inherited class
# Example of usage:
# lockedset = LockProxy(set([1,2,3]))
###
class LockProxy(object):
    def __init__(self, obj):
        self.__obj = obj
        self.__lock = RLock()
        # RLock because object methods may call own methods
    def __getattr__(self, name):
        def wrapped(*a, **k):
            with self.__lock:
                getattr(self.__obj, name)(*a, **k)
        return wrapped

###
# Locking can be done with class decorators
###
def lockedMethod(method):
    """Method decorator. Requires a lock object at self._lock"""
    def newmethod(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return newmethod

###
# Thread-safe (locaked) print
###
class WeioPrint():
    def __init__(self, *args, **kwargs):
        self._lock = Lock()
    
    @lockedMethod
    def output(self, *args, **kwargs):
        print(*args, **kwargs)

        # Flush the file or stdout
        if (kwargs.get('file') != None):
            kwargs['file'].flush()
        else:
            sys.stdout.flush()


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

class WeioClient():
    
    def __init__(self, info, connection):
        self.info = info
        self.connection = connection


###
# Global instances
###
attach = WeioAttach()
shared = WeioSharedVar()
console = WeioPrint()
