#!/usr/bin/python -u
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
# All rights not explicitly granted in the BSD license are reserved.
# See the included LICENSE file for more details.
#
###

import weioConfig
import weioFiles
import weioRunnerGlobals
import weioParser
import weioUserApi
import weioIO
import weioGpio

import imp
import threading


class weioControl(object):
    ###
    # Connect to UPER
    ###
    def init(self):
        # Init GPIO object for uper communication
        if (weioRunnerGlobals.WEIO_SERIAL_LINKED == False):
            try:
                weioIO.gpio = weioGpio.WeioGpio()
            except:
                print "LPC coprocessor is not present"
                weioIO.gpio = None

    ###
    # Load user module and start threads
    ###
    def start(self):

        # Get configuration from file
        confFile = weioConfig.getConfiguration()
        
        # Path of last opened project
        lp = confFile["absolut_root_path"] + '/' + confFile["last_opened_project"] + "/main.py"

        print "MODULE: ", lp

        # Check if main.py exists in current user project
        if (weioFiles.checkIfFileExists(lp)):
            #print "projectModule = ", projectModule
            pass
        else:
            print "Does not exist!"
            # Use the location of default www/defaultMain/main.py
            projectModule = confFile["absolut_root_path"] + '/' + "www/defaultMain/main.py"

        try:
            #userMain = __import__(projectModule, fromlist=[''])
            userMain = imp.load_source('mainModule', lp)

            # Calling user setup() if present
            if "setup" in vars(userMain):
                userMain.setup()
        except:
            print "MODULE CAN'T BE LOADED." \
                    "Maybe you have some errors in modules that you wish to import?"

        # Add user callback handlers for events
        for key in weioUserApi.attach.events:
            weioParser.addUserEvent(weioUserApi.attach.events[key].event,
                    weioUserApi.attach.events[key].handler)

        # Launching threads
        for key in weioUserApi.attach.procs:
            print key
            t = threading.Thread(target=weioUserApi.attach.procs[key].procFnc,
                        args=weioUserApi.attach.procs[key].procArgs)
            t.daemon = True
            t.start()

            weioRunnerGlobals.WEIO_SERIAL_LINKED = True

    ###
    # execute()
    ###
    def execute(self, req):
        if req['request'] in weioParser.weioSpells or req['request'] in weioParser.weioUserSpells:
            if req['request'] in weioParser.weioSpells:
                res = weioParser.weioSpells[req['request']](req['data'])
            elif req['request'] in weioParser.weioUserSpells:
                res = weioParser.weioUserSpells[req['request']](req['data'])
        else:
            res = None

        return res

    ###
    # stop()
    ###
    def stop(self):
        if (weioIO.gpio != None):
            if (weioRunnerGlobals.WEIO_SERIAL_LINKED == True):
                weioIO.gpio.stopReader()
                weioIO.gpio.reset()
