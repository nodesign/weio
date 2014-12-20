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

import tornado
import platform
import subprocess

from weioLib import weioConfig
from handlers import loginHandler

class WeioSigninHandler(loginHandler.BaseHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("../www/signin.html", errormessage = errormessage)

    def post(self):
        confFile = weioConfig.getConfiguration()
        fullName = self.get_argument("fullName", "")
        passwd = self.get_argument("password", "")
        boardname = self.get_argument("boardname", "")

        # This is two letters country code to be used to setup wifi region
        countryCode = self.get_argument("countryCode", "")

        print "************ ", fullName, passwd, boardname, countryCode

        data = {}
        # OK now is time to setup username and password
        confFile['user'] = fullName
        weioConfig.saveConfiguration(confFile)

        output = "OK PASSWD"
        #echo -e "weio\nweio" | passwd

        # ATTENTION, DON'T MESS WITH THIS STUFF ON YOUR LOCAL COMPUTER
        # First protection is mips detection, second is your own OS
        # who hopefully needs sudo to change passwd on the local machine
        if (platform.machine() == 'mips'):

            # Change root password
            command = "sh scripts/change_root_pswd.sh " + passwd
            print "EXEC : " + command

            try:
                subprocess.call(command, shell=True)
                firstTimeSwitch = "NO"
                confFile['first_time_run']=firstTimeSwitch
            except:
                output = "ERR_CMD PASSWD"
                print output

            # Change avahi name
            command = "sh scripts/change_boardname.sh " + boardname
            confFile['dns_name'] = boardname + ".local"
            weioConfig.saveConfiguration(confFile)
            print "EXEC : " + command

            try:
                subprocess.call(command, shell=True)
            except:
                output = "ERR_CMD BRDNAME"

        else:
            # On PC
            firstTimeSwitch = "NO"
            confFile['first_time_run']=firstTimeSwitch
        
        # Save new password in the config file
        confFile['password'] = passwd

        # Write in config file
        weioConfig.saveConfiguration(confFile)

        self.set_secure_cookie("user", tornado.escape.json_encode("weio"))
        self.redirect(self.get_argument("next", u"/"))

