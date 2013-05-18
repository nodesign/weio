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

import os
import weio_config


def scanFolders() :
    """This function scans ./user_weio folder and all folders inside that folder in search for files.
    Recognized file formats are html, py, js, css, txt all other file formats will be called other
    
    scanFolders() returns dictionary. 
    
    Dictionary words are : allFiles
    Behind words there are arrays of filenames (strings)
    """
    #Dictionary words are : html, py, js, css, txt, other, allFiles, allFilesExceptOther, allFolders
    
    html = []
    py = []
    js = []
    css = []
    txt = []
    other = []

    allFiles = []
    allFolders = []
    
    confFile = weio_config.getConfiguration()
    
    pathToCurrentProject = confFile["user_projects_path"] + confFile['last_opened_project'] 
    
    for dirname, dirnames, filenames in os.walk(pathToCurrentProject):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            #print os.path.join(dirname, subdirname)
            allFolders.append(os.path.join(dirname, subdirname))
    
        # print path to all filenames.
        index = 0
        for filename in filenames:
            #ignore this mac shit, TODO delete this condition when porting to electronics
            if (".DS_Store" == filename) :
                continue
            
            #allFiles.append(os.path.join(dirname, filename))
            if ".html" in filename :
                allFiles.append({'name': filename, 'id' : index, 'type' : "html", 'path' : os.path.join(dirname, filename), 'lastLinePosition' : 0})
            elif ".py" in filename : # NASTY BUG CORRECTED, pyc is also identified here because "py" is in "pyc", solution is provided
                if ".pyc" in filename : # ignore this one
                    pass
                else :
                    allFiles.append({'name': filename, 'id' : index, 'type' : "python", 'path' : os.path.join(dirname, filename), 'lastLinePosition' : 0})
            elif ".js" in filename :
                allFiles.append({'name': filename, 'id' : index, 'type' : "javascript", 'path' : os.path.join(dirname, filename), 'lastLinePosition' : 0})
            elif ".css" in filename :
                allFiles.append({'name': filename, 'id' : index, 'type' : "css", 'path' : os.path.join(dirname, filename), 'lastLinePosition' : 0}) 
            elif ".txt" in filename :
                allFiles.append({'name': filename, 'id' : index, 'type' : "text", 'path' : os.path.join(dirname, filename), 'lastLinePosition' : 0})
            else :
                allFiles.append({'name': filename, 'id' : index, 'type' : "other", 'path' : os.path.join(dirname, filename), 'lastLinePosition' : 0})
            
            index = index+1
              
            # parse filenames and sort them into arrays
            # if ".html" in filename :
            #                 html.append({'name': os.path.join(dirname, filename), 'id' : os.path.join(dirname, filename), 'type' : "html"})
            #             elif ".py" in filename :
            #                 py.append({'name': os.path.join(dirname, filename), 'id' : os.path.join(dirname, filename), 'type' : "python"})
            #             elif ".js" in filename :
            #                 js.append({'name': os.path.join(dirname, filename), 'id' : os.path.join(dirname, filename), 'type' : "javascript"})
            #             elif ".css" in filename :
            #                 css.append({'name': os.path.join(dirname, filename), 'id' : os.path.join(dirname, filename), 'type' : "css"}) 
            #             elif ".txt" in filename :
            #                 txt.append({'name': os.path.join(dirname, filename), 'id' : os.path.join(dirname, filename), 'type' : "text"})
            #             else :
            #                 other.append({'name': os.path.join(dirname, filename), 'id' : os.path.join(dirname, filename), 'type' : "other"})
            #             
    #return {'html' : html, 'py' : py, 'js' : js, 'css' : css, 'txt' : txt,
    #        'other' : other, 'allFiles' : allFiles, 'allFilesExceptOther' : html+py+js+css+txt, 'allFolders' : allFolders}
    
    # to accelerate communication other words are excluded
    
    return {'allFiles' : allFiles}
    
def getRawContentFromFile(path):
    
    """This function reads contents from given filename and returns it. Be aware that this function
     can explore the whole OS. Use checkIfPathIsInUserFolder(path) function to check if path is in user
     only folder."""
    
    inputFile = open(path, 'r')
    rawData = inputFile.read()
    inputFile.close()
    return rawData
    
def saveRawContentToFile(path, data):
    
    """This function writes contents to given filename. Be aware that this function
     can explore the whole OS. Use checkIfPathIsInUserFolder(path) function to check if path is in user
     only folder."""
    
    inputFile = open(path, 'w')
    print(inputFile)
    ret = inputFile.write(data)
    inputFile.close()
    
        
def checkIfPathIsInUserFolder(path):
    
    """This function checks if given path is in user folder user_weio/"""
    
    if "./static/user_weio" in (path) :
        return True
    else :
        return False
        
#print(scanFolders())
