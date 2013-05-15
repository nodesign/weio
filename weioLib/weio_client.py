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

# Weio client connects 
from tornado import ioloop
from tornado import iostream
import socket
import time
import sys
sys.path.append(r'./');

from weioLib import weio_globals, weio_gpio

# TODO don't use pickle
import pickle

def send_request():
    pass
    #stream.close()
    #ioloop.IOLoop.instance().stop()

class StdOutputToSocket():
    global out
    out = {}
    
    def write(self, msg):
        global out
        if "\n" in msg :
            out['stdout'] = out['stdout'] + msg
            stream.write(pickle.dumps(out))
            #stream.write(json.dumps(out))
        else :
            out['stdout'] = msg
         
class StdErrToSocket():
    global out
    out = {}
    
    def write(self, msg):
        global out
        if "\n" in msg :
            out['stdout'] = out['stdout'] + msg
            stream.write(pickle.dumps(out))
            #stream.write(json.dumps(out))
        else :
            out['stdout'] = msg
            
            
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
stream = iostream.IOStream(s)
stream.connect("uds_weio_main", send_request)

sys.stdout = StdOutputToSocket()
sys.stderr = StdErrToSocket()

ioloop.IOLoop.instance().start()