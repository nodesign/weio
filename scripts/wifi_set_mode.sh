#!/bin/sh
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
fi

if [ $1 == "ap" ]; then
    # Down the WiFi before reconfiguration
    wifi down

    # Copy AP files
    cp /etc/config/network.ap /etc/config/network
    cp /etc/config/wireless.ap /etc/config/wireless

    cp /etc/config/dhcp.ap /etc/config/dhcp
    cp /etc/config/firewall.ap /etc/config/firewall

elif [ $1 == "rescue" ]; then
    # Down the WiFi before reconfiguration
    wifi down
    
    # Down Avahi deamon
    avahi-daemon -k
    
    # Copy AP files
    cp /etc/config/network.ap /etc/config/network
    cp /etc/config/wireless.ap.rescue /etc/config/wireless

    cp /etc/config/dhcp.ap /etc/config/dhcp
    cp /etc/config/firewall.ap /etc/config/firewall

elif [ $1 == "sta" ]; then
    # Down the WiFi before reconfiguration
    wifi down

    # Down Avahi deamon
    avahi-daemon -k
    
    # Copy STA files
    cp /etc/config/network.sta /etc/config/network
    cp /etc/config/wireless.sta /etc/config/wireless

    cp /etc/config/dhcp.sta /etc/config/dhcp
    cp /etc/config/firewall.sta /etc/config/firewall
else
    echo "Unknown mode : should be 'ap' or 'sta'"
    exit
fi

# Restart the services
/etc/init.d/network restart
#/etc/init.d/firewall restart
/etc/init.d/dnsmasq restart
avahi-daemon -D

