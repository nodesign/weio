# encoding: utf-8
"""
WeioAPIbridge.py

Created by Uros Petrevski on 2013-05-05.
Copyright (c) 2013 Nodesign.net. All rights reserved.
"""

# -*- coding: utf-8 -*-
import subprocess
import os, signal
import socket
import functools
import errno
import os
from tornado import web, ioloop, iostream

import tornado_subprocess

from sockjs.tornado import SockJSRouter, SockJSConnection
import json
import ast

from weioLib import weio_gpio
from weioLib import weio_globals


class WeioAPIBridgeHandler(SockJSConnection):
    
    """Opens editor route."""
    def on_open(self, data):
        """On open asks weio for last saved project. List of files are scaned and sent to editor.
        Only contents of weio_main.py is sent at first time"""
        print "Opened WEIO API socket"
        
        
        
    def on_message(self, data):
        self.serve(data)
        
    def serve(self, request) :
        
        rq = ast.literal_eval(request)
        
        if 'digitalWrite' in rq['request'] :
            
            ins = rq['data']
            weio_gpio.digitalWrite(str(ins[0]), str(ins[1]))
            #print ins
            
        elif 'pinMode' in rq['request'] :
            ins = rq['data']
            weio_gpio.digitalWrite(ins[0], ins[1])
