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

from os.path import isfile, join

from sockjs.tornado import SockJSRouter, SockJSConnection

import functools
import json
# IMPORT BASIC CONFIGURATION FILE
from weioLib import weioConfig

clients = set()


class WeioSettingsHandler(SockJSConnection):

    # def get(self):
    #     try:
    #         errormessage = self.get_argument("error")
    #     except:
    #         errormessage = ""
    #     self.render("../www/settings.html", errormessage = errormessage)
    #     print "ISSSSSSSS"

    def __init__(self, *args, **kwargs):
        SockJSConnection.__init__(self, *args, **kwargs)
        self.errObject = []
        self.errReason = ""

    def getUserSettings(self, rq):
        print "USOOOOOOOOOO"
        config = weioConfig.getConfiguration()
        data = {}
        data['requested'] = rq['request']
        config['user'] = user
        data = {user}

        # Send user settings information to the client
        self.broadcast(clients, json.dumps(data))

    
