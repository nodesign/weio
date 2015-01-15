#!/usr/bin/env python
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
import sys
import hashlib
import ftplib
import os
import getpass
from subprocess import Popen
from subprocess import PIPE
import urllib


# store ftp username from keyboard input
global usr
# store ftp password from keyboard input
global pswd
# file size to be uploaded
global filesize
# progress bar of uloading file
global prgs

packetFile = "weio.tar.gz"

# save update config file
def saveConfiguration(conf):
    inputFile = open("update.weio", 'w')
    print(inputFile)
    ret = inputFile.write(json.dumps(conf, indent=4, sort_keys=True))
    inputFile.close()

# md5 checksum
def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
            md5.update(chunk)
    return md5.hexdigest()
    
# upload file to server
def uploadToServer(filename):    
    session = ftplib.FTP('ftp.we-io.net',usr,pswd)
    print "Connected to ftp"
    file = open(filename,'rb')                  # file to send
    session.cwd('www/downloads')
    
    # TODO basename filename
    session.storbinary('STOR ' + filename, file, callback = progressBar, blocksize = 1024)     # send the file
    #session.storbinary("STOR " + packetFile, file)
    file.close()                                    # close file and FTP
    session.quit()

# percent of uploaded data, callback
def progressBar(block):
    global prgs
    prgs += len(block)
    sys.stdout.write("%s%%      %s"%(str(int((100.0/filesize)*prgs)),"\r"))

# Check actual version on the server
def checkVersionOnServer():
    config = getConfigJson()
    url = config["weio_update_repository"]
    opener = urllib.FancyURLopener({})
    f = opener.open(url+"/update.weio")
    ver = json.loads(f.read())

    print "Actual version on the server is : ", ver['version']
    print

def getConfigJson():
    inputFile = open("../config.weio", 'r')
    rawData = inputFile.read()
    inputFile.close()
    return json.loads(rawData)

# example of default configuration    
weio_update = {}
weio_update['description'] = 'Bug fixes in architecture and design'
weio_update['version'] = '0.12'
weio_update['whatsnew'] = 'long text maybe from some file'
weio_update['url'] = 'http://www.we-io.net/downloads/weio' + weio_update['version'] + '.tar.gz'
weio_update['md5'] = '995884813e29f06b71a940975b202398'

nArguments = 4
noFTP = False
if (len(sys.argv)>=nArguments) :
    
    print
    checkVersionOnServer()
    print
    print "Connecting to WeIO Ftp server"

    for a in sys.argv:
        if (a == "local"):
            noFTP = True
 
    if (noFTP is False):
        usr = raw_input("Username :")
        pswd = getpass.getpass(prompt="Password :")

    print "Open config.weio"
    config = getConfigJson()
    
    # Overwrite local configuration file
    config["weio_version"] = sys.argv[1]
    config["port"] = 8080
    config["userAppPort"] = 80
    config["debug_mode"] = "False"
    config["extern_projects_path_flash"] = "/weioUser/flash"
    
    inputFile = open("../config.weio", 'w')
    ret = inputFile.write(json.dumps(config, indent=4, sort_keys=True))
    inputFile.close()
    print "Apply modifications and close config.weio"
    print "Run script"
    # Run strip script
    p = Popen(["sh", "../productionScripts/stripMe.sh"], stdout=PIPE, close_fds=True)
    # wait... I have to finish this process before sending
    p.communicate()
    print "Finished process"
    
    
    # Revert port in local conf file
    config["port"] = 8080
    config["userAppPort"] = 8082
    config["debug_mode"] = "True"
    config["extern_projects_path_flash"] = "/Users/uros/workNow/nodesign/weIO/weio/weioUser/flash"
    inputFile = open("../config.weio", 'w')
    ret = inputFile.write(json.dumps(config, indent=4, sort_keys=True))
    inputFile.close()
    
    if (os.path.exists(packetFile)) :
        
        weio_update['version'] = sys.argv[1]
        weio_update['description'] = sys.argv[2]
        url = config["weio_update_repository"]
        weio_update['url'] = url + '/' + packetFile
        weio_update['md5'] = md5sum(packetFile)
        weio_update['whatsnew'] = open('releases.weio', 'r').read()
        weio_update['kill_flag'] = "NO"

        if (len(sys.argv)>=3):
            weio_update['install_duration'] = sys.argv[3]
        else:
            weio_update['install_duration'] = 75

        saveConfiguration(weio_update)

        if (noFTP is False):
            try :

                print "Uploading " + packetFile + " ..."
                prgs = 0
                filesize = os.path.getsize(packetFile)
                uploadToServer(packetFile)
                print "Uploading update.weio ..."
                prgs = 0
                filesize = os.path.getsize("update.weio")
                uploadToServer("update.weio")
                print "Uploading releases.weio ..."
                prgs = 0
                filesize = os.path.getsize("releases.weio")
                uploadToServer("releases.weio")
                print "Done uploading"
                print
                checkVersionOnServer()
                size = os.path.getsize(packetFile)/1000
                print "File size of the packet : " + str(size) + " kb"

            except ValueError:
                print ValueError
                print "Upload didn't make it."
        else:
               print "Not sending to FTP local version is made"
    
else :
    print 
    print "WeIO update maker : [version] [description] [seconds needed for install] [local]"
    print "local opetion means that archive won't be sent to FTP server"
    print "Store release information in releases.txt file"
    print "example : ./updateMaker 0.12 'some bug fixes'"
    print
    checkVersionOnServer()
    