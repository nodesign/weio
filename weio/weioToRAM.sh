#!/bin/bash

# decompress to RAM
cp weioStripped.tar.bz2 /tmp

cd /tmp
tar -zxvf weioStripped.tar.bz2
rm weioStripped.tar.bz2
