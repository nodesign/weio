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

from handlers.weioJSPYHandler import connections

class WeioInfo():

    def getNumberOfConnectedClients(self):
        return len(connections)

    def getConnectedClients(self):
        return connections

    def getClientInfos(self, nClient):
        if (nClient < len(connections) and nClient > 0):
            return connections[nClient].request.headers
        else :
            return "Client of index %s don't exist" % nClient

    def sendToAllClients(self, data):
        for client in connections:
            client.write_message(data)

    def sendToClient(self, nClient, data):
        if (nClient < len(connections) and nClient > 0):
            connections[nClient].write_message(data)
        else :
            return "Client of index %s don't exist" % nClient

clients = WeioInfo()