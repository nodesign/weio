#!/bin/bash

# Update package base
./scripts/feeds update

# Install base packages
./scripts/feeds install

# Install additional packages
./scripts/feeds install python
./scripts/feeds install avahi-daemon
./scripts/feeds install ntpd
./scripts/feeds install motion
./scripts/feeds install mjpg-streamer
./scripts/feeds install fswebcam
./scripts/feeds install libv4l
./scripts/feeds install libi2c
./scripts/feeds install i2c-tools
./scripts/feeds install python-smbus
