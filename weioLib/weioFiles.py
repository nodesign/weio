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


import weioConfig
from collections import namedtuple
import shutil

import os
from os import listdir, sep
from os.path import abspath, basename, isdir
import uuid
from shutil import move
import tarfile

import json

# IMPORT BASIC CONFIGURATION FILE
from weioLib import weioConfig

#from sys import argv


_ntuple_diskusage = namedtuple('usage', 'total used free')


def addNode(path):
    n = {}
    n['label'] = os.path.basename(path)
    n['children'] = []

    files = listdirFiltered(path)

    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            n['children'].append(f)
        elif os.path.isdir(os.path.join(path, f)):
            n['children'].append(addNode(os.path.join(path, f)))

    return n

def listdirFiltered(path):
    dirs = os.listdir(path)
    for f in dirs:
        if ( not (f == "www") and not f.startswith('.') and not f.endswith('.pyc') and not f.startswith('__init__') ):
            yield f

def getFileTree(path) :
    """Scans user folder and all folders inside that folder in search for files.
    Exports HTML string that can be directly used inside editor
    """
    # Chop the trailing slash to use os.path.basename()
    if (path[-1] == "/"):
        path = path[:-1]

    # get tree in a form of dictionary
    td = addNode(path)
    # jqtree demands list of dictionaries as a format
    t = []
    t.append(td)

    #print(json.dumps(t, indent=4, sort_keys=True))
    return t

def listOnlyFolders(path):
    """Scan only folders. This is useful to retreive all project from user projects"""

    print "AAA ############## ", path
    return os.walk(path).next()[1]

def getFileType(path):
    """Extracts file extension and matches with proper name"""
    if (os.path.exists(path)) :
        extension = os.path.splitext(path)[1]

        types = {
        ".css" : "css",
        ".py": "python",
        ".js": "javascript",
        ".html":"html",
        ".txt" : "text",
        ".md":"text",
        ".json": "json",
        ".svg": "svg",
        ".xml":"xml",
        ".less":"less",
        ".coffee":"coffee"
        }

        images = {
        ".png" : "png",
        ".jpg" : "jpg",
        ".gif" : "gif",
        ".bmp" : "bmp"
        }

        if (extension in types) :
            return types[extension]
        else :
            if (extension in images) :
                return "image"
            else:
                return "other"
    else:
        return None

def getFilenameFromPath(path):
    """Extracts filename from path"""
    if (os.path.exists(path)) :
        return os.path.basename(path)
    else:
        return None

def getStinoFromFile(path):
    """Returns st_ino of file. This is used for unique file id number"""
    if (os.path.exists(path)) :
        return os.stat(path).st_ino
    else:
        return None

def getRawContentFromFile(path):

    """Reads contents from given filename and returns it. Be aware that this function
     can explore the whole OS. Use checkIfPathIsInUserFolder(path) function to check if path is in user
     only folder."""
    if (os.path.exists(path)) :
        inputFile = open(path, 'r')
        rawData = inputFile.read()
        inputFile.close()
        return rawData
    else:
        return None

def saveRawContentToFile(path, data):
    """Writes contents to given filename. Be aware that this function
     can explore the whole OS. Use checkIfPathIsInUserFolder(path) function to check if path is in user
     only folder."""

    tmp = "./"+str(uuid.uuid1())+".tmp"

    try :
        inputFile = open(tmp, 'w')
        print(inputFile)
        ret = inputFile.write(data)
        inputFile.close()
    except NameError:
        print NameError
        os.remove(tmp)
        return -1

    move(tmp, path)
    return 0

def checkIfFileExists(path):
    if (os.path.exists(path)) :
        return True
    else :
        return False

def checkIfDirectoryExists(path):
    if (os.path.isdir(path)):
        return True
    else :
        return False

def removeFile(path):
    """Removes specified file, if folder path is passed folder will be deleted"""
    if (os.path.isfile(path)):
        os.remove(path)
    elif (os.path.isdir(path)):
        shutil.rmtree(path)
    else :
        return None

def removeDirectory(path):
    """Removes specified directory even if directory is not empty."""
    shutil.rmtree(path)

def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in Megabytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total/1000000, used/1000000, free/1000000)

def createDirectory(path):
    """Creates new directory at given path. Creates all subdirectories if needed"""
    if not os.path.isdir(path):
        os.makedirs(path)

def createTarfile(output_filename, source_dir):
    """Creates TAR archive for bundling projects"""

    # kill all .pyc files first
    filelist = [ f for f in os.listdir(source_dir) if f.endswith(".pyc") ]
    for f in filelist:
        os.remove(source_dir+f)

    # compress
    tar = tarfile.open(output_filename, "w:gz")
    tar.add(source_dir, arcname=os.path.basename(source_dir)) # arcname=os.path.basename(source_dir)
    tar.close()

def unTarFile(sourceFilePath, destination):
    """Decompresses Tar archive and create new project. Destroys archive file after"""
    tar = tarfile.open(sourceFilePath)
    tar.extractall(destination)
    tar.close()
    removeFile(sourceFilePath)

def symlinkExternalProjects():
    config = weioConfig.getConfiguration()

    # Examples
    if ( os.path.lexists(config["absolut_root_path"] + "/examples") ):
        # unlink then link to make sure that path is correct
        try:
            os.unlink("www/examples")
        except:
            print "Symlink don't exist. Will create new one for examples"
        os.symlink(config["absolut_root_path"] + "/examples", "www/examples")

    # Flash
    if (os.path.lexists(config["extern_projects_path_flash"])):
        # unlink then link to make sure that path is correct
        try:
            os.unlink("www/flash")
        except:
            print "Symlink don't exist. Will create new one for flash"
        os.symlink(config["extern_projects_path_flash"], "www/flash")

    # SD
    if (os.path.lexists(config["extern_projects_path_sd"])):
        try:
            os.unlink("www/sd")
        except:
            print "Symlink don't exist. Will create new one for sd"
        os.symlink(config["extern_projects_path_sd"], "www/sd")

    # USB Flash
    if (os.path.lexists(config["extern_projects_path_usbFlash"])):
        try:
            os.unlink("www/usbFlash")
        except:
            print "Symlink don't exist. Will create new one for usbFlash"
        os.symlink(config["extern_projects_path_usbFlash"], "www/usbFlash")

    # Re-link current project's www
    lastStorage = os.path.basename(os.path.dirname(config["last_opened_project"]))
    lastWww = config["last_opened_project"] + '/' + 'www'
    #print "LS ", lastStorage
    if (lastStorage != "sd" and lastStorage != "usbFlash"):
        if os.path.lexists(lastWww):
            try:
                os.unlink(lastWww)
            except:
                print "Symlink don't exist. Will create new one for www"
            if (len(config["last_opened_project"]) > 0):
                os.symlink(config["absolut_root_path"] + "/www", lastWww)

 
