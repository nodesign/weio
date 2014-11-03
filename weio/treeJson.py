# Import the os module, for the os.walk function
import os
import collections
import json

def tree(): return collections.defaultdict(tree)

def add(t, keys):
  for key in keys:
    t = t[key]

s = tree()

# Set the directory you want to start from
path = '.'

for root, dirs, files in os.walk(path):
    for f in files:
        l = root.split('/')
        l.append(f)

        add(s, l)

print(json.dumps(s, indent=4, sort_keys=True))

