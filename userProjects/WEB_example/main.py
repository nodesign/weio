from weioLib import weio
import time

# Simple standalone application with web interface
# One button is present in browser, when user touches button
# buttonHandler callback will be called on the server side
# 
# Push method will push one incrimented number every second to
# the browser. ButtonHandler will restart counter
    
###
# Event Handlers
###
def buttonHandler(dataIn) :
    print "FROM BROWSER: ", dataIn
    weio.shared.numbers = 0
    
    
    
def push():
    weio.shared.numbers = 0
    
    while(1):
        if (weio.shared.websocketOpened) :
            print len(weio.shared.connectedClients)
            a = weio.shared.numbers
            print "COUNTING...", a  
            firstConnected = weio.shared.connectedClients[0]
            firstConnected.emit("userMsg",a)
            
            time.sleep(0.5)
            weio.shared.numbers+=1
        else :
            time.sleep(0.1)
            
            
# Attaches interrupt from Web client to "message" string
weio.attach.event('message', buttonHandler)

# Attaches event from server to browser
weio.attach.process(push)