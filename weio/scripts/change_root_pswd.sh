#!/bin/sh
echo "setting root password"
echo -e "$1\n$1" | passwd
echo "setting weio user SMB password. Same as root password"
(echo "$1"; echo "$1") | smbpasswd -s -a weio
