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


def getConfiguration():
    inputFile = open("config.weio", 'r')
    rawData = inputFile.read()
    inputFile.close()
    return json.loads(rawData)


def saveConfiguration(conf):
    inputFile = open("config.weio", 'w')
    print(inputFile)
    ret = inputFile.write(json.dumps(conf, indent=4, sort_keys=True))
    inputFile.close()
    
 
#example & test configuration 
# weioConfig = {}
# weioConfig['user_projects_path'] = 'userProjects/'
# weioConfig['last_opened_project'] = 'myFirstProject/'
# weioConfig['last_opened_files'] = ['index.html', 'weioMain.py']
# weioConfig['editor_html_path'] = 'editor/editor.html'
# weioConfig['preview_html_path'] = 'preview/preview.html'
# weioConfig['dependencies_path'] = 'clientDependencies'
# weioConfig['weio_lib_path'] = 'weioLib'
# weioConfig['absolut_root_path'] = '/tmp/weio'
# weioConfig['port'] = 8081
# weioConfig['ip'] = '0.0.0.0'
# 
# # 
# saveConfiguration(weioConfig)
# a = getConfiguration()
# print a['user_projects_path']
