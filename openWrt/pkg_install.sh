#!/bin/bash

# Update package base
./scripts/feeds update

# Install base packages
./scripts/feeds install

# Install additional packages
./scripts/feeds install python
./scripts/feeds install avahi-daemon
./scripts/feeds install ntpd
./scripts/feeds install mjpg-streamer
./scripts/feeds install fswebcam
./scripts/feeds install libv4l
./scripts/feeds install libi2c
./scripts/feeds install i2c-tools
./scripts/feeds install python-smbus
./scripts/feeds install madplay
./scripts/feeds install alsa-lib
./scripts/feeds install alsa-utils
./scripts/feeds install cython
./scripts/feeds install gevent
./scripts/feeds install bluez-libs
./scripts/feeds install bluez-utils
./scripts/feeds install python-bluez
./scripts/feeds install bluez-hcidump

