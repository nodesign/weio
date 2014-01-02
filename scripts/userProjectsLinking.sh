#!/bin/sh

# this script is checking if userWeio directroy exists with it's good symlinks and files
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

cd /weioUser
if [ ! -d "/weioUser/devices" ]; then
    echo "Missing link to devices directory. Creating symlink from /weio/devices"
    ln -s /weio/devices
fi

if [ ! -d "/weioUser/weioLib" ]; then
    echo "Missing link to weioLib directory. Creating symlink from /weio/weioLib"
    ln -s /weio/weioLib
fi

if [ ! -d "/weioUser/www" ]; then
    echo "Missing link to www directory. Creating symlink from /weio/www"
    ln -s /weio/www
fi

# cd /weio
# if [ ! -d "/weio/userProjects" ]; then
#     echo "Missing link to userProjects directory. Creating symlink from /weioUser/userProjects"
#     ln -s /weioUser/userProjects
# fi
cd /

