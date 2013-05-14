# configuration file
import json


def getConfiguration():
    inputFile = open("config.weio", 'r')
    rawData = inputFile.read()
    inputFile.close()
    return json.loads(rawData)


def saveConfiguration(conf):
    inputFile = open("config.weio", 'w')
    print(inputFile)
    ret = inputFile.write(json.dumps(conf))
    inputFile.close()
    
 
#example & test configuration 
# weio_config = {}
# weio_config['user_projects_path'] = 'userProjects/'
# weio_config['last_opened_project'] = 'myFirstProject/'
# weio_config['last_opened_files'] = ['index.html', 'weio_main.py']
# weio_config['editor_html_path'] = 'editor/editor.html'
# weio_config['preview_html_path'] = 'preview/preview.html'
# weio_config['dependencies_path'] = 'clientDependencies'
# weio_config['weio_lib_path'] = 'weioLib'
# weio_config['absolut_root_path'] = '/tmp/weio'
# weio_config['port'] = 8081
# weio_config['ip'] = '0.0.0.0'
# 
# # 
# saveConfiguration(weio_config)
# a = getConfiguration()
# print a['user_projects_path']
