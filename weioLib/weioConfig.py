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
# configuration file
import json
import os.path


def getConfiguration():
    inputFile = open("config.weio", 'r')
    passFile = None
    passRead = None
    if (os.path.isfile("pass.weio")):
        passFile = open("pass.weio", 'r')
        passRead = json.loads(passFile.read())
        passFile.close()
    else :
        print "Error, password file don't exist"
    
    rawData = inputFile.read()
    
    conf = json.loads(rawData)
    if not(passRead is None):
        conf["password"] = passRead["password"]
    else :
        conf["password"] = None

    inputFile.close()
    
    
    return conf 


def saveConfiguration(conf):
    inputFile = open("config.weio", 'w')
    passFile = open("pass.weio", 'w')
    
    pswd = {}
    pswd["password"] = conf["password"]
    
    passFile.write(json.dumps(pswd, indent=4, sort_keys=True))
    passFile.close()
    
    del conf["password"]
    
    #print(inputFile)
    ret = inputFile.write(json.dumps(conf, indent=4, sort_keys=True))
    inputFile.close()
    
 
#example & test configuration 
# weioConfig = {}
# weioConfig['last_opened_project'] = 'myFirstProject/'
# weioConfig['last_opened_files'] = ['index.html', 'weioMain.py']
# weioConfig['editor_html_path'] = 'editor/editor.html'
# weioConfig['preview_html_path'] = 'preview/preview.html'
# weioConfig['dependencies_path'] = 'clientDependencies'
# weioConfig['weio_lib_path'] = 'weioLib'
# weioConfig['absolut_root_path'] = '/tmp/weio'
# weioConfig['port'] = 8081
# weioConfig['ip'] = '0.0.0.0'
# 
# # 
# saveConfiguration(weioConfig)
# a = getConfiguration()
