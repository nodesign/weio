import os, sys

files = os.listdir(sys.argv[1])

for f in files:
    if not(".DS_Store" in f):
        print "file size on disk",f, os.path.getsize(sys.argv[1]+"/"+f)

