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

class UnixSocketClient:

    def __init__(self, name):
        self.name = name
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        self.sock.setblocking(0)
        self.stream = iostream.IOStream(self.sock)
        self.stream.connect("uds_" + name)
        ioloop.IOLoop.instance().start()
        
    def send_request(self):
        #out = pickle.dumps(self.name, pickle.HIGHEST_PROTOCOL)
        self.stream.write(self.name + "\n")
        #stream.read_until("\r\n\r\n", on_headers)
    def send(self, message):
        # serialize object and prepare for transfer
        #out = pickle.dumps(messageObj, pickle.HIGHEST_PROTOCOL)
        self.stream.write(message + "\n")

# 
# import socket
# import sys
# import pickle
# 
# class UnixSocketClient:
# 
#     def __init__(self, name):
#        
#         # Create a UDS socket
#         global sock
#         sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#         # define non-blocking socket
#         sock.setblocking(0)
#         #sock.settimeout(1)
#         # Connect the socket to the file where the server is listening
#         server_address = "uds_" + name
#         print >>sys.stderr, 'connecting to %s' % server_address
#         try:
#             sock.connect(server_address)
#             
#         except socket.error, msg:
#             print >>sys.stderr, msg
#             #I can't connect to the server, something is wrong I'll exit
#             sys.exit(1)
#     
#     def send(self, messageObj):
#         global sock
#         try:
#             
#             # serialize object and prepare for transfer
#             out = pickle.dumps(messageObj, pickle.HIGHEST_PROTOCOL)
#             
#             # print >>sys.stderr, 'sending "%s"' % message
#             
#             # Send data
#             sock.send(out + "\n")
#             
#         except socket.error, msg:
#             print >>sys.stderr, msg
#             sys.exit(1)
#     
#     def close(self):
#         print "closing connection"
#         global sock
#         # Strange thing, if I don't send something before closing Tornado will cut off
#         # last information :|
#         sock.sendAll("\n")
#         sock.close()
#     
#     # TODO this part of code is not yet finished, receive will call handler in his parent
#     def receive(self):
#         try :
#             data = sock.recv(1024)
#             return data
#         except :
#             return None 