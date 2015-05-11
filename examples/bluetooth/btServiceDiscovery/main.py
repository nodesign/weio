from weioLib.weio import *
import bluetooth
from subprocess import Popen, PIPE

def setup():

    # Reset BT and make sure that BT is UP
    execute("hciconfig hci0 down")
    execute("hciconfig hci0 up")
    result = execute("hciconfig")
    print result
    if ("UP RUNNING" in result):
       attach.process(myProcess)
    
def myProcess():
    print("Please wait while searching for BT services")
    
    # address None means to search all
    services = bluetooth.find_service(address=None)
    
    if len(services) > 0:
        print("Found " + str(len(services)) + " services")
    else:
        print("no services found")
    
    for svc in services:
        print("Service Name: %s"    % svc["name"])
        print("    Host:        %s" % svc["host"])
        print("    Description: %s" % svc["description"])
        print("    Provided By: %s" % svc["provider"])
        print("    Protocol:    %s" % svc["protocol"])
        print("    channel/PSM: %s" % svc["port"])
        print("    svc classes: %s "% svc["service-classes"])
        print("    profiles:    %s "% svc["profiles"])
        print("    service id:  %s "% svc["service-id"])
        print()

# Will be called on stop button
def stop():
    # Stopping BT
    execute("hciconfig hci0 down")

def execute(cmd): # cmd is string like in command line
    proc = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE)
    s = proc.communicate()
    # return console output
    return s[0]
    