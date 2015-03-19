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
# This file is part of WEIO and is published under BSD license.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by the WeIO project.
# 4. Neither the name of the WeIO nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY WEIO PROJECT AUTHORS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL WEIO PROJECT AUTHORS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
        login_required = self.get_argument("loginRequired", "NO")
        boardname = self.get_argument("boardname", "")
        timezone = self.get_argument("timezone", "UTC+1")
        # This is two letters country code to be used to setup wifi region
        countryCode = self.get_argument("countryCode", "")

        print "************ ", fullName, passwd, boardname, countryCode

        data = {}
        # OK now is time to setup username and password
        confFile['user'] = fullName
        confFile['login_required'] = login_required
        weioConfig.saveConfiguration(confFile)
        confFile['timezone'] = timezone
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
            # Change user time zone
            if timezone:
                commandConfig = "uci set system.@system[0].timezone=" + timezone  # Set timezone on openwrt config (required for system reboot)
                commandCommitConfig = "uci commit system.@system[0].timezone"
                try:
                    subprocess.call(commandConfig, shell=True)
                    subprocess.call(commandCommitConfig, shell=True)
                except:
                    output = "ERR_CMD TIMEZONE"
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

