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

import subprocess
import weioUnblock

import tornado.gen


@weioUnblock.unblock
def shellAsync(command) :
    """ Async shell command - executed in parallel thread

    N.B.
    As result to this call wil not be returned immidiately,
    this function should be called ONLY with tornado.gen yield
    """

    try :
        output = subprocess.check_output(command, shell=True)
    except :
        output = "ERR_CMD"
	
    return output


def shellBlocking(command) :
    """ Classic blocking shell subprocess """

    try :
        output = subprocess.check_output(command, shell=True)
    except :
        output = "ERR_CMD"
	
    return output


class WeioShellCommand():
    """ Shell command class that holds the command and
    has a async method to subprocess it in another thread and get the output.

    Sends output back via callback to calling yield tornado.gen.Task()
    """

    command = ''

    def set(self, newCommand):
        self.command = newCommand

    @weioUnblock.unblock
    def execute(self, callback) :
        """ Tornado Generator is waiting for the output with yield,
        although the command itselfis executed asynchroniously to unblock ioloop
        """

        result = shellBlocking(self.command)

        callback(result)


