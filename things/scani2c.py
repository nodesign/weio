from IoTPy.pyuper.ioboard import IoBoard
from IoTPy.pyuper.i2c import I2C
from IoTPy.pyuper.utils import IoTPy_IOError, IoTPy_ThingError, IoTPy_APIError, die

try:
	u = IoBoard()
except IoTPy_APIError, e: # seems can't establish connection with the UPER board
	details = e.args[0]
	die(details)

interface = I2C(u)
for address in xrange(0,128):
    print address
    try:
        interface.transaction(address, '', 0)
        print "geras:", address
    except IoTPy_IOError, IoTPy_APIError:
        pass