#######################################
#                                     #
#        HOW TO LINK TWITTER          #
#      DIRECT MESSAGES TO WEIO        #
#                                     #
#######################################

# Description : This example shows how to turns on the LED in differrent
#               colors according to received twitter direct messages. 
#               It use birdy library (https://github.com/inueni/birdy).
#               -> weio_red message turns LED on red
#               -> weio_green message turns LED on green
#               -> weio_blue message turns LED on blue 

# Instructions: To run this example the first think you need to do is create
#               your twitter application. Then you need to enable permissions
#               to read direct messages. Finally your need to generate keys 
#               and copy in this example. Below corresponding web sites: 
#               -> https://apps.twitter.com/
#               -> https://apps.twitter.com/app/<app number>/permissions
#               -> https://apps.twitter.com/app/<app number>/keys

# Requirements: This example needs birdy library (and his requirements).
#               Esier way to install is to use the pip package manager 
#               (already installed on the board) over ssh. The WeIO Flash
#               memory is to small for that purpose, so we recommend to
#               install this module on an SD card.
#
#               Insert SD card on the board and turn it on. Open your
#               computer command line and connect to WeIO over ssh with 
#               this command : 
#               -> ssh root@<board name>.local
#
#               Once you are logged in you need to create on your SD card a
#               directory tree with name and structure "/pythonExtra/build".
#               On WeIO SD card is mounted as "/weioUser/sd" directory.
#               The "/weioUser/sd/pythonExtra" directory is configured in 
#               "usr/lib/python2.7/site-packages/usrmodules.pth" as external 
#               python packages storage. It will contain birdy library and
#               his requirements. 
#               -> cd ..
#               -> mkdir weioUser/sd/pythonExtra
#               -> mkdir weioUser/sd/pythonExtra/build
#
#               Finally install the library on the SD card with this command:
#               -> pip install --target=/weioUser/sd/pythonExtra
#                  --build=/weioUser/sd/pythonExtra/build birdy               

from weioLib.weio import *
from birdy.twitter import UserClient, TwitterApiError

def setup():
    # attach twitter function to main process
    attach.process(twitter)
    
def twitter():
    # your app keys    
    CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
    CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
    ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
    ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'
    # initialize UserClient class with your app keys
    client = UserClient( CONSUMER_KEY, CONSUMER_SECRET,
                         ACCESS_TOKEN, ACCESS_TOKEN_SECRET )
    
    # create an infinite loop to check received messages
    while True:
        # use exception handler to manage twitter errors
        try :
            # get received direct messages
            directMsg = client.api.direct_messages.get()
            # get text of first list object (last received message)
            msg = directMsg.data[0]['text']
            # print message on the IDE console
            print "Last direct message received :", msg
            # test message to turn on the LED in a color
            if msg == "weio_red" :
                digitalWrite(18, LOW)
                digitalWrite(19, HIGH)
                digitalWrite(20, HIGH)
            if msg == "weio_green" :
                digitalWrite(18, HIGH)
                digitalWrite(19, LOW)
                digitalWrite(20, HIGH)
            if msg == "weio_blue" :
                digitalWrite(18, HIGH)
                digitalWrite(19, HIGH)
                digitalWrite(20, LOW)
        # catch eventual errors      
        except TwitterApiError, e:
            # print error on the IDE console
            print e
        # wait a minute to not exeed twitter API rate limits
        delay(60000)    