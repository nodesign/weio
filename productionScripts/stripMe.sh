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
rm weioStripped/uds_weio_main

# delete production scripts
rm -r weioStripped/productionScripts

# strip boostrap
rm -r weioStripped/static/bootstrap/docs
rm -r weioStripped/static/bootstrap/js/tests
rm -r weioStripped/static/bootstrap/node_modules
rm -r weioStripped/static/bootstrap/less/tests
rm weioStripped/static/bootstrap/less/*.less
rm weioStripped/static/bootstrap/*

# font awesome
rm -r weioStripped/static/Font-Awesome/docs

# ace

rm weioStripped/static/ace/mode-abap.js
rm weioStripped/static/ace/mode-asciidoc.js
rm weioStripped/static/ace/mode-c_cpp.js
rm weioStripped/static/ace/mode-c9search.js
rm weioStripped/static/ace/mode-clojure.js
rm weioStripped/static/ace/mode-coffee.js
rm weioStripped/static/ace/mode-coldfusion.js
rm weioStripped/static/ace/mode-csharp.js
rm weioStripped/static/ace/mode-dart.js
rm weioStripped/static/ace/mode-diff.js
rm weioStripped/static/ace/mode-dot.js
rm weioStripped/static/ace/mode-glsl.js
rm weioStripped/static/ace/mode-golang.js
rm weioStripped/static/ace/mode-groovy.js
rm weioStripped/static/ace/mode-haml.js
rm weioStripped/static/ace/mode-haxe.js
rm weioStripped/static/ace/mode-jade.js
rm weioStripped/static/ace/mode-java.js
rm weioStripped/static/ace/mode-json.js
rm weioStripped/static/ace/mode-jsp.js
rm weioStripped/static/ace/mode-jsx.js
rm weioStripped/static/ace/mode-latex.js
rm weioStripped/static/ace/mode-less.js
rm weioStripped/static/ace/mode-liquid.js
rm weioStripped/static/ace/mode-lisp.js
rm weioStripped/static/ace/mode-lua.js
rm weioStripped/static/ace/mode-luapage.js
rm weioStripped/static/ace/mode-lucene.js
rm weioStripped/static/ace/mode-makefile.js
rm weioStripped/static/ace/mode-markdown.js
rm weioStripped/static/ace/mode-objectivec.js
rm weioStripped/static/ace/mode-ocaml.js
rm weioStripped/static/ace/mode-perl.js
rm weioStripped/static/ace/mode-pgsql.js
rm weioStripped/static/ace/mode-php.js
rm weioStripped/static/ace/mode-powershell.js
rm weioStripped/static/ace/mode-r.js
rm weioStripped/static/ace/mode-rdoc.js
rm weioStripped/static/ace/mode-rhtml.js
rm weioStripped/static/ace/mode-ruby.js
rm weioStripped/static/ace/mode-sass.js
rm weioStripped/static/ace/mode-scad.js
rm weioStripped/static/ace/mode-scala.js
rm weioStripped/static/ace/mode-scss.js
rm weioStripped/static/ace/mode-sh.js
rm weioStripped/static/ace/mode-sql.js
rm weioStripped/static/ace/mode-stylus.js
rm weioStripped/static/ace/mode-svg.js
rm weioStripped/static/ace/mode-tcl.js
rm weioStripped/static/ace/mode-text.js
rm weioStripped/static/ace/mode-textile.js
rm weioStripped/static/ace/mode-typescript.js
rm weioStripped/static/ace/mode-xml.js
rm weioStripped/static/ace/mode-xquery.js
rm weioStripped/static/ace/mode-yaml.js
rm weioStripped/static/ace/theme-ambiance.js
rm weioStripped/static/ace/theme-chaos.js
rm weioStripped/static/ace/theme-chrome.js
rm weioStripped/static/ace/theme-clouds_midnight.js
rm weioStripped/static/ace/theme-clouds.js
rm weioStripped/static/ace/theme-cobalt.js
rm weioStripped/static/ace/theme-crimson_editor.js
rm weioStripped/static/ace/theme-dawn.js
rm weioStripped/static/ace/theme-dreamweaver.js
rm weioStripped/static/ace/theme-eclipse.js
rm weioStripped/static/ace/theme-github.js
rm weioStripped/static/ace/theme-idle_fingers.js
rm weioStripped/static/ace/theme-kr.js
rm weioStripped/static/ace/theme-merbivore_soft.js
rm weioStripped/static/ace/theme-merbivore.js
rm weioStripped/static/ace/theme-mono_industrial.js
rm weioStripped/static/ace/theme-monokai.js
rm weioStripped/static/ace/theme-pastel_on_dark.js
rm weioStripped/static/ace/theme-solarized_dark.js
rm weioStripped/static/ace/theme-solarized_light.js
rm weioStripped/static/ace/theme-tomorrow_night_blue.js
rm weioStripped/static/ace/theme-tomorrow_night_bright.js
rm weioStripped/static/ace/theme-tomorrow_night_eighties.js
rm weioStripped/static/ace/theme-tomorrow_night.js
rm weioStripped/static/ace/theme-tomorrow.js
rm weioStripped/static/ace/theme-twilight.js
rm weioStripped/static/ace/theme-vibrant_ink.js
rm weioStripped/static/ace/theme-xcode.js
rm weioStripped/static/ace/worker-coffee.js
rm weioStripped/static/ace/worker-json.js
rm weioStripped/static/ace/worker-xquery.js

# change web socket address from localhost to weio.local
sed 's/localhost:8081/weio.local:8081/' weioStripped/static/weio/weioApi.js > out
mv out weioStripped/static/js/weioApi.js

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