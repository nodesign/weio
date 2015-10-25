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

    filePath = sys.argv[1]
    directoryPath = None

    version = sys.argv[2]

    # check if file exists :
    if (checkIfFileExists(filePath)):
        # path exists
        # extract directroy name for path where json will be created later
        directoryPath = os.path.dirname(filePath)
 
        weioConfig = {}
        weioConfig['download_url'] = 'http://we-io.net/downloads/'+version+"/weio_recovery.bin"
        weioConfig['version'] = version
        weioConfig['md5'] = getMd5sum(filePath)
        weioConfig['size'] = os.path.getsize(filePath)
        weioConfig['title'] = "Update to " + version 
        weioConfig['body'] = "This is a brand new version of WeIO great software"

        saveConfiguration(directoryPath, weioConfig)
    else :
            print "Filename is incorrect! Please provide valid path and filename"
else:
    print "Enter filename of your binary first then version number (for example /somePath/weio_recovery.bin v1.2)"