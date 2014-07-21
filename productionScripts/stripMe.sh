#!/bin/bash

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


# clean old file
#rm weio.tar.bz2

if [ -d weio ]; then
    rm -r weio
fi

# after all process to decompress type : tar -zxvf weio.tar.gz
# make new dir for stripped version at level -1
mkdir weio 

# copy all visible files, ignore unvisible git files
rsync -av --exclude=".*" --exclude="productionScripts" ../ weio

# exclude production folders
rm -r weio/doc
rm -r weio/graphicsSource
rm -r weio/openWrt
rm -r weio/sandbox
rm -r weio/updateMaker
rm weio/README.md

# exclude local dependant symlinks that will break
rm -r weio/userFiles/examples
rm -r weio/userFiles/flash
rm weio/examples/userProjects/require.js

# kill all .pyc files to leave native arch to build them
find weio -name '*.pyc' -delete
# kill all .less files because they are compiled to .css
find weio -name '*.less' -delete
# kill all OS X crap
find weio -name '.DS_Store' -delete

# compress in every case
tar -zcvf weio.tar.gz weio/

echo "WeIO stripped and compressed"
tar -zcvf weio.tar.gz weio/
# kill weio folder
rm -r weio

# To decompress type : tar -zxvf weio.tar.gz

echo ""
echo "Created archive weio.tar.gz"
echo ""
echo "Now do:"
echo "$ scp -r weio.tar.gz root@weio.local:/tmp"
echo "and then in WeIO:"
echo "tar -xzvf /tmp/weio.tar.gz"

# make tar archive 
# if [ "$1" == "no_compression" ]; then
#     echo "WeIO stripped no compression is executed"
# else
#     echo "Patching WeIO project for production"
#     #patch weio/www/libs/weio/weioApi.js < 01_portChange.patch
#
#     echo "WeIO stripped and compressed"
#     tar -zcvf weio.tar.gz weio/
#     # kill weio folder
#     rm -r weio
#
#     # To decompress type : tar -zxvf weio.tar.gz
#
#     echo ""
#     echo "Created archive weio.tar.gz"
#     echo ""
#     echo "Now do:"
#     echo "$ scp -r weio.tar.gz root@weio.local:/tmp"
#     echo "and then in WeIO:"
#     echo "tar -xzvf /tmp/weio.tar.gz"
#
# fi



