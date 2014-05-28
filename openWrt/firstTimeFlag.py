# configuration file
import json
import sys

def getConfiguration(path):
    inputFile = open(path, 'r')
    rawData = inputFile.read()
    inputFile.close()
    return json.loads(rawData)

def saveConfiguration(path, conf):
    inputFile = open(path, 'w')
    print(inputFile)
    ret = inputFile.write(json.dumps(conf, indent=4, sort_keys=True))
    inputFile.close()

config = getConfiguration(sys.argv[1])
config['first_time_run'] = "YES"
config['port'] = 8080
config['userAppPort'] = 80
config['debug_mode'] = "False"
config['extern_projects_path'] = "/weioUser/userProjects"
config['absolut_root_path']= "/weio"
saveConfiguration(sys.argv[1], config)