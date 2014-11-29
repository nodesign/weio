#######################################
#                                     #
#        HOW TO LINK FACEBOOK         #
#         MESSAGES TO WEIO            #
#                                     #
#######################################

# Description: This example shows how to light the LED on board  
#              with different colors using received facebook messages. 
#              All received messages are valids includng messages sended
#              by yourself. Available keys are "red", "green" or "blue".
# WeIO functions: digitalWrite(pin,value) - All pins availables,  
# value is 1 and 0 or LOW and HIGH
#
# Create your facebook app: https://developers.facebook.com/
# Go to Tools -> Graph API Explorer -> Get Access token -> 
# Extended Permissions -> select read_mailbox permission and
# create your access token

from weioLib.weio import *
import urllib2, json

def setup():
    attach.process(myProcess)

def myProcess():
    
    print("Starting Facebook dialog")
    
    # Your access token 
    accessToken = " < HERE YOUR ACCESS TOKEN >"
    # Inbox url requiring access token
    url = "https://graph.facebook.com/me/inbox?access_token="+accessToken

    # Create infinite loop to check inbox messages
    while True:
        # get inbox data from url
        inbox = urllib2.urlopen(url).read()
        # transform string data in JSON python format
        jsonData = json.loads(inbox)
        # get messages from jsonData
        messages = jsonData["data"][0]["comments"]["data"]
        # get last received message
        color = messages[-1]["message"]

        # print last received message on the console
        print "Last received message :", color
        
        # write coresponding digital values to pins
        if color == "red":
            digitalWrite(18,LOW)
            digitalWrite(19,HIGH)
            digitalWrite(20,HIGH)
            
        if color == "green":
            digitalWrite(18,HIGH)
            digitalWrite(19,LOW)
            digitalWrite(20,HIGH)
            
        if color == "blue":
            digitalWrite(18,HIGH)
            digitalWrite(19,HIGH)
            digitalWrite(20,LOW)            
         
        # wait 5 seconds ( To not exceed the rate limit of calls)    
        delay(5000)