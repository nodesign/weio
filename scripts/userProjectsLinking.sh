#!/bin/sh

# it creates all necessary structure
# TODO SD card support to be added

if [ ! -d "/weioUser" ]; then
    echo "Missing weioUser directory. Creating it"
    mkdir /weioUser
    mkdir -p /weioUser/flash/userProjects
    cp -r /weio/www/libs/weio/boilerPlate/ /weioUser/flash/userProjects/helloWorld
    touch /weioUser/flash/__init__.py
    touch /weioUser/flash/userProjects/__init__.py
fi
