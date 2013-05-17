### 
#
# WEIO Web Of Things Platform
# Copyright (C) 2013 Nodesign.net, Uros PETREVSKI, Drasko DRASKOVIC
# All rights reserved
#
#               ##      ## ######## ####  #######  
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ######    ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#               ##  ##  ## ##        ##  ##     ## 
#                ###  ###  ######## ####  #######
#
#                    Web Of Things Platform 
#
# This file is part of WEIO
# WEIO is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WEIO is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors : 
# Uros PETREVSKI <uros@nodesign.net>
# Drasko DRASKOVIC <drasko.draskovic@gmail.com>
#
###

from tornado import ioloop
from tornado import iostream
import socket
import time
import sys
import json

def send_request():
    
    print "hello"
    for a in range(5) :
        print(str(a))
        time.sleep(0.1)
        
    stream.close()
    #stream.read_until("\r\n\r\n", on_headers)
    #stream.read_until_close(on_body, None)
    ioloop.IOLoop.instance().stop()

class StdOutputToSocket():
     def write(self, msg):
         #out = {}
         #out['stdout'] = msg
         stream.write(json.dumps(msg))
         
class StdErrToSocket():
    def write(self, msg):
        out = {}
        out['stderr'] = msg
        stream.write(json.dumps(out))


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
stream = iostream.IOStream(s)
stream.connect("uds_weio_mainStdOut", send_request)

sys.stdout = StdOutputToSocket()
#sys.stderr = StdErrToSocket()

ioloop.IOLoop.instance().start()


