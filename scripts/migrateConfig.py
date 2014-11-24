#!/usr/bin/python

import json

def getConfiguration(path):
    inputFile = open(path, 'r')
    rawData = inputFile.read()
    inputFile.close()
    return json.loads(rawData)


def saveConfiguration(path, conf):
    inputFile = open(path, 'w')
    ret = inputFile.write(json.dumps(conf, indent=4, sort_keys=True))
    inputFile.close()

print "Running migration program"
# Open old config file here
oldConfig = getConfiguration("/tmp/config.weio")
newConfig = getConfiguration("/weio/config.weio")

for parameter in newConfig:
    if (parameter in oldConfig):
        if not("weio_version" in parameter): # don't take the old version of sw, just migrate personal data
            newConfig[parameter] = oldConfig[parameter]

saveConfiguration("/weio/config.weio", newConfig)
