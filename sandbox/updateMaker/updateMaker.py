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

# configuration file
import json
import sys
import hashlib
import ftplib
import os
import getpass

# store ftp username from keyboard input
global usr
# store ftp password from keyboard input
global pswd
# file size to be uploaded
global filesize
# progress bar of uloading file
global prgs

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
    file = open(filename,'rb')                  # file to send
    session.cwd('www/downloads')
    session.storbinary('STOR ' + filename, file, callback = progressBar, blocksize = 1024)     # send the file
    file.close()                                    # close file and FTP
    session.quit()
# percent of uploaded data, callback
def progressBar(block):
    global prgs
    prgs += len(block)
    sys.stdout.write("%s%%      %s"%(str(int((100.0/filesize)*prgs)),"\r"))
    
# example of default configuration    
weio_update = {}
weio_update['description'] = 'Bug fixes in architecture and design'
weio_update['version'] = '0.12'
weio_update['whatsnew'] = 'long text maybe from some file'
weio_update['url'] = 'http://www.we-io.net/downloads/weio' + weio_update['version'] + '.tar.gz'
weio_update['md5'] = '995884813e29f06b71a940975b202398'


if (len(sys.argv)==4) :
    weio_update['version'] = sys.argv[1]
    weio_update['description'] = sys.argv[2]
    weio_update['url'] = 'http://www.we-io.net/downloads/' + sys.argv[3]
    weio_update['md5'] = md5sum(sys.argv[3])
    weio_update['whatsnew'] = open('releases.weio', 'r').read()

    saveConfiguration(weio_update)
    
    print "Connecting to WeIO Ftp server"
    print "CTR-C to exit without uploading files"
    usr = raw_input("Username :")
    pswd = getpass.getpass(prompt="Password :")
    try :
        
        print "Uploading " + sys.argv[3] + " ..."
        prgs = 0
        filesize = os.path.getsize(sys.argv[3])
        uploadToServer(sys.argv[3])
        print "Uploading update.weio ..."
        prgs = 0
        filesize = os.path.getsize("update.weio")
        uploadToServer("update.weio")
        print "Uploading releases.weio ..."
        prgs = 0
        filesize = os.path.getsize("releases.weio")
        uploadToServer("releases.weio")
        print "Done uploading"
    except ValueError:
        print ValueError
        print "Upload didn't make it."
    
else :
    print 
    print "WeIO update maker : [version] [description] [file]"
    print "Store release information in releases.txt file"
    print "example : ./updateMaker 0.12 'some bug fixes' weioStripped0.12.tar.bz2"
    print


