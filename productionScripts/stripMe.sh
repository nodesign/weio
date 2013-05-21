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
rm weioStripped.tar.bz2

# after all process to decompress type : tar -zxvf weioStripped.tar.gz
# make new dir for stripped version at level -1
mkdir weioStripped 

# copy all visible files, ignore unvisible git files
rsync -av --exclude=".*" ../ weioStripped

# strip uds_main
rm weioStripped/uds*

# delete production scripts
rm -r weioStripped/productionScripts

# strip boostrap
rm -r weioStripped/clientDependencies/bootstrap/docs
rm -r weioStripped/clientDependencies/bootstrap/js/tests
rm -r weioStripped/clientDependencies/bootstrap/node_modules
rm -r weioStripped/clientDependencies/bootstrap/less/tests
rm weioStripped/clientDependencies/bootstrap/less/*.less
rm weioStripped/clientDependencies/bootstrap/*

# font awesome
rm -r weioStripped/clientDependencies/Font-Awesome/docs

# ace

rm weioStripped/clientDependencies/ace/mode-abap.js
rm weioStripped/clientDependencies/ace/mode-asciidoc.js
rm weioStripped/clientDependencies/ace/mode-c_cpp.js
rm weioStripped/clientDependencies/ace/mode-c9search.js
rm weioStripped/clientDependencies/ace/mode-clojure.js
rm weioStripped/clientDependencies/ace/mode-coffee.js
rm weioStripped/clientDependencies/ace/mode-coldfusion.js
rm weioStripped/clientDependencies/ace/mode-csharp.js
rm weioStripped/clientDependencies/ace/mode-dart.js
rm weioStripped/clientDependencies/ace/mode-diff.js
rm weioStripped/clientDependencies/ace/mode-dot.js
rm weioStripped/clientDependencies/ace/mode-glsl.js
rm weioStripped/clientDependencies/ace/mode-golang.js
rm weioStripped/clientDependencies/ace/mode-groovy.js
rm weioStripped/clientDependencies/ace/mode-haml.js
rm weioStripped/clientDependencies/ace/mode-haxe.js
rm weioStripped/clientDependencies/ace/mode-jade.js
rm weioStripped/clientDependencies/ace/mode-java.js
rm weioStripped/clientDependencies/ace/mode-json.js
rm weioStripped/clientDependencies/ace/mode-jsp.js
rm weioStripped/clientDependencies/ace/mode-jsx.js
rm weioStripped/clientDependencies/ace/mode-latex.js
rm weioStripped/clientDependencies/ace/mode-less.js
rm weioStripped/clientDependencies/ace/mode-liquid.js
rm weioStripped/clientDependencies/ace/mode-lisp.js
rm weioStripped/clientDependencies/ace/mode-lua.js
rm weioStripped/clientDependencies/ace/mode-luapage.js
rm weioStripped/clientDependencies/ace/mode-lucene.js
rm weioStripped/clientDependencies/ace/mode-makefile.js
rm weioStripped/clientDependencies/ace/mode-markdown.js
rm weioStripped/clientDependencies/ace/mode-objectivec.js
rm weioStripped/clientDependencies/ace/mode-ocaml.js
rm weioStripped/clientDependencies/ace/mode-perl.js
rm weioStripped/clientDependencies/ace/mode-pgsql.js
rm weioStripped/clientDependencies/ace/mode-php.js
rm weioStripped/clientDependencies/ace/mode-powershell.js
rm weioStripped/clientDependencies/ace/mode-r.js
rm weioStripped/clientDependencies/ace/mode-rdoc.js
rm weioStripped/clientDependencies/ace/mode-rhtml.js
rm weioStripped/clientDependencies/ace/mode-ruby.js
rm weioStripped/clientDependencies/ace/mode-sass.js
rm weioStripped/clientDependencies/ace/mode-scad.js
rm weioStripped/clientDependencies/ace/mode-scala.js
rm weioStripped/clientDependencies/ace/mode-scss.js
rm weioStripped/clientDependencies/ace/mode-sh.js
rm weioStripped/clientDependencies/ace/mode-sql.js
rm weioStripped/clientDependencies/ace/mode-stylus.js
rm weioStripped/clientDependencies/ace/mode-svg.js
rm weioStripped/clientDependencies/ace/mode-tcl.js
rm weioStripped/clientDependencies/ace/mode-text.js
rm weioStripped/clientDependencies/ace/mode-textile.js
rm weioStripped/clientDependencies/ace/mode-typescript.js
rm weioStripped/clientDependencies/ace/mode-xml.js
rm weioStripped/clientDependencies/ace/mode-xquery.js
rm weioStripped/clientDependencies/ace/mode-yaml.js
rm weioStripped/clientDependencies/ace/theme-ambiance.js
rm weioStripped/clientDependencies/ace/theme-chaos.js
rm weioStripped/clientDependencies/ace/theme-chrome.js
rm weioStripped/clientDependencies/ace/theme-clouds_midnight.js
rm weioStripped/clientDependencies/ace/theme-clouds.js
rm weioStripped/clientDependencies/ace/theme-cobalt.js
rm weioStripped/clientDependencies/ace/theme-crimson_editor.js
rm weioStripped/clientDependencies/ace/theme-dawn.js
rm weioStripped/clientDependencies/ace/theme-dreamweaver.js
rm weioStripped/clientDependencies/ace/theme-eclipse.js
rm weioStripped/clientDependencies/ace/theme-github.js
rm weioStripped/clientDependencies/ace/theme-idle_fingers.js
rm weioStripped/clientDependencies/ace/theme-kr.js
rm weioStripped/clientDependencies/ace/theme-merbivore_soft.js
rm weioStripped/clientDependencies/ace/theme-merbivore.js
rm weioStripped/clientDependencies/ace/theme-mono_industrial.js
rm weioStripped/clientDependencies/ace/theme-monokai.js
rm weioStripped/clientDependencies/ace/theme-pastel_on_dark.js
rm weioStripped/clientDependencies/ace/theme-solarized_dark.js
rm weioStripped/clientDependencies/ace/theme-solarized_light.js
rm weioStripped/clientDependencies/ace/theme-tomorrow_night_blue.js
rm weioStripped/clientDependencies/ace/theme-tomorrow_night_bright.js
rm weioStripped/clientDependencies/ace/theme-tomorrow_night_eighties.js
rm weioStripped/clientDependencies/ace/theme-tomorrow_night.js
rm weioStripped/clientDependencies/ace/theme-tomorrow.js
rm weioStripped/clientDependencies/ace/theme-twilight.js
rm weioStripped/clientDependencies/ace/theme-vibrant_ink.js
rm weioStripped/clientDependencies/ace/theme-xcode.js
rm weioStripped/clientDependencies/ace/worker-coffee.js
rm weioStripped/clientDependencies/ace/worker-json.js
rm weioStripped/clientDependencies/ace/worker-xquery.js

# change web socket address from localhost to weio.local
sed 's/localhost:8081/weio.local:8081/' weioStripped/clientDependencies/weio/weioApi.js > out
mv out weioStripped/clientDependencies/js/weioApi.js

sed 's/localhost:8081/weio.local:8081/' weioStripped/editor/index.html > out
mv out weioStripped/editor/index.html

# rename to weio
mv weioStripped/ weio

# make tar archive 
# tar -zcvf weioStripped.tar.gz weioStripped/

# MAXIMUM COMPRESSION
tar cf - weio/ | bzip2 -9 - > weioStripped.tar.bz2 

# delete stripped folder
rm -r weio/

# to decompress type : tar -zxvf weioStripped.tar.gz