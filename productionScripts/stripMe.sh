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
# This file is part of WEIO and is published under BSD license.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by the WeIO project.
# 4. Neither the name of the WeIO nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY WEIO PROJECT AUTHORS AND CONTRIBUTORS ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL WEIO PROJECT AUTHORS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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



