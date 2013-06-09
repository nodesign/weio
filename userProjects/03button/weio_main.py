# Example of button interrupt

BUTTON_PIN = 0

def setup() :
    
    # tells that button is on pin 1
    pinMode(BUTTON_PIN, INPUT) 
    
    # Attaches interrupt when button is HIGH, positive voltage
    attach.interrupt(BUTTON_PIN, HIGH, onButtonPressed)
    
    # Attaches interrupt on falling edge
    attach.interrupt(BUTTON_PIN, FALLING, onButtonReleased)

def onButtonPressed(): 
    print "button is pressed"


def onButtonReleased() :
    print "button released" 


runWeio()