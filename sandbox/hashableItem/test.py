class Pin(object):
    def __init__(self, pin, mode):
        self.pin = pin
        self.mode = mode
    def __repr__(self):
        return "Pin(%s, %s)" % (self.pin, self.mode)
    def __eq__(self, other):
        if isinstance(other, Pin):
            # Check if pin is the same, mode is not relevant
            return (self.pin == other.pin)
        else:
            return False
    def __hash__(self):
        return hash(self.pin)


m = Pin(3,4)
a = set()
a.add(m)
print m in a
print a

m = Pin(3,18)
print m in a
print a

if (m in a):
    a.remove(m)

a.add(m)
print a

print a.pop()

