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

#from sys import argv


_ntuple_diskusage = namedtuple('usage', 'total used free')


def addNode(path):
    n = {}
    n['label'] = os.path.basename(path)
    n['children'] = []

    files = os.listdir(path)

    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            n['children'].append(f)
        elif os.path.isdir(os.path.join(path, f)):
            n['children'].append(addNode(os.path.join(path, f)))

    return n

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

    print(json.dumps(t, indent=4, sort_keys=True)) 
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
        
def checkIfPathIsInUserFolder(path):
    """Checks if given path is in user folder"""
    confFile = weioConfig.getConfiguration()
    pathToCurrentProject = confFile["user_projects_path"] + confFile['last_opened_project'] 
    
    if pathToCurrentProject in (path) :
        return True
    else :
        return False
        
def removeFile(path):
    """Removes specified file, if folder path is passed exception is rised"""
    if (os.path.exists(path)) :
        os.remove(path)
    else :
        return None

def removeDirectory(path):
    """Removes specified userProject directory even if directory is not empty. It will execute
        only in the case when path contains userProjects in its string"""
    if "userProjects" in path:
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
    
def recreateUserFiles():
    """Destroys userFiles directory than recreates it with good symlinks and __init__.py file. 
    UserFiles will be in the path that was defined inside config.weio file"""
    confFile = weioConfig.getConfiguration()
    targetPath = confFile["user_projects_path"] 
    if (checkIfDirectoryExists(targetPath)) :
        shutil.rmtree(targetPath)
    os.makedirs(targetPath)

    print "++++", targetPath
    
    if not(checkIfFileExists(targetPath + "__init__.py" )):
        f = open(targetPath+"__init__.py", 'w')
        f.write("")
        f.close()
        
    if (checkIfDirectoryExists(confFile["extern_projects_path"])):
        links = listUserDirectories(confFile["extern_projects_path"])
        for l in links:
            os.symlink(l, targetPath+os.path.basename(l))
            
            if not(checkIfFileExists(l+"/userProjects/require.js")):
                shutil.copyfile(confFile["absolut_root_path"]+"/www/libs/require.js", l+"/userProjects/require.js")
                
            #if not(os.path.islink(l+"/userProjects/require.js")):
            #    os.symlink(confFile["absolut_root_path"]+"/www/libs/require.js", l+"/userProjects/require.js")
            
        # for examples is manual treatement and symlink require.js
        os.symlink(confFile["absolut_root_path"] + "/examples", targetPath+"examples")
        if not(os.path.islink(targetPath+"examples"+"/userProjects/require.js")):
            os.symlink(confFile["absolut_root_path"]+"/www/libs/require.js", targetPath+"examples"+"/userProjects/require.js")
    
    

#print listUserDirectories("/Users/uros/workNow/nodesign/weIO/weio/weioUser/")
#recreateUserFiles()
#print listUserDirectories("/weioUser/")
#def makeSymLinksToUserDirs

#print(scanFolders())
