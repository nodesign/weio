import socket
import urllib
import re
import subprocess


def getLocalIpAddress() :
    """Gets local ip address"""
    cmd = "ifconfig wlan0 | grep 'inet addr:' | cut -d: -f2 | awk '{print $1}'"
    return subprocess.check_output(cmd, shell=True)
    
def getPublicIpAddress() :
    """Gets world ip address. TODO test if internet is reachable"""
    f = urllib.urlopen("http://www.canyouseeme.org/")
    html_doc = f.read()
    f.close()
    ipAddress = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)

    #response = urllib.urlopen('http://api.hostip.info/get_html.php?ip=' + ipAddress.group(0) + '&position=true').read()
    return urllib.urlopen('http://api.hostip.info/get_html.php?ip=' + ipAddress.group(0)).read()
    
