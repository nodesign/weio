import hashlib, sys, os, json

# Get MD5 checksum from file
def getMd5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
    return md5.hexdigest()

def checkIfFileExists(path):
    if (os.path.exists(path)) :
        return True
    else :
        return False

def saveConfiguration(path, conf):
    inputFile = open(path+"/updateWeio.json", 'w')
    print(inputFile)
    ret = inputFile.write(json.dumps(conf, indent=4, sort_keys=True))
    inputFile.close()


if (len(sys.argv)==3):

    directoryPath = sys.argv[1]
    version = sys.argv[2]

    # check if file exists :
    if (checkIfFileExists(directoryPath)):
        # path exists
        recipePath = directoryPath+"recipe"
        recoveryPath = directoryPath+"weio_recovery.bin"

        # Put all relevant files here for update
        weioRecipe = {}
        weioRecipe['download_url'] = 'http://we-io.net/downloads/'+version+"/recipe"
        weioRecipe['version'] = version
        weioRecipe['md5'] = getMd5sum(recipePath)
        weioRecipe['size'] = os.path.getsize(recipePath)
        weioRecipe['title'] = "Update to " + version 
        weioRecipe['body'] = "This is a brand new version of WeIO great software"

        weioRecovery = {}
        weioRecovery['download_url'] = 'http://we-io.net/downloads/'+version+"/weio_recovery.bin"
        weioRecovery['md5'] = getMd5sum(recoveryPath)
        weioRecovery['size'] = os.path.getsize(recoveryPath)

        weioConfig = {"recipe":weioRecipe, "recovery":weioRecovery}
        saveConfiguration(directoryPath, weioConfig)
    else :
            print "Filename is incorrect! Please provide valid path and filename"
else:
    print "Enter filename of your binary first then version number (for example /somePath/weio_recovery.bin v1.2)"