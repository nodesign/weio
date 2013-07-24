#! /usr/bin/env python

# tree.py
#
# Written by Doug Dahms
#
# Prints the tree structure for the path specified on the command line

from os import listdir, sep
from os.path import abspath, basename, isdir
from sys import argv

global htmlTree
htmlTree = "<li>"

def tree(dir, padding, print_files=True):
    global htmlTree
    #print padding[:-1] + '<label for="folder">' + basename(abspath(dir)) + '/' + "</label><input type='checkbox' id='folder1' />" 
    htmlTree+=padding[:-1] + '<label for="folder">' + basename(abspath(dir)) + '/' + "</label><input type='checkbox' id='folder1' />"
    htmlTree+="\n"
    #print "<ol>"
    htmlTree+="<ol>"
    htmlTree+="\n"
    padding = padding + ' '
    files = []
    if print_files:
        files = listdir(dir)
    else:
        files = [x for x in listdir(dir) if isdir(dir + sep + x)]
    count = 0
    for file in files:
        count += 1
        #print padding
        htmlTree+=padding
        htmlTree+="\n"
        path = dir + sep + file 
        if isdir(path):
            if count == len(files):
                #print "<li>"
                htmlTree+="<li>"
                htmlTree+="\n"
                tree(path, padding + '  ', print_files)
                #print "</li>"
                htmlTree+="</li>"
                htmlTree+="\n"
            else:
                #print "<li>"
                htmlTree+="<li>"
                htmlTree+="\n"
                tree(path, padding + ' ', print_files)
                #print "</li>"
                htmlTree+="</li>"
                htmlTree+="\n"
        else:
            #print padding + '<li class="file"><a href="">' + file + '</a></li>'
            htmlTree+=padding + '<li class="file"><a href="">' + file + '</a></li>'
            htmlTree+="\n"
    
    #print "</ol>"
    htmlTree+="</ol>"
    htmlTree+="\n"
    
def getTree() :
    global htmlTree
    tree(".", " ")
    htmlTree+="</li>"
    return htmlTree
    
    