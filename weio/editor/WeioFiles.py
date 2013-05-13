# Uros Petrevski, Nodesign.net 2013
import os



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
    
    for dirname, dirnames, filenames in os.walk('./static/user_weio'):
        # print path to all subdirectories first.
        for subdirname in dirnames:
            #print os.path.join(dirname, subdirname)
            allFolders.append(os.path.join(dirname, subdirname))
    
        # print path to all filenames.
        index = 0
        for filename in filenames:
            #ignore this mac shit, TODO delete this condition when porting to electronics
            if (".DS_Store"!= filename) :
                #allFiles.append(os.path.join(dirname, filename))
                if ".html" in filename :
                    allFiles.append({'name': filename, 'id' : index, 'type' : "html", 'path' : os.path.join(dirname, filename), 'lastLinePosition' : 0})
                elif ".py" in filename :
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