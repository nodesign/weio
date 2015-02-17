#######################################
#                                     #
#        HOW TO LINK TWITTER          #
#         MESSAGES TO WEIO            #
#                                     #
#######################################

# Description : This example shows how to turns on the LED on differrents
#               colors using twitter direct messages.
#               weio_red message turns LED on red
#               weio_green message turns LED on green
#               weio_blue message turns LED on blue 

# Create your app here: 
# https://apps.twitter.com/
# Set Read, Write and Access direct messages here:
# https://apps.twitter.com/app/7901200/permissions
# Get keys here: 
# apphttps://apps.twitter.com/app/7901200/keys

from weioLib.weio import *
from birdy.twitter import *

def setup():
    attach.process(twi)
    
def twi():    
    APP_KEY = 'YOUR APP KEY'
    APP_SECRET = 'YOUR APP SECRET'
    OAUTH_TOKEN = 'YOUR OAUTH TOKEN'
    OAUTH_TOKEN_SECRET = 'YOUR OAUTH TOKEN SECRET'
    
    client = UserClient(APP_KEY,
                        APP_SECRET,
                        OAUTH_TOKEN,
                        OAUTH_TOKEN_SECRET)
    
    while True:
        #userTimeline = client.api.statuses.user_timeline.get()
        try :
            directMsg = client.api.direct_messages.get()
            msg = directMsg.data[0]['text']
            
            print "Last direct message received :", msg
    
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
                
        except TwitterApiError, e:
            print e

        delay(60000)    