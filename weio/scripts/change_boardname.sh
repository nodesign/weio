#!/bin/sh

BOARD=$1

# Change hostname
#sed "s/^.*option hostname.*/\toption hostname '$BOARD'/" -i /etc/config/system

# Change avahi configuration
sed "s/host-name=.*/host-name=$BOARD/" -i /etc/avahi/avahi-daemon.conf

# Restart avahi
/etc/init.d/avahi-daemon restart

# Restart networking
#/etc/init.d/network restart

# Restart ssh
#/etc/init.d/dropbear restart


