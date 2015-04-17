#######################################
#                                     #
#  HOW TO LINK UNSEEN MAILS TO WEIO   #
#         USING IMAP LIBRARY          #
#                                     #
#######################################

# Description: This example shows how to lights the red LED on board when 
#              there are unseen mails in your inbox folder.
# WeIO functions: digitalWrite(pin,value) - All pins availables, value is 1 
# and 0 or LOW and HIGH
#
# Ensure that your account alow access to less secure apps:
# https://www.google.com/settings/security

from weioLib.weio import *

import imaplib

def setup():
    attach.process(googleInbox)
    
def googleInbox():
    # define imap server, username and password
    server   = 'imap.gmail.com'
    username = '<YOUR MAIL>'
    password = '<YOUR PASSWORD>'

    # connect to server
    account = imaplib.IMAP4_SSL(server, 993)
    # login 
    account.login(username, password)
    # select Inbox folder
    account.select('Inbox')

    # create infinite loop
    while True:
        # search unseen messages
        status, data = account.search(None,'(UNSEEN)')
        # if there are unseen messages lights the red LED
        if data[0] :
            print "UNSEEN MESSAGES"
            digitalWrite(18,LOW)
        else :
            digitalWrite(18,HIGH)
        # wait 2 seconds    
        delay(2000)